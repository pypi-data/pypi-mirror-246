import subprocess
import sys
import time
if __name__=='__main__':
    print("Building the current project (.), If error encoutered please run flashon on the current project ")
    time.sleep(5)
    print("[INFO] Building phase 2 Initiated")
    subprocess.run(['python','-m' 'build'])
    print("Your project is now built.")
