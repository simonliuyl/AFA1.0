# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨
#=================================================================
#   �����ļ�:   T3001_8445.py
#   �޸�ʱ��:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc

def SubModuleDealFst( ):

    TradeContext.__agentEigen__  = '0'   #�ӱ���־

    if (TradeContext.channelCode =='001' ): #���潻�ײ��Ʒ�Ʊ
        TradeContext.__billSaveCtl__  = '0'
    else:
        TradeContext.__billSaveCtl__  = '1'

    return True

def SubModuleDealSnd():

    AfaLoggerFunc.tradeInfo( "********************��ʼ����******************" )

    #���Ƚ��ɿ�����Ϣ��Ϊ��Ч���ٽ��ϴ���¼������Ϊ��Ч��ɾ�������ұ��еĹ�ϵ

    sqlstr =   "select * from FS_FC76 where AFC001='" + TradeContext.userNo + "'"

    #===�����������б����ֶ�,�ź��޸�===
    sqlstr = sqlstr + " and afc153 = '" + TradeContext.bankbm + "'"

    records = AfaDBFunc.SelectSql( sqlstr )
    
    if( records and len( records)>0 ):
        sqlstr  =   ""
        #begin 20100716 �������޸� ��ԭ���ĸ��¸�Ϊɾ��
        #sqlstr  =   "update fs_fc76 set flag='1' where afc001='" + TradeContext.userNo + "'"
        sqlstr = " delete from fs_fc76 where afc001='" + TradeContext.userNo + "'"

        #===�����������б����ֶ�,�ź��޸�===
        sqlstr = sqlstr + " and afc153 = '" + TradeContext.bankbm + "'"

        #if( AfaDBFunc.UpdateSqlCmt( sqlstr ) < 1 ):
        if( AfaDBFunc.DeleteSqlCmt( sqlstr ) < 1 ):
        #end
            TradeContext.errorCode, TradeContext.errorMsg='0001', '���ɿ�����Ϣ��Ϊ��Чʧ��,����ʧ��'
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg + AfaDBFunc.sqlErrMsg )
            return False

    #���Ȳ����Ƿ��в�¼����,����������Ϊ��Ч��û����Ҫ����
    AfaLoggerFunc.tradeInfo("����¼������Ϊ��Ч")

    sqlstr =   "select * from FS_FC84 where AFC001='" + TradeContext.userNo + "'"

    #===�����������б����ֶ�,�ź��޸�===
    sqlstr = sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

    records = AfaDBFunc.SelectSql( sqlstr )
    if( records and len( records)>0 ):
        sqlstr  =   ""
        sqlstr  =   "update fs_fc84 set flag='1' where afc001='" + TradeContext.userNo + "'"

        #===�����������б����ֶ�,�ź��޸�===
        sqlstr = sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

        if( AfaDBFunc.UpdateSqlCmt( sqlstr ) < 1 ):
            TradeContext.errorCode, TradeContext.errorMsg='0002', '���ϴ���¼������Ϊ��Чʧ��,����ʧ��'
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg  )
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            return False

    AfaLoggerFunc.tradeInfo("������������Ϊ��Ч")
    sqlstr =   "select * from FS_FC74 where AFC001='" + TradeContext.userNo + " ' "

    #===�����������б����ֶ�,�ź��޸�===
    sqlstr = sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

    records = AfaDBFunc.SelectSql( sqlstr )
    if( records and len( records)>0 ):
        sqlstr  =   ""
        sqlstr  =   "update fs_fc74 set flag='*' where afc001='" + TradeContext.userNo + "'"

        #===�����������б����ֶ�,�ź��޸�===
        sqlstr = sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

        if( AfaDBFunc.UpdateSqlCmt( sqlstr ) < 1 ):
            TradeContext.errorCode, TradeContext.errorMsg='0002', 'ɾ�����ҹ�ϵʧ��,����ʧ��'
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg + AfaDBFunc.sqlErrMsg )
            return False

    return True