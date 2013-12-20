#-*- coding: utf-8-*-#
import os 
import re
import shutil

import maya.cmds as cmds
import maya.mel as mel

import tools.commonTools
import tools.clothAndHairTools
import mainWindow

cT = tools.commonTools.CommonTools()  #实例化CommanTools类
clothHairT = tools.clothAndHairTools.ClothAndHairTools()  #实例化ClothAndHairTools类

mayaAppDir = os.environ["MAYA_APP_DIR"]
userPath = mayaAppDir + "/2013-x64/presets/attrPresets/nCloth" 
serverPath = "//192.168.1.5/Share/Scripts/mayaScripts/scripts/animation/clothAndHair/nClothPresets"

class ClothAndHairManagement():
    """毛发与布料管理类

    Description:
        3、预设管理、布料创建、布料属性调节

    Attributes:
        无
    """    
    def __init__(self):
        pass
      
    def getPresetsFromChar(self):
        """将特殊角色预设显示到窗体
    
        Description:
            1、拿到角色名
            2、在窗体Text处显示选中的角色名
            3、搜索Maya系统中的所有预设文件，得到带有该角色名标记的预设文件的预设名
            4、将所有结果显示到窗体
    
        Arguments:
            无
    
        Returns:
            无
        """
        charName = cmds.textScrollList(mainWindow.charsScrollList, query = True, selectItem = True)
        if charName[0] == "There Has No Elements!":
            cmds.textScrollList(mainWindow.cPreScrollList, edit = True, removeAll = True)
            cmds.textScrollList(mainWindow.cPreScrollList, edit = True, append = "There Has No Elements!")
        else:
            cmds.text(mainWindow.cPreText, edit = True, label = charName[0] + " 's presets")                
            cPresetsList = searchPresets(charName[0])
            cPresetsList.insert(0,"default")  #每个角色的预设前都添加default选项
            showListInWin(cPresetsList, mainWindow.cPreScrollList)
    
    def saveCharPreset(self):
        """保存布料预设
    
        Description:
            1、拿到布料节点，若为特殊预设则需要拿到角色名
            2、调用保存预设窗口，拿到用户输入的预设名并保存预设
            3、刷新对应窗体并选中新增项
    
        Arguments:
            无
    
        Returns:
            无
        """   
        clothHairT.checkSelMulti(1)
        selObj = cmds.ls(sl = True)
        lenOfSel = len(selObj)  
        if lenOfSel == 1:  #需要选择的是一个布料节点或带布料的物体
       
            nClothShapeName = cmds.ls(sl = True, type = "nCloth")
    
            charName = cmds.textScrollList(mainWindow.charsScrollList, query = True, selectItem=True)  #拿角色名
            if not charName:
                cmds.confirmDialog(title = "Warning", message = "Please Select A Char Name!", button = "OK", defaultButton = "OK")
            elif charName[0] == "There Has No Elements!":
                cmds.confirmDialog(title = "Warning", message = "There Has No Char In This Scene!", button = "OK", defaultButton = "OK")
            else:
                cPresetNewName = saveInPreWindow(nClothShapeName[0],charName[0])
                self.getPresetsFromChar()  #刷新特殊预设列表
                cmds.textScrollList(mainWindow.cPreScrollList, edit = True ,selectItem = cPresetNewName)  #在列表中选中该新增项
    
    def deleteCharPreset(self):
        """删除特殊角色预设
    
        Description:
            1、拿到预设文件的完整路径
            2、在Maya系统中搜索到该预设并将其删除
            3、刷新对应窗体
    
        Arguments:
            无
    
        Returns:
            无
        """
        fileList = []  
        fileList = cT.getFileListFromAPath(serverPath, fileList)  #拿到自定义预设路径下的所有文件名列表
        
        cPreName = cmds.textScrollList(mainWindow.cPreScrollList, query = True, selectItem=True) 
        if not cPreName:
            cmds.confirmDialog(title = "Warning", message = "Please Select A Char Preset!", button = "OK", defaultButton = "OK")
        elif cPreName[0] == "There Has No Elements!":
            cmds.confirmDialog(title = "Warning", message = "There Has No Preset To Delete!", button = "OK", defaultButton = "OK")
        elif cPreName[0] == "default":
            cmds.confirmDialog(title = "Warning", message = "This Preset Can't Be Deleted!", button = "OK", defaultButton = "OK")
        else:
            cPreFileName = cPreName[0] + ".mel"  #预删除的预设文件名
                    
            #判断文件是否存在
            if cPreFileName in fileList:
                YON = cmds.confirmDialog(title = "Confirm", message = "Do You Want To Delete This Preset?", 
                                         button = ["Yes", "No"], defaultButton = "Yes", cancelButton = "No", dismissString = "No")
                if YON == "No":
                    print "You Don't Want To Delete This Preset!"
                else:
                    fileForDelete = serverPath + "/" + str(cPreFileName)  #预删除文件的完整路径（服务器上）
                    os.remove(fileForDelete)  #删除文件
                    fileForDeleteBak = userPath + "/" + str(cPreFileName)  #预删除文件的完整路径（本地）
                    os.remove(fileForDeleteBak)  #删除文件
                    
                    self.getPresetsFromChar()  #刷新特殊预设列表
            else:
                print "The Preset File Is Not Exists!"
                self.getPresetsFromChar()  #刷新特殊预设列表
    
    def createNCloth(self, dynInf):
        """选中非布料物体创建布料
    
        Description:
            1、拿到物体名
            2、拿到预设名
            3、调用窗体创建布料
            4、刷新窗体的解算器显示列表（在子函数中实现）
    
        Arguments:
            无
    
        Returns:
            无
        """
        clothHairT.checkSelMulti(0)  #检测所选的物体是否都符合要求
        selObj = cmds.ls(sl = True)
        lenOfSel = len(selObj)  
        if lenOfSel >= 1:
            preFileDir = getPre(mainWindow.cPreScrollList)  #拿到布料预设名
            
            if not preFileDir:  #如果预设返回为空（包括没有选择预设、选择了default预设、预设文件不存在），则创建默认布料
                preFileDir = serverPath + "/default.mel" 
            else:
                preFileDir = preFileDir        
            
            createCNCWindow(preFileDir)  #打开创建布料的窗体
            
            dynInf.getNucleusName() #刷新显示列表
            cmds.textScrollList(mainWindow.nDynNodesScrollList, edit = True, removeAll = True)
    
    def deleteNCloth(self, dynInf):
        """选中布料物体，删除布料
        Description:
            1、拿到物体名
            2、删除布料
            3、刷新解算器列表
    
        Arguments:
            无
    
        Returns:
            无
        """
        clothHairT.checkSelMulti(1)
        selCloth = cmds.ls(sl = True)
        lenOfSel = len(selCloth)
        if lenOfSel >= 1:
            YON = cmds.confirmDialog(title = "Confirm", message = "Do You Want To Remove This Cloth?", 
                                         button = ["Yes", "No"], defaultButton = "Yes", cancelButton = "No", dismissString = "No")
            if YON == "No":
                print "You Don't Want To Remove This/These Cloth!"
            else:  
                clothHairT.selNClothShapeToMesh()  #拿到物体名
                selObj = cmds.ls(sl = True)
                for eachSelObj in selObj:
                    doDeleteNClothP(eachSelObj)  #删除布料
                    
                dynInf.getNucleusName() #刷新显示列表
                cmds.textScrollList(mainWindow.nDynNodesScrollList, edit = True, removeAll = True)
            
    def changePreset(self):
        """修改布料节点的预设
    
        Description:
            选择带布料节点的物体或布料节点，修改预设
    
        Arguments:
            无
    
        Returns:
            无
        """
        clothHairT.checkSelMulti(1)
        selCloth = cmds.ls(sl = True)
        lenOfSel = len(selCloth)
        if lenOfSel >= 1:        
            preFileDir = getPre(mainWindow.cPreScrollList)  #拿到布料预设名
            
            if not preFileDir:
                preFileDir = serverPath + "/default.mel" 
            else:
                preFileDir = preFileDir
                
            for eachSelCloth in selCloth:  #给这些布料预设
                changePresetP(eachSelCloth,preFileDir)
    
    def setClothArg(self):
        clothArgList = computeClothArg(mainWindow.softAndHardSlider)
        
        clothHairT.checkSelMulti(1)
        selObj = cmds.ls(sl = True)
        lenOfSel = len(selObj)  
        if lenOfSel == 1:  #需要选择的是一个布料节点或带布料的物体
            nClothShapeName = cmds.ls(sl = True, type = "nCloth")
            controlledClothNode =  nClothShapeName[0]
            
            cmds.setAttr(controlledClothNode+".compressionResistance", clothArgList[0])
            cmds.setAttr(controlledClothNode+".bendResistance", clothArgList[1])
            cmds.setAttr(controlledClothNode+".damp", clothArgList[2])


