#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/time.h>
#include <sys/stat.h>
#include "pcap_main.h"

#define PCAP_DEBUG 0
#define OUTPUT2FILE 0
#define OPTIMIZE_ANALYSIS 0

FUN_MODE function_mode = undefined;
char file_name[256]; /* pacp file name and path.*/
char program[16];
u_int32 target_src_ip;
u_int32 target_dst_ip;
u_int8 pkt_buf[2048];
u_int8 *p_buf;
FILE *wf_result_file = NULL;

PCAP_FILE_HEADER pcap_header;
PCAP_PKTHDR pcap_pkthdr;
MAC_HDR mac_hdr;
IP_HDR ip_hdr;
TCP_HDR tcp_hdr;
UDP_HDR udp_hdr;
ICMP_HDR icmp_hdr;

AVL_NODE *root = NULL;

u_int32 pcap_pkt_counts = 0;
u_int32 pkt_skipped_num = 0;
AT_STAT at_stat;

#define READ_BUF_SIZE (1<<14)
u_int32 unchecked_len = 0;
u_int8 read_buf[READ_BUF_SIZE];


/* 
* func_name: compare_key_data
* key < data, return less
* key > data, return greater
* key == data, return equal
*/
static COMPARE_RST compare_key_data(PCAP_DATA *key, PCAP_DATA *data)
{
	if(function_mode == statistic) {
		if(key->SourceIPAddress < data->SourceIPAddress)
			return less;
		if(key->SourceIPAddress > data->SourceIPAddress)
			return greater;
		
		if(key->DestinationIPAddress < data->DestinationIPAddress)
			return less;
		if(key->DestinationIPAddress > data->DestinationIPAddress)
			return greater;
	}
	
	if(key->Protocol < data->Protocol)
		return less;
	if(key->Protocol > data->Protocol)
		return greater;
	
	if(key->Protocol == ICMP) {
		if(key->Type < data->Type)
			return less;
		else if(key->Type > data->Type)
			return greater;
		else
			return equal;

	}else if(key->Protocol == TCP || key->Protocol == UDP){
		if(key->SourcePort < data->SourcePort)
			return less;
		else if(key->SourcePort > data->SourcePort)
			return greater;
		else
			return equal;

	}else {
		printf("skipped protocol\n");
	}
	
	return unknown;
}


/*
    AVL Tree: get the height of a node
*/
static int height( AVL_NODE* n )
{
    if( n == NULL )
        return -1;
    else
        return n->height;
}
 
/*
    AVL Tree: get maximum value of two integers
*/
static int max( int l, int r)
{
    return l > r ? l: r;
}
 
/*
    AVL Tree: 
    perform a rotation between a k2 node and its left child
 
    note: call single_rotate_with_left only if k2 node has a left child
*/
static AVL_NODE* single_rotate_with_left( AVL_NODE* k2 )
{
    AVL_NODE* k1 = NULL;
#if PCAP_DEBUG
	at_stat.LL_num++;
#endif
 
    k1 = k2->left;
    k2->left = k1->right;
    k1->right = k2;
 
    k2->height = max( height( k2->left ), height( k2->right ) ) + 1;
    k1->height = max( height( k1->left ), k2->height ) + 1;
    return k1; /* new root */
}
 
/*
    AVL Tree: 
    perform a rotation between a node (k1) and its right child
 
    note: call single_rotate_with_right only if
    the k1 node has a right child
*/
static AVL_NODE* single_rotate_with_right( AVL_NODE* k1 )
{
    AVL_NODE* k2;
#if PCAP_DEBUG
	at_stat.RR_num++;
#endif	
 
    k2 = k1->right;
    k1->right = k2->left;
    k2->left = k1;
 
    k1->height = max( height( k1->left ), height( k1->right ) ) + 1;
    k2->height = max( height( k2->right ), k1->height ) + 1;
 
    return k2;  /* New root */
}

/*
    AVL Tree: 
    perform the left-right double rotation,
 
    note: call double_rotate_with_left only if k3 node has
    a left child and k3's left child has a right child
*/
static AVL_NODE* double_rotate_with_left( AVL_NODE* k3 )
{
#if PCAP_DEBUG
	at_stat.LR_num++;
#endif	
    /* Rotate between k1 and k2 */
    k3->left = single_rotate_with_right( k3->left );
 
    /* Rotate between K3 and k2 */
    return single_rotate_with_left( k3 );
}
 
