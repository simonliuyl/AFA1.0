###############################################################################
# -*- coding: gbk -*-
# �ļ���ʶ��
# ժ    Ҫ�����շ�˰
#
# ��ǰ�汾��1.0
# ��    �ߣ�WJJ
# ������ڣ�2007��10��15��
###############################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc, os, sys, HostComm, HostContext, ConfigParser
from types import *

#��ȡ������Ϣ
def GetLappConfig( CfgFileName = None ):
    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )

        TradeContext.HOST_HOSTIP   = config.get('HOST_DZ', 'HOSTIP')
        TradeContext.HOST_USERNO   = config.get('HOST_DZ', 'USERNO')
        TradeContext.HOST_PASSWD   = config.get('HOST_DZ', 'PASSWD')
        
        TradeContext.HOST_LDIR     = os.environ['AFAP_HOME'] + "/data/ahfs/"        #����·��
        TradeContext.HOST_RDIR     = 'FTAXLIB'            #config.get('HOST_DZ', 'RDIR')  #Զ��·��
        TradeContext.TRACE         = config.get('HOST_DZ', 'TRACE')

        return 0

    except Exception, e:
        print str(e)
        return -1
        
#�����ʺ���ˮ��ϸ�ļ�
def GetDetailFile(rfilename, lfilename):
    try:
        #�����ļ�
        ftpShell = os.environ['AFAP_HOME'] + '/data/ahfs/shell/ahfs_ahfs.sh'
        ftpFp = open(ftpShell, "w")

        ftpFp.write('open ' + TradeContext.HOST_HOSTIP + '\n')
        ftpFp.write('user ' + TradeContext.HOST_USERNO + ' ' + TradeContext.HOST_PASSWD + '\n')

        #�����ļ�
        ftpFp.write('cd '  + TradeContext.HOST_RDIR + '\n')
        ftpFp.write('lcd ' + TradeContext.HOST_LDIR + '\n')
        ftpFp.write('quote type c 1381 ' + '\n')
        ftpFp.write('get ' + rfilename + ' ' + lfilename + '\n')

        ftpFp.close()

        ftpcmd = 'ftp -n < ' + ftpShell + ' 1>/dev/null 2>/dev/null '

        ret = os.system(ftpcmd)
        if ( ret != 0 ):
            return -1
        else:
            return 0

    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        AfaLoggerFunc.tradeInfo('FTP�����쳣')
        return -1
        
        
def SubModuleMainFst( ):
    TradeContext.__agentEigen__  = '0'   #�ӱ���־
    
    #ͨѶ�����
    HostContext.I1TRCD = '8847'                        #������
    HostContext.I1SBNO = TradeContext.brno             #���׻�����
    HostContext.I1USID = TradeContext.teller           #���׹�Ա��
    HostContext.I1AUUS = ""                            #��Ȩ��Ա
    HostContext.I1AUPS = ""                            #��Ȩ��Ա����
    HostContext.I1WSNO = TradeContext.termId           #�ն˺�
       
    #20111102 �º��޸� �ļ��������к� ȷ��Ψһ��
    #begin    
    #��ȡһ��4λ�����кţ�����ƴ���ͺ��ĵĿ����ļ��� ȷ��Ψһ��
    CrtSequence( )
        
    #HostContext.I1FINA = 'AG12345678'                             #�ļ�����
    HostContext.I1FINA = 'AG1234'+ TradeContext.sequenceNo         #�ļ����� (10λ)
    #end
    
    #HostContext.I1FINA = TradeContext.brno            #�ļ�����    
    HostContext.I1STDT = TradeContext.bgDate           #��ʼ���� 
    HostContext.I1EDDT = TradeContext.edDate           #��ֹ���� 
    HostContext.I1ACCN = TradeContext.accno            #�Թ������ʺ�
    AfaLoggerFunc.tradeInfo('���ؽ��:��ʼ����     = ' + HostContext.I1STDT)        #����ʱ��
    AfaLoggerFunc.tradeInfo('���ؽ��:��ֹ����     = ' + HostContext.I1EDDT)        #����ʱ��
    AfaLoggerFunc.tradeInfo('���ؽ��:�����ʺ�     = ' + HostContext.I1ACCN)        #����ʱ��

    HostTradeCode = "8847".ljust(10,' ')
    HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8847.map', HostTradeCode, "0002" )
    if( HostContext.host_Error ):
        AfaLoggerFunc.tradeInfo('>>>��������ʧ��=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   HostContext.host_ErrorMsg
        return False
    else:
        if ( HostContext.O1MGID == "AAAAAAA" ):
            AfaLoggerFunc.tradeInfo('>>>��ѯ�������=[' + HostContext.O1MGID + ']���׳ɹ�')
            AfaLoggerFunc.tradeInfo('���ؽ��:�ļ�����     = ' + HostContext.O1FINA)        #�ļ�����
            AfaLoggerFunc.tradeInfo('���ؽ��:��������     = ' + HostContext.O1TRDT)        #��������
            AfaLoggerFunc.tradeInfo('���ؽ��:����ʱ��     = ' + HostContext.O1TRTM)        #����ʱ��
        else:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   HostContext.O1INFO
            return False
    
    AfaLoggerFunc.tradeInfo( "********************��̨�ʺ���ˮ��ϸ��ѯ��ʼ***************" )
    if GetLappConfig() < 0 :
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "��ȡ�����ļ�����"
        return False
        
    AfaLoggerFunc.tradeInfo(TradeContext.HOST_HOSTIP)
    AfaLoggerFunc.tradeInfo(TradeContext.HOST_USERNO)
    AfaLoggerFunc.tradeInfo(TradeContext.HOST_PASSWD)
    AfaLoggerFunc.tradeInfo(TradeContext.TRACE      )
    AfaLoggerFunc.tradeInfo(TradeContext.HOST_LDIR  )
    AfaLoggerFunc.tradeInfo(TradeContext.HOST_RDIR  )

    #fileName    =   os.environ['AFAP_HOME'] + "/data/ahfs/" + TradeContext.FileName
    lFileName    =   'DOWN_8477_' + TradeContext.busiNo + '.txt'
    if GetDetailFile( HostContext.O1FINA,lFileName ) != 0 : 
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "ftp��ˮ��ϸ�ļ�ʧ��"
        return False
        
    AfaLoggerFunc.tradeInfo( "********************��̨�ʺ���ˮ��ϸ��ѯ����***************" )
    TradeContext.errorCode      =   "0000"
    TradeContext.errorMsg       =   "��̨�ʺ���ˮ��ϸ��ѯ�ɹ�"
    TradeContext.downFileName   =   lFileName
    return True


#20111102 �º�����
#begin
#------------------------------------------------------------------
#����һ��4λ�����
#------------------------------------------------------------------     
def CrtSequence( ):
    
    try:
        sqlStr = "SELECT NEXTVAL FOR FSYW_ONLINE_SEQ FROM SYSIBM.SYSDUMMY1"

        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '�������к��쳣' )
        AfaLoggerFunc.tradeInfo( "���кţ�" + str(records[0][0]) )
        
        #���к�
        TradeContext.sequenceNo = str(records[0][0]).rjust(4,'0')
        
        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '�������к��쳣' )
        
#end        