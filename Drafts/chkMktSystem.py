from cloudquant.interfaces import Strategy
import time, datetime, random

class Gr8Script59621f4ac9b34d73a39bcf475fc35020(Strategy):
    __script_name__ = 'FauconbergTwoCopy'
    
    tickerItrB = ['ADBE','ASML','AVGO','AZO','BIO','BKNG','BLK','GS','MS','COST','CMG','DDS','DECK','ELV','EQIX','FCNCA','FDS','FICO','FNGU','GWW','HUBS','HUM','IDXX','IIVI','INTU','KLAC','LRCX','MDB','MDGL','MELI','MPWR','MSCI','MSTR','MTD','NFLX','NOW','NVDA','ORLY','REGN','SAIA','SEDG','SMCI','SNPS','SOXX','SWAV','TDG','TMO','TSLA','ULTA','UNH','URI','SPY','QQQ'];
    
    bpRisk=5000; orderType=0; cycl=6; askRTE=1.0012; pxChk=1.21; plSpr=1.0012; bpMaxLoss=-bpRisk*0.20; plUnrlRTE=bpRisk*0.0010; lclTimeFreq=3; plUpperBand=bpRisk*0.01; plLowerBand=-bpRisk*0.01; plBandMult=bpRisk*0.01;
    
    # ARGX, NRGU, REGN, MSTR, CACC, LRCX, CACC, CELH, MPWR, MELI, CMG, CAT, ALGN, NVR, EQIX, AVGO, CTAS, DECK, HUBS, KRTX, TEAM, GNRC, GPI, COIN, URI, TDG, POOL, MKL, PEN, BLK, LLY, GWW, SNPS, FCNCA, FNGU, META, AZO, ADBE, ULTA, NOW 
     
    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        # return md.stat.prev_close>50.00 and md.stat.atr>5;
        # return md.stat.prev_close>50.00 and md.stat.atr>5 and md.stat.beta>0.66
        return symbol in Gr8Script59621f4ac9b34d73a39bcf475fc35020.tickerItrB;
        
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
        self.allocator=0;
        self.allocated=[0];
        self._atr, self._avol, self._beta, self._prev_close = md.stat.atr, md.stat.avol, md.stat.beta, md.stat.prev_close;

        print(self.symbol, service.time_to_string(service.system_time, '%Y-%m-%d'));
        self.filenameB=self.symbol+service.time_to_string(service.system_time, '%Y-%m-%d')+".txt"
        print(self.filenameB);
        self.qqqPrior=(md['QQQ'].stat.prev_close);
        self.spyPrior=(md['SPY'].stat.prev_close);
        self.qqqBid=(md['QQQ'].L1.bid);
        self.spyBid=(md['SPY'].L1.bid);
        
        # PRIOR SPY
        self.spBars =(md['SPY'].bar.daily_by_index(start=-40));
        self.spA=(self.spBars.close[-5]-self.spyPrior)/self.spBars.close[-5];
        self.spB=(self.spBars.close[-10]-self.spyPrior)/self.spBars.close[-10];
        self.spC=(self.spBars.close[-20]-self.spyPrior)/self.spBars.close[-20];
        self.spD=(self.spBars.close[-30]-self.spyPrior)/self.spBars.close[-30];
        print('SPY\t BENCH1')
        print(self.spA, self.spB, self.spC, self.spD)
        
        # PRIOR QQQ
        self.qqBars =(md['QQQ'].bar.daily_by_index(start=-40));
        self.qqA=(self.qqBars.close[-5]-self.qqqPrior)/self.qqBars.close[-5];
        self.qqB=(self.qqBars.close[-10]-self.qqqPrior)/self.qqBars.close[-10];
        self.qqC=(self.qqBars.close[-20]-self.qqqPrior)/self.qqBars.close[-20];
        self.qqD=(self.qqBars.close[-30]-self.qqqPrior)/self.qqBars.close[-30];
        print('QQQ\t BENCH2')
        print(self.qqA, self.qqB, self.qqC, self.qqD)
        
        # PRIOR TKR
        self.ctrlBars=md.bar.daily_by_index(start=-40);
        self.tkrA=(self.ctrlBars.close[-5]-self._prev_close)/self.ctrlBars.close[-5];
        self.tkrB=(self.ctrlBars.close[-10]-self._prev_close)/self.ctrlBars.close[-10];
        self.tkrC=(self.ctrlBars.close[-20]-self._prev_close)/self.ctrlBars.close[-20];
        self.tkrD=(self.ctrlBars.close[-30]-self._prev_close)/self.ctrlBars.close[-30];
        print(self.symbol, self._beta);
        print(self.tkrA, self.tkrB, self.tkrC, self.tkrD)
        
        if(self.tkrA<self.qqA and self.tkrD<self.spA):
            print('check higher')
        if(self.tkrA>self.qqA and self.tkrD>self.spA):
            print('check lower')
        
        
        self.timerA=int(self.__class__.lclTimeFreq);
        self.timerB=int(self.timerA+20);
        
        self.mktSpread=self.__class__.plSpr;
        self.mkOffer=self.__class__.pxChk;
        self.unrlRoll=self.__class__.plUnrlRTE;
        self.orderECN=self.__class__.orderType;
        self.chkMktSystem=0;
        self.bidPx, self.askPx, self.lstPx = md.L1.bid, md.L1.ask, md.L1.last;
        self.trajectoryBook=self.trajectoryBid=self.trajectoryAsk=self.trajectoryLast=self.trajectorySpread=[];
        self.chkTrajectoryQ=self.chkTrajectoryS=[0.00];
        self.tkrRate=[0.00];
        # ATR over 10 days based on an underlying 250 days of TR (True Range). USE TA Lib# 21 day avg vol.
        
        self.quvantity=int(self.__class__.bpRisk/md.stat.prev_close);
        self.riskAllowance=int(self.__class__.bpRisk);
        self.liquid_time = md.market_open_time + service.time_interval(minutes=21)
        self.illiquid_time = md.market_close_time - service.time_interval(minutes=45)
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=15), timer_id = "eod_1")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=12), timer_id = "eod_2")
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=10), repeat_interval=service.time_interval(seconds=self.__class__.lclTimeFreq), timer_id="Allocate")
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=10), repeat_interval=service.time_interval(seconds=self.timerB), timer_id="Review")
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=10), repeat_interval=service.time_interval(minutes=10), timer_id="Write")
        #400
    def on_timer(self, event, md, order, service, account):
        if(event.timer_id=="Write"):
            #print((md['QQQ'].L1.bid), (md['SPY'].L1.bid), md.L1.bid,  md.L1.ask,  md.L1.last, self.tkrRate[-1], self.chkTrajectoryQ[-1], self.chkTrajectoryQ[-1], self.chkTrajectoryS[-1], self.chkTrajectoryS[-1], 0, 0, self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1], self.allocator, self.chkMktSystem)
            #service.write_file(self.filenameB,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format('Write', self.qqqBid, self.spyBid, md.L1.bid,  md.L1.ask,  md.L1.last, self.tkrRate[-1], self.chkTrajectoryQ[-1], self.chkTrajectoryQ[-1], self.chkTrajectoryS[-1], self.chkTrajectoryS[-1], 0, 0, self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1], self.allocator, self.chkMktSystem));
            return;

        if(event.timer_id=="Review"):
            checkPriceA=max(md.L1.bid, md.L1.ask, md.L1.last); 
            checkPriceB=min(md.L1.bid, md.L1.ask, md.L1.last);
            checkMid=(checkPriceA+checkPriceB)/2;
            self.qqqBid=(md['QQQ'].L1.bid);
            self.spyBid=(md['SPY'].L1.bid);
            
            chkAsk=md.L1.ask;
            chkBid=md.L1.bid;
            chkLast=md.L1.last;
            
            if(chkLast*1.1<checkPriceA or chkBid*1.1<checkPriceA or chkAsk*1.1<checkPriceA):
                #service.write_file(self.filenameB,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format('chkDataFeed1',self.qqqBid, self.spyBid, chkBid, chkAsk, chkLast, self.tkrRate[-1], self.chkTrajectoryQ[-1], self.chkTrajectoryQ[-1], self.chkTrajectoryS[-1], self.chkTrajectoryS[-1], 0, 0, self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1], self.allocator, self.chkMktSystem));
                self.chkMktSystem=0;
                return 0;
            elif(chkLast*0.9>checkPriceB or chkBid*0.9>checkPriceB  or chkAsk*0.9>checkPriceB):
                #service.write_file(self.filenameB,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format('chkDataFeed2',self.qqqBid, self.spyBid, chkBid, chkAsk, chkLast, self.tkrRate[-1], self.chkTrajectoryQ[-1], self.chkTrajectoryQ[-1], self.chkTrajectoryS[-1], self.chkTrajectoryS[-1], 0, 0, self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1], self.allocator, self.chkMktSystem));
                self.chkMktSystem=0;
                return 0;
            else:
                self.chkMktSystem=1;
                tgtPX=((chkBid+chkAsk+chkLast)/3)
                baSpr=(chkAsk-chkBid); 
                self.trajectoryBook.append(tgtPX);
                self.trajectoryBid.append(chkBid);
                self.trajectoryAsk.append(chkAsk); 
                self.trajectorySpread.append(baSpr);
                tgtPX_RATE = ((tgtPX-self._prev_close)/self._prev_close);
                self.tkrRate.append(tgtPX_RATE);
                pass;
                
            if(self.chkMktSystem!=0 and len(self.trajectoryBook)>2):
                self.chkMktSystem=1;
                tkrRate=self.tkrRate[-1];
                qqTrajectory=( ( (md['QQQ'].L1.bid) - self.qqqPrior) /self.qqqPrior );
                spTrajectory=( ( (md['SPY'].L1.bid) - self.spyPrior) /self.spyPrior );
                self.chkTrajectoryQ.append(qqTrajectory);
                self.chkTrajectoryS.append(spTrajectory);
                chkQQQspread=tkrRate-qqTrajectory;
                chkSPYspread=tkrRate-spTrajectory;

                if(chkQQQspread>0.01):
                    if(self.tkrRate[-1]<self.chkTrajectoryQ[-1]):
                        self.allocator-=1;
                        #service.write_file(self.filenameB,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format('chkQQ[-][+0.01]',self.qqqBid, self.spyBid, chkBid, chkAsk, chkLast, self.tkrRate[-1], self.chkTrajectoryQ[-1], qqTrajectory, self.chkTrajectoryS[-1],spTrajectory, chkQQQspread, chkSPYspread, self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1],self.allocator, self.chkMktSystem));
                        pass;
                    if(self.tkrRate[-1]>self.chkTrajectoryQ[-1]):
                        self.allocator+=1;
                        #service.write_file(self.filenameB,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format('chkQQ[+][+0.01]',self.qqqBid, self.spyBid, chkBid, chkAsk, chkLast, self.tkrRate[-1], self.chkTrajectoryQ[-1], qqTrajectory, self.chkTrajectoryS[-1],spTrajectory, chkQQQspread, chkSPYspread, self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1],self.allocator, self.chkMktSystem));
                        pass;
                    pass;
                if(chkSPYspread>0.01):
                    if(self.tkrRate[-1]<self.chkTrajectoryS[-1]):
                        self.allocator-=1;
                        #service.write_file(self.filenameB,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format('chkSP[-][+0.01]',self.qqqBid, self.spyBid, chkBid, chkAsk, chkLast, self.tkrRate[-1], self.chkTrajectoryQ[-1], qqTrajectory, self.chkTrajectoryS[-1],spTrajectory, chkQQQspread, chkSPYspread, self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1],self.allocator, self.chkMktSystem));
                        pass;
                    if(self.tkrRate[-1]>self.chkTrajectoryS[-1]):
                        self.allocator+=1;
                        #service.write_file(self.filenameB,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format('chkSP[+][+0.01]',self.qqqBid, self.spyBid, chkBid, chkAsk, chkLast, self.tkrRate[-1], self.chkTrajectoryQ[-1], qqTrajectory, self.chkTrajectoryS[-1],spTrajectory, chkQQQspread, chkSPYspread, self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1],self.allocator, self.chkMktSystem));
                        pass;
                    pass;
                if(chkQQQspread<-0.01):
                    if(self.tkrRate[-1]<self.chkTrajectoryQ[-1]):
                        self.allocator-=1;
                        #service.write_file(self.filenameB,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format('chkQQ[-][-0.01]',self.qqqBid, self.spyBid, chkBid, chkAsk, chkLast, self.tkrRate[-1], self.chkTrajectoryQ[-1], qqTrajectory, self.chkTrajectoryS[-1],spTrajectory, chkQQQspread, chkSPYspread, self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1],self.allocator, self.chkMktSystem));                   
                        pass;
                    if(self.tkrRate[-1]>self.chkTrajectoryQ[-1]):
                        self.allocator+=1;
                        #service.write_file(self.filenameB,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format('chkQQ[+][-0.01]',self.qqqBid, self.spyBid, chkBid, chkAsk, chkLast, self.tkrRate[-1], self.chkTrajectoryQ[-1], qqTrajectory, self.chkTrajectoryS[-1],spTrajectory, chkQQQspread, chkSPYspread, self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1],self.allocator, self.chkMktSystem));                   
                        pass;
                    pass;
                if(chkSPYspread<-0.01):
                    if(self.tkrRate[-1]<self.chkTrajectoryS[-1]):
                        self.allocator-=1;
                        #service.write_file(self.filenameB,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format('chkSP[-][-0.01]',self.qqqBid, self.spyBid, chkBid, chkAsk, chkLast, self.tkrRate[-1], self.chkTrajectoryQ[-1], qqTrajectory, self.chkTrajectoryS[-1],spTrajectory, chkQQQspread, chkSPYspread, self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1],self.allocator, self.chkMktSystem));                   
                        pass;
                    if(self.tkrRate[-1]>self.chkTrajectoryS[-1]):
                        self.allocator+=1;
                        #service.write_file(self.filenameB,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format('chkSP[+][-0.01]',self.qqqBid, self.spyBid, chkBid, chkAsk, chkLast, self.tkrRate[-1], self.chkTrajectoryQ[-1], qqTrajectory, self.chkTrajectoryS[-1],spTrajectory, chkQQQspread, chkSPYspread, self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1],self.allocator, self.chkMktSystem));                   
                        pass;
                    pass;
                self.allocated.append(self.allocator);
                pass;
            return 1;
        
        def procPL_3(sprPam):
            chkPxA=0; Bpx=md.L1.bid; Apx=md.L1.ask; Lpx=md.L1.last;
            if(sprPam==3): qbA=Apx-((Apx-Bpx)/sprPam); reRack=max(Lpx, qbA)+self.mkOffer;pass;
            elif(sprPam==4): qbA=Apx-((Apx-Bpx)/sprPam); reRack=max(Lpx, qbA)+self.mkOffer;pass;
            reRack=int(reRack*10000 + 0.001) / 10000.0;
            dupeChk=int((random.randint(1, 50)/1000) * 1000 + 0.001) / 1000.0;
            for quoteUnit in self.adjustmentOne:
                self.venue+=1; reRack+=dupeChk;
                if(quoteUnit[3]==112 and self.venue%2==1 and account[self.symbol].position.shares>0):
                    newLevel = order.algo_sell(quoteUnit[0], algorithm='09528d6b-7d4f-4cc2-8611-8bbecb33785c', intent='decrease', order_quantity=-quoteUnit[1], price=reRack, user_key=112, allow_multiple_pending=40)
                    self.adjustmentOne.pop(chkPxA); chkPxA+=1;pass;
                elif(quoteUnit[3]==112 and self.venue%2==0 and account[self.symbol].position.shares>0):
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

        # data quality check.
        
        if(self.chkMktSystem==1 and len(account[self.symbol].pending.orders)>1):
            if(self.allocated[-1]<self.allocated[-2]):
                ### zeroPx Loop
                ## cancel bids
                self.orderECN=0;
                print('lower', self.allocated);
                print('ask', self.trajectoryAsk);
                print('bid', self.trajectoryBid);
                adjustBid=account[self.symbol].pending.orders; 
                ctPend=len(adjustBid);
                while(ctPend>0):
                    ctPend-=1;
                    pendingBid=adjustBid[ctPend];
                    if(pendingBid.shares>0):
                        discharge = order.cancel(order_id=pendingBid.order_id);
                        pass;
            
            if(len(self.allocated)>3 and self.allocated[-1] < self.allocated[-2] and account[self.symbol].position.capital_long>0):
                self.chkMktSystem==2;
                pngSOR = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=max(int(account[self.symbol].position.shares/2),1), user_key=2020, allow_multiple_pending=40);
                return;
            
            if(len(self.allocated)>2 and self.allocated[-1]<0 and self.allocated[-2]>0 and account[self.symbol].position.capital_long>0):
                self.chkMktSystem==2;
                pngSOR = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='exit', user_key=2020, allow_multiple_pending=40);
                return;
                
            procPL_1 = procPL_1();
            if(self.procPL21==3): procPL_3(3);pass;
            elif(self.procPL2==4): procPL_3(4);pass;
            self.orderECN=0;
            pass;
            
        if(account[self.symbol].position.capital_long==0 and self.chkMktSystem==2):
            # cancel and iterate before adding more orders to the stack.
            order.cancel(self.symbol);
            self.chkMktSystem==0;
            return;
            
            
        if(event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time and self.chkMktSystem==1 and self.allocator>0):
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
                            if(dmp>self.__class__.cycl and abs(account[self.symbol].position.capital_long)<self.riskAllowance*10 and len(account[self.symbol].pending.orders)<10 and self.quvantity>0):
                                ## self.allocator>0
                                if(len(account[self.symbol].pending.orders)>6 or self.allocated[-1]>self.allocated[-2]):
                                    #service.write_file(self.filenameB,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format('chkSP[+][-0.01]',self.qqqBid, self.spyBid, md.L1.bid, md.L1.ask, md.L1.last, self.tkrRate[-1], self.chkTrajectoryQ[-1], self.chkTrajectoryQ[-1], self.chkTrajectoryS[-1],self.chkTrajectoryS[-1], 'NA', 'NA', self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1], self.allocator, self.chkMktSystem));   
                                    self.orderECN=1;
                                    pass;
                                 
                                if(self.orderECN==1 and abs(account[self.symbol].position.capital_long)<self.riskAllowance*10):
                                    self.orderECN=0;
                                    ### zeroPx Loop
                                    ##
                                    zeroPx = min(md.L1.bid, md.L1.last, md.L1.ask) + 0.01;
                                    bidQty = int(self.quvantity)+1;
                                    if(self.allocated[-1]>self.allocated[-2]):
                                        bidQty+=self.allocated[-1]-self.allocated[-2];
                                        riskUnitOne = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=self.quvantity, user_key=111, allow_multiple_pending=40);
                                        riskUnitZero = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=bidQty, price=zeroPx, user_key=111, allow_multiple_pending=40);
                                        return riskUnitOne, riskUnitZero;
                                    
                                    riskUnitZero = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=bidQty+1, price=zeroPx, user_key=111, allow_multiple_pending=40);
                                    # onePx = md.L1.ask + 0.01;
                                    # riskUnitOnePx = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=bidQty, price=onePx, user_key=111, allow_multiple_pending=40);
                                    
                                    return riskUnitZero;
                                    
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
        if(event.user_tag==112 and event.intent=='decrease' and account[self.symbol].position.capital_long>0):
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
