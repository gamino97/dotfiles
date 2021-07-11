#!/usr/bin/env bash

/home/gamino/bashscripts/toggle_monitors.sh
feh --recursive --randomize --bg-fill ~/Imágenes/Wallpapers/ &
compton &
/usr/bin/gnome-keyring-daemon --start --components=ssh &
# nitrogen --restore &
/usr/bin/emacs --daemon &
nm-applet &
