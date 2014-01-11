# -*- coding: gbk -*-
###############################################################################
# 摘    要：代收非税_签到
#
# 当前版本：1.0
# 作    者：XZH
# 完成日期：2008年3月8日
###############################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaDBFunc, AfaLoggerFunc, sys, os
from types import *

##########################################签到##########################################
def Ahdx_Login():

    try:
        sqlStr = "SELECT STATUS FROM ABDT_UNITINFO WHERE"
        
        #begin 20100528 蔡永贵修改
        #sqlStr = sqlStr + " APPNO = '"      + 'AG2008'  + "'"
        sqlStr = sqlStr + " APPNO in ('AG2008','AG2012')"
        #end
        
        sqlStr = sqlStr + " AND AGENTTYPE IN ('1','2')"

        #AfaLoggerFunc.tradeInfo(sqlStr)

        records = AfaDBFunc.SelectSql( sqlStr )
        if (records==None or len(records) < 0):
            AfaLoggerFunc.tradeInfo('>>>处理结果:签到失败,数据库异常')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","签到失败,数据库异常"
            sys.exit(1)

        elif ( len(records) == 0 ):
            AfaLoggerFunc.tradeInfo('>>>处理结果:没有发现该单位信息,不能签到')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","没有发现该单位信息,不能签到"
            sys.exit(1)


        sqlStr = "UPDATE ABDT_UNITINFO SET STATUS='1' WHERE"
        
        #begin 20100528 蔡永贵修改
        #sqlStr = sqlStr + " APPNO = '"      + 'AG2008'  + "'"
        sqlStr = sqlStr + " APPNO in ('AG2008','AG2012')"
        #end
        
        sqlStr = sqlStr + " AND AGENTTYPE IN ('1','2')"

        retcode = AfaDBFunc.UpdateSqlCmt( sqlStr )
        if (retcode==None or retcode <= 0):
            AfaLoggerFunc.tradeInfo('>>>处理结果:签到失败,数据库异常')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","签到失败,数据库异常"
            sys.exit(1)

        AfaLoggerFunc.tradeInfo('>>>处理结果:签到成功')

    except Exception, e:
        AfaLoggerFunc.tradeInfo(str(e))
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001",str(e)
        sys.exit(1)
        
###########################################主函数###########################################
if __name__=='__main__':
    AfaLoggerFunc.tradeInfo('>>>非税签到')
    Ahdx_Login()
