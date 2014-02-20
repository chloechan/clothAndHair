#-*- coding: utf-8-*-#
import os


class CommonTools():
    """常用工具类

    Description:
        该类包括一些常用工具，主要是对列表、字符串等数据类型的一些自定义处理

    Attributes:
        无
    """
    def __init__(self):
        pass
    
    def delDupFromList(self, souList):
        """删除List中的重复元素
    
        Description:
            将List转化为Set，再转回List
    
        Arguments:
            souList：预删除重复元素的List
    
        Returns:
            desList：已删除重复元素的List
        """
        tempSet = set(souList)
        desList = list(tempSet)
        return desList
        
    def getFileListFromAPath(self, thePath, fileList):
        """拿到某个路径下的所有文件名
    
        Description:
            拿到某个路径下的所有文件名
                    
        Arguments:
            thePath：某个指定的文件目录
            fileList：文件名列表
    
        Returns:
            fileList：某个文件目录下的所有文件名列表
        """    
        for file in os.listdir(thePath):
            fileName = str(file)
            fileList.append(fileName)
        return fileList

    def rMatchString(self, bString, sString):
        """找到某个字符串，末尾匹配
    
        Description:
            从末尾开始匹配两个字符串，若匹配则返回1，不匹配则返回0
    
        Arguments:
            bString：长字符串
            sString：短字符串
    
        Returns:
            matchFlag：是否匹配的标记
        """
        if len(sString) > 0 and len(bString) >= len(sString):
            #若小字符串不为空，且大串长小串短（包括长度相同）
            n = -1
            matchFlag = 1  #1为匹配，0为不匹配
            for i in range(len(sString)):
                if sString[n-i] == bString[n-i]:
                    continue
                else:
                    matchFlag = 0
                    break
            
            return matchFlag
        else:
            #若小串为空，或大串短小串长
            return 0

