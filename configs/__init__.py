# coding=utf-8

common_mysql_config = {
    'user': 'root',
    'passwd': '',
    'host': '127.0.0.1',
    'db': 'autotrade',
    'connect_timeout': 3600,
    'charset': 'utf8'
}

yongjinbao_config = {"account": "帐号", "password": "加密后的密码"}

guangfa_config = {"username": "加密的客户号", "password": "加密的密码"}

yinghe_config = {"inputaccount": "客户号", "trdpwd": "加密后的密码"}

huatai_config = {"userName": "用户名", "servicePwd": "通讯密码", "trdpwd": "加密后的密码"}

xueqiu_config = {
    "username": "邮箱",
    "account": "手机号",
    "password": "加密后的密码",
    "portfolio_code": "组合代码(例:ZH818559)",
    "portfolio_market": "交易市场(例:us 或者 cn 或者 hk)"
}

global_config = {
    "response_format": {
        "int": [
            "current_amount", "enable_amount", "entrust_amount", "成交数量",
            "撤单数量", "委托数量", "股份可用", "买入冻结", "买出冻结", "当前持仓", "股份余额"
        ],
        "float": [
            "current_balance", "enable_balance", "fetch_balance",
            "market_value", "asset_balance", "av_buy_price", "cost_price",
            "income_balance", "market_value", "entrust_price",
            "business_amount", "business_price", "business_balance", "fare1",
            "occur_balance", "farex", "fare0", "occur_amount", "post_balance",
            "fare2", "fare3", "资金余额", "可用资金", "参考市值", "总资产", "股份参考盈亏", "委托价格",
            "参考盈亏", "参考市价", "参考市值"
        ]
    }
}

yjb_config = {
    "login_page": "https://jy.yongjinbao.com.cn/winner_gj/gjzq/",
    "login_api": "https://jy.yongjinbao.com.cn/winner_gj/gjzq/exchange.action",
    "verify_code_api":
    "https://jy.yongjinbao.com.cn/winner_gj/gjzq/user/extraCode.jsp",
    "prefix":
    "https://jy.yongjinbao.com.cn/winner_gj/gjzq/stock/exchange.action",
    "logout_api":
    "https://jy.yongjinbao.com.cn/winner_gj/gjzq/stock/exchange.action?function_id=20&login_type=stock",
    "login": {
        "function_id": 200,
        "login_type": "stock",
        "version": 200,
        "identity_type": "",
        "remember_me": "",
        "input_content": 1,
        "content_type": 0,
        "loginPasswordType": "B64",
        "disk_serial_id": "ST3250820AS",
        "cpuid": "-41315-FA76141D",
        "machinecode": "-41315-FA76141D"
    },
    "buy": {
        "service_type": "stock",
        "request_id": "buystock_302"
    },
    "sell": {
        "service_type": "stock",
        "request_id": "sellstock_302"
    },
    "position": {
        "request_id": "mystock_403"
    },
    "balance": {
        "request_id": "mystock_405"
    },
    "entrust": {
        "request_id": "trust_401",
        "sort_direction": 1,
        "deliver_type": "",
        "service_type": "stock"
    },
    "cancel_entrust": {
        "request_id": "chedan_304"
    },
    "current_deal": {
        "request_id": "bargain_402",
        "sort_direction": 1,
        "service_type": "stock"
    },
    "ipo_enable_amount": {
        "request_id": "buystock_300"
    },
    "exchangetype4stock": {
        "service_type": "stock",
        "function_id": "105"
    },
    "account4stock": {
        "service_type": "stock",
        "function_id": "407",
        "window_id": "StockMarketTrade"
    }
}

