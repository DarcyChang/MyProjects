/*
 * Tool for Hostname Lookup

 * Copyright 2010, Gemtek Corporation
 * All Rights Reserved.
  
 * THIS SOFTWARE IS OFFERED "AS IS", AND GEMTEK GRANTS NO WARRANTIES OF ANY
 * KIND, EXPRESS OR IMPLIED, BY STATUTE, COMMUNICATION OR OTHERWISE. GEMTEK
 * SPECIFICALLY DISCLAIMS ANY IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A SPECIFIC PURPOSE OR NONINFRINGEMENT CONCERNING THIS SOFTWARE.
 
 * $Id$
 */

#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "./hostnamelookup.h"

static char *resultTB = "CREATE TABLE result ("
            "ipv4 VARCHAR(16),"
            "hostname VARCHAR(256),"
			"date VARCHAR(32),"
			"seconds INTEGER);";

static char *resultTMP = "CREATE TABLE hostnametmp ("
            "ipv4 VARCHAR(16),"
            "hostname VARCHAR(256),"
			"protocol VARCHAR(16));"; 

static char *IPlist = "CREATE TABLE IPlist ("
            "ipv4 VARCHAR(16));";
			
void print_usage(char *program)
{
    fprintf(stderr, "Usage: ");    
   	fprintf(stderr, "%s [options] \n\n", program); 
    fprintf(stderr, " options :\n");
    fprintf(stderr, "  addv2 <IP Address> :\n");
    fprintf(stderr, "  add <IP Address>\n");
    fprintf(stderr, "  del <IP Address>\n");
    fprintf(stderr, "  list\n");
    fprintf(stderr, "  del_all\n");
    fprintf(stderr, "  do_req\n");
    fprintf(stderr, "  -h help\n");
    fprintf(stderr, "\n");
}

