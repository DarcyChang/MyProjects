/**
 *  @file goplayer_sample.c
 *
 *  A sample code to demo and verify goplayer library.
 *  This sample code presents how to use this library to play stream media and how to receive message from player.
 *
 *
 *  @section make_sec Make binary file
 *  Modifying the Makefile, the following items you should modify to fit your environment.
 *
 *  **ALI_MIPS_TOOLCHAIN_DIR**: specify toolchain install path.
 *
 *  **ALI_MIPS_SDK_DIR**: specify sdk path (required libraies and include files)
 *
 *  After executing the Makefile, the output result binary file **goplayer_sample** 
 *  should be generated.
 *
 *  @section manual_sec Executing goplayer_sample
 *
 *  **SYNOPSIS**

          goplayer_sample <uri> &

 *  **EXAMPLE**

          goplayer_sample http://127.0.0.1/test.wmv &

 *
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <malloc.h>
#include <signal.h>
#include <unistd.h>
#include <goplayer.h>
#include "cmdpipe.h"


static int b_exit = 0;

/**
 *  Callback function for player to notify APP.

 *  @param [out] type all possible responses from goplayer
 *  @param [out] data #GOPLAYER_STREAM_CALLBACK
 *  @see goplayer_open

 */
void cb_func(eGOPLAYER_CALLBACK_TYPE type, void *data)
{
	switch (type)
	{
		case eGOPLAYER_CBT_STATE_CHANGE:
		{
			if((eGOPLAYER_STATE)data == eGOPLAYER_STATE_PAUSE)
				printf("[sample]state : pause\n");
			else if ((eGOPLAYER_STATE)data == eGOPLAYER_STATE_PLAY)
				printf("[sample]state : play\n");
			else
				printf("[sample]state : stop\n");
		}
		break;

		case eGOPLAYER_CBT_BUFFERING:
		{
			int percent = (int)data;
			printf("[sample] buffering : %d \n", percent);
		}
		break;

		case eGOPLAYER_CBT_WARN_UNSUPPORT_AUDIO:
			printf("[sample] UNSUPPORT_AUDIO\n");
		break;

		case eGOPLAYER_CBT_WARN_UNSUPPORT_VIDEO:
			printf("[sample] UNSUPPORT_VIDEO\n");
		break;

		case eGOPLAYER_CBT_WARN_DECODE_ERR_AUDIO:
			printf("[sample] DECODE_ERR_AUDIO\n");
		break;

		case eGOPLAYER_CBT_WARN_DECODE_ERR_VIDEO:
			printf("[sample] DECODE_ERR_VIDEO\n");
		break;

		case eGOPLAYER_CBT_WARN_TRICK_BOS:
			printf("[sample] RW to BOS\n");
		break;

		case eGOPLAYER_CBT_WARN_TRICK_EOS:
			printf("[sample] FF to EOS\n");
		break;

		case eGOPLAYER_CBT_ERR_SOUPHTTP:
			printf("[sample] Soup http error code: %d\n", (int)data);
			b_exit = 1;
			break;

		case eGOPLAYER_CBT_ERR_TYPE_NOT_FOUND:
		case eGOPLAYER_CBT_ERR_DEMUX:			
		case eGOPLAYER_CBT_ERR_UNDEFINED:
			printf("[sample] Error : %s\n", (char*)data);
			b_exit = 1;
		break;

		case eGOPLAYER_CBT_FINISHED:
			printf("[sample] EOS\n");
			b_exit = 1;
		break;

		case eGOPLAYER_CBT_FRAME_CAPTURE:
			printf("[sample] frame captured path %s\n", (char*)data);
			break;

		case eGOPLAYER_CBT_MAX:
		break;
		default:
		break;
	}
}

