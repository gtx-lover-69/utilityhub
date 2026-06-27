import os
from colorama import *
from colorama.ansi import clear_screen
from tqdm import tqdm
import time
import sys
from sys import exit
import subprocess
import requests
import hashlib


def get_file_hash(file_obj):
    sha256_hash = hashlib.sha256()
    for chunk in iter(lambda: file_obj.read(4096), b""):
        sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def get_original_directory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def compare(raw_url, local_file_path):
    try:
        response = requests.get(raw_url, stream=True)
        response.raise_for_status()
        remote_hash = hashlib.sha256(response.content).hexdigest()

        with open(local_file_path, 'rb') as f:
            local_hash = get_file_hash(f)

        if remote_hash == local_hash:
            return True
        else:
            return False

    except Exception as e:
        print(f"Error during comparison: {e}")
        time.sleep(10)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching remote file: {e}")
        return None

clear_screen()
print("Initializing. Sit tight!")

def count_files(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
       count += len(files)
    return count

total = count_files('C:/Users/')

def download(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        filename = url.split('/')[-1]

        with open(filename, 'wb') as f:
            f.write(response.content)

        return filename

    except requests.RequestException as e:
        print(f"Failed to download: {e}")
        return None

def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

def find(name, path, state):
    clear_screen()

    iterator = os.walk(path)

    if state == "normal":
        iterator = tqdm(iterator, desc="Searching...", colour="blue", ascii="―━")

    for root, dirs, files in iterator:
        if name in files:
            full_path = os.path.join(root, name)

            try:
                with open(full_path, "rb"):
                    pass
                return full_path
            except PermissionError:
                continue

    return None

def main():
    print("Welcome to Matteo's Utility Suite!")
    selection = input("""    1. FileTool
    2. Music Tool
    3. Img2ASCII
    U. Check for updates
    0. Exit
    """)

    if selection.strip() == "1":
        result = find('filetool.exe', 'C:\\Users\\', 'normal')

        if result:
            clear_screen()
            print("Found! " + Style.DIM + result + Style.RESET_ALL)
            time.sleep(0.5)
            os.startfile(result)
            exit()

        else:
            clear_screen()
            getFileChoice = input("File not found. Press any key to download it.")
            if getFileChoice or getFileChoice == '':
                print("Downloading from GitHub...")
                filename = download('https://raw.githubusercontent.com/gtx-lover-69/Matteo-CLI-FileTool/main/filetool.exe')

                if filename:
                    time.sleep(0.5)
                    os.startfile(filename)
                    exit(0)

    elif selection.strip() == "2":
        result = find('musictool.exe', 'C:\\Users\\','normal')
        if result:
            clear_screen()
            print("Found! " + Style.DIM + result + Style.RESET_ALL)
            time.sleep(0.5)
            os.startfile(result)
            exit()
        else:
            clear_screen()
            getFileChoice = input("File not found. Press any key to download it.")
            if getFileChoice or getFileChoice == '':
                print("Downloading from GitHub...")
                filename = download('https://raw.githubusercontent.com/gtx-lover-69/Matteo-CLI-MusicTool/main/musictool.exe')

                if filename:
                    time.sleep(0.5)
                    os.startfile(filename)

    elif selection.strip() == "3":
        result = find('img2ascii.exe', 'C:\\Users\\','normal')
        if result:
            clear_screen()
            print("Found! " + Style.DIM + result + Style.RESET_ALL)
            time.sleep(0.5)
            os.startfile(result)
            exit()

        else:
            clear_screen()
            getFileChoice = input("File not found. Press any key to download it.")
            if getFileChoice or getFileChoice == '':
                print("Downloading from GitHub...")
                filename = download('https://raw.githubusercontent.com/gtx-lover-69/img2ascii/main/dist/converter.exe')

                if filename:
                    time.sleep(0.5)
                    os.startfile(filename)
                    exit()

    elif selection.strip().upper() == "U":
        result = find('updater.exe', 'C:\\Users\\','quiet')
        if not result:
            print("Downloading updater...")
            download('https://raw.githubusercontent.com/gtx-lover-69/utilityhub/main/dist/updater.exe')


        print("Checking for updates...")
        local_file = os.path.join(get_original_directory(), "main.exe")

        check = compare("https://raw.githubusercontent.com/gtx-lover-69/utilityhub/main/dist/main.exe",local_file)

        if check is True:
            print("No updates found.")
            time.sleep(1)


        elif check is False:
                print("Update found. Downloading... ")
                update_file = os.path.join(get_original_directory(),"main_new.exe")

                response = requests.get("https://raw.githubusercontent.com/gtx-lover-69/utilityhub/main/dist/main.exe",timeout=30)
                response.raise_for_status()

                with open(update_file, "wb") as f:
                    f.write(response.content)

                subprocess.Popen([
                    os.path.join(get_original_directory(), "updater.exe"),
                    local_file,
                    update_file
                ])

        else:
            print("Failed to check for updates.")
            time.sleep(2)

    elif selection.strip() == "0":
        exit()

    else:
        print("Invalid selection. Please try again.")
        time.sleep(1)
        clear_screen()


if __name__ == '__main__':
    clear_screen()
    main()
