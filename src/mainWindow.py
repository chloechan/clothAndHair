#-*- coding: utf-8-*-#
import maya.cmds as cmds
#
#以下为全局变量
#
aboutMenuItem = ""
     
charsScrollList = ""  #角色名列表
nucleusScrollList = ""  #解算器列表
nDynNodesScrollList = ""  #目标节点列表
refreshButton = ""  #刷新列表按钮

tOnButton = ""  #开解算器按钮
tOffButton = ""  #关解算器按钮
changeTextButton = ""  #开始帧设置按钮

cPreText = ""
cPreScrollList = ""
saveCPreButton = ""  #保存特殊人物预设按钮
delCPreButton = ""  #删除特殊人物预设按钮
createNCloButton = ""  #创建布料按钮
delNCloCButton = ""  #删除布料按钮
changeNCloButton = ""  #改变布料预设按钮   
softAndHardSlider = ""

nConsOptMenu = ""
nConsButton = ""  #创建约束按钮
nCollButton = ""  #创建碰撞按钮
inAttrButton = ""  #刷模型权重按钮
repairOptMenu = ""
repairButton = ""  #调用修穿帮工具按钮

gCacheCreButton = ""  #创建模型缓存按钮
nCacheCreButton = ""  #创建毛发缓存按钮
gCacheDelButton = ""  #删除模型缓存按钮
nCacheDelButton = ""  #删除毛发缓存按钮
gCacheAttButton = ""  #导入模型缓存按钮
nCacheAttButton = ""  #导入毛发缓存按钮
cachePrepareButton = ""  #缓存准备按钮
cacheUpButton = ""  #缓存上传按钮
attachCacheAllButton = ""  #一键上缓存按钮
deleteCacheAllButton = ""  #一键删缓存按钮


