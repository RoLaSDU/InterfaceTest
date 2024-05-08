# wrapper.py
import os
import subprocess
import sys

if __name__ == "__main__":
    os.setpgrp()  # Create new process group, become its leader
    command = sys.argv[1:]
    subprocess.run(command)
