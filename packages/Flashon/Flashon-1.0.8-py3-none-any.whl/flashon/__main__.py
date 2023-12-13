import subprocess
import sys
import time
if __name__=='__main__':
    print("Building the current project (.), If error found, please run flashon on the current project ")
    time.sleep(5)
    print('[INFO] Building phase 1 Initiated')
    try:
        subprocess.run(['python','setup.py','setup.cfg','pyproject.toml','sdist','bdist_wheel'])
    except subprocess.CalledProcessError as e:
        print(f'[FLASHON PROCESS ERROR] {e}')
    time.sleep(2)
    print("[INFO] Building phase 2 Initiated")
    try:
        subprocess.run(['python','-m' 'build'])
    except subprocess.CalledProcessError as p:
        print(f'[FLASHON PROCESS ERROR] {e}')
    print("Your project is now built.")
