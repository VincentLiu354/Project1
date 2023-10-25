# Project 1: Digging in the Dirt
#
# Author: Vincent Liu
# This program finds and displays all of the files in a directory and potentially its subdirectories and performs actions on certain files that 
# have interesting characteristics.
#   

# Importing libraries
from pathlib import Path
import pathlib
import os
import shutil
import time
import datetime
import re

def mainDirectory(path: Path) -> list:
        ''' Puts all the directories in a list and returns it, whilst sorting lexicographically'''
        newDirectory = list(path.iterdir())
        dirs = []
        subDirs = []
        path = []
        for x in newDirectory:
            if(x.is_dir()):
                 subDirs.append(x)
            else:
                 dirs.append(x)

        sorted(dirs)
        sorted(subDirs)
        path.append(dirs)
        path.append(subDirs)
        return path
        
def subDirectory(path: Path) -> list:
        ''' Puts all the directories, including subdirectories in a list and returns it, whilst sorting lexicographically'''
        newDirectory = list(path.iterdir())
        subDirs = []
        dirs = []
        path = []

        for x in newDirectory:
            if(x.is_dir()):
                subDirs.append(subDirectory(x))
            else:
                dirs.append(x)
        
        sorted(subDirs)
        sorted(dirs)
        path.append(dirs)
        path.append(subDirs)
        return path

     
def findExtension(path: Path, extension: str) -> list:
    ''' Appends all the files with the same extension in a list (with or without dot) and returns it'''
    extensionList = []
    for x in path.iterdir():
        if(x.is_dir()):
            extensionList.append(findExtension(x, extension))
        elif(x.suffix == extension or x.suffix[1:] == extension):
            extensionList.append(x) 
        
    return extensionList
   
     
def nameMatch(previousPath: Path, instruction: str) -> list:
    ''' Appends all the files with the exact same name (including extension) in a list and returns it'''
    matchList = []
    for x in previousPath.iterdir():
            if(x.is_dir()):
                matchList.append(nameMatch(x, instruction))
            elif((Path(x).name) == instruction):
                matchList.append(x)

    return matchList
    
def searchText(path: Path, instruction: str) -> list:
    ''' Searches for all files in the path that contains the given text, appends the files into a list and returns it'''
    textList = []
    for x in path.iterdir():
        if(x.is_dir()):
             textList.append(searchText(x, instruction))
        else:
            try:
                with open(x, 'r') as readFile:
                  file_contents = readFile.read()
                  match = re.search(instruction, file_contents)
                  if(match is not None):
                       textList.append(x)
            except:
                 pass
            
    return textList
                     
def searchBytes(path: Path, instruction: int) -> list:
    ''' Retrieves the bytes in each file and if its larger than the user input, the function appends the file into a list and returns it'''
    bytesList = []
    for x in path.iterdir():
        if(x.is_dir()):
            bytesList.append(searchBytes(x, instruction))
        file_stats = x.stat()
        if(file_stats.st_size > int(instruction)):
            bytesList.append(x)

    return bytesList

def searchBytes2(path: Path, instruction: int) -> list:
    ''' Retrieves the bytes in each file and if its smaller than the user input, the function appends the file into a list and returns it'''
    bytesList2 = []
    for x in path.iterdir():
        if(x.is_dir()):
            bytesList2.append(searchBytes2(x, instruction))
        file_stats = x.stat()
        if(file_stats.st_size < int(instruction)):
            bytesList2.append(x)

    return bytesList2

def printLine(previousPath: list) -> None:
    ''' Prints the first line of each interesting file'''
    for file in previousPath:
        if(type(file) == list):
            printLine(file)
        elif(file.is_dir()):
              print('NOT TEXT')
        else:
              try:
                f = open(file, 'r')
                first = f.readline()
                print(first, end='')
              except:
                   print('NOT TEXT')
               
def makeDup(previousPath: list) -> None:
    ''' Makes duplicate files for the previous interesting files, adding a ".dup" as a suffix'''
    for file in previousPath:
          if(type(file) == list):
               makeDup(file)
          else:
               shutil.copy(file, f'{file}.dup')

def touch(previousPath: list) -> None:
     ''' Modifies the last modified timestamp of the previous interesting files to the current time and date'''
     for file in previousPath:
          if(type(file) == list):
               touch(file)
          else:
               os.utime(file, None)

def printPaths(path: list) -> None:
    ''' Prints out the lists from the functions into the correct syntax'''
    for x in path:
        if(type(x) == list):
            printPaths(x)
        else:
            print(x)
       
def run() -> None:
    ''' Runs all the functions in order'''
    userInput = input()
    path = Path(userInput[2:]) 
    previousPath = []        

    if(userInput.startswith('D')):
            mainDirectory(path)
            printPaths(mainDirectory(path))
    elif(userInput.startswith('R')):
            subDirectory(path)
            printPaths(subDirectory(path))
    else:
         print('ERROR')
         run()
  
    def subRun() -> None:
        ''' Narrows the files into the interesting ones based on user input'''
        userInput2 = input()
        instruction = userInput2[2:]    
   
        if(userInput2 == ('A')):
            if(userInput.startswith('D')):
                printPaths(mainDirectory(path))
                previousPath.append(mainDirectory(path))   
            elif(userInput.startswith('R')):
                printPaths(subDirectory(path))
                previousPath.append(subDirectory(path))   

        elif(userInput2.startswith('N')):
                if(userInput2 == 'N'):
                    print('ERROR')
                    subRun()
                nameMatch(path, instruction)
                printPaths(nameMatch(path, instruction))
                previousPath.append(nameMatch(path, instruction))
        elif(userInput2.startswith('E')):
                extension = userInput2.split(' ')[-1]
                findExtension(path, extension)
                printPaths(findExtension(path, extension))
                previousPath.append(findExtension(path, extension))
        elif(userInput2.startswith('T')):
                searchText(path, instruction)
                printPaths(searchText(path, instruction))
                previousPath.append(searchText(path, instruction))
        elif(userInput2.startswith('>')):
                searchBytes(path, instruction)
                printPaths(searchBytes(path, instruction))
                previousPath.append(searchBytes(path, instruction))
        elif(userInput2.startswith('<')):
                searchBytes2(path, instruction)
                printPaths(searchBytes2(path, instruction))
                previousPath.append(searchBytes2(path, instruction))
        else:
            print('ERROR')
            subRun()
              
    subRun()   

    def actionRun() -> None:
        ''' Performs actions on the interesting files based on user input'''
        userInput3 = input()
        if(userInput3 == ('F')):
                printLine(previousPath)
        elif(userInput3 == ('D')):
                makeDup(previousPath)
        elif(userInput3 == ('T')):
                touch(previousPath)
        else:
             print('ERROR')
             actionRun()
                
    actionRun()
  
if __name__ == '__main__':
    ''' Only executes when the program is runned'''
    ''' Thus importing won't affect other modules'''
    run()





















