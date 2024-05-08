#!/bin/bash
# wrap1.sh
# needs to  chmod +x wrapper.sh, or else it doesnt excecute
trap "exit" INT TERM ERR
trap "kill 0" EXIT

echo "Starting wind wall in 5 seconds." 
echo "Please keep a safe distance!" 
sleep 1s
echo "4"
sleep 1s
echo "3"
sleep 1s
echo "2"
sleep 1s
echo "1"

python /home/deck/Downloads/windshape_api/example_read_rpm.py &

wait
