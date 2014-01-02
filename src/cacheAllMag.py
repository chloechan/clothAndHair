#-*- coding: utf-8-*-#
import os
import re
import shutil
import xml.dom.minidom as minidom

import maya.cmds as cmds
import maya.mel as mel

import tools.commonTools
import tools.clothAndHairTools

cT = tools.commonTools.CommonTools()  #实例化CommanTools类
clothHairT = tools.clothAndHairTools.ClothAndHairTools()  #实例化ClothAndHairTools类

thisFilePath = os.path.realpath(__file__).replace("\\","/")
thisFoldPath = thisFilePath.rsplit("/", 1)[0]
confDir = thisFoldPath + "/notice/conf.xml"

dom = minidom.parse(confDir)  #读取配置文件中的服务器盘符信息
root = dom.documentElement
serverLetterNode = root.getElementsByTagName("serverLetter")
serverLetter = serverLetterNode[0].getAttribute("Letter")  #服务器盘符

class CacheAllManagement():
    """缓存整体管理类

    Description:
        6、整理缓存，上传缓存，一键指认缓存，一键删除缓存

    Attributes:
        无
    """  
    def __init__(self):
        pass

    def prepareCacheGrade(self):
        """整理缓存文件

        Description:
            将场景中所有缓存节点所连接的缓存文件复制到某个指定路径下
                    
        Arguments:
            无
    
        Returns:
            无
        """
        #通过缓存拿到与之相连的物体名    
        cacheNodesList = clothHairT.getCacheNodes()
        #cacheNodesList =[u'YL_Char_RG_Hi_1_YL_Char_SF_Hi2_hairBackTop_hairSystemShapeCache1', u'geoCache_YL_Char_RG_Hi_1__YL_Char_SF_Hi2_body_Geo___1', u'geoCache_YL_Char_RG_Hi_1__YL_Char_SF_Hi2_cloth_Geo___1']

        result = True    
        for eachCacheNode in cacheNodesList:
            #eachCacheNode = "YL_Char_RG_Hi_1_YL_Char_SF_Hi2_hairBackTop_hairSystemShapeCache1"
            #eachCacheNode = "geoCache_YL_Char_RG_Hi_1__YL_Char_SF_Hi2_cloth_Geo___1"
            if isNOrGeoCacheNode(eachCacheNode) == "geoCache":
                cacheFlag = 1     
                
                isMultCache = cmds.listConnections(eachCacheNode, type = "cacheBlend")
                if isMultCache:
                    #若某个物体存在多个缓存,则选中该物体并显示提示信息
                    shapeWithCache = cmds.cacheFile(eachCacheNode, query=True, geometry=True)
                    objName = cmds.listRelatives(shapeWithCache[0], parent = True)  #拿到该cache的物体名
                    
                    cmds.select(objName[0],replace = True)
                    cmds.confirmDialog(title = "Warning", message = "Object %s Has More Than One Cache"%objName[0], button = "OK", defaultButton = "OK")
                    cmds.warning("Please Delete Other Cache Nodes And CacheBlend Node!")
                    result = False
                    break
                else:
                    #只有一个缓存                
                    shapeWithCache = cmds.cacheFile(eachCacheNode, query=True, geometry=True)
                    objName = cmds.listRelatives(shapeWithCache[0], parent = True)  #拿到该cache的物体名
                    print objName  #拿到该缓存多连的物体名
                        
                    cacheFinalDir = getFinalCacheDir(objName[0], cacheFlag)  #根据物体名拿到缓存预存放路径
                    ObjNameNew = getObjNameNew(objName[0])
                    eachCacheFileList = cmds.cacheFile(eachCacheNode, query = True, f = True )  #拿到缓存节点的文件信息，含mc与xml两个文件
                    
                    #将缓存文件存在该目录下（若目录不存在则创建）,并对其重命名
                    #若文件夹已经存在，则不做任何操作，若不存在则创建文件夹
                    if os.path.exists(cacheFinalDir):
                        pass
                    else:
                        os.makedirs(cacheFinalDir)
                        
                    newCacheFileDirMC = cacheFinalDir + ObjNameNew + ".mc"
                    newCacheFileDirXML = cacheFinalDir + ObjNameNew + ".xml"
                    for eacheachCacheFile in eachCacheFileList:
                        if eacheachCacheFile.find(".mc") >= 0:
                            shutil.copyfile(eacheachCacheFile, newCacheFileDirMC)  #复制缓存文件.mc
                        elif eacheachCacheFile.find(".xml") >= 0:
                            shutil.copyfile(eacheachCacheFile, newCacheFileDirXML)  #复制缓存文件.mc
                        
            elif isNOrGeoCacheNode(eachCacheNode) == "nCache":
                cacheFlag = 2
                
                isMultCache = cmds.listConnections(eachCacheNode, type = "cacheBlend")
                if isMultCache:
                    hairSystemName = cT.delDupFromList(cmds.listConnections(eachCacheNode, type = "hairSystem"))
                    hairSystemShapeName = cmds.listRelatives(hairSystemName[0], shapes = True)  #拿到该cache的hairSystemShape名
                    
                    cmds.select(hairSystemShapeName[0],replace = True)
                    cmds.confirmDialog(title = "Warning", message = "HairSystem %s Has More Than One Cache"%hairSystemShapeName[0], button = "OK", defaultButton = "OK")
                    cmds.warning("Please Delete Other Cache Nodes And CacheBlend Node!")
                    result = False
                    break
                else:
                    hairSystemName = cT.delDupFromList(cmds.listConnections(eachCacheNode, type = "hairSystem"))
                    hairSystemShapeName = cmds.listRelatives(hairSystemName[0], shapes = True)  #拿到该cache的hairSystemShape名
                    
                    cacheFinalDir = getFinalCacheDir(hairSystemShapeName[0], cacheFlag)  #根据物体名拿到缓存预存放路径
                    ObjNameNew = getObjNameNew(hairSystemShapeName[0])
                    eachCacheFileList = cmds.cacheFile(eachCacheNode, query = True, f = True )  #拿到缓存节点的文件信息，含mc与xml两个文件
                    
                    #将缓存文件存在该目录下（若目录不存在则创建）,并对其重命名
                    #若文件夹已经存在，则不做任何操作，若不存在则创建文件夹
                    if os.path.exists(cacheFinalDir):
                        pass
                    else:
                        os.makedirs(cacheFinalDir)
                        
                    newCacheFileDirMC = cacheFinalDir + ObjNameNew + ".mc"
                    newCacheFileDirXML = cacheFinalDir + ObjNameNew + ".xml"
                    for eacheachCacheFile in eachCacheFileList:
                        if eacheachCacheFile.find(".mc") >= 0:
                            shutil.copyfile(eacheachCacheFile, newCacheFileDirMC)  #复制缓存文件.mc
                        elif eacheachCacheFile.find(".xml") >= 0:
                            shutil.copyfile(eacheachCacheFile, newCacheFileDirXML)  #复制缓存文件.mc
                
        if result:
            cmds.confirmDialog(title = "OK", message = "Prepare Cache OK !", button = "OK", defaultButton = "OK")
        
    def uploadCache(self):
        """调用上传缓存文件夹的窗口""" 
        createUploadWindow()

    def attachCacheAll(self):
        """删除场景中所有的缓存节点,调用一键指缓存的窗口""" 
        cacheNodesList = clothHairT.getCacheNodes()
        if cacheNodesList:
            for eachNCacheNode in cacheNodesList:
                mel.eval('deleteCacheFile 2 {"keep", "%s"}'%eachNCacheNode)
        
        createAttachAllWindow()

    def deleteCacheAll(self):
        """删除场景中所有的缓存节点"""
        cacheNodesList = clothHairT.getCacheNodes()
        if cacheNodesList:
            for eachNCacheNode in cacheNodesList:
                mel.eval('deleteCacheFile 2 {"keep", "%s"}'%eachNCacheNode)
            
            cmds.confirmDialog(title = "OK", message = "Delete All Cache Successful!", button = "OK", defaultButton = "OK")
        else:
            cmds.confirmDialog(title = "Warning", message = "There Has No Cache In This Sence!", button = "OK", defaultButton = "OK")


