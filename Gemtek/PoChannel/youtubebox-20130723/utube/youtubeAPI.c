#include <stdio.h>
#include <string.h>
#include <stdlib.h> 
#include <libxml/xmlmemory.h>
#include <libxml/parser.h>
#include "youtubeAPI.h"

#if 1
#define DBGMSG(fmt, args...) printf("=YoutubeAPI=[%s(%d)] " fmt, __FUNCTION__, __LINE__, ##args)
#else
#define DBGMSG(fmt, args...)
#endif

#define system_exec(fmt, args...) \
	do { \
		char cmd[2048]; \
		snprintf(cmd, sizeof(cmd), fmt, ##args); \
		DBGMSG("%s\n", cmd); \
		system(cmd); \
	} while (0)


void set_default_value(XMLlist_t *list)
{
	list->author_name = strdup("null");
	list->author_url = strdup("null");
	list->author_id = strdup("null");
	list->entry_title = strdup("null");
	list->entry_playlistId = strdup("null");
	list->entry_published = strdup("null");
	list->entry_updated = strdup("null");
	list->media_thumbnail = strdup("null");
	list->media_videoId = strdup("null");
	list->media_uploaderId = strdup("null");
	list->media_link = strdup("null");
}

static void parser_author(xmlDocPtr doc,xmlNodePtr cur,XMLlist_t *list)
{
	xmlChar *key = NULL;

	// Get the childern Element Node of "author" node
	cur = cur->xmlChildrenNode;

	while (cur != NULL) 
	{
		// check for "name" childern element node of "author" node
		if ((!xmlStrcmp(cur->name, (const xmlChar *)"name")))
		{
			key = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
			if(key != NULL)
				list->author_name= strdup((char*)key);

			xmlFree(key);
		} // end of If loop "name"

		// check for "uri" childern element node of "author" node
		if ((!xmlStrcmp(cur->name, (const xmlChar *)"uri")))
		{
			key = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
			if(key != NULL)
			list->author_url= strdup((char*)key);

			xmlFree(key);
		} // end of If loop "name"

		// check for "userId" childern element node of "author" node
		if ((!xmlStrcmp(cur->name, (const xmlChar *)"userId")))
		{
			key = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
			if(key != NULL)
			list->author_id= strdup((char*)key);

			xmlFree(key);
		} // end of If loop "author_Id"

		cur = cur->next;
	}
}

static void parser_media(xmlDocPtr doc,xmlNodePtr cur,XMLlist_t *list)
{

	xmlChar *key = NULL;
	xmlAttrPtr attr = NULL;

	// Get the childern Element Node of "media" node
	cur = cur->xmlChildrenNode;

	while (cur != NULL) 
	{

		// check for "thumbnail" childern element node of "media" node
		if ((!xmlStrcmp(cur->name, (const xmlChar *)"thumbnail"))) 
		{
			// search for "name" attribute in the "thumbnail" node
			attr = xmlHasProp(cur, (const xmlChar*)"name");

			if(attr != NULL)
			{
				key = xmlGetProp(cur, (const xmlChar*)"name");				
				/*if((!xmlStrcmp(key,(const xmlChar *)"sddefault")))
				{  
					xmlFree(key);
					key = xmlGetProp(cur, (const xmlChar*)"url");
					if(key != NULL)
						list->media_thumbnail = strdup((char*)key);
				}
				else if((!xmlStrcmp(key,(const xmlChar *)"hddefault")))
				{
					xmlFree(key);
					key = xmlGetProp(cur, (const xmlChar*)"url");
					if(key != NULL)
						list->media_thumbnail = strdup((char*)key);
				}*/
				if((!xmlStrcmp(key,(const xmlChar *)"mqdefault")))
				{
					xmlFree(key);
					key = xmlGetProp(cur, (const xmlChar*)"url");
					if(key != NULL)
						list->media_thumbnail = strdup((char*)key);
				}
				else if((!xmlStrcmp(key,(const xmlChar *)"default")))
				{
					xmlFree(key);
					key = xmlGetProp(cur, (const xmlChar*)"url");
					if(key != NULL)
						list->media_thumbnail = strdup((char*)key);
				}
				xmlFree(key);
			}
		} // end of IF loop " thumbnail"

		// check for "videoid" childern element node of "media" node
		if ((!xmlStrcmp(cur->name, (const xmlChar *)"videoid")))
		{
			key = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
			if(key != NULL)
				list->media_videoId = strdup((char*)key);

			xmlFree(key);
		} // end of If loop "videoid"

		// check for "uploaderId" childern element node of "media" node
		if ((!xmlStrcmp(cur->name, (const xmlChar *)"uploaderId")))
		{
			key = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
			if(key != NULL)
				list->media_uploaderId = strdup((char*)key);

			xmlFree(key);
		} // end of If loop "uploader_Id"
		cur = cur->next;
	}
}

static void parser_entry (xmlDocPtr doc, xmlNodePtr cur, XMLlist_t *list) 
{
	xmlChar *key = NULL;
	xmlAttrPtr attr = NULL;
	
	// Get the childern Element Node of "entry" node
	cur = cur->xmlChildrenNode;

	while (cur != NULL) 
	{
		// check for "title" childern element node of "entry" node
		if ((!xmlStrcmp(cur->name, (const xmlChar *)"title")))
		{
			key = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);

			if(key != NULL)
				list->entry_title = strdup((char*)key);

			xmlFree(key);
		} // end of If loop "title"    

		// check for "published" childern element node of "entry" node
		if ((!xmlStrcmp(cur->name, (const xmlChar *)"published")))
		{
			key = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
			if(key != NULL)
				list->entry_published = strdup((char*)key);     

			xmlFree(key);
		} // end of If loop "published"

		// check for "updated" childern element node of "entry" node
		if ((!xmlStrcmp(cur->name, (const xmlChar *)"updated")))
		{
			key = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
			if(key != NULL)
				list->entry_updated = strdup((char*)key);

			xmlFree(key);
		} // end of If loop "updated"

		// check for "thumbnail" childern element node of "entry" node
		if ((!xmlStrcmp(cur->name, (const xmlChar *)"thumbnail")))
		{
			// search for "url" attribute in the "thumbnail" node
			attr = xmlHasProp(cur, (const xmlChar*)"url");

			if(attr != NULL)
			{
				key = xmlGetProp(cur, (const xmlChar*)"url");
				if(key != NULL)
					list->media_thumbnail= strdup((char*)key);
				       
				xmlFree(key);	
			}
			else
				 list->media_thumbnail = strdup("null");
		} // end of If loop "published"

		if ((!xmlStrcmp(cur->name, (const xmlChar *)"playlistId")))
		{
			key = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
			if(key != NULL)
				list->entry_playlistId= strdup((char*)key);

			xmlFree(key);
		} // end of If loop "updated"

		if ((!xmlStrcmp(cur->name, (const xmlChar *)"author"))) 
		{
			parser_author(doc, cur, list);
		} // end of IF loop " author"

		if ((!xmlStrcmp(cur->name, (const xmlChar *)"group"))) 
		{
			parser_media(doc, cur, list);
		} // end of IF loop " media"

		cur = cur->next;
	} // end of While loop
} // end of parseURL function()
	