class MainWindow():
    """主窗体类

    Description:
        插件的主窗体

    Attributes:
        无
    """    
    def __init__(self):
        pass

    def createMainWindow(self):
        """该函数实现插件主窗体的创建
    
        Description:
            主窗体由columnLayout来布局，分成五个并列的frameLayout分别承载各自模块的控件
    
        Arguments:
            无
    
        Returns:
            无
        """
        global aboutMenuItem
         
        global charsScrollList
        global nucleusScrollList
        global nDynNodesScrollList
        global refreshButton
        
        global tOnButton
        global tOffButton
        global changeTextButton
        
        global cPreText
        global cPreScrollList
        global saveCPreButton
        global delCPreButton
        global createNCloButton
        global delNCloCButton
        global changeNCloButton
        global softAndHardSlider
        
        global nConsOptMenu
        global nConsButton
        global nCollButton
        global inAttrButton
        global repairOptMenu
        global repairButton
        
        global gCacheCreButton
        global nCacheCreButton
        global gCacheDelButton
        global nCacheDelButton
        global gCacheAttButton
        global nCacheAttButton
        global cachePrepareButton
        global cacheUpButton
        global attachCacheAllButton
        global deleteCacheAllButton
        
        #
        #---------------------------------------以下为窗体的显示------------------------------------------------------
        #
        mainWindow = cmds.window(title = "NCloth NHair Plug-in", iconName = "CH", widthHeight = (300, 200), menuBar = True, resizeToFitChildren = True)
            
        cmds.columnLayout(adjustableColumn = True)
    
        cmds.menu(label = "Notice")
        aboutMenuItem = cmds.menuItem(label = "About...")
        cmds.menu(label = "Help", helpMenu = True)
        cmds.menuItem(label = "Help...")
        cmds.separator(style = "in")
        
        #
        #以下是nDynamics information模块的布局
        #
        cmds.frameLayout(label = "nDynamics information", borderStyle = "in", collapsable = 1, collapse = 0)
        
        nDynInforFormLayout = cmds.formLayout()
        charsText = cmds.text(label="chars:", align="left")
        charsScrollList = cmds.textScrollList("charsList", numberOfRows = 3)  #角色名列表
        nucleusText = cmds.text(label="nucleus:", align="left")
        nucleusScrollList = cmds.textScrollList("nucleusList", numberOfRows = 4)  #解算器列表
        nDynNodesText = cmds.text(label="nDynamics nodes connected with nucleus:", align="left")
        nDynNodesScrollList = cmds.textScrollList("nDynNodesList", numberOfRows = 6, allowMultiSelection = True)  #目标节点列表
        refreshButton = cmds.button(label = "Refresh", width = 92, height = 17)
        cmds.formLayout(nDynInforFormLayout, edit=True, 
                                            attachForm=[(charsText, "top", 4), (charsText, "left", 4),
                                                        (charsScrollList, "left", 4),(charsScrollList, "right", 4), 
                                                        (nucleusText, "left", 4),
                                                        (nucleusScrollList, "left", 4), (nucleusScrollList, "right", 4), 
                                                        (nDynNodesText, "left", 4),
                                                        (nDynNodesScrollList, "left", 4), (nDynNodesScrollList, "right", 4), 
                                                        (refreshButton, "right", 4), (refreshButton, "bottom", 4)], 
                                            attachControl=[(charsScrollList, 'top', 1, charsText), 
                                                           (nucleusText, 'top', 3, charsScrollList),
                                                           (nucleusScrollList, 'top', 1, nucleusText),
                                                           (nDynNodesText, 'top', 3, nucleusScrollList),
                                                           (nDynNodesScrollList, 'top', 1, nDynNodesText),
                                                           (refreshButton, 'top', 3, nDynNodesScrollList)])
        
        cmds.setParent("..")
        cmds.setParent("..")
        
        #
        #以下是nucleus management模块的布局
        #
        cmds.frameLayout(label = "nucleus management", borderStyle = "in", collapsable = 1, collapse = 1)
        
        nucleusFormLayout = cmds.formLayout()
        tOnButton = cmds.button(label = "Turn On", width = 92, height = 17)  #开解算器按钮
        tOffButton = cmds.button(label = "Turn Off", width = 92, height = 17)  #关解算器按钮
        changeTextButton = cmds.textFieldButtonGrp("startFrameGrp", buttonLabel='Change', columnWidth = [(1, 46), (2, 60)], height = 17, rowAttach = [(1, "both", 0), (2, "both", 0)])  #开始帧设置按钮
        cmds.formLayout(nucleusFormLayout, edit=True,
                                            attachForm=[(tOnButton, "top", 4), (tOnButton, "left", 4), (tOnButton, "bottom", 4),
                                                        (tOffButton, "top", 4), (tOffButton, "bottom", 4), 
                                                        (changeTextButton, "top", 3), (changeTextButton, "right", 4), (changeTextButton, "bottom", 3)], 
                                            attachControl=[(tOffButton, "left", 4, tOnButton), 
                                                           (changeTextButton, "left", 4, tOffButton)])
        cmds.setParent("..")    
        cmds.setParent("..")
        
        #
        #以下是nCloth nHair management模块的布局
        #
        cmds.frameLayout(label = "nCloth nHair management", borderStyle = "in", collapsable = 1, collapse = 1)
        
        chFormLayout = cmds.formLayout()
    
        cPreText = cmds.text("charNameText", label="xxxxxxxxxx 's presets:")  #角色名称
        cPreScrollList = cmds.textScrollList("cPreList", numberOfRows=4, width = 190)  #预设列表
        
        sAndDButtonColLayout = cmds.columnLayout( columnAttach=('both', 0), rowSpacing = 4, columnWidth = 94 )
        saveCPreButton = cmds.button(label = "Save Preset", width = 92, height = 17)  #保存特殊人物预设按钮
        delCPreButton = cmds.button(label = "Delete Preset", width = 92, height = 17)  #删除特殊人物预设按钮
        cmds.setParent("..")
        
        chSeparator = cmds.separator(style = "in")
        nClothButtonsRowLayout = cmds.rowLayout(numberOfColumns = 3, adjustableColumn = 3, columnAlign=(1, "left"), 
                                                columnAttach=[(1, "right", 4), (2, "right", 4), (3, "right", 0)])
        createNCloButton = cmds.button(label = "Create NCloth", width = 92, height = 17)  #创建布料按钮
        delNCloCButton = cmds.button(label = "Delete NCloth", width = 92, height = 17)  #删除布料按钮
        changeNCloButton = cmds.button(label = "Change Preset", width = 92, height = 17)  #改变布料预设按钮   
        cmds.setParent("..")
        chSeparatorTwo = cmds.separator(style="in")    
        softAndHardSlider = cmds.floatSliderGrp("softAndHardFSG", label = "Soft ---> Hard:", field = True, width = 280,
                                                columnWidth = [(1,95),(2,40),(3,140)], columnAlign = [(1,"left"),(2,"center"),(3,"center")],
                                                minValue = 0.0, maxValue = 10.0, value = 5.0)
        cmds.formLayout(chFormLayout, edit=True, 
                                      attachForm=[(cPreText, "top", 4), (cPreText, "left", 4),
                                                  (cPreScrollList, "left", 4),
                                                  (sAndDButtonColLayout, "right", 0), (sAndDButtonColLayout, "top", 38),
                                                  (chSeparator, "right", 4), (chSeparator, "left", 4),
                                                  (nClothButtonsRowLayout, "right", 4), (nClothButtonsRowLayout, "left", 4),
                                                  (chSeparatorTwo, "right", 4), (chSeparatorTwo, "left", 4),
                                                  (softAndHardSlider, "right", 4), (softAndHardSlider, "left", 4), (softAndHardSlider, "bottom", 4)], 
                                      attachControl=[(cPreScrollList, "top", 1, cPreText), 
                                                     (sAndDButtonColLayout, "left", 6, cPreScrollList),
                                                     (chSeparator, "top", 4, cPreScrollList),
                                                     (nClothButtonsRowLayout, "top", 4, chSeparator),
                                                     (chSeparatorTwo, "top", 4, nClothButtonsRowLayout),
                                                     (softAndHardSlider, "top", 4, chSeparatorTwo)])
        
        cmds.setParent("..")
        cmds.setParent("..")
        
        #
        #以下是resolving tools模块的布局
        #
        cmds.frameLayout( label = "resolving tools", borderStyle = "in", collapsable = 1, collapse = 1 )
        toolsFormLayout = cmds.formLayout()
        nConsRowLayout = cmds.rowLayout(numberOfColumns = 3, adjustableColumn = 3, columnAlign=(1, "left"), 
                                        columnAttach=[(1, "right", 4), (2, "right", 4), (3, "right", 0)])
        nConsText = cmds.text(label="nConstraint:", width = 92)
        nConsOptMenu = cmds.optionMenu("nConstraintOM", width = 92, height = 17)  #约束方式选项
        cmds.menuItem(label = "point to surface")
        cmds.menuItem(label = "component to component")
        cmds.menuItem(label = "transform")
        cmds.menuItem(label = "slide on surface")
        nConsButton = cmds.button(label = "Make Constraint", width = 92, height = 17)  #创建约束按钮
        cmds.setParent("..")
        nCollRowLayout = cmds.rowLayout(numberOfColumns = 3, adjustableColumn = 3, columnAlign=(1, "left"), 
                                        columnAttach=[(1, "right", 4), (2, "right", 4), (3, "right", 0)])
        nCollText = cmds.text(label="nCollider:", width = 92)
        nullTextA = cmds.text(label="  ", width = 92)
        nCollButton = cmds.button(label = "Make Collision", width = 92, height = 17)  #创建碰撞按钮
        cmds.setParent("..")
        inAttrRowLayout = cmds.rowLayout(numberOfColumns = 3, adjustableColumn = 3, columnAlign=(1, "left"), 
                                         columnAttach=[(1, "right", 4), (2, "right", 4), (3, "right", 0)])
        inAttrText = cmds.text(label="Input Attract:", width = 92)
        nullTextB = cmds.text(label="  ", width = 92)
        inAttrButton = cmds.button(label = "Paint Mesh", width = 92, height = 17)  #刷模型权重按钮
        cmds.setParent("..")
        repairRowLayout = cmds.rowLayout(numberOfColumns = 3, adjustableColumn = 3, columnAlign=(1, "left"), 
                                         columnAttach=[(1, "right", 4), (2, "right", 4), (3, "right", 0)])
        repairText = cmds.text(label="repair:", width = 92)
        repairOptMenu = cmds.optionMenu("repairToolsOM", width = 92, height = 17)  #修穿帮工具选项
        cmds.menuItem(label = "weights painting")
        cmds.menuItem(label = "points moving")
        repairButton = cmds.button(label = "Call tools", width = 92, height = 17)  #调用修穿帮工具按钮
        cmds.setParent("..")
        toolsSeparator = cmds.separator(style="in")
        hairSelRowLayout = cmds.rowLayout(numberOfColumns = 3, adjustableColumn = 3, columnAlign=(1, "left"), 
                                          columnAttach=[(1, "right", 4), (2, "right", 4), (3, "right", 0)])
        hairSelText = cmds.text(label="nHair select:", width = 92)
        cmds.optionMenu(width = 92, height = 17)  #毛发曲线选项
        cmds.menuItem(label = "to follicles")
        cmds.menuItem(label = "to outPut CVs")
        cmds.menuItem(label = "to pfxHair CVs")
        cmds.menuItem(label = "to hairSystem CVs")
        hairSelButton = cmds.button(label = "Convert", width = 92, height = 17)  #毛发转换选择按钮
        cmds.setParent("..")
        cmds.formLayout(toolsFormLayout, edit=True, 
                                         attachForm=[(nConsRowLayout, "top", 4), (nConsRowLayout, "left", 4), (nConsRowLayout, "right", 4),
                                                     (nCollRowLayout, "left", 4), (nCollRowLayout, "right", 4),
                                                     (inAttrRowLayout, "left", 4), (inAttrRowLayout, "right", 4),
                                                     (repairRowLayout, "left", 4), (repairRowLayout, "right", 4),
                                                     (toolsSeparator, "left", 4), (toolsSeparator, "right", 4),
                                                     (hairSelRowLayout, "left", 4), (hairSelRowLayout, "right", 4), (hairSelRowLayout, "bottom", 4)], 
                                         attachControl=[(nCollRowLayout, "top", 4, nConsRowLayout),
                                                        (inAttrRowLayout, "top", 4, nCollRowLayout),
                                                        (repairRowLayout, "top", 4, inAttrRowLayout),
                                                        (toolsSeparator, "top", 4, repairRowLayout),
                                                        (hairSelRowLayout, "top", 4, toolsSeparator)])
        
        cmds.setParent("..")
        cmds.setParent("..")
        
        #
        #以下是cache management模块的布局
        #
        cmds.frameLayout( label = "cache management", borderStyle = "in", collapsable = 1, collapse = 0 )
        cacheFormLayout = cmds.formLayout()
        cacheCreRowLayout = cmds.rowLayout(numberOfColumns = 3, adjustableColumn = 3, columnAlign=(1, "left"),
                                           columnAttach=[(1, "right", 4), (2, "right", 4), (3, "right", 0)])
        cacheCreText = cmds.text(label="cache creation:", width = 92)
        gCacheCreButton = cmds.button(label = "Create GeoCache", width = 92, height = 17)  #创建模型缓存按钮
        nCacheCreButton = cmds.button(label = "Create HairCache", width = 92, height = 17)  #创建毛发缓存按钮
        cmds.setParent("..")
        cacheDelRowLayout = cmds.rowLayout(numberOfColumns = 3, adjustableColumn = 3, columnAlign=(1, "left"),
                                           columnAttach=[(1, "right", 4), (2, "right", 4), (3, "right", 0)])
        cacheDelText = cmds.text(label="cache deletion:", width = 92)
        gCacheDelButton = cmds.button(label = "Delete GeoCache", width = 92, height = 17)  #删除模型缓存按钮
        nCacheDelButton = cmds.button(label = "Delete HairCache", width = 92, height = 17)  #删除毛发缓存按钮
        cmds.setParent("..")
        cacheAttRowLayout = cmds.rowLayout(numberOfColumns = 3, adjustableColumn = 3, columnAlign=(1, "left"),
                                           columnAttach=[(1, "right", 4), (2, "right", 4), (3, "right", 0)])
        cacheAttText = cmds.text(label="cache attaching:", width = 92)
        gCacheAttButton = cmds.button(label = "Attach GeoCache", width = 92, height = 17)  #导入模型缓存按钮
        nCacheAttButton = cmds.button(label = "Attach HairCache", width = 92, height = 17)  #导入毛发缓存按钮
        cmds.setParent("..")
        cachePrepareRowLayout = cmds.rowLayout(numberOfColumns = 3, adjustableColumn = 3, columnAlign=(1, "left"),
                                               columnAttach=[(1, "right", 4), (2, "right", 4), (3, "right", 0)])
        cachePrepareText = cmds.text(label="cache preparing:", width = 92)
        cachePrepareButton = cmds.button(label = "Prepare Cache", width = 92, height = 17)  #缓存准备按钮
    
        cmds.setParent("..")
        cacheUpRowLayout = cmds.rowLayout(numberOfColumns = 3, adjustableColumn = 3, columnAlign=(1, "left"),
                                          columnAttach=[(1, "right", 4), (2, "right", 4), (3, "right", 0)])
        cacheUpText = cmds.text(label="cache uploading:", width = 92)
        cacheUpButton = cmds.button(label = "Upload Cache", width = 92, height = 17)  #缓存上传按钮
        cmds.setParent("..")
        cacheSeparator = cmds.separator(style="in")
        attachCacheAllRowLayout = cmds.rowLayout(numberOfColumns = 3, adjustableColumn = 3, columnAlign=(1, "left"),
                                          columnAttach=[(1, "right", 4), (2, "right", 4), (3, "right", 0)])
        attachCacheAllText = cmds.text(label="all cache attaching:", width = 92)
        attachCacheAllButton = cmds.button(label = "Attach All", width = 92, height = 17)  #一键上缓存按钮
        deleteCacheAllButton = cmds.button(label = "Delete All", width = 92, height = 17)  #一键删缓存按钮
        cmds.setParent("..")
        cmds.formLayout(cacheFormLayout, edit=True, 
                                         attachForm=[(cacheCreRowLayout, "top", 4), (cacheCreRowLayout, "left", 4), (cacheCreRowLayout, "right", 4),
                                                     (cacheDelRowLayout, "left", 4), (cacheDelRowLayout, "right", 4),
                                                     (cacheAttRowLayout, "left", 4), (cacheAttRowLayout, "right", 4),
                                                     (cachePrepareRowLayout, "left", 4), (cachePrepareRowLayout, "right", 4),
                                                     (cacheUpRowLayout, "left", 4), (cacheUpRowLayout, "right", 4),
                                                     (cacheSeparator, "left", 4), (cacheSeparator, "right", 4),
                                                     (attachCacheAllRowLayout, "left", 4), (attachCacheAllRowLayout, "right", 4), (attachCacheAllRowLayout, "bottom", 4)], 
                                         attachControl=[(cacheDelRowLayout, "top", 4, cacheCreRowLayout),
                                                        (cacheAttRowLayout, "top", 4, cacheDelRowLayout),
                                                        (cachePrepareRowLayout, "top", 4, cacheAttRowLayout),
                                                        (cacheUpRowLayout, "top", 4, cachePrepareRowLayout),
                                                        (cacheSeparator, "top", 4, cacheUpRowLayout),
                                                        (attachCacheAllRowLayout, "top", 4, cacheSeparator)])
        
        cmds.setParent("..")
        cmds.setParent("..")
        cmds.showWindow(mainWindow)

        #
        #------------------------------------------------以下为窗体的触发事件--------------------------------------------------------
        #           
        cmds.menuItem(aboutMenuItem, edit = True, command = "clothAndHair.chMain.nInf.createNoticeWin()")
                    
        cmds.textScrollList(charsScrollList, edit = True, selectCommand = "clothAndHair.chMain.chMag.getPresetsFromChar()")  #角色名列表
        cmds.textScrollList(nucleusScrollList, edit = True, selectCommand = "clothAndHair.chMain.dynInf.getNodesFromNu()")  #解算器列表
        cmds.textScrollList(nDynNodesScrollList, edit = True, selectCommand = "clothAndHair.chMain.dynInf.selShapeFromNode()")  #目标节点列表
        cmds.button(refreshButton, edit = True, command = "clothAndHair.chMain.dynInf.refreshAll()")  #刷新列表按钮
        
        cmds.button(tOnButton, edit = True, command = "clothAndHair.chMain.nuMag.setNucleusOnOff('buttonOn', clothAndHair.chMain.dynInf)")  #开解算器按钮
        cmds.button(tOffButton,edit = True, command = "clothAndHair.chMain.nuMag.setNucleusOnOff('buttonOff', clothAndHair.chMain.dynInf)")  #关解算器按钮
        cmds.textFieldButtonGrp(changeTextButton, edit = True, buttonCommand = "clothAndHair.chMain.nuMag.setNucleusStartF()" )  #开始帧设置按钮
        
        cmds.button(saveCPreButton, edit = True, command = "clothAndHair.chMain.chMag.saveCharPreset()")  #保存特殊人物预设按钮
        cmds.button(delCPreButton, edit = True, command = "clothAndHair.chMain.chMag.deleteCharPreset()")  #删除特殊人物预设按钮
        cmds.button(createNCloButton, edit = True, command = "clothAndHair.chMain.chMag.createNCloth(clothAndHair.chMain.dynInf)")  #创建布料按钮
        cmds.button(delNCloCButton, edit = True, command = "clothAndHair.chMain.chMag.deleteNCloth(clothAndHair.chMain.dynInf)")  #删除布料按钮
        cmds.button(changeNCloButton, edit = True, command = "clothAndHair.chMain.chMag.changePreset()")  #改变布料预设按钮   
        cmds.floatSliderGrp(softAndHardSlider, edit = True, changeCommand = "clothAndHair.chMain.chMag.setClothArg()")
        
        cmds.button(nConsButton, edit = True, command = "clothAndHair.chMain.resT.makeConstraint()")  #创建约束按钮
        cmds.button(nCollButton, edit = True, command = "clothAndHair.chMain.resT.makeCollide()")  #创建碰撞按钮
        cmds.button(inAttrButton, edit = True, command = "clothAndHair.chMain.resT.paintMesh()")  #刷模型权重按钮
        cmds.button(repairButton, edit = True, command = "clothAndHair.chMain.resT.callRepairTools()")  #调用修穿帮工具按钮
        
        cmds.button(gCacheCreButton, edit = True, command = "clothAndHair.chMain.cacheM.createGeoCache()")  #创建模型缓存按钮
        cmds.button(nCacheCreButton, edit = True, command = "clothAndHair.chMain.cacheM.createNCache()")  #创建毛发缓存按钮
        cmds.button(gCacheDelButton, edit = True, command = "clothAndHair.chMain.cacheM.deleteGeoCache()")  #删除模型缓存按钮
        cmds.button(nCacheDelButton, edit = True, command = "clothAndHair.chMain.cacheM.deleteNCache()")  #删除毛发缓存按钮
        cmds.button(gCacheAttButton, edit = True, command = "clothAndHair.chMain.cacheM.attachGeoCache()")  #导入模型缓存按钮
        cmds.button(nCacheAttButton, edit = True, command = "clothAndHair.chMain.cacheM.attachNCache()")  #导入毛发缓存按钮
        cmds.button(cachePrepareButton, edit = True, command = "clothAndHair.chMain.cacheAllM.prepareCacheGrade()")  #缓存准备按钮
        cmds.button(cacheUpButton, edit = True, command = "clothAndHair.chMain.cacheAllM.uploadCache()")  #缓存上传按钮
        cmds.button(attachCacheAllButton, edit = True, command = "clothAndHair.chMain.cacheAllM.attachCacheAll()")  #一键上缓存按钮
        cmds.button(deleteCacheAllButton, edit = True, command = "clothAndHair.chMain.cacheAllM.deleteCacheAll()")  #一键删缓存按钮

