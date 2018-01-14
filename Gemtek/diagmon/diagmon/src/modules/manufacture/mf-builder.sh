#! /bin/sh

if [ $# != 3 ]; then
	echo "Usage mf-builder.sh add [feature name] [backdoor string]"
elif [ -n $2 ]; then
	mkdir feature/$2;
	cp Sample/Sample.c feature/$2/$2.c;
	cp Sample/Sample.h feature/$2/$2.h;
	cp Sample/rule.mk feature/$2/rule.mk;
	sed -i s/Sample/$2/g feature/$2/$2.c;
	sed -i s/Sample/$2/g feature/$2/$2.h;
	sed -i s/Sample/$2/g feature/$2/rule.mk;
	if [ -n $3 ]; then
		sed -i s/String/$3/g feature/$2/$2.c;
		echo "Create the feature test!!!"
		echo "please add \"{\"$3_Req\", $2},\" in include/handlers.h"
		echo "please add \"-include feature/$2/rule.mk\" in feature/rule.mk"
	fi
fi