def showListInWin(listForShow, tSLName):
    """将列表显示到窗体的某个textScrollList

    Description:
        若列表为空，则在textScrollList显示提示信息；若不为空，则在textScrollList显示列表

    Arguments:
        listForShow：于预显示的列表
        tSLName：对应预显示列表的窗体名

    Returns:
        无
    """
    cmds.textScrollList(tSLName, edit = True, removeAll = True)  #清空
       
    if not listForShow:
        #若检索到的列表为空则在窗体中显示提示信息
        cmds.textScrollList(tSLName, edit = True, append = "There Has No Elements!")
    else:        
        #将列表元素依次显示
        for each in listForShow:
            cmds.textScrollList(tSLName, edit = True, append = each)
            
def searchPresets(charNameTarget):
    """从Maya系统中搜索预设名

    Description:
        在Maya内置布料预设目录与Maya自定义布料预设目录中搜索，根据参数的不同而返回不同的预设列表

    Arguments:
        charNameTarget：目标角色名

    Returns:
        cPresetsList：某个角色的布料预设名列表
    """
    pFileList = []  #存放所有预设文件名
    cPresetsList = []  #存放所有角色预设名
        
    #调用函数拿到某路径下的所有文件名列表
    pFileList = cT.getFileListFromAPath(serverPath, pFileList)
    
    if not pFileList:
        print "There Has No Presets!"
    else:
        #将文件名列表转化为预设名列表
        for each in pFileList:
            #若目录下没有.mel文件，则没有预设
            if each.find(".mel") < 0:
                print "There Has No Presets!"
            else:
                (pPresetName,other) = each.rsplit(".",1)
                
                #若预设名不含“_”，则说明该预设为基本预设
                if pPresetName.find("_") >= 0:
                    (other, charName) = pPresetName.rsplit("_", 1)
                    
                    #判断特殊预设文件中角色标记与所选角色名是否相同
                    if charName == charNameTarget:
                        cPresetsList.append(pPresetName)  #将该项加入到特殊预设列表中
    
    return cPresetsList

