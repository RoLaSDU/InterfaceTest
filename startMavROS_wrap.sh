#!/bin/bash
# wrap1.sh
# needs to  chmod +x wrapper.sh, or else it doesnt excecute
trap "exit" INT TERM ERR
trap "kill 0" EXIT

source $(echo $EIT_DIR)/install/setup.bash &
source $(echo $EIT_DIR)/src/eit-playground/setup_gazebo.bash &
ros2 run mavros mavros_node --ros-args --param fcu_url:=udp://:14540@127.0.0.1:14557 --param plugin_denylist:="[odometry]"

wait