def isNOrGeoCacheNode(cacheNodeName):
    """判断是nCache或是geoCache

    Description:
        判断某个缓存节点是geo缓存还是n缓存
                
    Arguments:
        cacheNodeName：缓存节点名

    Returns:
        “nCache”：为nCache
        “geoCache”：为geoCache
    """
    cacheFileXML = cmds.cacheFile(cacheNodeName, query=True, f=True)[0]
    cacheSize = os.path.getsize(cacheFileXML)  #该XML文件的大小        
    if cacheSize > 5000:
        return "nCache"
    else:
        return "geoCache"


def getFinalCacheDir(objName,cacheFlag):
    """根据物体名拿到缓存预存放路径

    Description:
        根据物体名拿到缓存预存放路径
                
    Arguments:
        objName：物体名
        cacheFlag：缓存类型。1为cloth_cache；2为hair_cache

    Returns:
        finalCacheDir：某个缓存的存放路径
    """ 
    #根据物体名拿到缓存预存放路径
    finalDirUp = getFinalDirUp()
    
    longName = cmds.ls(objName, long = True)[0]  #拿到该物体所在组的命名空间
    charName = longName.split("|")[1].split(":")[0]  #若物体在跟目录下，则为该物体名
        
    if cacheFlag == 1:
        cacheflod = "/cloth_cache/"
    elif cacheFlag == 2:
        cacheflod = "/hair_cache/"
    
    finalCacheDir = finalDirUp + charName + cacheflod
    return finalCacheDir