/*
 * Parsing the XML file and Reading the Element Nodes
 */
static XMLlist_t **parser_doc (char *xmlFileName,int *max) 
{
	xmlDocPtr doc;  // pointer to parse xml Document
	xmlNodePtr cur; // node pointer. It interacts with individual node
	int index=0;
	XMLlist_t **list=NULL;
	
	// Parse XML file 
	doc = xmlParseFile(xmlFileName);

	// Check to see that the document was successfully parsed.
	if (doc == NULL ) {
		DBGMSG("Error!. Document is not parsed successfully. \n");
		return NULL;
	}

	// Retrieve the document's root element.
	cur = xmlDocGetRootElement(doc);

	// Check to make sure the document actually contains something
	if (cur == NULL) {
		DBGMSG("Document is Empty\n");
		xmlFreeDoc(doc);
		return NULL;
	}  

	/* We need to make sure the document is the right type. 
	* "root" is the root type of the documents used in user Config XML file 
	*/
	if (xmlStrcmp(cur->name, (const xmlChar *) "feed") && xmlStrcmp(cur->name, (const xmlChar *) "entry")) {
		DBGMSG("Document is of the wrong type, root node != feed or entry\n");
		xmlFreeDoc(doc);
		return NULL;
	}

	/* Get the first child node of cur.
	* At this point, cur points at the document root, 
	* which is the element "root"
	*/
	if((!xmlStrcmp(cur->name, (const xmlChar *) "feed")))
		cur = cur->xmlChildrenNode;

	index = 0;

	// This loop iterates through the elements that are children of "root"
	while (cur != NULL) 
	{
		if ((!xmlStrcmp(cur->name, (const xmlChar *)"entry")))
		{
			list = (XMLlist_t **)realloc(list,(index+1)*sizeof(XMLlist_t));
			list[index] = (XMLlist_t *)malloc(sizeof(XMLlist_t));
			set_default_value(list[index]);
			parser_entry(doc, cur, list[index]);   

			//if(strcmp(list[index]->media_videoId,"null"))
			//	get_video_reallink(list[index]);

			index++;
		}
		cur = cur->next;
	}
	*max = index;
	/* Save XML document to the Disk
	* Otherwise, you changes will not be reflected to the file.
	* Currently it's only in the memory
	*/
	xmlSaveFormatFile (xmlFileName, doc, 1);

	/*free the document */
	xmlFreeDoc(doc);

	/*
	* Free the global variables that may
	* have been allocated by the parser.
	*/
	xmlCleanupParser();  

	return list;
} // end of XMLParseDoc function

/*
 * Parsing the XML file and Reading the Element Nodes
 */
