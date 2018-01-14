/**
 *  @file goplayer.h
 *  player library include files.
 *
 *  @version   1.0.0
 *  @date    2012/09/12
 *  @example goplayer_sample.c
 */

#ifndef __GOPLAYER_H__
#define __GOPLAYER_H__

/*! 
 *  @mainpage GO Player Library
 *
 *  @section intro_sec Introduction
 *
 *  The document illustreates ALi GOPlayer library. The library encapsulates 
 *  client/server structure of streaming player into APIs which is easy for 
 *  programmers developing media player.
 *
  @section legal_sec Legal Notice
  THIS DOCUMENT CONTAINS PROPRIETARY TECHNICAL INFORMATION WHICH IS THE PROPERTY OF ALI 
  CORPORATION AND SHALL NOT BE DISCLOSED TO OTHERS IN WHOLE OR IN PART, REPRODUCED, COPIED, 
  OR USED AS THE BASIS FOR DESIGN, MANUFACTURING, OR SALE OF APPARATUS WITHOUT WRITTEN 
  PERMISSION OF ALI CORPORATION
  c 2012 ALI Corporation. All rights reserved.
 */

#ifdef __cplusplus
extern "C" {
#endif

#ifndef __cplusplus
  typedef  bool; /**< bool */
#endif

/**
 *  Debug Log Marco for goplayer.
 *  Log enable if define 'GOPLAYER_DBG' in Makefile.
 */
#ifdef GOPLAYER_DBG
#define GOPLAYER_LOG(x...) printf("GOPLAYER_LOG: " x)
#else
#define GOPLAYER_LOG(x...)
#endif

/**
 *  The response of state change notices APP what current state of player. 
 *  This enumeration indicates the value of #eGOPLAYER_CALLBACK_TYPE_STATE_CHANGE.
 */
typedef enum
{
	eGOPLAYER_STATE_STOP, /**< Current state of player is stop. */
	eGOPLAYER_STATE_PLAY, /**< Current state of player is playing. */
	eGOPLAYER_STATE_PAUSE /**< Current state of player is pause. */
}eGOPLAYER_STATE;

/**
 *  GOPlayer Callback Type enumeration
 *  This enumeration indicates possible responses from goplayer via callback function #GOPLAYER_STREAM_CALLBACK.
 */
typedef enum
{
	eGOPLAYER_CBT_NONE,
	eGOPLAYER_CBT_FINISHED, /**< Response for end of media stream. */
	eGOPLAYER_CBT_STATE_CHANGE, /**< Response of state change. */
	eGOPLAYER_CBT_BUFFERING, /**< Response of buffering percentage. */
	eGOPLAYER_CBT_WARN_UNSUPPORT_AUDIO,
	/**< Warning for audio decoder doesnot support the audio type. */
	eGOPLAYER_CBT_WARN_UNSUPPORT_VIDEO,
	/**< Warning for video decoder doesnot support the video type. */
	eGOPLAYER_CBT_WARN_DECODE_ERR_AUDIO,
	/**< Warning for audio decoder decodes error. */
	eGOPLAYER_CBT_WARN_DECODE_ERR_VIDEO,
	/**< Warning for video decoder decodes error. */
	eGOPLAYER_CBT_WARN_TRICK_BOS,
	/**< Indicates player has reached beginning of stream in trick mode. */
	eGOPLAYER_CBT_WARN_TRICK_EOS,
	/**< Indicates player has reached end of stream state in trick mode. */
	eGOPLAYER_CBT_ERR_SOUPHTTP, 
	/**< Error from soup http connection. */
	eGOPLAYER_CBT_ERR_TYPE_NOT_FOUND, 
	/**< player doesn't know the stream type. */
	eGOPLAYER_CBT_ERR_DEMUX, 
	/**< demuxing fails. */
	eGOPLAYER_CBT_ERR_UNDEFINED,
	/**< a undefined error from goplayer. */
	eGOPLAYER_CBT_FRAME_CAPTURE,
	/**< Frame capture finish. It can get the captured frame from path returned. */
	eGOPLAYER_CBT_MAX, /**< Just mark the end of response enumeration. */
}eGOPLAYER_CALLBACK_TYPE;

/**
 *  Type of stream information.
 */
typedef enum
{
	GOPLAYER_STREAM_INFO_TYPE_AUDIO, /**< Type of audio information. */
	GOPLAYER_STREAM_INFO_TYPE_SUBTITLE, /**< Type of subtitle information. */
	GOPLAYER_STREAM_INFO_TYPE_VIDEO, /**< Type of video information. */
	GOPLAYER_STREAM_INFO_TYPE_PROGRAM, /**< Type of program information. */
	GOPLAYER_STREAM_INFO_TYPE_CHAPTER, /**< Type of chapter information. */
	GOPLAYER_STREAM_INFO_TYPE_MEDIA_SIZE, /**< Type of media size information. */
}eGOPLAYER_STREAM_INFO_TYPE;

/**
 *  Callback function for player to notify APP
 *  @param[out] tpye The #eGOPLAYER_CALLBACK_TYPE enumeration indicates all possible responses tpye from player.
 *  @param[in, out] data The following table description.
 
 *  | type | data | data type |
 *  | :----: | :----: | :----: |
 *  | #eGOPLAYER_CBT_STATE_CHANGE | Value of #eGOPLAYER_STATE | #eGOPLAYER_STATE |
 *  | #eGOPLAYER_CBT_BUFFERING | Value of buffering percentage [0 - 100] | int |
 *  | #eGOPLAYER_CBT_WARN_UNSUPPORT_AUDIO #eGOPLAYER_CBT_WARN_UNSUPPORT_VIDEO #eGOPLAYER_CBT_WARN_DECODE_ERR_AUDIO #eGOPLAYER_CBT_WARN_DECODE_ERR_VIDEO | Detail descripation of warning | char |
 *  | #eGOPLAYER_CBT_ERR_SOUPHTTP | Status code of soup http. -1 means it's a general error of soup http.\nThese status codes all come from open source libsoup.\nPlease refere to soup-status.h for more detailed. | int |
 *  | #eGOPLAYER_CBT_ERR_TYPE_NOT_FOUND | Detail descripation of error | char |
 *  | #eGOPLAYER_CBT_ERR_DEMUX | Detail descripation of error | char |
 *  | #eGOPLAYER_CBT_ERR_UNDEFINED | Detail descripation of error | char |
 *  | #eGOPLAYER_CBT_FRAME_CAPTURE | store path, width and height of captured frame with format /path/to/captured/frame;h=xxxx,w=xxxx. For example, the format /tmp/nmpvidcapture.yuv;h=1088,w=1920 | char |
 */
typedef void(* GOPLAYER_STREAM_CALLBACK)(eGOPLAYER_CALLBACK_TYPE type, void *data);

#define TAG_TITLE_SIZE 30 
#define TAG_ARTIST_SIZE 30
#define TAG_ALBUM_SIZE 30
#define TAG_DATE_SIZE 11
#define TAG_COMMENT_SIZE 256
#define TAG_GENRE_SIZE 30

/**
* Media tag.
* used for goplayer_get_media_tag()
*/
typedef struct {
    char title[TAG_TITLE_SIZE]; 
    char artist[TAG_ARTIST_SIZE]; 
    char album[TAG_ALBUM_SIZE]; 
    char date[TAG_DATE_SIZE]; 
    char comment[TAG_COMMENT_SIZE]; 
    char genre[TAG_GENRE_SIZE]; 
    unsigned long bitrate;
}stGOPLAYER_MEDIA_TAG;

 #define DECNAME_SIZE 6
/**
 *  Audio stream detail information.
 */
 typedef struct {
    unsigned int channels;
    unsigned int depth;
    unsigned short samplerate;
    char decName[DECNAME_SIZE]; /**< for example, mp3, aac, amr, ac3, pcm, adpcm, wma... */
}stGOPLAYER_AUDIO_DETAIL_INFO;

/**
 *  Audio stream information.
 */
typedef struct {
	unsigned int track_index;
	char lang_code[5];
    stGOPLAYER_AUDIO_DETAIL_INFO *audDetailInfo;
    /**< Audio detail information. It's only present by calling goplayer_get_cur_stream_info.*/
}stGOPLAYER_AUDIO_TRACK_INFO;

/**
 *  Subtitle stream information.
 */
typedef struct {
	unsigned int track_index;
	char lang_code[5];
}stGOPLAYER_SUBTITLE_INFO;

/**
 *  Video stream information.
 */
typedef struct {
    unsigned long fourCC;
    unsigned short width;
    unsigned short height;
    unsigned short framerate;
}stGOPLAYER_VIDEO_TRACK_INFO;

/**
 *  Program stream information.
 */
typedef struct {
	unsigned int prog_index;
}stGOPLAYER_PROGRAM_INFO;

/**
 *  Chapter stream information.
 */
typedef struct {
	unsigned int chaper_index;
}stGOPLAYER_CHAPTER_INFO;

/**
 *  Stream information: union for specified type.
 */
typedef struct {
	unsigned int count;
	eGOPLAYER_STREAM_INFO_TYPE type;
	union {
		stGOPLAYER_AUDIO_TRACK_INFO *audio_track_info;
		stGOPLAYER_SUBTITLE_INFO *subtitle_info;
		stGOPLAYER_VIDEO_TRACK_INFO *video_track_info;
		stGOPLAYER_PROGRAM_INFO *program_info;
		stGOPLAYER_CHAPTER_INFO *chapter_info;
		long long mediaSize;
	} stream_info;
}goplayer_stream_info;

/**
 *  Create a new player with the given callback function.
 *  @param[in] streamCallback Callback function for player to notify APP.
 *  @return 0 for Success; Otherwise for Fail.
 */
int goplayer_open(GOPLAYER_STREAM_CALLBACK streamCallback);

/**
 *  The function close player when no longer used or before play another.
 *  @return 0 for Success; Otherwise for Fail.
 */
int goplayer_close();

/**
 *  Set to play with rate.
 *  @param[in] rate Play rate. Range: [-128~-2, 0~128]. 0 means pause.
 *  @return TRUE for playing with rate successfully. Otherwise, return FALSE.
 */
bool goplayer_play(int rate);

/**
 *  Set to seek.
 *  @param[in] time Time position in millisecond.
 *  @return TRUE if success. Otherwise, returns FALSE.
 */
bool goplayer_seek(double time);

#if 0
/**
 *  Disable goplayer use seek operation to simulate trick mode.
 *  If the stream don't have index table, goplayer use seek operation to simulate.
 *  In this case, the performance of trick mode is bad. 
 *  If client want to disable trick mode for no index table case, 
 *  use this function to disable. And must be called before any trick operation.
 *  @return TRUE if success. Otherwise, return FALSE.
 */
bool goplayer_disable_use_seek_for_trick();
#endif

/**
 *  Get the total time of the stream currently playing.
 *  @return Total time of stream in millisecond or -1 if unknown.
 */
int goplayer_get_total_time();

/**
 *  Get the current time of the stream currently playing.
 *  @return Current time of stream in millisecond or -1 if unknown.
 */
int goplayer_get_current_time();

/**
 *  Get download speed of http stream. <b>It's only available for http stream.</b>
 *  @param[out] dlSpeed download speed of http stream. 
 *  @return TRUE if \c dlSpeed is available.
 */
bool goplayer_get_download_speed(unsigned long long *dlSpeed);

/**
 *  Check the stream is seekable or not.
 *  @return -1:haven't decided yet, 0:isn't seekable, 1:is seekable.
 */
int goplayer_is_seekable();

#if 0
/**
 *  Get video information from goplayer.
 *  <b> Will be deprecated and replaced by goplayer_get_cur_stream_info(). </b>
 *  @param[in, out] width Video width.
 *  @param[in, out] height Video height.
 *  @param[in, out] framerate Stream frame rate.
 *  @param[in, out] bitrate Stream bit rate.
 *  @return TRUE if success. Otherwise, return FALSE.
 */
bool goplayer_get_video_info(int *width, int *height, int *framerate, int *bitrate);
#endif

/**
 *  Get stream information
 *  @param[in] type specified type for stream information.
 *  @param[out] info pointer of pointer of #goplayer_stream_info to get the stream information with specified type.
 *  Remember to call #goplayer_free_stream_info if you needn't these information.
 *  @return TRUE if success. Otherwise, return FALSE.
 */
bool goplayer_get_stream_info(eGOPLAYER_STREAM_INFO_TYPE type, goplayer_stream_info **info);

/**
 *  Get current stream information
 *  @param[in] type specified type for current stream information.
 *  @param[out] info pointer of pointer of #goplayer_stream_info to get current stream information with specified type.
 *  Remember to call #goplayer_free_stream_info if you needn't these information.
 *  @return TRUE if success. Otherwise, return FALSE.
 */
bool goplayer_get_cur_stream_info(eGOPLAYER_STREAM_INFO_TYPE type, goplayer_stream_info **info);

/**
 *  Frees the memory allocated by #goplayer_get_stream_info or #goplayer_get_cur_stream_info.
 *  @param[in] info A #goplayer_stream_info pointer.
 *  @return TRUE if success. Otherwise, return FALSE.
 */
bool goplayer_free_stream_info(goplayer_stream_info *info);

/**
 *  To change display position and dimension.
 *  @param[in] x X position to display.
 *  @param[in] y Y position to display.
 *  @param[in] width Width to be scale.
 *  @param[in] height Height to be scale.
 */
void goplayer_set_display_rect(int x, int y, unsigned int width, unsigned int height);

/**
 *  Set brightness of display.
 *  @param[in] grade Range: 0 - 100 Default: 50
 */
void goplayer_set_brightness(unsigned int grade);

/**
 *  Set contrast of display.
 *  @param[in] grade Range: 0 - 100 Default: 50
 */
void goplayer_set_contrast(unsigned int grade);

/**
 *  Set hue of display.
 *  @param[in] grade Range: 0 - 100 Default: 50
 */
void goplayer_set_hue(unsigned int grade);

/**
 *  Set saturation of display.
 *  @param[in] grade Range: 0 - 100 Default: 50
 */
void goplayer_set_saturation(unsigned int grade);

/**
 *  Set sharpness of display.
 *  @param[in] grade Range: 0 - 100 Default: 50
 */
void goplayer_set_sharpness(unsigned int grade);

/**
 *  Set brightness, contrast, hue, saturation and sharpness to default value.
 */
void goplayer_set_enhance_default();
    
/**
 *  Set the URI of media stream (and subtile) for playing.
 *  @param[in] uri The URI of media stream. The delimiter if them is ";"
 *  @param[in] start_time Start time in millisecond to play.
 *  @note uri format is "file:///usb/xxx.avi;file:///usb/xxx.srt;file:///usb/xxx.srt" or "file:///usb/xxx.avi;file:///usb/xxx.sub*file:///usb/xx.idx"
 */
bool goplayer_set_source_uri(const char *uri, unsigned int start_time);

/**
 *  Specify "User-Agent:" and "Cookies:" in http header.
 *  @param[in] header_fields String of User-Agent and Cookies. The delimiter of them is "\n".
 */
bool goplayer_set_http_option(char *header_fields);

/**
 *  Specify "proxy:", "proxy-id:" and "proxy-pw:" for authentication.
 *  @param[in] proxy_info String of proxy, proxy-id and proxy-pw. The delimiter of them is "\n".
 *  @note proxy_info format is "proxy:xxx.xxx.xx\nproxy-id:xxx\nproxy-pw:xx"
 */
bool goplayer_set_proxy(char *proxy_info);

/**
 *  Specify "user-id:" and "user-pw:" for authentication.
 *  @param[in] auth_info String of user-id and user-pw. The delimiter if them is "\n".
 */
bool goplayer_set_authentication(char *auth_info);

/**
 *  Set maximum buffering time in the buffering queue. 
 *  The unit is second.
 *  @image html buffering_queue.PNG "buffering queue diagram"
 *  @image rtf buffering_queue.PNG "buffering queue diagram"
 *  @image latex buffering_queue.PNG "buffering queue diagram" width=10cm
 *  @param[in] time Maximum buffering time in the buffering queue. 
 *  Default value is 20 seconds and we recommend using the default value.
 *  @param[in] low_percent Low percentage threshold of @e time to start buffering.
 *  @param[in] high_percent High percentage threshold of @e time to finish buffering.
 */
void goplayer_set_buffering_time(unsigned int time, unsigned int low_percent, unsigned int high_percent);
      
/**
 *  Change audio stream with given track index.
 *  @param[in] trackIdx Track index. Player can get information of track index from #goplayer_get_stream_info.
 *  If track index is invalid, server just ignores the command.
 *  If the given track index is -1, server switch to next audio stream circularly.
 */      
void goplayer_change_audio(int trackIdx);

/**
 *  Change subtitle stream with given track index.
 *  @param[in] trackIdx Track index. Player can get information of track index from #goplayer_get_stream_info.
 *  If track index is invalid, server just ignores the command.
 *  If the given track index is -1, server switch to next subtitle stream circularly.
 */
void goplayer_change_subtitle(int trackIdx);

/**
 *  Change video stream with given track index.
 *  @param[in] trackIdx Track index. Player can get information of track index from #goplayer_get_stream_info.
 *  If track index is invalid, server just ignores the command.
 *  If the given track index is -1, server switch to next subtitle stream circularly.
 */
bool goplayer_change_vidio(int trackIdx);

/**
 *  Change program stream with given program index.
 *  @param[in] progIdx Program index. Player can get information of track index from #goplayer_get_stream_info.
 *  If track index is invalid, server just ignores the command.
 *  If the given track index is -1, server switch to next subtitle stream circularly.
 */
bool goplayer_change_prog(int progIdx);

/**
 *  Change chapter stream with given chapter index.
 *  @param[in] chapId Chapter index. Player can get information of track index from #goplayer_get_stream_info.
 *  If track index is invalid, server just ignores the command.
 *  If the given track index is -1, server switch to next subtitle stream circularly.
 */
bool goplayer_change_chapter(int chapId);

/**
 *  Set volume with specified value.
 *  @param[in] volume Specified volume value to be set.
 *  @return TRUE if success. Otherwise, return FALSE.
 */
bool goplayer_set_volume(int volume);

/**
 *  Get current volume value.
 *  @return Current volume value; return -1 if unavailable.
 */
int goplayer_get_volume(void);

/**
 *  Set volume to mute.
 *  @param[in] b_mute Boolean for mute or not.
 *  @return TRUE if success. Otherwise, return FALSE.
 */
bool goplayer_set_volume_mute(bool b_mute);


/**
 *  Get last callback ststus.
 *  @return Current callback status of #eGOPLAYER_CALLBACK_TYPE.
 */
eGOPLAYER_CALLBACK_TYPE goplayer_get_return_status(void);

/**
 *  Set display visibility.
 *  @param[in] visibility Boolean for visibility.
 *  @return TRUE if success. Otherwise, return FALSE.
 */
bool goplayer_set_visibility(bool visibility);

/**
 *  Get current play rate.
 *  @return Current play rate.
 */
int goplayer_get_cur_play_rate(void);

/**
 *  Set HTTP option to server for get license.
 *  @param[in] httpopt HTTP option to be set.
 */
bool goplayer_set_playready_httpopt(const char *httpopt);

/**
 *  Set subtitle display on/off.
 *  @param[in] onoff Display or hide.
 */
void goplayer_set_subtitle_display(bool onoff);

/**
 *  Set video display on/off.
 *  @param[in] onoff Display or hide.
 */
void goplayer_set_video_display(bool onoff);

/**
 *  Get media tag
 *  @param[in] mediaTag a pointer of structure #stGOPLAYER_MEDIA_TAG
 *  @return TRUE if get media tag success.
 */
bool goplayer_get_media_tag(stGOPLAYER_MEDIA_TAG *mediaTag);

/**
 *  Set frame capture mode.
 *  Capture the first frame after #goplayer_set_source_uri (). 
 *  Should be called before #goplayer_set_source_uri () if you want to enter frame capture mode.
 *  When frame capture finish, it callback with #eGOPLAYER_CBT_FRAME_CAPTURE.
 *  And the only step you can do next is close player by calling #goplayer_close(). Othwise, the behavior is undefined.
 */
void goplayer_set_frame_capture_mode();
#ifdef __cplusplus
}
#endif
  
#endif /* __GOPLAYER_H__ */
