# Editor
# switchBox51OBSERVE   BDincer   5/25/2023 9:51:43 PM   QA-2.0.158
# N-00006   qabdincer/d1c248
# Voodoo=c982d0cd-9be5-4a35-b89f-1f66b2495ec4 Sell Limit ARCA at Script Price
# Voodoo=97a91492-1033-4a96-a546-9bff6df73b08 Buy Limit ARCA at Script Price
# Voodoo=8fa5330d-b32d-4083-86eb-d9a61a637b8b Sell Market GS SOR
# Voodoo=9e6b50d6-dee3-4314-a43b-49e9ae8088b6 Buy Market GS SOR

from cloudquant.interfaces import Strategy
import time, random, os

class Gr8Script126c752dd9b048b1ac18695a43ca97ec(Strategy):
    __script_name__ = 'switchBox51OBSERVE'
    
    strategyKey=0;allocationModel=10;testRTE=1.0057;riskMax=1500;
    
    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol == 'SWN'
        
    def __init__(self, **params):
        if('riskAllocation' in params):
            print(params['riskAllocation'])
            self.__class__.riskMax=params['riskAllocation'];
            
    
    def on_start(self, md, order, service, account):
        self.plMaxLoss=-self.__class__.riskMax*0.20;
        self.plUnrlRTE=self.__class__.riskMax*0.001;
        self.upperBand=self.__class__.riskMax*0.01;
        self.lowerBand=-self.__class__.riskMax*0.01;
        self.bandMult=self.__class__.riskMax*0.01;
        self.intervalRate=[0];
        self.rejectChecker=self.intvRate=self.accKey=0;
        self.allocationKey=1;
        self.yesterdayPrice = max(md.stat.prev_close, md.L1.open)
        if(self.yesterdayPrice == 0):
            self.yesterdayPrice = 500

        self.entryLevel=self.exitPrice=self.positionSize=self.spyQTY=0;
        self.cancelOrderBook=self.checkPendingBook=[];
        self.maxAllocate=int(self.yesterdayPrice*1.10);
        self.delay = service.time_interval(seconds=5);
        self.twentyMin = service.time_interval(minutes=20);
        self.underChecker=30;

        if(self.intervalRate[0]==0):
            print("TKR:{}\tPL MODEL: {}.{}\RISKMAX: {}\tRTE: {}\tTRADE DATE: {}".format(self.symbol, self.__class__.allocationModel, self.upperBand, self.__class__.riskMax, self.__class__.testRTE, service.time_to_string(service.system_time)))
        self.intervalRate[0]=0.0001;
        
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=5), repeat_interval=service.time_interval(seconds=5), timer_id="Allocate")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=16), timer_id = "eod_1")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=12), timer_id = "eod_2")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=5), timer_id = "eod_3")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=3), timer_id = "eod_4")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=2), timer_id = "eod_5")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=1), timer_id = "eod_6")
        self.liquid_time = md.market_open_time + service.time_interval(minutes=21)
        self.illiquid_time = md.market_close_time - service.time_interval(minutes=30)

    
    def on_timer(self, event, md, order, service, account):
        
        def underChecker():
            reRouteInventory=account[self.symbol].pending.orders;
            livePending=len(reRouteInventory);
            while(livePending>0):
                livePending-=1
                pendingExecution=reRouteInventory[livePending]
                if(pendingExecution.shares<0):
                    if(pendingExecution.price<md.L1.bid and event.timestamp<self.illiquid_time):
                        order.cancel(order_id=pendingExecution.order_id);
                        pass
                    pass
            return 1;
            
        def case_lower():
            adjustAsk=account[self.symbol].pending.orders; ctPend=len(adjustAsk);
            while(ctPend>0):
                ctPend-=1; pendingUnit=adjustAsk[ctPend];
                if(pendingUnit.shares<0):
                    if(pendingUnit.price<md.L1.bid):
                        order.cancel(order_id=pendingUnit.order_id);
                        pass;
                    pass;
            return 1;
        
        def turnover():
            turndownSymbol=account[self.symbol].pending.orders;
            ctTurnover=len(account[self.symbol].pending.orders);
            while(ctTurnover>0):
                ctTurnover-=1; cxlExecution=turndownSymbol[ctTurnover];
                if(cxlExecution.shares<0 and event.timestamp<self.illiquid_time):
                    order.cancel(order_id=cxlExecution.order_id);
                    pass;
            return 1;
        
        def case_close_strategy():
            turnoffSymbol=account[self.symbol].pending.orders; optimizer=len(turnoffSymbol);
            while(optimizer>0):
                optimizer-=1; clsUnit = turnoffSymbol[optimizer];
                if(clsUnit.shares<0 and event.timestamp<self.illiquid_time):
                    order.cancel(order_id=clsUnit.order_id);
                    pass;
                elif(clsUnit.shares>0):
                    order.cancel(order_id=clsUnit.order_id);
                    pass;
            return 1;
        
        ##########################################################################
        ## REJECT ORDER MANAGEMENT 
        ##########################################################################
        if(self.rejectChecker>10): return;
        ##########################################################################
        ## PL IS NOT SUFFICIENT  --- TURN THE SYSTEM OFF SEQUENCE 
        ##########################################################################
        if(self.__class__.strategyKey==1 and len(account[self.symbol].pending.orders)==0 and account[self.symbol].position==0): service.terminate();
        if(self.__class__.strategyKey==1 and len(account[self.symbol].pending.orders)==0 and len(account[self.symbol].position.inventory)==0): return;
        if(self.__class__.strategyKey==1): case_close_strategy(); pass;
        if(account.realized_mtm_pl+account.unrealized_entry_pl<self.plMaxLoss and self.__class__.strategyKey==0): self.__class__.strategyKey=1; case_close_strategy(); pass;
        
        ##########################################################################
        ## UNREALIZED PL IS SUFFICIENT      --- CLOSE THE POSITION 
        ##########################################################################
        if(account[self.symbol].position.entry_price>md.L1.bid):
            allocated=account[self.symbol].position.entry_price;
            marketBid=md.L1.bid;
            shares=account[self.symbol].position.shares;
            ##########################################################################
            ## CHK overChecker
            ##########################################################################
            print("RTS\t", allocated, marketBid, shares, allocated-marketBid)
            pass
        
        print("underchecker key", self.underChecker)
        if(account[self.symbol].unrealized_pl.entry_pl>self.plUnrlRTE):
            self.underChecker-=1;
            if(self.underChecker==29): underChecker();pass;
        else: self.underChecker=30;
        ##########################################################################
        ## UNREALIZED PL IS NOT SUFFICIENT  --- CLOSE THE POSITION 
        ##########################################################################
        if(account[self.symbol].unrealized_pl.entry_pl<-self.plUnrlRTE): case_lower();pass;
        
        ##########################################################################
        ## UNIT CANCELLED --- CAN REPRICE THE ORIGINAL OFFER THAT WAS CANCELLED
        ##########################################################################
        i=0
        if(event.timestamp<self.illiquid_time):
            chkBar=md.bar.minute_by_index(-5);
            print('chkBAR: OPEN CLOSE BVWAP HIGH')
            print(chkBar.open)
            print(chkBar.close)
            print(chkBar.bvwap)
            print(chkBar.high)
            if(len(chkBar.open)>1 and len(chkBar.close)>1 and len(chkBar.bvwap)>1 and len(chkBar.high)>1):
                chkUpperBar=max(max(chkBar.open), max(chkBar.close), max(chkBar.bvwap), max(chkBar.high));
                print('chkUpperBar')
                print(chkUpperBar)
                for unitsCancelled in self.cancelOrderBook:
                    mktPrice=chkUpperBar+(random.randint(0, 50)/10000);
                    if(unitsCancelled[3]==112):
                        upperChecker = order.algo_sell(unitsCancelled[0], algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=-unitsCancelled[1], price=mktPrice, user_key=112, allow_multiple_pending=40)
                        self.cancelOrderBook.pop(i)
                        i+=1
                        pass
        ##########################################################################
        ## SPY FUNCTIONS.
        ##########################################################################
        self.intervalRate.append(md.L1.percent_change_from_open)
        allocation_key=self._allocation_key(md)
        
        _allocation_Stat=self._clear_book_status(account)
        if(_allocation_Stat==1): turnover();pass;
        if(md.L1.is_halted==True): return;
        ##########################################################################
        ## EQUITY ALLOCATION
        ##########################################################################
        if(event.timer_id=="Allocate" and self.allocationKey==1 and event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time): self._check_indicators(event, md, order, service, account); pass;
            
        if(event.timer_id=="eod_1" or event.timer_id=="eod_2" or event.timer_id=="eod_3" or event.timer_id=="eod_4" or event.timer_id=="eod_5" or event.timer_id=="eod_6"):
            self.eod_functions(event, md, order, service, account)
            pass
        

    def on_fill(self, event, md, order, service, account):
        if(event.user_tag==111):
            randAdjust=random.randint(0, 50)/10000;
            self.exitPrice = event.price*self.__class__.testRTE-randAdjust
            if(event.intent in ["increase", "init"] and service.instruction_id == event.instruction_id):
                offerInventory = order.algo_sell(event.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity= event.shares, price=self.exitPrice, user_key=112, allow_multiple_pending=40)
                return offerInventory;
            else: return 0;
        else: return 0;

    def on_cancel(self, event, md, order, service, account):
        if(event.user_tag==112 and event.timestamp<self.illiquid_time): evtUnit=[event.symbol, event.shares, event.price, event.user_tag]; self.cancelOrderBook.append(evtUnit);return 1;
        else: return 0;

    def _clear_book_status(self, account):
        TtlNet=account[self.symbol].unrealized_pl.entry_pl+account[self.symbol].realized_pl.entry_pl_long;
        if(TtlNet>self.upperBand): self.upperBand=TtlNet+self.bandMult; self.lowerBand=TtlNet-self.bandMult; return 1;
        elif(TtlNet<self.lowerBand): self.upperBand=TtlNet+self.bandMult; self.lowerBand=TtlNet-self.bandMult; return 1;
        else: return 0;
    
    def _allocation_key(self, md):
        intervalChange = self.intervalRate[-1]-self.intervalRate[-2]
        if(intervalChange>0): self.allocationKey=0; self.accKey-=1;pass;
        else: self.allocationKey=1; self.accKey+=1; pass;
            
        if(md.L1.percent_change_from_open!=0): self.intvRate = intervalChange/md.L1.percent_change_from_open;pass;
        else: self.intvRate=0;pass;
        return self.allocationKey;
        

    def _check_indicators(self, event, md, order, service, account):

        def test_A(case1, case2):
            if(case1>case2): return 1;
            else: return 0;
            
        def test_B(case1, case2):
            if(case1>case2): return 0;
            else: return 1;
        
        barPointB = event.timestamp;
        barPointA = barPointB-1205000000;        
        bar20m = md.bar.minute(start=barPointA, end=barPointB, include_extended=True, today_only=False)
        #ONMINUTEBAR
        if(len(bar20m.high)>15 and len(bar20m.low)>15 and len(bar20m.spread)>15 and len(bar20m.askvol)>15 and len(bar20m.bidvol)>15 and len(bar20m.close)>15 and len(bar20m.bvwap)>15 and len(bar20m.open)>15 and len(bar20m.volume)>15):
            complexA=complexB=indication=-1;
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
                complexA=-1;complexB=0; indication=2;pass;
            elif(chk12A>0 and chk13B>0):
                complexA=-1;complexB=10;indication=2;pass;
            elif(chk12A>0 and chk13C>0):
                complexA=-1;complexB=15;indication=2;pass;
            elif(chk12A>0 and chk13x>0):
                complexA=-1;complexB=0; indication=2;pass;
            elif(chk12A>0 and chk13y>0):
                complexA=-1;complexB=10;indication=2;pass;
            elif(chk12A>0 and chk13z>0):
                complexA=-1;complexB=15;indication=2;pass;
            elif(chk12B>0 and chk13A>0):
                complexA=-1; complexB=0;indication=2;pass;
            elif(chk12B>0 and chk13B>0):
                complexA=-1; complexB=10;indication=2;pass;
            elif(chk12B>0 and chk13C>0):
                complexA=-1;complexB=15;indication=2;pass;
            elif(chk12B>0 and chk13x>0):
                complexA=-1;complexB=0;indication=2;pass;
            elif(chk12B>0 and chk13y>0):
                complexA=-1;complexB=10;indication=2;pass;
            elif(chk12B>0 and chk13z>0):
                complexA=-1;complexB=15;indication=2;pass;
            while(indication>0):
                basePx = md.L1.last;
                if((basePx-bar20m.low[-1])>0): indication+=1;pass;
                if((basePx-bar20m.vwap[-1])>0): indication+=1;pass;
                if((basePx-bar20m.open[-1])>0): indication+=1;pass;
                if((basePx-bar20m.close[-1])>0): indication+=1;pass;
                if(bar20m.low[-1]>bar20m.high[complexB]): indication+=1;pass;
                if(bar20m.low[-1]>bar20m.bvwap[complexB]): indication+=1;pass;
                if(bar20m.low[-1]>bar20m.open[complexB]): indication+=1;pass;
                if(bar20m.open[-1]>bar20m.close[complexB]): indication+=1;pass;
                if(basePx>bar20m.high[complexB]): indication+=1;pass;
                if(basePx>bar20m.bvwap[complexB]): indication+=1;pass;
                if(bar20m.spread[-1]>bar20m.spread[complexB]): indication+=1;pass;
                if(indication>=self.__class__.allocationModel):
                    self.entryLevel = min(min(bar20m.open[:-15]), min(bar20m.close[:-15]))-(random.randint(0, 50)/10000);
                    self.positionSize= int(self.__class__.riskMax/self.maxAllocate)+1;

                    if(account[self.symbol].position.shares==0 and len(account[self.symbol].pending.orders)<40):
                        pricedBid = order.algo_buy(self.symbol, algorithm='97a91492-1033-4a96-a546-9bff6df73b08', intent='increase', order_quantity=self.positionSize, price=self.entryLevel, user_key=111, allow_multiple_pending=40)
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
                        
                        ttlPendingCt=ttlShares=ttlNet=0; tickerOrderBox=[];
                        for unit in self.checkPendingBook:
                            ttlPendingCt+=1; ttlShares+=unit[1]; ttlNet+=unit[3];
                            tickerOrderBox.append([unit[0], unit[4]])
                        
                            if(ttlPendingCt>=30):
                                neTprice=ttlNet/ttlShares;
                                for risk in range(7, 19, 1):
                                    chkCancel = order.cancel(order_id=tickerOrderBox[risk][1])
                                ttlPendingCt=0;
                                break
                        pass
                    complexA=0;
                    break
                complexA=0;
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
                    pass
                    
            if(account[self.symbol].position.shares<0):
                if(self.positionSize<0):
                    order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=103)
                    pass
                    
        if event.timer_id=="eod_3":
            if(self.symbol=="SPY"):
                if(account[self.symbol].position.shares>0):
                    order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=account[self.symbol].position.shares, user_key=113)
                    pass
                if(account[self.symbol].position.shares<0):
                    order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=103)
                    pass

        if event.timer_id=="eod_4":
            if(account[self.symbol].position.shares>0):
                if(account[self.symbol].position.shares>4500):
                    positionClose=account[self.symbol].position.shares
                    while(positionClose>0):
                        positionClose-=2000
                        order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=2000, user_key=113)
                    pass    
                else:
                    order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=account[self.symbol].position.shares, user_key=113)
                    pass
            if(account[self.symbol].position.shares<0):
                order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=103)
                pass

        if event.timer_id=="eod_5":
            if(account[self.symbol].position.shares>0):
                order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=account[self.symbol].position.shares, user_key=113)
                pass
            if(account[self.symbol].position.shares<0):
                order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=103)
                pass
        
    def on_ack(self, event, md, order, service, account):
        pass

    def on_reject(self, event, md, order, service, account):
        self.rejectChecker+=1;
        pass

    def on_cancel_reject(self, event, md, order, service, account):
        pass

    @classmethod
    def using_extra_symbols(cls, symbol, md, service, account):
        return False 

    def _on_feedback(self, md, service, account):
        return ''
