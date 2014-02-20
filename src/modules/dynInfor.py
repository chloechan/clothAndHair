#-*- coding: utf-8-*-#
import maya.cmds as cmds

import tools.commonTools
import mainWindow

cT = tools.commonTools.CommonTools()  #实例化CommanTools类

class DynInfor():
    """解算相关信息显示类

    Description:
        1、显示场景中的角色名、解算器、相关节点信息

    Attributes:
        无
    """    
    
    def __init__(self):
        pass
    
    def getCharsName(self):
        """将场景中的角色名显示到窗体角色名列表中
    
        Description:
            1、搜索场景中的所有角色名
            2、将角色名显示到对应窗体
    
        Arguments:
            无
    
        Returns:
            无
        """
        charsNameList = searchCharsName()
        showListInWin(charsNameList, mainWindow.charsScrollList)
      
    def getNucleusName(self):
        """将场景中的解算器信息显示到窗体解算器显示列表中
    
        Description:
            1、搜索场景中的所有解算器信息
            2、将所有解算器信息显示到对应窗体
    
        Arguments:
            无
    
        Returns:
            无
        """
        nucleusList = searchNucleusName() 
        showListInWin(nucleusList, mainWindow.nucleusScrollList)
    
    def getNodesFromNu(self):
        """将与某个解算器相关的目标节点显示到窗体的目标节点列表中
    
        Description:
            1、拿到解算器名
            2、选中该解算器节点
            3、根据解算器名查找相关联的目标节点名
            4、将目标节点名显示到窗体
    
        Arguments:
            无
    
        Returns:
            无
        """
        #若存在解算器则显示目标节点列表，若不存在则显示提示信息
        oneNucleusInfo = cmds.textScrollList(mainWindow.nucleusScrollList, query = True, selectItem = True)
        if oneNucleusInfo[0] == "There Has No Elements!":    
            cmds.textScrollList(mainWindow.nDynNodesScrollList, edit = True, removeAll = True)
            cmds.textScrollList(mainWindow.nDynNodesScrollList, edit = True, append = "There Has No Elements!")
        else:
            (oneNucleusName, other) = oneNucleusInfo[0].split(" ----- ", 1)
            
            cmds.select(oneNucleusName, replace = True)
            
            targetNodesList = searchTargetNodes(oneNucleusName)
            
            showListInWin(targetNodesList, mainWindow.nDynNodesScrollList)
       
    def selShapeFromNode(self):
        """选中某个目标节点的shape节点
    
        Description:
            1、拿到节点名
            2、选中该节点的shape节点
    
        Arguments:
            无
    
        Returns:
            无
        """
        #若不存在目标节点，则显示提示信息，若存在则选中目标节点的shape节点        
        cmds.select(deselect = True)  #去除所有选择
        nodesList = cmds.textScrollList(mainWindow.nDynNodesScrollList, query = True, selectItem = True)
        if len(nodesList) >= 1:
            if nodesList[0] == "There Has No Elements!":
                print "There Has No Elements!"
            else:
                for eachNode in nodesList:
                    oneShapeNodeName = cmds.listRelatives(eachNode, shapes = True)            
                    cmds.select(oneShapeNodeName[0], add = True)
    
    def refreshAll(self):
        """刷新模块一
        Description:
            1、刷新角色名列表
            2、刷新解算器列表
            3、清空目标节点列表
    
        Arguments:
            无
    
        Returns:
            无
        """    
        self.getCharsName()
        self.getNucleusName()
        cmds.textScrollList(mainWindow.nDynNodesScrollList, edit = True, removeAll = True)
        cmds.text(mainWindow.cPreText, edit = True, label = "xxxxxxxxxx 's presets:") 
        cmds.textScrollList(mainWindow.cPreScrollList, edit = True, removeAll = True)

def searchCharsName():
    """检索当前场景中的所有角色名

    Description:
        根据绑定文件的命名规范与reference原则，从命名空间中就可获得角色名称

    Arguments:
        无

    Returns:
        allCharsNameList：所有角色名列表(无重复)
    """
    cmds.namespace(set = ":")
    allNamespace = cmds.namespaceInfo(listOnlyNamespaces = True)  #拿到所有根目录下的命名空间名称
    allCharsName = []
    
    for eachNamespace in allNamespace:
        #拿到带有_Char_的命名空间名称，从中拿到角色名
        
        if eachNamespace.find("_chr_") < 0:
            print "This Is Not A Char!"            
        else:
            namesapceWithChar = eachNamespace
            charName = namesapceWithChar.split("_")[2]  #charName存放角色名
            allCharsName.append(charName)

    allCharsNameList = cT.delDupFromList(allCharsName)  #调用函数去除list中的重复元素
    
    return allCharsNameList

def showListInWin(listForShow,tSLName):
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

def searchNucleusName():
    """检索当前场景中的所有解算器信息

    Description:
        拿到所有解算器的名称与各个解算器的开关状态

    Arguments:
        无

    Returns:
        allNucleusList：所有计算器信息列表
    """
    allNuName = cmds.ls(type = "nucleus") #拿到场景中的所有解算器
    allNucleus = []
    
    for eachNuName in allNuName:
        #拿到每一个解算器的开关状态，即enable属性值
        if cmds.getAttr(eachNuName + ".enable") == True:
            eachNuEnable = "On"
        else:
            eachNuEnable = "Off"
            
        eachNuNameWithEnable = eachNuName + " ----- " + eachNuEnable  #将解算器名与开关属性字符串组合
        allNucleus.append(eachNuNameWithEnable)
        
    allNucleusList = allNucleus
    return allNucleusList

def searchTargetNodes(oneNucleusName):
    """根据解算器名查找相关联的目标节点名

    Description:
        目标节点包括nCloth节点、nRigid节点、hairSystem节点
        
    Arguments:
        oneNucleusName：某个解算器名

    Returns:
        targetNodes：目标节点名列表
    """    
    nClothListTemp = cmds.listConnections(oneNucleusName, type = "nCloth")  #拿到某个解算器相关的nCloth节点名
    nRigidListTemp = cmds.listConnections(oneNucleusName, type = "nRigid")  #拿到某个解算器相关的nRigid节点名
    hairListTemp = cmds.listConnections(oneNucleusName, type = "hairSystem")  #拿到某个解算器相关的hairSystem节点名
    
    #检查listConnections的返回值是否为NoneType，若是，则将其转化为空列表
    if not nClothListTemp:
        nClothListTemp = []
    if not nRigidListTemp:
        nRigidListTemp = []
    if not hairListTemp:
        hairListTemp = []
        
    #检查listConnections的返回值列表是否有重复元素，若有，则删除重复值    
    nClothList = cT.delDupFromList(nClothListTemp)
    nRigidList = cT.delDupFromList(nRigidListTemp)
    hairList = cT.delDupFromList(hairListTemp)
    
    nClothAndHairListTemp = nClothList + hairList  #存放不带后缀的shape节点
    nClothAndHairList = []  #存放带后缀的shape节点
    
    for eachNode in nClothAndHairListTemp:
        nClothAndHairList.append(eachNode )
        
    targetNodes = nClothAndHairList + nRigidList  #所有目标节点名列表
    return targetNodes    

