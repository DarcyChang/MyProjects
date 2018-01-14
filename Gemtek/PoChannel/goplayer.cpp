#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/msg.h>
#include <sys/stat.h>
#include <malloc.h>
#include <pthread.h>
#include <errno.h>


#include "alidef.h"
#include "goplayer.h"

extern "C"
{
#include <cmdipc.h>
}

#define GOPLAYER_INVALID (-1)

static int qid_send, qid_recv, qid_v_recv;
static int b_exit = 0;
static int protocol_exit = 0;
static pthread_t msgrcv_threadID = 0;
static pthread_t timeout = 1;
static unsigned int create_count = 0;
static unsigned int close_count = 0;
static int total_time = -1;
static int cur_time = -1;
static int play_rate = 1;
static int seekable = -1;
#if 0
static int video_width = 0;
static int video_height = 0;
static int video_framerate = 0;
static int video_bitrate = 0;
#endif
static bool isServerInit = false;
static bool isSetCurSrc = false;
static bool isServerClosed = false;
static unsigned long flag = 0;
static goplayer_stream_info *g_info = NULL;
static goplayer_stream_info *g_cur_info = NULL;
static unsigned long long g_dlSpeed = GOPLAYER_INVALID;
static eGOPLAYER_CALLBACK_TYPE g_cb_type = eGOPLAYER_CBT_NONE;
static stGOPLAYER_MEDIA_TAG *g_media_tag = NULL;

static GOPLAYER_STREAM_CALLBACK g_streamCallback;

#define GOT_METADATA 0x1
#define GOT_TOTALTIME 0x2
#define GOT_SEEKABLE 0x4
#define GOT_CURRENTTIME 0x8
#define GOT_STREAMINFO 0x10
#define GOT_CURSTREAMINFO 0x20
#define GOT_STREAMINFO_F 0x40
#define GOT_CURSTREAMINFO_F 0x80
#define GOT_VIDEOINFO 0x100
#define GOT_DOWNLOAD_SPEED 0x200 
#define GOT_METADATA_F 0x400 
#define GOT_MEDIASIZE 0x800 

//media tag
#define MEDIA_TAG_TITLE "title"
#define MEDIA_TAG_ARTIST "artist"
#define MEDIA_TAG_ALBUM "album"
#define MEDIA_TAG_DATE "date"
#define MEDIA_TAG_COMMENT "comment"
#define MEDIA_TAG_GENRE "genre"
#define MEDIA_TAG_BITRATE "bitrate"

#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#define FBIO_WIN_ONOFF 	0x460017 /* ali_video_common.h */
#define TIMEOUT_SECONDS 10
void controlVideoLayer(int ctl)
{
	int fd = 0;

	fd = open("/dev/fb1", O_RDWR);
	if(fd < 0) {
		printf("Error cannot open framebuffer fb1\n");
		return;
	}
	if(ctl) {
		// open the video layer
		ioctl(fd, FBIO_WIN_ONOFF, 1);
	} else {
		// close the video layer
		ioctl(fd, FBIO_WIN_ONOFF, 0);
		printf("close the video layer\n");
	}
	close(fd);
}


/**
*  @param[in] expectFlag Flags to expect. It can be ORed.
*  @param[in] clearFlag Whether to clear the flags if it has got the flags.
*  @param[in] loopCnt loop count.
*  @param[in] usleepTime sleep time of each loop in us.
*  @return TRUE if all flags in \c expectFlag are set, otherwise return FALSE.
*/
static bool wait_response(unsigned long expectFlag, bool clearFlag, unsigned int loopCnt, unsigned long usleepTime)
{
	bool ret = false;
	for(; loopCnt; loopCnt--)
	{
		if((flag & expectFlag) == expectFlag)
		{
			ret = true;
			break;
		}
		usleep(usleepTime);
	}
	if(clearFlag)
	{
		flag &= ~expectFlag;
	}
	return ret;
}
//message send function : send a message to message queue--> qid_recv
static bool send_message(stMSG_QUE *pmsg_snd, long type, long sub_type, int val, bool clearMsg)
{
    if(clearMsg)
    {
        memset(pmsg_snd, 0, sizeof(stMSG_QUE));
    }
    pmsg_snd->msgtype = type;
    pmsg_snd->subtype = sub_type;
    pmsg_snd->val = val;

    if (msgsnd(qid_send, pmsg_snd, MSG_SIZE, 0) == -1) {
    	perror("msgsnd");
        return false;
    }
    return true;
}

static bool set_http_option(eCMD_TYPE type, char *info)
{
	stMSG_QUE msg_send;
	stVMSG_QUE *vmsg_snd = NULL;
	int msg_length = 0;

	if (isServerInit) {
		/* set Http header with V-Message for variable length */
		msg_length = strlen(info) + sizeof(stVMSG_QUE) + 1;
#if 1
		if(!send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_VMSG, msg_length, true))
		{
			return false;
		}
#else
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_VMSG;
		msg_send.val = msg_length;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
			return false;
		}
#endif
		vmsg_snd = (stVMSG_QUE *)calloc(msg_length, sizeof(stVMSG_QUE)); //length
		vmsg_snd->msgtype = eMSG_TYPE_CMD;
		vmsg_snd->subtype = type;
		vmsg_snd->len = strlen(info) + 1;
		strncpy(vmsg_snd->data, info, strlen(info));
		if (msgsnd(qid_send, vmsg_snd, (msg_length - sizeof(long)), IPC_NOWAIT) == -1) {
			free(vmsg_snd);
			perror("vmsg msgsnd");
			return false;
		}
		free(vmsg_snd);
		return true;
	}

	return false;

}

/*
static void video_info_parse(char *vinfo)
{
	char *pch = NULL;
	const char *delim = ",";

	GOPLAYER_LOG ("video_info_parse: %s\n", vinfo);
	pch = strtok(vinfo, delim);

	while (pch != NULL) {
		if (strstr(pch, "width") != NULL)
			video_width = atoi(strstr(pch, ":")+1);
		else if (strstr(pch, "height") != NULL)
			video_height = atoi(strstr(pch, ":")+1);
		else if (strstr(pch, "framerate") != NULL)
			video_framerate = atoi(strstr(pch, ":")+1);
		else if (strstr(pch, "bitrate:") != NULL)
			video_bitrate = atoi(strstr(pch, ":")+1);
		pch = strtok(NULL, delim);
	}
	if (pch)
		free(pch);
	GOPLAYER_LOG ("video_info_parse: width:%d, height:%d, framerate:%d, bitrate:%d\n", 
		video_width, video_height, video_framerate, video_bitrate);
}
*/
/*
* add detailed audio information to structure stGOPLAYER_AUDIO_TRACK_INFO.
*/
static void addAudDetailInfo(stGOPLAYER_AUDIO_TRACK_INFO *audio_track_info, const char *infoName)
{
	if(!audio_track_info->audDetailInfo)
	{
		audio_track_info->audDetailInfo = \
			(stGOPLAYER_AUDIO_DETAIL_INFO *)calloc(1, sizeof(stGOPLAYER_AUDIO_DETAIL_INFO));
	}
	if(strstr(infoName, "channels") != NULL)
	{
		audio_track_info->audDetailInfo->channels = atoi(strstr(infoName, ":")+1);
	}
	else if(strstr(infoName, "samplerate") != NULL)
	{
		audio_track_info->audDetailInfo->samplerate = atoi(strstr(infoName, ":")+1);
	}
	else if(strstr(infoName, "depth") != NULL)
	{
		audio_track_info->audDetailInfo->depth = atoi(strstr(infoName, ":")+1);
	}
	else if(strstr(infoName, "decoder") != NULL)
	{
		strncpy(audio_track_info->audDetailInfo->decName, strstr(infoName, ":")+1, DECNAME_SIZE);
	}
}

