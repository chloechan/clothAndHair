#-*- coding: utf-8-*-#
import os
import shutil

import maya.cmds as cmds
import maya.mel as mel

import tools.clothAndHairTools
import tools.commonTools

cT = tools.commonTools.CommonTools()  #实例化CommanTools类
clothHairT = tools.clothAndHairTools.ClothAndHairTools()  #实例化ClothAndHairTools类

class CacheManagment():
    """解算时缓存管理类

    Description:
        5、生成布料缓存、毛发缓存，删除布料缓存、毛发缓存，关联布料缓存、毛发缓存

    Attributes:
        无
    """  
    def __init__(self):
        pass
    
    def createNCache(self):
        """创建n缓存"""
        if clothHairT.checkSelHair():
            nHairCacheDir = getCacheFoldDir(2)  #拿到nCache存放路径
            if nHairCacheDir:
                createCacheWin(2, nHairCacheDir)  #若路径正确则调用生成nCache的窗口
                    
    def createGeoCache(self):
        """创建geo缓存"""
        if clothHairT.checkSelObj():  #若符合，则选择物体不变
            geoCacheDir = getCacheFoldDir(1) #拿到geoCache存放路径
            if geoCacheDir:                            
                createCacheWin(1, geoCacheDir)
        
    def deleteNCache(self):
        """删除n缓存"""
        if clothHairT.checkSelHair():
            deleteHairNCacheP()
               
    def deleteGeoCache(self):
        """删除geo缓存"""
        if clothHairT.checkSelObj():  #若符合，则选择物体不变
            deleteGeoCacheP()
                
    def attachNCache(self):
        """指认n缓存"""
        if clothHairT.checkSelHair():
            attachNCacheP()
        
    def attachGeoCache(self):
        """指认geo缓存"""
        if clothHairT.checkSelObj():  #若符合，则选择物体不变
            attachGeoCacheP()  


def getCacheFoldDir(cacheFlag):
    """拿到缓存应存放的文件夹路径

    Description:
        缓存文件存放路径由maya文件所在文件夹决定
                
    Arguments:
        cacheFlag： cacheFlag = 1 : clothGeoCache
                    cacheFlag = 2 : hairCache

    Returns:
        None:若文件没有保存到硬盘则返回空值
        nClothCacheDirApartA：缓存存放的文件夹路径
    """
    mayaFileDir = cmds.file(query = True, loc = True)
    if mayaFileDir == "unknown":
        cmds.confirmDialog(title = "Warning", message = "Please Save This File!", button = "OK", defaultButton = "OK")
        return None
    else:
        (upFileDir,fileName) = mayaFileDir.rsplit("/", 1)  #文件所在的文件夹名
        
        cacheDirMidA = "/nCache/"
    
        camId = fileName.rsplit(".")[0]  #镜头号

        longName = cmds.ls(sl = True, long = True)[0]  #拿到该物体所在组的命名空间
        charName = longName.split("|")[1].split(":")[0]  #若物体在跟目录下，则为该物体名
        
        if cacheFlag == 1:
            cacheDirMidB = "/cloth_cache/temp/"
        elif cacheFlag == 2:
            cacheDirMidB = "/hair_cache/temp/"
            
        cacheFoldDir = upFileDir + cacheDirMidA + camId + "/solCache/" + charName + cacheDirMidB

        finalCacheFold = ""
        if os.path.exists(cacheFoldDir):
            tempFileList = []        
            tempFileList = cT.getFileListFromAPath(cacheFoldDir, tempFileList)
            
            
            if not tempFileList:
                finalCacheFold = cacheFoldDir + "temp_1/"
            else:
                indexList = []
                for eachTempFile in tempFileList:
                    tempIndex = eachTempFile.split("_")[1]
                    indexList.append(int(tempIndex))
                indexList.sort()
                latestIndex = indexList[-1] + 1
                finalCacheFold = cacheFoldDir + "temp_" + str(latestIndex) + "/"
        else:
            finalCacheFold = cacheFoldDir + "temp_1/"
                    
        return finalCacheFold