#define FOURCC_FORMAT "c%c%c%c"
#define FOURCC_ARGS(fourcc) \
        ((gchar) ((fourcc)     &0xff)), \
        ((gchar) (((fourcc)>>8 )&0xff)), \
        ((gchar) (((fourcc)>>16)&0xff)), \
        ((gchar) (((fourcc)>>24)&0xff))
/**
 *  The function operates predefined behavior according to given command.

 *  When goplayer_sample is running in background, we can send command to goplayer by pipeline.

 *  For example, to send [pause] command to goplayer_sample for pause.

 *  \# echo pause > cmd_receiver

 *  table below list predefined action and corresponding command:

 *  | command | action | expression |
 *  |:-----|:-----|:-------|
 *  |play | set player to play | echo play > cmd_receiver |
 *  |pause | set player to pause | echo pause > cmd_receiver |
 *  |ff | set player to ff (4x) | echo ff > cmd_receiver |
 *  |rw | set player to rw (4x) | echo rw > cmd_receiver |
 *  |seek | set player to seek (seek to 10s of media) | echo seek > cmd_receiver |
 *  |getcurrenttime | get current time | echo getcurrenttime > cmd_receiver |
 *  |gettotaltime | get total time | echo gettotaltime > cmd_receiver |
 *  |isseekable | check the media is seekable or not | echo isseekable > cmd_receiver |
 *  |getvideoinfo | get video information (width, height, bit rate, frame rate) | echo getvideoinfo > cmd_receiver |
 *  |getstreaminfo | get stream information (multi-audio and multi-subtitle) | echo getstreaminfo > cmd_receiver |
 *  |getcurstreaminfo | get current stream information (cur-audio and cur-subtitle) | echo getcurstreaminfo > cmd_receiver |
 *  |setscale | change display position and dimension (x:100,y:100,width:200,height:200) | echo setdview > cmd_receiver |
 *  |setbrightness | set brightness (80) | echo setbrightness > cmd_receiver |
 *  |setcontrast | set contrast (80) | echo setcontrast > cmd_receiver |
 *  |sethue | set hue (80) | echo sethue > cmd_receiver
 *  |setsaturation | set saturation (80) | echo setsaturation > cmd_receiver |
 *  |setsharpness | set sharpness (80) | echo setsharpness > cmd_receiver |
 *  |setenhancedefault | set enhance to default (50) | echo setenhancedefault > cmd_receiver |
 *  |setsubtitleshow | set subtitle display | echo setsubtitleshow > cmd_receiver |
 *  |setsubtitlehide | set subtitle hide | echo setsubtitlehide > cmd_receiver |
 *  |changeaudio | set audio track to next | echo changeaudio > cmd_receiver |
 *  |changesubtitle | set subtitle track to next | echo changesubtitle > cmd_receiver |

 */
