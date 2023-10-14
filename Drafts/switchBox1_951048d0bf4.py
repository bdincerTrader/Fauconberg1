from cloudquant.interfaces import Strategy, Event
import ktgfunc
tickerUniv = ['AA','AAL','AAP','AAPL','AAXJ','ABB','ABBV','ABT','ACAD','ACGL','ACI','ACLS','ACN','ADM','ADP','ADSK','ADT','AEE','AEM','AEO','AEP','AER','AG','AGG','AJG','AKAM','ALB','ALC','ALGN', 'SPY']


class Gr8Script83f2ca8b951048d0bf486a832e212f5c(Strategy):
    __script_name__ = 'switchBox1'
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
    riskMax=100000
    intervalRate=[0]
    tkrDist = [('AA', 'MATS', 2.4513), ('AAL', 'ARLN', 1.5494), ('AAP', 'AUTO', 1.1371), ('AAPL', 'TECH', 1.2932), ('AAXJ', 'MISC', 0.8729), ('ABB', 'ENGN', 1.1471), ('ABBV', 'PHRM', 0.552), ('ABT', 'HLTH', 0.6638), ('ACAD', 'BIOT', 0.5551), ('ACGL', 'INSU', 0.7304), ('ACI', 'FOOD', 0), ('ACLS', 'TECH', 1.7267), ('ACN', 'TECH', 1.2412), ('ADM', 'TBCO', 0.8028), ('ADP', 'SRVC', 0.8174), ('ADSK', 'TECH', 1.5331), ('ADT', 'SRVC', 1.7105), ('AEE', 'UTIL', 0.4414), ('AEM', 'MATS', 0.696), ('AEO', 'RETL', 1.5148), ('AEP', 'UTIL', 0.4498), ('AER', 'BRKR', 2.0066), ('AG', 'MATS', 0.9213), ('AGG', 'MISC', -0.0153), ('AJG', 'INSU', 0.7003), ('AKAM', 'TECH', 0.8028), ('ALB', 'MATS', 1.5597), ('ALC', 'HLTH', 0.95), ('ALGN', 'HLTH', 1.595)]

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol in tickerUniv
 
    def on_start(self, md, order, service, account):
        self.status=self.entryLevel=self.entryLevel=self.exitPrice=self.orderStatus=self.positionSize=self.pendingKey=self.spyQTY=0
        self.order_Enter=self.order_Exit="0"
        
        self.delay = service.time_interval(seconds=5)
        self.twoMin = service.time_interval(minutes=1)
        self.fiveMin = service.time_interval(minutes=1)
        self.tenMin = service.time_interval(minutes=10)
        self.twentyMin = service.time_interval(minutes=20)
        self.oneHour = service.time_interval(hours=1)
        self.timerInterval = service.time_interval(seconds=30)
        service.clear_event_triggers()
        # type = service.symbol_list.in_list(service.symbol_list.get_handle('0e788f9d-4c44-4724-8581-21ef7e5dad09'), self.symbol)
        if(Gr8Script83f2ca8b951048d0bf486a832e212f5c.intervalRate[0]==0):
            print("PL MODEL: {}.{}\tTIMER: {}\tRTE: {}\tTRADE DATE: {}".format(Gr8Script83f2ca8b951048d0bf486a832e212f5c.allocationModel, Gr8Script83f2ca8b951048d0bf486a832e212f5c.upperBand, self.timerInterval, Gr8Script83f2ca8b951048d0bf486a832e212f5c.testRTE, service.time_to_string(service.system_time)))
        Gr8Script83f2ca8b951048d0bf486a832e212f5c.intervalRate[0]=0.0001
        for unit in Gr8Script83f2ca8b951048d0bf486a832e212f5c.tkrDist:
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
        
        def case_all():

            
            for ticker in Gr8Script83f2ca8b951048d0bf486a832e212f5c.tickerItr:
            
                longUnit=longUnits=shrtUnit=shrtUnits=0
                pendingBuy=pendingSell=0
                longRlz=longCash=longUnrl=0
                shrtRlz=shrtCash=shrtUnrl=0
            
                if(len(account[ticker].realized_pl.matched_trades)>0):
                    for items in account[ticker].position.inventory:
                        if(ticker!="SPY"):
                            longRlz+=account[ticker].realized_pl.entry_pl
                        elif(ticker=="SPY"):    
                            shrtRlz+=account[ticker].realized_pl.entry_pl
                          
                                    
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongRlz+=longRlz
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtRlz+=shrtRlz
                longPos=longUnits=longCash=longUnrl=xQuantityLong=0
                shrtPos=shrtUnits=shrtCash=shrtUnrl=xQuantityShrt=0
    
                if(len(account[ticker].position.inventory)>0):
                    ctInv = len(account[ticker].position.inventory)
                    while(ctInv>0):
                        ctInv-=1
                        if(account[ticker].position.capital_long>0):
                            longPos=1
                            longUnits+=1
                            longCash=account[ticker].position.capital_long
                            longUnrl=account[ticker].unrealized_pl.entry_pl
                            xQuantityLong+=account[ticker].position.shares
                            xPriceLong=account[ticker].position.entry_price
                            pass
                        elif(account[ticker].position.capital_short>0):
                            shrtPos=1
                            shrtUnits+=1
                            shrtCash=account[ticker].position.capital_short
                            shrtUnrl=account[ticker].unrealized_pl.entry_pl
                            xQuantityShrt+=account[ticker].position.shares
                            xPriceShort=account[ticker].position.entry_price
                            pass
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongCap+=longCash
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongUnit+=longPos
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongUnits+=longUnits
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongShares+=xQuantityLong
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongUrl+=longUnrl
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongTtl=Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongRlz+Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongUrl
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtCap+=shrtCash
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtUnit+=shrtPos
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtUnits+=shrtUnits
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtShares+=xQuantityShrt
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtUrl+=shrtUnrl
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtTtl=Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtRlz+Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtUrl
                pendingSell=pendingBuy=0
                
                ctPnd=len(account[ticker].pending.orders)
                while(ctPnd>0):
                    ctPnd-=1
                    if(account[ticker].pending.shares_short<0):
                        pendingSell+=1
                        pass
                    elif(account[ticker].pending.shares_long>0):
                        pendingBuy+=1
                        pass
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.TradePendBuy+=pendingBuy
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.TradePendSell+=pendingSell
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.TradePendTtl=Gr8Script83f2ca8b951048d0bf486a832e212f5c.TradePendBuy+Gr8Script83f2ca8b951048d0bf486a832e212f5c.TradePendSell
            


        def case_close_book():
            ctPending=len(account[self.symbol].pending.orders)
            while(ctPending>0):
                ctPending-=1
                if(account[self.symbol].pending.shares_short<0):
                    order.cancel(order_id=account[self.symbol].pending.orders[ctPending][10])
                    pass
                elif(account[self.symbol].pending.shares_long>0):
                    pass
        
        # checks to see if an inventory position is not currenly being offered,
        
        if(account[self.symbol].position.shares+account[self.symbol].pending.shares_short>0):
            qtOffer = account[self.symbol].position.shares+account[self.symbol].pending.shares_short
            pxEntry = account[self.symbol].position.entry_price
            pxOffer = pxEntry*1.0023
            print(self.symbol, account[self.symbol].position.shares, account[self.symbol].pending.shares_short, qtOffer, pxEntry, pxOffer)
            
            # Sell Limit EDGX
            order.algo_sell(self.symbol, algorithm='96317801-94be-47d7-9dff-3b398e518c93', intent='decrease', order_quantity=qtOffer, price=pxEntry*1.0023, allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-r999-96b59offload')
            
            # IOC LIMIT ORDER       
            #order.algo_sell(self.symbol, algorithm='8e0f3d16-1be3-4599-a143-be49bf7e10fc', intent='decrease', order_quantity=qtycheck, price=pxCheck*1.0023, allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-r999-96b59offload')
            #order.algo_sell(self.symbol, algorithm='8e0f3d16-1be3-4599-a143-be49bf7e10fc', intent='increase', order_quantity=50, price=md.L1.last*1.007,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-r999-96b59offload')
        
        
        # checks the P&L on the position and offers it more aggressively.
        def case_info():
            ctPositionLong=ctPositionShort=0
            posNetPx = account[self.symbol].position.entry_price
            print("CASE INFO: account[self.symbol].position.inventory")
            print(account[self.symbol].position.inventory)
            
            print('account[self.symbol].pending.orders')
            print(account[self.symbol].pending.orders)

            print('account[self.symbol].pending')
            print(account[self.symbol].pending)
            
            ctPending=len(account[self.symbol].pending.orders)
            cancelSize=0
            while(ctPending>0):
                caseInfoLogic=0
                ctPending-=1
                if(account[self.symbol].pending.shares_short<0):
                    if(posNetPx<md.L1.bid):
                        print("CANCEL AND RE-POST")
                        try:
                            cancelSize += order.cancel(order_id=account[self.symbol].pending.orders[ctPending][10])
                        except:
                            pass
                    pass
                elif(account[self.symbol].pending.shares_long>0):
                    pass
            
            print("cancelSize", cancelSize)
            if(cancelSize>0):
                rePrice = max(md.L1.ask, md.L1.last)
                order.algo_sell(self.symbol, algorithm='96317801-94be-47d7-9dff-3b398e518c93', intent='decrease', order_quantity=cancelSize, price=rePrice, allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-r999-96b59offload')
                pass
                
        # checks the P&L on the position and offers it more aggressively.        
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
            
            case_all()
            for ticker in Gr8Script83f2ca8b951048d0bf486a832e212f5c.tickerItr:
                if(account[ticker].position.capital_long>0):
                    self._hedge_positions(ticker, account[ticker].position.capital_long)

            ping_book_stat=self._book_status(md, order, service, event)
            ping_pl_stat=self._clear_book_status()
            ping_hedge_stat=self._adjust_hedges(event, md, order, service, account)
            pass

        if(Gr8Script83f2ca8b951048d0bf486a832e212f5c.allocationStatus==999):
            case_close_book()
        
        
        if event.timer_id=="unload":
            if(len(account[self.symbol].pending.orders)>0):
                order.cancel(self.symbol)
                pass
            if(account[self.symbol].position.shares>0):
                self.status=5
                if(self.positionSize>0):
                    # market order to exit EOD
                    order.algo_sell(self.symbol, algorithm='8fdee8fe-b772-46bd-b411-5544f7a0d917', intent='decrease', order_quantity=account[self.symbol].position.shares, user_key='7e5da6c3-ff12-5858-r999-96b59offlEOD')
                    pass
            if(account[self.symbol].position.shares<0):
                self.status=999
                if(self.positionSize<0):
                    order.send(self.symbol, 'buy', account[self.symbol].position.shares, type='MKT')
                    pass
                
        #FAVORABLE ALLOCATION CONDITIONS
        if(event.timer_id=="FiveMin" and Gr8Script83f2ca8b951048d0bf486a832e212f5c.allocationKey==1 and event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time):
            self._check_indicators(event, md, order, service, account)
            

    def on_fill(self, event, md, order, service, account):
        # print(event)
        pass


    def on_ack(self, event, md, order, service, account):
        # print(event)
        if(self.status == 1):
            self.order_Enter = event.instruction_id
            pass
        if(self.status == 2):
            self.order_Exit = event.instruction_id
            pass
            
    def on_cancel(self, event, md, order, service, account):
        if(event[4]=='C' and event.user_key=='7e5da6c3-ff12-5858-r999-96b59offload'):
            if(type(event[6]) is int):
                return -event[6]
        else:
            return 0

    def on_reject(self, event, md, order, service, account):
        print(event)

    def on_cancel_reject(self, event, md, order, service, account):
        pass
    
    def _clear_book_status(self):
        if(Gr8Script83f2ca8b951048d0bf486a832e212f5c.TtlNet>Gr8Script83f2ca8b951048d0bf486a832e212f5c.upperBand):
            Gr8Script83f2ca8b951048d0bf486a832e212f5c.upperBand+=500
            Gr8Script83f2ca8b951048d0bf486a832e212f5c.lowerBand=(Gr8Script83f2ca8b951048d0bf486a832e212f5c.TtlNet/2)
            Gr8Script83f2ca8b951048d0bf486a832e212f5c.allocationStatus=1
        elif(Gr8Script83f2ca8b951048d0bf486a832e212f5c.TtlNet<Gr8Script83f2ca8b951048d0bf486a832e212f5c.lowerBand):
            Gr8Script83f2ca8b951048d0bf486a832e212f5c.upperBand-=250
            Gr8Script83f2ca8b951048d0bf486a832e212f5c.lowerBand-=500
            Gr8Script83f2ca8b951048d0bf486a832e212f5c.allocationStatus=1
        else:
            Gr8Script83f2ca8b951048d0bf486a832e212f5c.allocationStatus=0
        return Gr8Script83f2ca8b951048d0bf486a832e212f5c.allocationStatus
    
    def _hedge_positions(self, ticker, long_capital):
        for unit in Gr8Script83f2ca8b951048d0bf486a832e212f5c.tkrDist:
            if(unit[0]==ticker):
                Gr8Script83f2ca8b951048d0bf486a832e212f5c.HedgeLong+=(long_capital*unit[2])

    def _reset_comm(self, md):
        Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongCap=Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongUnit=Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongUnits=Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongShares=Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongRlz=Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongUrl=Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongTtl=0
        Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtCap=Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtUnit=Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtUnits=Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtShares=Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtRlz=Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtUrl=Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtTtl=0
        Gr8Script83f2ca8b951048d0bf486a832e212f5c.TradeMatch=Gr8Script83f2ca8b951048d0bf486a832e212f5c.TradePendTtl=Gr8Script83f2ca8b951048d0bf486a832e212f5c.TradePendBuy=Gr8Script83f2ca8b951048d0bf486a832e212f5c.TradePendSell=Gr8Script83f2ca8b951048d0bf486a832e212f5c.TtlNet=Gr8Script83f2ca8b951048d0bf486a832e212f5c.HedgeLong=0
        Gr8Script83f2ca8b951048d0bf486a832e212f5c.intervalRate.append(md.L1.percent_change_from_open)
        return 0
    
    def _allocation_key(self, md):
        intervalChange = Gr8Script83f2ca8b951048d0bf486a832e212f5c.intervalRate[-1]-Gr8Script83f2ca8b951048d0bf486a832e212f5c.intervalRate[-2]
        if(intervalChange>0):
            Gr8Script83f2ca8b951048d0bf486a832e212f5c.allocationKey=0
            Gr8Script83f2ca8b951048d0bf486a832e212f5c.accKey-=1
            pass
        else:
            Gr8Script83f2ca8b951048d0bf486a832e212f5c.allocationKey=1
            Gr8Script83f2ca8b951048d0bf486a832e212f5c.accKey+=1
            pass
        if(md.L1.percent_change_from_open!=0):
            Gr8Script83f2ca8b951048d0bf486a832e212f5c.intvRate = intervalChange/md.L1.percent_change_from_open
            pass
        else:
            Gr8Script83f2ca8b951048d0bf486a832e212f5c.intvRate = 0
            pass
        return Gr8Script83f2ca8b951048d0bf486a832e212f5c.allocationKey
        
    def _book_status(self, md, order, service, event):
        TtlRlzd=Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongRlz+Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtRlz
        TtlUnrl=Gr8Script83f2ca8b951048d0bf486a832e212f5c.LongUrl+Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtUrl
        Gr8Script83f2ca8b951048d0bf486a832e212f5c.TtlNet=TtlRlzd+TtlUnrl
        return len(Gr8Script83f2ca8b951048d0bf486a832e212f5c.intervalRate)

    def _adjust_hedges(self, event, md, order, service, account):
        hedgeTwo = Gr8Script83f2ca8b951048d0bf486a832e212f5c.HedgeLong
        if(Gr8Script83f2ca8b951048d0bf486a832e212f5c.allocationKey==0):
            if(abs(Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtCap)<hedgeTwo):
                self.spyQTY = int((abs(Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtCap)-hedgeTwo)/400)
                if(self.spyQTY!=0):
                    #order.send('SPY', 'sell', self.spyQTY, type='MKT')
                    pass
        elif(Gr8Script83f2ca8b951048d0bf486a832e212f5c.allocationKey==1):        
            if(abs(Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtCap)>hedgeTwo):
                self.spyQTY = int((abs(Gr8Script83f2ca8b951048d0bf486a832e212f5c.ShrtCap)-hedgeTwo)/400)
                if(self.spyQTY!=0):
                    #order.send('SPY', 'buy', self.spyQTY, type='MKT')
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
            
        barPointA = event.timestamp-1260000001
        barPointB = event.timestamp
        bar20m = md.bar.minute(start=barPointA, end=barPointB, include_extended=True, today_only=False)
        #ONMINUTEBAR
        #order.algo_buy(self.symbol, algorithm='ab6c31db-1440-4501-87fe-446a208227a8', intent='increase', order_quantity=50, price=md.L1.last,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
          
        #order.algo_sell(self.symbol, algorithm='8e0f3d16-1be3-4599-a143-be49bf7e10fc', intent='increase', order_quantity=5, price=md.L1.last*1.007,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-r999-96b59offload')
        #order.algo_sell(self.symbol, algorithm='5366bcdd-6cb8-4570-b328-f4d04e733be1', intent='increase', order_quantity=21, price=md.L1.last*1.007,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-r999-96b59offload')
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
                    #order.algo_buy(self.symbol, algorithm='ab6c31db-1440-4501-87fe-446a208227a8', intent='increase', order_quantity=indication, price=md.L1.last,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
                    pass
                if((basePx-bar20m.vwap[-1])>0):
                    indication+=1
                    #order.algo_buy(self.symbol, algorithm='ab6c31db-1440-4501-87fe-446a208227a8', intent='increase', order_quantity=indication, price=md.L1.last,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
                    pass
                if((basePx-bar20m.open[-1])>0):
                    indication+=1
                    #order.algo_buy(self.symbol, algorithm='ab6c31db-1440-4501-87fe-446a208227a8', intent='increase', order_quantity=indication, price=md.L1.last,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
                    pass
                if((basePx-bar20m.close[-1])>0):
                    indication+=1
                    #order.algo_buy(self.symbol, algorithm='ab6c31db-1440-4501-87fe-446a208227a8', intent='increase', order_quantity=indication, price=md.L1.last,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
                    pass
                if(bar20m.low[-1]>bar20m.high[complexB]):
                    indication+=1
                    #order.algo_buy(self.symbol, algorithm='ab6c31db-1440-4501-87fe-446a208227a8', intent='increase', order_quantity=indication, price=md.L1.last,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
                    pass
                if(bar20m.low[-1]>bar20m.vwap[complexB]):
                    indication+=1
                    #order.algo_buy(self.symbol, algorithm='ab6c31db-1440-4501-87fe-446a208227a8', intent='increase', order_quantity=indication, price=md.L1.last,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
                    pass
                if(bar20m.low[-1]>bar20m.open[complexB]):
                    indication+=1
                    #order.algo_buy(self.symbol, algorithm='ab6c31db-1440-4501-87fe-446a208227a8', intent='increase', order_quantity=indication, price=md.L1.last,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
                    pass
                if(bar20m.open[-1]>bar20m.close[complexB]):
                    indication+=1
                    order.algo_buy(self.symbol, algorithm='ab6c31db-1440-4501-87fe-446a208227a8', intent='increase', order_quantity=indication, price=md.L1.last,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
                    pass
                if(basePx>bar20m.high[complexB]):
                    indication+=1
                    order.algo_buy(self.symbol, algorithm='ab6c31db-1440-4501-87fe-446a208227a8', intent='increase', order_quantity=indication, price=md.L1.last,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
                    pass
                if(basePx>bar20m.vwap[complexB]):
                    indication+=1
                    order.algo_buy(self.symbol, algorithm='ab6c31db-1440-4501-87fe-446a208227a8', intent='increase', order_quantity=indication, price=md.L1.last,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
                    pass
                if(bar20m.spread[-1]>bar20m.spread[complexB]):
                    indication+=1
                    order.algo_buy(self.symbol, algorithm='ab6c31db-1440-4501-87fe-446a208227a8', intent='increase', order_quantity=indication, price=md.L1.last,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
                    pass
                if(indication>=Gr8Script83f2ca8b951048d0bf486a832e212f5c.allocationModel):
                    self.status=1
                    self.orderStatus=1
                    self.pendingKey=len(Gr8Script83f2ca8b951048d0bf486a832e212f5c.intervalRate)
                    self.entryLevel = min(min(bar20m.open[:-17]), min(bar20m.close[:-17]))
                    self.positionSize= int(Gr8Script83f2ca8b951048d0bf486a832e212f5c.riskMax/self.entryLevel)
                    if(self.symbol!="SPY"):
                        #order.algo_buy(self.symbol, algorithm='ab6c31db-1440-4501-87fe-446a208227a8', intent='increase', order_quantity=50, price=md.L1.last,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
                        #order.algo_buy(self.symbol, algorithm='ab6c31db-1440-4501-87fe-446a208227a8', intent='increase', order_quantity=self.positionSize, price=self.entryLevel,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
                        #order.algo_buy(self.symbol, algorithm='f05365c7-408e-4db2-87d0-e3608d5a1039', intent='increase', order_quantity=self.positionSize, price=self.entryLevel,  allow_multiple_pending=True, user_key='7e5da6c3-ff12-5858-ordr-96b59initial')
                        pass
                    complexA=0
                    break
                else:
                    break   
