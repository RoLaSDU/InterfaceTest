#!/bin/bash
# wrap1.sh
# needs to  chmod +x wrapper.sh, or else it doesnt excecute
trap "exit" INT TERM ERR
trap "kill 0" EXIT

source $(echo $EIT_DIR)/install/setup.bash 
source $(echo $EIT_DIR)/src/eit-playground/setup_gazebo.bash 

export PX4_HOME_LAT=55.4719762 
export PX4_HOME_LON=10.3248095 
export PX4_HOME_ALT=7.4000000 

ros2 launch eit_playground posix.py vehicle:=sdu_drone_mono_cam_downward world:=~/eit_ros2_ws/src/eit-playground/worlds/hca_airport.world &

wait