static void stream_info_parse(stVMSG_QUE *vmsg, goplayer_stream_info *info, bool isCurrent)
{
	char *pch = NULL;
	const char *delim = ";";
	char *outer_ptr = NULL;
	char *subpch = NULL;
	const char *subdelim = ",";
	unsigned int count = 0;
	bool cur_init = false;

	GOPLAYER_LOG ("stream_info_parse: %s\n", (char*)vmsg);
	pch = strtok_r(vmsg->data, delim, &outer_ptr);

	while (pch != NULL) {
		GOPLAYER_LOG ("StreamInfo pch of line: %s\n", pch);
		if ((strstr(pch, "StreamNum") != NULL) || (isCurrent && !cur_init)) {
			if (isCurrent) {
				info->count = 1;
				cur_init = true;
			}
			else
				info->count = atoi(strstr(pch, ":")+1);
			if (info->count > 0) {
				switch(info->type) {
					case GOPLAYER_STREAM_INFO_TYPE_AUDIO:
						info->stream_info.audio_track_info = \
							(stGOPLAYER_AUDIO_TRACK_INFO *)calloc(info->count, sizeof(stGOPLAYER_AUDIO_TRACK_INFO));
					break;

					case GOPLAYER_STREAM_INFO_TYPE_SUBTITLE:
						info->stream_info.subtitle_info = \
							(stGOPLAYER_SUBTITLE_INFO *)calloc(info->count, sizeof(stGOPLAYER_SUBTITLE_INFO));
					break;

					case GOPLAYER_STREAM_INFO_TYPE_VIDEO:
						info->stream_info.video_track_info = \
							(stGOPLAYER_VIDEO_TRACK_INFO *)calloc(info->count, sizeof(stGOPLAYER_VIDEO_TRACK_INFO));
					break;

					case GOPLAYER_STREAM_INFO_TYPE_PROGRAM:
						info->stream_info.program_info = \
							(stGOPLAYER_PROGRAM_INFO *)calloc(info->count, sizeof(stGOPLAYER_PROGRAM_INFO));
					break;

					case GOPLAYER_STREAM_INFO_TYPE_CHAPTER:
						info->stream_info.chapter_info = \
							(stGOPLAYER_CHAPTER_INFO *)calloc(info->count, sizeof(stGOPLAYER_CHAPTER_INFO));
					break;

					default:
					break;
				}
			}
			GOPLAYER_LOG ("streamNum: %d in %d type\n", info->count, info->type);
			if (isCurrent)
				continue;
		} else {
			subpch = strtok(pch, subdelim);
			while (subpch != NULL && count < info->count) {
				//GOPLAYER_LOG ("StreamInfo subpch of line: %s\n", subpch);
				switch(info->type)
				{
					case GOPLAYER_STREAM_INFO_TYPE_AUDIO:
					{
						if (strstr(subpch, "TrackIndex") != NULL) {
							info->stream_info.audio_track_info[count].track_index = 
								atoi(strstr(subpch, ":")+1);
							//GOPLAYER_LOG ("[%d]TrackIndex: %d\n", count,
							//	info->stream_info.audio_track_info[count].track_index);
						}
						else if(strstr(subpch, "LanguageCode") != NULL)
						{
							strcpy(info->stream_info.audio_track_info[count].lang_code, 
								strstr(subpch, ":")+1);
							//GOPLAYER_LOG ("[%d]LanguageCode: %s\n", count,
							//	info->stream_info.audio_track_info[count].lang_code);
						}
						else if((strstr(subpch, "channels") != NULL) || 
							(strstr(subpch, "samplerate") != NULL) || 
							(strstr(subpch, "depth") != NULL) || 
							(strstr(subpch, "decoder") != NULL)) //Nick add
						{//only eRESPONSE_TYPE_CUR_STREAM_INFO will enter this branch.
							addAudDetailInfo(&info->stream_info.audio_track_info[count], subpch);
						}
					}
					break;

					case GOPLAYER_STREAM_INFO_TYPE_SUBTITLE:
					{
						if (strstr(subpch, "TrackIndex") != NULL) {
							info->stream_info.subtitle_info[count].track_index = \
								atoi(strstr(subpch, ":")+1);
						}
						else if(strstr(subpch, "LanguageCode") != NULL)
						{
							strcpy(info->stream_info.subtitle_info[count].lang_code, 
								strstr(subpch, ":")+1);
						}
					}
					break;

					case GOPLAYER_STREAM_INFO_TYPE_VIDEO:
					{
						if(strstr(subpch, "fourCC") != NULL)
						{
							memcpy(&info->stream_info.video_track_info->fourCC, 
								strstr(subpch, ":")+1, sizeof(unsigned long));
						}
						else if(strstr(subpch, "width") != NULL)
						{
							info->stream_info.video_track_info->width = atoi(strstr(subpch, ":")+1);
						}
						else if(strstr(subpch, "height") != NULL)
						{
							info->stream_info.video_track_info->height = atoi(strstr(subpch, ":")+1);
						}
						else if(strstr(subpch, "framerate") != NULL)
						{
							info->stream_info.video_track_info->framerate = atoi(strstr(subpch, ":")+1);
						}
					}
					break;

					case GOPLAYER_STREAM_INFO_TYPE_PROGRAM:
					{// not implement currently
						if (strstr(subpch, "TrackIndex") != NULL) {
							info->stream_info.program_info[count].prog_index= \
								atoi(strstr(subpch, ":")+1);
						}
						else if(strstr(subpch, "LanguageCode") != NULL)
						{
						
						}
					}
					break;

					case GOPLAYER_STREAM_INFO_TYPE_CHAPTER:
					{// not implement currently
						if (strstr(subpch, "TrackIndex") != NULL) {
							info->stream_info.chapter_info[count].chaper_index= \
								atoi(strstr(subpch, ":")+1);
						}
						else if(strstr(subpch, "LanguageCode") != NULL)
						{
						
						}
					}
					break;

					default:
					break;
				}
				subpch = strtok (NULL, subdelim);
			}
			count++; /* next stream */
		}
		pch = strtok_r(NULL, delim, &outer_ptr);
	}
	if (pch)
		free(pch);
	if (subpch)
		free(subpch);
}

