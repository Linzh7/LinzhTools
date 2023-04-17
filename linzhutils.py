import os
from pathlib import Path
import shutil
from tqdm import tqdm

def isFolderEmpty(folderPath):
    return len(os.listdir(folderPath)) == 0

def checkDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def movePairFile(src1, src2, dst1, dst2=None):
    if dst2 == None:
        dst2 = dst1
    fileList1 = getFileList(src1)
    fileList2 = getFileList(src2)
    fileList1.sort()
    fileList2.sort()
    i = 0
    j = 0
    while (i < len(fileList1) or j < len(fileList2)):
        name1 = fileList1[i].split('.')[0]
        name2 = fileList2[j].split('.')[0]
        if name1 == name2:
            shutil.move(f'{os.path.join(src1, fileList1[i])}',
                        f'{os.path.join(dst1, fileList1[i])}')
            shutil.move(f'{os.path.join(src2, fileList2[j])}',
                        f'{os.path.join(dst2, fileList2[j])}')
            i += 1
            j += 1
        elif name1 < name2:
            i += 1
        else:
            j += 1


def removeFile(path, pattern):
    fileList = Path(path).rglob(pattern)
    for i in tqdm(fileList):
        print(f'[LinzhUtil] Removing {i}...')
        os.remove(i)


def moveFileTo(src, dst, fileNamePattern):
    if not isFolderEmpty(dst):
        confirm = input(f"WARNING: {dst} is not empty. Do you want to proceed? (y/n) ")
        if confirm.lower() != 'y':
            print("Aborting move operation")
            return
    checkDir(dst)
    fileList = getFileListFromPattern(src)
    fileCount = len(list(fileList))
    if fileCount == 0:
        print(f"No files found in {src} that match pattern {fileNamePattern}")
        return
    print(f"Found {fileCount} files in {src} that match pattern {fileNamePattern}")
    for i in tqdm(list(fileList)):
        fileName = str(i).split('/')[-1]
        shutil.move(i, f'{os.path.join(dst, fileName)}')


def moveFileTo(src, dst, fileNamePattern):
    if not isFolderEmpty(dst):
        confirm = input(f"WARNING: {dst} is not empty. Do you want to proceed? (y/n) ")
        if confirm.lower() != 'y':
            print("Aborting move operation")
            return
    checkDir(dst)
    fileList = getFileListFromPattern(src)
    fileCount = len(list(fileList))
    if fileCount == 0:
        print(f"No files found in {src} that match pattern {fileNamePattern}")
        return
    print(f"Found {fileCount} files in {src} that match pattern {fileNamePattern}")
    for i in tqdm(list(fileList)):
        fileName = str(i).split('/')[-1]
        shutil.move(i, f'{os.path.join(dst, fileName)}')

def getFileListFromPattern(path, pattern):
    return Path(path).rglob(pattern)

def printNotInstance(ls, type):
    for i in ls:
        if not isinstance(i, type):
            try:
                type(i)
            except Exception as e:
                print("Error: {}".format(e))


def filesRename(folderPath, addName):
    fileList = getFileList(folderPath)
    for fileName in tqdm(fileList):
        os.rename(folderPath + fileName, folderPath + addName + fileName)


def getFileList(path):
    files = os.listdir(path)
    filtered_files = [f for f in files if not f.startswith('.')]
    return filtered_files


def getAllFileList(path):
    ls = []
    for root, dirs, files in os.walk(path):
        for file in files:
            ls.append(os.path.join(root, file))
    return ls


def getFolderList(path):
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]


def getFileContent(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


