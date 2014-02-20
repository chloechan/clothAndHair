#-*- coding: utf-8-*-#
import os

import maya.cmds as cmds

thisFilePath = os.path.realpath(__file__).replace("\\","/")
thisFoldPath = thisFilePath.rsplit("/", 2)[0]
noticeTextPath = thisFoldPath + "/readme.txt"

class NoticeInformation():
    """提示信息类

    Description:
        0、弹出窗体显示提示信息

    Attributes:
        无
    """
    def __init__(self):
        pass
    
    def createNoticeWin(self):
        """提示文件窗口"""
        noticeWindow = cmds.window(title = "Notice", iconName = "notice")
        cmds.columnLayout()
        noticeText = getNoticeText(noticeTextPath)
        cmds.scrollField(width = 600, height = 300, editable = False, wordWrap = True, text = noticeText)
        cmds.showWindow(noticeWindow)


def getNoticeText(noticeTextPath):
    """得到服务器上提示文件的内容"""
    noticeText = ""
    
    noticeFile = open(noticeTextPath)  #打开文件
    textLine = noticeFile.readline()    
    while textLine:  #逐行读取
        noticeText = noticeText + textLine
        textLine = noticeFile.readline()
    noticeFile.close()
    
    return noticeText
