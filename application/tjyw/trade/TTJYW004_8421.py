# -*- coding: gbk -*-
##################################################################
# 摘    要：TTJYW004_8421.py  通缴业务网银查询
# 当前版本：1.0
# 作    者：蔡永贵
# 完成日期：2011年03月08日
##################################################################
import TradeContext,AfaLoggerFunc,AfaFunc,AfaFlowControl,AfaDBFunc,HostContext,AfaHostFunc
from types import *

def SubModuleDoFst( ):
    try:
        AfaLoggerFunc.tradeInfo('--------------通缴业务网银查询开始--------------------')
        
        #柜员流水、中间业务流水、联系电话、交易机构、交易日期、交易时间、缴款人姓名、缴款金额 、缴款人账号、收款人账号、币种
        sql = "select bankserno,agentserialno,note1,brno,workdate,worktime,username,cast(amount as decimal(15,2)),draccno,craccno,currtype from afa_maintransdtl"
        sql = sql + " where agentserialno = '" + TradeContext.agentserialno + "'"
        sql = sql + " and        workdate = '" + TradeContext.workdate      + "'"
        
        #20120820陈浩注释，sysId 字段不需要，流水号和日期可唯一确定一笔交易
        #sql = sql + " and           sysid = '" + TradeContext.sysId         + "'"
        
        sql = sql + " and revtranf = '0' and bankstatus='0'"
        
        AfaLoggerFunc.tradeInfo('网银查询语句'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
        
        if records == None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"查询数据库失败"
            return False
        elif len(records) == 0:
            TradeContext.errorCode,TradeContext.errorMsg = "0001","没有该笔缴费记录"
            AfaLoggerFunc.tradeInfo('没有该笔缴费记录')
            return False
        else:
            TradeContext.O1TLSQ	   = str(records[0][0]).strip()                 #柜员流水
            TradeContext.SERIALNO  = str(records[0][1]).strip()                 #中间业务流水
            TradeContext.PHONE	   = str(records[0][2]).strip()                 #联系电话
            TradeContext.BANKNAME  = str(records[0][3]).strip()                 #交易机构
            TradeContext.TransDate = str(records[0][4]).strip()                 #交易日期
            TradeContext.TransTime = str(records[0][5]).strip()                 #交易时间
            TradeContext.PYRNAM	   = str(records[0][6]).strip()                 #缴款人姓名
            TradeContext.OCCAMT	   = str(records[0][7]).strip()                 #缴款金额
            TradeContext.PYRACCNO  = str(records[0][8]).strip()                 #缴款人账号
            TradeContext.REVACCNO  = str(records[0][9]).strip()                 #收款人账号
            TradeContext.CUR       = str(records[0][10]).strip().rjust(2,'0')   #币种

        #调用8810查询收款人账户信息
        HostContext.I1TRCD="8810"
        HostContext.I1SBNO=""
        HostContext.I1USID="999996"
        HostContext.I1AUUS=""
        HostContext.I1AUPS=""
        HostContext.I1WSNO=""
        HostContext.I1ACNO=TradeContext.REVACCNO
        HostContext.I1CYNO="01"
        HostContext.I1CFFG=""
        HostContext.I1PSWD=""
        HostContext.I1CETY=""
        HostContext.I1CCSQ=""
        HostContext.I1CTFG="0"
        AfaHostFunc.CommHost("8810")
        
        if(TradeContext.errorCode!="0000"):
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"到核心查询对公账户信息失败" 
            return False
        else:
            AfaLoggerFunc.tradeInfo( '>>>>查询账户信息成功' )
            TradeContext.REVNAME = HostContext.O1ACNM            #收款人户名
            TradeContext.REVBANK = HostContext.O1OPNT            #收款人开户行
        if len(TradeContext.PYRACCNO) != 0:
            #调用8810查询缴款人账户信息
            HostContext.I1TRCD="8810"
            HostContext.I1SBNO=""
            HostContext.I1USID="999996"
            HostContext.I1AUUS=""
            HostContext.I1AUPS=""
            HostContext.I1WSNO=""
            HostContext.I1ACNO=TradeContext.PYRACCNO
            HostContext.I1CYNO="01"
            HostContext.I1CFFG=""
            HostContext.I1PSWD=""
            HostContext.I1CETY=""
            HostContext.I1CCSQ=""
            HostContext.I1CTFG="0"
            AfaHostFunc.CommHost("8810")
            
            if(TradeContext.errorCode!="0000"):
                TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"到核心查询缴款人账户信息失败" 
                return False
            else:
                AfaLoggerFunc.tradeInfo( '>>>>查询账户信息成功' )
                TradeContext.SNDBNKNM = HostContext.O1OPNT            #收款人开户行
            
        #获取摘要代码
        if not AfaFunc.GetSummaryInfo( ):
            return False
        else:
            TradeContext.SUMMARY = TradeContext.__summaryName__               #摘要
            
        AfaLoggerFunc.tradeInfo('---------------通缴业务网银查询结束--------------------')
        
        return True 
    except  Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorMsg = str(e)
        AfaFlowControl.flowException( )
    
    
     