void hostnamelookup_addv2(char* ip, char* hostname, int len)
{
    sqlite3 *hostname_db, *IPlist_db;
    sqlite3_stmt *stmt = NULL;
    char sqlcmd[256] = "SELECT * FROM result;";
    char *errMsg = NULL;
    int row=0, column=0;
    char **result;
    int i = 0,rc;
    struct in_addr inp;
    int ip_range=0,count;
	
	if(len < 256)
    {  
        fprintf(stderr," hostname variable size length %d < 256!\n",len);
        return;
    }  

	ip_range=inet_aton(ip,&inp);
	if(ip_range == 0 || sscanf(ip, "%d.%d.%d.%d", &count, &count, &count, &count) != 4)
	{
		print_usage("hostnamelookup");
		return;			
	}

	bzero(hostname,256);

    /* Open database hostname.db */
	rc = sqlite3_open("/tmp/hostname.db", &hostname_db);
	if(rc != SQLITE_OK) {
		fprintf(stderr,"Cannot open hostname_db: %s\n",sqlite3_errmsg(hostname_db));
		return;
    }

   	/* Create table result */
    if(sqlite3_exec(hostname_db, resultTB, 0, 0, &errMsg) == SQLITE_OK)
		fprintf(stderr,"create table result first!\n");

		
	/* Get all hostname from result table */
    sqlite3_get_table(hostname_db, sqlcmd, &result, &row, &column, &errMsg);
	
	/* hostname compare from result table */
    for( i=4 ; i<( row + 1 ) * column ; i+=4 )
	{
		if(0 == strcmp(result[i],ip)){
			strcpy(hostname,result[i+1]);
			printf("From hostname database search HostName = %s\n", hostname);
			sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt, NULL);
			sqlite3_step(stmt);
    		sqlite3_reset(stmt);
			sqlite3_finalize(stmt);
			/* Release table */
    		sqlite3_free_table(result);	
			sqlite3_free(errMsg);	
    		sqlite3_close(hostname_db);
			return;
		}	
	}
	/* Release table */
    sqlite3_free_table(result);	

	/* Compare input IP repeat from table IPlist */
    /* Open database hostnametmp.db*/
	rc = sqlite3_open("/tmp/hostnametmp.db", &IPlist_db);
	if(rc != SQLITE_OK) {
		fprintf(stderr,"Cannot open hostnametmp.db: %s\n",sqlite3_errmsg(IPlist_db));
		return;
    }

   	/* Create table IPlist */
    if(sqlite3_exec(IPlist_db, IPlist, 0, 0, &errMsg) == SQLITE_OK)
		fprintf(stderr,"create table IPlist first!\n");

    snprintf(sqlcmd,256, "SELECT * FROM IPlist ;");
		
	/* Get all hostname from IPlist table */
    sqlite3_get_table(IPlist_db, sqlcmd, &result, &row, &column, &errMsg);
	
	if(row == 0){
    	snprintf(sqlcmd,256,"INSERT INTO IPlist (ipv4) VALUES('%s');", ip);
		sqlite3_prepare_v2(IPlist_db,sqlcmd,256, &stmt, NULL);
		sqlite3_step(stmt);
    	sqlite3_reset(stmt);
		sqlite3_finalize(stmt);
		/* Release table */
    	sqlite3_free_table(result);	
		sqlite3_free(errMsg);	
    	sqlite3_close(IPlist_db);
	}else if(row > 0 && row <= 10){		
		/* hostname compare from IPlist table */
    	for( i=1 ; i<( row + 1 ) * column ; i++ ){
			if(0 == strcmp(result[i],ip)){
				printf("Input IP repeat with last request IP\n");
				/* Release table */
    			sqlite3_free_table(result);	
				sqlite3_free(errMsg);	
    			sqlite3_close(IPlist_db);
    			sqlite3_close(hostname_db);
				return;
			}
		}	
    	snprintf(sqlcmd,256,"INSERT INTO IPlist (ipv4) VALUES('%s');", ip);
		sqlite3_prepare_v2(IPlist_db,sqlcmd,256, &stmt, NULL);
		sqlite3_step(stmt);
    	sqlite3_reset(stmt);
		sqlite3_finalize(stmt);
		if(row == 10){
    		snprintf(sqlcmd,256, "DELETE FROM IPlist where ipv4='%s' ;", result[1]);
			sqlite3_prepare_v2(IPlist_db,sqlcmd,256, &stmt, NULL);
			sqlite3_step(stmt);
    		sqlite3_reset(stmt);
			sqlite3_finalize(stmt);
		}
		/* Release table */
    	sqlite3_free_table(result);	
		sqlite3_free(errMsg);	
    	sqlite3_close(IPlist_db);
	}	
	/* Compare input IP repeat from table IPlist finish! */
	
	sleep(2); // Wait for insert large data.

	/* fork three process for three protocol and return result */
	pid_t pid,pid2,pid3,pid4;
    pid = fork();
    switch (pid) {
        case -1:
            printf("can't fork\n");
            exit(0);
            break;
        case 0:
            /* child process : do addv2_netbios */
//            printf("%s nbtscan fork ok\n",ip);
			addv2_netbios(ip, hostname);
            exit(0);
            break;
        default:
            /* parent */
			break;		
    }

    pid2 = fork();
    switch (pid2){
        case -1:
            printf("can't fork\n");
            exit(0);
            break;
        case 0:
            /* child process: do addv2_dns */
//            printf("%s dnsquery fork ok\n",ip);
			addv2_dns(ip, hostname);
            exit(0);
            break;
        default:
            /* parent */
            break;
    }
    
	pid3 = fork();
    switch (pid3){
        case -1:
            printf("can't fork\n");
            exit(0);
            break;
        case 0:
            /* child process: do addv2_bonjour */
//            printf("%s mDNSIdentify fork ok\n",ip);
			addv2_bonjour(ip, hostname);
            exit(0);
            break;
        default:
            /* parent */
            break;
    }
	pid4 = fork();
    switch (pid4){
        case -1:
            printf("can't fork\n");
            exit(0);
            break;
        case 0:
            /* child process: do addv2_bonjour */
//            printf("hostname result fork ok\n");
			hostnamelookup_result(ip, hostname);
            exit(0);
            break;
        default:
            /* parent */
            break;
    }

	/* Close database */
    sqlite3_close(hostname_db);
	return;
}
void hostnamelookup_result(char* ip, char* hostname)
{
    sqlite3 *hostname_db, *IPlist_db;
	sqlite3 *tmp_db;
    sqlite3_stmt *stmt;
    char sqlcmd[256] = ""; 
    char *errMsg = NULL;	
	int row=0, column=0;
	char **tmp;
	int rc;	

    /* Open resultTMP database */
    rc = sqlite3_open(HOSTNAME_DB_TMP_PATH,&tmp_db);
	if(rc != SQLITE_OK){
		printf("Can't open database to insert signatures: %s\n", sqlite3_errmsg(tmp_db));
        return;
	}
	
    /* Open database hostnametmp.db*/
	rc = sqlite3_open("/tmp/hostnametmp.db", &IPlist_db);
	if(rc != SQLITE_OK) {
		fprintf(stderr,"Cannot open hostnametmp.db: %s\n",sqlite3_errmsg(IPlist_db));
		return;
    }

	sleep(13); // Wait for three protocol parser
	
	/* Get ip from resultTMP table */
    snprintf(sqlcmd,256, "SELECT * FROM hostnametmp where ipv4='%s' ;", ip);
	if(sqlite3_get_table(tmp_db, sqlcmd, &tmp, &row, &column, &errMsg) != SQLITE_OK)
		fprintf(stderr,"search table resultTMP error!\n");	
	if(row == 0){
		printf("Database resultTMP is empty or can not find hostname by %s\n",ip);
   		snprintf(sqlcmd,256, "DELETE FROM IPlist where ipv4='%s' ;", ip);
		sqlite3_prepare_v2(IPlist_db,sqlcmd,256, &stmt, NULL);
		sqlite3_step(stmt);
   		sqlite3_reset(stmt);
		sqlite3_finalize(stmt);	
    	sqlite3_close(IPlist_db);
		/* Release table */
    	sqlite3_free_table(tmp);
    	sqlite3_free(errMsg);
    	/* Close database */
    	sqlite3_close(tmp_db);
		return;	
	}
	
	/* Release table */
    sqlite3_free_table(tmp);
    sqlite3_free(errMsg);
    
    time_t insert_date;
    time(&insert_date);
//	int seconds=time(&insert_date);
	int seconds=time((time_t*)NULL);
	
	/* Open resultTB database */
    rc = sqlite3_open(HOSTNAME_DB_PATH,&hostname_db);
	if(rc != SQLITE_OK){
		printf("Can't open database to insert signatures: %s\n", sqlite3_errmsg(hostname_db));
        return;
	}
   	
	/* Create resultTB table */
    if(sqlite3_exec(hostname_db, resultTB, 0, 0, &errMsg) == SQLITE_OK)
		fprintf(stderr,"create table resultTB first!\n");

	/* Get ip from resultTMP table by netbios*/
    snprintf(sqlcmd,256, "SELECT * FROM hostnametmp where ipv4='%s' and protocol='%s' ;", ip,"netbios");
	if(sqlite3_get_table(tmp_db, sqlcmd, &tmp, &row, &column, &errMsg) != SQLITE_OK)
		fprintf(stderr,"search table resultTMP error!\n");	
	if(row > 0){
    	snprintf(sqlcmd,256,"INSERT INTO result (ipv4, hostname, date, seconds) VALUES('%s', '%s', '%s', %d);", ip, tmp[4], ctime(&insert_date), seconds);
	    sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt, NULL);
        sqlite3_step(stmt);
    	sqlite3_reset(stmt);
		sqlite3_finalize(stmt);
    	snprintf(sqlcmd,256, "DELETE FROM hostnametmp where ipv4='%s' ;", ip);
		sqlite3_prepare_v2(tmp_db,sqlcmd,256, &stmt, NULL);
    	sqlite3_step(stmt);
    	sqlite3_reset(stmt);
    	sqlite3_finalize(stmt);
		/* Release table */
    	sqlite3_free_table(tmp);
    	sqlite3_free(errMsg);
    	/* Close database */
    	sqlite3_close(tmp_db);
    	sqlite3_close(hostname_db);
		return;
	}
	/* Release table */
    sqlite3_free_table(tmp);
    sqlite3_free(errMsg);

	/* Get ip from resultTMP table by bonjour*/
    snprintf(sqlcmd,256, "SELECT * FROM hostnametmp where ipv4='%s' and protocol='%s' ;", ip,"bonjour");
	if(sqlite3_get_table(tmp_db, sqlcmd, &tmp, &row, &column, &errMsg) != SQLITE_OK)
		fprintf(stderr,"search table resultTMP error!\n");	
	if(row > 0){
    	snprintf(sqlcmd,256,"INSERT INTO result (ipv4, hostname, date, seconds) VALUES('%s', '%s', '%s', %d);", ip, tmp[4], ctime(&insert_date), seconds);
	    sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt, NULL);
        sqlite3_step(stmt);
    	sqlite3_reset(stmt);
		sqlite3_finalize(stmt);
    	snprintf(sqlcmd,256, "DELETE FROM hostnametmp where ipv4='%s' ;", ip);
		sqlite3_prepare_v2(tmp_db,sqlcmd,256, &stmt, NULL);
    	sqlite3_step(stmt);
    	sqlite3_reset(stmt);
    	sqlite3_finalize(stmt);
		/* Release table */
    	sqlite3_free_table(tmp);
    	sqlite3_free(errMsg);
    	/* Close database */
    	sqlite3_close(tmp_db);
    	sqlite3_close(hostname_db);
		return;
	}
	/* Release table */
    sqlite3_free_table(tmp);
    sqlite3_free(errMsg);

	/* Get ip from resultTMP table by dnsquery*/
    snprintf(sqlcmd,256, "SELECT * FROM hostnametmp where ipv4='%s' and protocol='%s' ;", ip,"dnsquery");
	if(sqlite3_get_table(tmp_db, sqlcmd, &tmp, &row, &column, &errMsg) != SQLITE_OK)
		fprintf(stderr,"search table resultTMP error!\n");	
	if(row > 0){
    	snprintf(sqlcmd,256,"INSERT INTO result (ipv4, hostname, date, seconds) VALUES('%s', '%s', '%s', %d);", ip, tmp[4], ctime(&insert_date), seconds);
	    sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt, NULL);
        sqlite3_step(stmt);
    	sqlite3_reset(stmt);
		sqlite3_finalize(stmt);
    	snprintf(sqlcmd,256, "DELETE FROM hostnametmp where ipv4='%s' ;", ip);
		sqlite3_prepare_v2(tmp_db,sqlcmd,256, &stmt, NULL);
    	sqlite3_step(stmt);
    	sqlite3_reset(stmt);
    	sqlite3_finalize(stmt);
		/* Release table */
    	sqlite3_free_table(tmp);
    	sqlite3_free(errMsg);
    	/* Close database */
    	sqlite3_close(tmp_db);
    	sqlite3_close(hostname_db);
		return;
	}
}
void addv2_netbios(char* ip, char* hostname)
{
    sqlite3 *hostname_db;
    sqlite3_stmt *stmt = NULL;
	int found = 0; // found hostname = 1;
    char sqlcmd[256] = "";
    char *errMsg = NULL;
	char buf[128]="";
	char tmp[128]="";
	FILE *rf;
    int rc;
	
	bzero(hostname,256);
    
	/* Open database */
	rc = sqlite3_open(HOSTNAME_DB_TMP_PATH, &hostname_db);
	if(rc != SQLITE_OK) {
		fprintf(stderr,"Cannot open hostnametmp: %s\n",sqlite3_errmsg(hostname_db));
		return;
    }
	/* Create table */
    if(sqlite3_exec(hostname_db, resultTMP, 0, 0, &errMsg) == SQLITE_OK)
		fprintf(stderr,"create table resultTMP first!\n");

	bzero(sqlcmd,256);
	bzero(buf,128);
	bzero(tmp,128);

	/* NetBIOS protocol */
   	snprintf(buf,128, "nice -n 19 nbtscan -vh %s", ip);
	if((rf = popen(buf,"r")) == NULL){
		printf("NetBIOS popen() error!\n");
		exit(1);
	}
	/* parser NetBIOS */	
    while((fgets(tmp, sizeof(tmp), rf)) != NULL){
	  	if(strstr(tmp,"Workstation Service")){
        	strcpy(hostname,strtok(tmp," "));
            found = 1;
            while((fgets(tmp, sizeof(tmp), rf)) != NULL){
               	if(strstr(tmp,"00-00-00-00-00-00")) // Linux samba will return wrong MAC Address
				{
                   	found = 0;
                   	break;
               	}
            }
          	break;
       	}
   	}	            
	pclose(rf);
    if(found == 1){
//    	printf("\n %s HostName is %s\n", ip, hostname);
    	snprintf(sqlcmd,256,"INSERT INTO hostnametmp (ipv4, hostname, protocol) VALUES('%s', '%s', '%s');", ip, hostname, "netbios");
        sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt, NULL);
        sqlite3_step(stmt);
  		sqlite3_reset(stmt);
		sqlite3_finalize(stmt);
		sqlite3_free(errMsg);	
   		sqlite3_close(hostname_db);
		return;
	}
	sqlite3_free(errMsg);	
	/* Close database */
    sqlite3_close(hostname_db);

	return;
}
void addv2_dns(char* ip, char* hostname)
{
    sqlite3 *hostname_db;
    sqlite3_stmt *stmt = NULL;
    char sqlcmd[256] = "";
    char *errMsg = NULL;
	char buf[128]="";
	char tmp[128]="";
	FILE *rf;
    int rc;

	bzero(hostname,256);

    /* Open database */
	rc = sqlite3_open(HOSTNAME_DB_TMP_PATH, &hostname_db);
	if(rc != SQLITE_OK) {
		fprintf(stderr,"Cannot open hostnametmp : %s\n",sqlite3_errmsg(hostname_db));
		return;
    }

	/* Create table */
    if(sqlite3_exec(hostname_db, resultTMP, 0, 0, &errMsg) == SQLITE_OK)
		fprintf(stderr,"create table resultTMP first!\n");

	/* DNS protocol */
	bzero(buf,128);  
   	snprintf(buf,128, "nice -n 19 dnsquery -n %s 2>/dev/null", ip);
	if((rf = popen(buf,"r")) == NULL){
		printf("DNS query popen() error!\n");
		exit(1);
	}

	/* parser DNS */
	while((fgets(tmp, sizeof(tmp), rf)) != NULL) {
		strcpy(hostname,strtok(tmp,"\n"));
		if(0 == strcmp(hostname, "Failure")){
//			printf("DNS query Failure!\n");
			bzero(hostname,256);
       		pclose(rf);
			break;
		}else{
//			printf("\n %s HostName is %s\n", ip, hostname);
       		pclose(rf);		
    		snprintf(sqlcmd,256,"INSERT INTO hostnametmp (ipv4, hostname, protocol) VALUES('%s', '%s', '%s');", ip, hostname, "dnsquery");
            sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt, NULL);
            sqlite3_step(stmt);
   			sqlite3_reset(stmt);
            sqlite3_finalize(stmt);
			sqlite3_free(errMsg);	
   			sqlite3_close(hostname_db);
			return;
		}	
    }
	sqlite3_free(errMsg);	
	/* Close database */
    sqlite3_close(hostname_db);
	return;
}
void addv2_bonjour(char* ip, char* hostname)
{
    sqlite3 *hostname_db;
    sqlite3_stmt *stmt = NULL;
    char sqlcmd[256] = "";
    char *errMsg = NULL;
	char buf[128]="";
	char tmp[128]="";
	FILE *rf;
    int rc;

	bzero(hostname,256);

    /* Open database */
	rc = sqlite3_open(HOSTNAME_DB_TMP_PATH, &hostname_db);
	if(rc != SQLITE_OK) {
		fprintf(stderr,"Cannot open hostnametmp: %s\n",sqlite3_errmsg(hostname_db));
		return 0;
    }
	/* Create table */
    if(sqlite3_exec(hostname_db, resultTMP, 0, 0, &errMsg) == SQLITE_OK)
		fprintf(stderr,"create table resultTMP first!\n");

	/* Bonjour protocol */
    bzero(buf,128);
   	snprintf(buf,128, "nice -n 19 mDNSIdentify %s 2>/dev/null", ip);
	if((rf = popen(buf,"r")) == NULL){
		printf("Bonjour popen() error!\n");
		exit(1);
	}

	/* parser Bonjour */
    while((fgets(tmp, sizeof(tmp), rf)) != NULL){
       	if(strstr(tmp,"Addr")){
            strcpy(hostname,strtok(strtok(tmp," "),"."));
//            printf("\n %s HostName is %s\n", ip, hostname);
       		pclose(rf);
    		snprintf(sqlcmd,256,"INSERT INTO hostnametmp (ipv4, hostname, protocol) VALUES('%s', '%s', '%s');", ip, hostname, "bonjour");
            sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt, NULL);
            sqlite3_step(stmt); 
  			sqlite3_reset(stmt);
			sqlite3_finalize(stmt);
			sqlite3_free(errMsg);	
   			sqlite3_close(hostname_db);
			return;
        }
	}
