# Editor    Office of The Exchequer
# Fauconberg   BDincer   5/24/2023 5:58:59 PM   QA-2.0.158
# N-00068   qabdincer/d1c248
# Voodoo=c982d0cd-9be5-4a35-b89f-1f66b2495ec4 Sell Limit ARCA at Script Price
# Voodoo=8fa5330d-b32d-4083-86eb-d9a61a637b8b Sell Market GS SOR
# Voodoo=97a91492-1033-4a96-a546-9bff6df73b08 Buy Limit ARCA at Script Price
# Voodoo=5a8a9f9d-22a5-4155-87e7-4ebe8024a97b Sell Limit GS SOR at Script Price
# Voodoo=8b976c72-20cd-49db-9121-db2e5ace3385 Buy Limit GS SOR at Script Price
from cloudquant.interfaces import Strategy
import time, datetime, random

class Gr8Scriptcffda23257ae4d54a108e8990036b304(Strategy):
    __script_name__ = 'Fauconberg'
    
    bpRisk=20000; orderType=0; cycl=4; askRTE=1.0021; pxChk=1.21; plSpr=1.0012; bpMaxLoss=-bpRisk*0.20; plUnrlRTE=bpRisk*0.0010; lclTimeFreq=3; plUpperBand=bpRisk*.01; plLowerBand=-bpRisk*.01; plBandMult=bpRisk*.01; 

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol == 'MSTR'
        
    def __init__(self, **params):
        if('riskAllocation' in params):
            self.__class__.bpRisk=params['riskAllocation'];
            self.__class__.bpMaxLoss=-self.__class__.bpRisk*0.20;
            self.__class__.plUnrlRTE=self.__class__.bpRisk*params['plRiskBp'];
            self.__class__.lclTimeFreq=params['timeFreq'];
            self.__class__.plUpperBand=self.__class__.bpRisk*.01;
            self.__class__.plLowerBand=-self.__class__.bpRisk*.01;
            self.__class__.plBandMult=self.__class__.bpRisk*.01;
            print(params['riskAllocation'])
        if('cycl' in params):
            self.__class__.cycl=params['cycl'];
            print(params['cycl'])
        if('askRTE' in params):
            self.__class__.askRTE=params['askRTE'];
            print(params['askRTE'])
        if('plRoute' in params):    
            self.__class__.plSpr=params['plRoute'];
            print(params['plRoute'])
        if('mkSpread' in params):    
            self.__class__.pxChk=params['mkSpread'];
            self.__class__.orderType=params['orderType'];
            print(params['mkSpread'])
    
    def on_start(self, md, order, service, account):
        self.dataBook =[[],[],[],[],[],[],[],[],[]];
        self.bb1=[]; self.bb2=[]; self.bb3=[]; self.pendingCycle=[]; self.cxlComplete=[]; self.adjustmentOne=[]; self.venue=1; self.procPL2=0; self.procPL21=0;
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=10), repeat_interval=service.time_interval(seconds=self.__class__.lclTimeFreq), timer_id="Allocate")
        self.mktSpread=self.__class__.plSpr;
        self.mkOffer=self.__class__.pxChk;
        self.unrlRoll=self.__class__.plUnrlRTE;
        self.orderECN=self.__class__.orderType;
        # ATR over 10 days based on an underlying 250 days of TR (True Range). USE TA Lib# 21 day avg vol.
        self._atr, self._avol, self._beta, self._prev_close = md.stat.atr, md.stat.avol, md.stat.beta, md.stat.prev_close;
        self.quvantity=int(self.__class__.bpRisk/md.stat.prev_close);
        self.riskAllowance=int(self.__class__.bpRisk);
        self.liquid_time = md.market_open_time + service.time_interval(minutes=21)
        self.illiquid_time = md.market_close_time - service.time_interval(minutes=45)
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=15), timer_id = "eod_1")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=12), timer_id = "eod_2")
        
    def on_timer(self, event, md, order, service, account):
        
        def procPL_3(sprPam):
            chkPxA=0; Bpx=md.L1.bid; Apx=md.L1.ask; Lpx=md.L1.last;
            if(sprPam==3): qbA=Apx-((Apx-Bpx)/sprPam); reRack=max(Lpx, qbA)+self.mkOffer;pass;
            elif(sprPam==4): qbA=Apx-((Apx-Bpx)/sprPam); reRack=max(Lpx, qbA)+self.mkOffer;pass;
            reRack=int(reRack*10000 + 0.001) / 10000.0;
            dupeChk=int((random.randint(1, 50)/1000) * 1000 + 0.001) / 1000.0;
            for quoteUnit in self.adjustmentOne:
                self.venue+=1; reRack+=dupeChk;
                if(quoteUnit[3]==112 and self.venue%2==1):
                    newLevel = order.algo_sell(quoteUnit[0], algorithm='09528d6b-7d4f-4cc2-8611-8bbecb33785c', intent='decrease', order_quantity=-quoteUnit[1], price=reRack, user_key=112, allow_multiple_pending=40)
                    self.adjustmentOne.pop(chkPxA); chkPxA+=1;pass;
                elif(quoteUnit[3]==112 and self.venue%2==0):
                    newLevel = order.algo_sell(quoteUnit[0], algorithm='f8328375-d95c-4c10-aa7e-0c7fecf13336', intent='decrease', order_quantity=-quoteUnit[1], price=reRack, user_key=112, allow_multiple_pending=40)
                    self.adjustmentOne.pop(chkPxA); chkPxA+=1;pass;
            self.procPL21=0; self.procPL2=0;
            return 1;
                    
        def procPL_1():
            def procPL_2():
                adjustAsk=account[self.symbol].pending.orders; ctPend=len(adjustAsk);
                while(ctPend>0):
                    ctPend-=1; pendingUnit=adjustAsk[ctPend];
                    if(pendingUnit.shares<0):
                        discharge = order.cancel(order_id=pendingUnit.order_id);
                        pass;
                return 4;
                
            def procPL_21():
                adjustAsk=account[self.symbol].pending.orders; ctPend=len(adjustAsk);
                while(ctPend>0):
                    ctPend-=1; pendingUnit=adjustAsk[ctPend];
                    if(pendingUnit.shares<0):
                        discharge = order.cancel(order_id=pendingUnit.order_id);
                        pass;
                return 3;
            
            if(account[self.symbol].position.mtm_price*self.mktSpread<md.L1.bid): self.procPL2 = procPL_2();pass;
            elif(account[self.symbol].position.mtm_price*self.mktSpread<md.L1.last): self.procPL2 = procPL_2();pass;
            elif(account[self.symbol].position.mtm_price>md.L1.bid*self.mktSpread): self.procPL21 = procPL_21();pass;
            elif(account[self.symbol].unrealized_pl.entry_pl>self.unrlRoll): self.procPL2 = procPL_2();pass;
            elif(account[self.symbol].unrealized_pl.entry_pl<-self.unrlRoll): self.procPL21 = procPL_21();pass;
            return 1;
        
        if event.timer_id=="eod_1":
            if(len(account[self.symbol].pending.orders)>0):
                order.cancel(self.symbol);pass;
            else: return 1;
            
        if event.timer_id=="eod_2":
            if(account[self.symbol].position.shares>0):
                closeInventory = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=account[self.symbol].position.shares, user_key=113, allow_multiple_pending=40)
                return closeInventory;
            else: return 1;
                
        procPL_1 = procPL_1();
        if(self.procPL21==3): procPL_3(3);pass;
        elif(self.procPL2==4): procPL_3(4);pass;

        if(event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time):
            idxBar=md.bar.minute_by_index(-9)
            if(len(idxBar.askvol)>1):
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
                else: return 0;

                if(chk_bb0*chk_bb1==1):
                    if(len(idxBar.high)>1 and len(idxBar.low)>1 and len(idxBar.open)>1 and len(idxBar.close)>1 and len(idxBar.bvwap)>1):
                        self.dataBook[0].append(idxBar.high[-1]); self.dataBook[1].append(idxBar.low[-1]); self.dataBook[2].append(idxBar.open[-1]); self.dataBook[3].append(idxBar.close[-1]); self.dataBook[4].append(idxBar.bvwap[-1]);
                        data_bar=[];
                        data_bar.append(md.L1.daily_high); data_bar.append(md.L1.last); data_bar.append(md.L1.bid); data_bar.append(md.L1.ask);
                        i, j = 0, 5;
                        for item in data_bar:
                            if(type(data_bar[i])==float): self.dataBook[j].append(data_bar[i]);pass;
                            else: self.dataBook.append(self.dataBook[j][-1]);pass;
                            i+=1; j+=1;

                        if(len(self.dataBook[0])>1):
                            dmp=9; imbl=[];
                            for idx in range(0, 8, 1):
                                if(dmp>self.__class__.cycl):
                                    if(self.dataBook[idx][-1]-self.dataBook[idx][-2]>0): imbl.append([idx, self.dataBook[idx][-1]-self.dataBook[idx][-2]]);pass;
                                    else: dmp-=1;pass;
                                else:
                                    return 0;
                            if(dmp>self.__class__.cycl and abs(account[self.symbol].position.capital_long)<self.riskAllowance*10 and len(account[self.symbol].pending.orders)<10):
                                if(len(account[self.symbol].pending.orders)>6):
                                    self.orderECN=1;
                                    pass;
                                    
                                if(self.orderECN==1 and abs(account[self.symbol].position.capital_long)<self.riskAllowance*5):
                                    self.orderECN=0;
                                    zeroPx = min(md.L1.bid, md.L1.last, md.L1.ask) + 0.01;
                                    bidQty = int(self.quvantity)+1;
                                    riskUnitZero = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=bidQty+1, price=zeroPx, user_key=111, allow_multiple_pending=40);
                                    # onePx = md.L1.ask + 0.01;
                                    # riskUnitOnePx = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=bidQty, price=onePx, user_key=111, allow_multiple_pending=40);
                                    riskUnitOne = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=self.quvantity, user_key=111, allow_multiple_pending=40);
                                    return riskUnitOne;
                                    
                                else:
                                    mkPx=min(min(idxBar.open[:-6]), min(idxBar.close[:-6]), min(idxBar.bvwap[:-6]))-(random.randint(0, 50)/10000);
                                    mkPx=int((mkPx*10000) + 0.001) / 10000.0;
                                    lmtOrd = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.quvantity, price=mkPx, user_key=111, allow_multiple_pending=40);
                                    return lmtOrd;
                            else: return 0;
                        else: return 0;
                    else: return 0;
                else: return 0;
            else: return 0;
        else: return 0;
    def on_cancel(self, event, md, order, service, account):
        if(event.user_tag==112):
            confirmed=[event.symbol, event.shares, event.price, event.user_tag];
            self.adjustmentOne.append(confirmed);
            return confirmed;
        return 8;
    def on_fill(self, event, md, order, service, account):
        if(event.intent in ["increase", "init"] and service.instruction_id == event.instruction_id):
            if(event.user_tag==111):
                exitPrice=event.price*self.__class__.askRTE;
                offerInventory = order.algo_sell(event.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=event.shares, price=exitPrice, user_key=112, allow_multiple_pending=40)
                return offerInventory;
            else: return 1;
        else: return 0;
