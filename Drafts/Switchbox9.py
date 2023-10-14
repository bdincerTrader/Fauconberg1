# Editor    Office of The Underchecker
# Switchbox9   BDincer   5/30/2023 QA-2.0.159
# N-00009   qabdincer/d1c248
# Voodoo=c982d0cd-9be5-4a35-b89f-1f66b2495ec4 Sell Limit ARCA at Script Price
# Voodoo=97a91492-1033-4a96-a546-9bff6df73b08 Buy Limit ARCA at Script Price
# Voodoo=8fa5330d-b32d-4083-86eb-d9a61a637b8b Sell Market GS SOR
# Voodoo=9e6b50d6-dee3-4314-a43b-49e9ae8088b6 Buy Market GS SOR


from cloudquant.interfaces import Strategy
import time, random, os

class Gr8Script126c752dd9b048b1ac18695a43ca97ec(Strategy):
    __script_name__ = 'Switchbox9'
    
    allocationModel=10;testRTE=1.0057;riskMax=1500;rskStatistics=[];
    
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
        self.rejectChecker=0;
        self.intvRate=self.accKey=0;
        self.allocationKey=1;
        self.strategyKey=0;
        self.yesterdayPrice = max(md.stat.prev_close, md.L1.open)
        if(self.yesterdayPrice == 0):
            self.yesterdayPrice = 500;

        self.entryLevel=self.exitPrice=self.positionSize=self.spyQTY=0;
        self.cancelOrderBook=self.checkPendingBook=[];
        self.maxAllocate=int(self.yesterdayPrice*1.10);
        self.delay = service.time_interval(seconds=5);
        self.twentyMin = service.time_interval(minutes=20);
        self.underChecker=30;
        #self.__class__.rskStatistics=[[],[],[],[],[],[],[]];

        if(self.intervalRate[0]==0):
            print("TKR:{}\tPL MODEL: {}.{}\RISKMAX: {}\tRTE: {}\tTRADE DATE: {}".format(self.symbol, self.__class__.allocationModel, self.upperBand, self.__class__.riskMax, self.__class__.testRTE, service.time_to_string(service.system_time)))
        self.intervalRate[0]=0.0001;
        
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=5), repeat_interval=service.time_interval(seconds=5), timer_id="Allocate")
        #service.add_time_trigger(md.market_open_time + service.time_interval(minutes=10), repeat_interval=service.time_interval(minutes=1), timer_id="wrt_file")  
        
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
            reRouteInventory=account[self.symbol].pending.orders;livePending=len(reRouteInventory);
            while(livePending>0):
                livePending-=1; pendingExecution=reRouteInventory[livePending];
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
            turndownSymbol=account[self.symbol].pending.orders; ctTurnover=len(account[self.symbol].pending.orders);
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
        
        #if event.timer_id=="wrt_file": self.rsk_wrt(account, service);return;
        
        if(self.rejectChecker>10): return;
        if(self.strategyKey==1 and len(account[self.symbol].pending.orders)==0 and account[self.symbol].position==0): service.terminate();
        if(self.strategyKey==1 and len(account[self.symbol].pending.orders)==0 and len(account[self.symbol].position.inventory)==0): return;
        if(self.strategyKey==1): case_close_strategy(); pass;
        if(account.realized_mtm_pl+account.unrealized_entry_pl<self.plMaxLoss and self.strategyKey==0): self.strategyKey=1; case_close_strategy(); pass;
        
        if(account[self.symbol].position.entry_price>md.L1.bid):
            allocated=account[self.symbol].position.entry_price; marketBid=md.L1.bid;
            shares=account[self.symbol].position.shares;
            pass
        
        if(account[self.symbol].unrealized_pl.entry_pl>self.plUnrlRTE):
            self.underChecker-=1;
            if(self.underChecker==29): underChecker();pass;
            if(self.underChecker<=0): self.underChecker=30;pass;
        else: self.underChecker=30;

        if(account[self.symbol].unrealized_pl.entry_pl<-self.plUnrlRTE): case_lower();pass;
        
        i=0
        if(event.timestamp<self.illiquid_time):
            chkBar=md.bar.minute_by_index(-5);
            if(len(chkBar.open)>1 and len(chkBar.close)>1 and len(chkBar.bvwap)>1 and len(chkBar.high)>1):
                chkUpperBar=max(max(chkBar.open), max(chkBar.close), max(chkBar.bvwap), max(chkBar.high));
                for unitsCancelled in self.cancelOrderBook:
                    mktPrice=chkUpperBar+(random.randint(0, 50)/10000);
                    if(unitsCancelled[3]==112):
                        upperChecker = order.algo_sell(unitsCancelled[0], algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=-unitsCancelled[1], price=mktPrice, user_key=112, allow_multiple_pending=40)
                        self.cancelOrderBook.pop(i);i+=1;pass;

        self.intervalRate.append(md.L1.percent_change_from_open)
        allocation_key=self._allocation_key(md)
        
        _allocation_Stat=self._clear_book_status(account)
        if(_allocation_Stat==1): turnover();pass;
        if(md.L1.is_halted==True): return;

        if(event.timer_id=="Allocate" and self.allocationKey==1 and event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time): self._check_indicators(event, md, order, service, account); pass;

        if(event.timer_id=="eod_1" or event.timer_id=="eod_2" or event.timer_id=="eod_3" or event.timer_id=="eod_4" or event.timer_id=="eod_5" or event.timer_id=="eod_6"):
            self.eod_functions(event, md, order, service, account)
            pass

    def on_fill(self, event, md, order, service, account):
        if(event.user_tag==111):
            randAdjust=random.randint(0, 50)/10000;
            self.exitPrice = event.price*self.__class__.testRTE-randAdjust;
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
        intervalChange = self.intervalRate[-1]-self.intervalRate[-2];
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
                    pendingExecution=account[self.symbol].pending.orders;
                    ctPnd=len(pendingExecution)
                    if(ctPnd>19):
                        while(ctPnd>0):
                            ctPnd-=1;
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
        

    def on_reject(self, event, md, order, service, account):
        self.rejectChecker+=1;
        pass
        
    def rsk_wrt(self, account, service):
        self.__class__.rskStatistics[0].append(service.time_to_string(service.system_time))
        self.__class__.rskStatistics[1].append(account.unrealized_entry_pl)
        self.__class__.rskStatistics[2].append(account.realized_entry_pl)
        self.__class__.rskStatistics[3].append(account.realized_entry_pl+account.unrealized_entry_pl)
        self.__class__.rskStatistics[4].append(account.capital_used)
        self.__class__.rskStatistics[5].append(account.pending_capital_long)
        self.__class__.rskStatistics[6].append(len(account[self.symbol].pending.orders))
        return 9;
    def on_finish(self, md, order, service, account):
        idx1=self.__class__.rskStatistics[3].index(min(self.__class__.rskStatistics[3]))
        idx2=self.__class__.rskStatistics[3].index(max(self.__class__.rskStatistics[3]))
        idx3=self.__class__.rskStatistics[4].index(max(self.__class__.rskStatistics[4]))
        idx4=self.__class__.rskStatistics[5].index(max(self.__class__.rskStatistics[5]))
        idx5=self.__class__.rskStatistics[6].index(max(self.__class__.rskStatistics[6]))
        x=service.time_to_string(service.system_time)
        filename=self.symbol+'9.txt'
        service.write_file(filename, '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.symbol, service.time_to_string(service.system_time), self.__class__.rskStatistics[0][idx5], self.__class__.rskStatistics[1][idx5], self.__class__.rskStatistics[2][idx5], self.__class__.rskStatistics[4][idx5], self.__class__.rskStatistics[6][idx5], self.__class__.rskStatistics[0][idx4], self.__class__.rskStatistics[1][idx4], self.__class__.rskStatistics[2][idx4], self.__class__.rskStatistics[4][idx4], self.__class__.rskStatistics[5][idx4], self.__class__.rskStatistics[0][idx3], self.__class__.rskStatistics[1][idx3], self.__class__.rskStatistics[2][idx3], self.__class__.rskStatistics[4][idx3], self.__class__.rskStatistics[0][idx2], self.__class__.rskStatistics[1][idx2], self.__class__.rskStatistics[2][idx2], self.__class__.rskStatistics[4][idx2], self.__class__.rskStatistics[0][idx1], self.__class__.rskStatistics[1][idx1], self.__class__.rskStatistics[2][idx1], self.__class__.rskStatistics[4][idx1], account.realized_entry_pl, len(account.completed_orders)), mode="append")
        #file1 = open(filename, "a")  # append mode
        #file1.write(self.symbol, service.time_to_string(service.system_time), self.__class__.rskStatistics[0][idx5], self.__class__.rskStatistics[1][idx5], self.__class__.rskStatistics[2][idx5], self.__class__.rskStatistics[4][idx5], self.__class__.rskStatistics[0][idx4], self.__class__.rskStatistics[1][idx4], self.__class__.rskStatistics[2][idx4], self.__class__.rskStatistics[4][idx4], self.__class__.rskStatistics[0][idx3], self.__class__.rskStatistics[1][idx3], self.__class__.rskStatistics[2][idx3], self.__class__.rskStatistics[4][idx3], self.__class__.rskStatistics[0][idx2], self.__class__.rskStatistics[1][idx2], self.__class__.rskStatistics[2][idx2], self.__class__.rskStatistics[4][idx2], self.__class__.rskStatistics[0][idx1], self.__class__.rskStatistics[1][idx1], self.__class__.rskStatistics[2][idx1], self.__class__.rskStatistics[4][idx1], account.realized_entry_pl, len(account.completed_orders))
        #file1.close()
        return 1;