//	printf("Bonjour query Failure!\n");
    pclose(rf);
	sqlite3_free(errMsg);	
	/* Close database */
    sqlite3_close(hostname_db);
	return;
}
void hostnamelookup_add(char* ip, char* hostname, int len)
{
    sqlite3 *hostname_db;
    sqlite3_stmt *stmt = NULL;
	int found = 0; // found hostname = 1;
    char sqlcmd[256] = "SELECT * FROM result;";
    char *errMsg = NULL;
	char buf[128]="";
	char tmp[128]="";
    int row=0, column=0;
    char **result;
    int i = 0,rc;
	FILE *rf;
    struct in_addr inp;
    int ip_range=0,count;
	ip_range=inet_aton(ip,&inp);
    time_t insert_date;
    int seconds = time(&insert_date);

	if(len < 256)
	{
		fprintf(stderr," hostname variable size length %d < 256!\n",len);
        return;
	}

	if(ip_range == 0 || sscanf(ip, "%d.%d.%d.%d", &count, &count, &count, &count) != 4)
	{
		print_usage("hostnamelookup");
		return;			
	}

    /* Open database */
	rc = sqlite3_open("/tmp/hostname.db", &hostname_db);
	if(rc != SQLITE_OK) {
		fprintf(stderr,"Cannot open hostname_db: %s\n",sqlite3_errmsg(hostname_db));
		return;
    }

   	/* Create table */
    if(sqlite3_exec(hostname_db, resultTB, 0, 0, &errMsg) == SQLITE_OK)
		fprintf(stderr,"create table first!\n");

		
	/* Get all hostname from result table */
    sqlite3_get_table(hostname_db, sqlcmd, &result, &row, &column, &errMsg);
	
	/* hostname compare from result table */
    for( i=4 ; i<( row + 1 ) * column ; i+=4 )
	{
		if(0 == strcmp(result[i],ip)){
			strcpy(hostname,result[i+1]);
			printf("From hostname database search HostName = %s\n", hostname);
			sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt, NULL);
			sqlite3_step(stmt);
    		sqlite3_reset(stmt);
			sqlite3_finalize(stmt);
			sqlite3_free(errMsg);	
    		sqlite3_close(hostname_db);
			return;				
		}
	}
	/* Release table */
    sqlite3_free_table(result);
	bzero(hostname,256);
	bzero(sqlcmd,256);
	bzero(buf,128);
	bzero(tmp,128);

	/* NetBIOS protocol */
   	snprintf(buf,128, "nice -n 19 nbtscan -vh %s", ip);
	if((rf = popen(buf,"r")) == NULL){
		printf("NetBIOS popen() error!\n");
		exit(1);
	}

	/* parser NetBIOS */	
    while((fgets(tmp, sizeof(tmp), rf)) != NULL){
	   	if(strstr(tmp,"Workstation Service")){
           	strcpy(hostname,strtok(tmp," "));
           	found = 1;
           	while((fgets(tmp, sizeof(tmp), rf)) != NULL)
           	{
               	if(strstr(tmp,"00-00-00-00-00-00")) // Linux samba will return wrong MAC Address.
				{
                   	found = 0;
                   	break;
               	}
           	}
           	break;
       	}
   	}	            
	pclose(rf);
    if(found == 1){
       	printf("\nHostName is %s\n", hostname);
   	snprintf(sqlcmd,256,"INSERT INTO result (ipv4, hostname, date, seconds) VALUES('%s', '%s', '%s', %d);", ip, hostname, ctime(&insert_date), seconds);
	    sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt, NULL);
        sqlite3_step(stmt);
    	sqlite3_reset(stmt);
		sqlite3_finalize(stmt);
		sqlite3_free(errMsg);	
    	sqlite3_close(hostname_db);
		return;
	}
	printf("NetBIOS query Failure!\n");
	
	/* DNS protocol */
	bzero(buf,128);  
   	snprintf(buf,128, "nice -n 19 dnsquery -n %s 2>/dev/null", ip);
	if((rf = popen(buf,"r")) == NULL){
		printf("dnsquery popen() error!\n");
		exit(1);
	}

	/* parser DNS */
	while( (fgets(tmp, sizeof(tmp), rf)) != NULL) {
		strcpy(hostname,strtok(tmp,"\n"));
		if(0 == strcmp(hostname, "Failure")){
			printf("DNS query Failure!\n");
			bzero(hostname,256);
   			pclose(rf);
			break;
		}else{
			printf("\nHostName is %s\n", hostname);
       		pclose(rf);
   			snprintf(sqlcmd,256,"INSERT INTO result (ipv4, hostname, date, seconds) VALUES('%s', '%s', '%s', %d);", ip, hostname, ctime(&insert_date), seconds);
           	sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt, NULL);
           	sqlite3_step(stmt);
   			sqlite3_reset(stmt);
           	sqlite3_finalize(stmt);
			sqlite3_free(errMsg);	
   			sqlite3_close(hostname_db);
			return;
		}	
    }
	/* Bonjour protocol */
    bzero(buf,128);
   	snprintf(buf,128, "nice -n 19 mDNSIdentify %s 2>/dev/null", ip);
	if((rf = popen(buf,"r")) == NULL){
		printf("Bonjour popen() error!\n");
		exit(1);
	}
	/* parser Bonjour */
    while((fgets(tmp, sizeof(tmp), rf)) != NULL){
      	if(strstr(tmp,"Addr")){
            strcpy(hostname,strtok(strtok(tmp," "),"."));
            printf("\nHostName is %s\n", hostname);
       		pclose(rf);
   			snprintf(sqlcmd,256,"INSERT INTO result (ipv4, hostname, date, seconds) VALUES('%s', '%s', '%s', %d);", ip, hostname, ctime(&insert_date), seconds);
            sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt, NULL);
            sqlite3_step(stmt); 
    		sqlite3_reset(stmt);
			sqlite3_finalize(stmt);
			sqlite3_free(errMsg);	
    		sqlite3_close(hostname_db);
			return;
        }
    }	
	printf("Bonjour query Failure!\n");    
   	pclose(rf);
	sqlite3_free(errMsg);	
	/* Close database */
    sqlite3_close(hostname_db);

	return;
}

