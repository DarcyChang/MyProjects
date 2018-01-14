#include <sys/time.h> /* for timeval */

#define ICMP 0x01
#define TCP 0x06
#define UDP 0x11

#define block 4096

/* pcap file header */
struct pcap_file_header {
    unsigned char magic[4];
    unsigned char version_major[2];
    unsigned char version_minor[2];
    unsigned char thiszone[4];          /* gmt to local correction */
    unsigned char sigfigs[4];           /* accuracy of timestamps */
    unsigned char snaplen[4];           /* max length saved portion of each pkt */
    unsigned char linktype[4];          /* data link type (LINKTYPE_*) */
};

/* pcap packet header */
struct pcap_pkthdr {
    struct timeval ts;      /* time stamp */
    unsigned char caplen[4];    /* length of portion present */
    unsigned char len[4];       /* length this packet (off wire) */
};

/* MAC header */
struct mac_header{
    unsigned char mac_dest_0_3[4];      /* destination mac address[0-3] */
    unsigned char mac_dest_4_5[2];  /* destination mac address[4-5] */
    unsigned char mac_source_0_1[2];    /* source mac address[0-1] */
    unsigned char mac_source_2_5[4];    /* source mac address[2-5] */
    unsigned char mac_msg[2];       /* message type */
};
/* IP header */
struct ip_header{
    unsigned char ip_ver_ihl            /* Version(4bits)  and IHL(4bits) */
    unsigned char ip_tos;               /* Type of Service */
    unsigned char ip_len[2];            /* Total Length  */
    unsigned char ip_id[2];             /* Identification */
    unsigned char ip_flahs_off[2];      /* Flags(3 bits) and Fragment Offset(13bits) */
    unsigned char ip_ttl;               /* Time to Live */
    unsigned char ip_p;                 /* Protocol */
    unsigned char ip_sum[2];            /* Header Checksum */
    unsigned char ip_src[4];                /* Source Address */
    unsigned char ip_dst[4];                /* Destination Address */
    unsigned char ip_op_pad[4];             /* Option and Padding */

};

/* TCP header */
struct tcp_header {
    unsigned char th_sport[2];      /* source port */
    unsigned char th_dport[2];      /* destination port */
    unsigned char th_seq[4];        /* sequence number */
    unsigned char th_ack[4];        /* acknowledgement number */
    unsigned char off[2];       /* data offset, Reserved and Code*/
    unsigned char th_win[2];    /* window */
    unsigned char th_sum[2];    /* checksum */
    unsigned char th_urp[2];    /* urgent pointer */
};

/* UDP header*/
struct udp_header{
    unsigned char sport[2]; /* Source port */
    unsigned char dport[2]; /* Destination port */
    unsigned char len[2];   /* Datagram length */
    unsigned char crc[2];   /* Checksum */
};

/* ICMP packet structure. */
struct icmp{
    unsigned char icmp_type; /* ICMP message type*/
    unsigned char icmp_code; /* ICMP operation code */
    unsigned char icmp_chk[2]; /* ICMP checksum */
};

struct pcap_game_data{
    unsigned char SourceIPAddress[4];
    unsigned char DestinationIPAddress[4];
    unsigned char Protocol;
    unsigned char SourcePort[2];
    unsigned char DestinationPort[2];
    unsigned char Type;
    unsigned char Code;
}

int main{

    int pcaket_count = 0;
    initial fp; 
	fp = 0B;
	
    Read the pcap_file_header magic.

    /* 檢查輸入之檔案是否為 pcap file */
    if(pcap_file_header.magic isn’t equal “d4 c3 b2 a1” )
        return error;
	fp += 24B
	
    /* Create memory 4096 Bytes */
    char mem_buf[block];
	char uncheck_len[block];
	char checked_len[block];
	


    while(flag == false && mem_buf <= flag_EOF){ // until end of pcap file last data frame
        memcpy data frame header and data frame into mem_buf
		memcpy mem_buf uncheck_len
		memcpy checked_len 0
        if(read length < block){
			set flag = true
            set flag_EOF = read length
        }
        while(uncheck_len >= data frame header + MAC + IP + Protocol){ /* uncheck data length */
            read caplen
            fp += 16B;
			checked_len += 16B
            read source IP
            read destination IP
            read protocol

            switch(protocol){
                case TCP
                    read source port
                    read destination port

                case UDP
                    read source port
                    read destination port

                case ICMP
                    read type
                    read code
            }
            pcaket_count++;
            indicate ip function or statistic function
            checked_len += caplen;
            uncheck_len = uncheck_len-(16+caplen); // memory uncheck data length = 4096 -(16+caplen)
            fp = fp+(caplen+16-uncheck_len); // Jump to next data frame header
			if(mem_len - checked_len < 16+MAC+IP+protocol) //Todo : necessary ?
				break;
        } // End while
		fp -= uncheck_len;
    } // end while
}
