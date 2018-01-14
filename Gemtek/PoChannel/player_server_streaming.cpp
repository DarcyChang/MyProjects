/*
    player server for streaming source
    2011.9.02
    By Allen
*/
#include <string.h>
#include <map>
#include <sys/msg.h>
#include <pthread.h>
#include <malloc.h>
#include "alidef.h"
#include "recorder.h"
#include "streaming_player.h"
#include <stdlib.h>

#define SUPPORT_LINK_FILE


#define FLAG_NEED_TOTALTIME 1
#define FLAG_FINISHED_TOTALTIME 2
#define FLAG_NEED_METADATA 4
#define FLAG_FINISHED_METADATA 8

#define MAX_URL_LENGH 4096
//#define FAULT_HANDLER
//#define ELEMENTS_DEBUG_ENALBE
#define SERVER_INFO_PRINT(fmt, arg...) { \
    g_print(RED_STR"SERVER INFO:"DEFAULT_STR); g_print(fmt,##arg); }
    
#define SERVER_LOG_PRINT(fmt, arg...) { \
    g_print(BLUE_STR"SERVER LOG:"DEFAULT_STR); g_print(fmt,##arg); }

#define SERVER_WARNING_PRINT(fmt, arg...) { \
    g_print(GREEN_HL_STR"SERVER WARNING:"DEFAULT_STR); g_print(fmt,##arg); }

#define SERVER_ERROR_PRINT(fmt, arg...) { \
    g_print(RED_BLANKING_STR"SERVER ERROR:"DEFAULT_STR); g_print(fmt,##arg); }

using namespace std;
static int qid_send;
static int qid_v_send;
static int qid_recv;
static eOPEN_TYPE eAppType;
static GMainLoop *gmainloop;
static CStreamingPlayer *mini_player = NULL;
static CRecorder *recorder = NULL;

static gboolean bIsServerExit = FALSE;

static pthread_mutex_t mutex_start_gst = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t cond_start_gst = PTHREAD_COND_INITIALIZER;

static pthread_mutex_t mutex_has_mission = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t cond_has_mission = PTHREAD_COND_INITIALIZER;

static gboolean bDispatchRunning = FALSE;

static eCMD_TYPE mission_detail = eCMD_TYPE_MAX;
static gchar *play_url = NULL;
static gint start_play_time = 0, seek_pos = 0;

static gchar *info_proxy = NULL;
static gchar *info_request = NULL;
static gchar *info_authentication = NULL;
static gchar *info_dview = NULL;

static gchar *playready_licenseserver = NULL;
static gchar *playready_httpopt = NULL;

static gchar *dlna_protocol = NULL;

static guint low_percent = 0; 
static guint high_percent = 0;
static guint max_buffering_time = 0;

static gint disable_use_seek_for_trick=0;

static unsigned char flag = 0;
static pthread_mutex_t Mutex = PTHREAD_MUTEX_INITIALIZER;
// prevent multiple player instance. 
static pthread_mutex_t mutex_new_player = PTHREAD_MUTEX_INITIALIZER;

#ifdef ELEMENTS_DEBUG_ENALBE
static char gst_debug_info[8][64];
static int debug_num = 0;
#endif
char rec_name[256];
static gboolean redirect = FALSE;
static gchar *subtitle_uri = NULL;
static gboolean bDisplaySubtitle = TRUE;

typedef struct {
	ePLAYER_STATE player_state; 
	pthread_mutex_t mutex_player_state; //mutex for accessing player_state
} PLAYER_STATE;
static PLAYER_STATE player_state;

static STYPE_MAP_T stype_maps[] = {
//audio    
    {MPGPS, ".mpeg"},
    {MPGPS, ".mpg"},
    {MPGTS, ".ts"},
    {MPGTS, ".m2ts"},
    {MKV,   ".mkv"},
    {AVI,   ".avi"},
    {RM,    ".rmvb"},
    {RM,    ".rm"},
    {QTIME, ".mp4"},
    {QTIME, ".mov"},
    {SWF,   ".swf"},
    {FLV,   ".flv"},
    {INVALIDS, NULL}
};

static ePLAYER_STATE get_player_state (void)
{
	ePLAYER_STATE state;
	pthread_mutex_lock (&player_state.mutex_player_state);
	state = player_state.player_state;
	pthread_mutex_unlock (&player_state.mutex_player_state);
	return state;
}

static void set_player_state (ePLAYER_STATE state)
{
	pthread_mutex_lock (&player_state.mutex_player_state);
	player_state.player_state = state;
	pthread_mutex_unlock (&player_state.mutex_player_state);
}

static inline STREAM_TYPE_T get_media_types_by_suffix(gchar *stream_name)
{
    int i = 0;
    gchar *p_suffix = NULL;
    gchar suffix_c='.';
    
    p_suffix = strrchr(stream_name, suffix_c);
    if (!p_suffix) {
        return INVALIDS;
    }
    else {
        SERVER_LOG_PRINT("---- suffix : %s ----\n", p_suffix);
    }
    
    for (i=0;stype_maps[i].name != NULL;i++) {
        if(0 == strncmp(p_suffix, stype_maps[i].name, 
            strlen(stype_maps[i].name))) {
            SERVER_INFO_PRINT("demux name: %s\n", stype_maps[i].name);
            return stype_maps[i].type;
        }
    }
    
    return INVALIDS;
}

/*
    message send function : send a message to message queue--> qid_recv
    return: TRUE: success.
               FALSE: failed.
*/
static gboolean send_message(stMSG_QUE *pmsg_snd, long type, long sub_type, int val, gboolean clearMsg)
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
    	SERVER_ERROR_PRINT("---- send msg error %s %d ----\n", __func__, __LINE__);
        return FALSE;
    }
    return TRUE;
}
/*
    variable length message send function : send a variable length message to message queue
*/
static int send_vMessage(long type, long sub_type, int val, const char *data, long data_len)
{
	stVMSG_QUE *vmsg_snd = NULL;
	long msg_length = sizeof(stVMSG_QUE) + data_len;

	vmsg_snd = (stVMSG_QUE *)g_malloc0(msg_length);//length
	vmsg_snd->msgtype = type;
	vmsg_snd->subtype = sub_type;
	vmsg_snd->val = val;
	vmsg_snd->len = data_len;
	memcpy(vmsg_snd->data, data, data_len);
	
	if (msgsnd(qid_v_send, vmsg_snd, (msg_length - sizeof(long)), 0) == -1)
	{
		perror("msgsnd");
		SERVER_ERROR_PRINT ("\t*** Send vmsg error %s %d ***\n",__FUNCTION__,__LINE__);
	}
	g_free(vmsg_snd);
	return 0;
}
/*
 * Callback function for gstreamer player to notify APP
 * @ object (in) : un-use
 * @ type (in) : callback type
 * @ data (in) : un-use
 */
 static void cb_rec_funcforAP(gpointer object, eCB_RECORD_TYPE type, gpointer data)
{
	if (type == eCB_RECORD_TYPE_FILENAME)
	{
/*		stMSG_QUE msg = {0};
		msg.msgtype = eMSG_TYPE_CMD;
		msg.subtype = eCMD_TYPE_START_RECORD;
		strncpy(msg.data1, (char*)data, strlen((char*)data));
		msgsnd(qid_recv, (stMSG_QUE*)&msg, MSG_SIZE, 0);
*/
		strncpy(rec_name, "file://", 7);
		strncpy(rec_name+7, (char*)data, strlen((char*)data));
		g_print ("recive filename %s\n", rec_name);
	}
	else if(type == eCB_RECORD_TYPE_WARNING)
	{
		//g_print (L_RED_STR"Warning : %s\n"DEFAULT_STR,(char*)data);
	}
	else if (type == eCB_RECORD_TYPE_ERR)
	{
		g_print ("Error %s\n",(char*)data);
		g_print ("So, exit process\n");
		g_main_loop_quit (gmainloop);
	}

}
static gint getSoupHttpStatusCode(const gchar *data)
{
	const gchar *strTmp, *strTmp1;
	gint statusCode = -1;
	//A souphttpsrc error format is something like
	//("%s, Status Code:%d, URL: %s", msg->reason_phrase, msg->status_code, src->location)
	//ex.Cannot connect to destination (202.153.202.4), Status Code:4, URL: http://202.153.202.4/TERRY_FATOR_Title_2.avi
	if((strTmp = g_strrstr(data, "Status Code:")))
	{
		gchar *StrNum;  //a holder of status code.
		strTmp += sizeof("Status Code:") -1; //go to alphanumeric.
		if((strTmp1 = g_strstr_len(strTmp, 4, ",")) == NULL)
		{
			goto HELL;		
		}
		StrNum = g_strndup(strTmp, strTmp1 - strTmp);
		statusCode = (gint)g_ascii_strtoull(StrNum, NULL, 10);
		g_free(StrNum);	
	}
	else if((strTmp = g_strrstr(data, "libsoup status code ")))
	{
		strTmp += sizeof("libsoup status code ") -1; //go to alphanumeric.
		statusCode = (gint)g_ascii_strtoull(strTmp, NULL, 10);
	}
HELL:	
	return statusCode;
}
#if 0
/**
* According error msg from pipeline, parse error subtype.
*/
static eERR_SUB_TYPE parsing_err_subtype(const gchar *data)
{
	eERR_SUB_TYPE errSubtype = eERR_SUB_UNDEFINE;
	if(!data)
		goto err;
	if(g_strstr_len(data, sizeof("souphttpsrc:") - 1, "souphttpsrc:"))
	{
		errSubtype = eERR_SUB_SOUP_HTTP;
	}
err:
	return errSubtype;
}
#endif
/*
 * Callback function for gstreamer player to notify APP
 * @ object (in) : un-use
 * @ type (in) : callback type
 * @ data (in) : un-use
 */
static stMSG_QUE msg_server_cb;
static void cb_funcforAP(gpointer object, eCB_TYPE type, gpointer data)
{
	stMSG_QUE *pmsg_send = NULL;
    
    pmsg_send = &msg_server_cb;
	memset (pmsg_send, 0, sizeof(stMSG_QUE));

    switch (type)
    {
        case eCB_TYPE_UPDATESTREAMINFO:
        {
			pthread_mutex_lock (&Mutex);
			if (flag & FLAG_NEED_METADATA)
			{
				medadata_map metaData;
				metaData = mini_player->metaData();
				medadata_map::iterator it;
				for (it=metaData.begin(); it!=metaData.end(); it++)
				{
#if 1
					if (strlen(it->second.c_str()) < 200)
					{
						memset (pmsg_send, 0, sizeof(stMSG_QUE));
						memcpy (pmsg_send->data1,it->first.c_str(),strlen(it->first.c_str()));
						memcpy (pmsg_send->data2,it->second.c_str(),strlen(it->second.c_str()));
						if(!send_message(pmsg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_METADATA, 0, FALSE))
						{
							g_print ("\t*** Send msg error %s %d ***\n",__FUNCTION__,__LINE__);
						}
					}
					else
						g_print ("\t@^@^@\ttag [ %s ] content too large\t\n",it->first.c_str());
#else					
					memset (pmsg_send, 0, sizeof(stMSG_QUE));
					pmsg_send->msgtype = eMSG_TYPE_RESPONSE;
					pmsg_send->subtype = eRESPONSE_TYPE_METADATA;
					//g_print ("\t%s\t%s\n",it->first.c_str(), it->second.c_str());
					if (strlen(it->second.c_str()) < 200)
					{
						memcpy (pmsg_send->data1,it->first.c_str(),strlen(it->first.c_str()));
						memcpy (pmsg_send->data2,it->second.c_str(),strlen(it->second.c_str()));
						if (msgsnd(qid_send, (stMSG_QUE *)pmsg_send, MSG_SIZE, 0) == -1)
						{
							perror("msgsnd");
							g_print ("\t*** Send msg error %s %d ***\n",__FUNCTION__,__LINE__);
						}
					}
					else
						g_print ("\t@^@^@\ttag [ %s ] content too large\t\n",it->first.c_str());
#endif
				}
#if 1
				if(!send_message(pmsg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_METADATA_FINISHED, 0, TRUE))
				{
					g_print ("\t*** Send msg error %s %d ***\n",__FUNCTION__,__LINE__);
				}
#else
				memset (pmsg_send, 0, sizeof(stMSG_QUE));
				pmsg_send->msgtype = eMSG_TYPE_RESPONSE;
				pmsg_send->subtype = eRESPONSE_TYPE_METADATA_FINISHED;
				if (msgsnd(qid_send, (stMSG_QUE *)pmsg_send, MSG_SIZE, 0) == -1)
				{
					perror("msgsnd");
					g_print ("\t*** Send msg error %s %d ***\n",__FUNCTION__,__LINE__);
				}
#endif
			}
			flag |= FLAG_FINISHED_METADATA;
			pthread_mutex_unlock (&Mutex);
            SERVER_LOG_PRINT("---- %s total time -----\n", __func__);
        }
        break;
            
        case eCB_TYPE_STATE_CHANGE:
        {
#if 1
	    int val = -1;
            GstState cur_state = *((GstState *)data);
    	    if (GST_STATE_PAUSED == cur_state) {
                SERVER_INFO_PRINT("---- forcetv player state paused ----\n");
		val = ePLAYER_STATE_PAUSE;
            } else if (GST_STATE_PLAYING == cur_state) {
                SERVER_INFO_PRINT("---- forcetv player state playing ----\n");
		val = ePLAYER_STATE_PLAY;
            } else if (GST_STATE_NULL== cur_state
                || GST_STATE_READY== cur_state) {
                SERVER_INFO_PRINT("---- forcetv player state stopped ----\n");
		val = ePLAYER_STATE_STOP;
            } else { 
                SERVER_WARNING_PRINT("---- unknown state ----\n");
            }
            if(val != -1)
            {
		//state changed. Set it.
		set_player_state((ePLAYER_STATE)val);
            }
            if (-1 != val) {
                SERVER_INFO_PRINT("++++ forcetv player send STATECHANGE to UI ---\n");
                if(!send_message(pmsg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_STATE_CHANGE, val, TRUE)) //Nick add
                {
                    SERVER_ERROR_PRINT ("---- Send msg error %s %d ----\n" ,__func__,__LINE__);
                }
    	      }
#else
            GstState cur_state = *((GstState *)data);
            
    		pmsg_send->msgtype = eMSG_TYPE_RESPONSE;
    		pmsg_send->subtype = eRESPONSE_TYPE_STATE_CHANGE;
            pmsg_send->val = -1;
    		if (GST_STATE_PAUSED == cur_state) {
                SERVER_INFO_PRINT("---- forcetv player state paused ----\n");
			    pmsg_send->val = ePLAYER_STATE_PAUSE;
            } else if (GST_STATE_PLAYING == cur_state) {
                SERVER_INFO_PRINT("---- forcetv player state playing ----\n");
				pmsg_send->val = ePLAYER_STATE_PLAY;
            } else if (GST_STATE_NULL== cur_state
                || GST_STATE_READY== cur_state) {
                SERVER_INFO_PRINT("---- forcetv player state stopped ----\n");
				pmsg_send->val = ePLAYER_STATE_STOP;
            } else { 
                SERVER_WARNING_PRINT("---- unknown state ----\n");
            }

		if(pmsg_send->val != -1)
		{
			//state changed. Set it.
			set_player_state((ePLAYER_STATE)pmsg_send->val);
		}

    		if (-1 != pmsg_send->val) {
                SERVER_INFO_PRINT("++++ forcetv player send STATECHANGE to UI ---\n");
    			if (msgsnd(qid_send, pmsg_send, MSG_SIZE, 0) == -1) {
    				perror("msgsnd");
    				SERVER_ERROR_PRINT ("---- Send msg error %s %d ----\n" ,__func__,__LINE__);
    			}
    		}
#endif
        }
        break;
            
        case eCB_TYPE_BUFFERING:
        {
#if 1
            SERVER_INFO_PRINT ("++++ buffering...... %d/100\n", pmsg_send->val);
            if(!send_message(pmsg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_BUFFERING, *((int*)data), TRUE))
            {
                SERVER_ERROR_PRINT ("---- Send msg error %s %d ----\n",
                    __func__,__LINE__);
            }
#else
    		pmsg_send->msgtype = eMSG_TYPE_RESPONSE;
    		pmsg_send->subtype = eRESPONSE_TYPE_BUFFERING;
    		pmsg_send->val = *((int*)data);
            
            SERVER_INFO_PRINT ("++++ buffering...... %d/100\n", pmsg_send->val);
    		if (msgsnd(qid_send, pmsg_send, MSG_SIZE, IPC_NOWAIT) == -1) {
				perror("msgsnd");
    			SERVER_ERROR_PRINT ("---- Send msg error %s %d ----\n",
                    __func__,__LINE__);
    		}
#endif
        }
        break;

        case eCB_TYPE_WARNING:
        {
		gboolean UnsupportIsAvailable = TRUE;
    		pmsg_send->msgtype = eMSG_TYPE_WARNING;
		if(g_strstr_len((char*)data, 5, "audio"))
		{
			pmsg_send->subtype = eWARN_SUB_UNSUPPORT_AUDIO;
		}
		else if(g_strstr_len((char*)data, 8, "AdDecErr"))
		{
			pmsg_send->subtype = eWARN_SUB_DECODE_ERR_AUDIO;
		}
		else if(g_strstr_len((char*)data, 8, "VdDecErr"))
		{
			pmsg_send->subtype = eWARN_SUB_DECODE_ERR_VIDEO;
		}
		else if(g_strstr_len((char*)data, 5, "video")||g_strstr_len((char*)data, 5, "image"))
		{
			pmsg_send->subtype = eWARN_SUB_UNSUPPORT_VIDEO;
		}
		else
		{
		     //if the Unsupport is not video or audio type,we believe it is not available;
			UnsupportIsAvailable = FALSE;
		}
		if(UnsupportIsAvailable)	
		{
    		memcpy(pmsg_send->data1, data, strlen (((char*)data)));
    		if (msgsnd(qid_send, pmsg_send, MSG_SIZE, 0) == -1) {
				perror("msgsnd");
    			SERVER_ERROR_PRINT ("---- Send msg error %s %d ----\n", 
                    __func__, __LINE__);
    		}
        }
        }
        break;

        case eCB_TYPE_ERR:
        {
		gchar *debug;
		GError *err;
		int val = 0;
		eERR_SUB_TYPE subtype = eERR_SUB_UNDEFINE;
		GstMessage *message = (GstMessage *)data;

		gst_message_parse_error (message, &err, &debug);
		
		if (g_strrstr (GST_OBJECT_NAME(message->src),"souphttpsrc"))
		{
			val = getSoupHttpStatusCode(debug);
			subtype = eERR_SUB_SOUP_HTTP;
		}
		else if(err->code == GST_STREAM_ERROR_TYPE_NOT_FOUND)
		{
			subtype = eERR_SUB_TYPE_NOT_FOUND;
		}
		else if(err->code == GST_STREAM_ERROR_DEMUX)
		{
			subtype = eERR_SUB_DEMUX;
		}

		g_snprintf(pmsg_send->data1, MAX_MSG_DATA_SIZE, "%s:%s", GST_OBJECT_NAME(message->src), err->message);
		g_error_free (err);
		g_free (debug);
		
		SERVER_INFO_PRINT("++++ streaming player send ERROR msg to UI!\n");
		if(!send_message(pmsg_send, eMSG_TYPE_ERR, subtype, val, FALSE))
		{
			SERVER_ERROR_PRINT("---- Send msg error %s %d ----\n", 
			                    __func__, __LINE__);
		}		
        }
        break;

        case eCB_TYPE_FINISHED:
        {
		//WARNING: cannot use send_message() to send this message. Because the message is sending to player itself.
    		pmsg_send->msgtype = eMSG_TYPE_EOS;
    		pmsg_send->subtype = eCMD_TYPE_EOS;
            SERVER_INFO_PRINT("---- send eos msg to thread body ----!\n");
    		if (msgsnd(qid_recv, pmsg_send, MSG_SIZE, 0) == -1) {
				perror("msgsnd");
    			SERVER_ERROR_PRINT("\t*** Send msg eos %s %d ***\n",__func__,__LINE__);
    		}
        }
        break;

        case eCB_TYPE_REDIRECT:
        {
			redirect = TRUE;
			if(play_url)
				g_free(play_url);
			play_url = (gchar *)g_malloc0(MAX_URL_LENGH);		
			strncpy(play_url, (gchar *)data, strlen((gchar *)data));
        }
	  	break;		
        case eCB_TYPE_TRICKINFO:
	 {
	 	pthread_mutex_lock (&Mutex);
		pmsg_send->msgtype = eMSG_TYPE_WARNING;
		if(g_strstr_len((char*)data, 8, "trickBOS"))
		{
			pmsg_send->subtype = eWARN_SUB_TRICK_BOS;
		}
		else if(g_strstr_len((char*)data, 8, "trickEOS"))
		{
			pmsg_send->subtype = eWARN_SUB_TRICK_EOS;
		}
           SERVER_INFO_PRINT("---- send trickinfo msg to thread body ----!\n");
    		if (msgsnd(qid_send, pmsg_send, MSG_SIZE, 0) == -1) {
				perror("msgsnd");
    			SERVER_ERROR_PRINT("\t*** Send msg trickinfo %s %d ***\n",__func__,__LINE__);
    		}		
		pthread_mutex_unlock (&Mutex);
		break;
       }
	case eCB_TYPE_FRAMECAPTURE_INFO:
		memcpy(pmsg_send->data1, data, strlen((char*)data));
		if(!send_message(pmsg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_FRAME_CAPTURE, 1, FALSE))
		{
			SERVER_ERROR_PRINT("---- Send msg error %s %d ----\n", 
			                    __func__, __LINE__);
		}	
		break;
        default:
        SERVER_WARNING_PRINT("---- unsupported eCB type ----\n");
        break;
    }
}

static gint vmsg_proc(stVMSG_QUE *vmsg)
{
    SERVER_INFO_PRINT("----vmsg proc type=%d, len=%d, st=%d, name=%s----\n", 
        (int)vmsg->subtype, (int)vmsg->len, vmsg->val, vmsg->data);
    
    switch(vmsg->subtype)
    {
        case eCMD_TYPE_SET_CURRENTSOURCE:
        {
			int play_url_len = MAX_URL_LENGH;
			int subtitle_uri_len = 0;
			char *sub = NULL;

			sub = strstr(vmsg->data, ";file://");
			if (sub != NULL)
			{
				subtitle_uri_len = strlen(sub+1);
				play_url_len = vmsg->len - subtitle_uri_len - 2;
				subtitle_uri = (gchar *)g_malloc0(subtitle_uri_len+1);
				memset (subtitle_uri, 0, subtitle_uri_len+1);
				strncpy(subtitle_uri, vmsg->data+play_url_len+1, subtitle_uri_len);
			}
			else
			{
				play_url_len = (int)vmsg->len;
			}

            if (play_url_len > MAX_URL_LENGH)
            {
                SERVER_ERROR_PRINT("url size is not enough\n");
                return -1;
            }
            else
            {
			if (g_str_has_prefix(vmsg->data, "LIVE-"))
				strncpy(play_url, vmsg->data+5, play_url_len-5);
			else
				{
					#ifdef SUPPORT_LINK_FILE
					FILE *fp = NULL;
					long lSize = 0;
					char *buffer = NULL;
					size_t result = 0;
					// if the file name include ".vurl", it means the file is a hyperlink, and that data is describe the media url. 
					if(strstr(vmsg->data, ".vurl"))
					{
						char *fileurl = NULL;
						fileurl = vmsg->data+sizeof("file://")-1;
						if(!fileurl)
							goto fileerr;
						fp = fopen(fileurl, "r");
						if(!fp)
						{
							SERVER_ERROR_PRINT("open %s failed\n",fileurl);
							goto fileerr;
						}
						// obtain file size:
						fseek (fp , 0 , SEEK_END);
						lSize = ftell (fp);
						if(!lSize)
							goto fileerr;
						rewind (fp);
						buffer = (char*) malloc (sizeof(char)*lSize);
						if(buffer)
						{
							result = fread (buffer,1,lSize,fp);
							strncpy(play_url, buffer, lSize);
							SERVER_INFO_PRINT("[support link file] url = %s\n",play_url);
						}
						else
							goto fileerr;
					}
					else
						strncpy(play_url, vmsg->data, play_url_len);
			fileerr:
					if(fp)
						fclose(fp);
					if(buffer)
						free(buffer);
					#else
				strncpy(play_url, vmsg->data, play_url_len);
					#endif
				}
			
                start_play_time = vmsg->val;
                mission_detail = eCMD_TYPE_SET_CURRENTSOURCE;
                pthread_mutex_lock(&mutex_has_mission); 
                pthread_cond_signal(&cond_has_mission);
                pthread_mutex_unlock(&mutex_has_mission);
            }
        }
        break;

        case eCMD_TYPE_SET_HTTP_HEADERS:
        {
            SERVER_INFO_PRINT(RED_STR"---- set http param %s----\n"BLUE_STR, 
                vmsg->data);
		if(info_request)
			g_free(info_request);						
            info_request = g_strdup(vmsg->data);
            //mini_player->setHttpRequest(vmsg->data);
        }
        break;
            
        case eCMD_TYPE_SET_HTTP_PROXY:
        {
            SERVER_INFO_PRINT(RED_STR"---- set proxy %s----\n"BLUE_STR, 
                vmsg->data);
		if(info_proxy)
			g_free(info_proxy);						
            info_proxy = g_strdup(vmsg->data);    
            //mini_player->setProxy(vmsg->data);
        }
        break;

        case eCMD_TYPE_SET_HTTP_AUTHENTICATION:
        {
            SERVER_INFO_PRINT(RED_STR"---- set authentication %s----\n"BLUE_STR, vmsg->data);
		if(info_authentication) 
			g_free(info_authentication);						
            info_authentication = g_strdup(vmsg->data); 
            //mini_player->setAuthentication(vmsg->data);
        }            
        break;

        case eCMD_TYPE_SET_PLAYREADY_HTTPOPT:
        {
            SERVER_INFO_PRINT(RED_STR"---- set playready httpopt %s----\n"BLUE_STR, 
                vmsg->data);
		if(playready_httpopt) //Nick add
			g_free(playready_httpopt);			
            playready_httpopt = g_strdup(vmsg->data);    
        }
        break;

        case eCMD_TYPE_SET_PLAYREADY_LICENSESERVER:
        {
            SERVER_INFO_PRINT(RED_STR"---- set playready license server url %s----\n"BLUE_STR, 
                vmsg->data);
		if(playready_licenseserver)
			g_free(playready_licenseserver);			
            playready_licenseserver = g_strdup(vmsg->data);    
        }
        break;
	case eCMD_TYPE_SET_DLNA_PROTOCOL:
	{
            SERVER_INFO_PRINT(RED_STR"---- set DLNA protocol %s----\n"BLUE_STR, 
                vmsg->data);
		if(dlna_protocol)
			g_free(dlna_protocol);
		dlna_protocol = g_strdup(vmsg->data);
	}
	break;
        default:
            break;
    }
    return 0;
}

//check whether @cmdSubType can be processed in STOP state
static gboolean isValidCmdInStopState(long cmdSubType)
{
	gboolean ret = TRUE;
	switch(cmdSubType)
	{
		case eCMD_TYPE_SET_CURRENTSOURCE:
		case eCMD_TYPE_VMSG:
		case eCMD_TYPE_CLOSE:
		case eCMD_TYPE_STOP:
		case eCMD_TYPE_SET_BUFFERING_LOW_PERCENT:
		case eCMD_TYPE_SET_BUFFERING_HIGH_PERCENT:
		case eCMD_TYPE_SET_MAX_BUFFERING_TIME:
		case eCMD_TYPE_DVIEW:
		case eCMD_TYPE_DISABLE_USE_SEEK_FOR_TRICK:
		/* eCMD_TYPE_EOS used by lib thread to inform player EOS.
		*  player sate may have been changed to STOP by lib.
		*/
		case eCMD_TYPE_EOS:
		case eCMD_TYPE_SET_SUBTITLE_DISPLAY:
		case eCMD_TYPE_SET_DLNA_PROTOCOL:
		case eCMD_TYPE_SET_FRAME_CAPTURE:	
			break;
		default:
			ret = FALSE;
			break;
	}
	return ret;
}
/*
* new a player instance.
* newing a player should be protected by mutex for insurance.
*/
static void new_player(eOPEN_TYPE type, STREAM_TYPE_T stream_type)
{
	pthread_mutex_lock(&mutex_new_player); 
	if(!mini_player)
		mini_player = new CStreamingPlayer(type, stream_type);
	pthread_mutex_unlock(&mutex_new_player);
}

/*
    main thread for command dispatch
*/
static stMSG_QUE msg_recv = {0};
static stMSG_QUE msg_send = {0};
static void *command_dispatch_thread(void *p)
{
    gboolean vmsg_flag = FALSE;
    size_t msg_length = 0;
    void *vmsg_recv = NULL;
    
	SERVER_LOG_PRINT("---- dispatch thread enter ----\n");
	pthread_mutex_lock(&mutex_start_gst);
	pthread_cond_wait(&cond_start_gst, &mutex_start_gst);
	pthread_mutex_unlock(&mutex_start_gst);

	bDispatchRunning = TRUE;
	SERVER_LOG_PRINT("---- dispatch thread start ----\n");
	while (!bIsServerExit)
	{
		if (vmsg_flag)
		{
			if (msgrcv(qid_recv, vmsg_recv, msg_length, 0, 0) == -1)
			{
				perror("msgrcv");
				SERVER_ERROR_PRINT("---- get msg fail %s %d ----\n", __func__, __LINE__);
				continue;
			}
			else
			{
				vmsg_proc((stVMSG_QUE *)vmsg_recv);
				vmsg_flag = FALSE;
				free(vmsg_recv);
				vmsg_recv = NULL;
			}
		}

		memset (&msg_recv, 0 , sizeof(stMSG_QUE));
		if (msgrcv(qid_recv, (stMSG_QUE *)&msg_recv, MSG_SIZE, 0, 0) == -1)
		{
			perror("msgrcv");
			SERVER_ERROR_PRINT("---- get msg fail %s %d ----\n",__FUNCTION__,__LINE__);
			continue;
		}

		if (	(get_player_state() == ePLAYER_STATE_STOP) &&	
			!isValidCmdInStopState(msg_recv.subtype)) 
	    {
			//If set source havn't been completed, we must wait~~
			SERVER_WARNING_PRINT("---- wait set source, cmd:%ld can't be executed----\n", msg_recv.subtype);
		}
		else
		{
			switch (msg_recv.subtype)
			{
				case eCMD_TYPE_SET_CURRENTSOURCE:
				{
					SERVER_INFO_PRINT("---- force server set source ----\n");
					strncpy(play_url, msg_recv.data1, 256);//data1 is 256B
					start_play_time = msg_recv.val;

					mission_detail = eCMD_TYPE_SET_CURRENTSOURCE;
				
					pthread_mutex_lock(&mutex_has_mission); 
					pthread_cond_signal(&cond_has_mission);
					pthread_mutex_unlock(&mutex_has_mission);
				}
				break;
				case eCMD_TYPE_DVIEW:
    			{
					SERVER_INFO_PRINT(RED_STR"---- set dview param %s----\n"BLUE_STR, msg_recv.data1);
					if (mini_player)
						mini_player->setDview(msg_recv.data1);
					else
						info_dview = g_strdup(msg_recv.data1);
				}	
				break;
				case eCMD_TYPE_PLAY:
				{
					if (!mini_player)
					{
						STREAM_TYPE_T stream_type = INVALIDS;
						stream_type = get_media_types_by_suffix(rec_name);
						new_player(eAppType, stream_type); 
						mini_player->cb_funcforAP = cb_funcforAP;
						mini_player->setSubtitleDisplay(bDisplaySubtitle);
						mini_player->setCurrentSource(rec_name, 0);
					}
					//set play with rate
					{
						gboolean ret;
						gint rate;
						if (!msg_recv.val)
							rate = 1;
						else
							rate = msg_recv.val;
						ret = mini_player->setPlayRate(rate);
						send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_PLAY_RATE, ret, TRUE);
					}
					//mini_player->play();
				}
    			break;
				case eCMD_TYPE_PAUSE:
				{
					//mini_player->pause();
					if (mini_player)
					{	//pvr mode
							mini_player->pause();
					}
					else
							g_print ("[CMD] : PAUSE\tDo nothing\n");
				}	
				break;
				case eCMD_TYPE_STOP:
				{
					if (mini_player) 
					{
						mini_player->stop();
						delete mini_player;
						mini_player = NULL;
						set_player_state(ePLAYER_STATE_STOP);
					}
				}
				break;
				case eCMD_TYPE_TOTALTIME:
				{
					//mini_player->totalTime();
					send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_TOTALTIME, mini_player->totalTime(), TRUE);
				}
				break;
				case eCMD_TYPE_CURRENTTIME:
				{
					//mini_player->currentTime();
					if (eCMD_TYPE_SEEK == mission_detail) 
					{
						send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_CURRENTTIME, seek_pos, TRUE);
					}
					else
					{
						send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_CURRENTTIME, mini_player->currentTime(), TRUE); 
					}
				}
				break;
				case eCMD_TYPE_VIDEOINFO: //Will be deprecated. Don't use it.
				{
					SERVER_INFO_PRINT("---- query video info  -----\n");
					memset (&msg_send, 0, sizeof(stMSG_QUE));
					msg_send.msgtype = eMSG_TYPE_RESPONSE;
					msg_send.subtype = eRESPONSE_TYPE_VIDEOINFO;

					sprintf(msg_send.data1, "width:%d,height:%d,framerate:%d,bitrate:%d",
						mini_player->currentVideoInfo(VWIDTH),
						mini_player->currentVideoInfo(VHEIGHT),
						mini_player->currentVideoInfo(VFRAMERATE),
						mini_player->currentVideoInfo(VBITRATE));
								
					if (msgsnd(qid_send, (stMSG_QUE *)&msg_send, MSG_SIZE, 0) == -1)
					{
						perror("msgsnd");
						SERVER_ERROR_PRINT("\t*** Send msg error %s ***\n",__FUNCTION__);
					}
				}
				break;
				case eCMD_TYPE_VIDEOWIDTH: //Will be deprecated. Don't use it.
				{
					SERVER_INFO_PRINT("---- query video width  -----\n");
					send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_VIDEOWIDTH, mini_player->currentVideoInfo(VWIDTH), TRUE); 
				}
				break;
				case eCMD_TYPE_VIDEOHEIGHT: //Will be deprecated. Don't use it.
				{
					SERVER_INFO_PRINT("---- query video height -----\n");
					send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_VIDEOHEIGHT, mini_player->currentVideoInfo(VHEIGHT), TRUE); 
				}
				break;
				case eCMD_TYPE_VIDEOFRAMERATE: //Will be deprecated. Don't use it.
				{
					SERVER_INFO_PRINT("---- query video framerate -----\n");
					send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_VIDEOFRAMERATE, mini_player->currentVideoInfo(VFRAMERATE), TRUE); 
				}
				break;
				case eCMD_TYPE_VIDEOBITRATE: //Will be deprecated. Don't use it.
				{
					SERVER_INFO_PRINT("---- query video bitrate -----\n");
					send_message(&msg_send, eMSG_TYPE_RESPONSE, 
						eRESPONSE_TYPE_VIDEOBITRATE, mini_player->currentVideoInfo(VBITRATE), TRUE); //in byte per second
				}
				break;
				case eCMD_TYPE_ISSEEKABLE:
					send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_ISSEEKABLE, mini_player->isSeekable(), TRUE);
				break;
				case eCMD_TYPE_SEEK:
				{
					seek_pos = msg_recv.val;
					mission_detail = eCMD_TYPE_SEEK;
				
					pthread_mutex_lock(&mutex_has_mission); 
					pthread_cond_signal(&cond_has_mission);
					pthread_mutex_unlock(&mutex_has_mission);
				}
				break;
				case eCMD_TYPE_DISABLE_USE_SEEK_FOR_TRICK:
				{
					SERVER_INFO_PRINT("---- disable use seek for trick  -----\n");
					disable_use_seek_for_trick = 1;
					if (mini_player)
						mini_player->disableUseSeekforTrick();
				}
				break;
				case eCMD_TYPE_SET_PLAY_RATE:
				{
					gboolean ret;
						ret = mini_player->setPlayRate(msg_recv.val);
					send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_PLAY_RATE, ret, TRUE);
				}
				break;
				case eCMD_TYPE_EOS:
				{     
					if (mini_player) 
					{                    
						delete mini_player;
						mini_player = NULL;
						set_player_state(ePLAYER_STATE_STOP);

						SERVER_WARNING_PRINT("++++ send EOS Finish msg to UI ----\n");
						send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_FINISHED, 0, TRUE);
					}
				}
				break;
				case eCMD_TYPE_CLOSE:
				{
					SERVER_WARNING_PRINT("---- server recv cmd close ----%s %d\n", __func__, __LINE__);
					bIsServerExit = TRUE;
					pthread_mutex_lock(&mutex_has_mission); 
					pthread_cond_signal(&cond_has_mission);
					pthread_mutex_unlock(&mutex_has_mission);					
				}
				break;
				case eCMD_TYPE_START_RECORD:
				{
					g_print ("\tGot CMD:eCMD_TYPE_START_RECORD\n");
					g_print("\t[1] %s [2]%s\n",msg_recv.data1, msg_recv.data2);	//data1:uri data2:rec_info
					//delete streaming player
					//launch recorder
					delete mini_player;
					mini_player = NULL;
					g_print("\tdelete streaming player and launch recorder\n");

					recorder = new CRecorder(eRECORD_TYPE_STREAMING);
					recorder->cb_funcforAP = cb_rec_funcforAP;
					recorder->setCurrentSource(msg_recv.data1, 0);
					recorder->setRecordInfo(msg_recv.data2);
					recorder->play();
				}
				break;
				case eCMD_TYPE_STOP_RECORD:
				{
				    delete recorder;
				    recorder = NULL;
				}
				break;
				case eCMD_TYPE_RECORD_FINISHED:
				{
				    //delete recorder
				    //delete streaming file player
				    //launch streaming player
				    if (recorder)
				    {
				  	delete recorder;
					recorder = NULL;
				    }
				    //mini_player->stop();
				    delete mini_player;
				    mini_player = NULL;
				set_player_state(ePLAYER_STATE_STOP);
				    
				    SERVER_INFO_PRINT("---- force server set source ----\n");
				    strncpy(play_url, msg_recv.data1, 256);//data1 is 256B
				    start_play_time = 0;
			
				    mission_detail = eCMD_TYPE_SET_CURRENTSOURCE;
			
				    pthread_mutex_lock(&mutex_has_mission); 
				    pthread_cond_signal(&cond_has_mission);
				    pthread_mutex_unlock(&mutex_has_mission);
				}
				break;
				case eCMD_TYPE_VMSG:
				{
					vmsg_flag = TRUE;
					msg_length = msg_recv.val;
					vmsg_recv = malloc(msg_length);//length
					msg_length = (msg_length - sizeof(long));

					SERVER_INFO_PRINT("---- vmsg : len=%d ----\n", msg_length);
					if (vmsg_recv == NULL)
					{
						SERVER_ERROR_PRINT("---- malloc vmsg error ----\n");
						bIsServerExit = TRUE;
					} 
				}
				break;
				case eCMD_TYPE_BITRATE:
				{
					SERVER_INFO_PRINT("---- set bitrate ----\n");
					//mini_player->SetBitrate(msg_recv.val);
				}
				break;
				case eCMD_TYPE_METADATA:
				{
					// SERVER_INFO_PRINT("---- get meata data ---- \n");
					if (mini_player) 
					{
	 					pthread_mutex_lock (&Mutex);
						if (flag & FLAG_FINISHED_METADATA)
						{
							medadata_map metaData;
							metaData = mini_player->metaData();
							medadata_map::iterator it;
							for (it=metaData.begin(); it!=metaData.end(); it++)
							{
								memset (&msg_send, 0, sizeof(stMSG_QUE));
								msg_send.msgtype = eMSG_TYPE_RESPONSE;
								msg_send.subtype = eRESPONSE_TYPE_METADATA;
								//g_print ("\t\t%s\t%s\n",it->first.c_str(), it->second.c_str());
								if (strlen(it->second.c_str()) < 200)
		  					{
									memcpy (msg_send.data1,it->first.c_str(),strlen(it->first.c_str()));
									memcpy (msg_send.data2,it->second.c_str(),strlen(it->second.c_str()));
									if (msgsnd(qid_send, (stMSG_QUE *)&msg_send, MSG_SIZE, 0) == -1)
									{
										perror("msgsnd");
										g_print ("\t*** Send msg error %s %d ***\n",__FUNCTION__,__LINE__);
									}
								}
								else
									g_print ("\t@^@^@\ttag [ %s ] content too large\t\n",it->first.c_str());
							}
							memset (&msg_send, 0, sizeof(stMSG_QUE));
							msg_send.msgtype = eMSG_TYPE_RESPONSE;
							msg_send.subtype = eRESPONSE_TYPE_METADATA_FINISHED;
							if (msgsnd(qid_send, (stMSG_QUE *)&msg_send, MSG_SIZE, 0) == -1)
							{
								perror("msgsnd");
								g_print ("\t*** Send msg error %s %d ***\n",__FUNCTION__,__LINE__);
							}
						}
						else
							flag |= FLAG_NEED_METADATA;
						pthread_mutex_unlock (&Mutex);
					}
				}
				break;
				case eCMD_TYPE_STREAM_NUM:
				{
					// SERVER_INFO_PRINT("---- stream number ---- \n");
					if (mini_player)
					{                 
						memset (&msg_send, 0, sizeof(stMSG_QUE));
						msg_send.msgtype = eMSG_TYPE_RESPONSE;
						msg_send.subtype = eRESPONSE_TYPE_STREAM_NUM;
						memcpy (msg_send.data1, "n-audio", 8);
						memcpy (msg_send.data2, "2", 2);
						if (msgsnd(qid_send, (stMSG_QUE *)&msg_send, MSG_SIZE, 0) == -1) 
						{
							SERVER_ERROR_PRINT("---- send msg error %s %d ----\n", __FUNCTION__, __LINE__);
						}

						msg_send.msgtype = eMSG_TYPE_RESPONSE;
						msg_send.subtype = eRESPONSE_TYPE_STREAM_NUM;
						memcpy (msg_send.data1, "n-subtitle", 11);
						memcpy (msg_send.data2, "2", 2);
						if (msgsnd(qid_send, (stMSG_QUE *)&msg_send, MSG_SIZE, 0) == -1) 
						{
							SERVER_ERROR_PRINT("---- send msg error %s %d ----\n", __FUNCTION__, __LINE__);
						}
					}
				}
				break;
				case eCMD_TYPE_CUR_STREAM_INFO: //nick add
				{
					if (mini_player)
					{
						medadata_map curStreamInfo;
						medadata_map::iterator it;
						mini_player->GetCurStreamInfo(curStreamInfo);
						for (it=curStreamInfo.begin(); it!=curStreamInfo.end(); it++)
						{
							eSTREAM_INFO streamInfo; 
							//total length of variable message.
							// +1 for null terminate of second string.
							msg_length = strlen(it->second.c_str()) + sizeof(stVMSG_QUE) + 1;
							send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_VMSG, msg_length, TRUE);
							
							if(!strcmp(it->first.c_str(), "audio-info"))
							{
								streamInfo = STREAM_INFO_AUDIO;
							}
							else if(!strcmp(it->first.c_str(), "video-info"))
							{
								streamInfo = STREAM_INFO_VIDEO;
							}
							else
							{//subtitle
								streamInfo = STREAM_INFO_SUBTITLE;
							}
							send_vMessage(eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_CUR_STREAM_INFO, streamInfo, it->second.c_str(), strlen(it->second.c_str()) + 1);
						}
						//Notice cur stream info finish.
						send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_CUR_STREAM_INFO_FINISH, 0, TRUE);
					}
					break;
				}
				case eCMD_TYPE_STREAM_INFO:
				{
					if (mini_player)
					{
						medadata_map streamInfo;
						medadata_map::iterator it;
						streamInfo = mini_player->GetStreamInfo();
						for (it=streamInfo.begin(); it!=streamInfo.end(); it++)
						{
							eSTREAM_INFO streamInfo; 
							//total length of variable message.
							// +1 for null terminate of second string.
							msg_length = strlen(it->second.c_str()) + sizeof(stVMSG_QUE) + 1;
							send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_VMSG, msg_length, TRUE);
							if(!strcmp(it->first.c_str(), "audio-info"))
							{
								streamInfo = STREAM_INFO_AUDIO;
							}
							else
							{//subtitle
								streamInfo = STREAM_INFO_SUBTITLE;
							}

							send_vMessage(eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_STREAM_INFO, streamInfo, it->second.c_str(), strlen(it->second.c_str()) + 1);
						}
						//Notice stream info finish.
						send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_STREAM_INFO_FINISH, 0, TRUE);
					}
				}
				break;
				case eCMD_TYPE_CHANGE_SUBTITLE:
					g_print("change Subtitle to %d\n",msg_recv.val);
					mini_player->changeSubtitle(msg_recv.val);
				break;
				case eCMD_TYPE_CHANGE_AUDIO:
					g_print("change Audio to %d\n",msg_recv.val);
					mini_player->changeAudio(msg_recv.val);
				break;
				case eCMD_TYPE_BUFFERING_RESUME:
				break;
				case eCMD_TYPE_SET_BRIGHTNESS:
					SERVER_LOG_PRINT ("SET_BRIGHTNESS\n");
					mini_player->brightness(msg_recv.val);
				break;
  			   	case eCMD_TYPE_SET_CONTRAST:
					SERVER_LOG_PRINT ("SET_CONTRAST\n");
					mini_player->contrast(msg_recv.val);
				break;
  			   	case eCMD_TYPE_SET_HUE:
					SERVER_LOG_PRINT ("SET_HUE\n");
					mini_player->hue(msg_recv.val);
				break;
  			   	case eCMD_TYPE_SET_SATURATION:
					SERVER_LOG_PRINT ("SET_SATURATION\n");
					mini_player->saturation(msg_recv.val);
				break;
  			   	case eCMD_TYPE_SET_SHARPNESS:
					SERVER_LOG_PRINT ("SET_SHARPNESS\n");
					mini_player->sharpness(msg_recv.val);
				break;
  			   	case eCMD_TYPE_SET_VEDIO_ENHANCE_DEFAULT:
					SERVER_LOG_PRINT ("SET_VEDIO_ENHANCE_DEFAULT\n");
					mini_player->enhance_default();
				break;
				case eCMD_TYPE_SET_BUFFERING_LOW_PERCENT:
					SERVER_LOG_PRINT ("SET_BUFFERING_LOW_PERCENT\n");
					low_percent = msg_recv.val;
				break;
				case eCMD_TYPE_SET_BUFFERING_HIGH_PERCENT:
					SERVER_LOG_PRINT ("SET_BUFFERING_HIGH_PERCENT\n");
					high_percent = msg_recv.val;
				break;
				case eCMD_TYPE_SET_MAX_BUFFERING_TIME:
					SERVER_LOG_PRINT ("SET_MAX_BUFFERING_TIME\n");
					max_buffering_time = msg_recv.val;
				break;
				case eCMD_TYPE_SET_SUBTITLE_DISPLAY:
				{
					bDisplaySubtitle = (gboolean)msg_recv.val;
					if (mini_player)
						mini_player->setSubtitleDisplay(bDisplaySubtitle);
					break;
				}
				case eCMD_TYPE_SET_VIDEO_DISPLAY:
					if (mini_player)
						mini_player->setVideoDisplay((gboolean)msg_recv.val);
				break;
				case eCMD_TYPE_GET_DOWNLOAD_SPEED:
					if(mini_player)
					{
						guint64 networkSpeed;
						if(mini_player->getDownLoadSpeed(&networkSpeed))
						{
							sprintf(msg_send.data1, "%lld", networkSpeed);
							send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_DOWNLOAD_SPEED, 1, FALSE);
						}
						else
						{//return fail
							send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_DOWNLOAD_SPEED, 0, TRUE);
						}
					}

					break;
				case eCMD_TYPE_GET_MEDIA_SIZE:
					if(mini_player)
					{
						gint64 mediaSize;
						if((mediaSize = mini_player->totalSize()) > 0)
						{//total size is valid
							sprintf(msg_send.data1, "%lld", mediaSize);
							send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_GET_MEDIA_SIZE, 1, FALSE);
						}
						else
						{//total size is invalid
							send_message(&msg_send, eMSG_TYPE_RESPONSE, eRESPONSE_TYPE_GET_MEDIA_SIZE, 0, TRUE);
						}
					}
				break;
				case eCMD_TYPE_SET_FRAME_CAPTURE:
					new_player(eAppType, INVALIDS);
					mini_player->setFrameCaptureMode();
				break;
				default:
					SERVER_WARNING_PRINT("---- can not handle %ld ----\n", msg_recv.subtype);
				break;
    		}
		}
	}

	if (vmsg_recv) 
	{
		free(vmsg_recv);
	}
	g_main_loop_quit (gmainloop);
	SERVER_LOG_PRINT("\t@^@ Exit thread @^@\n");
	pthread_exit(NULL);

	return p;
}