static int vmsg_proc(stVMSG_QUE *vmsg)
{
	GOPLAYER_LOG("----vmsg proc type=%d, len=%d, st=%d, name=%s----\n",
	(int)vmsg->subtype, (int)vmsg->len, vmsg->val, vmsg->data);

	switch(vmsg->subtype)
	{
		case eRESPONSE_TYPE_STREAM_INFO:
		{
			if (vmsg->val == g_info->type) {
				stream_info_parse(vmsg, g_info, false);
				flag |= GOT_STREAMINFO;
			}
		}
		break;

		case eRESPONSE_TYPE_CUR_STREAM_INFO:
		{
			if (vmsg->val == g_cur_info->type) {
				stream_info_parse(vmsg, g_cur_info, true);
				flag |= GOT_CURSTREAMINFO;
			}
		}
		break;

		default:
		break;
	}
	return 0;
}

static void parse_metadata(const char *key, const char *val)
{
	if (strstr(key, MEDIA_TAG_TITLE) != NULL)
	{
		strncpy(g_media_tag->title, val, TAG_TITLE_SIZE);
	}
	else if (strstr(key, MEDIA_TAG_ARTIST) != NULL)
	{
		strncpy(g_media_tag->artist, val, TAG_ARTIST_SIZE);
	}
	else if (strstr(key, MEDIA_TAG_ALBUM) != NULL)
	{
		strncpy(g_media_tag->album, val, TAG_ALBUM_SIZE);
	}
	else if (strstr(key, MEDIA_TAG_DATE) != NULL)
	{
		strncpy(g_media_tag->date, val, TAG_DATE_SIZE);
	}
	else if (strstr(key, MEDIA_TAG_COMMENT) != NULL)
	{
		strncpy(g_media_tag->comment, val, TAG_COMMENT_SIZE);
	}
	else if (strstr(key, MEDIA_TAG_GENRE) != NULL)
	{
		strncpy(g_media_tag->genre, val, TAG_GENRE_SIZE);
	}
	else if (strstr(key, MEDIA_TAG_BITRATE) != NULL)
	{
		g_media_tag->bitrate = strtol (val, NULL, 10);
	}
}
static void *timeout_thread(void *p)
{
	pthread_detach(pthread_self());
    stMSG_QUE msg_send;       
    memset (&msg_send, 0, sizeof(stMSG_QUE));
    pthread_cond_t cond;      
    pthread_mutex_t mutex;    
    pthread_cond_init(&cond,NULL); 
    pthread_mutex_init(&mutex,NULL);
    pthread_mutex_lock(&mutex);    
    struct timespec to;       
    to.tv_sec = time(0)+TIMEOUT_SECONDS;
    to.tv_nsec = 0;
    int err = pthread_cond_timedwait(&cond, &mutex, &to);

	close_count++;
	unsigned int timeout_thread_count;
	timeout_thread_count = close_count;
    if(err == ETIMEDOUT){
        if(protocol_exit == 0 && create_count == timeout_thread_count){            
            msg_send.msgtype = eMSG_TYPE_ERR; 
            msg_send.subtype = eERR_SUB_UNDEFINE;
			strcpy(msg_send.data1, "timeout"); 
            msgsnd(qid_recv, (stMSG_QUE*)&msg_send, MSG_SIZE, 0);
			goplayer_close();
        }
    }
	pthread_mutex_unlock(&mutex);  
    return 0;
}
static void *msgrcv_thread(void *p)
{
	stMSG_QUE msg_recv;
	bool vmsg_flag = false;
	size_t msg_length = 0;
	void *vmsg_recv = NULL;

	while (!b_exit) {
		if (vmsg_flag) {
			if (msgrcv(qid_v_recv, vmsg_recv, msg_length, 0, 0) == -1) {
				perror("msgrcv");
				GOPLAYER_LOG("---- get vmsg fail %s %d ----\n", __func__, __LINE__);
				continue;
			} else {
				vmsg_proc((stVMSG_QUE *)vmsg_recv);
				vmsg_flag = false;
				free(vmsg_recv);
				vmsg_recv = NULL;
			}
		}

		memset (&msg_recv, 0 , sizeof(stMSG_QUE));
		if (msgrcv(qid_recv, (stMSG_QUE *)&msg_recv, MSG_SIZE, 0, 0) == -1) {
			perror("msgrcv");
			GOPLAYER_LOG("---- get msg fail %s %d ----\n", __func__, __LINE__);
			b_exit = 1;
		}

		if (msg_recv.msgtype == eMSG_TYPE_RESPONSE) {
			if (msg_recv.subtype == eRESPONSE_TYPE_TOTALTIME) {
				total_time = msg_recv.val;
				flag |= GOT_TOTALTIME;
				//GOPLAYER_LOG ("\t---\ttotalTime\t%ds\t---\n", total_time/1000);
			} else if (msg_recv.subtype == eRESPONSE_TYPE_CURRENTTIME) {
				cur_time = msg_recv.val;
				flag |= GOT_CURRENTTIME;
				//GOPLAYER_LOG ("\t***\tcurrentTime\t%ds\t***\n", cur_time/1000);
			} else if (msg_recv.subtype == eRESPONSE_TYPE_ISSEEKABLE) {
				seekable = msg_recv.val;
				flag |= GOT_SEEKABLE;
				//GOPLAYER_LOG ("\t$$$\tSEEKABLE %d\t$$$\n",msg_recv.val);
			} else if (msg_recv.subtype == eRESPONSE_TYPE_FINISHED) { /* Play Finished */
				//added by andrew
				do_command("touch /tmp/replay_ok");
				g_streamCallback(eGOPLAYER_CBT_FINISHED, NULL);
				g_cb_type = eGOPLAYER_CBT_FINISHED;
			} else if (msg_recv.subtype == eRESPONSE_TYPE_STATE_CHANGE) {
				g_streamCallback(eGOPLAYER_CBT_STATE_CHANGE, (void*)msg_recv.val);
				g_cb_type = eGOPLAYER_CBT_STATE_CHANGE;
				if(msg_recv.val == 0 || msg_recv.val == 1) 
					protocol_exit=1; 
			} else if (msg_recv.subtype == eRESPONSE_TYPE_BUFFERING) {
				g_streamCallback(eGOPLAYER_CBT_BUFFERING, (void*)msg_recv.val);
				g_cb_type = eGOPLAYER_CBT_BUFFERING;
				protocol_exit=1; 
				//GOPLAYER_LOG ("\t^^^\tBUFFERING %3d\t^^^\n", msg_recv.val);
			} else if (msg_recv.subtype == eRESPONSE_TYPE_CLOSE) {
				b_exit = 1;
				isServerClosed = true;
			} else if (msg_recv.subtype == eRESPONSE_TYPE_VMSG) {
				vmsg_flag = true;
				msg_length = msg_recv.val;
				vmsg_recv = (stVMSG_QUE *)calloc(msg_length, sizeof(stVMSG_QUE));
				msg_length = (msg_length - sizeof(long));
				GOPLAYER_LOG ("---- vmsg : len=%d ----\n", msg_length);
				if (vmsg_recv == NULL) {
					GOPLAYER_LOG ("---- malloc vmsg error ----\n");
				}
			}
#if 0
			else if (msg_recv.subtype == eRESPONSE_TYPE_VIDEOINFO) {
				video_info_parse(msg_recv.data1);
				flag |= GOT_VIDEOINFO;
			}
#endif
			else if (msg_recv.subtype == eRESPONSE_TYPE_STREAM_INFO_FINISH) {
				flag |= GOT_STREAMINFO_F;
				GOPLAYER_LOG("GOT_STREAMINFO_F\n");
			} else if (msg_recv.subtype == eRESPONSE_TYPE_CUR_STREAM_INFO_FINISH) {
				flag |= GOT_CURSTREAMINFO_F;
				GOPLAYER_LOG("GOT_CURSTREAMINFO_F\n");
			}else if(msg_recv.subtype == eRESPONSE_TYPE_DOWNLOAD_SPEED) {
				if(msg_recv.val)
				{
					g_dlSpeed = strtoll (msg_recv.data1, NULL, 10);
				}
				else
				{
					g_dlSpeed = GOPLAYER_INVALID;
				}
				flag |= GOT_DOWNLOAD_SPEED;
				GOPLAYER_LOG("GOT_DOWNLOAD_SPEED\n");
			}else if(msg_recv.subtype == eRESPONSE_TYPE_METADATA)	{
				parse_metadata(msg_recv.data1, msg_recv.data2);
				flag |= GOT_METADATA;
				GOPLAYER_LOG("GOT_METADATA\n");
			}else if(msg_recv.subtype == eRESPONSE_TYPE_METADATA_FINISHED) {
				flag |= GOT_METADATA_F;
				GOPLAYER_LOG("GOT_METADATA_F\n");
			}else if(msg_recv.subtype == eRESPONSE_TYPE_GET_MEDIA_SIZE) {
				if(msg_recv.val)
				{
					g_info->stream_info.mediaSize = strtoll (msg_recv.data1, NULL, 10);
				}
				else
				{
					g_info->stream_info.mediaSize = GOPLAYER_INVALID;
				}
				flag |= GOT_MEDIASIZE;
				GOPLAYER_LOG("GOT_MEDIASIZE\n");			
			}else if(msg_recv.subtype == eRESPONSE_TYPE_FRAME_CAPTURE) {
				if(msg_recv.val)
				{
					g_streamCallback(eGOPLAYER_CBT_FRAME_CAPTURE, (void*)msg_recv.data1);
					g_cb_type = eGOPLAYER_CBT_FRAME_CAPTURE;
				}
				else
					GOPLAYER_LOG ("---- frame capture failed ----\n");
			}
		} else if (msg_recv.msgtype == eMSG_TYPE_WARNING) {
			/* player transitions from rewind state to beginning of stream state */
			if (msg_recv.subtype == eWARN_SUB_UNSUPPORT_AUDIO) {
				g_streamCallback(eGOPLAYER_CBT_WARN_UNSUPPORT_AUDIO, (void*)msg_recv.data1);
				g_cb_type = eGOPLAYER_CBT_WARN_UNSUPPORT_AUDIO;
			} else if (msg_recv.subtype == eWARN_SUB_UNSUPPORT_VIDEO) {
				g_streamCallback(eGOPLAYER_CBT_WARN_UNSUPPORT_VIDEO, (void*)msg_recv.data1);
				g_cb_type = eGOPLAYER_CBT_WARN_UNSUPPORT_VIDEO;
			} else if (msg_recv.subtype == eWARN_SUB_DECODE_ERR_AUDIO) {
				g_streamCallback(eGOPLAYER_CBT_WARN_DECODE_ERR_AUDIO, (void*)msg_recv.data1);
				g_cb_type = eGOPLAYER_CBT_WARN_DECODE_ERR_AUDIO;
			} else if (msg_recv.subtype == eWARN_SUB_DECODE_ERR_VIDEO) {
				g_streamCallback(eGOPLAYER_CBT_WARN_DECODE_ERR_VIDEO, (void*)msg_recv.data1);
				g_cb_type = eGOPLAYER_CBT_WARN_DECODE_ERR_VIDEO;
			} else if (msg_recv.subtype == eWARN_SUB_TRICK_BOS) {
				g_streamCallback(eGOPLAYER_CBT_WARN_TRICK_BOS, NULL);
				g_cb_type = eGOPLAYER_CBT_WARN_TRICK_BOS;
				//GOPLAYER_LOG ("g_streamCallback eGOPLAYER_CBT_WARN_TRICK_BOS\n");
			} else if (msg_recv.subtype == eWARN_SUB_TRICK_EOS) {
				g_streamCallback(eGOPLAYER_CBT_WARN_TRICK_EOS, NULL);
				g_cb_type = eGOPLAYER_CBT_WARN_TRICK_EOS;
				//GOPLAYER_LOG ("g_streamCallback eGOPLAYER_CBT_WARN_TRICK_EOS\n");
			}
		} else if (msg_recv.msgtype == eMSG_TYPE_EOS) {
			//added by andrew
			do_command("touch /tmp/replay_ok");

			g_streamCallback(eGOPLAYER_CBT_FINISHED, NULL);
			g_cb_type = eGOPLAYER_CBT_FINISHED;
		} else if (msg_recv.msgtype == eMSG_TYPE_ERR) {
			switch (msg_recv.subtype)
			{
				case eERR_SUB_SOUP_HTTP:
					g_streamCallback(eGOPLAYER_CBT_ERR_SOUPHTTP, (void*)msg_recv.val);
					g_cb_type = eGOPLAYER_CBT_ERR_SOUPHTTP;
					break;
				case eERR_SUB_TYPE_NOT_FOUND:
					g_streamCallback(eGOPLAYER_CBT_ERR_TYPE_NOT_FOUND, (void*)msg_recv.data1);
					g_cb_type = eGOPLAYER_CBT_ERR_TYPE_NOT_FOUND;
					break;
				case eERR_SUB_DEMUX:
					g_streamCallback(eGOPLAYER_CBT_ERR_DEMUX, (void*)msg_recv.data1);
					g_cb_type = eGOPLAYER_CBT_ERR_DEMUX;
					break;
				default:
					g_streamCallback(eGOPLAYER_CBT_ERR_UNDEFINED, (void*)msg_recv.data1);
					g_cb_type = eGOPLAYER_CBT_ERR_UNDEFINED;
					break;
			}
			GOPLAYER_LOG ("goplayer occur ERROR: Close & Re-init, (%s)\n",msg_recv.data1);
		} else if (msg_recv.msgtype == 0xffff) /* thread error handle avoid deadlock */
			b_exit = 1;
	}

	if (msgctl(qid_recv, IPC_RMID, NULL) == -1)
		perror("msgctl");
	if (msgctl(qid_v_recv, IPC_RMID, NULL) == -1)
		perror("msgctl");

	return 0;
}


