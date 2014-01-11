# -*- coding: gbk -*-
##################################################################
#   农信银.查询打印.通存通兑错帐通知查询
#=================================================================
#   程序文件:   TRCC001_8589.py
#   修改时间:   2008-12-15
#   作者：      刘振东
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_notbka 

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作).通存通兑主机错帐查询[TRCC001_8589]进入***' )
    
    #=====必要性检查====
    AfaLoggerFunc.tradeInfo(">>>开始必要性检查")
    
    if( not TradeContext.existVariable( "TRCCO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '交易代码[TRCCO]不存在')
        
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始笔数[RECSTRNO]不存在')
        
    AfaLoggerFunc.tradeInfo(">>>必要性检查结束")
    
    #=====组织sql语句====
    AfaLoggerFunc.tradeInfo(">>>开始组织查询sql语句")
    
    wheresql = ""
    wheresql = wheresql + "NOTDAT='" + TradeContext.NOTDAT + "' " 
    wheresql = wheresql + " AND BESBNO='" + TradeContext.BESBNO + "' "
    
    ordersql = " order by NOTDAT DESC"
    
    start_no = TradeContext.RECSTRNO        #起始笔数
    sel_size = 10                           #查询笔数
    
    AfaLoggerFunc.tradeDebug(">>>结束组织查询sql语句")   
    
    #=====查询总记录数====
    allcount=rccpsDBTrcc_notbka.count(wheresql)
    
    if(allcount<0):
        return AfaFlowControl.ExitThisFlow('A099','查询总笔数失败' )
        
    #=====查询数据库====
    
    AfaLoggerFunc.tradeInfo("wheresql=" + wheresql)
    records = rccpsDBTrcc_notbka.selectm(start_no,sel_size,wheresql,ordersql)
    
    if(records == None):
        return AfaFlowControl.ExitThisFlow('A099','查询失败' )    
    if len(records) <= 0:
        return AfaFlowControl.ExitThisFlow('A099','未查找到数据' )
    else:
        #=====生成文件====
        try:
            filename = "rccps_" + TradeContext.BETELR+"_" + AfaUtilTools.GetHostDate() + "_" + TradeContext.TransCode
            fpath = os.environ["AFAP_HOME"] + "/tmp/"
            f = open(fpath + filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S099','打开文件失败')
    
    #=====写文件操作====
        try:
            filecontext=""
            AfaLoggerFunc.tradeInfo ("生成文件内容 ")
            for i in range(0,len(records)):
                #AfaLoggerFunc.tradeDebug("写入第"+str(i)+"笔记录开始")
                filecontext= records[i]['NOTDAT']        + "|" \
                           + records[i]['BESBNO']        + "|" \
                           + records[i]['STRINFO']       + "|" 
                           
                f.write(filecontext+"\n") 
                #AfaLoggerFunc.tradeDebug("写入第"+str(i)+"笔记录结束")     
        except Exception,e:                                        
            f.close()                                              
            return AfaFlowControl.ExitThisFlow('S099','写文件失败')
            AfaLoggerFunc.tradeInfo ("生成文件内容结束 ")
    
    #=====输出接口赋值====
    TradeContext.RECSTRNO=start_no              #起始笔数
    TradeContext.RECCOUNT=str(len(records))     #本次查询笔数
    TradeContext.RECALLCOUNT=str(allcount)      #总笔数
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="查询成功"
    TradeContext.PBDAFILE=filename              #文件名
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作).通存通兑错帐通知查询[TRCC001_8589]退出***' )
    return True 	
           
