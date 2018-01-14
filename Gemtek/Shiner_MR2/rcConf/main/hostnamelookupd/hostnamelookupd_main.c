/*
 * hostnamelookup main functions
 *
 * Copyright 2006-2009, Gemtek Corporation
 * All Rights Reserved.
 * 
 * $Id$
 */

#include <rcConf_common.h>
#include <sys/time.h>
#include <signal.h>
#include <unistd.h>
#include <hostnamelookup.h>

void hostname_time_count(int signo)
{
	sqlite3 *hostname_db;
	sqlite3 *IPlist_db;
	sqlite3_stmt *stmt_t;
    char sqlcmd[256] = "SELECT * FROM result;";
    char *errMsg = NULL;
    int row=0, column=0;
    char **result;
    int i = 0, rc;
	int tmp;

    /* Open database hostname.db */
	rc = sqlite3_open("/tmp/hostname.db", &hostname_db);
	if(rc != SQLITE_OK) {
        fprintf(stderr,"Cannot open hostname_db: %s\n",sqlite3_errmsg(hostname_db));
        return;
    }
	
	/* Open database hostnametmp.db*/
    rc = sqlite3_open("/tmp/hostnametmp.db", &IPlist_db);
    if(rc != SQLITE_OK) {
    	fprintf(stderr,"Cannot open hostnametmp.db: %s\n",sqlite3_errmsg(IPlist_db));
	}	

    /* Get all hostname from result table */
    sqlite3_get_table(hostname_db, sqlcmd, &result, &row, &column, &errMsg);

    for( i=4 ; i<( row + 1 ) * column ; i+=4 ){
		tmp=atoi(result[i+2]);
		tmp = tmp - 3600;
        if(tmp <= 0){
            snprintf(sqlcmd,256, "DELETE FROM result where ipv4='%s' ;", result[i]);
            sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt_t, NULL);
            sqlite3_step(stmt_t);
            sqlite3_reset(stmt_t);
            sqlite3_finalize(stmt_t);
    
        	snprintf(sqlcmd,256, "DELETE FROM IPlist where ipv4='%s' ;", result[i]);
        	sqlite3_prepare_v2(IPlist_db,sqlcmd,256, &stmt_t, NULL);
        	sqlite3_step(stmt_t);
        	sqlite3_reset(stmt_t);
        	sqlite3_finalize(stmt_t);
        
			continue;

		}
        snprintf(sqlcmd,256,"UPDATE result set timeout=%d where ipv4='%s' and hostname='%s';", tmp,result[i],result[i+1]);
        sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt_t, NULL);
        sqlite3_step(stmt_t);
        sqlite3_reset(stmt_t);
        sqlite3_finalize(stmt_t);
    }
	
    /* Release table */
    sqlite3_free_table(result);
	sqlite3_free(errMsg);
    /* Close database hostname.db */
    sqlite3_close(hostname_db);
    
	/* Get all hostname from IPlist table */
    snprintf(sqlcmd,256, "SELECT * FROM IPlist;");
    sqlite3_get_table(IPlist_db, sqlcmd, &result, &row, &column, &errMsg);
    for( i=2 ; i<( row + 1 ) * column ; i+=2 ){
		tmp=atoi(result[i+1]);
		tmp = tmp - 3600;
       	if(tmp <= 0){
       		snprintf(sqlcmd,256, "DELETE FROM IPlist where ipv4='%s' ;", result[i]);
       		sqlite3_prepare_v2(IPlist_db,sqlcmd,256, &stmt_t, NULL);
       		sqlite3_step(stmt_t);
       		sqlite3_reset(stmt_t);
       		sqlite3_finalize(stmt_t);
		}
	}
    /* Release table */
    sqlite3_free_table(result);
	sqlite3_free(errMsg);
    /* Close database hostnametmp.db */
    sqlite3_close(IPlist_db);
}

static int do_main(int argc, char *argv[])
{
	/* main area */

	struct itimerval timer; 
   	timer.it_value.tv_sec = 3600;
   	timer.it_value.tv_usec = 0;
   	timer.it_interval.tv_sec = 3600;
   	timer.it_interval.tv_usec = 0;
   	if(setitimer(ITIMER_REAL, &timer, NULL) < 0){
		printf("settimer error\n");
		return -1;
	}   
   	signal(SIGALRM, hostname_time_count);
    for(;;)
    	pause();

	return 0;
}

int hostnamelookupd_main(int argc, char *argv[])
{
	pid_t pid;

	signal(SIGCHLD, SIG_IGN);

	pid = fork();
	switch (pid) {
		case -1:
			DBGMSG("can't fork\n");
			exit(0);
			break;
		case 0:
			/* child process */
			DBGMSG("fork ok\n");
			(void) setsid();
			break;
		default:
			/* parent process should just die */
			_exit(0);
	}

	return do_main(argc, argv);
}
