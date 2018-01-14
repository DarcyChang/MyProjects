ifneq ($(BR2_TOOLCHAIN_EXTERNAL_PATH),)
	MIPS_TOOLCHAIN_DIR=$(BR2_TOOLCHAIN_EXTERNAL_PATH)/bin
else
	MIPS_TOOLCHAIN_DIR=/opt/mipsel-4.4/bin
endif

ifneq ($(BR2_TOOLCHAIN_EXTERNAL_PREFIX),)
	CROSS_COMPILE=$(MIPS_TOOLCHAIN_DIR)/$(BR2_TOOLCHAIN_EXTERNAL_PREFIX)-
else
	CROSS_COMPILE=$(MIPS_TOOLCHAIN_DIR)/mipsel-linux-gnu-
endif

CXX=$(CROSS_COMPILE)g++

#MPATH=$(TOPDIR)/build/staging/usr
MPATH=/home/darcy/ALi/SDK-20130924/buildroot/build/staging/usr

INCLUDE=-I${MPATH}/include \
	-I${MPATH}/include/glib-2.0 \
        -I${MPATH}/lib/glib-2.0/include \
        -I${MPATH}/include/libxml2 \
        -I${MPATH}/include/gstreamer-0.10
L_PATH=-L${MPATH}/lib 

LIBS=-lglib-2.0 \
     -lgstreamer-0.10 \
      -lgobject-2.0 \
     -lgthread-2.0 \
     -lgmodule-2.0 \
     -lxml2 \
     -ldl

PPLIB=-lppbox -lvod -lp2pengine

CXXFLAG= -g -Os -pipe -O2 -Wall -mtune=mips32r2 -mabi=32 -DM3701C -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 --sysroot=${MPATH}/../

all:rec dvbt streaming getdrmxml local miracast
mms: player_server_mms
pp: libpplive_mips.so player_server_pp_mips
local: libplayer_mips.so simple_mips player_server_mips sample_client_mips 
dvbt: libdvbt_mips.so player_server_dvbt_mips sample_client_dvbt_mips simple_dvbt_mips simple_sfu_mips 
online:libplayer_online.so player_server_online client_test simple_online
getdrmxml:libgetdrmxml_mips.so
streaming:libstreaming_mips.so player_server_streaming simple_streaming libgoplayer.so
miracast:libmirror_mips.so player_server_mirror libmiracastplayer.so 
rec : librecorder.so simple_recorder

####  mms  ###
player_server_mms:player_server_mms.cpp alidef.h
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} $< -o $@


###	pplive	###
	
libpplive_mips.so:pplive.h pplive.cpp
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -fPIC -shared pplive.cpp -o $@

player_server_pp_mips:player_server_pp.cpp pplive.h alidef.h
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -L. -lpplive_mips ${PPLIB} player_server_pp.cpp -o $@

### online player ####
libplayer_online.so:online_player.h online_player.cpp
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -fPIC -shared online_player.cpp -o $@

player_server_online:player_server_online.cpp online_player.h alidef.h libplayer_online.so
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -L. -lplayer_online ${PPLIB} player_server_online.cpp -o $@

client_test:client_test.cpp alidef.h client.h
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} $< -o $@

simple_online:simple_online.cpp online_player.h libplayer_online.so
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -L. -lplayer_online simple_online.cpp -o $@

###	streaming	###
libstreaming_mips.so:streaming_player.h streaming_player.cpp
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -fPIC -shared streaming_player.cpp -o $@

libgoplayer.so:goplayer.h goplayer.cpp
	${CXX} ${CXXFLAG} -DGOPLAYER_DBG ${INCLUDE} ${L_PATH} ${LIBS} -lshared -fPIC -shared goplayer.cpp -o $@

player_server_streaming:player_server_streaming.cpp recorder.h streaming_player.h alidef.h libstreaming_mips.so
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -L. -lrecorder -lstreaming_mips player_server_streaming.cpp -o $@

