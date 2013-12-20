#-*- coding: utf-8-*-#
import maya.cmds as cmds
import maya.mel as mel

import tools.commonTools
import tools.clothAndHairTools
import mainWindow
cT = tools.commonTools.CommonTools()  #实例化CommanTools类
clothHairT = tools.clothAndHairTools.ClothAndHairTools()  #实例化ClothAndHairTools类

class ResolvingTools():
    """解算工具类

    Description:
        4、解算工具模块

    Attributes:
        无
    """
    def __init__(self):
        pass
    
    def makeConstraint(self):
        nConstraintType = cmds.optionMenu(mainWindow.nConsOptMenu, query = True, value = True)

        if nConstraintType == "point to surface":
            mel.eval("createNConstraint pointToSurface 0")
        elif nConstraintType == "component to component":
            mel.eval("createNConstraint pointToPoint 0")
        elif nConstraintType == "transform":
            mel.eval("createNConstraint transform 0") 
        elif nConstraintType == "slide on surface":
            mel.eval("createNConstraint slideOnSurface 0")
                        
    def makeCollide(self):
        clothHairT.checkSelMulti(0)  #检测所选的物体是否都符合要求
        selObj = cmds.ls(sl = True)
        lenOfSel = len(selObj)  
        if lenOfSel >= 1:  #选中一个或多个非布料物体
            createCollideWindow()
        
    def paintMesh(self):
        mel.eval('setNClothMapType("inputAttract","",1)')
        mel.eval("artAttrNClothToolScript 4 inputAttract")
    
    def callRepairTools(self):
        repairType = cmds.optionMenu(mainWindow.repairOptMenu, query = True, value = True)
        
        if repairType == "weights painting":
            createBlendShapeToolWin()
        elif repairType == "points moving":
            print "doing now!"
        
#------------------------------------创建碰撞start-----------------------------------------
def createCollideWindow():
    makeCollideWin = cmds.window(title = "Create NCloth", iconName = "CN", widthHeight = (420, 80))
    mCFormLayout = cmds.formLayout()
    nucleusButton  = mel.eval('nucleusSolverButton("")')
    cmds.optionMenuGrp(nucleusButton, edit = True, cw = [1,50])
    mCButtonRowLayout = cmds.rowLayout(numberOfColumns = 2, columnAttach = [(1, "right", 0),(2, "right", 0)], columnWidth=[(1, 280), (2, 80)])
    makeColButton = cmds.button(label = "Make Collide", width = 75, command = (lambda x:doMakeCollide(makeCollideWin)))
    closeButton = cmds.button(label = "Close", width = 75, command = ('cmds.deleteUI(\"' + makeCollideWin + '\", window=True)'))
    cmds.setParent("..")
    cmds.formLayout(mCFormLayout, edit=True,
                    attachForm=[(nucleusButton, "top", 12), (nucleusButton, "left", 8), (nucleusButton, "right", 8),
                                (mCButtonRowLayout, "bottom", 12),(mCButtonRowLayout, "left", 24), (mCButtonRowLayout, "right", 24)], 
                    attachControl=[(mCButtonRowLayout, "top", 12, nucleusButton)])
    cmds.setParent("..")
    cmds.showWindow(makeCollideWin)

def doMakeCollide(makeCollideWin):
    mel.eval("makeCollideNCloth")
    cmds.deleteUI(makeCollideWin, window=True)    
#------------------------------------创建碰撞end-----------------------------------------
#------------------------------------blendshape工具start-----------------------------------------
def createBlendShapeToolWin():
    """创建主窗口"""
    blendShapeToolWin = cmds.window( title="BlendShape Tool", iconName='BT', widthHeight=(240, 170) )
    bSToolFormLayout = cmds.formLayout()
    bSToolColumnLayout = cmds.columnLayout( adjustableColumn=True ,rowSpacing = 4)
    cmds.button( label='1.  Duplicate Mesh',command = (lambda x:duplicateMesh()))
    cmds.button( label='2.  Import Cache...' ,command = (lambda x:importCache()))
    cmds.button( label='3.  Blend Shape',command = (lambda x:selectTwoObj()))
    cmds.separator( height=10, style='in' )
    cmds.button( label='4.  Paint Blend Shape Weight',command = (lambda x:openPaintBlendShapeWeightsTool()) )
    cmds.button( label='Close', command=('cmds.deleteUI(\"' + blendShapeToolWin + '\", window=True)') )
    cmds.setParent( '..' )
    cmds.formLayout(bSToolFormLayout, edit=True,
                    attachForm=[(bSToolColumnLayout, "top", 12), (bSToolColumnLayout, "left", 8),(bSToolColumnLayout, "right", 8), (bSToolColumnLayout, "bottom", 8)])    
    cmds.setParent("..")
    
    cmds.showWindow( blendShapeToolWin )
    
def duplicateMesh():
    """复制选中的模型"""
    #选择一个物体并获得物体名与命名空间
    selectObj = cmds.ls(sl=1,long = True) 
    
    if(selectObj == []):
        cmds.warning( "please select an object!") 
    else:        
        objFullName = selectObj[0]#得到物体的完整路劲名
        print objFullName
        objNamespace = cmds.ls(sl=1,showNamespace = True)[1]#获得所选物体的命名空间
        print objNamespace
        
        
        #复制带有命名空间的模型
        cmds.namespace(set=":%s"%objNamespace)#设置当前命名空间    
        objCopy = cmds.duplicate("%s"%objFullName,rr = True)[0]#复制出来的物体名为完整路径名
        print objCopy    
        cmds.select("%s"%objCopy,r = True)#选择复制出的模型(此句可以省略)
        
        #重命名为“原名+_Copy”
        objCopyRename = objFullName+"_Copy"
        print objCopyRename    
        cmds.rename("%s"%objCopy,"%s"%objCopyRename)

def importCache():
    """导入缓存"""
    mel.eval("attachGeometryCache")
    
def selectTwoObj():
    """根据已选的物体加选另一个物体，做blendShape"""
    selectObj = cmds.ls(sl=1,long = True)
    print selectObj
    objFullName = selectObj[0]
    print objFullName
    
    (otherLongInfo, targetName) =  selectObj[0].rsplit(":",1)#获得targetName(短命，不带命名空间)，用于blendShape的权重设置
    print targetName
    
    #如果所选的物体以“_Copy”结尾，则执行以下内容
    if(objFullName.endswith("_Copy")):
        (baseObjName,copyFlag) = objFullName.rsplit("_Copy",1)#去掉名称最后的"_Copy"
        print baseObjName    
        cmds.select("%s"%baseObjName,add=True)#加选去除“_Copy”的物体
        
        blendShapeName = cmds.blendShape()#创建blendShape
        print blendShapeName
    
        cmds.setAttr("%s.%s"%(blendShapeName[0],targetName),1)#将权重设置为1
        cmds.hide("%s"%objFullName)#隐藏targetObj
        cmds.select("%s"%baseObjName,r = True)#选择baseObj（此句可以省略）
    else:
        cmds.warning( "Can not create a blendShape now!") 
    
def openPaintBlendShapeWeightsTool():
        """打开刷blendShape的工具"""
        mel.eval("ArtPaintBlendShapeWeightsToolOptions")
        
#------------------------------------blendshape工具end-----------------------------------------