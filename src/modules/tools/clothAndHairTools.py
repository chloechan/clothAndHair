#-*- coding: utf-8-*-#

from xml.dom.minidom import parse

import maya.cmds as cmds

import commonTools

cT = commonTools.CommonTools()  #实例化CommanTools类



class ClothAndHairTools():
    """布料毛发解算插件的工具类

    Description:
        该类包括一些各个模块重复用到的方法

    Attributes:
        无
    """
    def __init__(self):
        pass
             
    def checkSelMulti(self, flag):
        """检查所选的多个物体是否都为目标物体
    
        Description:
            若所选的对象都是需要选择的，则保持原有选择（若需要选择的是布料，则无论选择的是带布料的物体还是布料节点，都会选择成布料节点）
            若所选的对象只要有一个不是需要选择的对象，则显示提示信息且取消所有选择
    
        Arguments:
            flag：为0，需要选择的是普通物体，若不是则显示提示信息
            flag：为1，需要选择的是带布料的物体或布料节点，若不是则显示提示信息，若是，则选择它的布料节点
    
        Returns:
                        无
        """   
        selObjs = cmds.ls(sl = True)
        if not selObjs:
            cmds.confirmDialog(title = "Warning", message = "Please Select Objects!", button = "OK", defaultButton = "OK")
        else:
            for eachObj in selObjs:
                eachSelType = cmds.nodeType(eachObj)
                
                if flag == 1 and eachSelType == "transform":
                    shapeName = cmds.listRelatives(eachObj, shapes = True)  #拿到obj物体的shape节点
                    isCloth = []
                    for eachShape in shapeName:
                        isClothTemp = cmds.listConnections(eachShape, type = "nCloth")  #判断所选物体是否为布料
                        if isClothTemp:
                            isCloth.append(isClothTemp[0])
                    if not isCloth:
                        cmds.confirmDialog(title = "Warning", message = "There Has An Object Not Connected With Cloth!", button = "OK", defaultButton = "OK")
                        cmds.select(deselect = True)  #去除所有选择
                        break
                    else:
                        cmds.select(eachObj, deselect = True)  #取消选择transform节点
                        nClothName = cT.delDupFromList(isCloth)  #若物体为布料物体则拿到布料的shape节点
                        nClothShapeName = cmds.listRelatives(nClothName[0], shapes = True)
                        cmds.select(nClothShapeName[0], add = True)  #选择布料shape节点
                
                elif flag == 1 and eachSelType == "nCloth":
                    pass
                
                elif flag == 0 and eachSelType == "transform":
                    shapeName = cmds.listRelatives(eachObj, shapes = True)  #拿到obj物体的shape节点
                    isCloth = []
                    for eachShape in shapeName:
                        isClothTemp = cmds.listConnections(eachShape, type = "nCloth")  #判断所选物体是否为布料
                        if isClothTemp:
                            isCloth.append(isClothTemp[0])
                    if isCloth:
                        cmds.confirmDialog(title = "Warning", message = "There Has An Object Connected With Cloth!", button = "OK", defaultButton = "OK")
                        cmds.select(deselect = True)  #去除所有选择
                        break
                    else:
                        pass
                        
                else:
                    cmds.confirmDialog(title = "Warning", message = "There Has An Object With Incorrect Type!", button = "OK", defaultButton = "OK")
                    cmds.select(deselect = True)  #去除所有选择
                    break   
            
    def selNClothShapeToMesh(self):
        """由所选择nClothShape节点去选择与其相连的mesh节点
    
        Description:
            由所选择nClothShape节点去选择与其相连的mesh节点择
    
        Arguments:
            无
    
        Returns:
            无
        """   
        nClothShapeName = cmds.ls(sl = True)
        for eachNClothShapeName in nClothShapeName:
            isMesh = cmds.listConnections(eachNClothShapeName, type = "mesh")
            if not isMesh:
                cmds.confirmDialog(title = "Warning", message = "This NClothShape Node Dosn't Connected With Object!", button = "OK", defaultButton = "OK")
                cmds.select(deselect = True)  #去除所有选择
                break
            else:
                cmds.select(eachNClothShapeName, deselect = True)
                objName = cT.delDupFromList(cmds.listConnections(eachNClothShapeName, type = "mesh"))
                cmds.select(objName[0], add = True)
    
    def selShapeToMesh(self):
        """由shape节点去选择与之相连的mesh节点
    
        Description:
            由shape节点去选择与之相连的mesh节点
    
        Arguments:
            无
    
        Returns:
            无
        """ 
        shapeName = cmds.ls(sl = True)
        for eachShape in shapeName:
            cmds.select(eachShape, deselect = True)
            objName = cmds.listRelatives(eachShape, parent = True)
            cmds.select(objName[0], add = True)
                        
    def checkSelHair(self):
        """检查是否选择了HairSystem节点
    
        Description:
            检查是否选择了HairSystem节点
    
        Arguments:
            若没有选择或选择的类型不正确，都返回False；当选择的节点都是hairSystem类型时，则返回True
    
        Returns:
            result:result = True：选择节点的类型正确
                result = False：选择节点的类型不正确
        """ 
        selName = cmds.ls(sl = True)
        result = True
        if not selName:
            result = False
        else:
            for eachSel in selName:
                if cmds.nodeType(eachSel) == "hairSystem":
                    pass
                else:
                    print "This Is Not A HairSystemShape Node!"
                    result = False
                    break
        return result
        
    def checkSelObj(self):
        """检查选中的物体是否为mesh节点
    
        Description:
            选有物体且所选的是mesh节点，返回True
            没选物体或所选物体类型不符合，则返回False
    
        Arguments:
            无
    
        Returns:        
            result = True：通过检查
            result = False：没通过检查，释放所有选择
        """
        selObj = cmds.ls(sl =True)
        lenOfSel = len(selObj)
        result = True
        if lenOfSel < 1:
            cmds.confirmDialog(title = "Warning", message = "Please Select Objects!", button = "OK", defaultButton = "OK")
            result = False
        else:
            for eachObj in selObj:
                if cmds.nodeType(eachObj) != "transform":
                    cmds.confirmDialog(title = "Warning", message = "There Has An Object With Incorrect Type!", button = "OK", defaultButton = "OK")
                    cmds.select(deselect = True)  #去除所有选择
                    result = False
                    break
        
        return result
        
            
    #fileDir = "F:/test/YC_Char_RG_Hi__head_hairSystemShape.xml"    
    
    def readXMLToGetSEFrame(self, fileDir):
        """读取xml文件的开始帧与结束帧
    
        Description:
            读取xml文件的开始帧与结束帧
    
        Arguments:
            fileDir：xml文件的路径
    
        Returns:
            startFrame：开始帧数
            endFrame：结束帧数
            
        """ 
        doc=parse(fileDir)
        timeAttr = ""
        timePerFrameAttr = ""
        for timeNode in doc.getElementsByTagName("time"):  #拿到便签time的属性值，即开始时间与结束时间
            timeAttr = timeNode.getAttribute("Range") 
        (srartTime, endTime) = timeAttr.split("-")
        for timeNode in doc.getElementsByTagName("cacheTimePerFrame"):  #拿到便签cacheTimePerFrame的属性值
            timePerFrameAttr = timeNode.getAttribute("TimePerFrame")
        
        startFrame = int(srartTime)/int(timePerFrameAttr)
        endFrame = int(endTime)/int(timePerFrameAttr)
        return (startFrame, endFrame)
        


        
    def getCacheNodes(self):
        """拿到场景中所有的cache节点
    
        Description:
            若场景中含有缓存节点，则返回所有的缓存节点列表
            若不含缓存节点，则返回空列表
                    
        Arguments:
            无
    
        Returns:
            targetCacheNodes：缓存节点列表
        """ 
        allCacheNodes = cmds.ls(dag=True, ap=True, type = "cacheFile")
        
        targetCacheNodes = []  #存放文件中所有缓存节点名
        for eachCacheNodes in allCacheNodes:
            if cmds.nodeType(eachCacheNodes) == "cacheFile":
                targetCacheNodes.append(eachCacheNodes)
        
        return targetCacheNodes