def createCacheWin(cacheFlag, cacheDir):
    """创建缓存窗体

    Description:
        无
        
    Arguments:
        cacheFlag： cacheFlag = 1 : clothGeoCache
                    cacheFlag = 2 : hairCache
        cacheDir：缓存路径

    Returns:
        无
    """
    if cacheFlag == 1:
        cacheflagName = "Cloth"
    elif cacheFlag == 2:
        cacheflagName = "Hair"
    
    cacheFlag = str(cacheFlag)  #将int型转化为str型,便于command的参数传递
    
    winTitle = "Create " + cacheflagName + " Cache"
    cacheWindow = cmds.window(title = winTitle, iconName = "CC", widthHeight = (420, 100))
    
    cCFormLayout = cmds.formLayout()
    textRowLayout = cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(1, 100), (2, 280)], rowSpacing = (1, 4))
    cacheDirText = cmds.text(label="Cache Directory: ")
    cacheDirTextField = cmds.textField(text = cacheDir, editable = False)
    cmds.setParent("..")
    cCButtonRowLayout = cmds.rowLayout(numberOfColumns = 2, columnAttach = [(1, "right", 0),(2, "right", 0)], columnWidth=[(1, 280), (2, 80)])
    cmds.button(label = "Create", width = 75, command = lambda x:createCacheP(cacheWindow, cacheDir, cacheFlag))
    cmds.button(label = "Close", width = 75,  command=('cmds.deleteUI(\"' + cacheWindow + '\", window=True)'))
    cmds.setParent("..")
    cmds.formLayout(cCFormLayout, edit=True, 
                        attachForm=[(textRowLayout, "top", 12), (textRowLayout, "left", 8), (textRowLayout, "right", 8),
                                    (cCButtonRowLayout, "bottom", 12),(cCButtonRowLayout, "left", 24), (cCButtonRowLayout, "right", 24)], 
                        attachControl=[(cCButtonRowLayout, "top", 12, textRowLayout)])
    cmds.setParent("..")
    
    cmds.showWindow(cacheWindow)


def createCacheP(cacheWindow, cacheDir, cacheFlag):
    """调用mel命令创建缓存
    Description:
        根据cache的不同创建不同的缓存

    Arguments:
        cacheWindow:窗体名（用于关闭窗体）
        cacheDir：缓存存放路径
        cacheFlag: cacheFlag = 1 : clothGeoCache
                    cacheFlag = 2 : hairCache

    Returns:
        无
    """
    cacheFlag = int(cacheFlag)
    
    #若文件夹已经存在，则不做任何操作，若不存在则创建文件夹
    if os.path.exists(cacheDir):
        pass
    else:
        os.makedirs(cacheDir)
        
    if cacheFlag == 1:  #创建几何体缓存
        deleteGeoCacheP()
        mel.eval('doCreateGeometryCache 6 { "2", "1", "10", "OneFile", "1", "%s","1","","0", "add", "0", "1", "1","0","1","mcc","0" }'%cacheDir)
        renameGeoCacheFile(cacheDir)
    
    elif cacheFlag == 2:    #创建毛发缓存
        deleteHairNCacheP()
        mel.eval('doCreateNclothCache 4 {"2", "1", "10", "OneFile", "1", "%s","1","","0", "add", "0", "1", "1","0","1" }'%cacheDir) 
        renameHairNCacheFile(cacheDir)
    
    cmds.deleteUI(cacheWindow, window=True)

