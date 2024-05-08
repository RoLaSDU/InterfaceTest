#!/bin/bash
# wrap1.sh
# needs to  chmod +x wrapper.sh, or else it doesnt excecute
trap "exit" INT TERM ERR
trap "kill 0" EXIT

source $(echo $EIT_DIR)/install/setup.bash &
source $(echo $EIT_DIR)/src/eit-playground/setup_gazebo.bash &
ros2 launch vrpn_mocap client.launch.yaml server:=192.168.16.50 prt:=3883

wait