def saveInPreWindow(nClothShapeName,charNameTarget):
    """创建预设保存窗口，输入预设名，保存预设

    Description:
        在预设保存窗口拿到用户输入的预设名，若预设名符合要求则保存预设

    Arguments:
        nClothShapeName：布料节点名称
        charNameTarget:目标角色名

    Returns:
        无
    """
    result = cmds.promptDialog(title = "Save Preset", message = "Char Preset Name:", button = ["Save", "Cancel"],
                                defaultButton = "Save", cancelButton = "Cancel", dismissString = "Cancel")  #拿到用户所选择的按钮
    if result == "Save":
        presetName = cmds.promptDialog(query=True, text=True)
        #
        #对输入的预设名进行检查：
        #        1、检查该预设名是否合理（只能是英文字母，不能含有下划线等符号）；
        #        2、检查预设名是否已经存在（maya自带该检查功能）
        #
        p = re.compile("^[A-Za-z]+$")  #正则表达式，匹配所有英文字母
        if not p.match(presetName):
            cmds.confirmDialog(title = "Warning", message = "Please Input Letters(a-z A-Z) Only!", button = "OK", defaultButton = "OK")
            saveInPreWindow(nClothShapeName,charNameTarget)  #递归调用，重新创建预设保存窗体
        else:
            cPresetName = presetName + "_" + charNameTarget
            savePresetP(nClothShapeName, cPresetName)
            return cPresetName    

