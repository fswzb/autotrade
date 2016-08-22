# coding: utf-8
'''

　　判断行情热点是否存在延续性，通常可以观察以下几种特征：

　　一、通过对大盘的带动效应研判最简单的方法是观察热点对大盘的带动效应，如果热点板块振臂一呼，迅速带动大盘放量上涨，市场反应积极，说明热点的出现正当其时，是行情所需，可以参与；反之，则需谨慎。研判大盘的反应，还应注意两点：一是大盘的上涨必须放量，确保人气已被激发，无量上涨，回调居多；二是在长期的熊市中，热点产生初期，对大盘的带动效应并不明显，往往热点需要连涨2-3日，市场才苏醒过来，这时需要参考其他条件综合考虑。

　　二、通过同板块的呼应度研判主力发动行情是有备而来，多半会仔细研究大盘状态、同板块股票的上涨潜力，在拉升的同时，也非常在意同板块股票的反应。如果反应积极，跟风热烈，可能会继续拉升；反之，如果市场反应不积极，一般不会孤军深入，贸然承担市场风险。板块股票呼应度如何，关键还是取决于主力机构的建仓状况、技术状态等。作为普通投资者，在观察板块呼应度的同时，应重点研究其中有多少股票从技术上看具体连续走强的条件，当板块中具备连续上涨条件的股票寥寥无几时，还是谨慎为炒。

　　三、通过热点启动的次数进行研判在建仓初期一段时间内，比如最近1-3个月，某些板块的股票可能会多次表现，但多数无功而返。反复表现过的板块股票，应该引起我们的充分重视，这往往是行情即将产生的信号。当主力通过反复振荡，吸足筹码后，真正的行情就会来临。判断振荡吸筹的方法是看股票的底部是否抬高，底部逐渐抬高、成交量逐渐放大、技术上逐渐向好，此时真正启动的可性度较高。

　　四、通过龙头股的阻力位进行研判热门板块的产生固然是适应了行情的需要，但龙头股的激发作用也不可小视。一般规律是，如果龙头股上档无明显的阻力，板块股票的跟风会相对积极；反之，当龙头股上档有明显的阻力时，既便其执意突破，但其他市场主力从谨慎性原则出发，也不会跟风太紧密。市场跟风的弱势效应，反过来也会阻碍龙头股行情的深入发展。

　　五、通过龙头股启动初期的资金流向进行研判热点的持续时间是同主力做多的决心成正比的，一个热点启动时，龙头股的主力资金必须是流入的（参考DDX指标），而且流入的量越大，该热点的持续时间就越长，如果同板块中多只个股都出现资金巨量流入，则说明热点已被各主力广泛认可，成为阶段行情亮点的可能性极大。反之，若热点启动初期，龙头股的主力资金是流出的，那么该热点遭遇昙花一现就是大概率事件了。


用市场下跌家数，与跌停家数判断市场危险程度，用市场上涨家数，与涨停家数，判断市场狂热程度，用涨停数曲线，判断市场可持续程度，都是非常有效的规避风险的办法。

一般普通止损止盈基本都是使用以下几个条件合并判断
a、高位下撤
b、macd死叉
c、预设利润到达
d、大幅高开
e、大幅低开

我试验了一种其他方法，效果还可以，分享一下、条件如下
a、每当高开2% - 4% 加一成仓
b、盈利达到4%以上，每处于该状态一天，减一成仓
c、盈利达到8%以上，每处于该状态一天，减三成仓
d、当大盘rsi及ar因子在（30、4）以下时，9%盈利即清仓。

'''