static void *command_proc_thread(void *priv)
{
	for(;;) 
	{
		if (bIsServerExit)
		{
			break;
		}

		pthread_mutex_lock(&mutex_has_mission);
		pthread_cond_wait(&cond_has_mission, &mutex_has_mission);
		pthread_mutex_unlock(&mutex_has_mission);

		switch(mission_detail)
		{
			case eCMD_TYPE_SET_CURRENTSOURCE:
			{
				STREAM_TYPE_T stream_type = INVALIDS;
src_redirect:
				stream_type = get_media_types_by_suffix(play_url);
				if (INVALIDS == stream_type)
				{
					SERVER_INFO_PRINT("---- uknown media type ----\n");
#ifndef DYNAMIC_LINK_ENABLE
					bIsServerExit = TRUE;
					break;
#endif
				}
				SERVER_INFO_PRINT(" ---- create pipeline st:%d----\n", start_play_time);

				new_player(eAppType, stream_type); 
				mini_player->cb_funcforAP= cb_funcforAP;
				if(disable_use_seek_for_trick)
					mini_player->disableUseSeekforTrick();

				// Set Subtitle Display with keeping setting
				mini_player->setSubtitleDisplay(bDisplaySubtitle);
				// Set Subtitle for each
				if (subtitle_uri)
				{
					char *pch = NULL;
					const char *delim = ";";
					pch = strtok(subtitle_uri, delim);
					while (pch != NULL)
					{
						mini_player->setSubtitle(pch);
						pch = strtok(NULL, delim);
					}
					g_free(subtitle_uri);
					subtitle_uri = NULL;
				}

				if(info_proxy)
				{
					SERVER_INFO_PRINT("set proxy info: %s\n", info_proxy);
					mini_player->setProxy(info_proxy);
					g_free(info_proxy);
					info_proxy = NULL;
        		}
                
        		if(info_request)
        		{
					SERVER_INFO_PRINT("set request info: %s\n", info_request);
					mini_player->setHttpRequest(info_request);	
					g_free(info_request);
					info_request = NULL;
				}
				
                if(info_authentication)
                {
					SERVER_INFO_PRINT("set authentication info: %s\n", info_authentication);
					mini_player->setAuthentication(info_authentication);
					g_free(info_authentication);
					info_authentication = NULL;
        		}
				if (info_dview)
				{
					SERVER_INFO_PRINT("set dview info: %s\n", info_dview);
					mini_player->setDview(info_dview);
					g_free(info_dview);
					info_dview = NULL;
				}
				if(playready_httpopt)
				{
					SERVER_INFO_PRINT("set playready http option: %s\n", playready_httpopt);
					mini_player->set_playready_httpopt(playready_httpopt);
					g_free(playready_httpopt);
					playready_httpopt = NULL;
        		}
				if(playready_licenseserver)
				{
					SERVER_INFO_PRINT("set playready license server url: %s\n", playready_licenseserver);
					mini_player->set_playready_license_server_url(playready_licenseserver);
					g_free(playready_licenseserver);
					playready_licenseserver = NULL;
        		}
				if(dlna_protocol)
				{
					SERVER_INFO_PRINT("set dlna protocol: %s\n", dlna_protocol);
					mini_player->set_dlna_protocol(dlna_protocol);	
					g_free(dlna_protocol);
					dlna_protocol = NULL;
				}

				mini_player->setBufferingTime(max_buffering_time, low_percent, high_percent);
    			mini_player->setCurrentSource((const gchar *)play_url, start_play_time);
				//mini_player->setLive (TRUE);
                mission_detail = eCMD_TYPE_MAX;                
		    	if(redirect)
		   		{
					if (mini_player) 
					{
						mini_player->stop();
						delete mini_player;
						mini_player = NULL;
						SERVER_WARNING_PRINT("the previous mini_player has been deleted\n");
					}
		      		redirect = FALSE;
					goto src_redirect;
		   		}  
            }
            break;

			case eCMD_TYPE_SEEK:
            {
			    mini_player->seek(seek_pos);
                mission_detail = eCMD_TYPE_MAX;
            }
            break;
            
            case eCMD_TYPE_PAUSE:
                break;

            case eCMD_TYPE_PLAY:
                break;

            default:
                break;
        }
    }
    pthread_exit(NULL);
      
    return NULL;
}

