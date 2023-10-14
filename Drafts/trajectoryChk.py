from cloudquant.interfaces import Strategy
import numpy as ktgChk
import time, datetime, random


class Gr8Script5f807358d61f415cb94736d3f374db21(Strategy):
    __script_name__ = 'tricolumnFitzneale'

    riskAllocation=5000; maxBP=10; timeFreq=3; cycl=6; orderType=0; benchmarkA="QQQ"; benchmarkB="SPY"; symbolWeights=10; bidGate=0; askGate=0;
    tickerItrA=['FNGU','TMO','ELV','DDS','GS','TSLA','NFLX','INSP','PANW','PLPC','FIVE','FICO','ZBRA','ASML','SMCI','TMV','URI','FNGU','SPOT','MSCI','EQIX','MSTR','MELI','PH','ACN','ADBE','ADSK','ALB','ALGN','ALNY','AMD','AMP','AMT','ANET','ANSS','AON','APD','ARGX','ASML','AVGO','AZO','BA','BDX','BIDU','BIIB','BILL','BKNG','BLK','MPWR','BURL','CAR','CAT','CDNS','CELH','CHTR','CI','CMG','CMI','COIN','COST','CRWD','CSL','CTAS','CVNA'];
    
    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return md.stat.prev_close>20.00 and md.stat.atr>5 and md.stat.avol>400000;
        # return symbol in Gr8Script5f807358d61f415cb94736d3f374db21.tickerItrA;
        # return md.stat.prev_close>50.00 and md.stat.atr>5;
        # return symbol == 'MSTR'
        
    def __init__(self, **params):
        if('riskAllocation' in params):
            self.__class__.riskAllocation=params['riskAllocation'];
            self.__class__.maxBP=params['maxBP'];
            self.__class__.timeFreq=params['timeFreq'];
            self.__class__.cycl=params['cycl'];
            self.__class__.orderType=params['orderType'];
            self.__class__.benchmarkA=params['benchmarkA']; 
            self.__class__.benchmarkB=params['benchmarkB'];
            self.__class__.symbolWeights=params['symbolWeights'];
            self.__class__.bidGate=params['bidGate'];
            self.__class__.askGate=params['askGate'];
            pass;
    
    def on_start(self, md, order, service, account):
    
        # FILE NAMES.
        #self.filetest='\\\EQKTG02'+'\\bdincer'+self.symbol+service.time_to_string(service.system_time, '%Y-%m-%d')+".txt";
        self.filetest=service.time_to_string(service.system_time, '%Y-%m-%d')+"999BOOKS.txt";
        self.filetestB=self.symbol+service.time_to_string(service.system_time, '%Y-%m-%d')+"-RBOOK.txt";
        self.filetestC=self.symbol+service.time_to_string(service.system_time, '%Y-%m-%d')+"-TRAJECTORY_Book.txt";
        print('symbol service time.:\t', self.symbol, service.time_to_string(service.system_time, '%Y-%m-%d'), self.filetest);
        
        self.RISKUNIT=self.__class__.riskAllocation; self.POSTUNIT=self.__class__.maxBP; self.DAYTIMER=self.__class__.timeFreq; self.CYCLE=self.__class__.cycl; self.ORDERECN=self.__class__.orderType;
        self.BENCHMARKA=self.__class__.benchmarkA; self.BENCHMARKB=self.__class__.benchmarkB; self.WEIGHTEDSYMBOL=self.__class__.symbolWeights; self.DEMANDGATE=self.__class__.bidGate; self.SUPPLYGATE=self.__class__.askGate;
        
        # SYMBOL STAT INFO
        self._atr, self._avol, self._beta, self._prev_close = md.stat.atr, md.stat.avol, md.stat.beta, md.stat.prev_close;

        # SYMBOL STATUS INDICATORS
        self.safetySymbol=640;
        self.qtyStat=540;
        self.limitBP=0;
        
        # CAPITAL REGULATORS.
        self.order_quantity_max=account.buying_power/self.WEIGHTEDSYMBOL;
        self.riskAllowance=int(self.RISKUNIT);
        self.quvantity=int(self.RISKUNIT/md.stat.prev_close);
        self.qtyZero=self.quvantity;
        self.limitBP=self.order_quantity_max-account[self.symbol].position.capital_long-account[self.symbol].pending.capital_long;
        self.plFlip=self.order_quantity_max/1000;
        print('order_quantity_max / limitBP', self.order_quantity_max, self.limitBP);


        # ANALYSIS PTS.
        self.dataBook =[[],[],[],[],[],[],[],[],[]];
        self.bb1=[];
        self.bb2=[];
        self.bb3=[];

        # [IDX] COUNTERS
        self.itr=0;
        self.qCtr=0;
        self.og=[0,0,0,0,0];
        
        self.invqCR=self.DAYTIMER*1000000;
        self.allocator=0;
        self.allocated=[0];
        
        # [RB] stack COUNTERS.
        self.ID_RB1=[];
        self.RBCT=[];
        self.ID_R1=[];
        self.ID_R2=[];
        self.ID_R3=[];
        self.ID_R4=[];
        
        # [BA SPREAD] QUARTILES.
        self.gates=[];
        self.demand=[];
        self.supply=[];

        # [BOUNDS] REFERENCES.
        self.chkMin=0;
        self.chkMinPt=0;
        self.chkMax=0;
        self.chkMaxPt=0;
        self.chkHtz=0;
        self.unloadUnits=0;
        self.chkHop=[];
        
        # BENCHMARK A [QQQ] DATAPOINTS.
        self.dfQ=0.00;
        self.chkTrajectoryQ=[0.00];
        self.qqqPrior=(md[self.BENCHMARKA].stat.prev_close);
        self.qqqBid=(md[self.BENCHMARKA].L1.bid);
        self.chkTrajectoryQ.append( ((self.qqqBid-self.qqqPrior)/self.qqqPrior));
        
        # BENCHMARK B [SPY] DATAPOINTS.
        self.dfS=0.00;
        self.chkTrajectoryS=[0.00];
        self.spyPrior=(md[self.BENCHMARKB].stat.prev_close);
        self.spyBid=(md[self.BENCHMARKB].L1.bid);
        self.chkTrajectoryS.append( ((self.spyBid-self.spyPrior)/self.spyPrior));

        # SYMBOL INDEX TRAJECTORIES.
        self.midPrice=0.00;
        self.pxChg=0.00;
        self.tkrRate=[0.00];
        self.trajectoryBook=[0.00];
        self.trajectoryBid=[0.00];
        self.trajectoryChk=[];
        self.trajectoryChk.append([0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,0,0]);
        
        
        self.trajectoryAsk=[0.00];
        self.trajectoryLast=[0.00];
        self.trajectorySpread=[0.00];
        self.pxTrajectory=[0.00];
        self.rtTrajectory=[0.00];
        self.rtTrajectoryHop=[0.00];
        self.trajectorySpread[0]=(md.L1.ask-md.L1.bid);
        
        # SYSTEM TRIGGERS/ TIMERS.
        self.liquid_time = md.market_open_time + service.time_interval(minutes=5);
        self.illiquid_time = md.market_close_time - service.time_interval(minutes=45);
        print(self.liquid_time)
        print(self.illiquid_time)
        self.ptA = int((self.illiquid_time-self.liquid_time) /1000000)-300;
        self.invCTR = int( self.ptA/ (self.DAYTIMER+20));
        print(self.invCTR);
        
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=5), repeat_interval=service.time_interval(seconds=int(self.DAYTIMER+20)), timer_id="Review")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=12), timer_id = "eod_2")
        pass;
        
    def on_timer(self, event, md, order, service, account):
        #### set the limit BP for the session/symbol.

        if event.timer_id=="eod_2":
            if(account[self.symbol].position.shares<0):
                blowitOUT = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=212, allow_multiple_pending=40);
                return blowitOUT;
            else:
                return 1;
            
        # "Review" Timer.
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
            oopH = self.ID_R4_INFO(account, md);
            wrtInfo = self.buff_LCL(account, service, md);
            
            # service.write_file(self.filetest,'{}'.format(self.trajectoryChk[-1]), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
            
            # MAINTAINS A FRESH PENDING ORDER BOOK.
            if(len(account[self.symbol].pending.orders)>28):
                order.cancel(self.symbol);
                pass;
            
            
          
            # self.invCTR-=1;
            if(self.ID_R4[-1][13]==1 or self.ID_R4[-1][21]==1 or self.ID_R4[-1][34]>0 or self.ID_R4[-1][34]<0):
                # postOne = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=1, user_key=555, allow_multiple_pending=40);
                #self.trajectoryChk.append([0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,0,0]);
                #service.write_file(self.filetest,'{}'.format(self.trajectoryChk[-1]), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                
                pass;

            if(self.ID_R4[-1][13]==1):
                self.og[0]+=1;
                self.trajectoryChk.append([0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,0,0]);
                self.trajectoryChk[-1][0], self.trajectoryChk[-1][1], self.trajectoryChk[-1][2], self.trajectoryChk[-1][3] = self.og[0], self.symbol, self.itr, self.invCTR;
                self.trajectoryChk[-1][4], self.trajectoryChk[-1][5], self.trajectoryChk[-1][6], self.trajectoryChk[-1][7] = service.time_to_string(service.system_time), self.allocated[-1], self.trajectoryBook[-1], self.ID_R4[-1][34];
                self.trajectoryChk[-1][8], self.trajectoryChk[-1][9], self.trajectoryChk[-1][10], self.trajectoryChk[-1][11] = self.ID_R4[-1][13], self.ID_R4[-1][21], self.qtyStat, self.trajectoryChk[-1][5]-self.trajectoryChk[0][5];
                
                self.trajectoryChk[-1][12], self.trajectoryChk[-1][13], self.trajectoryChk[-1][14] = (self.trajectoryChk[-1][5]-self.trajectoryChk[0][5])/(self.trajectoryChk[0][5]+0.00001), self.allocated[-1]-self.allocated[-2], (self.allocated[-1]-self.allocated[-2])/(self.allocated[-2]+0.00001);
                
                self.trajectoryChk[-1][15]=sum(idx[12] for idx in self.trajectoryChk[-len(self.trajectoryChk):])/-len(self.trajectoryChk);
                self.trajectoryChk[-1][16]=min(idy[5] for idy in self.trajectoryChk[-len(self.trajectoryChk):]);
                
                if(self.trajectoryChk[-1][5]<self.trajectoryChk[-1][15]):
                    self.trajectoryChk[-1][17]=1;
                    pass;
                
                if(self.trajectoryChk[-1][5]==self.trajectoryChk[-1][16]):
                    self.trajectoryChk[-1][18]=1;
                    pass;
                    
                self.trajectoryChk[-1][19]=self.ID_R3[-1][9];
                self.trajectoryChk[-1][20]=self.trajectoryBook[-1]-self.trajectoryBook[-2];
                self.trajectoryChk[-1][21]=1;
                self.trajectoryChk[-1][22]=self.og[4]+self.og[3]+self.og[2]+self.og[1]+self.og[0];
                self.trajectoryChk[-1][23], self.trajectoryChk[-1][24], self.trajectoryChk[-1][25], self.trajectoryChk[-1][26] , self.trajectoryChk[-1][27] = self.og[0], self.og[1], self.og[2], self.og[3], self.og[4];
                self.trajectoryChk[-1][28]=self.trajectoryChk[0][4];
                service.write_file(self.filetest,'{}'.format(self.trajectoryChk[-1]), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                
                if(self.safetySymbol!=750):
                    postOne = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=4, user_key=999, allow_multiple_pending=40);
                    pass;
                pass;
                
            if(self.ID_R4[-1][21]==1):
                self.og[1]+=1;
                self.trajectoryChk.append([0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,0,0]);
                self.trajectoryChk[-1][0], self.trajectoryChk[-1][1], self.trajectoryChk[-1][2], self.trajectoryChk[-1][3] = self.og[1], self.symbol, self.itr, self.invCTR;
                self.trajectoryChk[-1][4], self.trajectoryChk[-1][5], self.trajectoryChk[-1][6], self.trajectoryChk[-1][7] = service.time_to_string(service.system_time), self.allocated[-1], self.trajectoryBook[-1], self.ID_R4[-1][34];
                self.trajectoryChk[-1][8], self.trajectoryChk[-1][9], self.trajectoryChk[-1][10], self.trajectoryChk[-1][11] = self.ID_R4[-1][13], self.ID_R4[-1][21], self.qtyStat, self.trajectoryChk[-1][5]-self.trajectoryChk[0][5];
                self.trajectoryChk[-1][12], self.trajectoryChk[-1][13], self.trajectoryChk[-1][14] = (self.trajectoryChk[-1][5]-self.trajectoryChk[0][5])/(self.trajectoryChk[0][5]+0.00001), self.allocated[-1]-self.allocated[-2], (self.allocated[-1]-self.allocated[-2])/(self.allocated[-2]+0.00001);
                self.trajectoryChk[-1][15]=sum(idx[12] for idx in self.trajectoryChk[-len(self.trajectoryChk):])/-len(self.trajectoryChk);
                self.trajectoryChk[-1][16]=min(idy[5] for idy in self.trajectoryChk[-len(self.trajectoryChk):]);
                
                if(self.trajectoryChk[-1][5]<self.trajectoryChk[-1][15]):
                    self.trajectoryChk[-1][17]=1;
                    pass;
                
                if(self.trajectoryChk[-1][5]==self.trajectoryChk[-1][16]):
                    self.trajectoryChk[-1][18]=1;
                    pass;
                    
                self.trajectoryChk[-1][19]=self.ID_R3[-1][9];
                self.trajectoryChk[-1][20]=self.trajectoryBook[-1]-self.trajectoryBook[-2];
                self.trajectoryChk[-1][21]=2;
                self.trajectoryChk[-1][22]=self.og[4]+self.og[3]+self.og[2]+self.og[1]+self.og[0];
                self.trajectoryChk[-1][23], self.trajectoryChk[-1][24], self.trajectoryChk[-1][25], self.trajectoryChk[-1][26] , self.trajectoryChk[-1][27] = self.og[0], self.og[1], self.og[2], self.og[3], self.og[4];
                self.trajectoryChk[-1][28]=self.trajectoryChk[0][4];
                
                
                service.write_file(self.filetest,'{}'.format(self.trajectoryChk[-1]), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                if(self.safetySymbol!=750):
                    # postOne = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=1, user_key=555, allow_multiple_pending=40);
                    pass;
                pass;
            
            if(self.ID_R4[-1][34]>0):
                self.og[2]+=1;
                self.trajectoryChk.append([0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,0,0]);
                self.trajectoryChk[-1][0], self.trajectoryChk[-1][1], self.trajectoryChk[-1][2], self.trajectoryChk[-1][3] = self.og[2], self.symbol, self.itr, self.invCTR;
                self.trajectoryChk[-1][4], self.trajectoryChk[-1][5], self.trajectoryChk[-1][6], self.trajectoryChk[-1][7] = service.time_to_string(service.system_time), self.allocated[-1], self.trajectoryBook[-1], self.ID_R4[-1][34];
                self.trajectoryChk[-1][8], self.trajectoryChk[-1][9], self.trajectoryChk[-1][10], self.trajectoryChk[-1][11] = self.ID_R4[-1][13], self.ID_R4[-1][21], self.qtyStat, self.trajectoryChk[-1][5]-self.trajectoryChk[0][5];
                self.trajectoryChk[-1][12], self.trajectoryChk[-1][13], self.trajectoryChk[-1][14] = (self.trajectoryChk[-1][5]-self.trajectoryChk[0][5])/(self.trajectoryChk[0][5]+0.00001), self.allocated[-1]-self.allocated[-2], (self.allocated[-1]-self.allocated[-2])/(self.allocated[-2]+0.00001);
                self.trajectoryChk[-1][15]=sum(idx[12] for idx in self.trajectoryChk[-len(self.trajectoryChk):])/-len(self.trajectoryChk);
                self.trajectoryChk[-1][16]=min(idy[5] for idy in self.trajectoryChk[-len(self.trajectoryChk):]);
                
                if(self.trajectoryChk[-1][5]<self.trajectoryChk[-1][15]):
                    self.trajectoryChk[-1][17]=1;
                    pass;
                
                if(self.trajectoryChk[-1][5]==self.trajectoryChk[-1][16]):
                    self.trajectoryChk[-1][18]=1;
                    pass;
                    
                self.trajectoryChk[-1][19]=self.ID_R3[-1][9];
                self.trajectoryChk[-1][20]=self.trajectoryBook[-1]-self.trajectoryBook[-2];
                self.trajectoryChk[-1][21]=3;
                self.trajectoryChk[-1][22]=self.og[4]+self.og[3]+self.og[2]+self.og[1]+self.og[0];
                self.trajectoryChk[-1][23], self.trajectoryChk[-1][24], self.trajectoryChk[-1][25], self.trajectoryChk[-1][26] , self.trajectoryChk[-1][27] = self.og[0], self.og[1], self.og[2], self.og[3], self.og[4];
                self.trajectoryChk[-1][28]=self.trajectoryChk[0][4];
               
                service.write_file(self.filetest,'{}'.format(self.trajectoryChk[-1]), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                
                # rickey henderson condition.
                # darwin condition as well.
                
            if(len(self.ID_R4)>1):    
                if(self.ID_R4[-1][34]<self.ID_R4[-2][34]):
                    self.og[3]+=1;
                    self.trajectoryChk.append([0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,0,0]);
                    self.trajectoryChk[-1][0], self.trajectoryChk[-1][1], self.trajectoryChk[-1][2], self.trajectoryChk[-1][3] = self.og[3], self.symbol, self.itr, self.invCTR;
                    self.trajectoryChk[-1][4], self.trajectoryChk[-1][5], self.trajectoryChk[-1][6], self.trajectoryChk[-1][7] = service.time_to_string(service.system_time), self.allocated[-1], self.trajectoryBook[-1], self.ID_R4[-1][34];
                    self.trajectoryChk[-1][8], self.trajectoryChk[-1][9], self.trajectoryChk[-1][10], self.trajectoryChk[-1][11] = self.ID_R4[-1][13], self.ID_R4[-1][21], self.qtyStat, self.trajectoryChk[-1][5]-self.trajectoryChk[0][5];
                    self.trajectoryChk[-1][12], self.trajectoryChk[-1][13], self.trajectoryChk[-1][14] = (self.trajectoryChk[-1][5]-self.trajectoryChk[0][5])/(self.trajectoryChk[0][5]+0.00001), self.allocated[-1]-self.allocated[-2], (self.allocated[-1]-self.allocated[-2])/(self.allocated[-2]+0.00001);
                    self.trajectoryChk[-1][15]=sum(idx[12] for idx in self.trajectoryChk[-len(self.trajectoryChk):])/-len(self.trajectoryChk);
                    self.trajectoryChk[-1][16]=min(idy[5] for idy in self.trajectoryChk[-len(self.trajectoryChk):]);

                    if(self.trajectoryChk[-1][5]<self.trajectoryChk[-1][15]):
                        self.trajectoryChk[-1][17]=1;
                        pass;

                    if(self.trajectoryChk[-1][5]==self.trajectoryChk[-1][16]):
                        self.trajectoryChk[-1][18]=1;
                        pass;

                    self.trajectoryChk[-1][19]=self.ID_R3[-1][9];
                    self.trajectoryChk[-1][20]=self.trajectoryBook[-1]-self.trajectoryBook[-2];
                    self.trajectoryChk[-1][21]=4;
                    self.trajectoryChk[-1][22]=self.og[4]+self.og[3]+self.og[2]+self.og[1]+self.og[0];
                    self.trajectoryChk[-1][23], self.trajectoryChk[-1][24], self.trajectoryChk[-1][25], self.trajectoryChk[-1][26] , self.trajectoryChk[-1][27] = self.og[0], self.og[1], self.og[2], self.og[3], self.og[4];
                    self.trajectoryChk[-1][28]=self.trajectoryChk[0][4];
                    
                    service.write_file(self.filetest,'{}'.format(self.trajectoryChk[-1]), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                    
                    if(account[self.symbol].position.shares<0):
                        demitDosDos=order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=2, user_key=350, allow_multiple_pending=40);
                        pass;
                    pass;
                pass;
                
                
    def chkINFO(self, md):
        self.itr+=1;
        self.RBCT.append(0);
        self.chkHop.append([0.00,0.00,0.00]);
        self.midPrice=0.00;
        self.pxChg=0.00;
        self.gates.append([0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00]);
        self.ID_RB1.append([0.00,0.00,0.00,0.00,0,0,0,0,0,0,0]);
        self.ID_R3.append([0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]);
        self.ID_R4.append([0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]);
        
        self.demand.append([self.DEMANDGATE, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0]);
        self.supply.append([self.SUPPLYGATE, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0]);
        self.qqqBid=(md[self.BENCHMARKA].L1.bid);
        self.spyBid=(md[self.BENCHMARKB].L1.bid);
        self.chkMktSystem=1;
        self.midPrice=((md.L1.ask+md.L1.bid+md.L1.last)/3);
        self.pxChg=((self.midPrice - self._prev_close)/ self._prev_close);
        self.trajectoryBook.append(self.midPrice);
        self.tkrRate.append(self.pxChg);
        self.trajectoryBid.append(md.L1.bid);
        self.trajectoryAsk.append(md.L1.ask);
        self.trajectoryLast.append(md.L1.last);
        self.trajectorySpread.append(md.L1.ask-md.L1.bid);
        self.chkTrajectoryQ.append(((md[self.BENCHMARKA].L1.bid) - self.qqqPrior + 0.000001) /self.qqqPrior );
        self.chkTrajectoryS.append(((md[self.BENCHMARKB].L1.bid) - self.spyPrior + 0.000001) /self.spyPrior );
        self.dfQ=self.pxChg-self.chkTrajectoryQ[-1];
        self.dfS=self.pxChg-self.chkTrajectoryS[-1];
        self.pxTrajectory.append(self.midPrice);
        self.rtTrajectory.append(0.00);
        self.rtTrajectoryHop.append(0.00);
        self.ID_R4[-1][18]=md.L1.core_acc_volume;
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
            self.gates[-1][2]=(self.gates[-1][1]*2);
            self.gates[-1][3]=(self.gates[-1][1]*3);
            self.gates[-1][4]=self.trajectorySpread[-1];           
            self.gates[-1][12]=(self.gates[-1][4]+self.gates[-1][1]);
            self.gates[-1][13]=(self.gates[-1][4]+self.gates[-1][2]);
            self.gates[-1][14]=(self.gates[-1][4]+self.gates[-1][3]);
            self.gates[-1][15]=(self.gates[-1][4]*2)
            
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
                            
            # SWITCHED                
            if(self.gates[-1][11]<self.gates[-2][11]):
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
            # SWITCHED
            if(self.ID_R1[-1]<self.ID_R1[-2]):
                self.ID_RB1[-1][1]=1;
                # IF NEG_AVG_RATE
                
                if(len(self.allocated)>5 and self.ID_RB1[-1][4]==1):
                    self.ID_RB1[-1][7]=1;
                    
                    # SWITCHED GATES
                    if(self.allocated[-1]<0 and self.gates[-1][5]<0):
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
            # SWICHED. CHK IF R1 MOTION IS NEGATIVE.
            if(self.ID_R2[-1]<self.ID_R2[-2]):
                self.ID_RB1[-1][0]=1;
                # CHK GATES NEGATIVE.
                
                if(len(self.allocated)>5 and self.ID_RB1[-1][4]==1):
                    # SET [5] TO 1.
                    self.ID_RB1[-1][5]=1;
                    # SWITCH
                    if(self.allocated[-1]<0):
                        #increment.
                        self.RBCT[-1]+=1;
                        # SET [6] TO 1.
                        self.ID_RB1[-1][6]=1;
                        pass;
                    pass;
                    
                elif(len(self.allocated)>5 and self.ID_RB1[-1][4]==0):
                    # UPDATED GATE CONDITION.
                    self.ID_RB1[-1][9]=1;
                    # SWITCH
                    if(self.allocated[-1]<0 and self.trajectoryBook[-1]>0):
                        #increment.
                        self.RBCT[-1]+=1;
                        # SET [10] TO 1.
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
                 ## chk no SWITCH
                self.ID_R3[-1][0]=self.ID_R1[-1]-1;
                pass;
            
            ## chk SWITCH
            if(self.ID_R3[-1][0]<self.ID_R3[-2][0]):
                
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
        
    def ID_R4_INFO(self, account, md):
    
        if(len(self.ID_R1)>1):
            self.ID_R4[-1][0]=self.ID_R4[-1][18]-self.ID_R4[-2][18];
            self.ID_R4[-1][1]=self.ID_R4[-1][0]/self._avol;
            self.ID_R4[-1][2]=(self.ID_R4[-1][0]*self.invCTR)+md.L1.core_acc_volume;
            
            if(self.ID_R4[-1][2]<self._avol):
                self.ID_R4[-1][3]=1;
                self.ID_R4[-1][4]=self.ID_R4[-2][4]+1;
                pass;
            else:
                self.ID_R4[-1][4]=self.ID_R4[-2][4];
                pass;
                
            if(self.ID_R4[-1][3]==0):
                self.ID_R4[-1][5]=self.ID_R4[-2][5]+1;
                pass;
            else:
                self.ID_R4[-1][5]=self.ID_R4[-2][5];
                pass;
                
            self.ID_R4[-1][6]=self.ID_R4[-1][4]- self.ID_R4[-1][5];
    
            if(len(self.ID_R4)>3):    
                if(self.ID_R4[-1][6]>self.ID_R4[-2][6] and self.ID_R4[-2][6]>self.ID_R4[-3][6]):
                    self.ID_R4[-1][7]=0;
                    pass;
                else:
                    self.ID_R4[-1][7]=self.ID_R4[-2][7]+1;
                    pass;
                pass;    
                
            if(self.ID_R4[-1][7]>self.ID_R4[-2][7]):
                self.ID_R4[-1][8]=0;
                self.ID_R4[-1][9]=1;
                pass;
            else:
                self.ID_R4[-1][8]=1;
                self.ID_R4[-1][9]=0;
                pass;
           
            self.ID_R4[-1][10]=self.ID_R4[-1][5]+self.allocator;
            self.ID_R4[-1][11]=self.ID_R4[-1][10]-self.ID_R4[-2][10];
            
            if(self.ID_R4[-1][10]!=0):
                self.ID_R4[-1][12]=self.ID_R4[-1][11]/self.ID_R4[-1][10];
                pass;
                
            if(self.ID_R3[-1][8]==2 and self.ID_R3[-1][9]>0):
                # TEST UNIT 1
                self.ID_R4[-1][13]=1;
                pass;

            if(self.ID_R4[-2][13]==1 or self.ID_R4[-2][14]>0):
                if(self.ID_R3[-1][8]>0):
                    self.ID_R4[-1][14]=self.ID_R4[-2][14]+1;
                    pass;
                pass;
                
            if(self.ID_R3[-1][8]>self.ID_R3[-2][8]):
                self.ID_R4[-1][15]=self.ID_R4[-2][15]+1;
                pass;

                
            if(self.ID_R4[-1][13]==1):
                self.ID_R4[-1][16]=md.L1.daily_vwap;
                # chk1
                self.ID_R4[-1][17]=1;
                pass;
                
            if(len(self.ID_R4)>20 and self.ID_R4[-1][16]>0):
                self.ID_R4[-1][19]=min(self.trajectoryBook[-20:])
                pass;
                
            if(self.ID_R4[-1][19]>self.ID_R4[-1][16]):
                self.ID_R4[-1][20]=1;
                pass;
            
            if(self.ID_R3[-1][9]==1 and self.ID_R4[-1][8]==1):
                # chk2
                self.ID_R4[-1][21]=1;
                # CALC.
                self.ID_R4[-1][22]=self.trajectoryBook[-1];
                
                self.ID_R4[-1][24]=self.ID_R4[-2][24]+1
                pass;
            if(self.ID_R4[-1][21]!=1):
                self.ID_R4[-1][24]=self.ID_R4[-2][24];
                pass;
                
            if(self.ID_R4[-1][22]>0):
                self.ID_R4[-1][23]=min(self.trajectoryBook[-20:]);
                pass;
            
            if(self.ID_R4[-1][22]>0):
                if(self.ID_R4[-1][17]==1):
                    self.ID_R4[-1][25]=0;
                    pass;
                else:
                    self.ID_R4[-1][25]=self.ID_R4[-2][25]+1;
                    pass;
            else:
                self.ID_R4[-1][25]=self.ID_R4[-2][25];
                pass;
            
            
            if(self.ID_R4[-1][25]>0 and self.ID_R4[-1][21]==0):
                self.ID_R4[-1][26]=self.ID_R4[-2][26]-1;
                pass;
            else:
                self.ID_R4[-1][26]=self.ID_R4[-1][25];
                pass;
            
            if(self.ID_R4[-1][26]<self.ID_R4[-2][26]):
                self.ID_R4[-1][27]=1;
                pass;
            else:
                self.ID_R4[-1][27]=-1;
                pass;
            
            #CTRA
            self.ID_R4[-1][28]=self.ID_R4[-1][27]+self.ID_R4[-2][28]
            
            if(self.ID_R4[-1][21]==1 and self.ID_R4[-1][28]<0):
                self.ID_R4[-1][29]=1;
                pass;
            #CTRB
            self.ID_R4[-1][30]=self.ID_R4[-1][29]+self.ID_R4[-2][30];
            
            if(self.ID_R4[-1][30]>0 and self.ID_R4[-1][28]>0 and (self.ID_R4[-2][32]+self.ID_R4[-1][30])>0):
                self.ID_R4[-1][31]=-1;
                pass;
                
            #CTRC
            self.ID_R4[-1][32]=self.ID_R4[-2][32]+self.ID_R4[-1][31];
            
            if((self.ID_R4[-1][32]+self.ID_R4[-1][30])==0):
                self.ID_R4[-1][33]=1;
                pass;
                
            self.ID_R4[-1][34]=self.ID_R4[-1][30]+self.ID_R4[-1][32];
            pass;
        return 1;
        
    def buff_LCL(self, account, service, md):
        self.invCTR-=1;
        
        self.trajectoryChk.append([0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,0,0]);
        self.trajectoryChk[-1][0], self.trajectoryChk[-1][1], self.trajectoryChk[-1][2], self.trajectoryChk[-1][3] = self.og[0], self.symbol, self.itr, self.invCTR;
        self.trajectoryChk[-1][4], self.trajectoryChk[-1][5], self.trajectoryChk[-1][6], self.trajectoryChk[-1][7] = service.time_to_string(service.system_time), self.allocated[-1], self.trajectoryBook[-1], self.ID_R4[-1][34];
        self.trajectoryChk[-1][8], self.trajectoryChk[-1][9], self.trajectoryChk[-1][10], self.trajectoryChk[-1][11] = self.ID_R4[-1][13], self.ID_R4[-1][21], self.qtyStat, self.trajectoryChk[-1][5]-self.trajectoryChk[0][5];
        
        self.trajectoryChk[-1][12], self.trajectoryChk[-1][13], self.trajectoryChk[-1][14] = (self.trajectoryChk[-1][5]-self.trajectoryChk[0][5])/(self.trajectoryChk[0][5]+0.00001), self.allocated[-1]-self.allocated[-2], (self.allocated[-1]-self.allocated[-2])/(self.allocated[-2]+0.00001);
        
        self.trajectoryChk[-1][15]=sum(idx[12] for idx in self.trajectoryChk[-len(self.trajectoryChk):])/-len(self.trajectoryChk);
        self.trajectoryChk[-1][16]=min(idy[5] for idy in self.trajectoryChk[-len(self.trajectoryChk):]);
        
        if(self.trajectoryChk[-1][5]<self.trajectoryChk[-1][15]):
            self.trajectoryChk[-1][17]=1;
            pass;
        
        if(self.trajectoryChk[-1][5]==self.trajectoryChk[-1][16]):
            self.trajectoryChk[-1][18]=1;
            pass;
            
        self.trajectoryChk[-1][19]=self.ID_R3[-1][9];
        self.trajectoryChk[-1][20]=self.trajectoryBook[-1]-self.trajectoryBook[-2];
        self.trajectoryChk[-1][21]=1;
        self.trajectoryChk[-1][22]=self.og[4]+self.og[3]+self.og[2]+self.og[1]+self.og[0];
        self.trajectoryChk[-1][23], self.trajectoryChk[-1][24], self.trajectoryChk[-1][25], self.trajectoryChk[-1][26] , self.trajectoryChk[-1][27] = self.og[0], self.og[1], self.og[2], self.og[3], self.og[4];
        self.trajectoryChk[-1][28]=self.trajectoryChk[0][4];
        service.write_file(self.filetest,'{}'.format(self.trajectoryChk[-1]), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                
        # service.write_file(self.filetest,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.itr, self.invCTR, service.time_to_string(service.system_time), service.time_to_string(service.system_time),  self.symbol, self.allocator, self.ID_R1[-1], md.L1.bid,  md.L1.ask,  md.L1.last, self.ID_R1[-1], self.ID_R2[-1], self._avol,md.L1.core_acc_volume,md.L1.acc_volume,md.L1.daily_askvol,md.L1.daily_bidvol,md.L1.daily_high,md.L1.daily_low,md.L1.daily_spread,md.L1.daily_vwap,self.midPrice,self.tkrRate[-1], self.trajectoryBook[-1],self.trajectoryBid[-1],self.trajectoryAsk[-1],self.trajectoryLast[-1],self.trajectorySpread[-1],self.pxTrajectory[-1],self.rtTrajectory[-1],self.rtTrajectoryHop[-1],self.chkHop[-1][0],self.chkHop[-1][1],self.chkHop[-1][2],self.ID_RB1[-1][0],self.ID_RB1[-1][1],self.ID_RB1[-1][2],self.ID_RB1[-1][3],self.ID_RB1[-1][4],self.ID_RB1[-1][5],self.ID_RB1[-1][6],self.ID_RB1[-1][7],self.ID_RB1[-1][8],self.ID_RB1[-1][9],self.ID_RB1[-1][10],self.ID_R3[-1][0],self.ID_R3[-1][0],self.ID_R3[-1][1],self.ID_R3[-1][2],self.ID_R3[-1][3],self.ID_R3[-1][4],self.ID_R3[-1][5],self.ID_R3[-1][6],self.ID_R3[-1][7],self.ID_R3[-1][8],self.ID_R3[-1][9], self.RBCT[-1],self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4], self.demand[-1][6], self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4], self.supply[-1][6], self.gates[-1][0], self.gates[-1][1], self.gates[-1][2],self.gates[-1][3],self.gates[-1][4],self.gates[-1][5],self.gates[-1][12],self.gates[-1][13],self.gates[-1][14],self.gates[-1][15], self.filetest, self.ID_R4[-1][0],self.ID_R4[-1][1],self.ID_R4[-1][2],self.ID_R4[-1][3],self.ID_R4[-1][4],self.ID_R4[-1][5],self.ID_R4[-1][6],self.ID_R4[-1][7],self.ID_R4[-1][8],self.ID_R4[-1][9],self.ID_R4[-1][10],self.ID_R4[-1][11],self.ID_R4[-1][12],self.ID_R4[-1][13],self.ID_R4[-1][14],self.ID_R4[-1][15],self.ID_R4[-1][16],self.ID_R4[-1][17],self.ID_R4[-1][18],self.ID_R4[-1][19],self.ID_R4[-1][20],self.ID_R4[-1][21],self.ID_R4[-1][22],self.ID_R4[-1][23],self.ID_R4[-1][24],self.ID_R4[-1][25],self.ID_R4[-1][26],self.ID_R4[-1][27],self.ID_R4[-1][28],self.ID_R4[-1][29],self.ID_R4[-1][30],self.ID_R4[-1][31],self.ID_R4[-1][32],self.ID_R4[-1][33],self.ID_R4[-1][34]), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
        pass;
        #service.write_file(self.filetestC,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.itr, self.symbol, service.time_to_string(service.system_time), service.time_to_string(service.system_time), md.L1.bid,  md.L1.ask,  md.L1.last,self.midPrice, self.pxChg, self.tkrRate[-1],  self.chkTrajectoryQ[-1], self.chkTrajectoryS[-1], self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1], self.trajectoryLast[-1], self.trajectorySpread[-1], self.pxTrajectory[-1], self.allocated[-1], self.ID_RB1[-1][0], self.ID_RB1[-1][1], self.ID_RB1[-1][4], self.ID_RB1[-1][5], self.ID_RB1[-1][6], self.ID_RB1[-1][7], self.ID_RB1[-1][8], self.ID_RB1[-1][9], self.ID_RB1[-1][10], self.safetySymbol, self.allocator, self.sizeAgg,self.gates[-1][0], self.gates[-1][1], self.gates[-1][2], self.gates[-1][3], self.gates[-1][4], self.gates[-1][5], self.gates[-1][6], self.gates[-1][7], self.gates[-1][8], self.gates[-1][9], self.gates[-1][10], self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4], self.demand[-1][6], self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4], self.supply[-1][6], self.chkMin, self.chkMinPt, self.chkMax, self.chkMaxPt, self.ID_R1[-1], self.chkHop[-1][0], self.chkHop[-1][1], self.chkHop[-1][2], self.chkHtz, 0,  0, 0, 0, self.ID_R3[-1][0],self.ID_R3[-1][1],self.ID_R3[-1][2], self.ID_R3[-1][3],self.ID_R3[-1][4],self.ID_R3[-1][5],self.ID_R3[-1][6],self.ID_R3[-1][7],self.ID_R3[-1][8], self.ID_R3[-1][9], self.ID_R3[-1][10], self.ID_R3[-1][11], self.ID_R3[-1][12], self.ID_R3[-1][13], self.ID_R3[-1][14], self.ID_R3[-1][15], self.ID_R3[-1][16], self.ID_R3[-1][17], account.buying_power, account[self.symbol].position.shares, account[self.symbol].position.mtm_price, account[self.symbol].unrealized_pl.entry_pl,account[self.symbol].realized_pl.entry_pl,  account[self.symbol].pending.count_long, account[self.symbol].pending.shares_long,  account[self.symbol].pending.capital_long,  account[self.symbol].pending.count_short, account[self.symbol].pending.shares_short, account[self.symbol].pending.capital_short, self.ID_R4[-1][0], self.ID_R4[-1][1], self.ID_R4[-1][2], self.ID_R4[-1][3], self.ID_R4[-1][4], self.ID_R4[-1][5], self.ID_R4[-1][6], self.ID_R4[-1][7], self.ID_R4[-1][8], self.ID_R4[-1][9], self.ID_R4[-1][10], self.ID_R4[-1][11], self.ID_R4[-1][12], self.ID_R4[-1][13], self.ID_R4[-1][14], self.ID_R4[-1][15]), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
        #service.write_file(self.filetestB,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.itr, self.symbol, service.time_to_string(service.system_time), service.time_to_string(service.system_time), md.L1.bid,  md.L1.ask,  md.L1.last,self.midPrice, self.pxChg, self.safetySymbol, self.qtyStat, self.chkHtz, self.allocator, self.sizeAgg, self.gates[-1][0], self.gates[-1][1], self.gates[-1][2], self.gates[-1][3], self.gates[-1][4], self.gates[-1][5], self.gates[-1][6], self.gates[-1][7], self.gates[-1][8], self.gates[-1][9], self.gates[-1][10], self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4], self.demand[-1][6], self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4], self.supply[-1][6], self.ID_R3[-1][8], self.ID_R3[-1][9], self.chkMin, self.chkMinPt, self.chkMax, self.chkMaxPt, event.shares, event.price, event.instruction_id, event.user_tag, account.buying_power, account[self.symbol].position.shares, self.qCtr, self.qtyZero, self.quvantity, self.ID_R4[-1][10],self.ID_R4[-1][11], self.ID_R4[-1][12], self.ID_R4[-1][13], self.ID_R4[-1][14], self.ID_R4[-1][15], self.ID_R4[-1][16], account[self.symbol].position.mtm_price, account[self.symbol].unrealized_pl.entry_pl,account[self.symbol].realized_pl.entry_pl,  account[self.symbol].pending.count_long, account[self.symbol].pending.shares_long,  account[self.symbol].pending.capital_long,  account[self.symbol].pending.count_short, account[self.symbol].pending.shares_short, account[self.symbol].pending.capital_short));
        # service.write_file(self.filetestB,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.itr, self.symbol, service.time_to_string(service.system_time), service.time_to_string(service.system_time), md.L1.bid,  md.L1.ask,  md.L1.last,self.midPrice, self.pxChg, self.tkrRate[-1],  self.chkTrajectoryQ[-1], self.chkTrajectoryS[-1], self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1], self.trajectoryLast[-1], self.trajectorySpread[-1], self.pxTrajectory[-1], self.allocated[-1], self.ID_RB1[-1][0], self.ID_RB1[-1][1], self.ID_RB1[-1][4], self.ID_RB1[-1][5], self.ID_RB1[-1][6], self.ID_RB1[-1][7], self.ID_RB1[-1][8], self.ID_RB1[-1][9], self.ID_RB1[-1][10], self.safetySymbol, self.allocator, self.sizeAgg,self.gates[-1][0], self.gates[-1][1], self.gates[-1][2], self.gates[-1][3], self.gates[-1][4], self.gates[-1][5], self.gates[-1][6], self.gates[-1][7], self.gates[-1][8], self.gates[-1][9], self.gates[-1][10], self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4], self.demand[-1][6], self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4], self.supply[-1][6], self.chkMin, self.chkMinPt, self.chkMax, self.chkMaxPt, self.ID_R1[-1], self.chkHop[-1][0], self.chkHop[-1][1], self.chkHop[-1][2], event.shares, event.price, event.instruction_id, event.user_tag, self.ID_R3[-1][0],self.ID_R3[-1][1],self.ID_R3[-1][2], self.ID_R3[-1][3],self.ID_R3[-1][4],self.ID_R3[-1][5],self.ID_R3[-1][6],self.ID_R3[-1][7],self.ID_R3[-1][8], self.ID_R3[-1][9], account.buying_power, account[self.symbol].position.shares, self.qCtr, self.qtyZero, self.quvantity, account[self.symbol].position.mtm_price, account[self.symbol].unrealized_pl.entry_pl,account[self.symbol].realized_pl.entry_pl,  account[self.symbol].pending.count_long, account[self.symbol].pending.shares_long,  account[self.symbol].pending.capital_long, account[self.symbol].pending.count_short, account[self.symbol].pending.shares_short, account[self.symbol].pending.capital_short, self.ID_R4[-1][0],self.ID_R4[-1][1], self.ID_R4[-1][2], self.ID_R4[-1][3], self.ID_R4[-1][4], self.ID_R4[-1][5], self.ID_R4[-1][6], self.ID_R4[-1][7], self.ID_R4[-1][8], self.ID_R4[-1][9], self.ID_R4[-1][10],self.ID_R4[-1][11], self.ID_R4[-1][12], self.ID_R4[-1][13], self.ID_R4[-1][14], self.ID_R4[-1][15], self.ID_R4[-1][16], self.qtyStat));
        #service.write_file(self.filetestC,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.itr, self.symbol, service.time_to_string(service.system_time), service.time_to_string(service.system_time), md.L1.bid,  md.L1.ask,  md.L1.last,self.midPrice, self.pxChg, self.tkrRate[-1],  self.chkTrajectoryQ[-1], self.chkTrajectoryS[-1], self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1], self.trajectoryLast[-1], self.trajectorySpread[-1], self.pxTrajectory[-1], self.allocated[-1], self.ID_RB1[-1][0], self.ID_RB1[-1][1], self.ID_RB1[-1][4], self.ID_RB1[-1][5], self.ID_RB1[-1][6], self.ID_RB1[-1][7], self.ID_RB1[-1][8], self.ID_RB1[-1][9], self.ID_RB1[-1][10], self.safetySymbol, self.allocator, self.sizeAgg,self.gates[-1][0], self.gates[-1][1], self.gates[-1][2], self.gates[-1][3], self.gates[-1][4], self.gates[-1][5], self.gates[-1][6], self.gates[-1][7], self.gates[-1][8], self.gates[-1][9], self.gates[-1][10], self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4], self.demand[-1][6], self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4], self.supply[-1][6], self.chkMin, self.chkMinPt, self.chkMax, self.chkMaxPt, self.ID_R1[-1], self.chkHop[-1][0], self.chkHop[-1][1], self.chkHop[-1][2], self.RBCT_PRIME[-1][0], self.RBCT_PRIME[-1][1], self.RBCT_PRIME[-1][2], self.RBCT_PRIME[-1][3], self.ID_R3[-1][0],self.ID_R3[-1][1],self.ID_R3[-1][2], self.ID_R3[-1][3],self.ID_R3[-1][4],self.ID_R3[-1][5],self.ID_R3[-1][6],self.ID_R3[-1][7],self.ID_R3[-1][8], self.ID_R3[-1][9], account.buying_power, account[self.symbol].position.shares, self.qCtr, self.qtyZero, self.quvantity, account[self.symbol].position.mtm_price, account[self.symbol].unrealized_pl.entry_pl,account[self.symbol].realized_pl.entry_pl,  account[self.symbol].pending.count_long, account[self.symbol].pending.shares_long,  account[self.symbol].pending.capital_long,  account[self.symbol].pending.count_short, account[self.symbol].pending.shares_short, account[self.symbol].pending.capital_short, self.ID_R4[-1][0],self.ID_R4[-1][1], self.ID_R4[-1][2], self.ID_R4[-1][3], self.ID_R4[-1][4], self.ID_R4[-1][5], self.ID_R4[-1][6], self.ID_R4[-1][7], self.ID_R4[-1][8], self.ID_R4[-1][9], self.ID_R4[-1][10],self.ID_R4[-1][11], self.ID_R4[-1][12], self.ID_R4[-1][13], self.ID_R4[-1][14], self.ID_R4[-1][15], self.ID_R4[-1][16], self.qtyStat));  
        # service.write_file(self.filetestC,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.itr, self.symbol, service.time_to_string(service.system_time), service.time_to_string(service.system_time), md.L1.bid,  md.L1.ask,  md.L1.last,self.midPrice, self.pxChg, self.tkrRate[-1],  self.chkTrajectoryQ[-1], self.chkTrajectoryS[-1], self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1], self.trajectoryLast[-1], self.trajectorySpread[-1], self.pxTrajectory[-1], self.allocated[-1], self.ID_RB1[-1][0], self.ID_RB1[-1][1], self.ID_RB1[-1][4], self.ID_RB1[-1][5], self.ID_RB1[-1][6], self.ID_RB1[-1][7], self.ID_RB1[-1][8], self.ID_RB1[-1][9], self.ID_RB1[-1][10], self.safetySymbol, self.allocator, self.sizeAgg,self.gates[-1][0], self.gates[-1][1], self.gates[-1][2], self.gates[-1][3], self.gates[-1][4], self.gates[-1][5], self.gates[-1][6], self.gates[-1][7], self.gates[-1][8], self.gates[-1][9], self.gates[-1][10], self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4], self.demand[-1][6], self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4], self.supply[-1][6], self.chkMin, self.chkMinPt, self.chkMax, self.chkMaxPt, self.ID_R1[-1], self.chkHop[-1][0], self.chkHop[-1][1], self.chkHop[-1][2], self.chkHtz, 0,  0, 0, 0, self.ID_R3[-1][0],self.ID_R3[-1][1],self.ID_R3[-1][2], self.ID_R3[-1][3],self.ID_R3[-1][4],self.ID_R3[-1][5],self.ID_R3[-1][6],self.ID_R3[-1][7],self.ID_R3[-1][8], self.ID_R3[-1][9], self.ID_R3[-1][10], self.ID_R3[-1][11], self.ID_R3[-1][12], self.ID_R3[-1][13], self.ID_R3[-1][14], self.ID_R3[-1][15], self.ID_R3[-1][16], self.ID_R3[-1][17], account.buying_power, account[self.symbol].position.shares, account[self.symbol].position.mtm_price, account[self.symbol].unrealized_pl.entry_pl,account[self.symbol].realized_pl.entry_pl,  account[self.symbol].pending.count_long, account[self.symbol].pending.shares_long,  account[self.symbol].pending.capital_long,  account[self.symbol].pending.count_short, account[self.symbol].pending.shares_short, account[self.symbol].pending.capital_short, self.ID_R4[-1][0], self.ID_R4[-1][1], self.ID_R4[-1][2], self.ID_R4[-1][3], self.ID_R4[-1][4], self.ID_R4[-1][5], self.ID_R4[-1][6], self.ID_R4[-1][7], self.ID_R4[-1][8], self.ID_R4[-1][9], self.ID_R4[-1][10], self.ID_R4[-1][11], self.ID_R4[-1][12], self.ID_R4[-1][13], self.ID_R4[-1][14], self.ID_R4[-1][15]), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
        # self.itr, service.time_to_string(service.system_time), self.symbol,self.qCtr,self.allocator, md.L1.bid,  md.L1.ask,  md.L1.last, self.safetySymbol,self.qtyStat,self.dataBook[-1][0],self.dataBook[-1][1],self.dataBook[-1][2],self.dataBook[-1][3],self.dataBook[-1][4],self.dataBook[-1][5],self.dataBook[-1][6],self.dataBook[-1][7],self._avol,md.L1.core_acc_volume,md.L1.acc_volume,md.L1.daily_askvol,md.L1.daily_bidvol,md.L1.daily_high,md.L1.daily_low,md.L1.daily_spread,md.L1.daily_vwap,self.midPrice,self.pxChg,self.tkrRate,self.trajectoryBook[-1],self.trajectoryBid[-1],self.trajectoryAsk[-1],self.trajectoryLast[-1],self.trajectorySpread[-1],self.pxTrajectory[-1],self.rtTrajectory[-1],self.rtTrajectoryHop[-1],self.RBCT[-1],self.chkHop[-1][0],self.chkHop[-1][1],self.chkHop[-1][2],self.chkHop[-1][3],self.ID_RB1[-1][0],self.ID_RB1[-1][1],self.ID_RB1[-1][2],self.ID_RB1[-1][3],self.ID_RB1[-1][4],self.ID_RB1[-1][5],self.ID_RB1[-1][6],self.ID_RB1[-1][7],self.ID_RB1[-1][8],self.ID_RB1[-1][9],self.ID_RB1[-1][10],self.ID_R3[-1][0],self.ID_RB1[-1][1],self.ID_RB1[-1][2],self.ID_RB1[-1][3],self.ID_RB1[-1][4],self.ID_RB1[-1][5],self.ID_RB1[-1][6],self.ID_RB1[-1][7],self.ID_RB1[-1][8],self.ID_RB1[-1][9],self.ID_R4[-1][0],self.ID_R4[-1][1],self.ID_R4[-1][2],self.ID_R4[-1][3],self.ID_R4[-1][4],self.ID_R4[-1][5],self.ID_R4[-1][6],self.ID_R4[-1][7],self.ID_R4[-1][8],self.ID_R4[-1][9],self.ID_R4[-1][10],self.ID_R4[-1][11],self.ID_R4[-1][12],self.ID_R4[-1][13],self.ID_R4[-1][14],self.ID_R4[-1][15],self.ID_R4[-1][16],self.demand[-1][0],self.demand[-1][1],self.demand[-1][2],self.demand[-1][3],self.demand[-1][4],self.demand[-1][5],self.demand[-1][6],self.demand[-1][7],self.supply[-1][0],self.supply[-1][1],self.supply[-1][2],self.supply[-1][3],self.supply[-1][4],self.supply[-1][5],self.supply[-1][6],self.supply[-1][7]
