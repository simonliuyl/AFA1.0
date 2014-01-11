###############################################################################
# -*- coding: gbk -*-
# 文件标识：
# 摘    要：安徽非税上传数据信息
#
# 当前版本：1.0
# 作    者：WJJ
# 完成日期：2007年10月15日
###############################################################################
import TradeContext

TradeContext.sysType = 'cron'

import os,AfaLoggerFunc, ConfigParser, AfaUtilTools, sys, AfaDBFunc,AfaAdminFunc
from types import *

#读取配置文件中信息
def GetConfig( CfgFileName = None ):

    #---------------从数据库中提取信息--------------
    
    sqlstr =   "select hostip,upuser,uppasswd,upldir,uprdir from fs_businoconf where busino='34093127790003'"
    sqlstr = sqlstr + " and bankno='" + TradeContext.bankCode + "'"
    
    AfaLoggerFunc.tradeInfo( sqlstr )
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        AfaLoggerFunc.tradeInfo( "查找数据库异常：单位编码ftp配置信息表，联系科技人员" )
        return False
        
    if( len( records)==0 ):
        AfaLoggerFunc.tradeInfo( "没有查找到单位配置信息，联系科技人员" )
        return False
    else:  
        TradeContext.CROP_HOSTIP   = records[0][0].strip()
        TradeContext.CROP_USERNO   = records[0][1].strip()
        TradeContext.CROP_PASSWD   = records[0][2].strip()
        TradeContext.CROP_LDIR     = records[0][3].strip()
        TradeContext.CROP_RDIR     = records[0][4].strip()
        
        AfaLoggerFunc.tradeInfo( "当前单位编码：%s" %TradeContext.busiNo )
        AfaLoggerFunc.tradeInfo( "当前主机地址：%s" %TradeContext.CROP_HOSTIP )
        AfaLoggerFunc.tradeInfo( "账户：%s"         %TradeContext.CROP_USERNO )
        AfaLoggerFunc.tradeInfo( "密码：%s"         %TradeContext.CROP_PASSWD )
        AfaLoggerFunc.tradeInfo( "本地路径：%s"     %TradeContext.CROP_LDIR )
        return True   