void sendcmd_handler(gchar* cmd_str)
{
	if (!strcmp(cmd_str, "play"))
	{
		goplayer_play(1);
	}
	else if(!strcmp(cmd_str, "ff"))
	{
		goplayer_play(4);
	}
	else if(!strcmp(cmd_str, "rw"))
	{
		goplayer_play(-4);
	}
	else if(!strcmp(cmd_str, "seek"))
	{
		goplayer_seek(10000);
	}
	else if(!strncmp(cmd_str, "seek_forward", 12))
	{
		double seek_percent;
		char tmp[16]="";
		strcpy(tmp,strtok(cmd_str,"seek_forward ")); 	
		seek_percent = atof(tmp); 	
		goplayer_seek_forward(seek_percent);
	}
	else if(!strncmp(cmd_str, "seek_backward", 13))
	{
		double seek_percent;
		char tmp[16]="";
		strcpy(tmp,strtok(cmd_str,"seek_backward ")); 	
		seek_percent = atof(tmp); 	
		goplayer_seek_backward(seek_percent);
	}
	else if(!strcmp(cmd_str, "pause"))
	{
		goplayer_play(0);
	}
	else if(!strcmp(cmd_str, "getcurrenttime"))
	{
		printf("[sample] current time = %d\n", goplayer_get_current_time());
	}
	else if(!strcmp(cmd_str, "gettotaltime"))
	{
		printf("[sample] total time = %d\n", goplayer_get_total_time());
	}
	else if(!strcmp(cmd_str, "isseekable"))
	{
		printf("[sample] is seekable = %d\n", goplayer_is_seekable());
	}
	else if(!strcmp(cmd_str, "getstreaminfo"))
	{
		goplayer_stream_info *streaminfo = NULL;
		int i;
		if (goplayer_get_stream_info(GOPLAYER_STREAM_INFO_TYPE_AUDIO, &streaminfo)) {
			for (i=0; i<streaminfo->count; i++) {
				printf("[sample] type = audio, Track[%d] = %s\n", \
					streaminfo->stream_info.audio_track_info[i].track_index, \
					streaminfo->stream_info.audio_track_info[i].lang_code);
			}
			goplayer_free_stream_info(streaminfo);
		}
		if (goplayer_get_stream_info(GOPLAYER_STREAM_INFO_TYPE_SUBTITLE, &streaminfo)) {
			for (i=0; i<streaminfo->count; i++) {
				printf("[sample] type = subtitle, Track[%d] = %s\n", \
					streaminfo->stream_info.subtitle_info[i].track_index, \
					streaminfo->stream_info.subtitle_info[i].lang_code);
			}
			goplayer_free_stream_info(streaminfo);
		}
		if (goplayer_get_stream_info(GOPLAYER_STREAM_INFO_TYPE_MEDIA_SIZE, &streaminfo)) {
			printf("type = media size, size=%lld\n", streaminfo->stream_info.mediaSize);
			goplayer_free_stream_info(streaminfo);
		}
	}
	else if(!strcmp(cmd_str, "getcurstreaminfo"))
	{
		goplayer_stream_info *streaminfo = NULL;
                if(goplayer_get_cur_stream_info(GOPLAYER_STREAM_INFO_TYPE_VIDEO, &streaminfo))
                {
                    printf("[sample] type = video, fourCC:%"FOURCC_FORMAT", width:%d, height:%d, frame rate:%d\n",
                        FOURCC_ARGS(streaminfo->stream_info.video_track_info->fourCC), 
                        streaminfo->stream_info.video_track_info->width,
                        streaminfo->stream_info.video_track_info->height,
                        streaminfo->stream_info.video_track_info->framerate);
                    goplayer_free_stream_info(streaminfo);
                }
		if (goplayer_get_cur_stream_info(GOPLAYER_STREAM_INFO_TYPE_AUDIO, &streaminfo)) {
			printf("[sample] type = audio, Track[0] = %s\n", \
					streaminfo->stream_info.audio_track_info[0].lang_code);
                        if(streaminfo->stream_info.audio_track_info[0].audDetailInfo)
                        {
                            stGOPLAYER_AUDIO_DETAIL_INFO *audDetailInfo = streaminfo->stream_info.audio_track_info[0].audDetailInfo;
                            printf("channels:%d, sample rate:%d, depth:%d, decoder:%s\n", audDetailInfo->channels, audDetailInfo->samplerate, 
                                audDetailInfo->depth, audDetailInfo->decName);
                        }
			goplayer_free_stream_info(streaminfo);
		}
		if (goplayer_get_cur_stream_info(GOPLAYER_STREAM_INFO_TYPE_SUBTITLE, &streaminfo)) {
			printf("[sample] type = subtitle, Track[0] = %s\n", \
				streaminfo->stream_info.subtitle_info[0].lang_code);
			goplayer_free_stream_info(streaminfo);
		}
	}
	else if(!strcmp(cmd_str, "getdownloadspeed")) 
	{
		unsigned long long dlSpeed;
		if(goplayer_get_download_speed(&dlSpeed))
		{
			printf("download speed:%llu bps\n", dlSpeed);
		}
		else
			printf("getdownloadspeed failed!!\n");
	}
	else if(!strcmp(cmd_str, "setscale"))
	{
		goplayer_set_display_rect(100, 100, 200, 200);
	}
	else if(!strcmp(cmd_str, "setbrightness"))
	{
		goplayer_set_brightness(80);
	}
	else if(!strcmp(cmd_str, "setcontrast"))
	{
		goplayer_set_contrast(80);
	}
	else if(!strcmp(cmd_str, "sethue"))
	{
		goplayer_set_hue(80);
	}
	else if(!strcmp(cmd_str, "setsaturation"))
	{
		goplayer_set_saturation(80);
	}
	else if(!strcmp(cmd_str, "setsharpness"))
	{
		goplayer_set_sharpness(80);
	}
	else if(!strcmp(cmd_str, "setenhancedefault"))
	{
		goplayer_set_enhance_default();
	}
	else if(!strcmp(cmd_str, "setsubtitleshow"))
	{
		goplayer_set_subtitle_display(1);
	}
	else if(!strcmp(cmd_str, "setsubtitlehide"))
	{
		goplayer_set_subtitle_display(0);
	}
	else if(!strcmp(cmd_str, "changeaudio"))
	{
		goplayer_change_audio(-1);
	}
	else if(!strcmp(cmd_str, "changesubtitle"))
	{
		goplayer_change_subtitle(-1);
	}
	else if(!strcmp(cmd_str, "getmediatag"))
	{
		stGOPLAYER_MEDIA_TAG mediaTag;
		goplayer_get_media_tag(&mediaTag);
		
	}
}