def savePresetP(nClothShapeName, cPresetName):
    mel.eval('saveAttrPreset %s %s false'%(nClothShapeName,cPresetName))
    oldPresetFile = userPath + "/" + cPresetName + ".mel"
    newPresetFile = serverPath + "/" + cPresetName + ".mel"
    shutil.copyfile(oldPresetFile, newPresetFile)  #将本地保存的预设复制到服务器的指定目录下
    
def getPre(cPreList):
    """根据预设列表的选中项名称，得到该项的预设文件的完整路径

    Description:
        拿到在预设列表中的选中项名称
        若找到则返回预设文件路径，若预设列表中没有选中项或选中的是“default”则返回空字符
        
    Arguments:
        无

    Returns:
        cPreFileDir：特殊预设文件路径
        None:返回为空
    """
    cPreItem = cmds.textScrollList(cPreList, query = True, selectItem=True)

    pFileList = []    
    pFileList = cT.getFileListFromAPath(serverPath, pFileList)  #调用函数拿到Maya自定义路径下的所有文件名列表
    
    #若特殊预设列表中有选中项
    if cPreItem:
        if cPreItem[0] == "default":  #选择的预设为default
            return None
        else:
            cPreFileName = cPreItem[0] + ".mel"
            cPreFileDir = ""  #若预设文件没有找到，则相当于没有选择任何预设
            if cPreFileName in pFileList:
                cPreFileDir = serverPath + "/" + cPreFileName
            return cPreFileDir
    #若没有选择任何预设
    else:
        return None

def createCNCWindow(preFileDir): 
    """该函数实现创建布料窗体的创建

    Description:
        无
        
    Arguments:
        presetName:某个正确的布料预设路径

    Returns:
        无
    """
    createNClothWin = cmds.window(title = "Create NCloth", iconName = "CN", widthHeight = (420, 80))
    cNFormLayout = cmds.formLayout()
    nucleusButton  = mel.eval('nucleusSolverButton("")')
    cmds.optionMenuGrp(nucleusButton, edit = True, cw = [1,50])
    cButtonRowLayout = cmds.rowLayout(numberOfColumns = 2, columnAttach = [(1, "right", 0),(2, "right", 0)], columnWidth=[(1, 280), (2, 80)])
    createNButton = cmds.button(label = "Create", width = 75, command = (lambda x:createNClothP(preFileDir, createNClothWin)))
    closeNButton = cmds.button(label = "Close", width = 75, command = ('cmds.deleteUI(\"' + createNClothWin + '\", window=True)'))
    cmds.setParent("..")
    cmds.formLayout(cNFormLayout, edit=True, 
                    attachForm=[(nucleusButton, "top", 12), (nucleusButton, "left", 8), (nucleusButton, "right", 8),
                                (cButtonRowLayout, "bottom", 12),(cButtonRowLayout, "left", 24), (cButtonRowLayout, "right", 24)], 
                    attachControl=[(cButtonRowLayout, "top", 12, nucleusButton)])
    cmds.setParent("..")
    cmds.showWindow(createNClothWin)

def createNClothP(preFileDir, winName):
    """实现带预设的布料的创建

    Description:
        调用Mel命令实现布料的创建
        关闭创建布料的窗体
        关联预设
        
    Arguments:
        presetName:预设文件的完整路径
        winName：创建布料的窗体名，用于关掉窗体

    Returns:
        无
    """
    mel.eval('doCreateNCloth 0')
    cmds.deleteUI(winName, window = True)
    
    shapeName = cmds.ls(sl = True)  #执行完doCreateNCloth命令后会选中新生成的nclothShape节点
    for eachShapeName in shapeName:
        mel.eval('applyPresetToNode "%s" "" "" "%s" 1'%(eachShapeName, preFileDir))  #关联预设

def doDeleteNClothP(objName):
    mel.eval("removeNCloth %s"%objName)

def changePresetP(nClothShapeName, preFileDir):
    mel.eval('applyPresetToNode "%s" "" "" "%s" 1'%(nClothShapeName, preFileDir))

