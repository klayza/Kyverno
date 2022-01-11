import urllib.request
import requests
from bs4 import BeautifulSoup
from download import download
import os
from pathlib import Path

# Given an Apache open directory, the user is able to navigate and download folders recursively

Directory = "http://103.152.18.18/Data/English/hollywood/2021/"

def GetFolders(directory):
    folders = []
    r = requests.get(directory)
    raw_folders = BeautifulSoup(r.content, "html.parser").get_text().strip().split("\r\n")
    for folder in raw_folders:
        temp = ""
        for letter in folder:
            if letter == "/":
                break
            temp += letter
        folders.append(temp)
    del folders[0]

    return folders


def URLtoPath(link):
    count = 0
    path = ""
    for letter in link:
        if count == 3:
            path += letter
        elif letter == "/":
            count += 1
    return path


# Goes up a directory (Assumes there is no / at the end of the string)
def PathAscend(path):
    new_path = ""
    slashfound = False
    for i in range(len(path) - 1, -1, -1):
        if path[i] == "/" and not slashfound:
            slashfound = True
            continue
        if slashfound:
            new_path += path[i]
    return new_path[::-1]


def Help():
    print("Use commands: 'help', 'cd', 'dir', 'dl'")


def Cd(path):
    pass


# Replaces spaces with %20
def URLify(url):
    return url.replace(' ', '%20')


def Main():
    dir = input("Enter a directory URL: ")
    if dir[-1] == "/":
        index = dir.rfind("/")
        if len(dir) > index:
            dir = dir[0 : index : ] + dir[index + 1 : :]

    r = requests.get(dir)
    if r.status_code != 200:
        Main()

    print("Connected to " + dir)
    Help()

    while True:
        command = input("\n" + URLtoPath(dir) + "> ")

        # Dir
        if command == "dir" or command == "ls":
            for folder in GetFolders(dir):
                print(folder)
        
        # Help
        elif command == "help":
            Help()

        # Cd
        elif "cd" in command:
            # Goes back a folder
            if ".." in command:
                dir = PathAscend(dir)               # Need to fix cd .. in root
                continue

            path = dir + "/" + command[3:] 
            r = requests.get(path)

            if r.status_code != 200:
                print("Cannot find the path specified | " + "Code " + str(r.status_code))
                continue
            else:
                dir = path

        # Dl
        elif "dl" in command:
            # Target is set to current dir
            if command == "dl":
                response = input("Would you like to download all of the contents of this folder?").upper()
                if "Y" in response:
                    pass                            # Download recursively TODO
                else:
                    continue

            # Target is defined
            else:
                target = command[3:]
                # If user wants to download a single file
                if "." in target:
                    print(dir + "/" + target)
                    try:
                        downloads_path = str(Path.home() / "Downloads") + "/" + target
                        url = URLify(dir + "/" + target)
                        path = download(url, downloads_path)               # Need fix, and needs to be in try, except
                    except:
                        print("That file wasn't found")
                # If user wants to download a target folder 
                else:
                    pass                        # Recursive download TODO


#downloads_path = str(Path.home() / "Downloads") + "/"
#print(download("http://103.152.18.18/Data/English/hollywood/2021/Wolf%20(2021)/YIFYStatus.com.txt", downloads_path + "YIFYStatus.com.txt"))
#exit()

Main()
input()
