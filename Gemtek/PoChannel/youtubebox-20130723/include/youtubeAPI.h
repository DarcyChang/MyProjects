#ifndef YOUTUBEAPI_H
#define YOUTUBEAPI_H

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <sys/types.h>
#include <sys/file.h>
#include <json/json.h>
#include <libconfig.h>


/* The channel type */
typedef enum {
	CHTYPE_YOUTUBE_MOST_VIEW = 1000,
	CHTYPE_YOUTUBE_WATCH_LATER = 1001,
	CHTYPE_YOUTUBE_PLAYLIST = 1002,
	CHTYPE_YOUTUBE_SUBSCRIPTION = 1003,
	CHTYPE_YOUTUBE_KEYWORD = 1004,
	CHTYPE_YOUTUBE_PERSONAL_PLAYLIST = 1005,
	CHTYPE_MAX
} CHTYPE;

typedef struct XMLlist {
	char *entry_title;
	char *entry_published;
	char *entry_updated;
	char *entry_playlistId;
	char *media_videoId;
	char *media_uploaderId;
	char *media_thumbnail;
	char *media_link;
	char *author_name;
	char *author_url;
	char *author_id;
} XMLlist_t;

typedef struct youtubeInParamStruct {
	int chNum;
	int chType; // 1000, 1001, 1003, 1002, 1005...
	char access_key[128];
	char developerId[128]; // API KEY
	char keyword[256];
	char pageToken[16];
	int maxResults; // 1~50, default 5
	
} youtubeInParam_t;
	
typedef struct youtubeOutParamStruct {
	int totalCnt; // output param totalCnt of this page
	char prevPageToken[16]; // output param
	char nextPageToken[16]; // output param
	json_object *jsonOut;
} youtubeOutParam_t;

/**
 *  Get youtube playlist info
 *  @param[in] <youtubeparam> input parameters for query playlist info
 *  @param[out] <result> output for totalCnt, prevPageToken, nextPageToken and put playlist items in jsonOut
 *  @return 0 for Success; Otherwise for Fail.
 */
extern int get_youtube_info_v3(youtubeInParam_t *youtubeparam, youtubeOutParam_t *result);

extern XMLlist_t **get_playlist_info(char *token,char *url,char *orderby,int start_index,int max_result,int *max);
extern XMLlist_t **get_watch_later_info(char *token,char *orderby,int start_index,int max_result,int *max);
extern XMLlist_t **get_subscription_info(char *token,char *url,char *orderby,int start_index,int max_result,int *max);
extern XMLlist_t **get_mostviewed_info(char *token,char *orderby,int start_index,int max_result,int *max);
extern XMLlist_t **get_query_info(char *token,char *search_word,char *orderby,int start_index,int max_result,int *max);

extern XMLlist_t **get_upload_info(char *token,char *user_id,int *max);
extern XMLlist_t *get_program_info(char *token,char *video_id);
extern XMLlist_t **parser_all_info(unsigned int chNum, int *max);
extern XMLlist_t *parser_program_info(unsigned int chNum,int index);

extern void get_video_sig(XMLlist_t* list,char *sig,char *url);
extern void get_video_reallink(XMLlist_t* list);
extern void free_info(XMLlist_t *list);
extern void get_account_info(char *token,char *user_account,char *search_word,char *value);
extern void get_token_info(char *token);
extern int get_access_token(char *token);
extern XMLlist_t **get_xml_predl(int chNum, int pageNo, int *max);
extern XMLlist_t **get_xml_alimain(int chNum, int pageNo, int *max);

#endif

