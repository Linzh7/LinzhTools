###############################################################################
##
# Manual of Linzh's Util
##
# 1. Use '/' instead of '\\' in path stringf or rewrite some functions.
##
##
###############################################################################

# Divide Dataset
# from sklearn.model_selection import train_test_split
# x_train,x_test, y_train, y_test = train_test_split(train_data,train_target,test_size=0.3, random_state=0)

import os
from pathlib import Path
import shutil


def movePairFile(src1, src2, dst):
    fileList1 = getFileList(src1)
    fileList2 = getFileList(src2)
    fileList1.sort()
    fileList2.sort()
    i = 0
    j = 0
    while(i < len(fileList1) or j < len(fileList2)):
        name1 = fileList1[i].split('.')[0]
        name2 = fileList2[j].split('.')[0]
        if name1 == name2:
            shutil.move(f'{os.path.join(src1, fileList1[i])}', f'{os.path.join(dst, fileList1[i])}')
            shutil.move(f'{os.path.join(src2, fileList2[j])}', f'{os.path.join(dst, fileList2[j])}')
            i += 1
            j += 1
        elif name1 < name2:
            i += 1
        else:
            j += 1


def removeFile(path, pattern):
    for i in Path(path).rglob(pattern):
        print(f'[LinzhUtil] Removing {i}...')
        os.remove(i)


def moveFileTo(src, dst, fileNamePattern):
    for i in Path(src).rglob(fileNamePattern):
        fileName = str(i).split('\\')[-1]
        print(f'[LinzhUtil] Moving {i}...')
        shutil.move(i, f'{os.path.join(dst, fileName)}')


def moveFileTo_DEBUG(src, dst, fileNamePattern):
    for i in Path(src).rglob(fileNamePattern):
        fileName = str(i).split('\\')[-1]
        print(f'[LinzhUtil] Moving {i}...')
        shutil.move(i, f'{os.path.join(dst, fileName)}')
        break


def copyFileTo(src, dst, fileNamePattern):
    for i in Path(src).rglob(fileNamePattern):
        fileName = str(i).split('\\')[-1]
        print(f'[LinzhUtil] Copying {i}...')
        shutil.copyfile(i, f'{os.path.join(dst, fileName)}')


def copyFileTo_DEBUG(src, dst, fileNamePattern):
    for i in Path(src).rglob(fileNamePattern):
        fileName = str(i).split('\\')[-1]
        print(f'[LinzhUtil] Copying {i}...')
        shutil.copyfile(i, f'{os.path.join(dst, fileName)}')
        break


def printNotInstance(ls, type):
    for i in ls:
        if not isinstance(i, type):
            try:
                type(i)
            except Exception as e:
                print("Error: {}".format(e))


def filesRename(folderPath, addName):
    fileList = getFileList(folderPath)
    for fileName in fileList:
        os.rename(folderPath+fileName, folderPath+addName+fileName)


def getFileList(path):
    for a, b, file in os.walk(path):
        return file


def getFolderList(path):
    for a, folder, c in os.walk(path):
        return folder


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def MoveDoneFiles(FOLDER_PATH):
    fileList = getFileList(FOLDER_PATH)
    fileList.sort()
    for fileName in fileList:
        fileNameWithout = fileName.split('.')[0]
        if(os.path.exists(FOLDER_PATH+fileNameWithout+'.xml') and os.path.exists(FOLDER_PATH+fileNameWithout+'.xml')):
            os.system('mv {0}{1} {0}done/'.format(FOLDER_PATH, fileNameWithout + '.xml'))
            os.system('mv {0}{1} {0}done/'.format(FOLDER_PATH, fileNameWithout + '.jpg'))
            print('{0} moved.'.format(fileNameWithout))
    print('All moved.')
