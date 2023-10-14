from cloudquant.interfaces import Strategy
import time, random

class Gr8Scriptf1ae975d96ae427997fc4b712a537145(Strategy):
    __script_name__ = 'switchBox3v4'
    
    tickerItr = ['CHD','CHK','CHRW','CHTR','CI','CIEN','CIM','CIVI','CL','CLF','CLNE','CLX','CM','CMA','CMC','CMCSA','CME','CMG','CMI','CMS','CNC','CNHI','CNI','CNK','CNO','CNP','CNQ','CNX','COF','SPY']
    allocationKey=accKey=intvRate=TtlNet=allocationStatus=CancelBooks=strategyKey=LongCap=LongUnit=LongUnits=LongShares=LongRlz=LongUrl=LongTtl=ShrtCap=ShrtUnit=ShrtUnits=ShrtShares=ShrtRlz=ShrtUrl=ShrtTtl=TradeMatch=TradePendTtl=TradePendBuy=TradePendSell=HedgeLong=0
    allocationModel=10
    testRTE=1.0057

    riskMax=350
    plMaxLoss=-riskMax*0.20
    plUnrlRTE=riskMax*0.001
    upperBand=riskMax*.01
    lowerBand=-riskMax*.01
    bandMult=riskMax*.01
    intervalRate=[0]
    tkrAlpha = [[unit, 0] for unit in tickerItr]

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol in Gr8Scriptf1ae975d96ae427997fc4b712a537145.tickerItr
     
    def __init__(self, **params):
        if('riskAllocation' in params):
            print(params['riskAllocation'])
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.riskMax=params['riskAllocation']
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.plMaxLoss=-Gr8Scriptf1ae975d96ae427997fc4b712a537145.riskMax*0.20
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.plUnrlRTE=Gr8Scriptf1ae975d96ae427997fc4b712a537145.riskMax*0.001
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.upperBand=Gr8Scriptf1ae975d96ae427997fc4b712a537145.riskMax*0.01
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.lowerBand=-Gr8Scriptf1ae975d96ae427997fc4b712a537145.riskMax*0.01
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.bandMult=Gr8Scriptf1ae975d96ae427997fc4b712a537145.riskMax*0.01
    
    def on_start(self, md, order, service, account):
        self.yesterdayPrice = max(md.stat.prev_close, md.L1.open)
        if(self.yesterdayPrice == 0):
            self.yesterdayPrice = 500
        self.entryLevel=self.exitPrice=self.positionSize=self.spyQTY=0
        self.cancelOrderBook=self.checkPendingBook=[]
        self.maxAllocate=int(self.yesterdayPrice*1.10)
        self.delay = service.time_interval(seconds=5)
        self.twentyMin = service.time_interval(minutes=20)

        # type = service.symbol_list.in_list(service.symbol_list.get_handle('0e788f9d-4c44-4724-8581-21ef7e5dad09'), self.symbol)
        if(Gr8Scriptf1ae975d96ae427997fc4b712a537145.intervalRate[0]==0):
            print("PL MODEL: {}.{}\RISKMAX: {}\tRTE: {}\tTRADE DATE: {}".format(Gr8Scriptf1ae975d96ae427997fc4b712a537145.allocationModel, Gr8Scriptf1ae975d96ae427997fc4b712a537145.upperBand, Gr8Scriptf1ae975d96ae427997fc4b712a537145.riskMax, Gr8Scriptf1ae975d96ae427997fc4b712a537145.testRTE, service.time_to_string(service.system_time)))
        Gr8Scriptf1ae975d96ae427997fc4b712a537145.intervalRate[0]=0.0001
        
        print(Gr8Scriptf1ae975d96ae427997fc4b712a537145.tkrAlpha)
        
        i=0
        for unit in Gr8Scriptf1ae975d96ae427997fc4b712a537145.tkrAlpha:
            if(Gr8Scriptf1ae975d96ae427997fc4b712a537145.tkrAlpha[i][0]==self.symbol):
                Gr8Scriptf1ae975d96ae427997fc4b712a537145.tkrAlpha[i][1]=md.stat.beta
                break
            i+=1

        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=5), repeat_interval=service.time_interval(seconds=10), timer_id="Allocate")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=16), timer_id = "unload")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=12), timer_id = "liquidate")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=5), timer_id = "checkHedge")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=3), timer_id = "checkPositions")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=2), timer_id = "checkLargePositions")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=1), timer_id = "shutoff")
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
                    Gr8Scriptf1ae975d96ae427997fc4b712a537145.TradeMatch+=mtchTrades
                    
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongRlz+=account[ticker].realized_pl.entry_pl_long
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtRlz+=account[ticker].realized_pl.entry_pl_short
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
                    
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongCap+=longCash
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongUnit+=longPos
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongUnits+=longUnits
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongShares+=xQuantityLong
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongUrl+=longUnrl
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongTtl=Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongRlz+Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongUrl
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtCap+=shrtCash
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtUnit+=shrtPos
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtUnits+=shrtUnits
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtShares+=xQuantityShrt
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtUrl+=shrtUnrl
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtTtl=Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtRlz+Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtUrl
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
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.TradePendBuy+=pendingBuy
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.TradePendSell+=pendingSell
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.TradePendTtl=Gr8Scriptf1ae975d96ae427997fc4b712a537145.TradePendBuy+Gr8Scriptf1ae975d96ae427997fc4b712a537145.TradePendSell

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
                    
        if(Gr8Scriptf1ae975d96ae427997fc4b712a537145.strategyKey==1 and len(account[self.symbol].pending.orders)==0 and len(account[self.symbol].position.inventory)==0):
            print(self.symbol)
            return
            
        if(Gr8Scriptf1ae975d96ae427997fc4b712a537145.strategyKey==1):
            case_close_strategy()
            pass
        
        if(account.realized_mtm_pl+account.unrealized_entry_pl<Gr8Scriptf1ae975d96ae427997fc4b712a537145.plMaxLoss and Gr8Scriptf1ae975d96ae427997fc4b712a537145.strategyKey==0):
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.strategyKey=1
            case_close_strategy()
            pass
        
        if(Gr8Scriptf1ae975d96ae427997fc4b712a537145.strategyKey==1 and account.pending_capital_long==0 and account.open_capital_long==0 and len(account.open_symbols)==0):
            service.terminate()
        
        if(account[self.symbol].unrealized_pl.entry_pl>Gr8Scriptf1ae975d96ae427997fc4b712a537145.plUnrlRTE):
            case_info()
            pass
        
        
        i=0
        if(event.timestamp<self.illiquid_time):
            for unitsCancelled in self.cancelOrderBook:
                mktPrice = max(md.L1.ask, md.L1.last)-(random.randint(0, 50)/10000)
                if(unitsCancelled[3]==112):
                    rePriced = self._sell_limit_order_gs_smart(event, md, order, service, account, unitsCancelled[0], -unitsCancelled[1], mktPrice, 112, 'decrease')
                    self.cancelOrderBook.pop(i)
                    i+=1
                    pass

        if event.timer_id=="shutoff":
            service.terminate()
            pass
            
        if(self.symbol=="SPY"):
            self._reset_comm(md)  
            allocation_key=self._allocation_key(md)

            for ticker in Gr8Scriptf1ae975d96ae427997fc4b712a537145.tickerItr:
                case_all(ticker)
        
                if(account[ticker].position.capital_long>0):
                    self._hedge_positions(ticker, account[ticker].position.capital_long)
                    pass

            ping_book_stat=self._book_status(md, account, order, service, event)
            print("\n.upperBand\t", Gr8Scriptf1ae975d96ae427997fc4b712a537145.upperBand)
            print(".lowerBand\t", Gr8Scriptf1ae975d96ae427997fc4b712a537145.lowerBand)
            ping_pl_stat=self._clear_book_status()
            ping_hedge_stat=self._adjust_hedges(event, md, order, service, account)
            pass

        if(Gr8Scriptf1ae975d96ae427997fc4b712a537145.allocationStatus==1):
            case_close_book()
            pass
        
        if event.timer_id=="unload":
            if(len(account[self.symbol].pending.orders)>0):
                order.cancel(self.symbol)
                pass
            pass
                
        if event.timer_id=="liquidate":   
            if(account[self.symbol].position.shares>0):
                if(self.positionSize>0):
                    self._sell_market_gs_smart(event, md, order, service, account, self.symbol, account[self.symbol].position.shares, 113, 'decrease')
                    pass
                    
            if(account[self.symbol].position.shares<0):
                if(self.positionSize<0):
                    self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, abs(account[self.symbol].position.shares), 103, 'decrease')
                    pass
                    
        if event.timer_id=="checkHedge":
            if(self.symbol=="SPY"):
                if(account[self.symbol].position.shares>0):
                    self._sell_market_gs_smart(event, md, order, service, account, self.symbol, account[self.symbol].position.shares, 113, 'decrease')
                    pass
                if(account[self.symbol].position.shares<0):
                    self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, abs(account[self.symbol].position.shares), 103, 'decrease')
                    pass

        if event.timer_id=="checkPositions":
            if(account[self.symbol].position.shares>0):
                if(account[self.symbol].position.shares>4500):
                    positionClose=account[self.symbol].position.shares
                    while(positionClose>0):
                        positionClose-=2000
                        self._sell_market_gs_smart(event, md, order, service, account, self.symbol, 2000, 113, 'decrease')
                    pass    
                else:
                    self._sell_market_gs_smart(event, md, order, service, account, self.symbol, account[self.symbol].position.shares, 113, 'decrease')
                    pass
            if(account[self.symbol].position.shares<0):
                self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, abs(account[self.symbol].position.shares), 103, 'decrease')
                pass

        if event.timer_id=="checkLargePositions":
            if(account[self.symbol].position.shares>0):
               self._sell_market_gs_smart(event, md, order, service, account, self.symbol, account[self.symbol].position.shares, 113, 'decrease')
               pass
            if(account[self.symbol].position.shares<0):
                self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, abs(account[self.symbol].position.shares), 103, 'decrease')
                pass

        if(event.timer_id=="Allocate" and self.symbol!="SPY" and Gr8Scriptf1ae975d96ae427997fc4b712a537145.allocationKey==1 and event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time):
            self._check_indicators(event, md, order, service, account)
            
    def _buy_limit_order_gs_smart(self, event, md, order, service, account, ordrTkr, ordrSize, ordrPrice, ordrKey, ordrIntent):
        return order.algo_buy(ordrTkr, algorithm='8b976c72-20cd-49db-9121-db2e5ace3385', intent=ordrIntent, order_quantity=ordrSize, price=ordrPrice, user_key=ordrKey, allow_multiple_pending=40)  

    def _sell_limit_order_gs_smart(self, event, md, order, service, account, ordrTkr, ordrSize, ordrPrice, ordrKey, ordrIntent):
        return order.algo_sell(ordrTkr, algorithm='5a8a9f9d-22a5-4155-87e7-4ebe8024a97b', intent=ordrIntent, order_quantity=ordrSize, price=ordrPrice, user_key=ordrKey, allow_multiple_pending=40)      

    def on_fill(self, event, md, order, service, account):
        
        if(event.user_tag==111):
            randAdjust=random.randint(0, 50)/10000
            self.exitPrice = event.price*Gr8Scriptf1ae975d96ae427997fc4b712a537145.testRTE-randAdjust
            offerInventory = self._sell_limit_order_gs_smart(event, md, order, service, account, event.symbol, event.shares, self.exitPrice, 112, 'decrease')
            pass
            

    def on_ack(self, event, md, order, service, account):
        pass

    def on_cancel(self, event, md, order, service, account):

        if(event.user_tag==112 and event.timestamp<self.illiquid_time):
            evtUnit=[event.symbol, event.shares, event.price, event.user_tag]
            self.cancelOrderBook.append(evtUnit)
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.CancelBooks+=1
            return

    def on_reject(self, event, md, order, service, account):
        pass

    def on_cancel_reject(self, event, md, order, service, account):
        pass
    
    def _clear_book_status(self):
        if(Gr8Scriptf1ae975d96ae427997fc4b712a537145.TtlNet>Gr8Scriptf1ae975d96ae427997fc4b712a537145.upperBand):
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.upperBand=Gr8Scriptf1ae975d96ae427997fc4b712a537145.TtlNet+Gr8Scriptf1ae975d96ae427997fc4b712a537145.bandMult
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.lowerBand=Gr8Scriptf1ae975d96ae427997fc4b712a537145.TtlNet-Gr8Scriptf1ae975d96ae427997fc4b712a537145.bandMult
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.allocationStatus=1
        elif(Gr8Scriptf1ae975d96ae427997fc4b712a537145.TtlNet<Gr8Scriptf1ae975d96ae427997fc4b712a537145.lowerBand):
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.upperBand=Gr8Scriptf1ae975d96ae427997fc4b712a537145.TtlNet+Gr8Scriptf1ae975d96ae427997fc4b712a537145.bandMult
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.lowerBand=Gr8Scriptf1ae975d96ae427997fc4b712a537145.TtlNet-Gr8Scriptf1ae975d96ae427997fc4b712a537145.bandMult
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.allocationStatus=1
        else:
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.allocationStatus=0
        return Gr8Scriptf1ae975d96ae427997fc4b712a537145.allocationStatus
    
    def _hedge_positions(self, ticker, long_capital):
        for unit in Gr8Scriptf1ae975d96ae427997fc4b712a537145.tkrAlpha:
            if(unit[0]==ticker):
                Gr8Scriptf1ae975d96ae427997fc4b712a537145.HedgeLong+=(long_capital*unit[1])
                return Gr8Scriptf1ae975d96ae427997fc4b712a537145.HedgeLong

    def _reset_comm(self, md):
        Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongCap=Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongUnit=Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongUnits=Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongShares=Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongRlz=Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongUrl=Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongTtl=0
        Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtCap=Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtUnit=Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtUnits=Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtShares=Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtRlz=Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtUrl=Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtTtl=0
        Gr8Scriptf1ae975d96ae427997fc4b712a537145.TradeMatch=Gr8Scriptf1ae975d96ae427997fc4b712a537145.TradePendTtl=Gr8Scriptf1ae975d96ae427997fc4b712a537145.TradePendBuy=Gr8Scriptf1ae975d96ae427997fc4b712a537145.TradePendSell=Gr8Scriptf1ae975d96ae427997fc4b712a537145.TtlNet=Gr8Scriptf1ae975d96ae427997fc4b712a537145.HedgeLong=0
        Gr8Scriptf1ae975d96ae427997fc4b712a537145.intervalRate.append(md.L1.percent_change_from_open)
        return Gr8Scriptf1ae975d96ae427997fc4b712a537145.intervalRate
    
    def _allocation_key(self, md):
        intervalChange = Gr8Scriptf1ae975d96ae427997fc4b712a537145.intervalRate[-1]-Gr8Scriptf1ae975d96ae427997fc4b712a537145.intervalRate[-2]
        if(intervalChange>0):
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.allocationKey=0
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.accKey-=1
            pass
        else:
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.allocationKey=1
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.accKey+=1
            pass
            
        if(md.L1.percent_change_from_open!=0):
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.intvRate = intervalChange/md.L1.percent_change_from_open
            pass
        else:
            Gr8Scriptf1ae975d96ae427997fc4b712a537145.intvRate = 0
            pass
        return Gr8Scriptf1ae975d96ae427997fc4b712a537145.allocationKey
        
    def _book_status(self, md, account, order, service, event):
        TtlRlzd=Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongRlz+Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtRlz
        TtlUnrl=Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongUrl+Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtUrl
        Gr8Scriptf1ae975d96ae427997fc4b712a537145.TtlNet=TtlRlzd+TtlUnrl


        print("\n{}\tItr: {}    CRR%:  {}    PRR%:  {}    INTR%:  {}    KEY: {}".format(service.time_to_string(event.timestamp)[11:19], len(Gr8Scriptf1ae975d96ae427997fc4b712a537145.intervalRate), Gr8Scriptf1ae975d96ae427997fc4b712a537145.intervalRate[-1], Gr8Scriptf1ae975d96ae427997fc4b712a537145.intervalRate[-2], Gr8Scriptf1ae975d96ae427997fc4b712a537145.intvRate, Gr8Scriptf1ae975d96ae427997fc4b712a537145.allocationKey))
        print("L:  {}    POS:  {}    UNITS:  {}    RLZ:  {}    UNR:  {}    $NET LONG:  {}".format(Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongCap, Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongUnit, Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongUnits, Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongRlz, Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongUrl, Gr8Scriptf1ae975d96ae427997fc4b712a537145.LongTtl))
        print("S:  {}    POS:  {}    UNITS:  {}    RLZ:  {}    UNR:  {}    $NET SHRT:  {}".format(Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtCap, Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtUnit, Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtUnits, Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtRlz, Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtUrl, Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtTtl))
        print("#CLR:  {}    LIVE:  {}    B:  {}      S:  {}    RLZ:  {}    UNR:  {}    NET:  {}".format(Gr8Scriptf1ae975d96ae427997fc4b712a537145.TradeMatch, Gr8Scriptf1ae975d96ae427997fc4b712a537145.TradePendTtl, Gr8Scriptf1ae975d96ae427997fc4b712a537145.TradePendBuy, Gr8Scriptf1ae975d96ae427997fc4b712a537145.TradePendSell, TtlRlzd,TtlUnrl,Gr8Scriptf1ae975d96ae427997fc4b712a537145.TtlNet))
        print(Gr8Scriptf1ae975d96ae427997fc4b712a537145.CancelBooks)
        return len(Gr8Scriptf1ae975d96ae427997fc4b712a537145.intervalRate)


    def _sell_market_order_vwap_GS(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_sell(ordrTkr, algorithm='8c46b896-cef4-4b46-b02f-425f454a594e', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)    

    def _sell_market_gs_smart(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_sell(ordrTkr, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)
    
    def _buy_market_order_vwap_GS(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_buy(ordrTkr, algorithm='b4b979ae-370e-42a6-bf54-7b6a54a1bd4f', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)     

    def _buy_market_order_gs_smart(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_buy(ordrTkr, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)
    
    
    def _adjust_hedges(self, event, md, order, service, account):
        hedgeTwo = Gr8Scriptf1ae975d96ae427997fc4b712a537145.HedgeLong
        print("HEDGE:\t{}   ".format(hedgeTwo))
        if(Gr8Scriptf1ae975d96ae427997fc4b712a537145.allocationKey!=0):
            if(abs(Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtCap)<hedgeTwo):
                self.spyQTY = int((abs(Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtCap)-hedgeTwo)/400)
                if(self.spyQTY!=0):
                    if(account[self.symbol].position.shares>0):
                        short = self._sell_market_gs_smart(event, md, order, service, account, self.symbol, abs(self.spyQTY), 101, 'decrease')

                    elif(account[self.symbol].position.shares<0):
                        short = self._sell_market_gs_smart(event, md, order, service, account, self.symbol, abs(self.spyQTY), 101, 'increase')

                    elif(account[self.symbol].position.shares==0):    
                        short = self._sell_market_gs_smart(event, md, order, service, account, self.symbol, abs(self.spyQTY), 101, 'init')

                    else:
                        pass
                    pass
        elif(Gr8Scriptf1ae975d96ae427997fc4b712a537145.allocationKey!=1):        
            if(abs(Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtCap)>hedgeTwo):
                self.spyQTY = int((abs(Gr8Scriptf1ae975d96ae427997fc4b712a537145.ShrtCap)-hedgeTwo)/400)
                if(self.spyQTY!=0):
                    if(account[self.symbol].position.shares>0):
                        shrtBalance = self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, abs(self.spyQTY), 102, 'increase')

                    elif(account[self.symbol].position.shares<0):
                        shrtBalance = self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, abs(self.spyQTY), 102, 'decrease')

                    elif(account[self.symbol].position.shares==0):
                        shrtBalance = self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, abs(self.spyQTY), 102, 'init')

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
                if(indication>=Gr8Scriptf1ae975d96ae427997fc4b712a537145.allocationModel):
                    
                    #if(account.pending_capital_long>1000):
                    #    print(account.capital_used)
                    #    print(account.pending_capital_long)
                    
                    self.entryLevel = min(min(bar20m.open[:-15]), min(bar20m.close[:-15]))-(random.randint(0, 50)/10000)
                    self.positionSize= int(Gr8Scriptf1ae975d96ae427997fc4b712a537145.riskMax/self.maxAllocate)+1

                    if(account[self.symbol].position.shares==0 and len(account[self.symbol].pending.orders)<40):
                        pricedBid = self._buy_limit_order_gs_smart(event, md, order, service, account, self.symbol, self.positionSize, self.entryLevel, 111, 'increase')
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

    def _buy_market_order_nasd(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_buy(ordrTkr, algorithm='1f9b553d-30bf-40a3-8868-ebe70b5079b2', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)        
    
    def _buy_market_order_nyse(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_buy(ordrTkr, algorithm='96c01190-bbcc-40c2-b3c1-d645e3dff215', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)        
    
    def _buy_market_order_arca(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_buy(ordrTkr, algorithm='2b4fdc55-ff01-416e-a5ea-e1f1d4524c7d', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)    
    
    def _buy_market_order_edga(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_buy(ordrTkr, algorithm='f8257c14-07f8-47f6-b8a3-b3d98c4545fd', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)    
    
    def _buy_market_order_edgx(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_buy(ordrTkr, algorithm='f1e94eae-90f6-43b1-a1ae-66f88c67f260', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)

    def _sell_market_order_nasd(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_sell(ordrTkr, algorithm='5fc61945-3498-47da-abf6-b5dabdc9f4ac', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)  
    
    def _sell_market_order_nyse(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_sell(ordrTkr, algorithm='a5a329d1-f81e-4d4b-99c3-dfff4053e09f', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)  
    
    def _sell_market_order_arca(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_sell(ordrTkr, algorithm='8fdee8fe-b772-46bd-b411-5544f7a0d917', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)    
    
    def _sell_market_order_edga(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_sell(ordrTkr, algorithm='6852828c-b2cd-4e23-9ac5-68fb4c560a67', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)    
    
    def _sell_market_order_edgx(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_sell(ordrTkr, algorithm='c5c72497-0991-4dff-8a5c-f0812091f9b3', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)

    def _sell_limit_order_NASD(self, event, md, order, service, account, ordrTkr, ordrSize, ordrPrice, ordrKey, ordrIntent):
        return order.algo_sell(ordrTkr, algorithm='09528d6b-7d4f-4cc2-8611-8bbecb33785c', intent=ordrIntent, order_quantity=ordrSize, price=ordrPrice, user_key=ordrKey, allow_multiple_pending=True)

    def _sell_limit_order_NYSE(self, event, md, order, service, account, ordrTkr, ordrSize, ordrPrice, ordrKey, ordrIntent):
        return order.algo_sell(ordrTkr, algorithm='8587f4f5-0301-4645-aa97-fc530eb9f0c2', intent=ordrIntent, order_quantity=ordrSize, price=ordrPrice, user_key=ordrKey, allow_multiple_pending=True)
    
    def _sell_limit_order_ARCA(self, event, md, order, service, account, ordrTkr, ordrSize, ordrPrice, ordrKey, ordrIntent):
        return order.algo_sell(ordrTkr, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent=ordrIntent, order_quantity=ordrSize, price=ordrPrice, user_key=ordrKey, allow_multiple_pending=True)
    
    def _sell_limit_order_EDGA(self, event, md, order, service, account, ordrTkr, ordrSize, ordrPrice, ordrKey, ordrIntent):
        return order.algo_sell(ordrTkr, algorithm='811e2ed0-b096-48cd-9cf3-a24dbd4a3992', intent=ordrIntent, order_quantity=ordrSize, price=ordrPrice, user_key=ordrKey, allow_multiple_pending=True)

    def _sell_limit_order_EDGX(self, event, md, order, service, account, ordrTkr, ordrSize, ordrPrice, ordrKey, ordrIntent):
        return order.algo_sell(ordrTkr, algorithm='96317801-94be-47d7-9dff-3b398e518c93', intent=ordrIntent, order_quantity=ordrSize, price=ordrPrice, user_key=ordrKey, allow_multiple_pending=True)
        
