#!/bin/sh

ERRORCODE=$(urldecoder $(cat /tmp/videos | grep 'errorcode=' | sed 's/.*errorcode=\([^&]*\)&.*/\1/g'))
if [ x"$ERRORCODE" != x ]; then
	echo "### WARN!WARN!WARN! ### /tmp/videos contents error: " > /dev/console
	echo "### WARN!WARN!WARN! ###" $(urldecoder $(cat /tmp/videos)) > /dev/console
fi

urldecoder $(sed 's/.*url_encoded_fmt_stream_map=\([^&]*\)&.*/\1/g' /tmp/videos) | sed 's/,/\n/g' | grep itag=$1 | grep mp4 | sed -n '1,1p' > /tmp/targetSrc.txt
urldecoder $(cat /tmp/targetSrc.txt | grep 's=' | sed 's/.*s=\([^&]*\).*/\1/g') > /tmp/s.txt
urldecoder $(sed 's/.*url=\([^&]*\).*/\1/g' /tmp/targetSrc.txt) > /tmp/url.txt
urldecoder $(sed 's/.*sig=\([^&]*\).*/\1/g' /tmp/targetSrc.txt) > /tmp/sig.txt

if [ -s /tmp/s.txt ]; then
	echo "### WARN!WARN!WARN! ### TODO: need to handle 's=' of Youtube file link" > /dev/console
fi

#goplayer_sample $(cat /tmp/url.txt)"&signature="$(cat /tmp/sig.txt)
#wget -O $2.mp4 --user-agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36' $(cat /tmp/url.txt)"&signature="$(cat /tmp/sig.txt)