/*
   AVL Tree: 
   perform the right-left double rotation
 
   notes: call double_rotate_with_right only if k1 has a
   right child and k1's right child has a left child
*/
static AVL_NODE* double_rotate_with_right( AVL_NODE* k1 )
{
#if PCAP_DEBUG
	at_stat.RL_num++;
#endif	
    /* rotate between K3 and k2 */
    k1->right = single_rotate_with_left( k1->right );
 
    /* rotate between k1 and k2 */
    return single_rotate_with_right( k1 );
}

/*
    AVL Tree:
    remove all nodes of an AVL tree
*/
void dispose(AVL_NODE* t)
{
    if( t != NULL )
    {
        dispose( t->left );
        dispose( t->right );
        free( t );
    }
}
 
/*
    AVL Tree: 
    insert a new node into the tree
*/
static AVL_NODE* insert(PCAP_DATA *key, AVL_NODE* t )
{
    if( t == NULL )
    {
        /* Create and return a one-node tree */
#if PCAP_DEBUG
			printf("parent is null\n");
#endif
        t = (AVL_NODE*) calloc(1, sizeof(AVL_NODE));
        if( t == NULL )
        {
            fprintf (stderr, "Out of memory!!! (insert)\n");
            exit(1);
        }
        else
        {
            t->data = key;
            t->height = 0;
            t->left = t->right = NULL;
        }
    }
    else if( compare_key_data(key, t->data) == less)
    {
        t->left = insert( key, t->left );
        if( height( t->left ) - height( t->right ) == 2 ) {
            if( compare_key_data(key, t->left->data) == less)
                t = single_rotate_with_left( t );
            else
                t = double_rotate_with_left( t );
        }
    } 
	else if( compare_key_data(key, t->data) == greater)
	{
        t->right = insert( key, t->right );
        if( height( t->right ) - height( t->left ) == 2 ) {
            if( compare_key_data(key, t->right->data) == greater)
                t = single_rotate_with_right( t );
            else
                t = double_rotate_with_right( t );
        }
    }
	else
	{
		t->data->counts++;
	}
		
    /* Else X is in the tree already; we'll do nothing */
 
    t->height = max( height( t->left ), height( t->right ) ) + 1;
    return t;
}


static int check_pcap_ip_statistic(void)
{	
	PCAP_DATA *pcap_data;
	
	p_buf = pkt_buf;
	memcpy(&mac_hdr, p_buf, sizeof(mac_hdr));
	if(mac_hdr.mac_msg != IP) {
		pkt_skipped_num++;
#if PCAP_DEBUG		
		printf("[%d] found non-ip packet, type = 0x%04x\n", pcap_pkt_counts, htons(mac_hdr.mac_msg));
#endif
		return 0;
	}
	
	p_buf += sizeof(MAC_HDR); //skip MAC header
	memcpy(&ip_hdr, p_buf, sizeof(ip_hdr));
	
	if(function_mode == ip && (ip_hdr.ip_src != target_src_ip || ip_hdr.ip_dst != target_dst_ip)) {
		pkt_skipped_num++;
#if PCAP_DEBUG	
		printf("[%d] src_ip = 0x%08x, dst_ip = 0x%08x doesn't match\n", pcap_pkt_counts, ip_hdr.ip_src, ip_hdr.ip_dst);
#endif
		return 0;
	}

	pcap_data = (PCAP_DATA*) calloc(1, sizeof(PCAP_DATA));
	pcap_data->SourceIPAddress = htonl(ip_hdr.ip_src);
	pcap_data->DestinationIPAddress = htonl(ip_hdr.ip_dst);
	pcap_data->Protocol = ip_hdr.ip_p;

	if(ip_hdr.ip_p == TCP) {
		p_buf += sizeof(IP_HDR);
		memcpy(&tcp_hdr, p_buf, sizeof(tcp_hdr));
		pcap_data->SourcePort = htons(tcp_hdr.th_sport);
		pcap_data->DestinationPort = htons(tcp_hdr.th_dport);

	}else if (ip_hdr.ip_p == UDP) {
		p_buf += sizeof(IP_HDR);
		memcpy(&udp_hdr, p_buf, sizeof(udp_hdr));
		pcap_data->SourcePort = htons(udp_hdr.sport);
		pcap_data->DestinationPort = htons(udp_hdr.dport);
		
	}else if(ip_hdr.ip_p == ICMP) {
		p_buf += sizeof(IP_HDR);
		memcpy(&icmp_hdr, p_buf, sizeof(icmp_hdr));
		pcap_data->Type = icmp_hdr.icmp_type;
		pcap_data->Code = icmp_hdr.icmp_code;
	}else {
		pkt_skipped_num++;
#if PCAP_DEBUG		
		printf("IP protocol is 0x%x will skip\n", ip_hdr.ip_p);
#endif
		return 0;
	}
	pcap_data->counts = 1;	
	root = insert(pcap_data, root);
		
	return 0;
}

