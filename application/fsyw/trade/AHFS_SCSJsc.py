###############################################################################
# -*- coding: gbk -*-
# �ļ���ʶ��
# ժ    Ҫ�����շ�˰�ϴ�������Ϣ
#
# ��ǰ�汾��1.0
# ��    �ߣ�WJJ
# ������ڣ�2007��10��15��
###############################################################################
import TradeContext

TradeContext.sysType = 'cron'

import os,AfaLoggerFunc, ConfigParser, AfaUtilTools, sys, AfaDBFunc,AfaAdminFunc
from types import *

#��ȡ�����ļ�����Ϣ
def GetConfig( CfgFileName = None ):

    #---------------�����ݿ�����ȡ��Ϣ--------------
    
    #begin 20100528 �������޸�
    #sqlstr =   "select hostip,upuser,uppasswd,upldir,uprdir from fs_businoconf where busino='" + TradeContext.busiNo + "'"
    sqlstr =   "select hostip,upuser,uppasswd,upldir,uprdir from fs_businoconf where busino='" + TradeContext.busiNo + "'"
    sqlstr = sqlstr + " and bankno='" + TradeContext.bankCode + "'"
    #end
    
    AfaLoggerFunc.tradeInfo( sqlstr )
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        AfaLoggerFunc.tradeInfo( "�������ݿ��쳣����λ����ftp������Ϣ������ϵ�Ƽ���Ա" )
        return False
        
    if( len( records)==0 ):
        AfaLoggerFunc.tradeInfo( "û�в��ҵ���λ������Ϣ����ϵ�Ƽ���Ա" )
        return False
    else:  
        TradeContext.CROP_HOSTIP   = records[0][0].strip()
        TradeContext.CROP_USERNO   = records[0][1].strip()
        TradeContext.CROP_PASSWD   = records[0][2].strip()
        TradeContext.CROP_LDIR     = records[0][3].strip()
        TradeContext.CROP_RDIR     = records[0][4].strip()
        
        AfaLoggerFunc.tradeInfo( "��ǰ��λ���룺%s" %TradeContext.busiNo )
        AfaLoggerFunc.tradeInfo( "��ǰ������ַ��%s" %TradeContext.CROP_HOSTIP )
        AfaLoggerFunc.tradeInfo( "�˻���%s"         %TradeContext.CROP_USERNO )
        AfaLoggerFunc.tradeInfo( "���룺%s"         %TradeContext.CROP_PASSWD )
        AfaLoggerFunc.tradeInfo( "����·����%s"     %TradeContext.CROP_LDIR )
        return True   

#���շ�˰�ϴ����������ļ�
def WrtData(filename):
    
    
    AfaLoggerFunc.tradeInfo("��ʼд"+TradeContext.bankCode + filename + TradeContext.workDate + ".txt"+"�е�����")
    
    #�������ƺ��ֶ�ӳ��
    map         =   {"FC84":"AFC401,AAA010,AFC001,AFA031,AFA051,AFA101,AAA011,AFC002,AFC003,AFC004,AFC005,AFC006,AFC007,AFC008,AFC009,AFC010,AFC011,AFC012,AFC013,AFC015,AFC016,AFC187,AFA091", \
                     "FC74":"AFC401,AAA010,AFA101,AFC004,AFC006,AFC007,AFC008,AFC011,AFC015,AFC016,FZPH,AFA091", \
                     "FC75":"AAA010,AFC060,AFA050,AFC041,AFC061,AFC062,AFC063,AFC064,FBLRQ,AFA101", \
                     "FC76":"AFC001,AFA031,AFC163,AFC187,AFC183,AFC157,AFC181,AFA040,AFC180,AFA051, AFC166, AFC155,AFC153,AFC154,AFA183,AFA184,AFA185,AFA091,AFC015,AAA010"}

    try:
        dateTmp     =   TradeContext.workDate[0:4] + '-' + TradeContext.workDate[4:6] + '-' + TradeContext.workDate[6:8]
        #begin 20100608 �������޸�
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
            AfaLoggerFunc.tradeInfo( "��"+filename+"����û��Ҫ�ϴ�������" )
            return False
        else:  
            recCnt  =   len(records)
            
            #=====������ 20080819 �޸��ļ�����ɹ���ȷ��Ψһ��====
            #hp      =   open( TradeContext.CROP_LDIR + '/' + TradeContext.bankCode + filename + TradeContext.workDate + ".txt","w" )
            hp      =   open( TradeContext.CROP_LDIR + '/' + TradeContext.busiNo + filename + TradeContext.workDate + ".txt","w" )
            
            for i in range(recCnt):
                sep =   chr(31)
                
                #---------���������⴦����ˮ���룬��Ϊ��ˮ����ֻ��10λ�����ظ��Ŀ��ܣ������������ˮ�Ŷ��ĳ�18λ�ġ�---
                if filename == 'FC74':
                    tmpList     =   list(records[i])
                    if len(tmpList[0]) == 10:
                        tmpList[0]  =   tmpList[0] + tmpList[8][0:4] + tmpList[8][5:7] + tmpList[8][8:]
                        hp.write( sep.join( tmpList ) )
                    else:
                        AfaLoggerFunc.tradeInfo('��ˮ���벻��10λ')
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
            AfaLoggerFunc.tradeInfo("д"+TradeContext.busiNo + filename + TradeContext.workDate + ".txt"+"�е����ݽ���")
            return True
            
    except Exception, e:
        AfaLoggerFunc.tradeInfo(str(e))
        sys.exit(1)
        
