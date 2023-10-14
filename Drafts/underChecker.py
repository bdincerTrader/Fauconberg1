# Editor
# https://www.youtube.com/watch?v=AsdG0HyLHP0

from cloudquant.interfaces import Strategy
import time, datetime, random

class Gr8Scripte26cb7cc28424c93ad4a500576ab1541(Strategy):
    __script_name__ = 'underChecker'
    
    tickerItr=[]
    #tickerItr = ['AA','AAL','AAP','BEAM','BG','BAM','AXP']
    #tickerItr = ['EBAY','BEAM','AXP','BG','DIS','BG','DAL','CZR','ALK','ALL','ALLE','ALLY','ALV','AM','AMAT','AMBA','AMC','AMCR','AMD','AME','AMLP','AMP','AMZN','ARCC','ARE','ARKG','ARMK','ARR','ARRY','ARW','ARWR','ASB','ASML','ATI','ATO','ATVI','AU']
    bpRisk=50000; bpMaxLoss=-bpRisk*0.20; plUnrlRTE=bpRisk*0.0010; plUpperBand=bpRisk*.01; plLowerBand=-bpRisk*.01; plBandMult=bpRisk*.01; 
    bookOne=[[],[]];
    bookTwo=[];
    #bookTwo=[[unit, [], [], []] for unit in tickerItr]
    #bookOne.append(bookTwo)
    
    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol == 'GOOG'
        #return symbol in cls.tickerItr
        
    def __init__(self, **params):
        if('riskAllocation' in params):
            print(params['riskAllocation'])
    
    def on_start(self, md, order, service, account):
        #self.__class__.tickerItr.append(self.symbol)
        #self.__class__.bookOne.append([self.symbol, [], [], []])
        self.__class__.tickerItr.append(self.symbol)
        self.__class__.bookTwo.append([self.symbol, [], [], []])
        if(len(self.__class__.tickerItr)==1):
            self.__class__.bookOne.append(self.__class__.bookTwo)
            
        self.dataBook =[[],[],[],[],[],[],[],[],[]]
        self.bb1=[]; self.bb2=[]; self.bb3=[]; self.pendingCycle=[]; self.cxlComplete=[]; self.adjustmentOne=[];
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=10), repeat_interval=service.time_interval(seconds=3), timer_id="Allocate")           
        # ATR over 10 days based on an underlying 250 days of TR (True Range). USE TA Lib# 21 day avg vol.
        self._atr, self._avol, self._beta, self._prev_close = md.stat.atr, md.stat.avol, md.stat.beta, md.stat.prev_close;
        self.quvantity=int(self.__class__.bpRisk/md.stat.prev_close)
        self.liquid_time = md.market_open_time + service.time_interval(minutes=21)
        self.illiquid_time = md.market_close_time - service.time_interval(minutes=30)
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=15), timer_id = "eod_1")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=12), timer_id = "eod_2")
        
    def on_timer(self, event, md, order, service, account):
    
        def procPL_3():
            chkPxA=0;
            
            for quoteUnit in self.adjustmentOne:
                reRack=max(md.L1.ask, md.L1.last)+(random.randint(0, 50)/10000)
                if(quoteUnit[3]==112):
                    newLevel = order.algo_sell(quoteUnit[0], algorithm='5a8a9f9d-22a5-4155-87e7-4ebe8024a97b', intent='decrease', order_quantity=-quoteUnit[1], price=reRack, user_key=112, allow_multiple_pending=40)
                    self.adjustmentOne.pop(chkPxA);
                    chkPxA+=1;
                    pass
            return 1;
                    
        def procPL_1():
            def procPL_2():
                adjustAsk=account[self.symbol].pending.orders; ctPend=len(adjustAsk);
                while(ctPend>0):
                    ctPend-=1; pendingUnit=adjustAsk[ctPend];
                    print("SYSTEM PL procPL_2")
                    print(pendingUnit)
                    if(pendingUnit.shares<0):
                        if(pendingUnit.price<md.L1.bid):
                            discharge = order.cancel(order_id=pendingUnit.order_id);
                            pass;
                        pass;
                return 1;
                
            def procPL_21():
                adjustAsk=account[self.symbol].pending.orders; ctPend=len(adjustAsk);
                while(ctPend>0):
                    ctPend-=1; pendingUnit=adjustAsk[ctPend];
                    print("SYSTEM PL procPL_2")
                    print(pendingUnit)
                    if(pendingUnit.shares<0):
                        discharge = order.cancel(order_id=pendingUnit.order_id);
                        pass;
                return 1;
            if(account[self.symbol].unrealized_pl.entry_pl>self.__class__.plUnrlRTE):
                procPL_2 = procPL_2();pass;
            if(account[self.symbol].unrealized_pl.entry_pl<-self.__class__.plUnrlRTE):
                procPL_21 = procPL_21();pass;
            return 1;
        
        #if(self.symbol=='EBAY'): self.rsk_stat(account);pass;
        
        # PL - SEQUENTIAL POSITIVE ARRAY.
        if event.timer_id=="eod_1":
            if(len(account[self.symbol].pending.orders)>0):
                order.cancel(self.symbol)
                pass
            pass
            
        if event.timer_id=="eod_2":
            if(account[self.symbol].position.shares>0):
                order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=account[self.symbol].position.shares, user_key=113)
                pass
                
        procPL_1 = procPL_1();
        procPL_3 = procPL_3();

        if(event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time):
            idxBar=md.bar.minute_by_index(-9)
            chk_bb1, chk_b1 = 0, idxBar.askvol[-1];
            lockAskVol, lockBidVol = md.L1.daily_askvol, md.L1.daily_bidvol;
            
            if(chk_b1==0): self.bb1.append(0);pass;
            else:
                if(lockAskVol!=0): self.bb1.append(chk_b1/lockAskVol);pass;
                else: self.bb1.append(0);pass;
                pass;
    
            if(len(self.bb1)<6): chk_bb1=self.bb1[-1];pass;
            else: chk_bb1=max(self.bb1[-5:]);pass;
            
            if(chk_b1!=0 and chk_bb1==self.bb1[-1]): chk_bb1=1;pass;
            
            self.bb2.append(lockAskVol); self.bb3.append(lockBidVol);     
            # TERMINAL
            chk_bb0=chk_bb3=chk_bb2=0;
            if(chk_bb1==1):
                if(len(self.bb3)>1):
                    chk_bb3=self.bb3[-1]-self.bb3[-2];
                    if(chk_bb3>0):
                        chk_bb2=self.bb2[-1]-self.bb2[-2];
                        if(chk_bb3>chk_bb2):
                            chk_bb0=1;
                            pass
     
            # PACK
            if(chk_bb0*chk_bb1==1):
                self.dataBook[0].append(idxBar.high[-1]); self.dataBook[1].append(idxBar.low[-1]); self.dataBook[2].append(idxBar.open[-1]); self.dataBook[3].append(idxBar.close[-1]); self.dataBook[4].append(idxBar.bvwap[-1]);
                data_bar=[];
                data_bar.append(md.L1.daily_high); data_bar.append(md.L1.last); data_bar.append(md.L1.bid); data_bar.append(md.L1.ask);
                i, j = 0, 5;
                for item in data_bar:
                    if(type(data_bar[i])==float): self.dataBook[j].append(data_bar[i]);pass;
                    else: self.dataBook.append(self.dataBook[j][-1]);pass;
                    i+=1; j+=1;
                
                # STACK
                if(len(self.dataBook[0])>1):
                    dmp=9; imbl=[];
                    for idx in range(0, 8, 1):
                        if(dmp>6):
                            if(self.dataBook[idx][-1]-self.dataBook[idx][-2]>0): imbl.append([idx, self.dataBook[idx][-1]-self.dataBook[idx][-2]]);pass;
                            else: dmp-=1;pass;
                        else:
                            return
                    if(dmp>6):
                        mkPx=min(min(idxBar.open[:-6]), min(idxBar.close[:-6]), min(idxBar.bvwap[:-6]))-(random.randint(0, 50)/10000)
                        lmtOrd = order.algo_buy(self.symbol, algorithm='8b976c72-20cd-49db-9121-db2e5ace3385', intent='increase', order_quantity=self.quvantity, price=mkPx, user_key=111, allow_multiple_pending=True)
                    else:
                        return
                    pass
                                                                

        ## TODO
        #if(self.symbol=='EBAY'): 
        #    order.algo_buy(self.symbol, algorithm='8b976c72-20cd-49db-9121-db2e5ace3385', intent='increase', order_quantity=100, price=md.L1.bid*.98, user_key=111, allow_multiple_pending=True)
        #    order.cancel(self.symbol)
        
        
        
    def on_cancel(self, event, md, order, service, account):
        if(event.user_tag==112):
            confirmed=[event.symbol, event.shares, event.price, event.user_tag]
            self.adjustmentOne.append(confirmed)
            return
            
    def rsk_stat(self, account):
        longIdx=longUnits=longCash=longUnrl=longPx=longShares=shrtIdx=shrtUnits=shrtCash=shrtUnrl=shrtPx=shrtShares=sUnits=bUnits=0;
        self.pendingCycle=[];
        for inventory in account[self.symbol].position.inventory:
            if(inventory.execution.side==1):
                longIdx=1; longUnits+=1; longCash=account[self.symbol].position.capital_long; longUnrl=account[self.symbol].unrealized_pl.entry_pl; longPx=inventory.mtm_price; longShares+=inventory.execution.shares;pass;
            if(inventory.execution.side==-1):
                shrtIdx=1; shrtUnits+=1; shrtCash=account[self.symbol].position.capital_short; shrtUnrl=account[self.symbol].unrealized_pl.entry_pl; shrtPx=inventory.mtm_price; shrtShares+=inventory.execution.shares;pass;
            
        i=-1;
        for book in self.__class__.bookOne[2]:
            i+=1;
            if(book[0]==self.symbol):
                self.__class__.bookOne[2][i][1]=[longIdx, longUnits, longCash, longUnrl, longPx, longShares, shrtIdx, shrtUnits, shrtCash, shrtUnrl, shrtPx, shrtShares];
                break;
        
        for passive in account[self.symbol].pending.orders:
            if(passive.shares<0):
                sUnits+=1; self.pendingCycle.append([-1, abs(passive.shares), passive.price, passive.order_id, 1]);pass;
            if(passive.shares>0):
                bUnits+=1; self.pendingCycle.append([1, passive.shares, passive.price, passive.order_id, 1]);pass;

        j=-1;
        for book in self.__class__.bookOne[2]:
            j+=1;
            if(book[0]==self.symbol):
                self.__class__.bookOne[2][j][2]=[bUnits, sUnits, self.pendingCycle]
                break;
                
        # current- SPLIT THIS UP.
        self.__class__.bookOne[0]=[account.realized_entry_pl, account.realized_entry_pl_long, account.realized_entry_pl_short, account.capital_used, account.unrealized_entry_pl, account.unrealized_entry_pl_long, account.unrealized_entry_pl_short, account.num_positions_long, account.open_capital_long, account.num_positions_short, account.open_capital_short, account.unrealized_entry_pl_short] 
        self.__class__.bookOne[1]=[account.pending_capital_long, account.pending_capital_short]

        self.cxlComplete=[]
        for cxl in account.canceled_orders:
            self.cxlComplete.append([cxl.symbol, cxl.shares, cxl.price, cxl.user_tag, cxl.order_id])

        k=-1;
        for book in self.__class__.bookOne[2]:
            k+=1;
            if(book[0]==self.symbol):
                self.__class__.bookOne[2][k][3]=[self.cxlComplete]
                break;
                
        #print(account.completed_orders)
        #for dun in account.completed_orders:
        #    print(dun)
        #pass
        ## TODO
    
    def on_fill(self, event, md, order, service, account):
        if(event.intent in ["increase", "init"] and service.instruction_id == event.instruction_id):  
            if(event.user_tag==111):
                exitPrice=event.price*1.0026;
                offerInventory = order.algo_sell(event.symbol, algorithm='5a8a9f9d-22a5-4155-87e7-4ebe8024a97b', intent='decrease', order_quantity=event.shares, price=exitPrice, user_key=112, allow_multiple_pending=True)
                pass
            pass