def getFinalDirUp():
    """得到缓存存放的上级路径

    Description:
        通过场景文件所在路径信息得到缓存预存放的部分路径
                
    Arguments:
        无

    Returns:
        upFileDir + cacheDirMidA +camId +"/"：缓存预存放的部分路径
    """ 
    mayaFileDir = cmds.file(query = True, loc = True)
    if mayaFileDir == "unknown":
        cmds.confirmDialog(title = "Warning", message = "Please Save This File!", button = "OK", defaultButton = "OK")
        return None
    else:
        (upFileDir,fileName) = mayaFileDir.rsplit("/", 1)  #文件所在的文件夹名
        
        cacheDirMidA = "/Data/"
    
        camId = fileName.rsplit(".")[0]  #镜头号
        
        return upFileDir + cacheDirMidA +camId +"/solCache/"


def getObjNameNew(objName):
    """根据所选物体名得到当前最新的物体名"""
    if objName.find(":") >= 0:
        objNameNew = objName.replace(":", "__")  #由于系统命名不能带“：”，所以将“：”替换为“__”
    else:
        objNameNew = objName
        
    return objNameNew

def createUploadWindow():
    #---------------------------------------------以下窗体显示部分------------------------------------------
    uploadCacheWindow = cmds.window(title = "Upload Cache", iconName = "UC", widthHeight = (420, 160))
    
    uploadForm = cmds.formLayout()
    #------------------以下为标签的内容---------------------
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    
    #标签1
    child1 = cmds.rowColumnLayout(numberOfColumns=2)    
    chlid1Form = cmds.formLayout()
    uCOptionMenu = cmds.optionMenu(label = "Project Name:     ")
    projectNameList = getProjectName()  #添加optionMenu的项
    for projectName in projectNameList:
        cmds.menuItem(label = projectName)
    tFolder = getUploadDir(uCOptionMenu)    #拿到tFolder
    uploadTextRowLayout = cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(1, 88), (2, 280)], rowSpacing = (1, 4))
    uploadDirText = cmds.text(label="Upload Directory: ")
    uploadDirTextField = cmds.textField(text = tFolder, editable = False)
    cmds.setParent("..")        
    cmds.formLayout(chlid1Form, edit=True, attachForm=[(uCOptionMenu, "top", 6), (uCOptionMenu, "left", 6), (uCOptionMenu, "right", 4),
                                        (uploadTextRowLayout, "left", 4), (uploadTextRowLayout, "bottom", 10), (uploadTextRowLayout, "right", 4)],
                                        attachControl=[(uploadTextRowLayout, "top", 12, uCOptionMenu)] )
    cmds.setParent( '..' )
    cmds.setParent( '..' )

    #标签2
    child2 = cmds.rowColumnLayout(numberOfColumns=2)
    chlid2Form = cmds.formLayout()
    tFolder = ""
    chlid2TextFBG = cmds.textFieldButtonGrp(label = "Upload Directory: ", columnWidth = [(1, 90),(2, 260),(3,80)], text = tFolder, editable = False, buttonLabel = "brower")
    browerNoticeText = cmds.text("Please Select Project Name!")
    cmds.formLayout(chlid2Form, edit=True, attachForm=[(chlid2TextFBG, "top", 6), (chlid2TextFBG, "left", 0), (chlid2TextFBG, "right", 0),
                                                       (browerNoticeText, "left", 4), (browerNoticeText, "bottom", 10), (browerNoticeText, "right", 4)])
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
    cmds.tabLayout(tabs, edit=True, tabLabel=((child1, "Basic"), (child2, "Advanced")) )
    cmds.setParent( '..' )
    #----------------以下为button的内容-----------------
    uCButtonRowLayout = cmds.rowLayout(numberOfColumns = 2, columnAttach = [(1, "right", 0),(2, "right", 0)], columnWidth=[(1, 280), (2, 78)])
    #cmds.button(label = "Upload", width = 75, command = 'clothAndHair.chMain.otherWinCmd.doUploadCache(\"' + uCOptionMenu + '\", \"' + uploadCacheWindow+'\")')
    uploadButton = cmds.button(label = "Upload", width = 75)
    closeButton = cmds.button(label = "Close", width = 75)
    cmds.setParent("..")
    
    cmds.formLayout(uploadForm, edit=True, attachForm=[(tabs, "top", 4), (tabs, "left", 4), (tabs, "bottom", 50), (tabs, "right", 4),
                                                    (uCButtonRowLayout, "bottom", 12),(uCButtonRowLayout, "left", 52), (uCButtonRowLayout, "right", 4)],
                                                    attachControl=[(uCButtonRowLayout, "top", 12, tabs)] )
    cmds.showWindow(uploadCacheWindow)
    
    #---------------------------------------------以下窗体指令部分------------------------------------------
    cmds.optionMenu(uCOptionMenu, edit = True, changeCommand = (lambda x:changeProject(uploadDirTextField, uCOptionMenu)))
    cmds.textFieldButtonGrp(chlid2TextFBG, edit = True, buttonCommand = (lambda:getUploadDirAdv(chlid2TextFBG)))
    cmds.button(uploadButton, edit = True, command = lambda x:doUploadCache(tabs , child1 , child2 , uploadDirTextField , chlid2TextFBG , uploadCacheWindow ))
    cmds.button(closeButton, edit = True, command=('cmds.deleteUI(\"' + uploadCacheWindow + '\", window=True)'))

