# 269564-replaced Gr8Scriptbc647d165f044ffe89a4af2f179b3494 with 'self.__class__.'
# CHG 1: switched order from SOR to ARCA 'c982d0cd-9be5-4a35-b89f-1f66b2495ec4' 
# FOR LIMIT SELL ORDERS: line 269, 310 
# FOR LIMIT BUY ORDERS: line 563
# CHG 2: added def case_lower() fn in case position moves against the book.
# CHG 3: adjusted pricing in forLOOP unitsCancelled in self.cancelOrderBook.
from cloudquant.interfaces import Strategy
import time, random

class Gr8Scriptf6fd3016e01f42ca9b743a1888644643(Strategy):
    __script_name__ = 'switchBox4-ARCA'
    
    allocationModel=10;testRTE=1.0009;riskMax=10000;lvlTwo=0.99878;maxLoss=1.02;clockOne=4;clockTwo=31;
    
    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol == 'SWN'
        
    def __init__(self, **params):
        if('riskAllocation' in params):
            print(params['riskAllocation'])
            self.__class__.riskMax=params['riskAllocation'];
        if('allocationMode' in params):
            print(params['allocationMode'])
            self.__class__.allocationModel=params['allocationMode'];
            self.__class__.testRTE=params['spread'];
            self.__class__.lvlTwo=params['bidSpread'];
            self.__class__.maxLoss=params['stopLoss'];
            self.__class__.clockOne=params['freqOne'];
            self.__class__.clockTwo=params['freqTwo'];
    
    def on_start(self, md, order, service, account):                      
        self.yesterdayPrice = max(md.stat.prev_close, md.L1.open)
        if(self.yesterdayPrice == 0): self.yesterdayPrice = 500; pass;
       
        self.maxAllocate=int(self.yesterdayPrice*1.10);
        # self.delay = service.time_interval(seconds=5);
        self.riskModel = self.__class__.allocationModel;
        self.mktSpread = self.__class__.testRTE;
        self.mktAdjust = self.mktSpread * self.__class__.lvlTwo;
        self.posAdjust = self.__class__.lvlTwo;
        self.lossTolerance = self.__class__.maxLoss;
        self.decreaseRisk = [];
        self.timerOne=int(self.__class__.clockOne);
        self.timerTwo=int(self.__class__.clockTwo);
        self.status=0;
        print("TKR:{}\tMODEL: {}\t MKT SPR {}.{} \t TIMERS: {}|{}\tTRADE DATE: {}".format(self.symbol, self.riskModel, self.mktSpread, self.mktAdjust, self.timerOne, self.timerTwo, service.time_to_string(service.system_time)))
        
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=5), repeat_interval=service.time_interval(seconds=self.timerOne), timer_id="Allocate")
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=5), repeat_interval=service.time_interval(seconds=self.timerTwo), timer_id="Release")
        
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=10), timer_id = "eod_1")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=7), timer_id = "eod_2")
        
        self.liquid_time = md.market_open_time + service.time_interval(minutes=15)
        self.illiquid_time = md.market_close_time - service.time_interval(minutes=11)

    
    def on_timer(self, event, md, order, service, account):
        
        def eject():
            #placehodler for other handlers...
            order.cancel(self.symbol);
            return 1;
        

        if(event.timer_id=="Release"):
            
            if(self.status==0):
                chkItem = len(account[self.symbol].position.inventory)
                while(chkItem>0):
                    chkItem-=1;
                    if(account[self.symbol].position.capital_long>0):
                        pxUnit=account[self.symbol].position.entry_price;
                        # szUnit=account[self.symbol].position.shares;
                        if(pxUnit*self.posAdjust>md.L1.bid):
                            positive = eject();
                            pass;
                        elif(pxUnit*self.lossTolerance<md.L1.bid): 
                            negative = eject();
                            pass;
                        elif(pxUnit*self.lossTolerance<md.L1.last):
                            negative = eject();
                            pass;
                            
            self.status=0;
            if(len(self.decreaseRisk)>0):
                self.status=1;
                for allocation in self.decreaseRisk:
                    if(account[self.symbol].position.capital_long>0):
                        if((allocation[2]*self.lossTolerance)<md.L1.bid):
                            negative = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity= allocation[1], price=md.L1.bid*self.mktAdjust, user_key=112, allow_multiple_pending=40);
                            pass;
                        elif((allocation[2]*self.mktAdjust)>md.L1.bid):
                            positive = order.algo_sell(self.symbol, algorithm='f8328375-d95c-4c10-aa7e-0c7fecf13336', intent='decrease', order_quantity=allocation[1], price=md.L1.bid, user_key=112, allow_multiple_pending=40);
                            pass;
                        elif((allocation[2]*self.mktAdjust)>md.L1.last):
                            positive = order.algo_sell(self.symbol, algorithm='f8328375-d95c-4c10-aa7e-0c7fecf13336', intent='decrease', order_quantity=allocation[1], price=md.L1.last, user_key=112, allow_multiple_pending=40);
                            pass;
                        else:
                            neutral = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity= allocation[1], price=md.L1.ask, user_key=112, allow_multiple_pending=40);
                            pass;
                self.decreaseRisk=[];
                pass;
                
        if(event.timer_id=="Allocate" and event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time): chkOrder = self._check_indicators(event, md, order, service, account); return chkOrder;

        if(event.timer_id=="eod_1" or event.timer_id=="eod_2"): eodChk = self.eod_functions(event, md, order, service, account); return eodChk;

    def on_fill(self, event, md, order, service, account):
        if(event.user_tag==111):
            release = event.price*self.mktSpread;
            pxOne = int((release + (random.randint(21, 66)/10000)) * 10000 + 0.001) / 10000.0;
            if(event.intent in ["increase", "init"] and service.instruction_id == event.instruction_id):
                offerInventory = order.algo_sell(event.symbol, algorithm='f8328375-d95c-4c10-aa7e-0c7fecf13336', intent='decrease', order_quantity= event.shares, price=pxOne, user_key=112, allow_multiple_pending=40)
                return offerInventory;
            else: return 0;
        else: return 0;

    def on_cancel(self, event, md, order, service, account):
        if(event.user_tag==112 and event.timestamp<self.illiquid_time):
            self.decreaseRisk.append([event.symbol, abs(event.shares), event.price]);
            pass;

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
            if(indication>0):
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
                if(indication>=self.riskModel):
                    bidPx = min(min(bar20m.open[:-15]), min(bar20m.close[:-15]))-(random.randint(0, 50)/1000);
                    bidQty = int(self.__class__.riskMax/self.maxAllocate)+1;

                    if(account[self.symbol].position.shares==0 and len(account[self.symbol].pending.orders)<40):
                        riskUnit = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=bidQty, price=bidPx, user_key=111, allow_multiple_pending=40)
                        return riskUnit;
                    pass;
                pass;
            pass;
        return 1;

    def eod_functions(self, event, md, order, service, account):
    
        if(event.timer_id=="eod_1"):
            if(len(account[self.symbol].pending.orders)>0):
                order.cancel(self.symbol)
                return 1;
                
        elif(event.timer_id=="eod_2"):
            if(account[self.symbol].position.shares>0):
                closeLong = order.algo_sell(self.symbol, algorithm='09528d6b-7d4f-4cc2-8611-8bbecb33785c', intent='exit', user_key=113)
                return closeLong;
                    
            if(account[self.symbol].position.shares<0):
                closeShort = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=103)
                return closeShort;
        return 0;     
