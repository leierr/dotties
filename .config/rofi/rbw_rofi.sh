#!/bin/bash
rbw unlock
passphrase=$(rbw list | rofi -dmenu -i -config ~/.config/rofi/rbw.rasi | xargs -I{} rbw get "{}")
[[ -n "$passphrase" ]] && echo -n $passphrase | xclip -selection c -i
unset passphrase