static XMLlist_t *parser_video_doc (char *xmlFileName) 
{
	xmlDocPtr doc;  // pointer to parse xml Document
	xmlNodePtr cur; // node pointer. It interacts with individual node
	XMLlist_t *list = NULL;
	
	// Parse XML file 
	doc = xmlParseFile(xmlFileName);

	// Check to see that the document was successfully parsed.
	if (doc == NULL ) {
		DBGMSG("Error!. Document is not parsed successfully. \n");
		return NULL;
	}

	// Retrieve the document's root element.
	cur = xmlDocGetRootElement(doc);

	// Check to make sure the document actually contains something
	if (cur == NULL) {
		DBGMSG("Document is Empty\n");
		xmlFreeDoc(doc);
		return NULL;
	}  

	/* We need to make sure the document is the right type. 
	* "root" is the root type of the documents used in user Config XML file 
	*/
	if (xmlStrcmp(cur->name, (const xmlChar *) "feed") && xmlStrcmp(cur->name, (const xmlChar *) "entry")) {
		DBGMSG("Document is of the wrong type, root node != feed or entry\n");
		xmlFreeDoc(doc);
		return NULL;
	}

	/* Get the first child node of cur.
	* At this point, cur points at the document root, 
	* which is the element "root"
	*/
	if((!xmlStrcmp(cur->name, (const xmlChar *) "feed")))
		cur = cur->xmlChildrenNode;

	// This loop iterates through the elements that are children of "root"
	while (cur != NULL) 
	{
		if ((!xmlStrcmp(cur->name, (const xmlChar *)"entry")))
		{
			list = (XMLlist_t *)malloc(sizeof(XMLlist_t));
			set_default_value(list);
			parser_entry(doc, cur, list);   
		}
		cur = cur->next;
	}

	/* Save XML document to the Disk
	* Otherwise, you changes will not be reflected to the file.
	* Currently it's only in the memory
	*/
	xmlSaveFormatFile (xmlFileName, doc, 1);
	/*free the document */
	xmlFreeDoc(doc);
	/*
	* Free the global variables that may
	* have been allocated by the parser.
	*/
	xmlCleanupParser();  

	return list;
} // end of XMLParseDoc function

void get_video_sig(XMLlist_t* list,char *sig,char *url)
{
	FILE *fp;
	char *resolution[2] = {"22","18"};
	int j=0;

	memset(url,'\0',sizeof(url));
	memset(sig,'\0',sizeof(sig));

	for(j=0;j<2;j++)
	{
		DBGMSG("parser video_sig [%d], resolution:%s\n", j, resolution[j]);

		//system_exec("wget -O /tmp/videos --user-agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36' 'http://www.youtube.com/get_video_info?video_id=%s' >/dev/null 2>&1", list->media_videoId);
		system_exec("wget -O /tmp/videos --user-agent='Mozilla/5.0 (ipad; CPU OS 5_1 like Mac OS X ) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari' 'http://www.youtube.com/get_video_info?video_id=%s' >/dev/null 2>&1", list->media_videoId);

		system_exec("url_decode.sh %s", resolution[j]);

		fp=fopen("/tmp/sig.txt","r+");
		if(!fp)
			DBGMSG("can't open /tmp/sig.txt file\n");  
		else
		{
			fgets(sig,200,fp);
			fclose(fp);
		}
		
		fp=fopen("/tmp/url.txt","r+");
		if(!fp)
			DBGMSG("can't open /tmp/url.txt file\n");
		else
		{
			fgets(url,1024,fp);
			fclose(fp); 
		}
		
		DBGMSG("url:%s, sig:%s\n", url, sig);
		
		if(!strcmp(url,"")==0 && !strcmp(sig,"")==0)
			break;

	}
}

void get_video_reallink(XMLlist_t* list)
{
	char video_sig[200],video_url[1024];
	
	get_video_sig(list,video_sig,video_url);

	if(!strcmp(video_url,"")==0)
	{
		list->media_link = malloc(sizeof(char)*(sizeof(video_url)+sizeof(video_sig)+11));
		if(strstr(video_url,"url=") != NULL)
			sprintf(list->media_link,"%s&signature=%s",video_url+4,video_sig);
		else
			sprintf(list->media_link,"%s&signature=%s",video_url,video_sig);
	}
	system("rm -rf /tmp/videos /tmp/sig.txt /tmp/url.txt /tmp/sig1.txt /tmp/wget-log*");
}

void free_info(XMLlist_t *list)
{
	free(list->entry_title);
	list->entry_title = NULL;
	free(list->author_name);
	list->author_name = NULL;
	free(list->author_id);
	list->author_id = NULL;
	free(list->author_url);
	list->author_url = NULL;
	free(list->entry_published);
	list->entry_published = NULL;
	free(list->entry_updated);
	list->entry_updated = NULL;
	free(list->media_thumbnail);
	list->media_thumbnail= NULL;
	free(list->media_videoId);
	list->media_videoId = NULL;
	free(list->media_uploaderId);
	list->media_uploaderId = NULL;
	free(list->media_link);
	list->media_link = NULL;
	free(list->entry_playlistId);
	list->entry_playlistId = NULL;
	free( list);
	list = NULL;
}