yh_config = {
    "login_page": "https://www.chinastock.com.cn/trade/webtrade/login.jsp",
    "login_api":
    "https://www.chinastock.com.cn/trade/LoginServlet?ajaxFlag=mainlogin",
    "heart_beat":
    "https://www.chinastock.com.cn/trade/AjaxServlet?ajaxFlag=heartbeat",
    "unlock":
    "https://www.chinastock.com.cn/trade/AjaxServlet?ajaxFlag=unlockscreen",
    "trade_api": "https://www.chinastock.com.cn/trade/AjaxServlet",
    "trade_info_page":
    "https://www.chinastock.com.cn/trade/webtrade/tradeindex.jsp",
    "verify_code_api":
    "https://www.chinastock.com.cn/trade/webtrade/verifyCodeImage.jsp",
    "prefix": "https://www.chinastock.com.cn",
    "logout_api":
    "https://www.chinastock.com.cn/trade/webtrade/commons/keepalive.jsp?type=go",
    "login": {
        "logintype_rzrq": 0,
        "orgid": "",
        "inputtype": "C",
        "identifytype": 0,
        "isonlytrade": 1,
        "trdpwdjtws": "",
        "Authplain9320": "",
        "Authsign9321": "",
        "certdata9322": "",
        "ftype": "bsn"
    },
    "position": {
        "service_jsp": "/trade/webtrade/stock/stock_zjgf_query.jsp",
        "service_type": 1
    },
    "balance": {
        "service_jsp": "/trade/webtrade/stock/stock_zjgf_query.jsp",
        "service_type": 2
    },
    "entrust": {
        "service_jsp": "/trade/webtrade/stock/stock_wt_query.jsp"
    },
    "buy": {
        "marktype": "",
        "ajaxFlag": "wt"
    },
    "sell": {
        "ajaxFlag": "wt"
    },
    "fundpurchase": {
        "ajaxFlag": "wt",
        "bsflag": 3
    },
    "fundredemption": {
        "ajaxFlag": "wt",
        "bsflag": 4
    },
    "fundsubscribe": {
        "ajaxFlag": "wt",
        "bsflag": 5
    },
    "fundsplit": {
        "ajaxFlag": "wt",
        "bsflag": 85
    },
    "fundmerge": {
        "ajaxFlag": "wt",
        "bsflag": 86
    },
    "cancel_entrust": {
        "ajaxFlag": "stock_cancel"
    },
    "current_deal": {
        "service_jsp": "/trade/webtrade/stock/stock_cj_query.jsp"
    },
    "account4stock": {
        "service_jsp": "/trade/webtrade/zhgl/holderQuery.jsp"
    }
}

xq_config = {
    "login_api": "https://xueqiu.com/user/login",
    "prefix": "https://xueqiu.com/user/login",
    "portfolio_url": "https://xueqiu.com/p/",
    "search_stock_url": "https://xueqiu.com/stock/p/search.json",
    "rebalance_url": "https://xueqiu.com/cubes/rebalancing/create.json",
    "history_url": "https://xueqiu.com/cubes/rebalancing/history.json",
    "referer": "https://xueqiu.com/p/update?action=holdings&symbol=%s"
}

ht_config = {
    "login_page": "https://service.htsc.com.cn/service/login.jsp",
    "login_api":
    "https://service.htsc.com.cn/service/loginAction.do?method=login",
    "trade_info_page":
    "https://service.htsc.com.cn/service/flashbusiness_new3.jsp?etfCode=",
    "verify_code_api":
    "https://service.htsc.com.cn/service/pic/verifyCodeImage.jsp",
    "prefix": "https://tradegw.htsc.com.cn",
    "logout_api": "https://service.htsc.com.cn/service/login.jsp?logout=yes",
    "login": {
        "loginEvent": 1,
        "topath": "null",
        "accountType": 1,
        "userType": "jy",
        "hddInfo": "ST3250820AS"
    },
    "position": {
        "cssweb_type": "GET_STOCK_POSITION",
        "function_id": 403,
        "exchange_type": "",
        "stock_account": "",
        "stock_code": "",
        "query_direction": "",
        "query_mode": 0,
        "request_num": 100,
        "position_str": ""
    },
    "balance": {
        "cssweb_type": "GET_FUNDS",
        "function_id": 405,
        "identity_type": "",
        "money_type": ""
    },
    "entrust": {
        "cssweb_type": "GET_CANCEL_LIST",
        "function_id": 401,
        "exchange_type": "",
        "stock_account": "",
        "stock_code": "",
        "query_direction": "",
        "sort_direction": 0,
        "request_num": 100,
        "position_str": ""
    },
    "buy": {
        "cssweb_type": "STOCK_BUY",
        "function_id": 302,
        "exchange_type": "",
        "stock_account": "",
        "stock_code": "",
        "query_direction": "",
        "sort_direction": 0,
        "request_num": 100,
        "identity_type": "",
        "entrust_bs": 1
    },
    "sell": {
        "cssweb_type": "STOCK_SALE",
        "function_id": 302,
        "exchange_type": "",
        "stock_account": "",
        "stock_code": "",
        "query_direction": "",
        "sort_direction": 0,
        "request_num": 100,
        "identity_type": "",
        "entrust_bs": 2
    },
    "cancel_entrust": {
        "cssweb_type": "STOCK_CANCEL",
        "function_id": 304,
        "exchange_type": "",
        "stock_code": "",
        "identity_type": "",
        "entrust_bs": 2,
        "batch_flag": 0
    },
    "exchangebill": {
        "cssweb_type": "GET_EXCHANGEBILL",
        "request_num": 100,
        "end_date": "",
        "start_date": "",
        "exchange_type": "",
        "stock_code": "",
        "deliver_type": 1,
        "query_direction": "",
        "function_id": 308,
        "stock_account": "",
        "position_str": ""
    }
}