#if OUTPUT2FILE
void output_node_info(PCAP_DATA *data)
{
	FILE *wf = wf_result_file;
	
	u_int32 src_ip = htonl(data->SourceIPAddress);
	u_int32 dst_ip = htonl(data->DestinationIPAddress);

	fprintf(wf, "<%d>\t", at_stat.node_counts);
	fprintf(wf, "%d.%d.%d.%d", (src_ip >> 24) & 0xff, (src_ip >> 16) & 0xff, (src_ip >> 8) & 0xff, src_ip & 0xff);
	fprintf(wf, "  %d.%d.%d.%d", (dst_ip >> 24) & 0xff, (dst_ip >> 16) & 0xff, (dst_ip >> 8) & 0xff, dst_ip & 0xff);
	
	if(data->Protocol == TCP){
		fputs("  TCP", wf);
		fprintf(wf, "  sp:%d  dp:%d", data->SourcePort, data->DestinationPort);

	}else if(data->Protocol == UDP) {
		fputs("  UDP", wf);
		fprintf(wf, "  sp:%d  dp:%d", data->SourcePort, data->DestinationPort);
	}else {
		fputs("  ICMP", wf);
		fprintf(wf, "  type=%d  code=%d", data->Type, data->Code);
	}

	fprintf(wf, "  counts=%d\n", data->counts);

}


void output_inorder(AVL_NODE *ptr)
{
	if(ptr != NULL) {
		output_inorder(ptr->left);
		output_node_info(ptr->data);
		at_stat.total_counts_in_all_nodes += ptr->data->counts;
		at_stat.node_counts++;
		output_inorder(ptr->right);
	}
}

int output_result(AVL_NODE *ptr)
{
	FILE *wf = NULL;
	
	if((wf_result_file = fopen(RESULT_FILE_NAME, "w")) == NULL) {
		printf("Cannot open pcap file %s\n", "result.out");
		return -1;
	}

	wf = wf_result_file;

	//memset(op_str, 0x0, sizeof(op_str));

	fputs("\n", wf);
	fputs("*************************************************\n", wf);
	fputs("***           Show analysis result            ***\n", wf);
	fputs("*************************************************\n", wf);
	fputs("\n", wf);
	fputs("<idx> ", wf);
	if(function_mode == statistic) {
		fputs("  sip  |", wf);
		fputs("  dip  |", wf);
	}
	fputs("  protocol  |", wf);
	fputs("  L4 info  |", wf);
	fputs("  counts", wf);
	fputs("\n\n", wf);

	output_inorder(root);

	fputs("\n", wf);
	fputs("*************************************************\n", wf);
	fputs("Summary:", wf);
	fprintf(wf, "Total counts in all AVL nodes = %d\n", at_stat.total_counts_in_all_nodes);
	fprintf(wf, "Skipped packets num = %d\n", pkt_skipped_num);
	fprintf(wf, "Total packets number in PCAP file = %d\n", pcap_pkt_counts);
	fprintf(wf, "Total AVL tree nodes number = %d\n", at_stat.node_counts);
	
#if PCAP_DEBUG	
	fprintf(wf, "LL_num = %d\n", at_stat.LL_num);
	fprintf(wf, "LR_num = %d\n", at_stat.LR_num);
	fprintf(wf, "RR_num = %d\n", at_stat.RR_num);
	fprintf(wf, "RL_num = %d\n", at_stat.RL_num);
#endif

	fputs("*************************************************\n", wf);
	
	if(wf_result_file != NULL) {
		fclose(wf_result_file);
		wf_result_file = NULL;
	}
	return 0;
}
#endif

void show_node_info(PCAP_DATA *data)
{
	u_int32 src_ip = data->SourceIPAddress;
	u_int32 dst_ip = data->DestinationIPAddress;

	printf("<%d>\t", at_stat.node_counts);

	if(function_mode == statistic) {
		printf("%d.%d.%d.%d", (src_ip >> 24) & 0xff, (src_ip >> 16) & 0xff, (src_ip >> 8) & 0xff, src_ip & 0xff);
		printf("  %d.%d.%d.%d", (dst_ip >> 24) & 0xff, (dst_ip >> 16) & 0xff, (dst_ip >> 8) & 0xff, dst_ip & 0xff);
	}

	if(data->Protocol == TCP){
		printf("  TCP");
		printf("  sp:%d  dp:%d", data->SourcePort, data->DestinationPort);

	}else if(data->Protocol == UDP) {
		printf("  UDP");
		printf("  sp:%d  dp:%d", data->SourcePort, data->DestinationPort);
	}else {
		printf("  ICMP");
		printf("  type=%d  code=%d", data->Type, data->Code);
	}

	printf("  counts=%d\n", data->counts);

}

