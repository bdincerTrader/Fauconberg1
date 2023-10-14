from cloudquant.interfaces import Strategy, Event
import ktgfunc
tickerUniv = ['AA','AAL','AAP','AAPL','AAXJ','ABB','ABBV','ABT','ACAD','ACGL','ACI','ACLS','ACN','ADM','ADP','ADSK','ADT','AEE','AEM','AEO','AEP','AER','AG','AGG','AJG','AKAM','ALB','ALC','ALGN', 'SPY']


class Gr8Script8c04b32f5abd4c5384c2481ac2556e30(Strategy):
    __script_name__ = 'switchBox2'
    tickerItr = ['AA','AAL','AAP','AAPL','AAXJ','ABB','ABBV','ABT','ACAD','ACGL','ACI','ACLS','ACN','ADM','ADP','ADSK','ADT','AEE','AEM','AEO','AEP','AER','AG','AGG','AJG','AKAM','ALB','ALC','ALGN', 'SPY']
    allocationKey=accKey=intvRate=TtlNet=allocationStatus=0
    allocationModel=10
    testRTE=1.0057
    LongCap=LongUnit=LongUnits=LongShares=LongRlz=LongUrl=LongTtl=0
    ShrtCap=ShrtUnit=ShrtUnits=ShrtShares=ShrtRlz=ShrtUrl=ShrtTtl=0
    TradeMatch=TradePendTtl=TradePendBuy=TradePendSell=HedgeLong=0
    #TODO
    upperBand=500
    lowerBand=-500
    intervalRate=[0]
    tkrDist = [('AA', 'MATS', 2.4513), ('AAL', 'ARLN', 1.5494), ('AAP', 'AUTO', 1.1371), ('AAPL', 'TECH', 1.2932), ('AAXJ', 'MISC', 0.8729), ('ABB', 'ENGN', 1.1471), ('ABBV', 'PHRM', 0.552), ('ABT', 'HLTH', 0.6638), ('ACAD', 'BIOT', 0.5551), ('ACGL', 'INSU', 0.7304), ('ACI', 'FOOD', 0), ('ACLS', 'TECH', 1.7267), ('ACN', 'TECH', 1.2412), ('ADM', 'TBCO', 0.8028), ('ADP', 'SRVC', 0.8174), ('ADSK', 'TECH', 1.5331), ('ADT', 'SRVC', 1.7105), ('AEE', 'UTIL', 0.4414), ('AEM', 'MATS', 0.696), ('AEO', 'RETL', 1.5148), ('AEP', 'UTIL', 0.4498), ('AER', 'BRKR', 2.0066), ('AG', 'MATS', 0.9213), ('AGG', 'MISC', -0.0153), ('AJG', 'INSU', 0.7003), ('AKAM', 'TECH', 0.8028), ('ALB', 'MATS', 1.5597), ('ALC', 'HLTH', 0.95), ('ALGN', 'HLTH', 1.595)]

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol in tickerUniv
 
    def on_start(self, md, order, service, account):
        self.status=self.entryLevel=self.entryLevel=self.exitPrice=self.orderStatus=self.positionSize=self.pendingKey=self.spyQTY=0
        self.order_Enter=self.order_Exit="0"
        self.riskMax=100000
        self.delay = service.time_interval(seconds=5)
        self.twoMin = service.time_interval(minutes=1)
        self.fiveMin = service.time_interval(minutes=1)
        self.tenMin = service.time_interval(minutes=10)
        self.twentyMin = service.time_interval(minutes=20)
        self.oneHour = service.time_interval(hours=1)
        self.timerInterval = service.time_interval(seconds=30)
        service.clear_event_triggers()
        # type = service.symbol_list.in_list(service.symbol_list.get_handle('0e788f9d-4c44-4724-8581-21ef7e5dad09'), self.symbol)
        if(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intervalRate[0]==0):
            print("PL MODEL: {}.{}\tTIMER: {}\tRTE: {}\tTRADE DATE: {}".format(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationModel, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.upperBand, self.timerInterval, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.testRTE, service.time_to_string(service.system_time)))
        Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intervalRate[0]=0.0001
        for unit in Gr8Script8c04b32f5abd4c5384c2481ac2556e30.tkrDist:
            if(unit[0]==self.symbol):
                print(unit)
        service.add_time_trigger(md.market_open_time+self.fiveMin+self.delay, repeat_interval=self.fiveMin,timer_id="FiveMin")
        service.add_time_trigger(service.time(15,30), timer_id = "illiquid")
        service.add_time_trigger(service.time(9,45), timer_id = "liquid")
        service.add_time_trigger(service.time(15,44), timer_id = "unload")
        service.add_time_trigger(service.time(15,59), timer_id = "shutoff")
        self.liquid_time = md.market_open_time + service.time_interval(minutes=21)
        self.illiquid_time = md.market_open_time + service.time_interval(hours=6)

    
    def on_timer(self, event, md, order, service, account):

        def case_all(ticker):
            longUnit=longUnits=shrtUnit=shrtUnits=0
            pendingBuy=pendingSell=0
            longRlz=longCash=longUnrl=0
            shrtRlz=shrtCash=shrtUnrl=0
            
            if(len(account[ticker].realized_pl.matched_trades)>0):
                ctRlz = len(account[ticker].realized_pl.matched_trades)
                Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradeMatch+=ctRlz
                
                matchedTrade=account[ticker].realized_pl.matched_trades
                
                while(ctRlz>0):
                    ctRlz-=1
                    matchedTradeUnit=matchedTrade[ctRlz]
                    
                    if(matchedTradeUnit[1][1]==1):
                        longRlz+=matchedTradeUnit[3]
                        pass
                    elif(matchedTradeUnit[1][1]==-1):
                        shrtRlz+=matchedTradeUnit[3]
                        pass
                    
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongRlz+=longRlz
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtRlz+=shrtRlz
            longPos=longUnits=longCash=longUnrl=xQuantityLong=0
            shrtPos=shrtUnits=shrtCash=shrtUnrl=xQuantityShrt=0

            if(len(account[ticker].position.inventory)>0):
            
                ctInv = len(account[ticker].position.inventory)
                inventoryItem = account[ticker].position.inventory
                
                while(ctInv>0):
                    ctInv-=1
                    
                    executedAll = inventoryItem[ctInv]
                    executed=executedAll[2]
                
                    if(executed[1]==1):
                        longPos=1
                        longUnits+=1
                        longCash=account[ticker].position.capital_long
                        longUnrl=account[ticker].unrealized_pl.entry_pl
                        tkrLong=executed[0]
                        longIndicator=executed[1]
                        xQuantityLong+=executed[2]
                        xPriceLong=executed[3]
                        xTimeLong=executed[4]
                        pass
                    elif(executed==-1):
                        shrtPos=1
                        shrtUnits+=1
                        shrtCash=account[ticker].position.capital_short
                        shrtUnrl=account[ticker].unrealized_pl.entry_pl
                        tkrShort=executed[0]
                        shortIndicator=executed[1]
                        xQuantityShrt+=executed[2]
                        xPriceShort=executed[3]
                        xTimeShort=executed[4]
                        pass
                    
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongCap+=longCash
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongUnit+=longPos
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongUnits+=longUnits
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongShares+=xQuantityLong
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongUrl+=longUnrl
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongTtl=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongRlz+Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongUrl
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtCap+=shrtCash
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtUnit+=shrtPos
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtUnits+=shrtUnits
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtShares+=xQuantityShrt
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtUrl+=shrtUnrl
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtTtl=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtRlz+Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtUrl
            pendingSell=pendingBuy=0
            
            ctPending=len(account[ticker].pending.orders)
            pendingExecution=account[ticker].pending.orders
            
            while(ctPending>0):
                ctPending-=1
                crrOrder = pendingExecution[ctPending]
                if(crrOrder[3]<0):
                    pendingSell+=1
                    pass
                elif(crrOrder[3]>0):
                    pendingBuy+=1
                    pass
                
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradePendBuy+=pendingBuy
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradePendSell+=pendingSell
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradePendTtl=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradePendBuy+Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradePendSell
            return

            
        def case_info():
            ctPositionLong=ctPositionShort=releaseItem=0
            xPriceLong=xPriceShort=[]
            
            ctInventoryItem = len(account[self.symbol].position.inventory)
            inventoryItem = account[self.symbol].position.inventory
            
            while(ctInventoryItem>0):
                ctInventoryItem-=1
  
                executedVars = inventoryItem[ctInventoryItem]
                executed=executedVars[2]
                
                if(executed[1]==1):
                    ctPositionLong+=1
                    tkrLong = executed[0]
                    longIndicator = executed[1]
                    xQuantityLong = executed[2]
                    xPriceLong.append(executed[3])
                    xTimeLong = executed[4]
                    pass
                elif(executed[1]==-1):
                    ctPositionShort+=1
                    tkrShort = executed[0]
                    shortIndicator = executed[1]
                    xQuantityShort = executed[2]
                    xPriceShort.append(executed[3])
                    xTimeShort = executed[4]
                    pass
                
            ctPending=len(account[self.symbol].pending.orders)
            pendingExecution=account[self.symbol].pending.orders
            while(ctPending>0):
                ctPending-=1
                crrOrder = pendingExecution[ctPending]
                if(crrOrder[3]<0):
                    if(min(xPriceLong)<md.L1.bid):
                        reRackOffer = order.cancel(order_id=crrOrder[10])
                        return reRackOffer
                    pass
                elif(crrOrder[3]>0):
                    #print("re-rack the bid: {}   Entry: {} Bid: {}".format(self.symbol, account[self.symbol].pending.orders[ctPending][2], md.L1.bid))
                    pass
            return
                
        def case_close_book():
            ctPending=len(account[self.symbol].pending.orders)
            pendingExecution=account[self.symbol].pending.orders
            while(ctPending>0):
                ctPending-=1
                crrOrder = pendingExecution[ctPending]
                if(crrOrder[3]<0):
                    adjustOffer = order.cancel(order_id=crrOrder[10])
                    return adjustOffer
                elif(crrOrder[3]>0):
                    pass
            return
                
        if(account[self.symbol].unrealized_pl.entry_pl>50):
            case_info()
            self.status=0
            pass

        if event.timer_id=="shutoff":
            service.terminate()
            pass
        
        if(self.symbol=="SPY"):
            self._reset_comm(md)
            allocation_key=self._allocation_key(md)
            
            # conv. account object from dict. to list.
            # access using ints.
            securities = account

            for ticker in securities:
                case_all(ticker)
                if(account[ticker].position.capital_long>0):
                    self._hedge_positions(ticker, account[ticker].position.capital_long)

            ping_book_stat=self._book_status(md, order, service, event)
            print("\nGr8Script8c04b32f5abd4c5384c2481ac2556e30.upperBand\t", Gr8Script8c04b32f5abd4c5384c2481ac2556e30.upperBand)
            print("Gr8Script8c04b32f5abd4c5384c2481ac2556e30.lowerBand\t", Gr8Script8c04b32f5abd4c5384c2481ac2556e30.lowerBand)
            ping_pl_stat=self._clear_book_status()
            ping_hedge_stat=self._adjust_hedges(event, md, order, service, account)
            pass

        if(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationStatus==1):
            # print("Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationStatus: {}\tself.symbol: {}\tself.STATUS: {}".format(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationStatus, self.symbol, self.status))
            case_close_book()
        
        
        if event.timer_id=="unload":
            if(len(account[self.symbol].pending.orders)>0):
                order.cancel(self.symbol)
                pass
            if(account[self.symbol].position.shares>0):
                self.status=5
                if(self.positionSize>0):
                    order.send(self.symbol, 'sell', account[self.symbol].position.shares, type='MKT')
                    pass
            if(account[self.symbol].position.shares<0):
                self.status=999
                if(self.positionSize<0):
                    order.send(self.symbol, 'buy', account[self.symbol].position.shares, type='MKT')
                    pass
                
        #FAVORABLE ALLOCATION CONDITIONS
        if(event.timer_id=="FiveMin" and Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationKey==1 and event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time):
            self._check_indicators(event, md, order, service, account)
            
    def _buy_limit_order_gs_smart(self, event, md, order, service, account, ordrTkr, ordrSize, ordrPrice, ordrKey, ordrIntent):
        return order.algo_buy(ordrTkr, algorithm='8b976c72-20cd-49db-9121-db2e5ace3385', intent=ordrIntent, order_quantity=ordrSize, price=ordrPrice, user_key=ordrKey, allow_multiple_pending=True)  

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

        if(event.user_key=='7e5da6c3-ff12-5858-ordr-96b59initial'):
            self.status = 2
            self.exitPrice = self.entryLevel*Gr8Script8c04b32f5abd4c5384c2481ac2556e30.testRTE
            offerInventory = self._sell_limit_order_EDGA(event, md, order, service, account, event.symbol, event.shares, self.exitPrice, '7e5da6c3-ff12-5858-r999-96b59offload', 'decrease')
            # order.algo_sell(self.symbol, algorithm='limit', intent='none', order_quantity=event.shares, price=self.exitPrice, allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-r999-96b59offload')
            return offerInventory
        if(self.status==2):
            self.orderStatus=0
            self.status=0
            pass

    def on_ack(self, event, md, order, service, account):
        if(self.status == 1):
            self.order_Enter = event.instruction_id
            pass
        if(self.status == 2):
            self.order_Exit = event.instruction_id
            pass

    def on_cancel(self, event, md, order, service, account):
        def discharge_position(pellet):
            if(event.timestamp<self.illiquid_time and account[self.symbol].position.capital_long>0):
                rePriced = self._sell_limit_order_EDGA(event, md, order, service, account, pellet[0], pellet[1], pellet[2], '7e5da6c3-ff12-5858-r999-96b59offload', 'decrease')
                # rePriced = order.algo_sell(pellet[0], algorithm='limit', intent='none', order_quantity=pellet[1], price=pellet[2], allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-r999-96b59offload')
                return rePriced

        if(event[4]=='C' and event.user_key=='7e5da6c3-ff12-5858-r999-96b59offload'):
            if(account[self.symbol].position.shares>0):
                #print(event)
                mktPrice = max(md.L1.ask, md.L1.last)
                pellet=[event[9],-event[6], mktPrice]
                reRack = discharge_position(pellet)
                return reRack
            pass

    def on_reject(self, event, md, order, service, account):
        print(event)

    def on_cancel_reject(self, event, md, order, service, account):
        pass
    
    def _clear_book_status(self):
        if(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TtlNet>Gr8Script8c04b32f5abd4c5384c2481ac2556e30.upperBand):
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.upperBand+=500
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.lowerBand=(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TtlNet/2)
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationStatus=1
        elif(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TtlNet<Gr8Script8c04b32f5abd4c5384c2481ac2556e30.lowerBand):
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.upperBand-=250
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.lowerBand-=500
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationStatus=1
        else:
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationStatus=0
        return Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationStatus
    
    def _hedge_positions(self, ticker, long_capital):
        for unit in Gr8Script8c04b32f5abd4c5384c2481ac2556e30.tkrDist:
            if(unit[0]==ticker):
                Gr8Script8c04b32f5abd4c5384c2481ac2556e30.HedgeLong+=(long_capital*unit[2])
                return Gr8Script8c04b32f5abd4c5384c2481ac2556e30.HedgeLong

    def _reset_comm(self, md):
        Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongCap=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongUnit=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongUnits=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongShares=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongRlz=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongUrl=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongTtl=0
        Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtCap=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtUnit=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtUnits=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtShares=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtRlz=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtUrl=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtTtl=0
        Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradeMatch=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradePendTtl=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradePendBuy=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradePendSell=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TtlNet=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.HedgeLong=0
        Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intervalRate.append(md.L1.percent_change_from_open)
        return Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intervalRate
    
    def _allocation_key(self, md):
        intervalChange = Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intervalRate[-1]-Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intervalRate[-2]
        if(intervalChange>0):
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationKey=0
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.accKey-=1
            pass
        else:
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationKey=1
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.accKey+=1
            pass
        if(md.L1.percent_change_from_open!=0):
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intvRate = intervalChange/md.L1.percent_change_from_open
            pass
        else:
            Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intvRate = 0
            pass
        return Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationKey
        
    def _book_status(self, md, order, service, event):
        TtlRlzd=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongRlz+Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtRlz
        TtlUnrl=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongUrl+Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtUrl
        Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TtlNet=TtlRlzd+TtlUnrl
        
        
        print("\n{}\tItr: {}    CRR%:  {}    PRR%:  {}    INTR%:  {}    KEY: {}".format(service.time_to_string(event.timestamp)[11:19], len(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intervalRate), Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intervalRate[-1], Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intervalRate[-2], Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intvRate, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationKey))
        print("L:  {}    POS:  {}    UNITS:  {}    RLZ:  {}    UNR:  {}    $NET LONG:  {}".format(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongCap, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongUnit, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongUnits, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongRlz, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongUrl, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongTtl))
        print("S:  {}    POS:  {}    UNITS:  {}    RLZ:  {}    UNR:  {}    $NET SHRT:  {}".format(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtCap, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtUnit, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtUnits, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtRlz, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtUrl, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtTtl))
        print("#CLR:  {}    LIVE:  {}    B:  {}      S:  {}    RLZ:  {}    UNR:  {}    NET:  {}".format(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradeMatch, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradePendTtl, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradePendBuy, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradePendSell, TtlRlzd,TtlUnrl,Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TtlNet))
        
        #print("\n{}\tItr: {}    CRR%:  {:.4f}    PRR%:  {:.4f}    INTR%:  {:.4f}    KEY: {}".format(service.time_to_string(event.timestamp)[11:19], len(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intervalRate), Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intervalRate[-1], Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intervalRate[-2], Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intvRate, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationKey))
        #print("L:  {:.0f}    POS:  {}    UNITS:  {}    RLZ:  {:.0f}    UNR:  {:.0f}    $NET LONG:  {:.0f}".format(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongCap, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongUnit, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongUnits, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongRlz, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongUrl, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.LongTtl))
        #print("S:  {:.0f}    POS:  {}    UNITS:  {}    RLZ:  {:.0f}    UNR:  {:.0f}    $NET SHRT:  {:.0f}".format(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtCap, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtUnit, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtUnits, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtRlz, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtUrl, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtTtl))
        #print("#CLR:  {}    LIVE:  {}    B:  {}      S:  {}    RLZ:  {:.0f}    UNR:  {:.0f}    NET:  {:.0f}".format(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradeMatch, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradePendTtl, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradePendBuy, Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TradePendSell, TtlRlzd,TtlUnrl,Gr8Script8c04b32f5abd4c5384c2481ac2556e30.TtlNet))
        return len(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intervalRate)


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
        return order.algo_buy(ordrTkr, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent=ordrIntent, order_quantity=ordrSize, user_key=ordrKey)
    
    
    def _adjust_hedges(self, event, md, order, service, account):
        hedgeTwo = Gr8Script8c04b32f5abd4c5384c2481ac2556e30.HedgeLong
        print("HEDGE:\t{}   ".format(hedgeTwo))
        if(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationKey==0):
            if(abs(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtCap)<hedgeTwo):
                self.spyQTY = int((abs(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtCap)-hedgeTwo)/1200)
                if(self.spyQTY!=0):
                    if(account[self.symbol].position.shares>0):
                        short = self._sell_market_gs_smart(event, md, order, service, account, self.symbol, self.spyQTY, '7e5da6c3-add1-5858-rSPY-96b59ofhedge', 'decrease')
                        return short
                    elif(account[self.symbol].position.shares<0):
                        short = self._sell_market_gs_smart(event, md, order, service, account, self.symbol, self.spyQTY, '7e5da6c3-add1-5858-rSPY-96b59ofhedge', 'increase')
                        return short
                    elif(account[self.symbol].position.shares==0):    
                        short = self._sell_market_gs_smart(event, md, order, service, account, self.symbol, self.spyQTY, '7e5da6c3-add1-5858-rSPY-96b59ofhedge', 'init')
                        return short
                    else:
                        pass
                    pass
        elif(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationKey==1):        
            if(abs(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtCap)>hedgeTwo):
                self.spyQTY = int((abs(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.ShrtCap)-hedgeTwo)/1200)
                if(self.spyQTY!=0):
                    if(account[self.symbol].position.shares>0):
                        shrtBalance = self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, self.spyQTY, '7e5da6c3-add1-5858-rSPY-96b59ofhedge', 'increase')
                        return shrtBalance
                    elif(account[self.symbol].position.shares<0):
                        shrtBalance = self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, self.spyQTY, '7e5da6c3-add1-5858-rSPY-96b59ofhedge', 'decrease')
                        return shrtBalance
                    elif(account[self.symbol].position.shares==0):
                        shrtBalance = self._buy_market_order_gs_smart(event, md, order, service, account, self.symbol, self.spyQTY, '7e5da6c3-add1-5858-rSPY-96b59ofhedge', 'init')
                        return shrtBalance
                    else:
                        pass
                    pass
        return hedgeTwo

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
            while(indication>=0):
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
                if(indication>=Gr8Script8c04b32f5abd4c5384c2481ac2556e30.allocationModel):
                    self.status=1
                    self.orderStatus=1
                    self.pendingKey=len(Gr8Script8c04b32f5abd4c5384c2481ac2556e30.intervalRate)
                    self.entryLevel = min(min(bar20m.open[:-17]), min(bar20m.close[:-17]))
                    self.positionSize= int(self.riskMax/self.entryLevel)
                    if(self.symbol!="SPY"):
                        if(account[self.symbol].position.shares==0):
                            pricedBid = self._buy_limit_order_gs_smart(event, md, order, service, account, self.symbol, self.positionSize, self.entryLevel, '7e5da6c3-ff12-5858-ordr-96b59initial', 'init')
                            return pricedBid
                        else:
                            pricedBid = self._buy_limit_order_gs_smart(event, md, order, service, account, self.symbol, self.positionSize, self.entryLevel, '7e5da6c3-ff12-5858-ordr-96b59initial', 'increase')
                            return pricedBid
                        # order.algo_buy(self.symbol, algorithm='limit', intent='increase', order_quantity=self.positionSize, price=self.entryLevel, allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
                        # pass
                    complexA=0
                    break
                else:
                    break
        pass

