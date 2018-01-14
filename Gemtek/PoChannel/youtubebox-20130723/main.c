#include "include/youtubeAPI.h"

void helpString(int type)
{
	switch(type)
	{
		case 1:
			printf("youtube playlist url orderby start_index max_result\n");
			break;
		case 2:
			printf("youtube program video_id\n");
			break;
		case 3:
			printf("youtube watch_later orderby start_index max_result\n");
			break;
		case 4:
			printf("youtube subscription url orderby start_index max_result\n");
			break; 
		case 5:
			printf("youtube mostviewed orderby start_index max_result\n");
			break; 
		case 6:
			printf("youtube query keyword orderby start_index max_result\n");
			break;      
		case 99:
			printf("Please input your command as bellow:\n");
			printf("----------------------------------\n");
			printf("playlist: get playlist info\n");
			printf("program: get program info\n");
			printf("watch_later: get watch_later info\n");
			printf("subscription: get subscription info\n");
			printf("mostviewed: get mostviewed info\n");
			printf("query: get query info\n");
			printf("----------------------------------\n");
		break;
	}

}

int main(int argc, char *argv[])
{
	XMLlist_t **list = NULL;
	char url_link[128];
	char token[100];
	char query[100];
	char video_id[50];
	char orderby[50];
	int start_index=0,i=0,max=0;
	int max_result =0;
	char FuncName[20];
	FILE *fp;

	if(argc < 1)
	{
		printf("Please input your command(ex: playlist,subscription....)\n");
		return 0;
	}
	else
	{
		strcpy((char *)FuncName, argv[1]);
		if(memcmp(FuncName, "get_token", 9) == 0)
		{
			get_access_token(token);
			printf("access_token:%s\n",token);
		}
		else if(memcmp(FuncName, "playlist", 8) == 0)
		{
			if(argc == 6)
			{  
				strcpy((char *)url_link, argv[2]);
				strcpy((char *)orderby, argv[3]);
				start_index= atoi(argv[4]);
				max_result= atoi(argv[5]);

				if(get_access_token(token))
				{
					list = get_playlist_info(token,url_link,orderby,start_index,max_result,&max);

					if(max <= 0)
					{
						printf("Get invalid value in %s\n",FuncName);
						return 0;
					}

					for(i=0;i<max;i++)
					{
						get_video_reallink(list[i]);
						printf("======================Playlist[%d]======================\n",i+1);
						printf("entry_title:%s\n",list[i]->entry_title);
						printf("entry_published:%s\n",list[i]->entry_published);
						printf("entry_updated:%s\n",list[i]->entry_updated);
						printf("author_name:%s\n",list[i]->author_name);
						printf("author_id:%s\n",list[i]->author_id);
						printf("author_url:%s\n",list[i]->author_url);
						printf("media_thumbnail:%s\n",list[i]->media_thumbnail);
						printf("media_videoId:%s\n",list[i]->media_videoId);
						printf("media_uploaderId:%s\n",list[i]->media_uploaderId);
						printf("media_link:%s\n",list[i]->media_link);
					}

					fp=fopen("/tmp/play_y2b.txt","w");
					fprintf(fp,"%s",list[0]->media_link);
					fclose(fp);

					for(i=0;i<max;i++)
						free_info(list[i]);
				}
			}
			else
				helpString(1);
		}
		else if(memcmp(FuncName, "program", 7) == 0)
		{
			if(argc == 3)
			{  
				strcpy((char *)video_id, argv[2]);

				if(get_access_token(token))
				{
					get_program_info(token,video_id);

					if(max <= 0)
					{
						printf("Get invalid value in %s\n",FuncName);
						return 0;
					}
					
					get_video_reallink(list[0]);
					printf("======================ProgramList======================\n");
					printf("entry_title:%s\n",list[0]->entry_title);
					printf("entry_published:%s\n",list[0]->entry_published);
					printf("entry_updated:%s\n",list[0]->entry_updated);
					printf("author_name:%s\n",list[0]->author_name);
					printf("author_id:%s\n",list[0]->author_id);
					printf("author_url:%s\n",list[0]->author_url);
					printf("media_thumbnail:%s\n",list[0]->media_thumbnail);
					printf("media_videoId:%s\n",list[0]->media_videoId);
					printf("media_uploaderId:%s\n",list[0]->media_uploaderId);
					printf("media_link:%s\n",list[0]->media_link);

					fp=fopen("/tmp/play_y2b.txt","w");
					fprintf(fp,"%s",list[0]->media_link);
					fclose(fp);

					free_info(list[0]);
				}
			}
			else
				helpString(2);
		}
		else if(memcmp(FuncName, "watch_later", 11) == 0)
		{
			if(argc == 5)
			{  
				strcpy((char *)orderby, argv[2]);
				start_index= atoi(argv[3]);
				max_result= atoi(argv[4]);

				if(get_access_token(token))
				{
					list = get_watch_later_info(token,orderby,start_index,max_result,&max);

					if(max <= 0)
					{
						printf("Get invalid value in %s\n",FuncName);
						return 0;
					}

					for(i=0;i<max;i++)
					{
						get_video_reallink(list[i]);
						printf("======================Watch_Later[%d]======================\n",i+1);
						printf("entry_title:%s\n",list[i]->entry_title);
						printf("entry_published:%s\n",list[i]->entry_published);
						printf("entry_updated:%s\n",list[i]->entry_updated);
						printf("author_name:%s\n",list[i]->author_name);
						printf("author_id:%s\n",list[i]->author_id);
						printf("author_url:%s\n",list[i]->author_url);
						printf("media_thumbnail:%s\n",list[i]->media_thumbnail);
						printf("media_videoId:%s\n",list[i]->media_videoId);
						printf("media_uploaderId:%s\n",list[i]->media_uploaderId);
						printf("media_link:%s\n",list[i]->media_link);
					}

					fp=fopen("/tmp/play_y2b.txt","w");
					fprintf(fp,"%s",list[0]->media_link);
					fclose(fp);

					for(i=0;i<max;i++)
						free_info(list[i]);
				}
			}
			else
				helpString(3);

		}
		else if(memcmp(FuncName, "subscription", 11) == 0)
		{
			if(argc == 6)
			{  
				strcpy((char *)url_link, argv[2]);
				strcpy((char *)orderby, argv[3]);
				start_index= atoi(argv[4]);
				max_result= atoi(argv[5]);
				
				if(get_access_token(token))
				{
					list = get_subscription_info(token,url_link,orderby,start_index,max_result,&max);

					if(max <= 0)
					{
						printf("Get invalid value in %s\n",FuncName);
						return 0;
					}

					for(i=0;i<max;i++)
					{
						get_video_reallink(list[i]);
						printf("======================SubScription[%d]======================\n",i+1);
						printf("entry_title:%s\n",list[i]->entry_title);
						printf("entry_published:%s\n",list[i]->entry_published);
						printf("entry_updated:%s\n",list[i]->entry_updated);
						printf("author_name:%s\n",list[i]->author_name);
						printf("author_id:%s\n",list[i]->author_id);
						printf("author_url:%s\n",list[i]->author_url);
						printf("media_thumbnail:%s\n",list[i]->media_thumbnail);
						printf("media_videoId:%s\n",list[i]->media_videoId);
						printf("media_uploaderId:%s\n",list[i]->media_uploaderId);
						printf("media_link:%s\n",list[i]->media_link);

					}

					fp=fopen("/tmp/play_y2b.txt","w");
					fprintf(fp,"%s",list[0]->media_link);
					fclose(fp);

					for(i=0;i<max;i++)
						free_info(list[i]);
				}
			}
			else
				helpString(4);
		}
		else if(memcmp(FuncName, "most_view",9) == 0)
		{
			if(argc == 5)
			{  
				strcpy((char *)orderby, argv[2]);
				start_index= atoi(argv[3]);
				max_result= atoi(argv[4]);
				
				if(get_access_token(token))
				{
					list = get_mostviewed_info(token,orderby,start_index,max_result,&max);

					if(max <= 0)
					{
						printf("Get invalid value in %s\n",FuncName);
						return 0;
					}

					for(i=0;i<max;i++)
					{
						get_video_reallink(list[i]);
						printf("======================MostView[%d]======================\n",i+1);
						printf("entry_title:%s\n",list[i]->entry_title);
						printf("entry_published:%s\n",list[i]->entry_published);
						printf("entry_updated:%s\n",list[i]->entry_updated);
						printf("author_name:%s\n",list[i]->author_name);
						printf("author_id:%s\n",list[i]->author_id);
						printf("author_url:%s\n",list[i]->author_url);
						printf("media_thumbnail:%s\n",list[i]->media_thumbnail);
						printf("media_videoId:%s\n",list[i]->media_videoId);
						printf("media_uploaderId:%s\n",list[i]->media_uploaderId);
						printf("media_link:%s\n",list[i]->media_link);
					}

					fp=fopen("/tmp/play_y2b.txt","w");
					fprintf(fp,"%s",list[0]->media_link);
					fclose(fp);

					for(i=0;i<max;i++)
						free_info(list[i]);
				}
			}
			else
				helpString(5);
		}
		else if(memcmp(FuncName, "query",5) == 0)
		{
			if(argc == 6)
			{  
				strcpy((char *)query, argv[2]);
				strcpy((char *)orderby, argv[3]);
				start_index= atoi(argv[4]);
				max_result= atoi(argv[5]);
				
				if(get_access_token(token))
				{
					list = get_query_info(token,query,orderby,start_index,max_result,&max);

					if(max <= 0)
					{
						printf("Get invalid value in %s\n",FuncName);
						return 0;
					}

					for(i=0;i<max;i++)
					{
						get_video_reallink(list[i]);
						printf("======================QueryList[%d]======================\n",i+1);
						printf("entry_title:%s\n",list[i]->entry_title);
						printf("entry_published:%s\n",list[i]->entry_published);
						printf("entry_updated:%s\n",list[i]->entry_updated);
						printf("author_name:%s\n",list[i]->author_name);
						printf("author_id:%s\n",list[i]->author_id);
						printf("author_url:%s\n",list[i]->author_url);
						printf("media_thumbnail:%s\n",list[i]->media_thumbnail);
						printf("media_videoId:%s\n",list[i]->media_videoId);
						printf("media_uploaderId:%s\n",list[i]->media_uploaderId);
						printf("media_link:%s\n",list[i]->media_link);
					}

					fp=fopen("/tmp/play_y2b.txt","w");
					fprintf(fp,"%s",list[0]->media_link);
					fclose(fp);

					for(i=0;i<max;i++)
						free_info(list[i]);
				}
			}
			else
				helpString(6);
		}
	}
	return 1;
}