#安徽非税上传数据生成文件
def WrtData(filename):
    
    
    AfaLoggerFunc.tradeInfo("开始写"+TradeContext.bankCode + filename + TradeContext.workDate + ".txt"+"中的数据")
    
    #建立名称和字段映射
    map         =   {"FC84":"AFC401,AAA010,AFC001,AFA031,AFA051,AFA101,AAA011,AFC002,AFC003,AFC004,AFC005,AFC006,AFC007,AFC008,AFC009,AFC010,AFC011,AFC012,AFC013,AFC015,AFC016,AFC187,AFA091", \
                     "FC74":"AFC401,AAA010,AFA101,AFC004,AFC006,AFC007,AFC008,AFC011,AFC015,AFC016,FZPH,AFA091", \
                     "FC75":"AAA010,AFC060,AFA050,AFC041,AFC061,AFC062,AFC063,AFC064,FBLRQ,AFA101", \
                     "FC76":"AFC001,AFA031,AFC163,AFC187,AFC183,AFC157,AFC181,AFA040,AFC180,AFA051, AFC166, AFC155,AFC153,AFC154,AFA183,AFA184,AFA185,AFA091,AFC015,AAA010"}

    try:
        dateTmp     =   TradeContext.workDate[0:4] + '-' + TradeContext.workDate[4:6] + '-' + TradeContext.workDate[6:8]
        #begin 20100608 蔡永贵修改
        if filename == 'FC74':
            #sqlstr      =   "select " + map[filename] + " from FS_" + filename + " where FLAG != '*' and busino='" + TradeContext.busiNo + "' and afc015='" + dateTmp + "'"
            sqlstr      =   "select " + map[filename] + " from FS_" + filename + " where FLAG != '*' and busino='" + TradeContext.busiNo + "' and DATE='" + TradeContext.workDate + "'"          
            
        else:
            sqlstr      =   "select " + map[filename] + " from FS_" + filename + " where FLAG = '0' and busino='" + TradeContext.busiNo + "' and DATE='" + TradeContext.workDate + "'"
        
        if filename == 'FC76':
            sqlstr      =   sqlstr + " and bankno = '" + TradeContext.bankCode + "'"
        else:
            sqlstr      =   sqlstr + " and afa101 = '" + TradeContext.bankCode + "'"
        #end
            
        records = AfaDBFunc.SelectSql( sqlstr )
        if( records == None or len( records)==0 ):
            AfaLoggerFunc.tradeInfo( sqlstr )
            AfaLoggerFunc.tradeInfo( "在"+filename+"表中没有要上传的数据" )
            return False
        else:  
            recCnt  =   len(records)
            
            #=====刘雨龙 20080819 修改文件名组成规则，确保唯一性====
            #hp      =   open( TradeContext.CROP_LDIR + '/' + TradeContext.bankCode + filename + TradeContext.workDate + ".txt","w" )
            hp      =   open( TradeContext.CROP_LDIR + '/' + TradeContext.busiNo + filename + TradeContext.workDate + ".txt","w" )
            
            for i in range(recCnt):
                sep =   chr(31)
                
                #---------在这里特殊处理流水号码，因为流水号码只有10位，有重复的可能，故在这里把流水号都改成18位的。---
                if filename == 'FC74':
                    tmpList     =   list(records[i])
                    if len(tmpList[0]) == 10:
                        tmpList[0]  =   tmpList[0] + tmpList[8][0:4] + tmpList[8][5:7] + tmpList[8][8:]
                        hp.write( sep.join( tmpList ) )
                    else:
                        AfaLoggerFunc.tradeInfo('流水号码不是10位')
                        sys.exit(1)
                elif filename == 'FC84':
                    tmpList     =   list(records[i])
                    serNoList   =   [k+ tmpList[19][0:4] + tmpList[19][5:7] + tmpList[19][8:] for k in tmpList[0].split(':')]
                    tmpList[0]  =   ':'.join(serNoList)
                    hp.write( sep.join( tmpList ) )
                else:
                    #hp.write( sep.join(str(records[i]).strip()) )
                    hp.write( sep.join(records[i]) )
                    
                if filename == 'FC74' :
                    hp.write(sep+''+sep+'')
                if i != recCnt:
                    hp.write(chr(12))
                    
            hp.close()
            AfaLoggerFunc.tradeInfo(sqlstr)
            AfaLoggerFunc.tradeInfo("写"+TradeContext.busiNo + filename + TradeContext.workDate + ".txt"+"中的数据结束")
            return True
            
    except Exception, e:
        AfaLoggerFunc.tradeInfo(str(e))
        sys.exit(1)
        
def PutData(filename):
    AfaLoggerFunc.tradeInfo("开始上传文件:"+TradeContext.busiNo + filename + TradeContext.workDate + ".txt"+"中的数据")
    try:
        #创建文件
        ftpShell = os.environ['AFAP_HOME'] + '/data/ahfs/shell/ftp_ahfs.sh'
        ftpFp = open(ftpShell, "w")

        ftpFp.write('open ' + TradeContext.CROP_HOSTIP + '\n')
        ftpFp.write('user ' + TradeContext.CROP_USERNO + ' ' + TradeContext.CROP_PASSWD + '\n')

        #上传文件
        if TradeContext.CROP_RDIR :
            ftpFp.write('cd ' + TradeContext.CROP_RDIR + '\n')
            
        ftpFp.write('lcd ' + TradeContext.CROP_LDIR + '\n')
        ftpFp.write('bin ' + '\n')
 
        #=====刘雨龙　　20080819 修改文件名称保证唯一性====
        #ftpFp.write('put ' + TradeContext.bankCode + filename + TradeContext.workDate + ".txt" + '\n')
        ftpFp.write('put ' + TradeContext.busiNo + filename + TradeContext.workDate + ".txt " + TradeContext.bankCode+filename+TradeContext.workDate+'.txt\n')

        ftpFp.close()

        ftpcmd = 'ftp -n < ' + ftpShell + ' 1>/dev/null 2>/dev/null '
        ret = os.system(ftpcmd)
        if ( ret != 0 ):
            AfaLoggerFunc.tradeInfo( "上传文件" + TradeContext.busiNo   + filename + TradeContext.workDate + ".txt" + "失败" )
            #AfaLoggerFunc.tradeInfo( "上传文件" + TradeContext.bankCode + filename + TradeContext.workDate + ".txt" + "失败" )
            return -1
        else:
            AfaLoggerFunc.tradeInfo( "上传文件" + TradeContext.busiNo   + filename + TradeContext.workDate + ".txt" + "成功" )
            #AfaLoggerFunc.tradeInfo( "上传文件" + TradeContext.bankCode + filename + TradeContext.workDate + ".txt" + "成功" )
            return 0

    except Exception, e:
        AfaLoggerFunc.tradeInfo('FTP处理异常')
        return -1
    
                        
        