int get_access_token(char *token)
{
	int shift_num=0;
   	char search_word[] = {"access_token"};
	int word_size = 0;
	char *pos1,*pos2;
	FILE *fp;
	char buf[150];
	
	memset(buf,'\0',sizeof(buf));
	memset(token,'\0',sizeof(token));

	system_exec("curl https://accounts.google.com/o/oauth2/token -o /tmp/refresh_token.html -d \"client_id=443051022796.apps.googleusercontent.com&client_secret=toCHPxayGFGKDnd0-qjZcZ4g&refresh_token=1/z0GHvJhZIzglVFwjEudm-5Lk4DfOUKMWp0MtlBDEkU8&grant_type=refresh_token\" -k >/dev/null 2>&1");

	fp=fopen("/tmp/refresh_token.html","r+");
	if(!fp)
	{
		DBGMSG("can't open /tmp/refresh_token.html file\n");
		return -1;
	}

	word_size = strlen(search_word);

	while(!feof(fp))
	{
		fgets(buf,150,fp);
		pos1 = strstr(buf,search_word);
		if(pos1 != NULL)
		{	
			shift_num = (pos1-buf)+word_size+5;
			pos2=strchr(buf+shift_num,'\"');
			strncpy(token,buf+shift_num,pos2-pos1-(word_size+5));
			fclose(fp);
			return 0;
		}
	}
	fclose(fp);
	return 0;
}

void get_token_info(char *token)
{
	int shift_num=0;
	char search_word[] = {"token"};
	int word_size = 0;
	char *pos1,*pos2;
	FILE *fp;
	char buf[150];

	memset(buf,'\0',sizeof(buf));
	memset(token,'\0',sizeof(token));

	system_exec("curl -X GET https://176.32.87.225:9090/gccu/v2/login -o /tmp/token.html -d '{\"deviceModel\":\"WMTA-174N\",\"deviceSN\":\"GMH130124000054\",\"bindingStatus\":\"0\", \"deviceMAC\":\"20:10:7A:CB:F5:71\"}' -H 'Content-Type: application/json' -k >/dev/null 2>&1");

	fp=fopen("/tmp/token.html","r+");
	if(!fp)
	{
		DBGMSG("can't open /tmp/user_info.html file\n");
		return;
	}

	word_size = strlen(search_word);

	while(!feof(fp))
	{

		fgets(buf,150,fp);
		pos1 = strstr(buf,search_word);
		if(pos1 != NULL)
		{	
			 shift_num = (pos1-buf)+word_size+3;
			 pos2=strchr(buf+shift_num,'\"');
			 strncpy(token,buf+shift_num,pos2-pos1-(word_size+3));
			 fclose(fp);
			 return;
		}
	}
   	fclose(fp);

}

void get_account_info(char *token,char *user_account,char *search_word,char *value)
{
	int shift_num=0;
	int word_size=0;
	char *pos1,*pos2;
	FILE *fp;
	char buf[512];

	memset(buf,'\0',sizeof(buf));

	word_size = strlen(search_word);

	system_exec("curl -X GET https://176.32.87.225:9090/ytbox/v1/account_info -o /tmp/user_info.html -d '{\"cloudId\": \"\",\"youtubeAccount\":\"%s\"}' -H 'Authorization:%s' -H 'Content-Type: application/json' -k >/dev/null 2>&1", user_account, token);

	fp=fopen("/tmp/user_info.html","r+");
	if(!fp)
	{
		DBGMSG("can't open /tmp/user_info.html file\n");
		return;
	}

	while(!feof(fp))
	{
		fgets(buf,512,fp);
		pos1 = strstr(buf,search_word);
		if(pos1 != NULL)
		{	
			shift_num = (pos1-buf)+word_size+3;
			pos2=strchr(buf+shift_num,'\"');
			strncpy(value,buf+shift_num,pos2-pos1-(word_size+3));
			fclose(fp);
			return;
		}
	}
	fclose(fp);
}

XMLlist_t **get_watch_later_info(char *token,char *orderby,int start_index,int max_result,int *max)
{
	if(start_index > 0)
		system_exec("curl -o /tmp/watch_info.xml -H 'Authorization:Bearer %s' 'https://gdata.youtube.com/feeds/api/users/default/watch_later?start-index=%d&max-results=%d&v=2.1' -k >/dev/null 2>&1", token, start_index, max_result);
	else
		system_exec("curl -o /tmp/watch_info.xml -H 'Authorization:Bearer %s' 'https://gdata.youtube.com/feeds/api/users/default/watch_later?max-results=%d&v=2.1' -k >/dev/null 2>&1", token, max_result);

	return parser_doc("/tmp/watch_info.xml",max);
}

XMLlist_t **get_upload_info(char *token,char *user_id,int *max)
{
	system_exec("curl -o /tmp/upload_info.xml -H 'Authorization:Bearer %s' 'https://gdata.youtube.com/feeds/api/users/%s/uploads' -k >/dev/null 2>&1", token, user_id);

	return parser_doc("/tmp/upload_info.xml",max);
}