int goplayer_open(GOPLAYER_STREAM_CALLBACK streamCallback)
{
	unsigned long cnt = 0;
	time_t timec = {0};
	stMSG_QUE msg_recv;
	char launch_cmd[40];
	//struct stat sb;

	/* Kill player_server_streaming if exists */
	sprintf (launch_cmd, "killall player_server_streaming");
	do_command (launch_cmd);

#if 0  // Check sever binary exist or not
	sprintf (launch_cmd, "/ufs/bin/player_server_streaming");
	if (stat(launch_cmd, &sb) != 0) {
		perror("stat");
		GOPLAYER_LOG ("===Can not find player_server_streaming===\n");
		return -1;
	}
#endif

	sprintf (launch_cmd, "player_server_streaming&");
	if (do_command (launch_cmd) != 0) {
		perror("do_command");
		GOPLAYER_LOG ("===Can not launch player_server_streaming===\n");
		return -1;
	}

	if ((qid_recv = msgget(KEY_CLIENT, 0644 | IPC_CREAT)) == -1) {
		perror("msgget");
		GOPLAYER_LOG ("===Can not create msg queue CLIENT===\n");
		return -1;
	}

	if ((qid_v_recv = msgget(KEY_V_CLIENT, 0644 | IPC_CREAT)) == -1) {
		perror("msgget");
		GOPLAYER_LOG ("===Can not create Vmsg queue CLIENT===\n");
		return -1;
	}
	GOPLAYER_LOG ("receiver: ready to receive messages, qid_recv = %d \n", qid_recv);

	for(;;) {
		GOPLAYER_LOG ("[%s(%d)][%s] msgrcv before ..\n", __FILE__, __LINE__, __func__);
		if (msgrcv(qid_recv, (stMSG_QUE *)&msg_recv, MSG_SIZE, 0, 0) == -1) {
			perror("msgrcv");
		}
		GOPLAYER_LOG ("[%s(%d)][%s] msgrcv after !\n", __FILE__, __LINE__, __func__);
		if (msg_recv.msgtype == eMSG_TYPE_RESPONSE && 
			msg_recv.subtype == eRESPONSE_TYPE_OPEN) {
			if ((qid_send = msgget(KEY_SERVER, 0644)) == -1) {
				perror("msgget");
				GOPLAYER_LOG ("===Can not access msg queue SERVER===\n");
				return -1;
			}
			GOPLAYER_LOG ("connect success, qid_send = %d\n", qid_send);
			time_t timep;
			time(&timep);
			GOPLAYER_LOG ("\t\t%10lu\t%s %f\n",cnt++,ctime(&timep), difftime(timep,timec));
			timec=timep;
			break;
		}else if (msg_recv.msgtype == eMSG_TYPE_RESPONSE && 
			msg_recv.subtype == eRESPONSE_TYPE_CLOSE) {
			GOPLAYER_LOG ("connect fail !! (return -1)\n");
			return -1;
		}
	}
	/* Set for re-entry */
	b_exit = 0;
	protocol_exit=0;
	g_streamCallback = streamCallback;
	if (pthread_create(&msgrcv_threadID, NULL, msgrcv_thread, (void*)0) != 0) {
		GOPLAYER_LOG ("Create msgrcv_thread FAIL !!!\n");
		return -1;
	}
	flag = 0;
	cur_time = -1;
	play_rate = 1;
	isServerInit = true;
	isSetCurSrc = false;
	isServerClosed = false;
	g_cb_type = eGOPLAYER_CBT_NONE;
	return 0;
}