#--------------------------------------------upload窗体执行start------------------------------------------------------
def getProjectName():
    """拿到服务器上的所有项目文件名（四个英文大写字母）

    Description:
        拿到服务器上的所有项目文件名（四个英文大写字母）
        若没有项目文件，则返回空
        若服务器盘符不存在，则返回提示信息

    Arguments:
        无

    Returns:
        projectNameList：项目文件名列表            
    """
    projectNameList = []
    fileList = []
    if os.path.exists(serverLetter):
        fileList = cT.getFileListFromAPath(serverLetter, fileList)
        
        p = re.compile("^[A-Z]{4}$")  #正则表达式，匹配四个大写的英文字母            
        for eachFileName in fileList:
            if p.match(eachFileName):
                projectNameList.append(eachFileName)
            else:
                pass           
        
        if not projectNameList:
            #若服务器盘符下没有项目文件
            projectNameList.append("None")
        else:
            pass
    else:
        #若服务器盘符不存在
        projectNameList.append("Can't Find " + serverLetter)
        
    return projectNameList

def changeProject(uploadDirTextField, uCOptionMenu):
    """通过选择不同的项目文件修改目标路径"""
    tFolder = getUploadDir(uCOptionMenu)
    cmds.textField(uploadDirTextField, edit = True, text = tFolder, editable = False)

def getUploadDir(uCOptionMenu):
    """得到服务器上传路径"""
    projectName = cmds.optionMenu(uCOptionMenu, query = True, value = True)
    
    mayaFileDir = cmds.file(query = True, loc = True)
    (upFileDir,fileName) = mayaFileDir.rsplit("/", 1)  #文件所在的文件夹名
    camName = fileName.rsplit(".", 1)[0]  #文件名
    
    tFolder = serverLetter + projectName + "/Data/" + camName + "/solCache/"  #服务器项目文件路径
    return tFolder

def getSourceDir():
    """得到本地路径"""
    mayaFileDir = cmds.file(query = True, loc = True)
    (upFileDir,fileName) = mayaFileDir.rsplit("/", 1)  #文件所在的文件夹名
    camName = fileName.rsplit(".", 1)[0]  #文件名
    
    sFolder = upFileDir + "/Data/" + camName + "/solCache/"  #本地项目文件路径
    return sFolder

def getUploadDirAdv(chlid2TextFBG):
    """得到自定义的服务器上传路径"""
    uploadDirFromCh = cmds.fileDialog2(fileMode = 3, dialogStyle = 2, returnFilter = True)
    
    mayaFileDir = cmds.file(query = True, loc = True)
    (upFileDir,fileName) = mayaFileDir.rsplit("/", 1)  #文件所在的文件夹名
    camName = fileName.rsplit(".", 1)[0]  #文件名

    if uploadDirFromCh:
        tFolder = uploadDirFromCh[0] + "/Data/" + camName + "/solCache/"  #服务器文件路径
    else:
        tFolder = ""    #若没有选择，则为空
    
    cmds.textFieldButtonGrp(chlid2TextFBG, edit = True, text = tFolder, editable = False)

def copyFolderOs(sFolder,tFolder):
    """复制文件夹及其子文件夹/文件

    Description:
        复制文件夹及其子文件夹/文件
                
    Arguments:
        sFolder：源文件路径
        tFolder：目标文件路径

    Returns:
        upFileDir + cacheDirMidA +camId +"/"：缓存预存放的部分路径
    """ 

    sourcePath = sFolder  #原文件夹
    destPath = tFolder  #目标文件夹

    for root, dirs, files in os.walk(sourcePath):
 
        dest = destPath + root.replace(sourcePath, '')
 
        #若目标文件夹不存在，则创建
        if not os.path.isdir(dest):
            os.makedirs(dest) 
            print 'Directory created at: ' + dest
 
        #复制当前路径下的所有文件
        for f in files: 

            oldLoc = root + '/' + f
            newLoc = dest + '/' + f
 
            if not os.path.isfile(newLoc):
                try:
                    shutil.copy2(oldLoc, newLoc)
                    print 'File ' + f + ' copied.'
                except IOError:
                    print 'file "' + f + '" already exists'