###########################################主函数###########################################
if __name__=='__main__':
    
    #初始化TradeContext
    #TradeContext.workDate       =   AfaUtilTools.GetSysDate( )
    #TradeContext.workDate  =   '20091130'
    if (len(sys.argv) == 2):
        TradeContext.workDate    = sys.argv[1]
    else:
        TradeContext.workDate    =   AfaAdminFunc.getTimeFromNow(int(-1))
    #TradeContext.workTime       =   AfaUtilTools.GetSysTime( )
    #TradeContext.zoneno         =   
    #TradeContext.brno           =   
    #TradeContext.teller         =   
    #TradeContext.authPwd        =   
    #TradeContext.termId         =   
    #TradeContext.appNo          =   
    #TradeContext.busiNo         =   
    #TradeContext.TransCode      =   "8448"
    #TradeContext.workDate       = '20120323'
    
    #TradeContext.sysId = "AG2008"


    AfaLoggerFunc.tradeInfo( "*************************上传数据开始********************" )
    
    #begin 20100528 蔡永贵修改
    #sqlstr  = "select distinct busino from abdt_unitinfo where appno='AG2008'"
    #sqlstr  = "select distinct busino, appno from abdt_unitinfo where appno in('AG2008','AG2012')"
    sqlstr  = " select busino,bankno from fs_businoinfo "
    #end
    
    
    records = AfaDBFunc.SelectSql( sqlstr )
    if records == None or len(records)==0 :
        AfaLoggerFunc.tradeInfo("查找单位信息表异常")
        sys.exit(1)
    
    AfaLoggerFunc.tradeInfo(str(records))    
    for i in range( len(records) ):
    
        #bgein 20100528 蔡永贵修改
        #TradeContext.appNo        = 'AG2008'
        TradeContext.bankCode     = records[i][1].strip()
        #end
        
        TradeContext.busiNo       = records[i][0].strip()
        
        #begin 20100607 蔡永贵 修改银行编码获取方式为根据业务编号来取得
        #--------根据单位编号获取银行代码----------------------
        #sqlstr   =   "select bankno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
        #records1 = AfaDBFunc.SelectSql( sqlstr )
        #if records1 == None or len(records1)==0 :
        #    AfaLoggerFunc.tradeInfo("查找银行编码信息表失败")
        #    continue

        #else:
        #    TradeContext.bankCode     = records1[0][0].strip()
            
        if( TradeContext.bankCode == '012' ):
            TradeContext.appNo = 'AG2008';
        else:
            TradeContext.appNo = 'AG2012';
        
        #end    
        
        #----------------获取财政ftp信息---------------------
        GetConfig()
        fileList    =   ["FC76","FC74","FC75","FC84"]    
            
        for file in fileList:
            #直接向财政ftp以便于取得文件
            WrtData(file) 
    
    AfaLoggerFunc.tradeInfo('**********上传数据结束**********')
    sys.exit(0)