void inorder(AVL_NODE *ptr)
{
	if(ptr != NULL) {
		inorder(ptr->left);
		show_node_info(ptr->data);
		at_stat.total_counts_in_all_nodes += ptr->data->counts;
		at_stat.node_counts++;
		inorder(ptr->right);
	}
}

void display_all_node_info(AVL_NODE *ptr)
{
	printf("\n");
	printf("*************************************************\n");
	printf("***           Show analysis result            ***\n");
	printf("*************************************************\n");
	printf("\n");
	printf("<idx> ");
	if(function_mode == statistic) {
		printf("  sip  |");
		printf("  dip  |");
	}
	printf("  protocol  |");
	printf("  L4 info  |");
	printf("  counts");
	printf("\n\n");

	inorder(root);

	printf("\n");
	printf("*************************************************\n");
	printf("Summary:");
	printf("Total counts in all AVL nodes = %d\n", at_stat.total_counts_in_all_nodes);
	printf("Skipped packets num = %d\n", pkt_skipped_num);
	printf("Total packets number in PCAP file = %d\n", pcap_pkt_counts);
	printf("Total AVL tree nodes number = %d\n", at_stat.node_counts);
	
#if PCAP_DEBUG	
	printf("LL_num = %d\n", at_stat.LL_num);
	printf("LR_num = %d\n", at_stat.LR_num);
	printf("RR_num = %d\n", at_stat.RR_num);
	printf("RL_num = %d\n", at_stat.RL_num);
#endif

	printf("*************************************************\n");
}


static int pcap_package_handle(void)
{
	int ret = 0;
	FILE *rf_pcap_file;
	char *p_read_buf = NULL;
	struct stat pcap_file;
	u_int32 total_pkt_cap_len = 0;

#if OPTIMIZE_ANALYSIS
	u_int32 total_read_size = 0;
	u_int32 total_read_counts = 0;
	u_int32 forward_counts = 0;
#endif	

	if((rf_pcap_file = fopen(file_name, "r")) == NULL) {
		printf("Cannot open pcap file %s\n", file_name);
		return -1;
	}

	fseek(rf_pcap_file, sizeof(pcap_header), SEEK_SET);
	total_pkt_cap_len += sizeof(pcap_header);
	
#if OPTIMIZE_ANALYSIS	
	total_read_size += sizeof(pcap_header);
#endif
	
	while(!feof(rf_pcap_file))
	{
		memset(read_buf, 0x0, sizeof(read_buf));
		unchecked_len = fread(read_buf, 1, READ_BUF_SIZE, rf_pcap_file);
		p_read_buf = (char*) read_buf;
		
#if OPTIMIZE_ANALYSIS	
		total_read_size += unchecked_len;
		total_read_counts++;
#endif		
		
		while(unchecked_len > 0)
		{
			if(unchecked_len < sizeof(PCAP_PKTHDR) + sizeof(MAC_HDR)) {
				fseek(rf_pcap_file, -(unchecked_len), SEEK_CUR);
				break;
			}
				
			memset(&pcap_pkthdr, 0x0, sizeof(pcap_pkthdr));
			memcpy(&pcap_pkthdr, p_read_buf, sizeof(pcap_pkthdr));
			unchecked_len -= sizeof(pcap_pkthdr);
			p_read_buf += sizeof(pcap_pkthdr);

#if OPTIMIZE_ANALYSIS	
			if((unchecked_len < pcap_pkthdr.caplen) 
				&& (unchecked_len > (sizeof(MAC_HDR)+sizeof(IP_HDR)+sizeof(TCP_HDR))))
				forward_counts++;
#endif
			if(unchecked_len >= pcap_pkthdr.caplen) {
				pcap_pkt_counts++;
				total_pkt_cap_len += (pcap_pkthdr.caplen + sizeof(pcap_pkthdr));
			}else {
				fseek(rf_pcap_file, -(unchecked_len + sizeof(pcap_pkthdr)), SEEK_CUR);
				break;
			}
				
			memset(pkt_buf, 0x0, sizeof(pkt_buf));
			memcpy(pkt_buf, p_read_buf, pcap_pkthdr.caplen);
			unchecked_len -= pcap_pkthdr.caplen;
			p_read_buf += pcap_pkthdr.caplen;

			if(function_mode == ip || function_mode == statistic) {
				ret = check_pcap_ip_statistic();
			}else {
				printf("Undefined function mode");
				exit(EXIT_FAILURE);
			}
		}
	}

	stat(file_name, &pcap_file);
	if((int)pcap_file.st_size != total_pkt_cap_len) {
		printf("pcap file size doesn't equal total caplen in pcap file\n");
		printf("total packets cap_len = %d\n", total_pkt_cap_len);
		printf("pcap file size = %d\n", (int)pcap_file.st_size);
		return -1;
	}else {
		display_all_node_info(root);
	}

#if OPTIMIZE_ANALYSIS	
	printf("total_read_size = %d\n", total_read_size);
	printf("total_read_counts = %d\n", total_read_counts);
	printf("forward_counts = %d\n", forward_counts);
#endif	
	
#if OUTPUT2FILE	
	output_result(root);
#endif

	dispose(root);

	if(rf_pcap_file != NULL) {
		fclose(rf_pcap_file);
		rf_pcap_file = NULL;
	}

	return 0;
}


