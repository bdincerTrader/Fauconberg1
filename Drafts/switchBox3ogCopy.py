from cloudquant.interfaces import Strategy
import time, random

#845972 #31069132
class Gr8Scripteb9137832684455794101021b5d15620(Strategy):
    __script_name__ = 'switchBox3ogCopy'
    
    #tickerItr = ['NIO', 'NAT', 'ARR', 'AMCR', 'AMC', 'SWN', 'BTG', 'BOIL', 'GOLD', 'KGC', 'KMI', 'NOK', 'ITUB',  'KMI', 'AGNC', 'RIG', 'ET', 'SPY']
    #tickerItr = ['FCEL','ARR','LUMN', 'UEC', 'BTG','UVXY','AMC','BOIL','BKNG','SWN','MELI','MSTR','KGC','NU','NOK','SPY']
    #tickerItr = ['FCEL','ARR','LUMN', 'UEC', 'BTG','UVXY','AMC','BOIL','AMC','SWN','SIRI','MSTR','KGC','NU','NOK','SPY']
    #tickerItr = ['FCEL','ARR','LUMN', 'UEC', 'BTG','UVXY','AMC','BOIL','AMC','SWN','SIRI','CMG','KGC','NU','NOK','SPY']
    #tickerItr = ['BTG','FCEL','LUMN','UEC','UVXY','SWN','SIRI','CMG','KGC','NU','NOK','SPY']
    tickerItr = ['FCEL','ARR','LUMN', 'UEC', 'BTG','UVXY','AMC','NAT','BOIL','SWN','SIRI','KGC','NU','NOK','SPY']
    #tickerItr = ['BTG','FCEL','LUMN','UEC','UVXY','NU','AMC','SPY']
    allocationKey=accKey=intvRate=TtlNet=allocationStatus=CancelBooks=strategyKey=LongCap=LongUnit=LongUnits=LongShares=LongRlz=LongUrl=LongTtl=ShrtCap=ShrtUnit=ShrtUnits=ShrtShares=ShrtRlz=ShrtUrl=ShrtTtl=TradeMatch=TradePendTtl=TradePendBuy=TradePendSell=HedgeLong=0
    allocationModel, testRTE, riskMax = 10, 1.0057, 123
    plMaxLoss=-riskMax*0.20
    plUnrlRTE=riskMax*0.001
    upperBand=riskMax*.01
    lowerBand=-riskMax*.01
    bandMult=riskMax*.01
    intervalRate=[0]
    tkrAlpha = [[unit, 0] for unit in tickerItr]

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol in Gr8Scripteb9137832684455794101021b5d15620.tickerItr
     
    def __init__(self, **params):
        if('riskAllocation' in params):
            print(params['riskAllocation'])
            Gr8Scripteb9137832684455794101021b5d15620.riskMax=params['riskAllocation']
            Gr8Scripteb9137832684455794101021b5d15620.plMaxLoss=-Gr8Scripteb9137832684455794101021b5d15620.riskMax*0.20
            Gr8Scripteb9137832684455794101021b5d15620.plUnrlRTE=Gr8Scripteb9137832684455794101021b5d15620.riskMax*0.001
            Gr8Scripteb9137832684455794101021b5d15620.upperBand=Gr8Scripteb9137832684455794101021b5d15620.riskMax*0.01
            Gr8Scripteb9137832684455794101021b5d15620.lowerBand=-Gr8Scripteb9137832684455794101021b5d15620.riskMax*0.01
            Gr8Scripteb9137832684455794101021b5d15620.bandMult=Gr8Scripteb9137832684455794101021b5d15620.riskMax*0.01
    
    def on_start(self, md, order, service, account):
        self.rejectChecker=0
        self.yesterdayPrice = max(md.stat.prev_close, md.L1.open)
        if(self.yesterdayPrice == 0):
            self.yesterdayPrice = 500
        self.entryLevel=self.exitPrice=self.positionSize=self.spyQTY=0
        self.cancelOrderBook=self.checkPendingBook=[]
        self.maxAllocate=int(self.yesterdayPrice*1.10)
        self.delay = service.time_interval(seconds=5)
        self.twentyMin = service.time_interval(minutes=20)

        # type = service.symbol_list.in_list(service.symbol_list.get_handle('0e788f9d-4c44-4724-8581-21ef7e5dad09'), self.symbol)
        if(Gr8Scripteb9137832684455794101021b5d15620.intervalRate[0]==0):
            print("PL MODEL: {}.{}\RISKMAX: {}\tRTE: {}\tTRADE DATE: {}".format(Gr8Scripteb9137832684455794101021b5d15620.allocationModel, Gr8Scripteb9137832684455794101021b5d15620.upperBand, Gr8Scripteb9137832684455794101021b5d15620.riskMax, Gr8Scripteb9137832684455794101021b5d15620.testRTE, service.time_to_string(service.system_time)))
        Gr8Scripteb9137832684455794101021b5d15620.intervalRate[0]=0.0001
        
        print(Gr8Scripteb9137832684455794101021b5d15620.tkrAlpha)
        
        i=0
        for unit in Gr8Scripteb9137832684455794101021b5d15620.tkrAlpha:
            if(Gr8Scripteb9137832684455794101021b5d15620.tkrAlpha[i][0]==self.symbol):
                Gr8Scripteb9137832684455794101021b5d15620.tkrAlpha[i][1]=md.stat.beta
                break
            i+=1

        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=5), repeat_interval=service.time_interval(seconds=10), timer_id="Allocate")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=16), timer_id = "eod_1")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=12), timer_id = "eod_2")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=5), timer_id = "eod_3")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=3), timer_id = "eod_4")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=2), timer_id = "eod_5")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=1), timer_id = "eod_6")
        self.liquid_time = md.market_open_time + service.time_interval(minutes=21)
        self.illiquid_time = md.market_close_time - service.time_interval(minutes=30)

    
    def on_timer(self, event, md, order, service, account):
        

        def case_all(ticker):
            longUnit=longUnits=shrtUnit=shrtUnits=pendingBuy=pendingSell=longRlz=longCash=longUnrl=shrtRlz=shrtCash=shrtUnrl=0
            
            if(account[ticker].realized_pl.entry_pl!=0 or account[ticker].realized_pl.mtm_pl!=0):

                cpyDict = [account[ticker].realized_pl]
                for key in cpyDict:

                    item = str(key)
                    splt_itm = item.split("entry_execution")
                    mtchTrades=-1
                    for itm in splt_itm:
                        mtchTrades+=1
                    Gr8Scripteb9137832684455794101021b5d15620.TradeMatch+=mtchTrades
                    
            Gr8Scripteb9137832684455794101021b5d15620.LongRlz+=account[ticker].realized_pl.entry_pl_long
            Gr8Scripteb9137832684455794101021b5d15620.ShrtRlz+=account[ticker].realized_pl.entry_pl_short
            longPos=longUnits=longCash=longUnrl=xQuantityLong=shrtPos=shrtUnits=shrtCash=shrtUnrl=xQuantityShrt=0
            
            if(len(account[ticker].position.inventory)>0):
                ctInv = len(account[ticker].position.inventory)
                while(ctInv>0):
                    ctInv-=1
                    
                    if(account[ticker].position.inventory[ctInv].execution.side==1):
                        longPos=1
                        longUnits+=1
                        longCash=account[ticker].position.capital_long
                        longUnrl=account[ticker].unrealized_pl.entry_pl
                        xQuantityLong+=account[ticker].position.inventory[ctInv].execution.shares
                        xPriceLong=account[ticker].position.inventory[ctInv].execution.price
                        xTimeLong=account[ticker].position.inventory[ctInv].execution.time
                        pass
                    elif(account[ticker].position.inventory[ctInv].execution.side==-1):
                        shrtPos=1
                        shrtUnits+=1
                        shrtCash=account[ticker].position.capital_short
                        shrtUnrl=account[ticker].unrealized_pl.entry_pl
                        tkrShort=account[ticker].position.inventory[ctInv].execution.symbol
                        shortIndicator=account[ticker].position.inventory[ctInv].execution.side
                        xQuantityShrt+=account[ticker].position.inventory[ctInv].execution.shares
                        xPriceShort=account[ticker].position.inventory[ctInv].execution.price
                        xTimeShort=account[ticker].position.inventory[ctInv].execution.time
                        pass
                    
            Gr8Scripteb9137832684455794101021b5d15620.LongCap+=longCash
            Gr8Scripteb9137832684455794101021b5d15620.LongUnit+=longPos
            Gr8Scripteb9137832684455794101021b5d15620.LongUnits+=longUnits
            Gr8Scripteb9137832684455794101021b5d15620.LongShares+=xQuantityLong
            Gr8Scripteb9137832684455794101021b5d15620.LongUrl+=longUnrl
            Gr8Scripteb9137832684455794101021b5d15620.LongTtl=Gr8Scripteb9137832684455794101021b5d15620.LongRlz+Gr8Scripteb9137832684455794101021b5d15620.LongUrl
            Gr8Scripteb9137832684455794101021b5d15620.ShrtCap+=shrtCash
            Gr8Scripteb9137832684455794101021b5d15620.ShrtUnit+=shrtPos
            Gr8Scripteb9137832684455794101021b5d15620.ShrtUnits+=shrtUnits
            Gr8Scripteb9137832684455794101021b5d15620.ShrtShares+=xQuantityShrt
            Gr8Scripteb9137832684455794101021b5d15620.ShrtUrl+=shrtUnrl
            Gr8Scripteb9137832684455794101021b5d15620.ShrtTtl=Gr8Scripteb9137832684455794101021b5d15620.ShrtRlz+Gr8Scripteb9137832684455794101021b5d15620.ShrtUrl
            pendingSell=pendingBuy=0
            
            ctPnd=len(account[ticker].pending.orders)
            while(ctPnd>0):
                ctPnd-=1
                pendingExecution=account[ticker].pending.orders

                if(pendingExecution[ctPnd].shares<0):
                    pendingSell+=1
                    pass
                elif(pendingExecution[ctPnd].shares>0):
                    pendingBuy+=1
                    pass
            Gr8Scripteb9137832684455794101021b5d15620.TradePendBuy+=pendingBuy
            Gr8Scripteb9137832684455794101021b5d15620.TradePendSell+=pendingSell
            Gr8Scripteb9137832684455794101021b5d15620.TradePendTtl=Gr8Scripteb9137832684455794101021b5d15620.TradePendBuy+Gr8Scripteb9137832684455794101021b5d15620.TradePendSell

        def case_info():
            ctPositionLong=ctPositionShort=releaseItem=0
            xPriceLong=xPriceShort=[]
            
            ctInventoryItem = len(account[self.symbol].position.inventory)
            inventoryItem = account[self.symbol].position.inventory

            while(ctInventoryItem>0):
                ctInventoryItem-=1
                executedVars = inventoryItem[ctInventoryItem]
                
                if(inventoryItem[ctInventoryItem].execution.side==1):
                    ctPositionLong+=1
                    xPriceLong.append(inventoryItem[ctInventoryItem].execution.price)
                    pass
                elif(inventoryItem[ctInventoryItem].execution.side==-1):
                    ctPositionShort+=1
                    xPriceShort.append(inventoryItem[ctInventoryItem].execution.price)
                    pass
                
            ctPending=len(account[self.symbol].pending.orders)
            reRouteInventory=account[self.symbol].pending.orders
            while(ctPending>0):
                ctPending-=1
                pendingExecution=reRouteInventory[ctPending]
                if(pendingExecution.shares<0):
                    if(min(xPriceLong)<md.L1.bid and event.timestamp<self.illiquid_time):
                        infoCase = order.cancel(order_id=pendingExecution.order_id)
                        pass
                    pass
                elif(pendingExecution.shares>0):
                    pass

        def case_close_book():
            
            ctPending=len(account[self.symbol].pending.orders)
            pendingInventory=account[self.symbol].pending.orders
            while(ctPending>0):
                ctPending-=1
                cxlExecution=pendingInventory[ctPending]
                if(cxlExecution.shares<0 and event.timestamp<self.illiquid_time):
                    order.cancel(order_id=cxlExecution.order_id)
                    pass
                elif(cxlExecution.shares>0):
                    pass

        def case_close_strategy():
        
            ctPending=len(account[self.symbol].pending.orders)
            pendingExecution=account[self.symbol].pending.orders
            while(ctPending>0):
                ctPending-=1
                clsUnit = pendingExecution[ctPending]

                if(clsUnit.shares<0 and event.timestamp<self.illiquid_time):
                    order.cancel(order_id=clsUnit.order_id)
                    pass
                elif(clsUnit.shares>0):
                    order.cancel(order_id=clsUnit.order_id)
                    pass
        
        if(self.rejectChecker==1):
            return            
        
        if(Gr8Scripteb9137832684455794101021b5d15620.strategyKey==1 and len(account[self.symbol].pending.orders)==0 and len(account[self.symbol].position.inventory)==0):
            return
            
        if(Gr8Scripteb9137832684455794101021b5d15620.strategyKey==1):
            case_close_strategy()
            pass
        
        if(account.realized_mtm_pl+account.unrealized_entry_pl<Gr8Scripteb9137832684455794101021b5d15620.plMaxLoss and Gr8Scripteb9137832684455794101021b5d15620.strategyKey==0):
            Gr8Scripteb9137832684455794101021b5d15620.strategyKey=1
            case_close_strategy()
            pass
        
        if(Gr8Scripteb9137832684455794101021b5d15620.strategyKey==1 and account.pending_capital_long==0 and account.open_capital_long==0 and len(account.open_symbols)==0):
            service.terminate()
        
        if(account[self.symbol].unrealized_pl.entry_pl>Gr8Scripteb9137832684455794101021b5d15620.plUnrlRTE):
            case_info()
            pass
        
        
        i=0
        if(event.timestamp<self.illiquid_time):
            for unitsCancelled in self.cancelOrderBook:
                mktPrice = max(md.L1.ask, md.L1.last)-(random.randint(0, 50)/10000)
                if(unitsCancelled[3]==112):
                    rePriced = order.algo_sell(unitsCancelled[0], algorithm='5a8a9f9d-22a5-4155-87e7-4ebe8024a97b', intent='decrease', order_quantity=-unitsCancelled[1], price=mktPrice, user_key=112, allow_multiple_pending=40)
                    # rePriced = self._sell_limit_order_gs_smart(event, md, order, service, account, unitsCancelled[0], -unitsCancelled[1], mktPrice, 112, 'decrease')
                    self.cancelOrderBook.pop(i)
                    i+=1
                    pass

        if(self.symbol=="SPY"):
            self._reset_comm(md)  
            allocation_key=self._allocation_key(md)

            for ticker in Gr8Scripteb9137832684455794101021b5d15620.tickerItr:
                case_all(ticker)
        
                if(account[ticker].position.capital_long>0):
                    self._hedge_positions(ticker, account[ticker].position.capital_long)
                    pass

            ping_book_stat=self._book_status(md, account, order, service, event)
            ping_pl_stat=self._clear_book_status()
            ping_hedge_stat=self._adjust_hedges(event, md, order, service, account)
            pass

        if(Gr8Scripteb9137832684455794101021b5d15620.allocationStatus==1):
            case_close_book()
            pass
        
        if(event.timer_id=="Allocate" and self.symbol!="SPY" and Gr8Scripteb9137832684455794101021b5d15620.allocationKey==1 and event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time):
            self._check_indicators(event, md, order, service, account)
            pass
            
        if(event.timer_id=="eod_1" or event.timer_id=="eod_2" or event.timer_id=="eod_3" or event.timer_id=="eod_4" or event.timer_id=="eod_5" or event.timer_id=="eod_6"):
            self.eod_functions(event, md, order, service, account)
            pass
        

    def on_fill(self, event, md, order, service, account):
        
        if(event.user_tag==111):
            randAdjust=random.randint(0, 50)/10000
            self.exitPrice = event.price*Gr8Scripteb9137832684455794101021b5d15620.testRTE-randAdjust
            if(event.intent in ["increase", "init"] and service.instruction_id == event.instruction_id):
                offerInventory = order.algo_sell(event.symbol, algorithm='5a8a9f9d-22a5-4155-87e7-4ebe8024a97b', intent='decrease', order_quantity= event.shares, price=self.exitPrice, user_key=112, allow_multiple_pending=40)
                pass
                #offerInventory = self._sell_limit_order_gs_smart(event, md, order, service, account, event.symbol, event.shares, self.exitPrice, 112, 'decrease')
            pass




    def on_cancel(self, event, md, order, service, account):

        if(event.user_tag==112 and event.timestamp<self.illiquid_time):
            evtUnit=[event.symbol, event.shares, event.price, event.user_tag]
            self.cancelOrderBook.append(evtUnit)
            Gr8Scripteb9137832684455794101021b5d15620.CancelBooks+=1
            return

    def _clear_book_status(self):
        if(Gr8Scripteb9137832684455794101021b5d15620.TtlNet>Gr8Scripteb9137832684455794101021b5d15620.upperBand):
            Gr8Scripteb9137832684455794101021b5d15620.upperBand=Gr8Scripteb9137832684455794101021b5d15620.TtlNet+Gr8Scripteb9137832684455794101021b5d15620.bandMult
            Gr8Scripteb9137832684455794101021b5d15620.lowerBand=Gr8Scripteb9137832684455794101021b5d15620.TtlNet-Gr8Scripteb9137832684455794101021b5d15620.bandMult
            Gr8Scripteb9137832684455794101021b5d15620.allocationStatus=1
        elif(Gr8Scripteb9137832684455794101021b5d15620.TtlNet<Gr8Scripteb9137832684455794101021b5d15620.lowerBand):
            Gr8Scripteb9137832684455794101021b5d15620.upperBand=Gr8Scripteb9137832684455794101021b5d15620.TtlNet+Gr8Scripteb9137832684455794101021b5d15620.bandMult
            Gr8Scripteb9137832684455794101021b5d15620.lowerBand=Gr8Scripteb9137832684455794101021b5d15620.TtlNet-Gr8Scripteb9137832684455794101021b5d15620.bandMult
            Gr8Scripteb9137832684455794101021b5d15620.allocationStatus=1
        else:
            Gr8Scripteb9137832684455794101021b5d15620.allocationStatus=0
        return Gr8Scripteb9137832684455794101021b5d15620.allocationStatus
    
    def _hedge_positions(self, ticker, long_capital):
        for unit in Gr8Scripteb9137832684455794101021b5d15620.tkrAlpha:
            if(unit[0]==ticker):
                Gr8Scripteb9137832684455794101021b5d15620.HedgeLong+=(long_capital*unit[1])
                return Gr8Scripteb9137832684455794101021b5d15620.HedgeLong

    def _reset_comm(self, md):
        Gr8Scripteb9137832684455794101021b5d15620.LongCap=Gr8Scripteb9137832684455794101021b5d15620.LongUnit=Gr8Scripteb9137832684455794101021b5d15620.LongUnits=Gr8Scripteb9137832684455794101021b5d15620.LongShares=Gr8Scripteb9137832684455794101021b5d15620.LongRlz=Gr8Scripteb9137832684455794101021b5d15620.LongUrl=Gr8Scripteb9137832684455794101021b5d15620.LongTtl=0
        Gr8Scripteb9137832684455794101021b5d15620.ShrtCap=Gr8Scripteb9137832684455794101021b5d15620.ShrtUnit=Gr8Scripteb9137832684455794101021b5d15620.ShrtUnits=Gr8Scripteb9137832684455794101021b5d15620.ShrtShares=Gr8Scripteb9137832684455794101021b5d15620.ShrtRlz=Gr8Scripteb9137832684455794101021b5d15620.ShrtUrl=Gr8Scripteb9137832684455794101021b5d15620.ShrtTtl=0
        Gr8Scripteb9137832684455794101021b5d15620.TradeMatch=Gr8Scripteb9137832684455794101021b5d15620.TradePendTtl=Gr8Scripteb9137832684455794101021b5d15620.TradePendBuy=Gr8Scripteb9137832684455794101021b5d15620.TradePendSell=Gr8Scripteb9137832684455794101021b5d15620.TtlNet=Gr8Scripteb9137832684455794101021b5d15620.HedgeLong=0
        Gr8Scripteb9137832684455794101021b5d15620.intervalRate.append(md.L1.percent_change_from_open)
        return Gr8Scripteb9137832684455794101021b5d15620.intervalRate
    
    def _allocation_key(self, md):
        intervalChange = Gr8Scripteb9137832684455794101021b5d15620.intervalRate[-1]-Gr8Scripteb9137832684455794101021b5d15620.intervalRate[-2]
        if(intervalChange>0):
            Gr8Scripteb9137832684455794101021b5d15620.allocationKey=0
            Gr8Scripteb9137832684455794101021b5d15620.accKey-=1
            pass
        else:
            Gr8Scripteb9137832684455794101021b5d15620.allocationKey=1
            Gr8Scripteb9137832684455794101021b5d15620.accKey+=1
            pass
            
        if(md.L1.percent_change_from_open!=0):
            Gr8Scripteb9137832684455794101021b5d15620.intvRate = intervalChange/md.L1.percent_change_from_open
            pass
        else:
            Gr8Scripteb9137832684455794101021b5d15620.intvRate = 0
            pass
        return Gr8Scripteb9137832684455794101021b5d15620.allocationKey
        
    def _book_status(self, md, account, order, service, event):
        TtlRlzd=Gr8Scripteb9137832684455794101021b5d15620.LongRlz+Gr8Scripteb9137832684455794101021b5d15620.ShrtRlz
        TtlUnrl=Gr8Scripteb9137832684455794101021b5d15620.LongUrl+Gr8Scripteb9137832684455794101021b5d15620.ShrtUrl
        Gr8Scripteb9137832684455794101021b5d15620.TtlNet=TtlRlzd+TtlUnrl
        return len(Gr8Scripteb9137832684455794101021b5d15620.intervalRate)

    def _adjust_hedges(self, event, md, order, service, account):
        hedgeTwo = Gr8Scripteb9137832684455794101021b5d15620.HedgeLong
        if(Gr8Scripteb9137832684455794101021b5d15620.allocationKey!=0):
            if(abs(Gr8Scripteb9137832684455794101021b5d15620.ShrtCap)<hedgeTwo):
                self.spyQTY = int((abs(Gr8Scripteb9137832684455794101021b5d15620.ShrtCap)-hedgeTwo)/400)
                if(self.spyQTY!=0):
                    if(account[self.symbol].position.shares>0):
                        short = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=abs(self.spyQTY), user_key=101)
                        #short = self._sell_market_gs_smart(event, md, order, service, account, self.symbol, abs(self.spyQTY), 101, 'decrease')
                        pass

                    elif(account[self.symbol].position.shares<0):
                        short = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=abs(self.spyQTY), user_key=101)
                        #short = self._sell_market_gs_smart(event, md, order, service, account, self.symbol, abs(self.spyQTY), 101, 'increase')
                        pass

                    elif(account[self.symbol].position.shares==0):
                        short = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='init', order_quantity=abs(self.spyQTY), user_key=101)
                        #short = self._sell_market_gs_smart(event, md, order, service, account, self.symbol, abs(self.spyQTY), 101, 'init')
                        pass

                    else:
                        pass
                    pass
        elif(Gr8Scripteb9137832684455794101021b5d15620.allocationKey!=1):        
            if(abs(Gr8Scripteb9137832684455794101021b5d15620.ShrtCap)>hedgeTwo):
                self.spyQTY = int((abs(Gr8Scripteb9137832684455794101021b5d15620.ShrtCap)-hedgeTwo)/400)
                if(self.spyQTY!=0):
                    if(account[self.symbol].position.shares>0):
                        shrtBalance = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=abs(self.spyQTY), user_key=102)
                        #shrtBalance = self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, abs(self.spyQTY), 102, 'increase')
                        pass
                    elif(account[self.symbol].position.shares<0):
                        shrtBalance = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(self.spyQTY), user_key=102)
                        #shrtBalance = self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, abs(self.spyQTY), 102, 'decrease')
                        pass

                    elif(account[self.symbol].position.shares==0):
                        shrtBalance = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='init', order_quantity=abs(self.spyQTY), user_key=102)
                        #shrtBalance = self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, abs(self.spyQTY), 102, 'init')
                        pass
                    else:
                        pass
                    pass

    def _check_indicators(self, event, md, order, service, account):

        def test_A(case1, case2):
            if(case1>case2):
                return 1
            else:
                return 0
            
        def test_B(case1, case2):
            if(case1>case2):
                return 0
            else:
                return 1
            
        barPointA = event.timestamp-1205000000
        barPointB = event.timestamp
        
        bar20m = md.bar.minute(start=barPointA, end=barPointB, include_extended=True, today_only=False)
        #ONMINUTEBAR
        if(len(bar20m.high)>15 and len(bar20m.low)>15 and len(bar20m.spread)>15 and len(bar20m.askvol)>15 and len(bar20m.bidvol)>15 and len(bar20m.close)>15 and len(bar20m.vwap)>15 and len(bar20m.open)>15 and len(bar20m.volume)>15):
            complexA=complexB=indication=-1
            #(1,0)chk12A
            chk12A=test_A(bar20m.bidvol[-1], bar20m.askvol[-1])
            #(0,1)chk12B
            chk12B=test_B(bar20m.bidvol[-1], bar20m.askvol[-1])
            #(1,0)chk13A
            chk13A=test_A(bar20m.bidvol[-1], bar20m.askvol[0])
            chk13B=test_A(bar20m.bidvol[-1], bar20m.askvol[10])
            chk13C=test_A(bar20m.bidvol[-1], bar20m.askvol[15])
            #(0,1)chk13b
            chk13x=test_B(bar20m.bidvol[-1], bar20m.askvol[0])
            chk13y=test_B(bar20m.bidvol[-1], bar20m.askvol[10])
            chk13z=test_B(bar20m.bidvol[-1], bar20m.askvol[15])
            #GATE1 and GATE2
            if(chk12A>0 and chk13A>0):
                complexA=-1
                complexB=0
                indication=2
                pass
            elif(chk12A>0 and chk13B>0):
                complexA=-1
                complexB=10
                indication=2
                pass
            elif(chk12A>0 and chk13C>0):
                complexA=-1
                complexB=15
                indication=2
                pass
            elif(chk12A>0 and chk13x>0):
                complexA=-1
                complexB=0
                indication=2
                pass
            elif(chk12A>0 and chk13y>0):
                complexA=-1
                complexB=10
                indication=2
                pass
            elif(chk12A>0 and chk13z>0):
                complexA=-1
                complexB=15
                indication=2
                pass
            elif(chk12B>0 and chk13A>0):
                complexA=-1
                complexB=0
                indication=2
                pass
            elif(chk12B>0 and chk13B>0):
                complexA=-1
                complexB=10
                indication=2
                pass
            elif(chk12B>0 and chk13C>0):
                complexA=-1
                complexB=15
                indication=2
                pass
            elif(chk12B>0 and chk13x>0):
                complexA=-1
                complexB=0
                indication=2
                pass
            elif(chk12B>0 and chk13y>0):
                complexA=-1
                complexB=10
                indication=2
                pass
            elif(chk12B>0 and chk13z>0):
                complexA=-1
                complexB=15
                indication=2
                pass
            while(indication>0):
                basePx = md.L1.last
                if((basePx-bar20m.low[-1])>0):
                    indication+=1
                    pass
                if((basePx-bar20m.vwap[-1])>0):
                    indication+=1
                    pass
                if((basePx-bar20m.open[-1])>0):
                    indication+=1
                    pass
                if((basePx-bar20m.close[-1])>0):
                    indication+=1
                    pass
                if(bar20m.low[-1]>bar20m.high[complexB]):
                    indication+=1
                    pass
                if(bar20m.low[-1]>bar20m.vwap[complexB]):
                    indication+=1
                    pass
                if(bar20m.low[-1]>bar20m.open[complexB]):
                    indication+=1
                    pass
                if(bar20m.open[-1]>bar20m.close[complexB]):
                    indication+=1
                    pass
                if(basePx>bar20m.high[complexB]):
                    indication+=1
                    pass
                if(basePx>bar20m.vwap[complexB]):
                    indication+=1
                    pass
                if(bar20m.spread[-1]>bar20m.spread[complexB]):
                    indication+=1
                    pass
                if(indication>=Gr8Scripteb9137832684455794101021b5d15620.allocationModel):
                    
                    #if(account.pending_capital_long>1000):
                    #    print(account.capital_used)
                    #    print(account.pending_capital_long)
                    
                    #if(md.L1.is_halted==true):
                    #    return
                    self.entryLevel = min(min(bar20m.open[:-15]), min(bar20m.close[:-15]))-(random.randint(0, 50)/10000)
                    self.positionSize= int(Gr8Scripteb9137832684455794101021b5d15620.riskMax/self.maxAllocate)+1

                    if(account[self.symbol].position.shares==0 and len(account[self.symbol].pending.orders)<40):
                        pricedBid = order.algo_buy(self.symbol, algorithm='8b976c72-20cd-49db-9121-db2e5ace3385', intent='increase', order_quantity=self.positionSize, price=self.entryLevel, user_key=111, allow_multiple_pending=40)  
                        #pricedBid = self._buy_limit_order_gs_smart(event, md, order, service, account, self.symbol, self.positionSize, self.entryLevel, 111, 'increase')
                        pass
                    complexA=0
                    break
                else:
                    self.checkPendingBook=[]
                    pendingExecution=account[self.symbol].pending.orders
                    ctPnd=len(pendingExecution)
                    if(ctPnd>19):
                        while(ctPnd>0):
                            ctPnd-=1
                            if(pendingExecution[ctPnd].shares<0):
                                pass
                            elif(pendingExecution[ctPnd].shares>0):
                                self.checkPendingBook.append([pendingExecution[ctPnd].symbol, pendingExecution[ctPnd].shares, round(pendingExecution[ctPnd].price, 3), round(pendingExecution[ctPnd].shares*pendingExecution[ctPnd].price, 2), pendingExecution[ctPnd].order_id])
                                pass
                        
                        ttlPendingCt=ttlShares=ttlNet=0
                        tickerOrderBox=[]
                        for unit in self.checkPendingBook:
                            ttlPendingCt+=1
                            ttlShares+=unit[1]
                            ttlNet+=unit[3]
                            tickerOrderBox.append([ unit[0], unit[4] ])
                        
                            if(ttlPendingCt>=30):
                                neTprice=ttlNet/ttlShares
                                for risk in range(7, 19, 1):
                                    chkCancel = order.cancel(order_id=tickerOrderBox[risk][1])
                                ttlPendingCt=0
                                break
                        pass
                    complexA=0
                    break
                complexA=0    
                break
            pass
        pass

    def eod_functions(self, event, md, order, service, account):

        if event.timer_id=="eod_6":
            service.terminate()
            pass
            
        if event.timer_id=="eod_1":
            if(len(account[self.symbol].pending.orders)>0):
                order.cancel(self.symbol)
                pass
            pass
                
        if event.timer_id=="eod_2":   
            if(account[self.symbol].position.shares>0):
                if(self.positionSize>0):
                    order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=account[self.symbol].position.shares, user_key=113)
                    # self._sell_market_gs_smart(event, md, order, service, account, self.symbol, account[self.symbol].position.shares, 113, 'decrease')
                    pass
                    
            if(account[self.symbol].position.shares<0):
                if(self.positionSize<0):
                    order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=103)
                    # self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, abs(account[self.symbol].position.shares), 103, 'decrease')
                    pass
                    
        if event.timer_id=="eod_3":
            if(self.symbol=="SPY"):
                if(account[self.symbol].position.shares>0):
                    order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=account[self.symbol].position.shares, user_key=113)
                    # self._sell_market_gs_smart(event, md, order, service, account, self.symbol, account[self.symbol].position.shares, 113, 'decrease')
                    pass
                if(account[self.symbol].position.shares<0):
                    order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=103)
                    # self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, abs(account[self.symbol].position.shares), 103, 'decrease')
                    pass

        if event.timer_id=="eod_4":
            if(account[self.symbol].position.shares>0):
                if(account[self.symbol].position.shares>4500):
                    positionClose=account[self.symbol].position.shares
                    while(positionClose>0):
                        positionClose-=2000
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=2000, user_key=113)
                        # self._sell_market_gs_smart(event, md, order, service, account, self.symbol, 2000, 113, 'decrease')
                    pass    
                else:
                    order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=account[self.symbol].position.shares, user_key=113)
                    # self._sell_market_gs_smart(event, md, order, service, account, self.symbol, account[self.symbol].position.shares, 113, 'decrease')
                    pass
            if(account[self.symbol].position.shares<0):
                order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=103)
                # self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, abs(account[self.symbol].position.shares), 103, 'decrease')
                pass

        if event.timer_id=="eod_5":
            if(account[self.symbol].position.shares>0):
                order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=account[self.symbol].position.shares, user_key=113)
                # self._sell_market_gs_smart(event, md, order, service, account, self.symbol, account[self.symbol].position.shares, 113, 'decrease')
                pass
            if(account[self.symbol].position.shares<0):
                order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=103)
                # self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, abs(account[self.symbol].position.shares), 103, 'decrease')
                pass
            

    def on_ack(self, event, md, order, service, account):
        pass

    def on_reject(self, event, md, order, service, account):
        self.rejectChecker=1
        pass

    def on_cancel_reject(self, event, md, order, service, account):
        pass
    