simple_streaming:simple_streaming.cpp streaming_player.h libstreaming_mips.so 
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -L. -lstreaming_mips simple_streaming.cpp -o $@

#simple_streaming:simple_streaming.cpp streaming_player.h libstreaming_mips.so
#	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -L. -lstreaming_mips -lnmpstreambuffer simple_streaming.cpp -o $@

###     getdrmxml      ###
libgetdrmxml_mips.so:get_drm_xml.h get_drm_xml.cpp
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -fPIC -shared get_drm_xml.cpp -o $@

###     mirror         ###
libmirror_mips.so:mirror_player.h mirror_player.cpp
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -fPIC -shared mirror_player.cpp -o $@

player_server_mirror:player_server_mirror.cpp mirror_player.h alidef.h libmirror_mips.so
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -L. -lmirror_mips player_server_mirror.cpp -o $@

libmiracastplayer.so:miracastplayer.h miracastplayer.cpp
	${CXX} ${CXXFLAG} -DMIRACASTPLAYER_DBG ${INCLUDE} ${L_PATH} ${LIBS} -lshared -fPIC -shared miracastplayer.cpp -o $@

###	recorder	###
librecorder.so:recorder.h recorder.cpp
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -fPIC -shared recorder.cpp -o $@

simple_recorder:simple_recorder.cpp recorder.h librecorder.so
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -L. -lrecorder $< -o $@

###	dvbt	###
libdvbt_mips.so:dvbt_player.h dvbt_player.cpp
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -fPIC -shared dvbt_player.cpp -o $@
    
player_server_dvbt_mips:player_server_dvbt.cpp recorder.h dvbt_player.h alidef.h libdvbt_mips.so
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -L. -ldvbt_mips -lrecorder player_server_dvbt.cpp -o $@
    
simple_dvbt_mips:simpledvbt.cpp dvbt_player.h libdvbt_mips.so
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -L. -ldvbt_mips simpledvbt.cpp -o $@

sample_client_dvbt_mips:sample_client_dvbt.cpp alidef.h
	 ${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} sample_client_dvbt.cpp -o $@

simple_sfu_mips:simplesfu.cpp dvbt_player.h libdvbt_mips.so
	 ${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -L. -ldvbt_mips simplesfu.cpp -o $@

###	local_player	###

libplayer_mips.so:local_player.h local_player.cpp
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -fPIC -shared local_player.cpp -o $@

simple_mips:simple.cpp local_player.h libplayer_mips.so
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -L. -lplayer_mips simple.cpp -o $@

player_server_mips:player_server.cpp local_player.h alidef.h libplayer_mips.so
	${CXX} ${CXXFLAG} ${INCLUDE} ${L_PATH} ${LIBS} -L. -lplayer_mips player_server.cpp -o $@

sample_client_mips:sample_client.cpp alidef.h
	${CXX} ${CXXFLAG} sample_client.cpp -o $@

sendcmd_mips:sendcmd.cpp alidef.h
	${CXX} ${CXXFLAG} sendcmd.cpp -o $@

########################
clean_online:
	@rm -f libplayer_online.so player_server_online client_test

clean_streaming:
	@rm -f libstreaming_mips.so player_server_streaming simple_streamingg libgoplayer.so
clean_miracast:
	@rm -f libmirror_mips.so player_server_mirror libmiracastplayer.so
clean_dvbt:
	@rm -f libdvbt_mips.so player_server_dvbt_mips simple_dvbt_mips sample_client_dvbt_mips simple_sfu_mips

clean_recorder:
	@rm -f librecorder.so simple_recorder

clean_pp:
	@rm -f libpplive_mips.so player_server_pp_mips

clean_local:
	@rm -f libplayer_mips.so  simple_mips player_server_mips  sample_client_mips getcmd_mips

clean: clean_pp clean_dvbt clean_local clean_online clean_streaming
	