def renameGeoCacheFile(cacheDir):
    """重命名geo缓存文件"""
    #生成geoCache后会自动选择选择物体的shape节点（不带布料）或output节点（带布料）
    clothHairT.selShapeToMesh()  #由shape节点或output节点去选择与之相连的mesh节点
    
    objName = cmds.ls(sl = True, type = "transform")
    
    fileList = []
    fileList = cT.getFileListFromAPath(cacheDir, fileList)  #拿到指定路径的所有文件列表
    
    for eachObj in objName:            
        cacheName = ""
        if len(getGeoCacheFromObj(eachObj)) == 1:
            cacheName = getGeoCacheFromObj(eachObj)[0]  #拿到新生成的geoCache节点名
            print cacheName
        elif len(getGeoCacheFromObj(eachObj)) > 1:
            #若含有多个geoCache（除了新生成的，原来就有geoCache）
            cacheNodeList = getGeoCacheFromObj(eachObj)
            print cacheNodeList
            for eachCacheNode in cacheNodeList:
                eachCacheNodeEnable = cmds.getAttr(eachCacheNode + ".enable")
                if eachCacheNodeEnable == 1:  #新生成的enable属性为1，其他的为0
                    cacheName = eachCacheNode
            
        oldCacheName = cmds.getAttr(cacheName + ".cacheName")  #拿到新生成的缓存文件名
        oldCacheFileMC = oldCacheName + ".mc"  
        oldCacheFileXML = oldCacheName + ".xml"
        
        newCacheDir = cacheDir.rsplit("/", 3)[0] + "/"
        newCacheName = getCacheFileName(eachObj, newCacheDir)   #拿到最终缓存文件名
        newCacheFileMC = newCacheName + ".mc"
        newCacheFileXML =newCacheName + ".xml"
        
        for eachFile in fileList:
            if eachFile == oldCacheFileMC:
                shutil.copyfile(cacheDir + oldCacheFileMC, newCacheDir + newCacheFileMC)  #复制缓存文件.mc                
            elif eachFile == oldCacheFileXML:
                shutil.copyfile(cacheDir + oldCacheFileXML, newCacheDir + newCacheFileXML)  #复制缓存文件.xml
        
        cmds.setAttr(cacheName + ".cachePath", newCacheDir, type = "string")                             
        cmds.setAttr(cacheName + ".cacheName", newCacheName, type = "string")


def renameHairNCacheFile(cacheDir):
    """重命名n缓存文件"""
    hairShapes = cmds.ls(sl = True)
    
    fileList = []
    fileList = cT.getFileListFromAPath(cacheDir, fileList)  #拿到指定路径的所有文件列表
        
    for eachHairShape in hairShapes:
        if len(getHairCacheFromShape(eachHairShape)) == 1:
            #有一个缓存
            hairCacheName = getHairCacheFromShape(eachHairShape)[0]
            print hairCacheName
        elif len(getHairCacheFromShape(eachHairShape)) > 1:
            #有多个缓存
            hairCahceList = getHairCacheFromShape(eachHairShape)
            print hairCahceList
            for eachHairCache in hairCahceList:
                eachHairCacheEnable = cmds.getAttr(eachHairCache + ".enable")
                if eachHairCacheEnable == 1:  #新生成的enable属性为1，其他的为0
                    hairCacheName = eachHairCache
        
        oldCacheName = cmds.getAttr(hairCacheName + ".cacheName")
        oldCacheFileMC = oldCacheName + ".mc"  
        oldCacheFileXML = oldCacheName + ".xml"
        
        newCacheDir = cacheDir.rsplit("/", 3)[0] + "/"
        newCacheName = getCacheFileName(eachHairShape, newCacheDir)   #拿到最终缓存文件名
        newCacheFileMC = newCacheName + ".mc"
        newCacheFileXML =newCacheName + ".xml"
        
        for eachFile in fileList:
            if eachFile == oldCacheFileMC:
                shutil.copyfile(cacheDir + oldCacheFileMC, newCacheDir + newCacheFileMC)  #复制缓存文件.mc
            elif eachFile == oldCacheFileXML:
                shutil.copyfile(cacheDir + oldCacheFileXML, newCacheDir + newCacheFileXML)  #复制缓存文件.xml
        
        cmds.setAttr(hairCacheName + ".cachePath", newCacheDir, type = "string")        
        cmds.setAttr(hairCacheName + ".cacheName", newCacheName, type = "string")
    

def getCacheFileName(objName, cacheDir):
    """拿到所选择物体的名称并加后缀序列号，以此作为缓存名

    Description:
        拿到所选物体的名称，在相应的文件目录下搜索该物体的当前最大的序列号，合成最终物体名
                
    Arguments:
        objName：物体名
        cacheDir：缓存存放路径

    Returns:
        cacheName：带有序列号后缀的物体名
    """
    if objName.find(":") >= 0:
        objNameNew = objName.replace(":", "__")  #由于系统命名不能带“：”，所以将“：”替换为“__”
    else:
        objNameNew = objName
  
    cacheIndex = int(checkCacheIndex(objNameNew, cacheDir)) + 1
    cacheFileName = objNameNew + "___" + str(cacheIndex)
    return cacheFileName

