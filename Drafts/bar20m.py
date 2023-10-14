# 2023.04.24
# https://ui.kite.ktg.local/#/glossary/338

from cloudquant.interfaces import Strategy
import ktgfunc

tickerUniv = ['AA','AAL','AAP','AAPL','AAXJ','ABB','ABBV','ABT','ACAD','ACGL','ACI','ACLS','ACN','ADM','ADP','ADSK','ADT','AEE','AEM','AEO','AEP','AER','AG','AGG','AJG','AKAM','ALB','ALC','ALGN', 'SPY']


class Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2(Strategy):
    __script_name__ = 'switchBox3'
    tickerItr = ['AA','AAL','AAP','AAPL','AAXJ','ABB','ABBV','ABT','ACAD','ACGL','ACI','ACLS','ACN','ADM','ADP','ADSK','ADT','AEE','AEM','AEO','AEP','AER','AG','AGG','AJG','AKAM','ALB','ALC','ALGN', 'SPY']
    allocationKey=accKey=intvRate=TtlNet=allocationStatus=CancelBooks=0
    allocationModel=10
    testRTE=1.0057
    testBpAdjustmentPrice=0.03
    LongCap=LongUnit=LongUnits=LongShares=LongRlz=LongUrl=LongTtl=0
    ShrtCap=ShrtUnit=ShrtUnits=ShrtShares=ShrtRlz=ShrtUrl=ShrtTtl=0
    TradeMatch=TradePendTtl=TradePendBuy=TradePendSell=HedgeLong=0
    #TODO
    riskMax=50000
    upperBand=riskMax*0.01
    lowerBand=-riskMax*0.01
    adjustBand=riskMax*0.01
    plRoll=riskMax*0.001
    intervalRate=[0]
    tkrDist = [('AA', 'MATS', 2.4513), ('AAL', 'ARLN', 1.5494), ('AAP', 'AUTO', 1.1371), ('AAPL', 'TECH', 1.2932), ('AAXJ', 'MISC', 0.8729), ('ABB', 'ENGN', 1.1471), ('ABBV', 'PHRM', 0.552), ('ABT', 'HLTH', 0.6638), ('ACAD', 'BIOT', 0.5551), ('ACGL', 'INSU', 0.7304), ('ACI', 'FOOD', 0), ('ACLS', 'TECH', 1.7267), ('ACN', 'TECH', 1.2412), ('ADM', 'TBCO', 0.8028), ('ADP', 'SRVC', 0.8174), ('ADSK', 'TECH', 1.5331), ('ADT', 'SRVC', 1.7105), ('AEE', 'UTIL', 0.4414), ('AEM', 'MATS', 0.696), ('AEO', 'RETL', 1.5148), ('AEP', 'UTIL', 0.4498), ('AER', 'BRKR', 2.0066), ('AG', 'MATS', 0.9213), ('AGG', 'MISC', -0.0153), ('AJG', 'INSU', 0.7003), ('AKAM', 'TECH', 0.8028), ('ALB', 'MATS', 1.5597), ('ALC', 'HLTH', 0.95), ('ALGN', 'HLTH', 1.595)]

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol in tickerUniv
 
    def on_start(self, md, order, service, account):
        
        self.status=self.entryLevel=self.exitPrice=self.orderStatus=self.positionSize=self.pendingKey=self.spyQTY=0
        self.cancelOrderBook = []
        self.checkPendingBook = []
        self.delay = service.time_interval(seconds=5)
        self.twoMin = service.time_interval(minutes=1)
        self.fiveMin = service.time_interval(minutes=1)
        self.tenMin = service.time_interval(minutes=10)
        self.twentyMin = service.time_interval(minutes=20)
        self.oneHour = service.time_interval(hours=1)
        self.timerInterval = service.time_interval(seconds=30)

        # type = service.symbol_list.in_list(service.symbol_list.get_handle('0e788f9d-4c44-4724-8581-21ef7e5dad09'), self.symbol)
        if(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intervalRate[0]==0):
            print("PL MODEL: {}.{}\tRISK: {}\tBAND: {}\tRTE: {}\tBP Adjust: {}\tTRADE DATE: {}".format(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationModel, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.upperBand, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.riskMax, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.plRoll, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.testRTE, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.testBpAdjustmentPrice, service.time_to_string(service.system_time)))
        Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intervalRate[0]=0.0001
        for unit in Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.tkrDist:
            if(unit[0]==self.symbol):
                print(unit)
        service.add_time_trigger(md.market_open_time+self.fiveMin+self.delay, repeat_interval=self.fiveMin,timer_id="FiveMin")
        service.add_time_trigger(md.market_close_time-service.time_interval(minutes=16), timer_id = "unload")
        service.add_time_trigger(md.market_close_time-service.time_interval(minutes=1), timer_id = "shutoff")
        self.liquid_time = md.market_open_time + service.time_interval(minutes=21)
        self.illiquid_time = md.market_close_time-service.time_interval(minutes=30)

    
    def on_timer(self, event, md, order, service, account):
        
        
        def case_all(ticker):
            longUnit=longUnits=shrtUnit=shrtUnits=0
            pendingBuy=pendingSell=0
            longRlz=longCash=longUnrl=0
            shrtRlz=shrtCash=shrtUnrl=0
            #print('account[ticker].realized_pl')
            #print(account[ticker].realized_pl)

            if(account[ticker].realized_pl.entry_pl!=0 or account[ticker].realized_pl.mtm_pl!=0):
                #print('type(account[ticker].realized_pl.matched_trades)') 
                #print(dir(account[ticker].realized_pl))
                #print('account[ticker].realized_pl.entry_pl_long')
                #print(account[ticker].realized_pl.entry_pl_long)

                cpyDict = [account[ticker].realized_pl]
                mtchTrades=-1
                for key in cpyDict:
                    #print('key')
                    item = str(key)
                    #print(type(key))
                    #print(dir(key))
                    #print(key._matched_trades)
                    #Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradeMatch+=len(key._matched_trades)
                    splt_itm = item.split("entry_execution")
                    #print('splt_itm')
                    #print(splt_itm)
                    #print(splt_itm)
                    for itm in splt_itm:
                        mtchTrades+=1
                        #print(type(itm))
                        #print(mtchTrades)
                        #print('ITM')
                        #print(itm)
                Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradeMatch+=mtchTrades
                    
            if(ticker!="SPY"):        
                Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongRlz+=account[ticker].realized_pl.entry_pl
            
            if(ticker=="SPY"):
                Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtRlz+=account[ticker].realized_pl.entry_pl
                
            longPos=longUnits=longCash=longUnrl=xQuantityLong=0
            shrtPos=shrtUnits=shrtCash=shrtUnrl=xQuantityShrt=0
 
            
            if(len(account[ticker].position.inventory)>0):
                ctInv = len(account[ticker].position.inventory)
                
                # print(account[ticker].position.inventory)
                while(ctInv>0):
                    ctInv-=1
                    #print('account[ticker].position.inventory[ctInv]')
                    #print(account[ticker].position.inventory[ctInv])
                    #print('account[ticker].position.inventory[ctInv].execution')
                    #print(account[ticker].position.inventory[ctInv].execution)
                    
                    if(account[ticker].position.inventory[ctInv].execution.side==1):
                        longPos=1
                        longUnits+=1
                        longCash=account[ticker].position.capital_long
                        longUnrl=account[ticker].unrealized_pl.entry_pl
                        tkrLong=account[ticker].position.inventory[ctInv].execution.symbol
                        longIndicator=account[ticker].position.inventory[ctInv].execution.side
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
                    
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongCap+=longCash
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongUnit+=longPos
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongUnits+=longUnits
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongShares+=xQuantityLong
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongUrl+=longUnrl
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongTtl=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongRlz+Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongUrl
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtCap+=shrtCash
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtUnit+=shrtPos
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtUnits+=shrtUnits
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtShares+=xQuantityShrt
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtUrl+=shrtUnrl
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtTtl=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtRlz+Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtUrl
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
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradePendBuy+=pendingBuy
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradePendSell+=pendingSell
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradePendTtl=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradePendBuy+Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradePendSell

        def case_info():
            ctPositionLong=ctPositionShort=releaseItem=0
            xPriceLong=xPriceShort=[]
            
            ctInventoryItem = len(account[self.symbol].position.inventory)
            inventoryItem = account[self.symbol].position.inventory
            #print('account[self.symbol].position.inventory')
            #print(account[self.symbol].position.inventory)
            
            while(ctInventoryItem>0):
                ctInventoryItem-=1
                
                #print('executedVars = inventoryItem[ctInventoryItem]')
                executedVars = inventoryItem[ctInventoryItem]
                #print(executedVars)
                
                if(inventoryItem[ctInventoryItem].execution.side==1):
                    ctPositionLong+=1
                    tkrLong = inventoryItem[ctInventoryItem].execution.symbol
                    longIndicator = inventoryItem[ctInventoryItem].execution.side
                    xQuantityLong = inventoryItem[ctInventoryItem].execution.shares
                    xPriceLong.append(inventoryItem[ctInventoryItem].execution.price)
                    xTimeLong = inventoryItem[ctInventoryItem].execution.time
                    pass
                elif(inventoryItem[ctInventoryItem].execution.side==-1):
                    ctPositionShort+=1
                    tkrShort = inventoryItem[ctInventoryItem].execution.symbol
                    shortIndicator = inventoryItem[ctInventoryItem].execution.side
                    xQuantityShort = inventoryItem[ctInventoryItem].execution.shares
                    xPriceShort.append(inventoryItem[ctInventoryItem].execution.price)
                    xTimeShort = inventoryItem[ctInventoryItem].execution.time
                    pass
                
            ctPending=len(account[self.symbol].pending.orders)
            
            while(ctPending>0):
                ctPending-=1
                pendingExecution=account[self.symbol].pending.orders
                if(pendingExecution[ctPending].shares<0):                    
                    if(min(xPriceLong)<md.L1.bid):
                        infoCase = order.cancel(order_id=pendingExecution[ctPending].order_id)

                    pass
                elif(pendingExecution[ctPending].shares>0):
                    #print("re-rack the bid: {}   Entry: {} Bid: {}".format(self.symbol, account[self.symbol].pending.orders[ctPending][2], md.L1.bid))
                    pass

        def case_close_book():
            ctPending=len(account[self.symbol].pending.orders)
            pendingExecution=account[self.symbol].pending.orders
            while(ctPending>0):
                ctPending-=1
                crrOrder = pendingExecution[ctPending]
                #print('pendingExecution[ctPending].order_id')
                #print(pendingExecution[ctPending].order_id)
                
                if(pendingExecution[ctPending].shares<0):
                    order.cancel(order_id=pendingExecution[ctPending].order_id)
                    pass
                elif(pendingExecution[ctPending].shares>0):
                    pass

        
        def case_pending_orders():
            ctPnd=len(account[self.symbol].pending.orders)
            while(ctPnd>0):
                ctPnd-=1
                
                pendingExecution=account[self.symbol].pending.orders
                chkTime = event.timestamp - pendingExecution[ctPnd].timestamp

                if(pendingExecution[ctPnd].shares<0):
                    chkPriceSpreadSell=pendingExecution[ctPnd].price - md.L1.last
                    #service.write_file('pending-trade-CXL', '{},{},{},{},{},{},{},{},{},{},{},{}'.format(service.time_to_string(event.timestamp)[11:19], pendingExecution[ctPnd].timestamp, chkTime, "S", pendingExecution[ctPnd].symbol, pendingExecution[ctPnd].shares, pendingExecution[ctPnd].price, md.L1.ask, md.L1.last, chkPriceSpreadSell, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intervalRate[-1], account[self.symbol].unrealized_pl.entry_pl))
                    pass
                elif(pendingExecution[ctPnd].shares>0):
                    chkPriceSpreadBuy=md.L1.last-pendingExecution[ctPnd].price
                    chkPriceSpreadKillrate=chkPriceSpreadBuy/md.L1.last
                    if(chkPriceSpreadKillrate>Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.testBpAdjustmentPrice):
                        order.cancel(order_id=pendingExecution[ctPnd].order_id)
                    #service.write_file('pending-trade-CXL', '{},{},{},{},{},{},{},{},{},{},{},{}'.format(service.time_to_string(event.timestamp)[11:19], pendingExecution[ctPnd].timestamp, chkTime, "B",  pendingExecution[ctPnd].symbol, pendingExecution[ctPnd].shares, pendingExecution[ctPnd].price, md.L1.ask, md.L1.last, chkPriceSpreadBuy, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intervalRate[-1], account[self.symbol].unrealized_pl.entry_pl))
                    pass
        
        case_pending_orders()
        
        if(account[self.symbol].unrealized_pl.entry_pl>Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.plRoll):
            case_info()
            self.status=0
            pass
        
        
        i=0
        if(len(self.cancelOrderBook)>0):
            pass
        
        if(event.timestamp<self.illiquid_time):
            for unitsCancelled in self.cancelOrderBook:
                #print("CANCEL ORDERS---CANCEL ORDERS---CANCEL ORDERS---CANCEL ORDERS-\t\t", self.symbol)
                #print(unitsCancelled)
                #evtUnit=[event.symbol, event.shares, event.price, event.user_tag]
                mktPrice = max(md.L1.ask, md.L1.last)
                if(unitsCancelled[3]==112):
                    rePriced = self._sell_limit_order_gs_smart(event, md, order, service, account, unitsCancelled[0], -unitsCancelled[1], mktPrice, 112, 'decrease')
                self.cancelOrderBook.pop(i)
                i+=1
                # print(self.cancelOrderBook)

        if event.timer_id=="shutoff":
            service.terminate()
            pass
        
        if(self.symbol=="SPY"):
            self._reset_comm(md)
            allocation_key=self._allocation_key(md)
            
            # conv. account object from dict. to list.
            # access using ints.
            
            # print('account')
            #print(account)

            for ticker in Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.tickerItr:
                case_all(ticker)
                if(account[ticker].position.capital_long>0):
                    self._hedge_positions(ticker, account[ticker].position.capital_long)

            ping_book_stat=self._book_status(md, order, service, event)
            print("\nupperBand\t", Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.upperBand)
            print("lowerBand\t", Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.lowerBand)
            ping_pl_stat=self._clear_book_status()
            ping_hedge_stat=self._adjust_hedges(event, md, order, service, account)
            pass

        if(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationStatus==1):
            # print("Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationStatus: {}\tself.symbol: {}\tself.STATUS: {}".format(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationStatus, self.symbol, self.status))
            case_close_book()
        
        if event.timer_id=="unload":
            if(len(account[self.symbol].pending.orders)>0):
                order.cancel(self.symbol)
                pass
            if(account[self.symbol].position.shares>0):
                self.status=5
                if(self.positionSize>0):
                    self._sell_market_gs_smart(event, md, order, service, account, self.symbol, account[self.symbol].position.shares, 113, 'decrease')
                    pass
            if(account[self.symbol].position.shares<0):
                self.status=999
                if(self.positionSize<0):
                    # self._buy_limit_order_gs_smart(event, md, order, service, account, self.symbol, account[self.symbol].position.shares, self.entryLevel, 111, 'increase')
                    self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, abs(account[self.symbol].position.shares), 103, 'decrease')
                    # order.send(self.symbol, 'buy', account[self.symbol].position.shares, type='MKT')
                    pass
                
        #FAVORABLE ALLOCATION CONDITIONS
        if(event.timer_id=="FiveMin" and Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationKey==1 and event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time):
            self._check_indicators(event, md, order, service, account)
            
    def _buy_limit_order_gs_smart(self, event, md, order, service, account, ordrTkr, ordrSize, ordrPrice, ordrKey, ordrIntent):
        return order.algo_buy(ordrTkr, algorithm='8b976c72-20cd-49db-9121-db2e5ace3385', intent=ordrIntent, order_quantity=ordrSize, price=ordrPrice, user_key=ordrKey, allow_multiple_pending=True)  


    def _sell_limit_order_gs_smart(self, event, md, order, service, account, ordrTkr, ordrSize, ordrPrice, ordrKey, ordrIntent):
        return order.algo_sell(ordrTkr, algorithm='5a8a9f9d-22a5-4155-87e7-4ebe8024a97b', intent=ordrIntent, order_quantity=ordrSize, price=ordrPrice, user_key=ordrKey, allow_multiple_pending=True)      

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
  
    def on_fill(self, event, md, order, service, account):
        #print("on_fill")
        #print(event)
        if(event.user_tag==111):
            self.status = 2
            self.exitPrice = self.entryLevel*Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.testRTE
            stopPrice = self.entryLevel*0.99
            offerInventory = self._sell_limit_order_gs_smart(event, md, order, service, account, event.symbol, event.shares, self.exitPrice, 112, 'decrease')
            #print("SELL")
            #print(offerInventory)
            # order.algo_sell(self.symbol, algorithm='limit', intent='none', order_quantity=event.shares, price=self.exitPrice, allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-r999-96b59offload')
            return offerInventory
        if(self.status==2):
            self.orderStatus=0
            self.status=0

    def on_ack(self, event, md, order, service, account):
        if(self.status == 1):
            pass
        if(self.status == 2):
            pass

    def on_cancel(self, event, md, order, service, account):
        #print("on_cancel")
        #print(event)
        if(event.user_tag==112):
            evtUnit=[event.symbol, event.shares, event.price, event.user_tag]
            self.cancelOrderBook.append(evtUnit)
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.CancelBooks+=1

    def on_reject(self, event, md, order, service, account):
        print("reject\t",event)

    def on_cancel_reject(self, event, md, order, service, account):
        print("cancel reject\t", event)
        pass
    
    def _clear_book_status(self):
        if(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TtlNet>Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.upperBand):
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.upperBand=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TtlNet+Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.adjustBand
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.lowerBand=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TtlNet-Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.adjustBand
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationStatus=1
        elif(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TtlNet<Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.lowerBand):
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.upperBand=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TtlNet+Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.adjustBand
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.lowerBand=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TtlNet-Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.adjustBand
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationStatus=1
        else:
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationStatus=0
        return Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationStatus
    
    def _hedge_positions(self, ticker, long_capital):
        for unit in Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.tkrDist:
            if(unit[0]==ticker):
                Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.HedgeLong+=(long_capital*unit[2])
                return Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.HedgeLong

    def _reset_comm(self, md):
        Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongCap=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongUnit=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongUnits=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongShares=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongRlz=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongUrl=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongTtl=0
        Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtCap=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtUnit=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtUnits=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtShares=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtRlz=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtUrl=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtTtl=0
        Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradeMatch=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradePendTtl=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradePendBuy=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradePendSell=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TtlNet=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.HedgeLong=0
        Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intervalRate.append(md.L1.percent_change_from_open)
        return Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intervalRate
    
    def _allocation_key(self, md):
        intervalChange = Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intervalRate[-1]-Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intervalRate[-2]
        if(intervalChange>0):
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationKey=0
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.accKey-=1
            pass
        else:
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationKey=1
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.accKey+=1
            pass
        if(md.L1.percent_change_from_open!=0):
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intvRate = intervalChange/md.L1.percent_change_from_open
            pass
        else:
            Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intvRate = 0
            pass
        return Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationKey
        
    def _book_status(self, md, order, service, event):
        TtlRlzd=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongRlz+Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtRlz
        TtlUnrl=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongUrl+Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtUrl
        Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TtlNet=TtlRlzd+TtlUnrl
        print("\n{}\tItr: {}    CRR%:  {}    PRR%:  {}    INTR%:  {}    KEY: {}".format(service.time_to_string(event.timestamp)[11:19], len(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intervalRate), Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intervalRate[-1], Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intervalRate[-2], Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intvRate, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationKey))
        print("L:  {}    POS:  {}    UNITS:  {}    RLZ:  {}    UNR:  {}    $NET LONG:  {}".format(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongCap, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongUnit, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongUnits, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongRlz, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongUrl, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongTtl))
        print("S:  {}    POS:  {}    UNITS:  {}    RLZ:  {}    UNR:  {}    $NET SHRT:  {}".format(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtCap, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtUnit, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtUnits, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtRlz, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtUrl, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtTtl))
        print("#CLR:  {}    LIVE:  {}    B:  {}      S:  {}    RLZ:  {}    UNR:  {}    NET:  {}".format(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradeMatch, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradePendTtl, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradePendBuy, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradePendSell, TtlRlzd,TtlUnrl,Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TtlNet))
        
        #print("\n{}\tItr: {}    CRR%:  {:.4f}    PRR%:  {:.4f}    INTR%:  {:.4f}    KEY: {}".format(service.time_to_string(event.timestamp)[11:19], len(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intervalRate), Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intervalRate[-1], Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intervalRate[-2], Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intvRate, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationKey))
        #print("L:  {:.0f}    POS:  {}    UNITS:  {}    RLZ:  {:.0f}    UNR:  {:.0f}    $NET LONG:  {:.0f}".format(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongCap, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongUnit, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongUnits, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongRlz, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongUrl, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.LongTtl))
        #print("S:  {:.0f}    POS:  {}    UNITS:  {}    RLZ:  {:.0f}    UNR:  {:.0f}    $NET SHRT:  {:.0f}".format(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtCap, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtUnit, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtUnits, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtRlz, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtUrl, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtTtl))
        #print("#CLR:  {}    LIVE:  {}    B:  {}      S:  {}    RLZ:  {:.0f}    UNR:  {:.0f}    NET:  {:.0f}".format(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradeMatch, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradePendTtl, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradePendBuy, Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TradePendSell, TtlRlzd,TtlUnrl,Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.TtlNet))
        print(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.CancelBooks)
        return len(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intervalRate)


    def _sell_market_order_vwap_GS(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_sell(ordrTkr, algorithm='8c46b896-cef4-4b46-b02f-425f454a594e', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)    

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

    def _sell_market_gs_smart(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_sell(ordrTkr, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)
    
    def _buy_market_order_vwap_GS(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        return order.algo_buy(ordrTkr, algorithm='b4b979ae-370e-42a6-bf54-7b6a54a1bd4f', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)     
    
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

    def _buy_market_order_gs_smart(self, event, md, order, service, account, ordrTkr, ordrSize, ordrKey, ordrIntent):
        order.algo_buy(ordrTkr, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)
    
    
    def _adjust_hedges(self, event, md, order, service, account):
        hedgeTwo = Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.HedgeLong
        #print("HEDGE:\t{:.0f}   ".format(hedgeTwo))
        if(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationKey==0):
            if(abs(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtCap)<hedgeTwo):
                self.spyQTY = int((abs(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtCap)-hedgeTwo)/400)
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
        elif(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationKey==1):        
            if(abs(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtCap)>hedgeTwo):
                self.spyQTY = int((abs(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.ShrtCap)-hedgeTwo)/400)
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
            
        barPointA = event.timestamp-self.twentyMin-self.delay
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
                #20m: BIN 1
                complexA=19
                complexB=0
                indication=2
                pass
            elif(chk12A>0 and chk13B>0):
                complexA=19
                complexB=10
                indication=2
                pass
            elif(chk12A>0 and chk13C>0):
                complexA=19
                complexB=15
                indication=2
                pass
            elif(chk12A>0 and chk13x>0):
                complexA=19
                complexB=0
                indication=2
                pass
            elif(chk12A>0 and chk13y>0):
                complexA=19
                complexB=10
                indication=2
                pass
            elif(chk12A>0 and chk13z>0):
                complexA=19
                complexB=15
                indication=2
                pass
            elif(chk12B>0 and chk13A>0):
                complexA=19
                complexB=0
                indication=2
                pass
            elif(chk12B>0 and chk13B>0):
                complexA=19
                complexB=10
                indication=2
                pass
            elif(chk12B>0 and chk13C>0):
                complexA=19
                complexB=15
                indication=2
                pass
            elif(chk12B>0 and chk13x>0):
                complexA=19
                complexB=0
                indication=2
                pass
            elif(chk12B>0 and chk13y>0):
                complexA=19
                complexB=10
                indication=2
                pass
            elif(chk12B>0 and chk13z>0):
                complexA=19
                complexB=15
                indication=2
                pass
            while(complexA>=0):
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
                if(indication>=Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.allocationModel):
                    self.status=1
                    self.orderStatus=1
                    self.pendingKey=len(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.intervalRate)
                    self.entryLevel = min(min(bar20m.open[:-15]), min(bar20m.close[:-15]))
                    self.positionSize= int(Gr8Scriptbc6d88c3ab7b44729d96f59cedfe4ff2.riskMax/self.entryLevel)
                    # print(self.positionSize)
                    

                    #order.algo_buy(self.symbol, algorithm='limit', intent='increase', order_quantity=self.positionSize, price=self.entryLevel, allow_multiple_pending=True, user_key=111)
                    #order.algo_buy(self.symbol, algorithm='8b976c72-20cd-49db-9121-db2e5ace3385', intent='increase', order_quantity=self.positionSize, price=self.entryLevel, allow_multiple_pending=True, )
                    
                    if(self.symbol!="SPY"):
                        if(account[self.symbol].position.shares==0):
                            pricedBid = self._buy_limit_order_gs_smart(event, md, order, service, account, self.symbol, self.positionSize, self.entryLevel, 111, 'increase')
                            
                            pass 
                            # order.algo_buy(self.symbol, algorithm='limit', intent='increase', order_quantity=self.positionSize, price=self.entryLevel, allow_multiple_pending=True, user_key=111)
                            #order.algo_buy(self.symbol, algorithm='8b976c72-20cd-49db-9121-db2e5ace3385', intent='increase', order_quantity=self.positionSize, price=self.entryLevel,  allow_multiple_pending=True)
                            
                            #order.algo_buy(self.symbol, algorithm='8b976c72-20cd-49db-9121-db2e5ace3385', intent='init', order_quantity=self.positionSize, price=self.entryLevel, user_key='7e5da6c3-ff12-5858-ordr-96b59initial', allow_multiple_pending=True)
                        else:
                            #return self._buy_limit_order_gs_smart(event, md, order, service, account, self.symbol, self.positionSize, self.entryLevel, '7e5da6c3-ff12-5858-ordr-96b59initial', 'increase')
                            # order.algo_buy(self.symbol, algorithm='limit', intent='increase', order_quantity=self.positionSize, price=self.entryLevel, allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
                            pass
                    complexA=0
                    break
                else:
                    break
        pass