int goplayer_close()
{
	stMSG_QUE msg_send;
	int i, msg_ret;
	char launch_cmd[40];
	if (isServerInit) {
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_CLOSE;
		msg_ret = msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0);
		/* Reset player status */
		flag = 0;
		cur_time = -1;
		play_rate = 1;
		isServerInit = false;
		isSetCurSrc = false;
		/* Check server close response */
		if (msg_ret != -1) {
			GOPLAYER_LOG ("[%s(%d)][%s]", __FILE__, __LINE__, __func__);
			for (i=0; i<60; i++) {
				printf(".");
				if (isServerClosed) {
					pthread_join(msgrcv_threadID, NULL);
					isServerClosed = false;
					g_cb_type = eGOPLAYER_CBT_NONE;
					printf("\n");
					if(i > 20){
						GOPLAYER_LOG ("[%s(%d)][%s] #### WARNING #### It takes over 1 sec to close goplayer (i=%d)!!\n", 
							__FILE__, __LINE__, __func__, i);
					}
					GOPLAYER_LOG ("Player Server Close Success !!!\n");
					return 0;
				}
				usleep(50000);
			}
			printf("\n");
		} else {
			perror("msgsnd");
			GOPLAYER_LOG ("[%s @ %d]: Send eCMD_TYPE_CLOSE Fail !!!\n", __FUNCTION__, __LINE__);
		}
		/* force close msgrcv_thread when server abnormal */
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = 0xffff;
		msgsnd(qid_recv, (stMSG_QUE*)&msg_send, MSG_SIZE, 0);
		pthread_join(msgrcv_threadID, NULL);
		/* Force Kill player_server_streaming */
		sprintf (launch_cmd, "killall player_server_streaming");
		do_command (launch_cmd);
		GOPLAYER_LOG ("[%s(%d)][%s] Force Kill Player Server !!! (wait server response timeout)\n", __FILE__, __LINE__, __func__);
		controlVideoLayer(0);
		GOPLAYER_LOG ("[%s(%d)][%s] do controlVideoLayer(0)!!\n", __FILE__, __LINE__, __func__);
	}

	return 0;
}


void goplayer_set_buffering_time(unsigned int time, 
	unsigned int low_percent, unsigned int high_percent)
{
	stMSG_QUE msg_send;

	/* set buffering */
#if 1
	send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_SET_MAX_BUFFERING_TIME, time, true);
#else	
	memset (&msg_send,0,sizeof(stMSG_QUE));
	msg_send.msgtype = eMSG_TYPE_CMD;
	msg_send.subtype = eCMD_TYPE_SET_MAX_BUFFERING_TIME;
	msg_send.val = time; // 20s
	if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1)
		perror("msgsnd");
#endif
#if 1
	send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_SET_BUFFERING_HIGH_PERCENT, high_percent, true);
#else
	memset (&msg_send,0,sizeof(stMSG_QUE));
	msg_send.msgtype = eMSG_TYPE_CMD;
	msg_send.subtype = eCMD_TYPE_SET_BUFFERING_HIGH_PERCENT;
	msg_send.val = high_percent; /* 15% (20s x 15% = 3s) */
	if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1)
		perror("msgsnd");
#endif
#if 1
	send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_SET_BUFFERING_LOW_PERCENT, low_percent, true);
#else
	memset (&msg_send,0,sizeof(stMSG_QUE));
	msg_send.msgtype = eMSG_TYPE_CMD;
	msg_send.subtype = eCMD_TYPE_SET_BUFFERING_LOW_PERCENT;
	msg_send.val = low_percent; /* 3% (20s x 3% = 0.6s) */
	if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1)
		perror("msgsnd");
#endif
}

void goplayer_set_frame_capture_mode()
{
	stMSG_QUE msg_send;
	send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_SET_FRAME_CAPTURE, 0, true);
}
bool goplayer_set_source_uri(const char *uri, unsigned int start_time)
{
	stMSG_QUE msg_send;
	stVMSG_QUE *vmsg_snd = NULL;
	int msg_length = 0;

	if (isServerInit) {
		/* set CurrentSource with V-Message for variable and long URL */
		msg_length = strlen(uri) + sizeof(stVMSG_QUE) + 1;
#if 1
		if(!send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_VMSG, msg_length, true))
		{
			return false;
		}
#else		
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_VMSG;
		msg_send.val = msg_length;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
			return false;
		}
