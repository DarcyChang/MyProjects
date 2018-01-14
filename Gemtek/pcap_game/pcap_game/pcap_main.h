#ifndef PCAP_MAIN_H_INCLUDED
#define PCAP_MAIN_H_INCLUDED

typedef char int8;
typedef short int16;
typedef int int32;
typedef unsigned char u_int8;
typedef unsigned short u_int16;
typedef unsigned int u_int32;

#define IP 0x0008
#define ICMP 0x01
#define TCP 0x06
#define UDP 0x11

#define RESULT_FILE_NAME "result.out"

typedef enum fun_mode{
	ip = 0,
	statistic = 1,
	undefined = 2
}FUN_MODE;

typedef enum compare_rst{
	less = 0,
	greater = 1,
	equal = 2,
	unknown
}COMPARE_RST;

/* pcap file header */
typedef struct pcap_file_header{
	u_int32 magic;
	u_int16 version_major;
	u_int16 version_minor;
	int32 thiszone;          /* gmt to local correction */
	u_int32 sigfigs;           /* accuracy of timestamps */
	u_int32 snaplen;           /* max length saved portion of each pkt */
	u_int32 linktype;          /* data link type (LINKTYPE_*) */
}PCAP_FILE_HEADER;

/* pcap packet header */
typedef struct pcap_pkthdr{
	struct timeval ts;      /* time stamp */
	u_int32 caplen;    /* length of portion present */
	u_int32 len;       /* length this packet (off wire) */
}PCAP_PKTHDR;

/* MAC header */
typedef struct mac_header{
	u_int8 mac_dst[6];      /* destination mac address*/
	u_int8 mac_src[6];    /* source mac address*/
	u_int16 mac_msg;       /* message type */
}MAC_HDR;

/* IP header */
typedef struct ip_header{
	u_int8 ip_ver_ihl;            /* Version(4bits)  and IHL(4bits) */
	u_int8 ip_tos;               /* Type of Service */
	u_int16 ip_len;            /* Total Length  */
	u_int16 ip_id;             /* Identification */
	u_int16 ip_flahs_off;      /* Flags(3 bits) and Fragment Offset(13bits) */
	u_int8 ip_ttl;               /* Time to Live */
	u_int8 ip_p;                 /* Protocol */
	u_int16 ip_sum;            /* Header Checksum */
	u_int32 ip_src;                /* Source Address */
	u_int32 ip_dst;                /* Destination Address */
	//u_int32 ip_op_pad;             /* Option and Padding */
}IP_HDR;

/* TCP header */
typedef struct tcp_header{
	u_int16 th_sport;      /* source port */
	u_int16 th_dport;      /* destination port */
	u_int32 th_seq;        /* sequence number */
	u_int32 th_ack;        /* acknowledgement number */
	u_int16 off;       /* data offset, Reserved and Code*/
	u_int16 th_win;    /* window */
	u_int16 th_sum;    /* checksum */
	u_int16 th_urp;    /* urgent pointer */
}TCP_HDR;

/* UDP header*/
typedef struct udp_header{
	u_int16 sport; /* Source port */
	u_int16 dport; /* Destination port */
	u_int16 len;   /* Datagram length */
	u_int16 crc;   /* Checksum */
}UDP_HDR;

/* ICMP packet structure. */
typedef struct icmp_header{
	u_int8 icmp_type; /* ICMP message type*/
	u_int8 icmp_code; /* ICMP operation code */
	u_int16 icmp_chk; /* ICMP checksum */
}ICMP_HDR;

typedef struct pcap_data{
	u_int32 SourceIPAddress;
	u_int32 DestinationIPAddress;
	u_int8 Protocol;
	u_int16 SourcePort;
	u_int16 DestinationPort;
	u_int8 Type;
	u_int8 Code;
	u_int32 counts;
}PCAP_DATA;

/* AVL node*/
typedef struct node{
    PCAP_DATA *data;
    struct node*  left;
    struct node*  right;
    int      height;
} AVL_NODE;

typedef struct avl_tree_statistic{
	u_int32 node_counts;
	u_int32 total_counts_in_all_nodes;
	u_int32 LL_num;
	u_int32 LR_num;
	u_int32 RR_num;
	u_int32 RL_num;
}AT_STAT;

void show_node_info(PCAP_DATA *data);
void print_usage(void);

#endif /* PCAP_MAIN_H_INCLUDED */