XMLlist_t **get_playlist_info(char *token,char *url,char *orderby,int start_index,int max_result,int *max)
{
	char buf[128];
	int shift_num=0;
	char *pos;

	memset(buf,'\0',sizeof(buf));

	pos = strstr(url,"v=2");
	shift_num = pos - url;
	strncpy(buf,url,shift_num);

	if(start_index > 1)
		system_exec("curl -o /tmp/playlist_info.xml -H 'Authorization:Bearer %s' '%sstart-index=%d&max-results=%d&v=2.1' -k >/dev/null 2>&1", token, buf, start_index, max_result);
	else
		system_exec("curl -o /tmp/playlist_info.xml -H 'Authorization:Bearer %s' '%smax-results=%d&v=2.1' -k >/dev/null 2>&1", token, buf, max_result);

	return parser_doc("/tmp/playlist_info.xml",max);
}

XMLlist_t **get_subscription_info(char *token,char *url,char *orderby,int start_index,int max_result,int *max)
{
	char buf[128];
	int shift_num=0;
	char *pos;

	memset(buf,'\0',sizeof(buf));

	pos = strstr(url,"v=2");
	shift_num = pos - url;
	strncpy(buf,url,shift_num);

	if(start_index>1)
		system_exec("curl -o /tmp/sub_info.xml -H 'Authorization:Bearer %s' '%sstart-index=%d&max-results=%d&v=2.1' -k >/dev/null 2>&1", token, buf, start_index, max_result);
	else
		system_exec("curl -o /tmp/sub_info.xml -H 'Authorization:Bearer %s' '%smax-results=%d&v=2.1' -k >/dev/null 2>&1", token, buf, max_result);

	return parser_doc("/tmp/sub_info.xml",max);
   
}

XMLlist_t **get_mostviewed_info(char *token,char *orderby,int start_index,int max_result,int *max)
{
	if(start_index > 1)
		system_exec("curl -o /tmp/mostview_info.xml -H 'Authorization:Bearer %s' 'https://gdata.youtube.com/feeds/api/standardfeeds/most_viewed?start-index=%d&max-results=%d&v=2.1' -k >/dev/null 2>&1", token, start_index, max_result);
	else
		system_exec("curl -o /tmp/mostview_info.xml -H 'Authorization:Bearer %s' 'https://gdata.youtube.com/feeds/api/standardfeeds/most_viewed?max-results=%d&v=2.1' -k >/dev/null 2>&1", token, max_result);

	return parser_doc("/tmp/mostview_info.xml",max);
}


XMLlist_t **get_query_info(char *token,char *search_word,char *orderby,int start_index,int max_result,int *max)
{
	if(start_index > 1)
		system_exec("curl -o /tmp/keyword_info.xml -H 'Authorization:Bearer %s' 'https://gdata.youtube.com/feeds/api/videos?q=%s&start-index=%d&max-results=%d&v=2.1' -k >/dev/null 2>&1", token, search_word, start_index, max_result);
	else
		system_exec("curl -o /tmp/keyword_info.xml -H 'Authorization:Bearer %s' 'https://gdata.youtube.com/feeds/api/videos?q=%s&max-results=%d&v=2.1' -k >/dev/null 2>&1", token, search_word, max_result);

	return parser_doc("/tmp/keyword_info.xml",max);
}

XMLlist_t *get_program_info(char *token,char *video_id)
{
	system_exec("curl -o /tmp/program_info.xml -H 'Authorization:Bearer %s' 'https://gdata.youtube.com/feeds/api/videos/%s?v=2.1' -k >/dev/null 2>&1", token, video_id);
	
	return parser_video_doc ("/tmp/program_info.xml"); 
}

XMLlist_t **parser_all_info(unsigned int chNum, int *max)
{
	XMLlist_t **programs = NULL;
	char video_sig[200], video_url[1024], file_path[128];
	FILE *fp;	int k, kmax;	

	snprintf(file_path, sizeof(file_path), "/tmp/ch/%d/ch.xml", chNum);

	fp = fopen(file_path,"r");
	if(fp)
		programs =   parser_doc(file_path, max);	
	else
		return NULL;
	
	kmax = *max;	
	if(kmax > 0) {	
		for(k=0; k<kmax; k++) {	
			snprintf(file_path, sizeof(file_path), "/tmp/ch/%d/%d.sig", chNum, k);		
			fp = fopen(file_path, "r");		
			if(fp) {			
				fgets(video_sig, sizeof(video_sig), fp);		
				fclose(fp);	
			}			
			snprintf(file_path, sizeof(file_path), "/tmp/ch/%d/%d.url", chNum, k);	
			fp = fopen(file_path, "r");		
			if(fp) {				
				fgets(video_url, sizeof(video_url), fp);	
				fclose(fp);			
			}			
			if(0 != strcmp(video_url, "")) {	
				programs[k]->media_link = malloc(sizeof(char)*(sizeof(video_url)+sizeof(video_sig)+11));	
				if(strstr(video_url, "url=") != NULL)	
					sprintf(programs[k]->media_link, "%s&signature=%s", video_url+4, video_sig);		
				else				
					sprintf(programs[k]->media_link, "%s&signature=%s", video_url, video_sig);	
				}		
			}	
		}	
	return programs;
}

