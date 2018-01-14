#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <sys/types.h>

static int php_htoi(char *s)
{
	int value;
	int c;

	c = ((unsigned char *)s)[0];
	if (isupper(c))
		c = tolower(c);
	value = (c >= '0' && c <= '9' ? c - '0' : c - 'a' + 10) * 16;

	c = ((unsigned char *)s)[1];
	if (isupper(c))
		c = tolower(c);
	value += c >= '0' && c <= '9' ? c - '0' : c - 'a' + 10;

	return (value);
}

int php_url_decode(char *str, int len)
{
	char *dest = str;
	char *data = str;

	while (len--) {
		if (*data == '+') {
			*dest = ' ';
		}
		else if (*data == '%' && len >= 2 && isxdigit((int) *(data + 1))
				 && isxdigit((int) *(data + 2))) {
			*dest = (char) php_htoi(data + 1);
			data += 2;
			len -= 2;
		} else {
			*dest = *data;
		}
		data++;
		dest++;
	}
	*dest = '\0';
	return dest - str;
}

#if 0
wget -O video_info "http://www.youtube.com/get_video_info?video_id=DKxa9yhcN98"
./urldecoder $(sed 's/.*&url_encoded_fmt_stream_map=\([^&]*\)&.*/\1/g' video_info) | sed 's/,/\n/g' | grep hd720 | grep mp4 | sed -n '1,1p' > targetSrc.txt
./urldecoder $(sed 's/.*&url=\([^&]*\).*/\1/g' targetSrc.txt) > url.txt
./urldecoder $(sed 's/.*&sig=\([^&]*\).*/\1/g' targetSrc.txt) > sig.txt
wget -O video.mp4 $(cat url.txt)"&signature="$(cat sig.txt)
#endif

int main(int argc, char* argv[]) {

	if(argc < 2){
		return 0;
	}

	char *foo = argv[1];
	php_url_decode(foo, strlen(foo));
	printf("%s\n", foo);
	return 0;
}

