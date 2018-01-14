/*
 *------------------------------------------------------------------
 * hostnamelookup.h - Gets hostname from ip address APIs 
 *
 * May 2013
 *
 * Copyright (c) 2006-2010 by cisco Systems, Inc.
 * All rights reserved.
 *------------------------------------------------------------------
 */

#ifndef __HOSTNAMELOOKUP_H__
#define __HOSTNAMELOOKUP_H__

#include <sqlite3.h>
#include <netinet/in.h>
#include <arpa/inet.h>            
#include <sys/socket.h>
#include <time.h>

#define HOSTNAME_TIMEOUT_SET "/tmp/hostname_timeout_set" 
#define HOSTNAME_DB_PATH "/tmp/hostname.db"
#define HOSTNAME_DB_TMP_PATH "/tmp/hostnametmp.db"

extern void print_usage(char *program);
extern void hostnamelookup_addv2(char* ip, char* hostname, int len);
extern void addv2_netbios(char* ip, char* hostname);
extern void addv2_dns(char* ip, char* hostname);
extern void addv2_bonjour(char* ip, char* hostname);
extern void hostnamelookup_add(char* ip, char* hostname, int len);
extern void hostnamelookup_del(char* ip);
extern void hostnamelookup_list();
extern void hostnamelookup_del_all();
extern void hostnamelookup_timeout(char* timeout);
extern void hostnamelookup_do_request();
extern void hostnamelookup_compare(char* ip, char* hostname );



#endif /* __HOSTNAMELOOKUP_H__ */