def checkCacheIndex(objName, cacheDir):
    """拿到指定目录下的指定物体的最大序列号

    Description:
        若文件夹下没有指定物体的缓存文件，则当前最大序列号为0
        若文件夹下有指定物体的缓存文件，则选择最大的序列号返回
                
    Arguments:
        objName：物体名
        cacheDir：缓存存放路径

    Returns:
        latestIndex：某文件夹下的最大序列号
    """
    fileList = []
    fileList = cT.getFileListFromAPath(cacheDir, fileList)
    if not fileList:
        return 0
    else:
        cacheIndexlist = []
        #取得某物体的文件的序列号并存入序列号列表
        for eachFile in fileList:
            if eachFile.rsplit("___", 1)[0] != eachFile:  #若存在可分的文件
                (fileNameWithoutId, cacheIndexTemp) = eachFile.rsplit("___", 1)
                (cacheIndex,other) = cacheIndexTemp.rsplit(".",1)
                if fileNameWithoutId == objName:
                    cacheIndexlist.append(int(cacheIndex))
        
        if not cacheIndexlist:
            return 0
        else:
            cacheIndexlist.sort()  #对存放序列号的列表进行排序
            latestIndex = cacheIndexlist[-1]
            return latestIndex  #返回最大的序列号

def deleteHairNCacheP():
    """删除所有所选物体的所有nCache

    Description:
        若所选物体都含有nCache，则全都删除
        若所选物体中有一个不含nCache，则提示
                
    Arguments:
        无

    Returns:
        无
    """
    hairShapeList = cmds.ls(sl = True)
    
    for eachHairShape in hairShapeList:
        if len(getHairCacheFromShape(eachHairShape)) >= 1:
            nCacheNodes = getHairCacheFromShape(eachHairShape)
            for eachNCacheNode in nCacheNodes:
                mel.eval('deleteCacheFile 2 {"keep", "%s"}'%eachNCacheNode)
        else:
            pass

def deleteGeoCacheP():
    """删除所有所选物体的所有geoCache

    Description:
        若所选物体都含有geoCache，则全都删除
        若所选物体中有一个不含geoCache，则提示
                
    Arguments:
        无

    Returns:
        无
    """
    objName = cmds.ls(sl = True)

    for eachObj in objName:
        if len(getGeoCacheFromObj(eachObj)) >= 1:
            geoCacheNodes = getGeoCacheFromObj(eachObj)
            for eachGeoCacheNode in geoCacheNodes:
                mel.eval('deleteCacheFile 2 {"keep", "%s"}'%eachGeoCacheNode)
        else:
            pass


def getHairCacheFromShape(hairShapeName):
    """根据hairSystemShape节点拿到该节点相连的缓存列表

    Description:
        若存在缓存（一个或多个），返回缓存节点列表；若不存在缓存，返回空
                
    Arguments:
        hairShapeName：hairSystemShape节点名
        
    Returns:
        hairCacheList：缓存节点名列表
    """
    isCacheBlend = cmds.listConnections(hairShapeName, type = "cacheBlend")
    
    if isCacheBlend:  #存在多个缓存
        hairCacheList = cT.delDupFromList(cmds.listConnections(isCacheBlend, type = "cacheFile"))
    else:
        hasCache = cmds.listConnections(hairShapeName, type = "cacheFile")
        if hasCache:
            hairCacheList = cT.delDupFromList(cmds.listConnections(hairShapeName, type = "cacheFile"))
        else:
            hairCacheList = []
    
    return hairCacheList


def getGeoCacheFromObj(objName):
    """根据物体名拿到该物体相连的缓存列表

    Description:
        若存在缓存（一个或多个），返回缓存节点列表；若不存在缓存，返回空
                
    Arguments:
        objName：物体名
        
    Returns:
        cacheNodes：缓存节点列表
    """
    cacheNodesList = clothHairT.getCacheNodes()  #拿到所有的cacheNode
    cacheNodes = []
    if cacheNodesList:
        for eachCacheNode in cacheNodesList:
            isGeoCache = cmds.cacheFile(eachCacheNode, query=True, geometry=True)
            if isGeoCache:  #为geoCache,不是hairCache
                shapeWithCache = cmds.cacheFile(eachCacheNode, query=True, geometry=True)
                objWithCache = cmds.listRelatives(shapeWithCache[0], parent = True)  #拿到该cache的物体名
                if objWithCache[0] == objName:
                    cacheNodes.append(eachCacheNode)
    return cacheNodes   

def attachNCacheP():
    mel.eval('attachNclothCache')

def attachGeoCacheP():
    mel.eval('attachGeometryCache')