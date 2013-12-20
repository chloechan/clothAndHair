#-*- coding: utf-8-*-#
import re

import maya.cmds as cmds

import mainWindow

class NucleusManagement():
    """解算器管理类

    Description:
        2、包含解算器相关的管理

    Attributes:
        无
    """
    def __init__(self):
        pass
    
    def setNucleusOnOff(self, buttonX, dynInf):
        """设置某个解算器的开关状态
    
        Description:
            1、拿到解算器名
            2、若为On按钮，则设置对应解算器的开关状态为On；若为Off按钮，则设置对应解算器的开关状态为Off
            3、刷新窗口解算器列表
            
        Arguments:
            buttonX：按钮Turn On或者按钮Turn Off
    
        Returns:
            无
        """    
        oneNucleusName = comfSelRightNu(mainWindow.nucleusScrollList)
        
        if not oneNucleusName:
            print "Please Select A Right Nucleus!"
        else:
            #若按钮为Turn On，则将解算器enable属性设置为on；若按钮为Turn Off，则将解算器enable属性设置为off；
            if buttonX == "buttonOn":
                cmds.setAttr(oneNucleusName + ".enable", 1)
                print "You Have Set The Nucleus On!"
            else:
                cmds.setAttr(oneNucleusName + ".enable", 0)
                print "You Have Set The Nucleus Off!"
            
            dynInf.getNucleusName()  #调用方法刷新解算器列表
        
    def setNucleusStartF(self):
        """设置某个解算器的开始帧数
    
        Description:
            1、拿到解算器名
            2、拿到开始帧数
            3、设置对应解算器的开始帧数
            4、设置时间轴的开始帧数
                    
        Arguments:
            无
    
        Returns:
            无
        """    
        oneNucleusName = comfSelRightNu(mainWindow.nucleusScrollList)  
            
        if not oneNucleusName:
            print "Please Select A Right Nucleus!"
        else:
            startFrame = getStartFrame(mainWindow.changeTextButton)
            
            if not startFrame:
                print "Please Input A Right Integer!"
            else:
                cmds.setAttr(oneNucleusName + ".startFrame", int(startFrame))  #设置对应解算器的开始帧数
                print "This Nucleus's Start Frame Is: " + startFrame
                
                YON = cmds.confirmDialog(title = "Confirm", message = "Do You Want To Set %s As Start Time Of The Playback Range?"%startFrame, 
                                         button = ["Yes", "No"], defaultButton = "Yes", cancelButton = "No", dismissString = "No")
                if YON == "No":
                    print "You Don't Want Set The Start Time Of The Playback Range!"
                else:  
                    setPlayback(int(startFrame))  #设置时间轴的开始帧数


def comfSelRightNu(tSLName):
    """拿到一个有效的解算器名

    Description:
        若没选择解算器则提示，若选择解算器无效则提示，直到选择一个有效的解算器才返回
        
    Arguments:
        tSLName：解算器列表

    Returns:
        oneNucleusName：某个有效的解算器名
    """    
    oneNucleusInfo = cmds.textScrollList(tSLName, query = True, selectItem = True)        
    #若没有选择解算器列表中的某一项，则提示“请选择某个解算器”
    if not oneNucleusInfo:
        cmds.confirmDialog(title = "Warning", message = "Please Select A Nucleus!", button = "OK", defaultButton = "OK")
    else:
        #若场景中没有解算器，则提示“没有解算器”
        if oneNucleusInfo[0] == "There Has No Elements!":    
            cmds.confirmDialog(title = "Warning", message = "There Has No Nucleus!", button = "OK", defaultButton = "OK")
        else:
            (oneNucleusName, other) = oneNucleusInfo[0].split(" ----- ", 1)
            return oneNucleusName

def getStartFrame(tBGrp):
    """拿到一个有效的开始帧数

    Description:
        若输入为整数，则返回；若输入为空或含有非整数字符，则提示
                
    Arguments:
        tBGrp：设置开始帧的窗体

    Returns:
        startFrame：有效的开始帧数
    """    
    startFrame = cmds.textFieldButtonGrp(tBGrp, query = True, text = True)

    p = re.compile("^-?[0-9]\d*$")  #正则表达式，匹配所有整数
    #若输入为整数，则返回，若输入不为整数，则显示提示信息
    if not p.match(startFrame):
        cmds.confirmDialog(title = "Warning", message = "Please Input A Integer!", button = "OK", defaultButton = "OK")
    else:
        return startFrame

def setPlayback(startFrame):
    """设置时间轴的开始帧

    Description:
        设置时间播放轴的开始帧，并将当前帧设为开始帧
                
    Arguments:
        startFrame：开始帧数

    Returns:
        无
    """    
    cmds.playbackOptions(minTime = startFrame)
    cmds.playbackOptions(animationStartTime = startFrame)
    
    cmds.currentTime(startFrame, edit=True)