def PutData(filename):
    AfaLoggerFunc.tradeInfo("��ʼ�ϴ��ļ�:"+TradeContext.busiNo + filename + TradeContext.workDate + ".txt"+"�е�����")
    try:
        #�����ļ�
        ftpShell = os.environ['AFAP_HOME'] + '/data/ahfs/shell/ftp_ahfs.sh'
        ftpFp = open(ftpShell, "w")

        ftpFp.write('open ' + TradeContext.CROP_HOSTIP + '\n')
        ftpFp.write('user ' + TradeContext.CROP_USERNO + ' ' + TradeContext.CROP_PASSWD + '\n')

        #�ϴ��ļ�
        if TradeContext.CROP_RDIR :
            ftpFp.write('cd ' + TradeContext.CROP_RDIR + '\n')
            
        ftpFp.write('lcd ' + TradeContext.CROP_LDIR + '\n')
        ftpFp.write('bin ' + '\n')
 
        #=====����������20080819 �޸��ļ����Ʊ�֤Ψһ��====
        #ftpFp.write('put ' + TradeContext.bankCode + filename + TradeContext.workDate + ".txt" + '\n')
        ftpFp.write('put ' + TradeContext.busiNo + filename + TradeContext.workDate + ".txt " + TradeContext.bankCode+filename+TradeContext.workDate+'.txt\n')

        ftpFp.close()

        ftpcmd = 'ftp -n < ' + ftpShell + ' 1>/dev/null 2>/dev/null '
        ret = os.system(ftpcmd)
        if ( ret != 0 ):
            AfaLoggerFunc.tradeInfo( "�ϴ��ļ�" + TradeContext.busiNo   + filename + TradeContext.workDate + ".txt" + "ʧ��" )
            #AfaLoggerFunc.tradeInfo( "�ϴ��ļ�" + TradeContext.bankCode + filename + TradeContext.workDate + ".txt" + "ʧ��" )
            return -1
        else:
            AfaLoggerFunc.tradeInfo( "�ϴ��ļ�" + TradeContext.busiNo   + filename + TradeContext.workDate + ".txt" + "�ɹ�" )
            #AfaLoggerFunc.tradeInfo( "�ϴ��ļ�" + TradeContext.bankCode + filename + TradeContext.workDate + ".txt" + "�ɹ�" )
            return 0

    except Exception, e:
        AfaLoggerFunc.tradeInfo('FTP�����쳣')
        return -1
    
                        
        
###########################################������###########################################
if __name__=='__main__':
    
    #��ʼ��TradeContext
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


    AfaLoggerFunc.tradeInfo( "*************************�ϴ����ݿ�ʼ********************" )
    
    #begin 20100528 �������޸�
    #sqlstr  = "select distinct busino from abdt_unitinfo where appno='AG2008'"
    #sqlstr  = "select distinct busino, appno from abdt_unitinfo where appno in('AG2008','AG2012')"
    sqlstr  = " select busino,bankno from fs_businoinfo where busino='34093127790003'"
    #end
    
    
    records = AfaDBFunc.SelectSql( sqlstr )
    if records == None or len(records)==0 :
        AfaLoggerFunc.tradeInfo("���ҵ�λ��Ϣ���쳣")
        sys.exit(1)
    
    AfaLoggerFunc.tradeInfo(str(records))    
    for i in range( len(records) ):
    
        #bgein 20100528 �������޸�
        #TradeContext.appNo        = 'AG2008'
        TradeContext.bankCode     = records[i][1].strip()
        #end
        
        TradeContext.busiNo       = records[i][0].strip()
        
        #begin 20100607 ������ �޸����б����ȡ��ʽΪ����ҵ������ȡ��
        #--------���ݵ�λ��Ż�ȡ���д���----------------------
        #sqlstr   =   "select bankno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
        #records1 = AfaDBFunc.SelectSql( sqlstr )
        #if records1 == None or len(records1)==0 :
        #    AfaLoggerFunc.tradeInfo("�������б�����Ϣ��ʧ��")
        #    continue

        #else:
        #    TradeContext.bankCode     = records1[0][0].strip()
            
        if( TradeContext.bankCode == '012' ):
            TradeContext.appNo = 'AG2008';
        else:
            TradeContext.appNo = 'AG2012';
        
        #end    
        
        #----------------��ȡ����ftp��Ϣ---------------------
        GetConfig()
        fileList    =   ["FC76","FC74","FC75","FC84"]    
            
        for file in fileList:
            #ֱ�������ftp�Ա���ȡ���ļ�
            if ( WrtData(file) ) :
                AfaLoggerFunc.tradeInfo( "ok")  
    
    AfaLoggerFunc.tradeInfo('**********�ϴ����ݽ���**********')
    sys.exit(0)