#endif
		vmsg_snd = (stVMSG_QUE *)calloc(msg_length, sizeof(stVMSG_QUE)); //length
		vmsg_snd->msgtype = eMSG_TYPE_CMD;
		vmsg_snd->subtype = eCMD_TYPE_SET_CURRENTSOURCE;
		vmsg_snd->len = strlen(uri) + 1;
		vmsg_snd->val = start_time;
		strncpy(vmsg_snd->data, uri, strlen(uri));
		if (msgsnd(qid_send, vmsg_snd, (msg_length - sizeof(long)), IPC_NOWAIT) == -1) {
			free(vmsg_snd);
			return false;
		}
		free(vmsg_snd);
		isSetCurSrc = true;

		if(pthread_create(&timeout, NULL, timeout_thread, NULL) != 0) {
            GOPLAYER_LOG ("Create timeout_thread FAIL !!!\n");
            return -1;  
        }
        create_count++;

		return true;
	}

	return false;
}


bool goplayer_play(int rate)
{
	stMSG_QUE msg_send;

	if (isServerInit && isSetCurSrc) {
#if 1
		int subtype;
		if(0 == rate)
			subtype = eCMD_TYPE_PAUSE;
		else
			subtype = eCMD_TYPE_PLAY;
		if(!send_message(&msg_send, eMSG_TYPE_CMD, subtype, rate, true))
		{
			return false;
		}
#else
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		if (0 == rate)
			msg_send.subtype = eCMD_TYPE_PAUSE;
		else
			msg_send.subtype = eCMD_TYPE_PLAY;
		msg_send.val = rate;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
			return false;
		}
#endif
		play_rate = rate;
		return true;
	}
	return false;
}


int goplayer_get_total_time()
{
	stMSG_QUE msg_send;
//	int i;

	if ((flag & GOT_TOTALTIME) && total_time != -1)
		return total_time;
	if (isSetCurSrc) {
#if 1
		if(!send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_TOTALTIME, 0, true))
		{
			return -1;
		}
#else		
//		flag &= ~GOT_TOTALTIME;
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_TOTALTIME;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
			return -1;
		}
#endif
#if 1
		if(wait_response(GOT_TOTALTIME, true, 10, 10000))
		{
			return total_time;
		}
#else
		for (i=0; i<10; i++) {
			if (flag & GOT_TOTALTIME)
				return total_time;
			usleep(10000);
		}
#endif
	}

	return -1;
}


int goplayer_get_current_time()
{
	stMSG_QUE msg_send;
//	int i;

	if (isSetCurSrc) {
		/* Avoid to get (current time + 1) in pause state */
		if (0 == play_rate)
			return cur_time;
#if 1
		if(!send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_CURRENTTIME, 0, true))
		{
			return -1;
		}
#else
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_CURRENTTIME;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
			return -1;
		}
#endif
#if 1		
		wait_response(GOT_CURRENTTIME, true, 10, 10000);
#else
		for (i=0; i<10; i++) {
			if (flag & GOT_CURRENTTIME) {
				flag &= ~GOT_CURRENTTIME;
				return cur_time;
			}
			usleep(10000);
		}
#endif
		return cur_time;
	}

	return -1;
}


int goplayer_is_seekable()
{
	stMSG_QUE msg_send;
//	int i;

	if (isSetCurSrc) {
		/* Check if Seekable */
		if (flag & GOT_SEEKABLE){
			return seekable;
		}else {
#if 1
			if(!send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_ISSEEKABLE, 0, true))
			{
				return -1;
			}
#else			
			memset (&msg_send, 0, sizeof(stMSG_QUE));
			msg_send.msgtype = eMSG_TYPE_CMD;
			msg_send.subtype = eCMD_TYPE_ISSEEKABLE;
			if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
				perror("msgsnd");
				return -1;
			}
#endif
#if 1
			if(wait_response(GOT_SEEKABLE, false, 100, 10000))
			{
				return seekable;
			}
#else
			for (i=0; i<10; i++) {
				if (flag & GOT_SEEKABLE)
					return seekable;
				usleep(10000);
			}
#endif
		}
	}
	GOPLAYER_LOG ("\t$$$\t SOURCE URI need set before query SEEKABLE \t$$$\n");

	return -1;
}


void goplayer_set_display_rect(int x, int y, unsigned int width, unsigned int height)
{
	stMSG_QUE msg_send;

	if (isServerInit) {
#if 1
		memset (&msg_send,0,sizeof(stMSG_QUE));
		sprintf (msg_send.data1, "%d:%d:%d:%d", x, y, width, height);
		GOPLAYER_LOG ("setDview: %s\n", msg_send.data1);
		send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_DVIEW, 0, false);
#else	
		memset (&msg_send,0,sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_DVIEW;
		sprintf (msg_send.data1, "%d:%d:%d:%d", x, y, width, height);
		GOPLAYER_LOG ("setDview: %s\n", msg_send.data1);
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1)
			perror("msgsnd");
#endif
	}
}


bool goplayer_seek(double time)
{
	stMSG_QUE msg_send;

	if (isSetCurSrc && goplayer_is_seekable() == 1) {
#if 1
		if(!send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_SEEK, time, true))
		{
			return false;
		}
#else		
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_SEEK;
		msg_send.val = time;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
			return false;
		}
#endif
		GOPLAYER_LOG ("\t$$$\t SEEKTO %.3f\t$$$\n", time/1000);
		return true;
	}

	return false;
}

bool goplayer_seek_forward(double seek_percent)
{
	int seek_current_time, seek_total_time;
	double seek_time;
	
	seek_current_time = goplayer_get_current_time();
	seek_total_time = goplayer_get_total_time();
	seek_time = seek_current_time + (seek_total_time * (seek_percent/100));	
	if(seek_time > seek_total_time)
		seek_time=seek_total_time-1;
	goplayer_seek(seek_time);
	return true;
}

bool goplayer_seek_backward(double seek_percent)
{
	int seek_current_time, seek_total_time;
	double seek_time;

	seek_current_time = goplayer_get_current_time();
	seek_total_time = goplayer_get_total_time();
	seek_time = seek_current_time - (seek_total_time * (seek_percent/100));	
	if(seek_time < 0)
		seek_time=0;
	goplayer_seek(seek_time);
	return true;
}

