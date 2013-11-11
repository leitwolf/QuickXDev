QuickXDev
=========

Powerful quick-cocos2d-x develop plugin for sublime text 2/3

中文介绍：<a href="http://my.oschina.net/lonewolf/blog?catalog=412647" target="_blank">http://my.oschina.net/lonewolf/blog?catalog=412647</a>

## Description

A quick-cocos2d-x develop plugin for sublime text 2/3.

##Features

 * quick-cocos2d-x api completions support(framework and cocos2dx tolua)
 * goto definition
 * run with player
 * system api completions support (lua 5.1)
 * some snippets,like if-else,if-elseif-else,while,comment,repeat-until....
 * create new lua file with template
 * lua biuld system

## Installation

Download .zip source file, then unzip it,rename it with "QuickXDev",then clone "QuickXDev" folder into the SublimeText ```Packages``` directory.  A restart of SublimeText might be nessecary to complete the install.


## Usage

###setting

```
{
	"quick_cocos2dx_root": "<path>/quick-cocos2d-x",
    "template_attr": {
        "author": "<your name>"
    }
}
```
you must set "quick_cocos2dx_root"

### goto definition
select a word then right click ->Goto Definition or press key ctrl+shift+g
 * support framework (i.e. CCNodeExtend, display.newScene, newScene, display.CENTER)
 * support cocos2dx (i.e. CCMoveBy, getWritablePath, CCMoveTo:create, create, kCCHTTPRequestMethodGET)
