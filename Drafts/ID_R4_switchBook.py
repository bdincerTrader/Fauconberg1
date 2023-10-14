from cloudquant.interfaces import Strategy
import numpy as ktgChk
import time, datetime, random

class Gr8Script91cd0bc5dd3c4ed89293b2f964c1c593(Strategy):
    __script_name__ = 'switchBook'
    
    bpRisk=5; orderType=0; cycl=6; bpMaxLoss=-bpRisk*0.20; plUnrlRTE=bpRisk*0.0010; lclTimeFreq=3; plUpperBand=bpRisk*0.01; plLowerBand=-bpRisk*0.01; plBandMult=bpRisk*0.01;
    BENCHMARK_A="QQQ";BENCHMARK_B="SPY";
    demandBid=0; supplyAsk=0;
    maxItem=10;
    tickerItrBbRon=['AVGO','UNH','CHTR','KLAC','DE','CI','NOC','PAYC','ANSS','MOH','INTU','VGT','CVNA','ANET', 'SPY', 'QQQ'];
    

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol in Gr8Scripte26cb7cc28424c93ad4a500576ab1541.tickerItrBbRon;
        #return md.stat.prev_close>20.00 and md.stat.atr>5 and md.stat.avol>400000;
        

    def __init__(self, **params):
        if('riskAllocation' in params):
            self.__class__.bpRisk=params['riskAllocation'];
            self.__class__.maxCapUnit=params['maxBP'];
            self.__class__.lclTimeFreq=params['timeFreq'];
            self.__class__.cycl=params['cycl'];
            self.__class__.orderType=params['orderType'];
            self.__class__.BENCHMARK_A=params['benchmarkA']; 
            self.__class__.BENCHMARK_B=params['benchmarkB'];
            self.__class__.maxItem=params['maxSymbolTrade'];
            self.__class__.demandBid=params['bidGate'];
            self.__class__.supplyAsk=params['askGate'];
            print('riskAllocation>>', params['riskAllocation'], '\n', 'plRiskBp>> self.__class__.bpRisk*params[plRiskBp]', \
            '\n', '[maxBP]', self.__class__.maxCapUnit, '[maxSymbolTrade]', self.__class__.maxItem, 'timeFreq..', params['timeFreq'],'\n','cycl', params['cycl'],\
            '\n','orderType',params['orderType'],'\n', 'benchmarkA', params['benchmarkA'], '\n','benchmarkB', params['benchmarkB']);
            pass;
            

    def on_start(self, md, order, service, account):
        self.arrSymbol=self.__class__.maxItem;

        #self.filetest='\\\EQKTG02'+'\\bdincer'+self.symbol+service.time_to_string(service.system_time, '%Y-%m-%d')+".txt";
        self.filetest=service.time_to_string(service.system_time, '%Y-%m-%d')+"-exitPROD.txt";
        self.filetest2=service.time_to_string(service.system_time, '%Y-%m-%d')+"-ordersPROD.txt";
        self.filetest3=self.symbol+service.time_to_string(service.system_time, '%Y-%m-%d')+"-ordersPROD.txt";
        self.filetestC=self.symbol+service.time_to_string(service.system_time, '%Y-%m-%d')+"-ORDERbookPROD.txt";
        print(self.symbol, service.time_to_string(service.system_time, '%Y-%m-%d'), self.filetest);
        self.dataBook =[[],[],[],[],[],[],[],[],[]];
        self.bb1=[]; self.bb2=[]; self.bb3=[];                                                                                              
        self.orderECN=self.__class__.orderType;                             
        self._atr, self._avol, self._beta, self._prev_close = md.stat.atr, md.stat.avol, md.stat.beta, md.stat.prev_close;
        self.riskUnit=self.__class__.bpRisk;
        self.quvantity=int(self.riskUnit/md.stat.prev_close);
        self.qtyZero=self.quvantity;
        self.qCtr=0;
        
        self.riskAllowance=int(self.riskUnit);
        self.cycle=self.__class__.cycl;
        self.dayTimer=self.__class__.lclTimeFreq;
        self.plCond=0;
        self.sizeAgg=0;
        
        #RB STACK
        self.postUnit=self.__class__.maxCapUnit;
        self.itr=0;self.ID_R1=[];self.ID_R2=[];self.ID_RB1=[];
        self.RBCT=[];self.RBCT_PRIME=[];
        self.gates=[]; self.demand=[]; self.supply=[];
        self.demandGate=self.__class__.demandBid;
        self.supplyGate=self.__class__.supplyAsk;
        self.orderBook=[];
        self.marketDepth=([0, 0, 0],[0, 0, 0],[0, 0, 0]);
        self.chkMin=0;
        self.chkMinPt=0;
        self.chkMax=0;
        self.chkMaxPt=0;
        self.chkHop=[];
        self.chkHtz=0;
        self.ID_R3=[];
        self.ID_R4=[];
        self.SWITCH_BOOK=[];
        self.limitBP=0;
        self.order_quantity_max=account.buying_power/self.arrSymbol;
        self.plFlip=self.order_quantity_max/1000;
        self.unloadUnits=0
        
        # COUNTER.
        self.allocator=0; self.allocated=[0];                           
        self.safetySymbol=640;
        self.qtyStat=540;
        self.benchMarkA=self.__class__.BENCHMARK_A;
        self.chkTrajectoryQ=[0.00]; self.qqqPrior=(md[self.benchMarkA].stat.prev_close); self.qqqBid=(md[self.benchMarkA].L1.bid); self.chkTrajectoryQ.append( ((self.qqqBid-self.qqqPrior)/self.qqqPrior)); self.tkrQQQ=0.00; self.dfQ=0.00;
        self.benchMarkB=self.__class__.BENCHMARK_B;
        self.chkTrajectoryS=[0.00]; self.spyPrior=(md[self.benchMarkB].stat.prev_close); self.spyBid=(md[self.benchMarkB].L1.bid); self.chkTrajectoryS.append( ((self.spyBid-self.spyPrior)/self.spyPrior)); self.tkrSPY=0.00; self.dfS=0.00;
        self.tkrRate=[0.00]; self.trajectoryBook=[0.00]; self.trajectoryBid=[0.00]; self.trajectoryAsk=[0.00]; self.trajectoryLast=[0.00]; self.trajectorySpread=[0.00]; self.pxTrajectory=[0.00];self.rtTrajectory=[0.00];self.rtTrajectoryHop=[0.00];
        self.midPrice=0.00; self.pxChg=0.00;
        self.trajectorySpread[0]=(md.L1.ask-md.L1.bid);
        
        print('order_quantity_max', self.order_quantity_max);
        self.limitBP=self.order_quantity_max-account[self.symbol].position.capital_long-account[self.symbol].pending.capital_long;
        
        print('limitBP', self.limitBP);
        
        self.liquid_time = md.market_open_time + service.time_interval(minutes=21)
        self.illiquid_time = md.market_close_time - service.time_interval(minutes=45)
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=10), repeat_interval=service.time_interval(seconds=self.dayTimer), timer_id="Allocate")
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=10), repeat_interval=service.time_interval(seconds=self.dayTimer+30), timer_id="Orderbook")
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=5), repeat_interval=service.time_interval(seconds=int(self.dayTimer+20)), timer_id="Review")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=45), timer_id = "eod_1")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=12), timer_id = "eod_2")
        pass;
        
    def on_timer(self, event, md, order, service, account):
    
        self.limitBP=self.order_quantity_max-account[self.symbol].position.capital_long-account[self.symbol].pending.capital_long;
        
        

        if(event.timer_id=="Review"):
        
            ITR_A = self.chkINFO(md);
            ITR_B = self.chkPerimeter();
            ITR_C = self.chkInterior();         
            oopA = self.mk1_info(md);
            oopB = self.mk2_info();
            oopC = self.mk3_info();
            oopD = self.mk4_info();
            oopE = self.ID_R1_INFO();
            oopF = self.ID_R2_INFO();
            oopG = self.ID_R3_INFO();
            oopH = self.ID_R4_INFO(account);
            wrtInfo = self.buff_LCL(account, service, md);
            
            # MAINTAINS A FRESH PENDING ORDER BOOK.
            
            if(len(account[self.symbol].pending.orders)>28):
                order.cancel(self.symbol);
            
            if(len(self.allocated)>5 and self.allocated[-2]>1):
                if(self.allocated[-1]>self.allocated[-2]>self.allocated[-3]):
                    self.safetySymbol=640; self.orderECN==1; self.quvantity+=1;  self.qCtr+=1; return 1;
                elif(self.allocated[-1]==self.allocated[-2] and self.allocator>1):
                    self.safetySymbol=640; self.orderECN==0; return 0;
                elif(self.allocated[-1]<self.allocated[-2] and self.allocator>1):
                    self.safetySymbol=640; self.orderECN==0; return 0;
                elif(self.allocated[-1]<self.allocated[-2] and self.allocator<0):
                    self.safetySymbol=750;
                    self.orderECN==-1;
                    return -1;
            else:
                return 1;
            return 1;


        if(event.timer_id=="Orderbook"):
            if(self.symbol=="QQQ" or self.symbol=="SPY"):
                return;
                
            self.unloadUnits=0;
            plA= account[self.symbol].position.capital_long*1.01
            
            # RICKEY HENDERSON.
            if(account[self.symbol].unrealized_pl.entry_pl>plA):
                if(len(self.ID_R3)>2):
                    # service.write_file(self.filetest,'{},{},{},{},{},{},{},{},{},{}'.format(self.itr, service.time_to_string(service.system_time), self.symbol,  1407, self.trajectoryBook[-1], self.safetySymbol, self.allocator, self.allocated[-1], self.ID_R3[-1][9], self.qtyStat), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                    chkPL_CapLong = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=max(int(account[self.symbol].position.shares/4),1), user_key=1407, allow_multiple_pending=40);
                    pass;
                pass;    
            
            # P&L FLIPPER.
            if(account[self.symbol].unrealized_pl.entry_pl>self.plFlip):
                if(len(self.ID_R3)>2):
                    # service.write_file(self.filetest,'{},{},{},{},{},{},{},{},{},{}'.format(self.itr, service.time_to_string(service.system_time), self.symbol,  1809, self.trajectoryBook[-1], self.safetySymbol, self.allocator, self.allocated[-1], self.ID_R3[-1][9], self.qtyStat), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                    chkPL_Flipper = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=max(int(account[self.symbol].position.shares/4),1), user_key=1809, allow_multiple_pending=40);
                    pass;
                pass;
            if(account[self.symbol].position.mtm_price<self.midPrice*1.020):
                ## self.unloadUnits+=(account[self.symbol].position.shares*.10)
                pass;
            if(account[self.symbol].position.mtm_price<self.midPrice*1.015):
                # self.unloadUnits+=(account[self.symbol].position.shares*.05)
                pass;
            if(account[self.symbol].position.mtm_price<self.midPrice*1.01):
                # self.unloadUnits+=(account[self.symbol].position.shares*.02)
                pass;
            if(account[self.symbol].position.mtm_price<self.midPrice*1.0050):
                # self.unloadUnits+=(account[self.symbol].position.shares*.01)
                pass;

            if(self.chkHtz>=0):    
                # self.unloadUnits+=(account[self.symbol].position.shares*.01)
                pass;
            if(event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time and self.allocator>1 and self.ID_R3[-1][9]==0):
                # self.unloadUnits+=(account[self.symbol].position.shares*.01)
                pass;
              
            # DECREASE POSITIONS USING THE 'UNLOADUNITS'
            if(self.unloadUnits<account[self.symbol].position.shares and account[self.symbol].position.shares>0 and (self.unloadUnits-1)>1):
                # clsUnitRisk = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=int(self.unloadUnits), user_key=1802, allow_multiple_pending=40);
                pass;
            elif(account[self.symbol].position.shares>0):
                # clsUnitRisk = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=(account[self.symbol].position.shares), user_key=1912, allow_multiple_pending=40);
                pass;
            
            # 2% RULE.  
            # BRIDGEBUILDER.  
            if(account[self.symbol].position.mtm_price>max(md.L1.bid,self.midPrice)*1.0077):
                # service.write_file(self.filetest,'{},{},{},{},{},{},{},{},{},{}'.format(self.itr, service.time_to_string(service.system_time), self.symbol,  750.750, self.trajectoryBook[-1], self.safetySymbol, self.allocator, self.allocated[-1], self.ID_R3[-1][9], self.qtyStat), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                self.safetySymbol=750;
                pass;
            
            return;
            
        if(self.allocator<0):
            self.safetySymbol=750;
            return -1;
        
        if(self.allocator<0 or self.safetySymbol==750):
            self.safetySymbol=750;
            cancelAllOrders=account[self.symbol].pending.orders; ctOrders=len(cancelAllOrders);
            if(ctOrders!=0):
                order.cancel(self.symbol);
                return -1;
            elif(account[self.symbol].position.shares>0):
                png97b = order.algo_sell(self.symbol, algorithm='5a8a9f9d-22a5-4155-87e7-4ebe8024a97b', intent='decrease', order_quantity=account[self.symbol].position.shares, user_key=2121, allow_multiple_pending=40);
                return -2;
        elif(self.allocator>1 and self.safetySymbol!=750):
            if(self.safetySymbol!=555):
                self.safetySymbol=640;
                pass;
            else:
                return 0;
        
        if event.timer_id=="eod_1":
            if(len(account[self.symbol].pending.orders)>0):
                order.cancel(self.symbol);pass;
            else: return 1;
            
        if event.timer_id=="eod_2":
            if(account[self.symbol].position.shares>0):
                closeInventory = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=account[self.symbol].position.shares, user_key=113, allow_multiple_pending=40)
                return closeInventory;
            else: return 1;
        
        
        # ALLOCATOR- TYPE A
        # PENDING ORDER LIMIT IS NOT BREACHED.
        # MAX BP IS NOT BREACHED.
        self.limitBP=self.order_quantity_max-account[self.symbol].position.capital_long-account[self.symbol].pending.capital_long;
        if(event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time and self.allocator>1 and self.ID_R3[-1][9]==1 and self.postUnit>0 and len(account[self.symbol].pending.orders)<30 and self.limitBP>0):            
            
            if(self.symbol=="QQQ" or self.symbol=="SPY"):
                return;
        
            if(self.ID_RB1[-1][6]==1):
                self.marketDepth[0][0]+=1;
                service.write_file(self.filetest2,'{},{},{},{},{},{},{},{},{},{}'.format(self.itr, service.time_to_string(service.system_time), self.symbol,  6, self.trajectoryBook[-1], self.safetySymbol, self.allocator, self.allocated[-1], self.ID_R3[-1][9], self.qtyStat), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                postBB = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=self.postUnit, user_key=212, allow_multiple_pending=40);
                postB = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.postUnit, price=self.demand[-1][self.demandGate], user_key=212, allow_multiple_pending=40);
                pass;
            elif(self.ID_RB1[-1][8]==1):
                self.marketDepth[1][0]+=1;
                service.write_file(self.filetest2,'{},{},{},{},{},{},{},{},{},{}'.format(self.itr, service.time_to_string(service.system_time), self.symbol,  8, self.trajectoryBook[-1], self.safetySymbol, self.allocator, self.allocated[-1], self.ID_R3[-1][9], self.qtyStat), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                
                postCC = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=self.postUnit, user_key=212, allow_multiple_pending=40);
                postC = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.postUnit, price=self.demand[-1][self.demandGate], user_key=212, allow_multiple_pending=40);
                pass;
            elif(self.ID_RB1[-1][10]==1):
                self.marketDepth[2][0]+=1;
                service.write_file(self.filetest2,'{},{},{},{},{},{},{},{},{},{}'.format(self.itr, service.time_to_string(service.system_time), self.symbol, 10, self.trajectoryBook[-1], self.safetySymbol, self.allocator, self.allocated[-1], self.ID_R3[-1][9], self.qtyStat), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                
                postDD = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=self.postUnit, user_key=212, allow_multiple_pending=40);
                postD = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.postUnit, price=self.demand[-2][self.demandGate], user_key=212, allow_multiple_pending=40);
                pass;
            pass;



        # ALLOCATOR- TYPE B
        # PENDING ORDER LIMIT IS NOT BREACHED.
        # MAX BP IS NOT BREACHED.
        self.limitBP=self.order_quantity_max-account[self.symbol].position.capital_long-account[self.symbol].pending.capital_long;
        if(event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time and self.allocator>1 and self.ID_R3[-1][9]==1 and len(account[self.symbol].pending.orders)<30 and self.limitBP>0):
            if(account[self.symbol].position.shares<0):
                demitRisk = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=115, allow_multiple_pending=40);
                return;
                

            if(self.symbol=="QQQ" or self.symbol=="SPY"):
                return;
                
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
                                if(dmp>self.cycle):
                                    if(self.dataBook[idx][-1]-self.dataBook[idx][-2]>0): imbl.append([idx, self.dataBook[idx][-1]-self.dataBook[idx][-2]]);pass;
                                    else: dmp-=1;pass;
                                else:
                                    return 0;
                                    
                            if(dmp>self.cycle and self.quvantity>0):
                            
                                zeroPx = min(md.L1.bid, md.L1.last, md.L1.ask) + 0.01;
                                bidQty = int(self.quvantity)+1;
                                maxQty = int(self.limitBP/zeroPx)+1
                                
                                if(bidQty>maxQty):
                                    bidQty=maxQty;

                                if(len(account[self.symbol].pending.orders)>6):
                                    self.orderECN=1;
                                    pass;
                                    
                                if(self.orderECN==1):
                                    self.orderECN=0;
                                    service.write_file(self.filetest2,'{},{},{},{},{},{},{},{},{},{}'.format(self.itr, service.time_to_string(service.system_time), self.symbol, min(self.quvantity, maxQty), self.trajectoryBook[-1],  self.safetySymbol, self.allocator, self.allocated[-1], self.ID_R3[-1][9], self.qtyStat), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                                    riskUnitLMT = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=bidQty, price=self.demand[-1][self.demandGate]-abs(self.trajectorySpread[-1]*3), user_key=111, allow_multiple_pending=40);
                                    self.qCtr=0;
                                    riskUnitMKT = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=min(self.quvantity, maxQty), user_key=111, allow_multiple_pending=40);
                                    return riskUnitLMT, riskUnitMKT;
                                else:
                                    service.write_file(self.filetest2,'{},{},{},{},{},{},{},{},{},{}'.format(self.itr, service.time_to_string(service.system_time), self.symbol, min(self.quvantity, maxQty), self.trajectoryBook[-1],  self.safetySymbol, self.allocator, self.allocated[-1], self.ID_R3[-1][9], self.qtyStat), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                                    lmtOrd = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=min(self.quvantity, maxQty), price=self.demand[-1][self.demandGate]-abs(self.trajectorySpread[-1]*3), user_key=111, allow_multiple_pending=40);
                                    return lmtOrd;
                            else: return 0;
                        else: return 0;
                    else: return 0;
                else: return 0;
            else: return 0;
        else: return 0;        
    def chkINFO(self, md):
        self.itr+=1;
        self.RBCT.append(0);
        self.RBCT_PRIME.append([0.00,0.00,0.00,0.00]);
        self.SWITCH_BOOK.append([0.00,0.00,0.00,0.00]);
        self.chkHop.append([0.00,0.00,0.00]);
        self.midPrice=0.00; self.pxChg=0.00;
        self.gates.append([0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00]);
        self.ID_RB1.append([0.00,0.00,0.00,0.00,0,0,0,0,0,0,0]);
        self.demand.append([self.demandGate, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0]);
        self.supply.append([self.supplyGate, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0]);
        self.qqqBid=(md[self.benchMarkA].L1.bid);
        self.spyBid=(md[self.benchMarkB].L1.bid);
        self.chkMktSystem=1;
        self.midPrice=((md.L1.ask+md.L1.bid+md.L1.last)/3);
        self.pxChg=((self.midPrice - self._prev_close)/ self._prev_close);
        self.trajectoryBook.append(self.midPrice);
        self.tkrRate.append(self.pxChg);
        self.trajectoryBid.append(md.L1.bid);
        self.trajectoryAsk.append(md.L1.ask);
        self.trajectoryLast.append(md.L1.last);
        self.trajectorySpread.append(md.L1.ask-md.L1.bid);
        self.chkTrajectoryQ.append(((md[self.benchMarkA].L1.bid) - self.qqqPrior + 0.000001) /self.qqqPrior );
        self.chkTrajectoryS.append(((md[self.benchMarkB].L1.bid) - self.spyPrior + 0.000001) /self.spyPrior );
        self.dfQ=self.pxChg-self.chkTrajectoryQ[-1];
        self.dfS=self.pxChg-self.chkTrajectoryS[-1];
        self.pxTrajectory.append(self.midPrice);
        self.rtTrajectory.append(0.00);
        self.rtTrajectoryHop.append(0.00);
        self.ID_R3.append([0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]);
        self.ID_R4.append([0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00]);
        return 1;

    def chkPerimeter(self):
        if(len(self.pxTrajectory)>2):
            if(self.trajectoryBook[-1]<self.trajectoryBook[-2]):
                self.chkMin=self.trajectoryBook[-1];
                self.chkMinPt+=1;
                pass;
            if(self.trajectoryBook[-1]>self.trajectoryBook[-2]):
                self.chkMax=self.trajectoryBook[-1];
                self.chkMaxPt+=1;
                pass;
            pass;
        return 1;
    
    def chkInterior(self):
        if(len(self.demand)>10 and len(self.supply)>10):
            self.demand[-1][5]=self.trajectoryBid[-10:]+self.trajectoryLast[-10:]+self.trajectoryBook[-10:];
            self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4] = ktgChk.percentile(self.demand[-1][5], [ 10, 50, 75, 100]);
            self.demand[-1][6]=(self.demand[-1][1]+self.demand[-1][2]+self.demand[-1][3]+self.demand[-1][4])/4;
            self.demand[-1][7]=self.itr;
            self.supply[-1][5]=self.trajectoryAsk[-10:]+self.trajectoryLast[-10:]+self.trajectoryBook[-10:];
            self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4] = ktgChk.percentile(self.supply[-1][5], [ 25, 50, 75, 100]);
            self.supply[-1][6]=(self.supply[-1][1]+self.supply[-1][2]+self.supply[-1][3]+self.supply[-1][4])/4;
            self.supply[-1][7]=self.itr;
            pass;
        elif(len(self.demand)>3 and len(self.supply)>3):
            self.demand[-1][5]=self.trajectoryBid[-4:]+self.trajectoryLast[-4:]+self.trajectoryBook[-4:];
            self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4] = ktgChk.percentile(self.demand[-1][5], [ 10, 50, 75, 100]);
            self.demand[-1][6]=(self.demand[-1][1]+self.demand[-1][2]+self.demand[-1][3]+self.demand[-1][4])/4;
            self.demand[-1][7]=self.itr;
            self.supply[-1][5]=self.trajectoryAsk[-4:]+self.trajectoryLast[-4:]+self.trajectoryBook[-4:];
            self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4] = ktgChk.percentile(self.supply[-1][5], [ 25, 50, 75, 100]);
            self.supply[-1][6]=(self.supply[-1][1]+self.supply[-1][2]+self.supply[-1][3]+self.supply[-1][4])/4;
            self.supply[-1][7]=self.itr;
            pass;
        return 1;

    def mk1_info(self, md):
        if(len(self.pxTrajectory)>2):
            self.chkHop[-1][-1]=self.chkHop[-2][1];
            self.pxTrajectory[-1]=(self.midPrice-self.trajectoryBook[-2]);
            if(self.trajectoryBook[-2]!=0 and self.rtTrajectory[-2]!=0):
                self.rtTrajectory[-1]=self.pxTrajectory[-1]/self.trajectoryBook[-2];
                self.rtTrajectoryHop[-1]=self.rtTrajectory[-1]/self.rtTrajectory[-2];
                pass;
            else:
                self.rtTrajectory[-1]=0.00001;
                self.rtTrajectoryHop[-1]=0.000001;
                pass;
                
            if(self.rtTrajectoryHop[-1]>self.rtTrajectoryHop[-2]):
                self.chkHop[-1][0]=1;
                self.chkHop[-1][1]=self.chkHop[-1][1]+1;
                self.chkHop[-1][2]=self.chkHop[-1][1]-self.chkHop[-2][1];
                pass;
            
            self.gates[-1][0]=md.L1.last-md.L1.bid;
            self.gates[-1][1]=(self.trajectorySpread[-1]/4);
            self.gates[-1][2]=(self.gates[-1][1]*2)
            self.gates[-1][3]=(self.gates[-1][1]*3)
            self.gates[-1][4]=self.trajectorySpread[-1];
            
            if(self.gates[-1][0]>=self.gates[-1][4]):
                self.gates[-1][5]=4;
                pass;
            elif(self.gates[-1][0]>=self.gates[-1][3]):
                self.gates[-1][5]=3;
                pass;
            elif(self.gates[-1][0]<=self.gates[-1][1]):
                self.gates[-1][5]=-4;
                pass;
            elif(self.gates[-1][0]<=self.gates[-1][2]):
                self.gates[-1][5]=-3;
                pass;
            else:
                self.gates[-1][5]=0;
                pass;
            pass;
        else:
            self.pxTrajectory[-1]=0;
            pass;
           
        return 1;
        
    def mk2_info(self):
    
        if(len(self.gates)>10):
            self.gates[-1][6]=sum(cy[5] for cy in self.gates[-10:])/9;
            self.gates[-1][7]=min(ap[6] for ap in self.gates[-10:]);
            self.gates[-1][8]=max(lt[6] for lt in self.gates[-10:]);
            if(self.gates[-1][7]==self.gates[-1][6]):
                self.gates[-1][9]=1;
                pass;
            if(self.gates[-1][8]==self.gates[-1][6]):
                self.gates[-1][10]=1;
                pass;
                
            self.gates[-1][11]=sum(self.allocated[-10:])/9;
                            
            if(self.gates[-1][11]>self.gates[-2][11]):
                self.ID_RB1[-1][4]=1;
                pass;
            else:
                self.ID_RB1[-1][4]=0;
                pass;
            pass;
        else:
            self.gates[-1][6]=self.gates[-1][5];
            pass;
            
        return 1;

    def mk3_info(self):
        if(self.dfQ>0.01):
            if(self.tkrRate[-1]<self.chkTrajectoryQ[-1]):
                self.allocator-=1;
                pass;
            if(self.tkrRate[-1]>self.chkTrajectoryQ[-1]):
                self.allocator+=1;
                pass;
            pass;
        if(self.dfS>0.01):
            if(self.tkrRate[-1]<self.chkTrajectoryS[-1]):
                self.allocator-=1;
                pass;
            if(self.tkrRate[-1]>self.chkTrajectoryS[-1]):
                self.allocator+=1;
                pass;
            pass;
        if(self.dfQ<-0.01):
            if(self.tkrRate[-1]<self.chkTrajectoryQ[-1]):
                self.allocator-=1;
                pass;
            if(self.tkrRate[-1]>self.chkTrajectoryQ[-1]):
                self.allocator+=1;
                pass;
            pass;
        if(self.dfS<-0.01):
            if(self.tkrRate[-1]<self.chkTrajectoryS[-1]):
                self.allocator-=1;
                pass;
            if(self.tkrRate[-1]>self.chkTrajectoryS[-1]):
                self.allocator+=1;
                pass;
            pass;
        return 1;    
              
    def mk4_info(self):
        self.allocated.append(self.allocator);       
        self.ID_R1.append(self.allocated[-1]/self.itr);
        return;
        
    def ID_R1_INFO(self):   
        if(len(self.ID_R1)>1):    
            self.ID_R2.append(self.ID_R1[-1]-self.ID_R1[-2]);
            if(self.ID_R1[-1]>self.ID_R1[-2]):
                self.ID_RB1[-1][1]=1;
                if(len(self.allocated)>5 and self.ID_RB1[-1][4]==1):
                    self.ID_RB1[-1][7]=1;
                    if(self.allocated[-1]>0 and self.gates[-1][6]>0):
                        self.RBCT[-1]+=1;
                        self.ID_RB1[-1][8]=1;
                        pass;
                    pass;
                pass;
            self.ID_RB1[-1][2]=self.trajectoryBook[-1]-self.trajectoryBook[-2];
            self.ID_RB1[-1][3]=((self.trajectoryBook[-1]-self.trajectoryBook[-2])/self.trajectoryBook[-2]);
            pass;
        else:
            self.ID_R2.append(0);
            self.ID_RB1[-1][1]=0;
            pass;
        return 1;
        
    def ID_R2_INFO(self):   
        if(len(self.ID_R2)>1):
            if(self.ID_R2[-1]>self.ID_R2[-2]):
                self.ID_RB1[-1][0]=1;
                if(len(self.allocated)>5 and self.ID_RB1[-1][4]==1):
                    self.ID_RB1[-1][5]=1;
                    if(self.allocated[-1]>0):
                        self.RBCT[-1]+=1;
                        self.ID_RB1[-1][6]=1;
                        pass;
                    pass;
                elif(len(self.allocated)>5 and self.ID_RB1[-1][4]==0):
                    self.ID_RB1[-1][9]=1;
                    if(self.allocated[-1]>0 and self.trajectoryBook[-1]>0):
                        self.RBCT[-1]+=1;
                        self.ID_RB1[-1][10]=1;
                        pass;
                pass;
            else:
                self.ID_RB1[-1][0]=0;
                pass;
        else:
            self.ID_RB1[-1][0]=0;
            pass;
        return 1;
        
    def ID_R3_INFO(self): 
        if(len(self.ID_R1)>1):
            if(self.ID_R1[-2]==0):
                self.ID_R3[-1][0]=self.ID_R1[-1];
                pass;
            else:
                self.ID_R3[-1][0]=self.ID_R1[-1]-1;
                pass;
                
            if(self.ID_R3[-1][0]>self.ID_R3[-2][0]):
                self.ID_R3[-1][1]=1;
                pass;
                
            self.ID_R3[-1][2]=self.ID_R3[-1][1]+self.ID_R3[-2][2];
            self.ID_R3[-1][3]=self.ID_R3[-1][2]-self.ID_R3[-2][2];
            
            if(self.RBCT[-1]>=1 and self.RBCT[-2]==0):
                if(self.ID_R3[-1][2]>0):
                    self.ID_R3[-1][4]=self.ID_R3[-2][4]+self.ID_R3[-1][3];
                    pass;
                pass;    
            if(self.RBCT[-1]==1):
                self.ID_R3[-1][6]=self.trajectoryBook[-1];
                pass;
                
            if(self.RBCT[-1]>1):
                self.ID_R3[-1][5]=self.trajectoryBook[-1];
                self.ID_R3[-1][7]=-1;
                self.ID_R3[-1][8]=self.ID_R3[-1][1];
                pass;
            elif(self.ID_R3[-2][8]>0):
                self.ID_R3[-1][8]=self.ID_R3[-1][1]+self.ID_R3[-2][8];
                pass;
                
            if(self.ID_R3[-1][8]>self.ID_R3[-2][8]):
                self.ID_R3[-1][9]=1;
                pass;
            pass;
        return 1;
        
    def ID_R4_INFO(self, account): 
        if(len(self.ID_R1)>1):
            self.ID_R4[-1][16]=self.qCtr;
            
            if(self.qCtr!=0):
                self.ID_R4[-1][0]=self.quvantity/self.qCtr;
                pass;
                
            if(self.qCtr==0):
                self.ID_R4[-1][1]=self.quvantity-self.qtyZero;
                pass;
            
            if(self.ID_R4[-1][1]!=0):
                self.ID_R4[-1][2]=self.midPrice;
                pass;
            
            self.ID_R4[-1][3]=self.ID_R4[-1][2]*self.ID_R4[-1][1];
            self.ID_R4[-1][4]=self.ID_R4[-2][4]+self.ID_R4[-1][3];
            
            if(self.ID_R4[-1][16]<self.ID_R4[-2][16]):
                self.ID_R4[-1][5]=self.ID_R4[-2][5]+self.ID_R4[-1][1];
                pass;

            self.ID_R4[-1][6]=self.ID_R4[-1][5]+self.ID_R4[-2][6];
            self.ID_R4[-1][7]=self.ID_R4[-1][6]/self.itr;
            
            if(self.ID_R4[-2][7]!=0):
                self.ID_R4[-1][8]=self.ID_R4[-1][7]-self.ID_R4[-2][7];
                pass;
            
            self.ID_R4[-1][9]=self.ID_R4[-1][8]+self.ID_R4[-2][9];

            if(self.ID_R4[-1][9]>1 and self.ID_R4[-1][9]>self.ID_R4[-2][10]):
                self.ID_R4[-1][10]=self.ID_R4[-1][9]+self.ID_R4[-2][10];
                pass;
            else:
                self.ID_R4[-1][10]=self.ID_R4[-2][10]+self.ID_R4[-1][8];
                pass;

            if(self.ID_R4[-1][10]>self.ID_R4[-2][10]):
                self.ID_R4[-1][11]=1;
                self.chkHtz=self.ID_R4[-1][13];
                pass;
            else:
                self.chkHtz-=self.quvantity;
                pass;
            
            self.ID_R4[-1][12]=self.ID_R4[-1][11]*self.quvantity;
            self.ID_R4[-1][13]=self.ID_R4[-2][13]+self.ID_R4[-1][12];
            
            if(self.ID_R4[-1][11]==1):
                self.ID_R4[-1][14]=self.midPrice;
                pass;
                
            self.ID_R4[-1][15]=self.ID_R4[-1][14]*account[self.symbol].position.shares;
            pass;
        return 1;
        
    def buff_LCL(self, account, service, md):
        if(self.symbol=="QQQ" or self.symbol=="SPY"):
            return;
        # service.write_file(self.filetest3,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.itr, self.symbol, service.time_to_string(service.system_time), service.time_to_string(service.system_time), md.L1.bid,  md.L1.ask,  md.L1.last, self.midPrice, self.pxChg, self.tkrRate[-1],  self.chkTrajectoryQ[-1], self.chkTrajectoryS[-1], self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1], self.trajectoryLast[-1], self.trajectorySpread[-1], self.pxTrajectory[-1], self.allocator, self.allocated[-1], self.ID_RB1[-1][0], self.ID_RB1[-1][1], self.ID_RB1[-1][4], self.ID_RB1[-1][5], self.ID_RB1[-1][6], self.ID_RB1[-1][7], self.ID_RB1[-1][8], self.ID_RB1[-1][9], self.ID_RB1[-1][10], self.safetySymbol, self.allocator, self.sizeAgg,self.gates[-1][0], self.gates[-1][1], self.gates[-1][2], self.gates[-1][3], self.gates[-1][4], self.gates[-1][5], self.gates[-1][6], self.gates[-1][7], self.gates[-1][8], self.gates[-1][9], self.gates[-1][10], self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4], self.demand[-1][6], self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4], self.supply[-1][6], self.chkMin, self.chkMinPt, self.chkMax, self.chkMaxPt, self.ID_R1[-1], self.chkHop[-1][0], self.chkHop[-1][1], self.chkHop[-1][2], self.RBCT_PRIME[-1][0], self.RBCT_PRIME[-1][1], self.RBCT_PRIME[-1][2], self.RBCT_PRIME[-1][3], self.ID_R3[-1][0],self.ID_R3[-1][1],self.ID_R3[-1][2], self.ID_R3[-1][3],self.ID_R3[-1][4],self.ID_R3[-1][5],self.ID_R3[-1][6],self.ID_R3[-1][7],self.ID_R3[-1][8], self.ID_R3[-1][9], account.buying_power, account[self.symbol].position.shares, self.qCtr, self.qtyZero, self.quvantity, account[self.symbol].position.mtm_price, account[self.symbol].unrealized_pl.entry_pl,account[self.symbol].realized_pl.entry_pl,  account[self.symbol].pending.count_long, account[self.symbol].pending.shares_long,  account[self.symbol].pending.capital_long,  account[self.symbol].pending.count_short, account[self.symbol].pending.shares_short, account[self.symbol].pending.capital_short, self.ID_R4[-1][0],self.ID_R4[-1][1], self.ID_R4[-1][2], self.ID_R4[-1][3], self.ID_R4[-1][4], self.ID_R4[-1][5], self.ID_R4[-1][6], self.ID_R4[-1][7], self.ID_R4[-1][8], self.ID_R4[-1][9], self.ID_R4[-1][10],self.ID_R4[-1][11], self.ID_R4[-1][12], self.ID_R4[-1][13], self.ID_R4[-1][14], self.ID_R4[-1][15], self.ID_R4[-1][16], self.qtyStat), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
        return;
        #service.write_file(self.filetestC,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.itr, self.symbol, service.time_to_string(service.system_time), service.time_to_string(service.system_time), md.L1.bid,  md.L1.ask,  md.L1.last,self.midPrice, self.pxChg, self.tkrRate[-1],  self.chkTrajectoryQ[-1], self.chkTrajectoryS[-1], self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1], self.trajectoryLast[-1], self.trajectorySpread[-1], self.pxTrajectory[-1], self.allocated[-1], self.ID_RB1[-1][0], self.ID_RB1[-1][1], self.ID_RB1[-1][4], self.ID_RB1[-1][5], self.ID_RB1[-1][6], self.ID_RB1[-1][7], self.ID_RB1[-1][8], self.ID_RB1[-1][9], self.ID_RB1[-1][10], self.safetySymbol, self.allocator, self.sizeAgg,self.gates[-1][0], self.gates[-1][1], self.gates[-1][2], self.gates[-1][3], self.gates[-1][4], self.gates[-1][5], self.gates[-1][6], self.gates[-1][7], self.gates[-1][8], self.gates[-1][9], self.gates[-1][10], self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4], self.demand[-1][6], self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4], self.supply[-1][6], self.chkMin, self.chkMinPt, self.chkMax, self.chkMaxPt, self.ID_R1[-1], self.chkHop[-1][0], self.chkHop[-1][1], self.chkHop[-1][2], self.chkHtz, 0,  0, 0, 0, self.ID_R3[-1][0],self.ID_R3[-1][1],self.ID_R3[-1][2], self.ID_R3[-1][3],self.ID_R3[-1][4],self.ID_R3[-1][5],self.ID_R3[-1][6],self.ID_R3[-1][7],self.ID_R3[-1][8], self.ID_R3[-1][9], self.ID_R3[-1][10], self.ID_R3[-1][11], self.ID_R3[-1][12], self.ID_R3[-1][13], self.ID_R3[-1][14], self.ID_R3[-1][15], self.ID_R3[-1][16], self.ID_R3[-1][17], account.buying_power, account[self.symbol].position.shares, account[self.symbol].position.mtm_price, account[self.symbol].unrealized_pl.entry_pl,account[self.symbol].realized_pl.entry_pl,  account[self.symbol].pending.count_long, account[self.symbol].pending.shares_long,  account[self.symbol].pending.capital_long,  account[self.symbol].pending.count_short, account[self.symbol].pending.shares_short, account[self.symbol].pending.capital_short, self.ID_R4[-1][0], self.ID_R4[-1][1], self.ID_R4[-1][2], self.ID_R4[-1][3], self.ID_R4[-1][4], self.ID_R4[-1][5], self.ID_R4[-1][6], self.ID_R4[-1][7], self.ID_R4[-1][8], self.ID_R4[-1][9], self.ID_R4[-1][10], self.ID_R4[-1][11], self.ID_R4[-1][12], self.ID_R4[-1][13], self.ID_R4[-1][14], self.ID_R4[-1][15]), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
        #service.write_file(self.filetestB,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.itr, self.symbol, service.time_to_string(service.system_time), service.time_to_string(service.system_time), md.L1.bid,  md.L1.ask,  md.L1.last,self.midPrice, self.pxChg, self.safetySymbol, self.qtyStat, self.chkHtz, self.allocator, self.sizeAgg, self.gates[-1][0], self.gates[-1][1], self.gates[-1][2], self.gates[-1][3], self.gates[-1][4], self.gates[-1][5], self.gates[-1][6], self.gates[-1][7], self.gates[-1][8], self.gates[-1][9], self.gates[-1][10], self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4], self.demand[-1][6], self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4], self.supply[-1][6], self.ID_R3[-1][8], self.ID_R3[-1][9], self.chkMin, self.chkMinPt, self.chkMax, self.chkMaxPt, event.shares, event.price, event.instruction_id, event.user_tag, account.buying_power, account[self.symbol].position.shares, self.qCtr, self.qtyZero, self.quvantity, self.ID_R4[-1][10],self.ID_R4[-1][11], self.ID_R4[-1][12], self.ID_R4[-1][13], self.ID_R4[-1][14], self.ID_R4[-1][15], self.ID_R4[-1][16], account[self.symbol].position.mtm_price, account[self.symbol].unrealized_pl.entry_pl,account[self.symbol].realized_pl.entry_pl,  account[self.symbol].pending.count_long, account[self.symbol].pending.shares_long,  account[self.symbol].pending.capital_long,  account[self.symbol].pending.count_short, account[self.symbol].pending.shares_short, account[self.symbol].pending.capital_short));
        # service.write_file(self.filetestB,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.itr, self.symbol, service.time_to_string(service.system_time), service.time_to_string(service.system_time), md.L1.bid,  md.L1.ask,  md.L1.last,self.midPrice, self.pxChg, self.tkrRate[-1],  self.chkTrajectoryQ[-1], self.chkTrajectoryS[-1], self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1], self.trajectoryLast[-1], self.trajectorySpread[-1], self.pxTrajectory[-1], self.allocated[-1], self.ID_RB1[-1][0], self.ID_RB1[-1][1], self.ID_RB1[-1][4], self.ID_RB1[-1][5], self.ID_RB1[-1][6], self.ID_RB1[-1][7], self.ID_RB1[-1][8], self.ID_RB1[-1][9], self.ID_RB1[-1][10], self.safetySymbol, self.allocator, self.sizeAgg,self.gates[-1][0], self.gates[-1][1], self.gates[-1][2], self.gates[-1][3], self.gates[-1][4], self.gates[-1][5], self.gates[-1][6], self.gates[-1][7], self.gates[-1][8], self.gates[-1][9], self.gates[-1][10], self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4], self.demand[-1][6], self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4], self.supply[-1][6], self.chkMin, self.chkMinPt, self.chkMax, self.chkMaxPt, self.ID_R1[-1], self.chkHop[-1][0], self.chkHop[-1][1], self.chkHop[-1][2], event.shares, event.price, event.instruction_id, event.user_tag, self.ID_R3[-1][0],self.ID_R3[-1][1],self.ID_R3[-1][2], self.ID_R3[-1][3],self.ID_R3[-1][4],self.ID_R3[-1][5],self.ID_R3[-1][6],self.ID_R3[-1][7],self.ID_R3[-1][8], self.ID_R3[-1][9], account.buying_power, account[self.symbol].position.shares, self.qCtr, self.qtyZero, self.quvantity, account[self.symbol].position.mtm_price, account[self.symbol].unrealized_pl.entry_pl,account[self.symbol].realized_pl.entry_pl,  account[self.symbol].pending.count_long, account[self.symbol].pending.shares_long,  account[self.symbol].pending.capital_long, account[self.symbol].pending.count_short, account[self.symbol].pending.shares_short, account[self.symbol].pending.capital_short, self.ID_R4[-1][0],self.ID_R4[-1][1], self.ID_R4[-1][2], self.ID_R4[-1][3], self.ID_R4[-1][4], self.ID_R4[-1][5], self.ID_R4[-1][6], self.ID_R4[-1][7], self.ID_R4[-1][8], self.ID_R4[-1][9], self.ID_R4[-1][10],self.ID_R4[-1][11], self.ID_R4[-1][12], self.ID_R4[-1][13], self.ID_R4[-1][14], self.ID_R4[-1][15], self.ID_R4[-1][16], self.qtyStat));
        #service.write_file(self.filetestC,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.itr, self.symbol, service.time_to_string(service.system_time), service.time_to_string(service.system_time), md.L1.bid,  md.L1.ask,  md.L1.last,self.midPrice, self.pxChg, self.tkrRate[-1],  self.chkTrajectoryQ[-1], self.chkTrajectoryS[-1], self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1], self.trajectoryLast[-1], self.trajectorySpread[-1], self.pxTrajectory[-1], self.allocated[-1], self.ID_RB1[-1][0], self.ID_RB1[-1][1], self.ID_RB1[-1][4], self.ID_RB1[-1][5], self.ID_RB1[-1][6], self.ID_RB1[-1][7], self.ID_RB1[-1][8], self.ID_RB1[-1][9], self.ID_RB1[-1][10], self.safetySymbol, self.allocator, self.sizeAgg,self.gates[-1][0], self.gates[-1][1], self.gates[-1][2], self.gates[-1][3], self.gates[-1][4], self.gates[-1][5], self.gates[-1][6], self.gates[-1][7], self.gates[-1][8], self.gates[-1][9], self.gates[-1][10], self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4], self.demand[-1][6], self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4], self.supply[-1][6], self.chkMin, self.chkMinPt, self.chkMax, self.chkMaxPt, self.ID_R1[-1], self.chkHop[-1][0], self.chkHop[-1][1], self.chkHop[-1][2], self.RBCT_PRIME[-1][0], self.RBCT_PRIME[-1][1], self.RBCT_PRIME[-1][2], self.RBCT_PRIME[-1][3], self.ID_R3[-1][0],self.ID_R3[-1][1],self.ID_R3[-1][2], self.ID_R3[-1][3],self.ID_R3[-1][4],self.ID_R3[-1][5],self.ID_R3[-1][6],self.ID_R3[-1][7],self.ID_R3[-1][8], self.ID_R3[-1][9], account.buying_power, account[self.symbol].position.shares, self.qCtr, self.qtyZero, self.quvantity, account[self.symbol].position.mtm_price, account[self.symbol].unrealized_pl.entry_pl,account[self.symbol].realized_pl.entry_pl,  account[self.symbol].pending.count_long, account[self.symbol].pending.shares_long,  account[self.symbol].pending.capital_long,  account[self.symbol].pending.count_short, account[self.symbol].pending.shares_short, account[self.symbol].pending.capital_short, self.ID_R4[-1][0],self.ID_R4[-1][1], self.ID_R4[-1][2], self.ID_R4[-1][3], self.ID_R4[-1][4], self.ID_R4[-1][5], self.ID_R4[-1][6], self.ID_R4[-1][7], self.ID_R4[-1][8], self.ID_R4[-1][9], self.ID_R4[-1][10],self.ID_R4[-1][11], self.ID_R4[-1][12], self.ID_R4[-1][13], self.ID_R4[-1][14], self.ID_R4[-1][15], self.ID_R4[-1][16], self.qtyStat));  
        # service.write_file(self.filetestC,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.itr, self.symbol, service.time_to_string(service.system_time), service.time_to_string(service.system_time), md.L1.bid,  md.L1.ask,  md.L1.last,self.midPrice, self.pxChg, self.tkrRate[-1],  self.chkTrajectoryQ[-1], self.chkTrajectoryS[-1], self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1], self.trajectoryLast[-1], self.trajectorySpread[-1], self.pxTrajectory[-1], self.allocated[-1], self.ID_RB1[-1][0], self.ID_RB1[-1][1], self.ID_RB1[-1][4], self.ID_RB1[-1][5], self.ID_RB1[-1][6], self.ID_RB1[-1][7], self.ID_RB1[-1][8], self.ID_RB1[-1][9], self.ID_RB1[-1][10], self.safetySymbol, self.allocator, self.sizeAgg,self.gates[-1][0], self.gates[-1][1], self.gates[-1][2], self.gates[-1][3], self.gates[-1][4], self.gates[-1][5], self.gates[-1][6], self.gates[-1][7], self.gates[-1][8], self.gates[-1][9], self.gates[-1][10], self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4], self.demand[-1][6], self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4], self.supply[-1][6], self.chkMin, self.chkMinPt, self.chkMax, self.chkMaxPt, self.ID_R1[-1], self.chkHop[-1][0], self.chkHop[-1][1], self.chkHop[-1][2], self.chkHtz, 0,  0, 0, 0, self.ID_R3[-1][0],self.ID_R3[-1][1],self.ID_R3[-1][2], self.ID_R3[-1][3],self.ID_R3[-1][4],self.ID_R3[-1][5],self.ID_R3[-1][6],self.ID_R3[-1][7],self.ID_R3[-1][8], self.ID_R3[-1][9], self.ID_R3[-1][10], self.ID_R3[-1][11], self.ID_R3[-1][12], self.ID_R3[-1][13], self.ID_R3[-1][14], self.ID_R3[-1][15], self.ID_R3[-1][16], self.ID_R3[-1][17], account.buying_power, account[self.symbol].position.shares, account[self.symbol].position.mtm_price, account[self.symbol].unrealized_pl.entry_pl,account[self.symbol].realized_pl.entry_pl,  account[self.symbol].pending.count_long, account[self.symbol].pending.shares_long,  account[self.symbol].pending.capital_long,  account[self.symbol].pending.count_short, account[self.symbol].pending.shares_short, account[self.symbol].pending.capital_short, self.ID_R4[-1][0], self.ID_R4[-1][1], self.ID_R4[-1][2], self.ID_R4[-1][3], self.ID_R4[-1][4], self.ID_R4[-1][5], self.ID_R4[-1][6], self.ID_R4[-1][7], self.ID_R4[-1][8], self.ID_R4[-1][9], self.ID_R4[-1][10], self.ID_R4[-1][11], self.ID_R4[-1][12], self.ID_R4[-1][13], self.ID_R4[-1][14], self.ID_R4[-1][15]), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
        
        