/*
 * Callback function for signal handle
 * Current support signal SIGINT, SIGUSR1
 * SIGINT : exit this process
 * SIGUSR1 : query buffer status
 * @ sig (in) : signal number
 */
static void Sigal_Handler(int sig)
{
	//stMSG_QUE *pmsg_send = NULL;
	SERVER_INFO_PRINT("Catched signal: %d ... !!\n", sig);

	if (sig == SIGINT)
	{
		//mini_player->setDview("0:0:1280:720");
		//sleep (1);
		stMSG_QUE msg = {0};
		msg.msgtype = eMSG_TYPE_CMD;
		msg.subtype = eCMD_TYPE_CLOSE;
		if (msgsnd(qid_recv, (stMSG_QUE *)&msg, MSG_SIZE, 0) == -1)
		{
			perror("msgsnd");
			g_print ("\t*** Send msg error %s %d ***\n",__FUNCTION__,__LINE__);
		}
	}
    else if (sig == SIGUSR1) {
        if (mini_player) {
            mini_player->watch();
        }
    } 
#ifdef FAULT_HANDLER
	else if(sig == SIGSEGV)
	{
		g_print ("\t*** got SIGSEGV, please attach to gdb for debug ***\n");
		while(1)
		{
			sleep (1);
		}
	}
#endif
}

