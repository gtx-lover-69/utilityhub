import os
import time
import subprocess
import sys

old_file = sys.argv[1]
new_file = sys.argv[2]

time.sleep(2)

while True:
    try:
        os.remove(old_file)
        break
    except:
        time.sleep(1)

os.rename(new_file, old_file)

subprocess.Popen([old_file])