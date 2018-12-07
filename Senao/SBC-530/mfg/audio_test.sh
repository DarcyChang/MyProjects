#!/bin/bash

DEV=$(sshpass -p senao ssh senao@localhost PULSE_RUNTIME_PATH=/run/user/1000/pulse/ pacmd list-cards | grep analog-input  | cut -d: -f1 | grep $1 | awk '{print $1}')

DEV1=$(echo $DEV | grep "analog-input-rear-mic")

if [ -n "$DEV1" ]; then
    DEV="analog-input-rear-mic"
fi

if [ -n "$1" ]; then
    sshpass -p senao ssh senao@localhost PULSE_RUNTIME_PATH=/run/user/1000/pulse/ pacmd set-source-port 1 $DEV
else
    echo "usage: $0 [line|mic] <threshold>"
    exit 1
fi

threshold=-20
if [ ! -z "$2" ]; then
    threshold=$2
fi

#set output volume
Output_NAME=$(sshpass -p senao ssh senao@localhost PULSE_RUNTIME_PATH=/run/user/1000/pulse/ pacmd list-sinks | grep name: | cut -d'<' -f2 | sed 's/.$//')
sshpass -p senao ssh senao@localhost PULSE_RUNTIME_PATH=/run/user/1000/pulse/ pacmd set-sink-volume $Output_NAME 0x10000

#set input volume
Input_NAME=$(sshpass -p senao ssh senao@localhost PULSE_RUNTIME_PATH=/run/user/1000/pulse/ pacmd list-sources | grep alsa_input | cut -d'<' -f2 | sed 's/.$//')
sshpass -p senao ssh senao@localhost PULSE_RUNTIME_PATH=/run/user/1000/pulse/ pacmd set-source-volume $Input_NAME 0x1000

wav_file=test_$1.wav
aplay sound/piano2.wav &
arecord -D hw:0,0 sound/$wav_file -f S16_LE -r 44100 -c 2 -d 6
cd sound && rm -f collection.musly && musly -N > /dev/null && musly -x wav -a ./ > /dev/null
val=$(musly -d | grep .//$wav_file -A3 | grep gaussian.covar_logdet: | cut -d' ' -f2)
result=$(echo "$val > $threshold" | bc)
if [ "$result" = "1" ]; then
    echo "Test Pass"
else
    echo "Test Fail"
fi
rm -f $wav_file
