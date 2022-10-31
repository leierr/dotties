#!/bin/bash

# ] ---- FUNCTIONS ---- [

function startus () {
	pgrep -x $1 > /dev/null || $1 &
}

function divide_workspaces () {
	desktops=(1 2 3 4 5 6 7 8 9 0)
	readarray -t monitor_list < <(bspc query -M)
	declare -A monitor_desktops

	for ((m=0;m<${#monitor_list[@]};m++)); do
		for ((d=$m; d<${#desktops[@]}; d+=${#monitor_list[@]})); do
			monitor_desktops[${monitor_list[$m]}]+=" ${desktops[d]}"
		done
		bspc monitor ${monitor_list[$m]} -d ${monitor_desktops[${monitor_list[$m]}]}
	done
	unset {desktops,monitor_list,monitor_desktops}
}

function startus_polybar () {
	# Terminate already running bar instances
	killall -q polybar

	# Wait until the processes have been shut down
	while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done

	if type "xrandr"; then
	  for m in $(xrandr --query | grep " connected" | cut -d" " -f1); do
	    MONITOR=$m polybar --reload main &
	  done
	else
	  polybar --reload main &
	fi
}
