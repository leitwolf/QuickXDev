QuickXDev
=========

Powerful quick-cocos2d-x develop plugin for sublime text 2/3

## Description

A quick-cocos2d-x develop plugin for sublime text 2/3.

##Features

 * quick-cocos2d-x api completions support(framework and cocos2dx tolua)
 * goto definition
 * system api completions support (lua 5.1)
 * some snippets,like if-else,if-elseif-else,while,comment,repeat-until....
 * create new lua file with template

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
 * support framework functions (i.e. display.newScene or newScene)
 * support cocos2dx functions (i.e. getWritablePath or CCMoveTo:create or create)
 * support cocos2dx classes (i.e. CCMoveBy)