def doUploadCache(tabs, child1, child2, uploadDirTextField, chlid2TextFBG, uploadCacheWindow):
    """将本地指定路径内的所有文件复制到服务器的指定路径下
    
        Description:
            可实现多次上传，重名则自动覆盖，只保留最新版本
            若本地文件夹存在，则上传；若不存在，则显示提示信息
                    
        Arguments:
            tabs：标签名
            child1：子标签名
            child2：子标签名
            uploadDirTextField:标签1的上传地址
            chlid2TextFBG:标签2的上传地址
            uploadCacheWindow：上传窗口名
    
        Returns:
            无
    """ 
    tabName = cmds.tabLayout(tabs, query = True, selectTab = True)
    chlid1Name = cmds.rowColumnLayout(child1, query = True, fullPathName = True).rsplit("|", 1)[1]
    chlid2Name  = cmds.rowColumnLayout(child2, query = True, fullPathName = True).rsplit("|", 1)[1]
    tFolder = ""
    if tabName == chlid1Name:
        tFolder = cmds.textField(uploadDirTextField, query = True, text = True)
    elif tabName == chlid2Name:
        tFolder = cmds.textFieldButtonGrp(chlid2TextFBG, query = True, text = True)
    sFolder = getSourceDir()
          
    if not tFolder:
        cmds.confirmDialog(title = "OK", message = "Please Select A Directory To Upload!", button = "OK", defaultButton = "OK")
    elif not os.path.exists(sFolder) and tFolder:
        cmds.confirmDialog(title = "Warning", message = "Please Prepare Cache!", button = "OK", defaultButton = "OK")
        cmds.deleteUI(uploadCacheWindow, window=True) 
    else:
        print "-------------source folder---------------" 
        print sFolder
        print "-------------target folder---------------" 
        print tFolder
        copyFolderOs(sFolder,tFolder)
        cmds.confirmDialog(title = "OK", message = "Upload Cache OK !", button = "OK", defaultButton = "OK")
        cmds.deleteUI(uploadCacheWindow, window=True)
#--------------------------------------------upload窗体执行end------------------------------------------------------

def createAttachAllWindow():
    #---------------------------------------------以下窗体显示部分------------------------------------------
    attachCacheWindow = cmds.window(title = "Attach Cache", iconName = "AC", widthHeight = (420, 180))
    
    attachForm = cmds.formLayout()
    #------------------以下为标签的内容---------------------
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    
    #标签1
    child1 = cmds.rowColumnLayout(numberOfColumns=2)    
    chlid1Form = cmds.formLayout()
    
    projectOptionMenu = cmds.optionMenuGrp(label = "Project Name:     ")
    projectNameList = getProjectName()  #添加projectOptionMenu的项
    for projectName in projectNameList:
        pItem = cmds.menuItem(label = projectName)
    cameraOptionMenu = cmds.optionMenuGrp(label = "Camera Name:    ")
    cameraNameList = getCameraName(projectOptionMenu)  #添加cameraOptionMenu的项
    for cameraName in cameraNameList:
        cmds.menuItem(label = cameraName)

    tFolder = getAttachDir(projectOptionMenu, cameraOptionMenu)    #拿到tFolder
    attachTextRowLayout = cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(1, 88), (2, 280)], rowSpacing = (1, 4))
    attachDirText = cmds.text(label = "Attach Directory: ")
    attachDirTextField = cmds.textField(text = tFolder, editable = False)
    cmds.setParent("..")        
    cmds.formLayout(chlid1Form, edit=True, attachForm=[(projectOptionMenu, "top", 6), (projectOptionMenu, "left", 4), (projectOptionMenu, "right", 4),
                                        (cameraOptionMenu, "left", 4), (cameraOptionMenu, "right", 4),
                                        (attachTextRowLayout, "left", 4), (attachTextRowLayout, "bottom", 10), (attachTextRowLayout, "right", 4)],
                                        attachControl=[(cameraOptionMenu, "top", 6, projectOptionMenu), (attachTextRowLayout, "top", 6, cameraOptionMenu)] )
    cmds.setParent( '..' )
    cmds.setParent( '..' )

    #标签2
    child2 = cmds.rowColumnLayout(numberOfColumns=2)
    chlid2Form = cmds.formLayout()
    tFolder = ""
    chlid2TextFBG = cmds.textFieldButtonGrp(label = "Attach Directory: ", columnWidth = [(1, 90),(2, 260),(3,80)], text = tFolder, editable = False, buttonLabel = "brower")
    browerNoticeText = cmds.text("Please Select solCache Folder!")
    cmds.formLayout(chlid2Form, edit=True, attachForm=[(chlid2TextFBG, "top", 6), (chlid2TextFBG, "left", 0), (chlid2TextFBG, "right", 0),
                                                       (browerNoticeText, "left", 4), (browerNoticeText, "bottom", 10), (browerNoticeText, "right", 4)])
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
    cmds.tabLayout(tabs, edit=True, tabLabel=((child1, "Basic"), (child2, "Advanced")) )
    cmds.setParent( '..' )
    #----------------以下为button的内容-----------------
    aCButtonRowLayout = cmds.rowLayout(numberOfColumns = 2, columnAttach = [(1, "right", 0),(2, "right", 0)], columnWidth=[(1, 280), (2, 78)])
    attachButton = cmds.button(label = "Attach", width = 75)
    closeButton = cmds.button(label = "Close", width = 75)
    cmds.setParent("..")
    
    cmds.formLayout(attachForm, edit=True, attachForm=[(tabs, "top", 4), (tabs, "left", 4), (tabs, "bottom", 50), (tabs, "right", 4),
                                                    (aCButtonRowLayout, "bottom", 12),(aCButtonRowLayout, "left", 52), (aCButtonRowLayout, "right", 4)],
                                                    attachControl=[(aCButtonRowLayout, "top", 12, tabs)] )
    cmds.showWindow(attachCacheWindow)

    #---------------------------------------------以下窗体指令部分------------------------------------------
    cmds.optionMenuGrp(projectOptionMenu, edit = True, changeCommand = (lambda x:changeAttachProject(attachDirTextField, projectOptionMenu, cameraOptionMenu)))
    cmds.optionMenuGrp(cameraOptionMenu, edit = True, changeCommand = (lambda x:changeAttachCamera(attachDirTextField, projectOptionMenu, cameraOptionMenu)))
    cmds.textFieldButtonGrp(chlid2TextFBG, edit = True, buttonCommand = (lambda:getAttachDirAdv(chlid2TextFBG)))
    cmds.button(attachButton, edit = True, command = (lambda x:doAttachCacheAll(tabs, child1, child2, attachDirTextField, chlid2TextFBG, attachCacheWindow)))
    cmds.button(closeButton, edit = True, command=('cmds.deleteUI(\"' + attachCacheWindow + '\", window=True)'))

