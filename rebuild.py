#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Author: lonewolf
# Date: 2013-11-11 23:08:52
# 
import os
import re
import codecs
try:
    import helper
except ImportError:
    from . import helper

snippetTemplate = """<snippet>
    <content><![CDATA[$content]]></content>
    <tabTrigger>$trigger</tabTrigger>
    <scope>source.lua</scope>
    <description>$desc</description>
</snippet>
"""

# user definition path: user_definition.json
USER_DEFINITIONS=[]
# auto completions path: SAVE_DIR/md5(filePath)/...
SAVE_DIR=""

def rebuild(dir,saveDir):
    global USER_DEFINITIONS
    global SAVE_DIR
    USER_DEFINITIONS=[]
    SAVE_DIR=saveDir
    # delete files first
    deleteFiles(saveDir,saveDir)
    parseDir(dir)
    return USER_DEFINITIONS

def rebuildSingle(file,saveDir):	
    global USER_DEFINITIONS
    global SAVE_DIR
    USER_DEFINITIONS=[]
    SAVE_DIR=saveDir
    parseLua(file)
    return [USER_DEFINITIONS,file]

def parseDir(dir):
    for item in os.listdir(dir):
        path=os.path.join(dir,item)
        if os.path.isdir(path):
            parseDir(path)
        elif os.path.isfile(path):
            if helper.checkFileExt(path,"lua"):
                parseLua(path)

def parseLua(file):
    # remove all file
    md5filename=helper.md5(file)
    saveDir=os.path.join(SAVE_DIR,md5filename)
    deleteFiles(saveDir,saveDir)
    # create dir
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    # add filepath to filepath.txt for debug
    filepath=os.path.join(saveDir,"filepath.txt")
    helper.writeFile(filepath,file)
    completionsList=[]
    f=codecs.open(file,"r","utf-8")
    lineNum=0
    while True:
        line=f.readline()
        if line:
            lineNum+=1
            # class
            m=re.match("^local\s+(\w+)\s*=\s*\{\}",line)
            if m:
                completionsList.append(m.group(1))
                handleDefinition(m.group(1),None,file,lineNum)
                continue
            m=re.match("^local\s+(\w+)\s*=\s*class\(",line)
            if m:
                completionsList.append(m.group(1))
                handleDefinition(m.group(1),None,file,lineNum)
                continue
            m=re.match("^(\w+)\s*=\s*class\(",line)
            if m:
                completionsList.append(m.group(1))
                handleDefinition(m.group(1),None,file,lineNum)
                continue
            # function
            m=re.match("^function\s+(\w+\.*\w*)\s*\((.*)\)",line)
            if m:
                saveFunction(saveDir,"",m.group(1),m.group(2))
                handleDefinition(m.group(1),m.group(2),file,lineNum)
                continue
            # class function
            m=re.match("^function\s+(\w+)\:(\w+)\s*\((.*)\)",line)
            if m:
                method=m.group(2)
                if method=="ctor":
                    continue
                saveFunction(saveDir,m.group(1),method,m.group(3))
                handleDefinition(m.group(2),m.group(3),file,lineNum,m.group(1)+":"+m.group(2))
                continue
            # local property
            m=re.match("^\s*local\s+(\w+)\s*",line)
            if m:
                completionsList.append(m.group(1))
                continue
            m=re.match("^\s*(self\.\w+)\s*=",line)
            if m:
                completionsList.append(m.group(1))
                continue
            # global property
            m=re.match("^(\w+\.?\w*)\s*=",line)
            if m:
                completionsList.append(m.group(1))
                handleDefinition(m.group(1),None,file,lineNum)
                continue
        else:
            break
    f.close()
    saveCompletions(completionsList,saveDir,"c")
    
def handleDefinition(function,param,file,lineNum,showFunc=None):
    if showFunc==None:
        showFunc=function
    if param!=None:
        showFunc+="("+handleParam(param)[0]+")"
    arr=[]
    index=function.find(".")
    if index==-1:
        index=function.find(":")
    if index!=-1:
        str1=function[(index+1):]
        arr.append(str1)
    arr.append(function)
    USER_DEFINITIONS.append([arr,showFunc,file,lineNum,0])

def saveFunction(saveDir,classname,function,param): 
    arr=handleParam(param)
    content=function+"(%s)"%(arr[1])
    trigger=function+"(%s)"%(arr[0])
    template=snippetTemplate.replace("$content",content)
    template=template.replace("$trigger",trigger)
    template=template.replace("$desc",classname)
    a=""
    if arr[0]!="":
        args=arr[0].split(",")
        for i in range(0,len(args)):
            args[i]=re.sub("\W","",args[i])
        a="-".join(args)
        a="-"+a
    saveName=function+a+".sublime-snippet"
    savePath=os.path.join(saveDir,saveName)
    f=open(savePath, "w+")
    f.write(template)
    f.close()

def handleParam(param):
    args=[]
    for item in param.split(","):
        str1=re.sub("\s","",item)
        if str1!="" and str1!="void":
            args.append(str1)
    args2=[]
    for i in range(0,len(args)):
        args2.append("${%d:%s}"%(i+1,args[i]))
    a1=", ".join(args)
    a2=", ".join(args2)
    return [a1,a2]

def saveCompletions(completionsList,saveDir,filename):    
    if len(completionsList)>0:        
        # remove duplicate
        completionsList=sorted(set(completionsList),key=completionsList.index)
        for item in completionsList:
            template=snippetTemplate.replace("$content",item)
            template=template.replace("$trigger",item)
            template=template.replace("$desc",".")
            name=re.sub("\W","_",item)
            saveName=name+".sublime-snippet"
            savePath=os.path.join(saveDir,saveName)
            f=open(savePath, "w+")
            f.write(template)
            f.close()

# delete files under dir
def deleteFiles(path,root):
    if not os.path.exists(path):
        return
    if os.path.isfile(path):
        try:
            os.remove(path)
        except Exception:
            pass
    elif os.path.isdir(path):
        for item in os.listdir(path):
            itemsrc=os.path.join(path,item)
            deleteFiles(itemsrc,root)
        if path!=root:            
            try:
                os.rmdir(path)
            except Exception:
                pass