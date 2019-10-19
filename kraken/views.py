from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from os import listdir
import os, sys
from os.path import isfile, join
import time, math, json

from kraken.forms import DirectoryForm

# Create your views here.

prefix = "\\\sydsrv01\\projects\\"

def table_errmessage(message, filepaths, outObject):
    outObject["filepaths"] = filepaths
    outObject["errmessage"] = message
    return outObject

def table_getFileType(file):
    filetype = file.split(".")[-1]
    # print(filetype)

    return filetype

def table_splitDirectory(directories, listToAppend):
    paths = directories.split(",")
    allpaths = [x for x in paths if x]
    for i in allpaths:
        table_makeFilepathObj(i, listToAppend)
        
    return listToAppend

def table_getFilenames(pathobj, appendList):
    print("RUNNING getFilenames")
    try:
        try:
            print(pathobj)
            # Remove unnecessary spaces before/after the file name
            folder = pathobj["filepath"].strip()
        except:
            folder = pathobj
            print("---------------")
            print(pathobj)
        
        filelist = []

        ## BRING THIS BACK
        # onlyfiles = [filelist.append(f) for f in listdir(folder) if isfile(join(folder, f))]

        getfiles = [appendList.append(table_getFileData(f, folder)) for f in listdir(folder) if isfile(join(folder, f))]

        return appendList

    except Exception as e:
        print("-----------ERROR-----------")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        print("---------------------------")
        return [str(e)]

def table_getFileData(file, folder):

    fileObj = {}

    fileObj["filename"] = file.replace(" ", "&nbsp;")
    fileObj["filepath"] = folder
    fileObj["created"] = time.ctime(os.path.getctime(folder + "/" + file))
    fileObj["lastModified"] = time.ctime(os.path.getmtime(folder + "/" + file))
    fileObj["fileType"] = table_getFileType(file)

    fileObj["fileSize"] = '{:,.0f}'.format(os.path.getsize(folder + "/" + file)/float(1<<10))+" KB"

    return fileObj

def table_makeFilepathObj(path, listToAppend):
    pathObj = {}

    try:
        x = path.replace("\r\n", "")
        x = x.replace("K:", prefix)

        pathObj["filepath"] = x

        # listdir(pathObj["filepath"])

        pathObj["error"] = "All Good"

        testList = []


        testfiles = [testList.append(f) for f in listdir(pathObj["filepath"]) if isfile(join(pathObj["filepath"], f))]

        if testList == []:
            pathObj["empty"] = "true"
        else:
            pathObj["empty"] = "false"
    except:
        pathObj["error"] = "SORRY, there's a problem with at least ONE of the input directories"
        pathObj["empty"] = "false"

    listToAppend.append(pathObj)

    return listToAppend

def table_runMultipleDirectories(directory, filepaths, files):
    table_splitDirectory(directory, filepaths)

    print("---------FILEPATHS------------")
    print(filepaths)

    for path in filepaths:
        table_getFilenames(path, files)

    return files

def table_runSingleDirectory(directory, filepaths, files):

    print("---------FILEPATHS------------")
    print(filepaths)

    try:
        folder = directory.replace("K:", prefix)
        table_makeFilepathObj(folder, filepaths)
    except:
        folder = prefix
        table_makeFilepathObj(folder, filepaths)
    for path in filepaths:
        table_getFilenames(path, files)

    return files

########################################################################################

def kraken_app(request):
    log = []
    print("KRAKEN")
    # If the form is submitted i.e. POST request
    if request.method == 'POST' and 'visualiser' in request.POST:
        print("POSTED")
        # Set our form to DirectoryForm
        # This will populate our directory form with whatever the user tried to submit
        dirForm = DirectoryForm(request.POST)
        
        # Checks that the form is valid
        if dirForm.is_valid():

            # Retrieve the input data from user form and clean it up
            directory = dirForm.cleaned_data['directory'].strip()
            
            # Response output
            out = {}

            # Filenames
            files = []

            # Folder directories
            filepaths = []

            try:
                
                # MULTIPLE DIRECTORIES ------------------------------------------------
                # If there's a comma in the list of directories
                if "," in directory:
                    # -------------------------------------
                    try:

                        table_runMultipleDirectories(directory, filepaths, files)

                    except Exception as e: 

                        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

                # SINGLE DIRECTORIES ------------------------------------------------
                else:
                    # try:
                    log.append(json.dumps(filepaths))
                    table_runSingleDirectory(directory, filepaths, files)

                # OUTPUT TO USER

                try:
                    # print("FILEPATH: " + json.dumps(filepaths))
                    out["filepaths"] = filepaths
                    # files.sort()
                    out["log"] = log
                    out["files"] = files

                    # out["fileobj"] = fileobjlist
                    print(json.dumps(out,indent=4, sort_keys=True))
                except Exception as e: 
                    print("3------------------------------")
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

                return render(request, "kraken/table.html", {"out": out})
            except:
                return render(request, "kraken/table.html", {"out": out})

    else:
        # The form we created in forms.py
        dirForm = DirectoryForm()

    # What is seen by the user - form and template of the form
    return render(request, "kraken/form.html", {"form": dirForm})