#--------------------------------------------attachAll窗体执行start------------------------------------------------------
def getCameraName(projectOptionMenu):
    """得到服务器上的镜头文件夹列表"""
    cameraNameList = []
    fileList = []
    projectName = cmds.optionMenuGrp(projectOptionMenu, query = True, value = True)  #拿到项目名
    if projectName == "None" or projectName == "Can't Find " + serverLetter:
        cameraNameList.append("None")
    else:
        cameraFolder = serverLetter + projectName +"/Data/"
        if os.path.exists(cameraFolder):
            fileList = cT.getFileListFromAPath(cameraFolder, fileList)  #拿到所有的文件
            if not fileList:
                cameraNameList.append("None")
            else:
                for eachFile in fileList:
                    if eachFile.find(".") < 0:
                        cameraNameList.append(eachFile)  #拿到所有的镜头文件
        else:
            cameraNameList.append("None")

    return cameraNameList


def getAttachDir(projectOptionMenu, cameraOptionMenu):
    """得到服务器上传路径"""
    projectName = cmds.optionMenuGrp(projectOptionMenu, query = True, value = True)
    cameraName = cmds.optionMenuGrp(cameraOptionMenu, query = True, value = True)
    if projectName == "None" or projectName == "Can't Find " + serverLetter or cameraName == "None":
        return ""
    else:
        tFolder = serverLetter + projectName + "/Data/" + cameraName + "/solCache/"  #服务器项目文件路径
        if os.path.exists(tFolder):
            return tFolder
        else:
            return ""
        

def getAttachDirAdv(chlid2TextFBG):
    """得到自定义的服务器上传路径"""
    attachDirFromCh = cmds.fileDialog2(fileMode = 3, dialogStyle = 2, returnFilter = True)
    
    if attachDirFromCh:
        tFolder = attachDirFromCh[0]
    else:
        tFolder = ""    #若没有选择，则为空
    
    cmds.textFieldButtonGrp(chlid2TextFBG, edit = True, text = tFolder, editable = False)


def changeAttachProject(attachDirTextField, projectOptionMenu, cameraOptionMenu):
    """通过选择不同的项目文件修改目标路径"""

    cameraNameList = getCameraName(projectOptionMenu)  #拿到cameraOptionMenu的项
    cMenuItemList = getCameraItems(cameraOptionMenu)  #拿到cameraOptionMenu的item

    for each in cMenuItemList:  #删除旧项    
        cmds.deleteUI(each)    

    cmds.optionMenuGrp(cameraOptionMenu, edit = True)
    for cameraName in cameraNameList:  #添加新项
        cmds.menuItem(label = cameraName)
    
    tFolder = getAttachDir(projectOptionMenu, cameraOptionMenu)
    cmds.textField(attachDirTextField, edit = True, text = tFolder, editable = False)