bool goplayer_get_media_tag(stGOPLAYER_MEDIA_TAG *mediaTag)
{
	bool ret = false;
	if(isSetCurSrc)
	{
		stMSG_QUE msg_send;
		g_media_tag = mediaTag;
		memset (g_media_tag, 0, sizeof(stGOPLAYER_MEDIA_TAG));
		if(send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_METADATA, 0, true))
		{
			if(wait_response(GOT_METADATA | GOT_METADATA_F, true, 10, 10000))
			{
				ret = true;
#if 0
				printf("\033[22;32m""%s=%s\n""\033[0m", MEDIA_TAG_TITLE, g_media_tag->title);
				printf("\033[22;32m""%s=%s\n""\033[0m", MEDIA_TAG_ARTIST, g_media_tag->artist);
				printf("\033[22;32m""%s=%s\n""\033[0m", MEDIA_TAG_ALBUM, g_media_tag->album);
				printf("\033[22;32m""%s=%s\n""\033[0m", MEDIA_TAG_DATE, g_media_tag->date);
				printf("\033[22;32m""%s=%s\n""\033[0m", MEDIA_TAG_COMMENT, g_media_tag->comment);
				printf("\033[22;32m""%s=%s\n""\033[0m", MEDIA_TAG_GENRE, g_media_tag->genre);
				printf("\033[22;32m""%s=%lu\n""\033[0m", MEDIA_TAG_BITRATE, g_media_tag->bitrate);
#endif
			}
		}
	}
	return ret;
}
bool goplayer_get_stream_info(eGOPLAYER_STREAM_INFO_TYPE type, goplayer_stream_info **info)
{
	stMSG_QUE msg_send;
//	int i;

	if (isSetCurSrc) {
		*info = (goplayer_stream_info *)calloc(1, sizeof(goplayer_stream_info));
		g_info = *info;
		g_info->type = type;
		if(type == GOPLAYER_STREAM_INFO_TYPE_MEDIA_SIZE)
		{
			if(send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_GET_MEDIA_SIZE, 0, true))
			{
				if(wait_response(GOT_MEDIASIZE, true, 10, 10000))
				{
					if(g_info->stream_info.mediaSize > 0)
					{
						return true;
					}
				}
			}
			goto HELL;
		}
		else
		{
#if 1		
			if(!send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_STREAM_INFO, 0, true))
			{
				goto HELL;
			}
#else
			memset (&msg_send, 0, sizeof(stMSG_QUE));
			msg_send.msgtype = eMSG_TYPE_CMD;
			msg_send.subtype = eCMD_TYPE_STREAM_INFO;
			if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
				perror("msgsnd");
				return false;
			}
#endif
#if 1
			if(wait_response(GOT_STREAMINFO | GOT_STREAMINFO_F, true, 20, 20000))
			{
				//GOPLAYER_LOG ("goplayer_get_stream_info got stream info at [%d]\n", i);
				if (g_info->count > 0)
					return true;
			}
#else
			for (i=0; i<20; i++) {
				if ((flag & GOT_STREAMINFO) && (flag & GOT_STREAMINFO_F)) {
					//GOPLAYER_LOG ("goplayer_get_stream_info got stream info at [%d]\n", i);
					flag &= ~GOT_STREAMINFO;
					flag &= ~GOT_STREAMINFO_F;
					if (g_info->count > 0)
						return true;
					else
						break;
				}
				usleep(20000);
			}
#endif
			GOPLAYER_LOG ("Got none specified stream info !!!\n");
HELL:
			free(*info);
		}
	}

	return false;
}


bool goplayer_get_cur_stream_info(eGOPLAYER_STREAM_INFO_TYPE type, goplayer_stream_info **info)
{
	stMSG_QUE msg_send;
//	int i;

	if (isSetCurSrc) {
		*info = (goplayer_stream_info *)calloc(1, sizeof(goplayer_stream_info));
		g_cur_info = *info;
		g_cur_info->type = type;
#if 1
		if(!send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_CUR_STREAM_INFO, 0, true))
		{
			goto HELL;
		}
#else
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_CUR_STREAM_INFO;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
			return false;
		}
#endif
#if 1
		if(wait_response(GOT_CURSTREAMINFO | GOT_CURSTREAMINFO_F, true, 30, 20000))
		{
			if (g_cur_info->count > 0)
				return true;
		}
#else
		for (i=0; i<20; i++) {
			if ((flag & GOT_CURSTREAMINFO) && (flag & GOT_CURSTREAMINFO_F)) {
				//GOPLAYER_LOG ("goplayer_get_cur_stream_info got current stream info at [%d]\n", i);
				flag &= ~GOT_CURSTREAMINFO;
				flag &= ~GOT_CURSTREAMINFO_F;
				if (g_cur_info->count > 0)
					return true;
				else
					break;
			}
			usleep(20000);
		}
#endif
		GOPLAYER_LOG ("Got none specified current stream info !!!\n");
HELL:
		free(*info);
	}

	return false;
}


bool goplayer_free_stream_info(goplayer_stream_info *info)
{
	if (info) {
		switch(info->type)
		{
			case GOPLAYER_STREAM_INFO_TYPE_AUDIO:
				if(info->stream_info.audio_track_info->audDetailInfo)
				{//free audio detailed info
					free(info->stream_info.audio_track_info->audDetailInfo);
				}
				free(info->stream_info.audio_track_info);
				GOPLAYER_LOG ("goplayer_free_stream_info: audio_track_info\n");
			break;

			case GOPLAYER_STREAM_INFO_TYPE_SUBTITLE:
				free(info->stream_info.subtitle_info);
				GOPLAYER_LOG ("goplayer_free_stream_info: subtitle_info\n");
			break;

			case GOPLAYER_STREAM_INFO_TYPE_VIDEO:
				free(info->stream_info.video_track_info);
				GOPLAYER_LOG ("goplayer_free_stream_info: video_track_info\n");
			break;

			case GOPLAYER_STREAM_INFO_TYPE_PROGRAM:
				free(info->stream_info.program_info);
				GOPLAYER_LOG ("goplayer_free_stream_info: program_info\n");
			break;

			case GOPLAYER_STREAM_INFO_TYPE_CHAPTER:
				free(info->stream_info.chapter_info);
				GOPLAYER_LOG ("goplayer_free_stream_info: chapter_info\n");
			break;

			default:
			break;
		}
		free (info);
		info = NULL;
		return true;
	}
	return false;
}


void goplayer_change_audio(int trackIdx)
{
	stMSG_QUE msg_send;

	if (isSetCurSrc) {
#if 1
		send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_CHANGE_AUDIO, trackIdx, true);
#else		
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_CHANGE_AUDIO;
		msg_send.val = trackIdx;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
		}
#endif
	}
}


void goplayer_change_subtitle(int trackIdx)
{
	stMSG_QUE msg_send;

	if (isSetCurSrc) {
#if 1
		send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_CHANGE_SUBTITLE, trackIdx, true);
#else
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_CHANGE_SUBTITLE;
		msg_send.val = trackIdx;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
		}
#endif
	}
}


bool goplayer_change_prog(int progIdx)
{
	return false;
}


bool goplayer_change_chapter(int chapId)
{
	return false;
}

bool goplayer_get_download_speed(unsigned long long *dlSpeed)
{
	stMSG_QUE msg_send;
	bool ret = false;
	if(isSetCurSrc)
	{
		send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_GET_DOWNLOAD_SPEED, 0, true);
		//wait response
		if(wait_response(GOT_DOWNLOAD_SPEED, true, 10, 10000))
		{
			if(g_dlSpeed != (unsigned long long)GOPLAYER_INVALID)
			{
				*dlSpeed = g_dlSpeed;
				ret = true;
			}
		}
	}
	return ret;		
}
#if 0
//be replaced by goplayer_get_cur_stream_info().
bool goplayer_get_video_info(int *width, int *height, int *framerate, int *bitrate)
{
	stMSG_QUE msg_send;
	int i;

	if (isSetCurSrc) {
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_VIDEOINFO;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
			return false;
		}
		for (i=0; i<10; i++) {
			if (flag & GOT_VIDEOINFO) {
				flag &= ~GOT_VIDEOINFO;
				if(width)
					*width = video_width;
				if(height)
					*height = video_height;
				if(framerate)
					*framerate = video_framerate;
				if(bitrate)
					*bitrate = video_bitrate;
				return true;
			}
			usleep(10000);
		}
	}

	return false;
}
#endif