void hostnamelookup_del(char* ip)
{
    sqlite3 *hostname_db, *IPlist_db;
    sqlite3_stmt *stmt = NULL;
	char sqlcmd[256];
	int rc;

    /* Open database */
    if(sqlite3_open_v2(HOSTNAME_DB_PATH, &hostname_db, SQLITE_OPEN_READWRITE, NULL)) {
        return;
    }

    snprintf(sqlcmd,256, "DELETE FROM result where ipv4='%s' ;", ip);                                          
    sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt, NULL);
    rc = sqlite3_step(stmt);
	if(rc != SQLITE_DONE) exit(-1);
    sqlite3_reset(stmt);
    sqlite3_finalize(stmt);

    /* Close database */
    sqlite3_close(hostname_db);

    /* Open database hostnametmp.db*/
	rc = sqlite3_open("/tmp/hostnametmp.db", &IPlist_db);
	if(rc != SQLITE_OK) {
		fprintf(stderr,"Cannot open hostnametmp.db: %s\n",sqlite3_errmsg(IPlist_db));
		return;
    }
    
	snprintf(sqlcmd,256, "DELETE FROM IPlist where ipv4='%s' ;", ip);
	sqlite3_prepare_v2(IPlist_db,sqlcmd,256, &stmt, NULL);
	sqlite3_step(stmt);
    sqlite3_reset(stmt);
	sqlite3_finalize(stmt);
	
    sqlite3_close(IPlist_db);
	return;
}
void hostnamelookup_list()
{
    sqlite3 *hostname_db;
    char sqlcmd[256] = "SELECT * FROM result;"; 
    char *errMsg = NULL;	
	int row=0, column=0;
	char **result;
	int i = 0,rc;
	
    /* Open database */
    rc = sqlite3_open("/tmp/hostname.db",&hostname_db);
	if(rc != SQLITE_OK){
		printf("Can't open database to insert signatures: %s\n", sqlite3_errmsg(hostname_db));
        return;
	}
	
   	/* Create table */
    if(sqlite3_exec(hostname_db, resultTB, 0, 0, &errMsg) == SQLITE_OK)
		fprintf(stderr,"create table first!\n");
	
	/* Get all hostname from result table */
	sqlite3_get_table(hostname_db, sqlcmd, &result, &row, &column, &errMsg);
	
	if(row == 0){
		printf("Database /tmp/hostname.db is empty\n");
		/* Release table */
    	sqlite3_free_table(result);
    	sqlite3_free(errMsg);
    	/* Close database */
    	sqlite3_close(hostname_db);
		return;
	}

	
	/* show all hostname from result table */
//	printf( "row:%d column=%d \n" , row , column );
	printf("%-15s | %-35s | %s\n", result[0], result[1], result[2]);
	printf("-------------------------------------------------------------------------------------------\n");
 	for( i=4 ; i<( row + 1 ) * column ; i+=4 ){
  		printf( "%-15s | %-35s | %s\n", result[i], result[i+1], result[i+2]);
	}

    /* Release table */
    sqlite3_free_table(result);
	sqlite3_free(errMsg);	
	/* Close database */
	sqlite3_close(hostname_db);
}