def changeAttachCamera(attachDirTextField, projectOptionMenu, cameraOptionMenu):
    tFolder = getAttachDir(projectOptionMenu, cameraOptionMenu)
    cmds.textField(attachDirTextField, edit = True, text = tFolder, editable = False)


def getCameraItems(cameraOptionMenu):
    """拿到cameraOptionMenu的item"""
    return cmds.optionMenuGrp(cameraOptionMenu, query = True, itemListLong = True)
    
def doAttachCacheAll(tabs, child1, child2, attachDirTextField, chlid2TextFBG, attachCacheWindow):
    tabName = cmds.tabLayout(tabs, query = True, selectTab = True)
    chlid1Name = cmds.rowColumnLayout(child1, query = True, fullPathName = True).rsplit("|", 1)[1]
    chlid2Name  = cmds.rowColumnLayout(child2, query = True, fullPathName = True).rsplit("|", 1)[1]
    tFolder = ""
    if tabName == chlid1Name:
        tFolder = cmds.textField(attachDirTextField, query = True, text = True)
    elif tabName == chlid2Name:
        tFolder = cmds.textFieldButtonGrp(chlid2TextFBG, query = True, text = True)
        
    if not tFolder:
        #若该场景文件夹在服务器上不存在
        cmds.confirmDialog(title = "Warning", message = "Please Select A Right Camera!", button = "OK", defaultButton = "OK")
        cmds.deleteUI(attachCacheWindow, window=True)
    else:
        #若该场景文件夹在服务器上存在
        clothCacheXMLList = getCacheXMLFromDir(tFolder, "cloth")  #拿到与该场景相关的所有物体缓存文件
        hairCacheXMLList = getCacheXMLFromDir(tFolder, "hair")  #拿到与该场景相关的所有毛发缓存文件
                
        allCacheXMLList = clothCacheXMLList + hairCacheXMLList
        if not allCacheXMLList:  
            #若该场景文件下的缓存列表为空
            cmds.confirmDialog(title = "Warning", message = "There Has No Caches About This Camera Uploaded !", button = "OK", defaultButton = "OK")
            cmds.deleteUI(attachCacheWindow, window=True)
        else:  
            #若该场景文件下的缓存列表不为空
            allDagObjects = cmds.ls(dagObjects = True, type = "transform")  #拿到场景中所有的transform节点(不包括shape节点)
            for eachDagObject in allDagObjects:
                eachClothCacheDir = []
                eachClothCacheFile = []
                for eachClothCacheXML in clothCacheXMLList:  #遍历缓存文件，根据缓存名去推断物体名
                    eachClothCacheNameTemp = eachClothCacheXML.rsplit("/", 1)[1].split(".")[0]
                    eachClothCacheName = eachClothCacheNameTemp.replace("__", ":")
                    
                    if cT.rMatchString(eachDagObject, eachClothCacheName) == 1:
                        #若物体名中包含缓存名（或重合），则将该缓存文件加入到预连接列表中
                        eachClothCacheDir.append(eachClothCacheXML.rsplit("/", 1)[0] + "/")  #缓存存放路径
                        eachClothCacheFile.append(eachClothCacheNameTemp)  #缓存名
                
                clothCacheNumber = len(eachClothCacheDir)  #eachClothCacheDir的长度与eachClothCacheFile的长度相同
                if clothCacheNumber >= 1:
                    for i in range(clothCacheNumber):  #正常情况下一个物体只有一个缓存（i = 0），但若某个物体与多个缓存文件匹配，则依次连接
                        attachClothCacheInfo = attachClothCacheNode(eachDagObject, eachClothCacheDir[i], eachClothCacheFile[i])
                        cmds.warning("!!!----- " + attachClothCacheInfo)
                        #print "cacheFileName:"+eachClothCacheFile[i]
            
            allHairSystemShape = cmds.ls(dagObjects = True, type = "hairSystem")  #拿到场景中所有的hairSystem节点
            for eachHairSystemShape in allHairSystemShape:
                eachHairCacheDir = []
                eachHairCacheFile = []
                for eachHairCacheXML in hairCacheXMLList:  #遍历缓存文件，根据缓存名去推断物体名
                    eachHairCacheNameTemp = eachHairCacheXML.rsplit("/", 1)[1].split(".")[0]
                    eachHairCacheName = eachHairCacheNameTemp.replace("__", ":")  #replace方法：找到则替换，没找到则直接赋予
                
                    if cT.rMatchString(eachHairSystemShape, eachHairCacheName) == 1:
                        #若物体名中包含缓存名（或重合），则将该缓存文件加入到预连接列表中
                        eachHairCacheDir.append(eachHairCacheXML.rsplit("/", 1)[0] + "/")  #缓存存放文件夹路径
                        eachHairCacheFile.append(eachHairCacheNameTemp)  #缓存文件名
                        
                hairCacheNumber = len(eachHairCacheDir)  #eachHairCacheDir的长度与eachHairCacheFile的长度相同
                if hairCacheNumber >= 1:
                    for i in range(hairCacheNumber):  #正常情况下一个物体只有一个缓存（i = 0），但若某个物体与多个缓存文件匹配，则依次连接
                        attachHairCacheInfo = attachHairCacheNode(eachHairSystemShape, eachHairCacheDir[i], eachHairCacheFile[i])
                        cmds.warning("!!!----- " + attachHairCacheInfo)
                        #print "cacheFileName:"+eachHairCacheFile[i]

            
            cmds.confirmDialog(title = "OK", message = "Attach All Cache Successful!", button = "OK", defaultButton = "OK")
            cmds.deleteUI(attachCacheWindow, window=True)
            
                    