XMLlist_t *parser_program_info(unsigned int chNum,int index)
{
	XMLlist_t *programs = NULL;
	char video_sig[200], video_url[1024], file_path[128];
	FILE *fp;	

	snprintf(file_path, sizeof(file_path), "/tmp/ch/%d/ch_%d.xml", chNum,index);

	fp = fopen(file_path,"r");
	if(fp)
		programs =  parser_video_doc(file_path);	
	else
		return NULL;

	snprintf(file_path, sizeof(file_path), "/tmp/ch/%d/%d.sig", chNum, index);		
	fp = fopen(file_path, "r");		
	if(fp) {			
		fgets(video_sig, sizeof(video_sig), fp);		
		fclose(fp);	
	}			

	snprintf(file_path, sizeof(file_path), "/tmp/ch/%d/%d.url", chNum, index);	
	fp = fopen(file_path, "r");		
	if(fp) {				
		fgets(video_url, sizeof(video_url), fp);	
		fclose(fp);			
	}			
	if(0 != strcmp(video_url, "")) {	
		programs->media_link = malloc(sizeof(char)*(sizeof(video_url)+sizeof(video_sig)+11));	
		if(strstr(video_url, "url=") != NULL)	
			sprintf(programs->media_link, "%s&signature=%s", video_url+4, video_sig);		
		else				
			sprintf(programs->media_link, "%s&signature=%s", video_url, video_sig);	
	}	

	return programs;
}

XMLlist_t **get_xml_predl(int chNum, int pageNo, int *max)
{
	char filepath[128];
	snprintf(filepath, sizeof(filepath), "/tmp/ch/%d/%d.xml", chNum, pageNo);
	return parser_doc(filepath, max);
}

XMLlist_t **get_xml_alimain(int chNum, int pageNo, int *max)
{
	char filepath[128];
	XMLlist_t **programs = NULL;
	char video_sig[200], video_url[1024], file_path[128];
	FILE *fp;
	int k, kmax;

	snprintf(filepath, sizeof(filepath), "/tmp/ch/%d/%d.xml", chNum, pageNo);
	programs =  parser_doc(filepath, max);
	kmax = *max;

	if(kmax > 0) {
		for(k=0; k<kmax; k++) {
			snprintf(file_path, sizeof(file_path), "/tmp/ch/%d/%d.sig", chNum, (pageNo*25)+k );
			fp = fopen(file_path, "r");
			if(fp) {
				fgets(video_sig, sizeof(video_sig), fp);
				fclose(fp);
			}
			snprintf(file_path, sizeof(file_path), "/tmp/ch/%d/%d.url", chNum, (pageNo*25)+k );
			fp = fopen(file_path, "r");
			if(fp) {
				fgets(video_url, sizeof(video_url), fp);
				fclose(fp);
			}
			if(0 != strcmp(video_url, "")) {
				programs[k]->media_link = malloc(sizeof(char)*(sizeof(video_url)+sizeof(video_sig)+11));
				if(strstr(video_url, "url=") != NULL)
					sprintf(programs[k]->media_link, "%s&signature=%s", video_url+4, video_sig);
				else
					sprintf(programs[k]->media_link, "%s&signature=%s", video_url, video_sig);
			}
		}
	}

	return programs;
}

