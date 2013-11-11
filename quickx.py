#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Author: lonewolf
# Date: 2013-10-26 11:23:48
# 
import sublime
import sublime_plugin
import functools
import os
import datetime
import json
import re
import subprocess
import sys
try:
    import helper
except ImportError:
    from . import helper


CUR_PATH = os.path.dirname(os.path.realpath(__file__))
LIB_PATH="quickxlib"
DEFINITION_LIST=[]

# init plugin,load definitions
def init():
    global DEFINITION_LIST
    path=os.path.join(CUR_PATH,LIB_PATH,"definition","quickx.json")
    f=open(path,"r")
    data=f.read()
    f.close()
    DEFINITION_LIST=json.loads(data)

def checkRoot():    
    # quick_cocos2dx_root
    settings = helper.loadSettings("quickx")
    quick_cocos2dx_root = settings.get("quick_cocos2dx_root", "")
    if len(quick_cocos2dx_root)==0:
        sublime.error_message("quick_cocos2dx_root no set")
        return False
    return quick_cocos2dx_root

class LuaNewFileCommand(sublime_plugin.WindowCommand):
    def run(self, dirs):
        self.window.run_command("hide_panel")
        title = "untitle"
        on_done = functools.partial(self.on_done, dirs[0])
        v = self.window.show_input_panel(
            "File Name:", title + ".lua", on_done, None, None)
        v.sel().clear()
        v.sel().add(sublime.Region(0, len(title)))

    def on_done(self, path, name):
        filePath = os.path.join(path, name)
        if os.path.exists(filePath):
            sublime.error_message("Unable to create file, file exists.")
        else:
            # load template file
            tmplPath = os.path.join(CUR_PATH,LIB_PATH, "lua.tmpl")
            code = helper.readFile(tmplPath)
            # add attribute
            settings = helper.loadSettings("quickx")
            format = settings.get("date_format", "%Y-%m-%d %H:%M:%S")
            date = datetime.datetime.now().strftime(format)
            code = code.replace("${date}", date)
            attr = settings.get("template_attr", {})
            for key in attr:
                code = code.replace("${%s}" % (key), attr.get(key, ""))
            # save
            helper.writeFile(filePath, code)
            v=sublime.active_window().open_file(filePath)
            # cursor
            v.run_command("insert_snippet",{"contents":code})
            sublime.status_message("Lua file create success!")

    def is_enabled(self, dirs):
        return len(dirs) == 1

process=None
class QuickxRunWithPlayerCommand(sublime_plugin.WindowCommand):
    def run(self, dirs):
        # root
        quick_cocos2dx_root = checkRoot()
        if not quick_cocos2dx_root:
            return
        # player path for platform
        playerPath=""
        if sublime.platform()=="osx":
            playerPath=quick_cocos2dx_root+"/player/bin/mac/quick-x-player.app/Contents/MacOS/quick-x-player"
        elif sublime.platform()=="windows":
            playerPath=quick_cocos2dx_root+"/player/bin/win32/quick-x-player.exe"
        if playerPath=="" or not os.path.exists(playerPath):
            sublime.error_message("player no exists")
            return
        args=[playerPath]
        # param
        path=dirs[0]
        configPath=path+"/config.lua"
        args.append("-workdir")
        args.append(os.path.split(path)[0])
        args.append("-file")
        args.append("scripts/main.lua")
        args.append("-load-framework")
        if os.path.exists(configPath):
            f=open(configPath,"r")
            width=640
            height=960
            while True:
                line=f.readline()
                if line:
                    # debug
                    m=re.match("^DEBUG\s*=\s*(\d+)",line)
                    if m:
                        debug=m.group(1)
                        # print debug
                        if debug=="0":
                            args.append("-disable-write-debug-log")
                            args.append("-disable-console")
                        elif debug=="1":
                            args.append("-disable-write-debug-log")
                            args.append("-console")                            
                        else:
                            args.append("-write-debug-log")
                            args.append("-console")
                    # resolution
                    m=re.match("^CONFIG_SCREEN_WIDTH\s*=\s*(\d+)",line)
                    if m:
                        width=m.group(1)
                    m=re.match("^CONFIG_SCREEN_HEIGHT\s*=\s*(\d+)",line)
                    if m:  
                        height=m.group(1)
                else:
                    break
            f.close()
        args.append("-size")
        args.append(width+"x"+height)
        for i in range(0,len(args)):
            args[i]=args[i].encode(sys.getfilesystemencoding())
        global process
        if process:
            process.kill()
        if sublime.platform()=="osx":
            process=subprocess.Popen(args)
        elif sublime.platform()=="windows":
            process=subprocess.Popen(args,shell=True)
        
        
    def is_enabled(self, dirs):
        if len(dirs)!=1:
            return False
        mainLuaPath=dirs[0]+"/main.lua"
        if not os.path.exists(mainLuaPath):
            return False
        return True

    def is_visible(self, dirs):
        if len(dirs)!=1:
            return False
        mainLuaPath=dirs[0]+"/main.lua"
        if not os.path.exists(mainLuaPath):
            return False
        return True
        
class QuickxGotoDefinitionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # select text
        sel=self.view.substr(self.view.sel()[0])
        if len(sel)==0:
            return
        quick_cocos2dx_root = checkRoot()
        if not quick_cocos2dx_root:
            return
        # find all match file
        matchList=[]
        showList=[]
        for item in DEFINITION_LIST:
            for key in item[0]:
                if key==sel:
                    matchList.append(item)
                    showList.append(item[1])
        if len(matchList)==0:
            sublime.status_message("Can not find definition '%s'"%(sel))
        elif len(matchList)==1:
            filepath=os.path.join(quick_cocos2dx_root,matchList[0][2])
            if os.path.exists(filepath):
                self.view.window().open_file(filepath+":"+str(matchList[0][3]),sublime.ENCODED_POSITION)
            else:
                sublime.status_message("%s not exists"%(filepath))
        else:
            # multi match
            self.matchList=matchList
            self.quick_cocos2dx_root=quick_cocos2dx_root
            on_done = functools.partial(self.on_done)
            self.view.window().show_quick_panel(showList,on_done)
        
    def on_done(self,index):
        if index==-1:
            return
        item=self.matchList[index]
        filepath=os.path.join(self.quick_cocos2dx_root,item[2])
        if os.path.exists(filepath):
            self.view.window().open_file(filepath+":"+str(item[3]),sublime.ENCODED_POSITION)
        else:
            sublime.status_message("%s not exists"%(filepath))
        
    def is_enabled(self):
        return helper.checkFileExt(self.view.file_name(),"lua")

    def is_visible(self):
        return helper.checkFileExt(self.view.file_name(),"lua")

# st3
def plugin_loaded():
    sublime.set_timeout(init, 200)

# st2
if not helper.isST3():
    init()