void hostnamelookup_del_all() 
{
    sqlite3 *hostname_db, *IPlist_db;
	sqlite3_stmt *stmt;
    char sqlcmd[256] = "DELETE FROM result;";
	int rc;
   
    /* Open database */
    if(sqlite3_open_v2(HOSTNAME_DB_PATH, &hostname_db, SQLITE_OPEN_READWRITE, NULL)) {
        return;
    }   

    /* Delete all from result table */
    sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt, NULL);
   	rc = sqlite3_step(stmt);
	if(rc != SQLITE_DONE) exit(-1);
   	sqlite3_reset(stmt);
	sqlite3_finalize(stmt);

    /* Close database */
    sqlite3_close(hostname_db);
   	
    /* Open database hostnametmp.db*/
	rc = sqlite3_open("/tmp/hostnametmp.db", &IPlist_db);
	if(rc != SQLITE_OK) {
		fprintf(stderr,"Cannot open hostnametmp.db: %s\n",sqlite3_errmsg(IPlist_db));
		return;
    }

    /* Delete all from IPlist table */
    snprintf(sqlcmd,256, "DELETE FROM IPlist ;");
	sqlite3_prepare_v2(IPlist_db,sqlcmd,256, &stmt, NULL);
	sqlite3_step(stmt);
    sqlite3_reset(stmt);
	sqlite3_finalize(stmt);
	
    sqlite3_close(IPlist_db);
	return;
}
void hostnamelookup_do_request()
{  
    sqlite3 *hostname_db, *IPlist_db;
    sqlite3_stmt *stmt_c;
    char sqlcmd[256] = "SELECT * FROM result;";
    char *errMsg = NULL;
    int row=0, column=0;
    char **result;
    int i = 0,rc;

    /* Open database */
    rc = sqlite3_open("/tmp/hostname.db", &hostname_db);
    if(rc != SQLITE_OK) {
        fprintf(stderr,"Cannot open hostname_db: %s\n",sqlite3_errmsg(hostname_db));
        return;
    }

    /* Get all hostname from result table */
    sqlite3_get_table(hostname_db, sqlcmd, &result, &row, &column, &errMsg);

    if(row == 0){
        /* Release table */
        sqlite3_free_table(result);
        sqlite3_free(errMsg);
        /* Close database */
        sqlite3_close(hostname_db);
        return;
    }

    time_t insert_date;
    int seconds = time(&insert_date);

    /* Open database hostnametmp.db*/
	rc = sqlite3_open("/tmp/hostnametmp.db", &IPlist_db);
	if(rc != SQLITE_OK) {
		fprintf(stderr,"Cannot open hostnametmp.db: %s\n",sqlite3_errmsg(IPlist_db));
		return;
    }

    for( i=4 ; i<( row + 1 ) * column ; i+=4 ){
		if(seconds - atoi(result[i+3]) >= 86400){
			snprintf(sqlcmd,256, "DELETE FROM result where ipv4='%s' ;", result[i]);
			sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt_c, NULL);
    		sqlite3_step(stmt_c);            
    		sqlite3_reset(stmt_c);
    		sqlite3_finalize(stmt_c); 

   			snprintf(sqlcmd,256, "DELETE FROM IPlist where ipv4='%s' ;", result[i]);
			sqlite3_prepare_v2(IPlist_db,sqlcmd,256, &stmt_c, NULL);
			sqlite3_step(stmt_c);
   			sqlite3_reset(stmt_c);
			sqlite3_finalize(stmt_c);
    		
		}else
        	hostnamelookup_compare(result[i], result[i+1]);
    }
    /* Release table */
    sqlite3_free_table(result);
    sqlite3_free(errMsg);
    /* Close database */
    sqlite3_close(hostname_db);
    sqlite3_close(IPlist_db);
}
void hostnamelookup_compare(char* ip, char* old_name)
{
    sqlite3 *hostname_db, *IPlist_db;
    sqlite3_stmt *stmt_c;
	char sqlcmd[256] = "";
    int found = 0; // found hostname = 1;
	int rc;
    char buf[128]="";
    char tmp[128]="";
    FILE *rf;	
	char new_hostname[256]="";

    /* Open database */
    rc = sqlite3_open("/tmp/hostname.db", &hostname_db);
    if(rc != SQLITE_OK) {
	    fprintf(stderr,"Cannot open hostname_db: %s\n",sqlite3_errmsg(hostname_db));
    	return;
    }
	
	
    bzero(new_hostname, 256);
    bzero(buf,128);
    bzero(tmp,128);

	/* NetBIOS protocol */
   	snprintf(buf,128, "nice -n 19 nbtscan -vh %s", ip);
	if((rf = popen(buf,"r")) == NULL){
		printf("NetBIOS popen() error!\n");
		exit(1);
	}
	/* parser NetBIOS */
    while((fgets(tmp, sizeof(tmp), rf)) != NULL){
    	if(strstr(tmp,"Workstation Service")){
            strcpy(new_hostname,strtok(tmp," "));
            found = 1;
            while((fgets(tmp, sizeof(tmp), rf)) != NULL){   
                if(strstr(tmp,"00-00-00-00-00-00")) // Linux samba will return wrong MAC Address.
                {
                    found = 0;
                    break;
                }
            }
            break;
        }
    }
	pclose(rf);
    if(found == 1 && 0 == strcmp(new_hostname,old_name)){
        sqlite3_close(hostname_db);
		return ;
    }else if(found == 1 && 0 != strcmp(new_hostname,old_name)){
		snprintf(sqlcmd,256,"UPDATE result set hostname='%s' where ipv4='%s' and hostname='%s';", new_hostname,ip,old_name);
        sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt_c, NULL);
        sqlite3_step(stmt_c);            
        sqlite3_reset(stmt_c);
		sqlite3_finalize(stmt_c);        
        sqlite3_close(hostname_db); 
		return ;
    }
	/* DNS protocol */
    bzero(buf,128);
   	snprintf(buf,128, "nice -n 19 dnsquery -n %s 2>/dev/null", ip);
	if((rf = popen(buf,"r")) == NULL){
		printf("DNS query popen() error!\n");
		exit(1);
	}

    /* parser DNS */
    while( (fgets(tmp, sizeof(tmp), rf)) != NULL) {
        strcpy(new_hostname,strtok(tmp,"\n"));
        if(0 == strcmp(new_hostname, "Failure")){   
			bzero(new_hostname, 256);
			pclose(rf);
            break;
        }else if(0 == strcmp(new_hostname,old_name)){
          	sqlite3_close(hostname_db);
			pclose(rf);
			return ;
		}else if(0 != strcmp(new_hostname,old_name)){            
			snprintf(sqlcmd,256,"UPDATE result set hostname='%s' where ipv4='%s' and hostname='%s';", new_hostname,ip,old_name);
           	sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt_c, NULL);
           	sqlite3_step(stmt_c);            
           	sqlite3_reset(stmt_c);
           	sqlite3_finalize(stmt_c);        
           	sqlite3_close(hostname_db); 
       		pclose(rf);
    		return ;
        }
    }
		
	/* Bonjour protocol */
    bzero(buf,128);
   	snprintf(buf,128, "nice -n 19 mDNSIdentify %s 2>/dev/null", ip);
	if((rf = popen(buf,"r")) == NULL){
		printf("Bonjour popen() error!\n");
		exit(1);
	}
    /* parser Bonjour */
    while((fgets(tmp, sizeof(tmp), rf)) != NULL){
        if(strstr(tmp,"Addr")){   
            strcpy(new_hostname,strtok(strtok(tmp," "),"."));
			if(0 == strcmp(new_hostname,old_name)){
           		sqlite3_close(hostname_db);
				pclose(rf);
				return ;
			}else if(0 != strcmp(new_hostname,old_name)){
				snprintf(sqlcmd,256,"UPDATE result set hostname='%s' where ipv4='%s' and hostname='%s';", new_hostname,ip,old_name);
           		sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt_c, NULL);
           		sqlite3_step(stmt_c);    
           		sqlite3_reset(stmt_c);
           		sqlite3_finalize(stmt_c);        
           		sqlite3_close(hostname_db); 
       			pclose(rf);
               	return ;
			}
        }
    }
    pclose(rf);
	printf("Can't find %s when send request\n",ip);
    snprintf(sqlcmd,256, "DELETE FROM result where ipv4='%s' ;", ip);
	sqlite3_prepare_v2(hostname_db,sqlcmd,256, &stmt_c, NULL);
    sqlite3_step(stmt_c);            
    sqlite3_reset(stmt_c);
    sqlite3_finalize(stmt_c); 

    /* Close database */
    sqlite3_close(hostname_db);

    /* Open database hostnametmp.db*/
	rc = sqlite3_open("/tmp/hostnametmp.db", &IPlist_db);
	if(rc != SQLITE_OK) {
		fprintf(stderr,"Cannot open hostnametmp.db: %s\n",sqlite3_errmsg(IPlist_db));
		return;
    }

   	snprintf(sqlcmd,256, "DELETE FROM IPlist where ipv4='%s' ;", ip);
	sqlite3_prepare_v2(IPlist_db,sqlcmd,256, &stmt_c, NULL);
	sqlite3_step(stmt_c);
   	sqlite3_reset(stmt_c);
	sqlite3_finalize(stmt_c);
		
    sqlite3_close(IPlist_db);
	
	return;
}