int get_youtube_info_v3(youtubeInParam_t *youtubeparam, youtubeOutParam_t *result)
{
    char apiURL[1024];
    char cfg_path[128];
    char *yPlaylistId = NULL;
    char *keyword = "NULL";
    int downloadFail = 0;
    FILE *ch_fp;
    config_t *ch_conf = &(config_t){};

    memset(apiURL, 0, sizeof(apiURL));
    memset(result, 0, sizeof(youtubeOutParam_t));

    /* Step 1. Read Channel info from /usr/app/conf/channel_list/%d.cfg */
    // TODO: check get_youtube_cfg() in download_service-1.0/youtube.c to know how to read channel info from xx.cfg


    snprintf(cfg_path, sizeof(cfg_path), "/usr/appdb/conf/channel_list/%d.cfg", youtubeparam->chNum);
    ch_fp = fopen(cfg_path, "r");
    if(ch_fp == NULL) {
        DBGMSG("Cannot open %s!\n", cfg_path);
        return -1;
    }
    config_init(ch_conf);
    flock(fileno(ch_fp), LOCK_EX); // lock
    config_read(ch_conf, ch_fp);
    flock(fileno(ch_fp),LOCK_UN); // unlock
    fclose(ch_fp);

    config_lookup_string(ch_conf, "yPlaylistId", (const char **)&yPlaylistId);
    config_lookup_string(ch_conf, "keyword", (const char **)&keyword);

    /* Step 2. Get Youtube V3 API URL (according to channel type) */
    // TODO : form the JSON download URL, if any parameter is missing returns fail
    /* {YOUR_API_KEY} = youtubeparam->developerId 
       {PLAYLIST_ID} => read from /usr/app/conf/channel_list/%d.cfg */
#if 0    
    if(youtubeparam->chType == CHTYPE_YOUTUBE_MOST_VIEW){
        snprintf(apiURL, sizeof(apiURL), "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=%d&pageToken=%s&playlistId=%s&key=%s", youtubeparam->maxResults, youtubeparam->pageToken, yPlaylistId, youtubeparam->developerId);
    }else if(youtubeparam->chType == CHTYPE_YOUTUBE_WATCH_LATER){
#else
    if(youtubeparam->chType == CHTYPE_YOUTUBE_WATCH_LATER){
#endif
        snprintf(apiURL, sizeof(apiURL), "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=%d&pageToken=%s&playlistId=%s&key=%s", youtubeparam->maxResults, youtubeparam->pageToken, yPlaylistId, youtubeparam->developerId);
    }else if(youtubeparam->chType == CHTYPE_YOUTUBE_PLAYLIST){
        snprintf(apiURL, sizeof(apiURL), "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=%d&pageToken=%s&playlistId=%s&key=%s", youtubeparam->maxResults, youtubeparam->pageToken, yPlaylistId, youtubeparam->developerId);
    }else if(youtubeparam->chType == CHTYPE_YOUTUBE_SUBSCRIPTION){
#if 0
		if(yPlaylistId == NULL){
DBGMSG("darcy yPlaylistId = %s", yPlaylistId);		
			snprintf(apiURL, sizeof(apiURL), "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=%d&pageToken=%s&channelId=%s&type=video&key=%s", youtubeparam->maxResults, youtubeparam->pageToken, yChannelId, youtubeparam->developerId);
		}else{
        	snprintf(apiURL, sizeof(apiURL), "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=%d&pageToken=%s&playlistId=%s&key=%s", youtubeparam->maxResults, youtubeparam->pageToken, yPlaylistId, youtubeparam->developerId);
		}
#else
        snprintf(apiURL, sizeof(apiURL), "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=%d&pageToken=%s&playlistId=%s&key=%s", youtubeparam->maxResults, youtubeparam->pageToken, yPlaylistId, youtubeparam->developerId);
#endif 
    }else if(youtubeparam->chType == CHTYPE_YOUTUBE_KEYWORD){
		snprintf(apiURL, sizeof(apiURL), "https://www.googleapis.com/youtube/v3/search?part=snippet&q=%s&maxResults=%d&pageToken=%s&type=video&key=%s", keyword, youtubeparam->maxResults, youtubeparam->pageToken, youtubeparam->developerId);
    }else if(youtubeparam->chType == CHTYPE_YOUTUBE_PERSONAL_PLAYLIST){
        snprintf(apiURL, sizeof(apiURL), "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=%d&pageToken=%s&playlistId=%s&key=%s", youtubeparam->maxResults, youtubeparam->pageToken, yPlaylistId, youtubeparam->developerId);
    }else{
        DBGMSG("Unknow chType = %d !\n", youtubeparam->chType);
    }
    config_destroy(ch_conf);

    if(strlen(apiURL) == 0){
        DBGMSG("Get Youtube V3 API URL fail!\n");
        return -1;
    }


    /* Step 3. Download the JSON file from Youtube V3 API */
    // TODO : check other download functions in this file
    // TODO : need check file downloading success or fail
    //

    /*system_exec("curl -o /tmp/ch/%d/.json -H 'Authorization:Bearer %s' '%s' -k >/dev/null 2>&1", youtubeparam->chNum, youtubeparam->access_key, apiURL);*/

    system_exec("curl -o /tmp/ch/%d/.json -H 'Authorization:Bearer %s' '%s' -k >/dev/null 2>&1",youtubeparam->chNum, youtubeparam->access_key, apiURL);

    snprintf(cfg_path, sizeof(cfg_path), "/tmp/ch/%d/.json", youtubeparam->chNum);
    ch_fp = fopen(cfg_path, "r");
    if(ch_fp == NULL) {
        DBGMSG("Not found %s!\n", cfg_path);
        return -1;
    }
    char tmp[128]="";
    while((fgets(tmp, sizeof(tmp), ch_fp)) != NULL){
        if(strstr(tmp,"error")|| strstr(tmp,"401")){
            downloadFail = 1;
            break;
        }
    }
    fclose(ch_fp);
    if(downloadFail){
        DBGMSG("Download JSON fail!\n");
        return -1;
    }


    /* Step 4. Parse the JSON file and form the output result */
    // TODO : check cloud_service-1.0/JSON_to_CFG.c to know how to parsing the JSON
    // TODO : chekc jsonc-0.10/ document to know how to form jsonOut
   	json_object *object, *obj_items, *obj_pageInfo, *obj_snippet, *obj_thumbnails, *obj_medium, *obj_resourceId, *obj_tmp;
 	json_object *obj_id;
    json_object *val, *val2, *val3, *val4, *val5, *val6, *val7;
    struct lh_entry *entry, *entry2, *entry3, *entry4, *entry5, *entry6, *entry7, *entry8;
    char *key=NULL, *key2=NULL, *key3=NULL, *key4=NULL, *key5=NULL, *key6=NULL, *key7=NULL;
    int i;

    result->jsonOut = json_object_new_array();

    snprintf(cfg_path, sizeof(cfg_path), "/tmp/ch/%d/.json", youtubeparam->chNum);

    object = json_object_from_file((char*)cfg_path);
    if(object){
        for(entry = json_object_get_object(object)->head; entry; entry = entry->next) {
            if(entry) {
                key = (char *)entry->k;
                val = (struct json_object *)entry->v;
                if(!strcmp(key, "nextPageToken")){
                    strcpy(result->nextPageToken, json_object_get_string(val));
                }else if(!strcmp(key, "prevPageToken")){
                    strcpy(result->prevPageToken, json_object_get_string(val));
                }
            }
        }
    }

    obj_pageInfo = json_object_object_get(object, "pageInfo");
    if(obj_pageInfo){
        for(entry2 = json_object_get_object(obj_pageInfo)->head; entry2; entry2 = entry2->next) {
            if(entry2) {
                key = (char *)entry2->k;
                val = (struct json_object *)entry2->v;
                if(!strcmp(key, "totalResults"))
                    result->totalCnt = atoi(json_object_get_string(val));
            }
        }
    }
    obj_items = json_object_object_get(object, "items");

    for(i=0; i < json_object_array_length(obj_items); i++){
        json_object *obj = json_object_array_get_idx(obj_items, i);
        if(obj){
            obj_tmp = json_object_new_object();
            for(entry3 = json_object_get_object(obj)->head; entry3; entry3 = entry3->next) {
                if(entry3){
                    key2 = (char *)entry3->k;
                    val2 = (struct json_object *)entry3->v;
					// following code for channel type =  keyword 
					if(!strcmp(key2,"id") && youtubeparam->chType == CHTYPE_YOUTUBE_KEYWORD){
						obj_id = json_object_object_get(obj, "id");
						if(obj_id){
							for(entry8 = json_object_get_object(obj_id)->head; entry8; entry8 = entry8->next){
								if(entry8) {
									key7 = (char *)entry8->k;
									val7 = (struct json_object *)entry8->v;
									if(!strcmp(key7, "videoId"))
										json_object_object_add(obj_tmp, key7, val7);
								}
							}
						}			
					}// end if channel type == keyword
                    if(!strcmp(key2, "snippet")){
                        obj_snippet = json_object_object_get(obj, "snippet");
                        if(obj_snippet){
                            for(entry4 = json_object_get_object(obj_snippet)->head; entry4; entry4 = entry4->next){
                                if(entry4){
                                    key3 = (char *)entry4->k;
                                    val3 = (struct json_object *)entry4->v;
                                    if(!strcmp(key3, "title"))
                                        json_object_object_add(obj_tmp, key3, val3);
                                    else if(!strcmp(key3,"thumbnails")){
                                        obj_thumbnails = json_object_object_get(obj_snippet, "thumbnails");
                                        if(obj_thumbnails){
                                            for(entry5 = json_object_get_object(obj_thumbnails)->head; entry5; entry5 = entry5->next) {
                                                if(entry5) {
                                                    key4 = (char *)entry5->k;
                                                    val4 = (struct json_object *)entry5->v;
                                                    if(!strcmp(key4, "medium")){
                                                       obj_medium = json_object_object_get(obj_thumbnails, "medium");
                                                        if(obj_medium){
                                                            for(entry6 = json_object_get_object(obj_medium)->head; entry6; entry6 = entry6->next){
                                                                if(entry6) {
                                                                    key5 = (char *)entry6->k;
                                                                    val5 = (struct json_object *)entry6->v;
                                                                    if(!strcmp(key5, "url"))
                                                                        json_object_object_add(obj_tmp, "thumbnails", val5);
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }// end else if thumbnails
                                    else if(!strcmp(key3,"resourceId")){
                                        obj_resourceId = json_object_object_get(obj_snippet, "resourceId");
                                        if(obj_resourceId){
                                            for(entry7 = json_object_get_object(obj_resourceId)->head; entry7; entry7 = entry7->next){
                                                if(entry7) {
                                                    key6 = (char *)entry7->k;
                                                    val6 = (struct json_object *)entry7->v;
                                                    if(!strcmp(key6, "videoId"))
                                                        json_object_object_add(obj_tmp, key6, val6);
                                                }
                                            }
                                        }
                                    }
                                } // end if entry4
                            } // end for entry4
                        } // end if snippet
                    } // end if key2 
                } // end if entry3
            } // end for entry3
            json_object_array_add(result->jsonOut,obj_tmp);
        } // end if(obj)
    } // end for i 
    return 0;
}