bool goplayer_set_http_option(char *header_fields)
{
	return set_http_option(eCMD_TYPE_SET_HTTP_HEADERS, header_fields);
}


bool goplayer_set_proxy(char *proxy_info)
{
	return set_http_option(eCMD_TYPE_SET_HTTP_PROXY, proxy_info);
}


bool goplayer_set_authentication(char *auth_info)
{
	return set_http_option(eCMD_TYPE_SET_HTTP_AUTHENTICATION, auth_info);
}


eGOPLAYER_CALLBACK_TYPE goplayer_get_return_status(void)
{
	return g_cb_type;
}


int goplayer_get_cur_play_rate(void)
{
	return play_rate;
}


bool goplayer_set_playready_httpopt(const char *httpopt)
{
	stMSG_QUE msg_send;
	stVMSG_QUE *vmsg_snd = NULL;
	int msg_length = 0;

	if (isServerInit) {
		/* set CurrentSource with V-Message for variable and long URL */
		msg_length = strlen(httpopt) + sizeof(stVMSG_QUE) + 1;
#if 1
		if(!send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_VMSG, msg_length, true))
		{
			return false;
		}
#else
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_VMSG;
		msg_send.val = msg_length;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
			return false;
		}
#endif
		vmsg_snd = (stVMSG_QUE *)calloc(msg_length, sizeof(stVMSG_QUE)); //length
		vmsg_snd->msgtype = eMSG_TYPE_CMD;
		vmsg_snd->subtype = eCMD_TYPE_SET_PLAYREADY_HTTPOPT;
		vmsg_snd->len = strlen(httpopt) + 1;
		strncpy(vmsg_snd->data, httpopt, strlen(httpopt));
		if (msgsnd(qid_send, vmsg_snd, (msg_length - sizeof(long)), IPC_NOWAIT) == -1) {
			free(vmsg_snd);
			return false;
		}
		free(vmsg_snd);
		return true;
	}

	return false;
}


bool goplayer_set_volume(int volume)
{
	char launch_cmd[32];

	printf("set volume number is %d\n",volume);
	sprintf (launch_cmd, "amixer cset numid=2 %d", volume);
	if (do_command (launch_cmd) != 0) {
		perror("do_command");
		GOPLAYER_LOG ("~~~Can not set volume~~~\n");
		return -1;
	}

	return true;
}


int  goplayer_get_volume(void)
{
	char launch_cmd[32];
	FILE *output;
	char buffer[256];
	int vol = -1;

	sprintf (launch_cmd, "amixer cget numid=2");
	GOPLAYER_LOG("Enter goplayer_get_volume\n");
	output = popen(launch_cmd, "r");
	GOPLAYER_LOG("Enter while loop in goplayer_get_volume\n");
	while (fgets(buffer, sizeof(buffer), output)) {
		if (strstr(buffer, ": values=") != NULL) {
			vol = atoi(strstr(buffer, ": values=")+9);
		}
	}
	GOPLAYER_LOG("Leave while loop in goplayer_get_volume\n");
	pclose(output);
	GOPLAYER_LOG("Leave goplayer_get_volume\n");

	return vol;
}


bool goplayer_set_volume_mute(bool b_mute)
{
	char launch_cmd[32];
	int vol_sw = b_mute? 0 : 1;

	sprintf (launch_cmd, "amixer cset numid=1 %d &", vol_sw);
	if (do_command (launch_cmd) != 0) {
		perror("do_command");
		GOPLAYER_LOG ("~~~Can not set volume mute/unmute~~~\n");
		return -1;
	}

	return true;
}


void goplayer_set_brightness(unsigned int grade)
{
	stMSG_QUE msg_send;

	if (isServerInit && isSetCurSrc) {
#if 1
		send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_SET_BRIGHTNESS, grade, true);
#else
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_SET_BRIGHTNESS;
		msg_send.val = grade;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
		}
#endif
	}
}


void goplayer_set_contrast(unsigned int grade)
{
	stMSG_QUE msg_send;

	if (isServerInit && isSetCurSrc) {
#if 1
		send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_SET_CONTRAST, grade, true);
#else
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_SET_CONTRAST;
		msg_send.val = grade;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
		}
#endif
	}
}


void goplayer_set_hue(unsigned int grade)
{
	stMSG_QUE msg_send;

	if (isServerInit && isSetCurSrc) {
#if 1
		send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_SET_HUE, grade, true);
#else
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_SET_HUE;
		msg_send.val = grade;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
		}
#endif
	}
}


void goplayer_set_saturation(unsigned int grade)
{
	stMSG_QUE msg_send;

	if (isServerInit && isSetCurSrc) {
#if 1
		send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_SET_SATURATION, grade, true);
#else
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_SET_SATURATION;
		msg_send.val = grade;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
		}
#endif
	}
}


void goplayer_set_sharpness(unsigned int grade)
{
	stMSG_QUE msg_send;

	if (isServerInit && isSetCurSrc) {
#if 1
		send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_SET_SHARPNESS, grade, true);
#else
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_SET_SHARPNESS;
		msg_send.val = grade;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
		}
#endif
	}
}


void goplayer_set_enhance_default()
{
	stMSG_QUE msg_send;

	if (isServerInit && isSetCurSrc) {
#if 1
		send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_SET_VEDIO_ENHANCE_DEFAULT, 0, true);
#else
		memset (&msg_send, 0, sizeof(stMSG_QUE));
		msg_send.msgtype = eMSG_TYPE_CMD;
		msg_send.subtype = eCMD_TYPE_SET_VEDIO_ENHANCE_DEFAULT;
		if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
			perror("msgsnd");
		}
#endif
	}
}


void goplayer_set_subtitle_display(bool onoff)
{
	stMSG_QUE msg_send;
#if 1
	send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_SET_SUBTITLE_DISPLAY, (int)onoff, true);
#else
	memset (&msg_send, 0, sizeof(stMSG_QUE));
	msg_send.msgtype = eMSG_TYPE_CMD;
	msg_send.subtype = eCMD_TYPE_SET_SUBTITLE_DISPLAY;
	msg_send.val = (int)onoff;
	if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
		perror("msgsnd");
	}
#endif
}

void goplayer_set_video_display(bool onoff)
{
	stMSG_QUE msg_send;
#if 1
	send_message(&msg_send, eMSG_TYPE_CMD, eCMD_TYPE_SET_VIDEO_DISPLAY, (int)onoff, true);
#else
	memset (&msg_send, 0, sizeof(stMSG_QUE));
	msg_send.msgtype = eMSG_TYPE_CMD;
	msg_send.subtype = eCMD_TYPE_SET_VIDEO_DISPLAY;
	msg_send.val = (int)onoff;
	if (msgsnd(qid_send, (stMSG_QUE*)&msg_send, MSG_SIZE, 0) == -1) {
		perror("msgsnd");
	}
#endif
}