void Sigal_Handler(int sig)
{
	printf ("Catched signal: %d ... !!\n", sig);
	goplayer_close();
	b_exit = 1;
}


/**
 * Main function.
 * Create a player to play a stream media from uri and create a command pipe to receive external command.
 * @param argc argument count.
 * @param argv arguments const string array, argv[1] specify the target uri for test.
 * @return return 0.

 * **sample code:**

 * @snippet goplayer_sample.c main function
 */
int main(int argc, char * argv[])
{
//! [main function]
	CMDPIPE* cmdpipe;
	char* uri = NULL;

	signal (SIGINT, Sigal_Handler);

	if (argc<2)
	{
		printf ("[sample] Need uri\n");
		return 0;
	}
	uri = (char *)malloc(strlen(argv[1])+1);
	memset (uri, 0 ,sizeof (strlen(argv[1])+1));
	memcpy (uri, argv[1],strlen(argv[1]));
	cmdpipe = cmd_pipe_create(NULL);
	cmd_pipe_start(cmdpipe, sendcmd_handler);

#if 0
       goplayer_open(cb_func);
       goplayer_set_source_uri(uri, 0);

       for (;;) {
               usleep(100000);
               if (b_exit)
                       break;
       }
       goplayer_close();
#else
       int playCount = 0;
       int ret = 0;
       while(!b_exit){

               playCount++;
               printf("-------------------------------------------------------- \n");
               printf("[sample] playCount = %d\n", playCount);
               printf("-------------------------------------------------------- \n");

               goplayer_close();
               ret = goplayer_open(cb_func);
               if(ret == 0)
               {
                       goplayer_set_http_option("User-Agent:VLC/2.0.5 LibVLC/2.0.5");
                       goplayer_set_source_uri(uri, 0);
               }

               if (!b_exit){
                       sleep(5);
                       system("echo '*****************************************************************************' > /dev/console\n");
                       system("ps | grep player[_] > /dev/console ");
                       system("echo '*****************************************************************************' > /dev/console\n");
                       system("free");
                       system("echo '*****************************************************************************' > /dev/console\n");
                       sleep(10);
               }
       }
#endif
	printf("EXIT !!!\n");
	cmd_pipe_close(cmdpipe);
	if(uri)
		free(uri);

	return 0;
//! [main function]
}