int main(int argc, char** argv)
{
	char hostname[256]="";
    if(argc < 2){
        print_usage(argv[0]); 
        exit(0);
    }
  	
	if(!strcmp(argv[1],"list"))
	{
		if(argc != 2)
		{
			print_usage(argv[0]);
			exit(0);
		}
		hostnamelookup_list();
	}
	else if(!strcmp(argv[1],"del_all"))
	{
        if(argc != 2)
        {   
            print_usage(argv[0]);
            exit(0);
        }
		hostnamelookup_del_all();
	}
    else if(!strcmp(argv[1],"do_req"))                                                                                        
    {  
        if(argc != 2)
        {   
            print_usage(argv[0]);          
            exit(0);
        }
		hostnamelookup_do_request();
    }	
    else if(!strcmp(argv[1],"addv2"))
    {  
        if(argc != 3)
        {
            print_usage(argv[0]);          
            exit(0);
        }
        hostnamelookup_addv2(argv[2], hostname, sizeof(hostname));
    } 
	else if(!strcmp(argv[1],"add"))
	{
		if(argc != 3)
		{
			print_usage(argv[0]);
            exit(0);
		}
		hostnamelookup_add(argv[2], hostname, sizeof(hostname));
	}
	else if(!strcmp(argv[1],"del"))
	{
        if(argc != 3)
        {
            print_usage(argv[0]);
            exit(0);
        }
		hostnamelookup_del(argv[2]);
	}
	else
		print_usage(argv[0]);

	return 0;	
}