gf_config = {
    "login_api": "https://trade.gf.com.cn/login",
    "login_page": "https://trade.gf.com.cn/",
    "verify_code_api": "https://trade.gf.com.cn/yzm.jpgx",
    "prefix": "https://trade.gf.com.cn/entry",
    "logout_api": "https://trade.gf.com.cn/entry",
    "login": {
        "authtype": 2,
        "disknum": "1SVEYNFA915146",
        "loginType": 2,
        "origin": "web"
    },
    "balance": {
        "classname": "com.gf.etrade.control.StockUF2Control",
        "method": "queryAssert"
    },
    "position": {
        "classname": "com.gf.etrade.control.StockUF2Control",
        "method": "queryCC",
        "request_num": 500,
        "start": 0,
        "limit": 10
    },
    "entrust": {
        "classname": "com.gf.etrade.control.StockUF2Control",
        "method": "queryDRWT",
        "action_in": 1,
        "request_num": 100,
        "query_direction": 0,
        "start": 0,
        "limit": 10
    },
    "cancel_entrust": {
        "classname": "com.gf.etrade.control.StockUF2Control",
        "method": "cancel",
        "exchange_type": 1,
        "batch_flag": 0
    },
    "accountinfo": {
        "classname": "com.gf.etrade.control.FrameWorkControl",
        "method": "getMainJS"
    },
    "buy": {
        "classname": "com.gf.etrade.control.StockUF2Control",
        "method": "entrust",
        "entrust_bs": 1
    },
    "sell": {
        "classname": "com.gf.etrade.control.StockUF2Control",
        "method": "entrust",
        "entrust_bs": 2
    },
    "cnjj_apply": {
        "classname": "com.gf.etrade.control.StockUF2Control",
        "method": "CNJJSS",
        "entrust_bs": 1
    },
    "cnjj_redeem": {
        "classname": "com.gf.etrade.control.StockUF2Control",
        "method": "CNJJSS",
        "entrust_bs": 2
    },
    "fundsubscribe": {
        "classname": "com.gf.etrade.control.SHLOFFundControl",
        "method": "assetSecuprtTrade",
        "entrust_bs": 1
    },
    "fundpurchase": {
        "classname": "com.gf.etrade.control.SHLOFFundControl",
        "method": "assetSecuprtTrade",
        "entrust_bs": 1
    },
    "fundredemption": {
        "classname": "com.gf.etrade.control.StockUF2Control",
        "method": "doDZJYEntrust",
        "entrust_bs": 2
    },
    "fundmerge": {
        "classname": "com.gf.etrade.control.SHLOFFundControl",
        "method": "assetSecuprtTrade",
        "entrust_bs": ""
    },
    "fundsplit": {
        "classname": "com.gf.etrade.control.StockUF2Control",
        "method": "doDZJYEntrust",
        "entrust_bs": ""
    },
    "nxbQueryPrice": {
        "classname": "com.gf.etrade.control.NXBUF2Control",
        "method": "nxbQueryPrice"
    },
    "nxbentrust": {
        "classname": "com.gf.etrade.control.NXBUF2Control",
        "method": "nxbentrust"
    },
    "nxbQueryDeliver": {
        "classname": "com.gf.etrade.control.NXBUF2Control",
        "method": "nxbQueryDeliver"
    },
    "nxbQueryHisDeliver": {
        "classname": "com.gf.etrade.control.NXBUF2Control",
        "method": "nxbQueryHisDeliver"
    },
    "nxbQueryEntrust": {
        "classname": "com.gf.etrade.control.NXBUF2Control",
        "method": "nxbQueryEntrust"
    },
    "queryOfStkCodes": {
        "classname": "com.gf.etrade.control.NXBUF2Control",
        "method": "queryOfStkCodes"
    },
    "queryNXBOfStock": {
        "classname": "com.gf.etrade.control.NXBUF2Control",
        "method": "queryNXBOfStock"
    },
    "nxbentrustcancel": {
        "classname": "com.gf.etrade.control.NXBUF2Control",
        "method": "nxbentrustcancel"
    },
    "exchangebill": {
        "classname": "com.gf.etrade.control.StockUF2Control",
        "method": "queryDeliver",
        "request_num": 50,
        "query_direction": 0,
        "start_date": "",
        "end_date": "",
        "deliver_type": 1
    },
    "queryStockInfo": {
        "classname": "com.gf.etrade.control.StockUF2Control",
        "method": "getStockHQ"
    }
}
