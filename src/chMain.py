#-*- coding: utf-8-*-#
import maya.cmds as cmds

import mainWindow
import noticeInfor
import dynInfor
import nucleusMag
import clothAndHairMag
import resolvingTools
import cacheMag
import cacheAllMag

mWin = mainWindow.MainWindow()  #实例化MainWindow类
nInf = noticeInfor.NoticeInformation()  #实例化NoticeInformation类
dynInf = dynInfor.DynInfor()  #实例化DynInfor类
nuMag = nucleusMag.NucleusManagement()  #实例化NucleusManagement类
chMag = clothAndHairMag.ClothAndHairManagement()  #实例化ClothAndHairManagement类
resT = resolvingTools.ResolvingTools()  #实例化ResolvingTools类
cacheM = cacheMag.CacheManagment()  #实例化CacheManagment类
cacheAllM = cacheAllMag.CacheAllManagement()  #实例化CacheAllManagement类


def main():
    """插件主入口

    Description:
        实现窗体的所有初始化操作

    Arguments:
        无

    Returns:
        无
    """
    
    mWin.createMainWindow()  #实现窗体初始化
    
    dynInf.getCharsName()  #实现角色名的初始显示
    dynInf.getNucleusName()  #实现解算器信息的初始显示
        