static int check_ip_address_legal(char* ip_str, u_int32* ip)
{
	struct in_addr inp; // in_addr need to modify, not use count. 
	int ip_range = 0, count[4] = {0};

	ip_range = inet_aton(ip_str,&inp);
	if(ip_range == 0 || sscanf(ip_str, "%d.%d.%d.%d", &count[0], &count[1], &count[2], &count[3]) != 4)
		return -1;

	*ip = (count[0] & 0xff) + ((count[1] & 0xff) << 8) + ((count[2] & 0xff) << 16) + ((count[3] & 0xff) << 24);
		
	return 0;	
}

static int pcap_file_verification(char* file_path)
{
	FILE *rf_pcap_file;
	u_int32 read_len = 0;
	
	if((rf_pcap_file = fopen(file_path, "r")) == NULL) {
		printf("Cannot open pcap file %s\n", file_path);
		return -1;
	}
	
	memset(&pcap_header, 0x0, sizeof(pcap_header));
	read_len = fread(&pcap_header, 1, sizeof(pcap_header), rf_pcap_file);
	if(read_len < sizeof(pcap_header)) {
		printf("pcap file format incorrect!!\n");
		return -1;
	}

	if(htonl(pcap_header.magic) != 0xd4c3b2a1) {
		printf("pcap file magic number incorrect [0x%08x]\n", pcap_header.magic);
		return -1;
	}

	if(rf_pcap_file != NULL) {
		fclose(rf_pcap_file);
		rf_pcap_file = NULL;
	}

	strcpy(file_name, file_path);
	return 0;
}


static int check_parameters(int argc, char** argv)
{
	int ret = 0;

	if(argc != 3 && argc != 5) {
		printf("Input parameters number is incorrect!\n");
		print_usage();
		return -1;
	}

	ret = pcap_file_verification(argv[1]);
	if(ret == -1) {
		printf("pcap file check failed\n");
		return -1;
	}
	
	if(!strcmp(argv[2], "ip")){
		ret = check_ip_address_legal(argv[3], &target_src_ip); //source ip
		if(ret != 0) {
			printf("Source ip [%s] is incorrect\n", argv[3]);
			return -1;
		}

		ret = check_ip_address_legal(argv[4], &target_dst_ip); //destination ip
		if (ret != 0) {
			printf("Destination ip [%s] is incorrect\n", argv[4]);
			return -1;
		}

		function_mode = ip;
	
	}else if(!strcmp(argv[2], "statistic")) {
	
		function_mode = statistic;
	
	}else {
		printf("Unknown parameter [%s]\n", argv[2]);
		print_usage();
		return -1;
	}

	return 0;
}


void print_usage()
{
	printf("\nUsage: "); 
	printf("%s <pacp file name> [options] \n\n", program);   
	printf("%s <pcap file name> ip <Source IP Address> <Destination IP Address>\n", program); 
	printf("%s <pcap file name> statistic\n", program); 
	printf("\n");
}

int main(int argc, char** argv)
{	
	int ret = 0;

	memset(&at_stat, 0x0, sizeof(AT_STAT));
	memset(program, 0x0, sizeof(program));
	strncpy(program, argv[0], sizeof(program));
	
	ret = check_parameters(argc, argv);
	if(ret == -1)
		exit(EXIT_FAILURE);

	ret = pcap_package_handle();
	if(ret == 0)
		printf("pcap analysis finish!\n");
	else
		printf("pcap analysis failed!\n");

	exit(EXIT_SUCCESS);
}