def attachClothCacheNode(eachDagObject, eachObjCacheDir, eachObjCacheFile):
    """连接物体缓存"""
    objShapeName = cmds.listRelatives(eachDagObject, shapes = True)  #拿到物体的shape节点
    connectFlag = False
    for eachShapeNode in objShapeName:                    
        if eachShapeNode.find("Deformed") >= 0:
            switch = mel.eval('createHistorySwitch("%s",false)'%eachShapeNode)
            cacheNode = cmds.cacheFile(fileName = eachObjCacheFile, directory = eachObjCacheDir, ia = "%s.inp[0]"%switch, attachFile = True)                
            cmds.setAttr("%s.playFromCache"% switch, 1)
            cmds.connectAttr(cacheNode+".inRange", switch+".playFromCache")
            connectFlag = True

    if not connectFlag:
        switch = mel.eval('createHistorySwitch("%s",false)'%objShapeName[0])
        cacheNode = cmds.cacheFile(fileName = eachObjCacheFile, directory = eachObjCacheDir, ia = "%s.inp[0]"%switch, attachFile = True)            
        cmds.setAttr("%s.playFromCache"% switch, 1)
        cmds.connectAttr(cacheNode+".inRange", switch+".playFromCache")
        
    return eachDagObject + " Attach To : " + eachObjCacheDir + eachObjCacheFile + ".xml"
    
def attachHairCacheNode(eachDagObject, eachObjCacheDir, eachObjCacheFile):    
    """连接毛发缓存"""
    cacheNode = cmds.cacheFile(attachFile = True, fileName = eachObjCacheFile, directory = eachObjCacheDir, 
            channelName = [eachDagObject + "_hairCounts", eachDagObject + "_vertexCounts", eachDagObject + "_positions"], 
            inAttr = [eachDagObject + ".hairCounts", eachDagObject + ".vertexCounts", eachDagObject + ".positions"])
    cmds.setAttr("%s.playFromCache"% eachDagObject, 1)
    cmds.connectAttr(cacheNode+".inRange", eachDagObject+".playFromCache")
    
    return eachDagObject + " Attach To : " + eachObjCacheDir + eachObjCacheFile + ".xml"

def getCacheXMLFromDir(upFolder, cacheFlag):
    """在服务器上拿到与该文件相关的所有缓存文件（.xml）"""
    allCacheFile = DFS_Dir(upFolder)  #深度优先遍历该文件夹下的所有文件
                
    clothCacheFileXML = []
    hairCacheFileXML = []
    
    for eachCacheFile in allCacheFile:
        if eachCacheFile.find(".xml") >= 0 and eachCacheFile.find("cloth_cache") >= 0:
            newEachCacheFile = eachCacheFile.replace("\\", "/")
            clothCacheFileXML.append(newEachCacheFile)
        elif eachCacheFile.find(".xml") >= 0 and eachCacheFile.find("hair_cache") >= 0:
            newEachCacheFile = eachCacheFile.replace("\\", "/")
            hairCacheFileXML.append(newEachCacheFile)
    
    if cacheFlag == "cloth":
        return clothCacheFileXML
    elif cacheFlag == "hair":
        return hairCacheFileXML

def DFS_Dir(path, dirCallback = None, fileCallback = None):
    """深度优先遍历文件路劲下的酥油文件/文件夹"""
    stack = []  
    ret = []  
    stack.append(path);  
    while len(stack) > 0:  
        tmp = stack.pop(len(stack) - 1)  
        if(os.path.isdir(tmp)):  
            ret.append(tmp)  
            for item in os.listdir(tmp):  
                stack.append(os.path.join(tmp, item))  
            if dirCallback:  
                dirCallback(tmp)  
        elif(os.path.isfile(tmp)):  
            ret.append(tmp)  
            if fileCallback:  
                fileCallback(tmp)  
    return ret  
#--------------------------------------------attachAll窗体执行end------------------------------------------------------