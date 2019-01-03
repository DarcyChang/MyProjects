# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
#export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias ll='ls -alF --color=auto'
alias la='ls -A --color=auto'
alias l='ls -CF --color=auto'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

# Darcy's some setting
alias vi='vim'

# Darcy's some symbol link
alias 192='ssh 10.5.100.192' # Intel EasyConnect CAP1
alias 193='ssh 10.5.100.193' # Intel EasyConnect CAP1 advantage and CAP2 (Ubuntu 14.04 LTS 64 bit)
alias 199='ssh 10.5.100.199' # VMware ubuntu 14.04.1 LTS x86_64, Boke, DropAP
alias 209='ssh autobuild@10.5.100.209' # VMware ubuntu 14.04.3 LTS x86_64, Autobuild Server. password gemtek1234
alias macmini='ssh gemtek@10.5.182.181' # Mac mini, password is "gemtek12345"
alias macmpro='ssh darcy@10.70.51.30' # Macbook pro"

# Serial port
alias usb0_57600='cu -l /dev/ttyUSB0 -s 57600'
alias usb0_115200='cu -l /dev/ttyUSB0 -s 115200'
alias usb1_9600='cu -l /dev/ttyUSB1 -s 9600'
alias usb1_57600='cu -l /dev/ttyUSB1 -s 57600'
alias usb1_115200='cu -l /dev/ttyUSB1 -s 115200'
alias usb2_57600='cu -l /dev/ttyUSB2 -s 57600'
alias usb2_115200='cu -l /dev/ttyUSB2 -s 115200'

# Bitcasa
#alias bitcasa_mount='sudo mount.bitcasa cychang0916@gmail.com /home/darcy/Bitcasa/ -o password=Cychang0'
#alias bitcasa_remount='sudo umount Bitcasa ; sudo mount.bitcasa cychang0916@gmail.com /home/darcy/Bitcasa/ -o password=Cychang0'

# More detail please see following link:                                                                                                          
# http://xta.github.io/HalloweenBash/

function parse_git_branch {
	git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}
export PS1="\[\e[0;42m\]\u@\h:\w\$(parse_git_branch)\\$ \[\e[0m\]"

# Android studio
username=$(users | awk '{print $1}')
export ANDROID_HOME=/home/$username/Android/Sdk
export PATH=~/bin:/home/$username/Android/sdk/platform-tools:$ANDROID_HOME/tools:$ANT_HOME/bin:$PATH
export PATH=${PATH}:/home/$username/Android/Sdk/tools
export PATH=${PATH}:/home/$username/Android/Sdk/tools/bin/
export PATH=${PATH}:/home/$username/Android/Sdk/platform-tools

# Java
#export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
export JAVA_HOME=/usr/lib/jvm/java-8-oracle
export PATH=$JAVA_HOME/bin:$PATH

# Pycharm
export PATH=${PATH}:/home/$username/Tools/pycharm-community-2017.2.3/bin/

# history command
xport HISTTIMEFORMAT="%d/%m/%y %T "

# tar and untar
# tar -czvf file.tar.gz files # tar gz
# tar -xzvf file.tar.gz # untar gz
# tar -C /tmp/dir -zvxf file.tar.gz
# tar -xjvf file.tar.gz # untar bzip2
# tar -Jxvf file.tar.gz # untar tar.xz
# unzip file.zip -d /tmp/dir # untar zip
