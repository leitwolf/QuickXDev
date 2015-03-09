QuickXDev  --ver 3.3
=========

Powerful quick-cocos2d-x develop plugin for sublime text 2/3

CHINESE：<a href="http://my.oschina.net/lonewolf/blog?catalog=412647" target="_blank">http://my.oschina.net/lonewolf/blog?catalog=412647</a>

## Description

A quick-cocos2d-x develop plugin for sublime text 2/3.

##Features

 * quick-cocos2d-x api completions support(framework and cocos2dx tolua)
 * goto definition
 * create new project
 * run with player
 * compile scripts
 * user definition auto completion
 * system api completions support (lua 5.1)
 * some snippets,like if-else,if-elseif-else,while,comment,repeat-until....
 * create new lua file with template
 * lua biuld system

## Installation

1.Install via [Package Control](https://sublime.wbond.net/)

2.Download .zip source file, then unzip it,rename it with "QuickXDev",then clone "QuickXDev" folder into the SublimeText ```Packages``` directory.  A restart of SublimeText might be nessecary to complete the install.


## Usage

###setting

```
{
    "quick_cocos2dx_root": "<path>/quick-cocos2d-x",
    "author": "<your name>",
    "compile_scripts_key": "encrypt_key"
}
```
you must set "quick_cocos2dx_root"

### goto definition

select a word then right click ->Goto Definition or press key ctrl+shift+g
 * support framework (i.e. CCNodeExtend, display.newScene, newScene, display.CENTER)
 * support cocos2dx (i.e. CCMoveBy, getWritablePath, CCMoveTo:create, create, kCCHTTPRequestMethodGET)
 * support user definition 

### Create New Project

 right click a folder on the sidebar,select "Create New Project",enter the package name,then a new project will created.

### Run with player

 right click "src" folder on the sidebar,select "Run With Player",the player will run with current project.

### Compile Scripts

 right click "src" folder on the sidebar,select "Compile Scripts",enter the output file,then it will compile all scripts to the output file.

### User definition auto completion

 right click "src" folder on the sidebar,select "Rebuild User Definition".
 and when you save a lua file in sublime,it will auto build all user definition in the current file.