int main (gint argc, gchar *argv[])
{
    pthread_t threadID_main = 0, threadID_proc = 0;
	if ((qid_send = msgget(KEY_CLIENT, 0644)) == -1) {
		SERVER_ERROR_PRINT("---- can not access msg queue %s %d ----\n",__func__,__LINE__);
		exit(1);
	}
	if ((qid_v_send = msgget(KEY_V_CLIENT, 0644)) == -1) {
		SERVER_ERROR_PRINT("---- can not access vmsg queue %s %d ----\n",__func__,__LINE__);
		exit(1);
	}
	// Create our message queue to receive client command
    system("ipcrm -Q 100220");
	if ((qid_recv = msgget(KEY_SERVER, 0644 | IPC_CREAT)) == -1) {
		SERVER_ERROR_PRINT("---- Can not create msg que %s %d ----\n", 
            __FUNCTION__, __LINE__);
        exit(1);
	}

//do malloc optimize
    mallopt(M_MMAP_MAX, 0); //disable mmap
    //mallopt(M_TRIM_THRESHOLD, -1);//disable memory trim
    signal(SIGINT, Sigal_Handler);
	signal(SIGUSR1, Sigal_Handler);
#ifdef FAULT_HANDLER
	signal(SIGSEGV, Sigal_Handler);
#endif
    bIsServerExit = FALSE;

#ifdef ELEMENTS_DEBUG_ENALBE
    strcpy(gst_debug_info[debug_num], "--gst-debug-level=1");
    debug_num++;
    
    strcpy(gst_debug_info[debug_num], "--gst-debug=basesrc:4");
    debug_num++;
    //strcpy(gst_debug_info[debug_num], "--gst-debug=souphttpsrc:4");
    //debug_num++;
    //strcpy(gst_debug_info[debug_num], "--gst-debug=mpegtsdemux:1");
    //debug_num++;
    //strcpy(gst_debug_info[debug_num], "--gst-debug=flvdemux:4");
    //debug_num++; 
    //strcpy(gst_debug_info[debug_num], "--gst-debug=pipeline:4");
    //debug_num++; 

    argv[argc++] = (char *)gst_debug_info[0];
    argv[argc++] = (char *)gst_debug_info[1];
    //argv[argc++] = (char *)gst_debug_info[2];

    //argc = (argc + debug_num);

//    strcpy(gst_debug_info[2], "GST_STATES:4");
//    debug_num++;
//    strcpy(gst_debug_info[3], "GST_CAT_PARENTAGE:4");
//    debug_num++;
#endif

#if 0
    eAppType = eOPEN_TYPE_INVALID;
    for(i=0;ctype_maps[i].name != NULL;i++) {
        if (argv[1] && strncasecmp(ctype_maps[i].name, argv[1], strlen(ctype_maps[i].name)) == 0) {
        	eAppType = ctype_maps[i].type;
            SERVER_INFO_PRINT("---- open player for %s ----\n", ctype_maps[i].name);
            break;
        }
    }
#endif
	player_state.player_state = ePLAYER_STATE_STOP; //initialize
    gmainloop = g_main_loop_new(NULL, FALSE);
    gst_init(&argc, &argv);

	// create thread to handle client command
	pthread_create(&threadID_main, NULL, command_dispatch_thread, (void*)0);
	pthread_create(&threadID_proc, NULL, command_proc_thread, (void*)0);    

    while(!bDispatchRunning) {
        pthread_mutex_lock(&mutex_start_gst);
        pthread_cond_signal(&cond_start_gst); 
        pthread_mutex_unlock(&mutex_start_gst);
        g_usleep(20*1000);
    }

    play_url = (gchar *)g_malloc0(MAX_URL_LENGH);
    if (play_url == NULL) {
        SERVER_ERROR_PRINT("url name malloc failed\n");
        exit(1);
    }
	memset(&msg_send, 0, sizeof(stMSG_QUE));
	msg_send.msgtype = eMSG_TYPE_RESPONSE;
	msg_send.subtype = eRESPONSE_TYPE_OPEN;
	if (msgsnd(qid_send, &msg_send, MSG_SIZE, 0) == -1) {
		perror("msgsnd");
		SERVER_ERROR_PRINT("---- Send msg error %s %d ----\n",
            __func__, __LINE__);
	}	

    SERVER_LOG_PRINT("---- player Server start Playing ----\n");
    g_main_loop_run (gmainloop);
    
	pthread_join(threadID_main, NULL);
    pthread_join(threadID_proc, NULL);

    pthread_cond_destroy(&cond_has_mission);
	pthread_mutex_destroy(&mutex_has_mission);
    
	pthread_mutex_destroy(&mutex_start_gst);
    pthread_cond_destroy(&cond_start_gst);

	pthread_mutex_destroy(&Mutex);

//=========================================================================
	delete mini_player;
	mini_player = NULL;
    g_free(play_url);
	  
	// Delete our message queue
	// Do not receive any command from client
	if (msgctl(qid_recv, IPC_RMID, NULL) == -1)
	{
		perror("msgctl");
		SERVER_ERROR_PRINT ("\t*** Can not delete msg que %s %d ***\n",__FUNCTION__,__LINE__);
	}

	memset (&msg_send,0,sizeof(stMSG_QUE));
	msg_send.msgtype = eMSG_TYPE_RESPONSE;
	msg_send.subtype = eRESPONSE_TYPE_CLOSE;
	if (msgsnd(qid_send, (stMSG_QUE *)&msg_send, MSG_SIZE, 0) == -1)
	{
		perror("msgsnd");
		SERVER_ERROR_PRINT ("\t*** Send msg error %s %d ***\n",__FUNCTION__,__LINE__);
	}	
	SERVER_LOG_PRINT("=== Player Server Exit OK ===\n");

	return 0;
}