def computeClothArg(sHfloatSlider):
    #[0]:friction  [1]: stretchResistance  [2]:compressionResistance  
    #[3]:bendResistance  [4]:bendAngleDropoff  [5]:mass  [6]:tangentialDrag
    #[7]:damp  [8]:maxIterations  [9]:pushOutRadius
    clothArgList = [0.100, 20.000, 10.000, 0.100, 0.000, 1.000, 0.000, 0.000, 10000, 0.028]  #clothArgList[0]
    
    softCloth = [0.05, 60.0, 10.0, 0.05, 0.3, 0.05, 0.05, 0.2, 1000.0, 0.108]
    midCloth = [2.0, 40.0, 40.0, 3.0, 0.603, 1.5, 0.4, 4.0, 1000.0, 10.0]
    hardCloth = [0.6, 50.0, 50.0, 10.0, 0.72, 3.0, 0.2, 8.0, 1000.0, 10.0]
    
    softAndHardValue = cmds.floatSliderGrp(sHfloatSlider, query = True, value = True)
    
    if softAndHardValue <= 5.0:
        friction = softCloth[0] + (midCloth[0] - softCloth[0]) / 5 * softAndHardValue  #[0]
        stretchResistance = softCloth[1] + (midCloth[1] - softCloth[1]) / 5 * softAndHardValue  #[1]
        compressionResistance = softCloth[2] + (midCloth[2] - softCloth[2]) / 5 * softAndHardValue  #[2]
        bendResistance = softCloth[3] + (midCloth[3] - softCloth[3]) / 5 * softAndHardValue  #[3]
        bendAngleDropoff = softCloth[4] + (midCloth[4] - softCloth[4]) / 5 * softAndHardValue  #[4]
        mass = softCloth[5] + (midCloth[5] - softCloth[5]) / 5 * softAndHardValue  #[5]
        tangentialDrag = softCloth[6] + (midCloth[6] - softCloth[6]) / 5 * softAndHardValue  #[6]
        damp = softCloth[7] + (midCloth[7] - softCloth[7]) / 5 * softAndHardValue  #[7]
        maxIterations = softCloth[8] + (midCloth[8] - softCloth[8]) / 5 * softAndHardValue  #[8]
        pushOutRadius = softCloth[9] + (midCloth[9] - softCloth[9]) / 5 * softAndHardValue  #[9]
        
        clothArgList[0] = friction
        clothArgList[1] = stretchResistance
        clothArgList[2] = compressionResistance
        clothArgList[3] = bendResistance
        clothArgList[4] = bendAngleDropoff
        clothArgList[5] = mass
        clothArgList[6] = tangentialDrag
        clothArgList[7] = damp
        clothArgList[8] = maxIterations
        clothArgList[9] = pushOutRadius
        
        
    elif softAndHardValue > 5.0:
        friction = midCloth[0] + (hardCloth[0] - midCloth[0]) / 5 * (softAndHardValue - 5)  #[0]
        stretchResistance = midCloth[1] + (hardCloth[1] - midCloth[1]) / 5 * (softAndHardValue - 5)  #[1]
        compressionResistance = midCloth[2] + (hardCloth[2] - midCloth[2]) / 5 * softAndHardValue  #[2]
        bendResistance = midCloth[3] + (hardCloth[3] - midCloth[3]) / 5 * softAndHardValue  #[3]
        bendAngleDropoff = midCloth[4] + (hardCloth[4] - midCloth[4]) / 5 * softAndHardValue  #[4]
        mass = midCloth[5] + (hardCloth[5] - midCloth[5]) / 5 * softAndHardValue  #[5]
        tangentialDrag = midCloth[6] + (hardCloth[6] - midCloth[6]) / 5 * softAndHardValue  #[6]
        damp = midCloth[7] + (hardCloth[7] - midCloth[7]) / 5 * softAndHardValue  #[7]
        maxIterations = midCloth[8] + (hardCloth[8] - midCloth[8]) / 5 * softAndHardValue  #[8]
        pushOutRadius = midCloth[9] + (hardCloth[9] - midCloth[9]) / 5 * softAndHardValue  #[9]
        
        clothArgList[0] = friction
        clothArgList[1] = stretchResistance
        clothArgList[2] = compressionResistance
        clothArgList[3] = bendResistance
        clothArgList[4] = bendAngleDropoff
        clothArgList[5] = mass
        clothArgList[6] = tangentialDrag
        clothArgList[7] = damp
        clothArgList[8] = maxIterations
        clothArgList[9] = pushOutRadius
    
    return clothArgList
