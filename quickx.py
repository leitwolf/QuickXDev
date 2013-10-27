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

class QuickxGotoDefinitionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # select text
        sel=self.view.substr(self.view.sel()[0])
        if len(sel)==0:
        	return
        # quick_cocos2dx_root
        settings = helper.loadSettings("quickx")
        quick_cocos2dx_root = settings.get("quick_cocos2dx_root", "")
        if len(quick_cocos2dx_root)==0:
        	sublime.error_message("quick_cocos2dx_root no set")
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

