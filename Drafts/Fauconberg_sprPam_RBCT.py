from cloudquant.interfaces import Strategy
import numpy as ktgChk
import time, datetime, random

class Gr8Script17b09ac5f7834bbcba0a0f40e2eb1ec5(Strategy):
    __script_name__ = 'Fauconberg'
    
    bpRisk=5; orderType=0; cycl=6; askRTE=1.0012; pxChk=1.21; plSpr=1.0012; bpMaxLoss=-bpRisk*0.20; plUnrlRTE=bpRisk*0.0010; lclTimeFreq=3; plUpperBand=bpRisk*0.01; plLowerBand=-bpRisk*0.01; plBandMult=bpRisk*0.01;
    BENCHMARK_A="QQQ";BENCHMARK_B="SPY";
    demandBid=0; supplyAsk=0;
    dntItems=[];
    tickerItrA=['FNGU','TMO','ELV','DDS','GS','TSLA','NFLX','INSP','PANW','PLPC','FIVE','FICO','ZBRA','ASML','SMCI','TMV','URI','FNGU','SPOT','MSCI','EQIX','MSTR','MELI','PH','ACN','ADBE','ADSK','ALB','ALGN','ALNY','AMD','AMP','AMT','ANET','ANSS','AON','APD','ARGX','ASML','AVGO','AZO','BA','BDX','BIDU','BIIB','BILL','BKNG','BLK','MPWR','BURL','CAR','CAT','CDNS','CELH','CHTR','CI','CMG','CMI','COIN','COST','CRWD','CSL','CTAS','CVNA'];
    tickerItrB = ['GS','MPWR','TMO','ELV','DDS','ORLY','MSCI','EQIX','MSTR','MELI','BKNG','PH','INSP','PANW','PLPC','FIVE','AVGO','URI','FNGU','SPOT','TFX','WING','GWW','LLY','MSCI','URI','FSLR','SWAV','GUSH','REGN','PANW','FIVE','FICO','ZBRA','ASML','SMCI','TMV','LRCX','ACLS','FCNCA','CMG'];
    # tickerItrC = ['ACN','ADBE','ADSK','ALB','ALGN','ALNY','AMD','AMP','AMT','ANET','ANSS','AON','APD','ARGX','ASML','AVGO','AZO','BA','BDX','BIDU','BIIB','BILL','BKNG','BLK','BRK.A','BURL','CAR','CAT','CDNS','CELH','CHTR','CI','CMG','CMI','COIN','COST','CRWD','CSL','CTAS','CVNA','DDOG','DE','DECK','DHR','DPST','DPZ','ELF','ELV','ENPH','EPAM','EQIX','ESS','FCNCA','FDS','FICO','FNGU','FSLR','GNRC','GS','GWW','HCA','HUBB','HUBS','HUM','ICLR','IDXX','IGV','ILMN','INSP','INTU','ISRG','IT','ITW','KLAC','LII','LIN','LLY','LMT','LPLA','LRCX','LULU','MA','MCK','MCO','MDB','MDY','MELI','META','MLM','MOH','MPWR','MSCI','MSFT','MSI','MSTR','MTD','NFLX','NOC','NOW','NVDA','NVR','NXPI','ODFL','OIH','ORLY','PANW','PAYC','PEN','PH','PODD','POOL','PSA','PXD','REGN','RETA','RGEN','RH','RMD','ROK','ROKU','ROP','SAIA','SBAC','SEDG','SHW','SIMO','SMCI','SN','SNOW','SNPS','SOXX','SPGI','SPOT','STE','SYK','TDG','TDY','TEAM','TMO','TSCO','TSLA','ULTA','UNH','UPST','URI','VGT','VRTX','W','WAT','WCC','WDAY','WSO','WST','ZBRA','ZS'];
    tickerItrD = ['SAM','VMI','TYL','MUSA','BLD','BIO','RS','COO','NICE','EG','HII','KRTX','LAD','TFX','WIRE','JLL','CYBR','MEDP','GLOB','FCN','UTHR','SWAV','MKTX','MSGS','CRL','PCTY','RNR','ARCB','DUOL'];
    tickerItrE=['ACN','ADBE','ADSK','ALB','ALGN','ALNY','AMD','AMP','AMT','ANET','ANSS','AON','APD','ARGX','ASML','AVGO','AZO','BA','BDX','BIDU','BIIB','BILL','BKNG','BLK','BRK.A','BURL','CAR','CAT','CDNS','CELH','CHTR','CI','CMG','CMI','COIN','COST','CRWD','CSL','CTAS','CVNA'];
    tickerItrF=['DDOG','DE','DECK','DHR','DPST','DPZ','ELF','ELV','ENPH','EPAM','EQIX','ESS','FCNCA','FDS','FICO','FNGU','FSLR','GNRC','GS','GWW','HCA','HUBB','HUBS','HUM','ICLR','IDXX','IGV','ILMN','INSP','INTU','ISRG','IT','ITW','KLAC','LII','LIN','LLY','LMT','LPLA','LRCX'];
    tickerItrG=['LULU','MA','MCK','MCO','MDB','MDY','MELI','META','MLM','MOH','MPWR','MSCI','MSFT','MSI','MSTR','MTD','NFLX','NOC','NOW','NVDA','NVR','NXPI','ODFL','OIH','ORLY','PANW','PAYC','PEN','PH','PODD','POOL','PSA','PXD','REGN','RETA','RGEN','RH','RMD','ROK','ROKU'];
    tickerItrH=['ROP','SAIA','SBAC','SEDG','SHW','SIMO','SMCI','SN','SNOW','SNPS','SOXX','SPGI','SPOT','STE','SYK','TDG','TDY','TEAM','TMO','TSCO','TSLA','ULTA','UNH','UPST','URI','VGT','VRTX','W','WAT','WCC','WDAY','WSO','WST','ZBRA','ZS'];
     
    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        #return md.stat.prev_close>50.00 and md.stat.atr>5 and md.stat.avol>555555;
        return symbol in Gr8Script17b09ac5f7834bbcba0a0f40e2eb1ec5.tickerItrA;
        # return md.stat.prev_close>50.00 and md.stat.atr>5;
        #return symbol == 'MSTR'
        
    def __init__(self, **params):
        if('riskAllocation' in params):
            self.__class__.bpRisk=params['riskAllocation'];
            self.__class__.plUnrlRTE=self.__class__.bpRisk*params['plRiskBp'];
            self.__class__.maxCapUnit=params['maxBP'];
            self.__class__.lclTimeFreq=params['timeFreq'];
            self.__class__.cycl=params['cycl'];
            self.__class__.askRTE=params['askRTE'];
            self.__class__.plSpr=params['plRoute']; 
            self.__class__.pxChk=params['mkSpread']; 
            self.__class__.orderType=params['orderType'];
            self.__class__.BENCHMARK_A=params['benchmarkA']; 
            self.__class__.BENCHMARK_B=params['benchmarkB'];
            self.__class__.maxSymbolPart=(params['maxSymbolTrade']);
            
            self.__class__.demandBid=params['bidGate'];
            self.__class__.supplyAsk=params['askGate'];
            print('riskAllocation>>', params['riskAllocation'], '\n', 'plRiskBp>> self.__class__.bpRisk*params[plRiskBp]',\
            self.__class__.plUnrlRTE, '\n', 'timeFreq..', params['timeFreq'], '\n','cycl', params['cycl'], '\n', 'askRTE',\
            params['askRTE'],'\n','plRoute', params['plRoute'],'\n', 'mkSpread', params['mkSpread'],'\n','orderType',\
            params['orderType'],'\n', 'benchmarkA', params['benchmarkA'], '\n','benchmarkB', params['benchmarkB']);
            pass;
            
    
    def on_start(self, md, order, service, account):
        #print(self.__class__.dntItems);
        #print("A VOL", self.symbol, md.stat.avol);
        self.arrSymbol=self.__class__.maxSymbolPart;
            
        #self.filetest='\\\EQKTG02'+'\\bdincer'+self.symbol+service.time_to_string(service.system_time, '%Y-%m-%d')+".txt";
        self.filetest=self.symbol+service.time_to_string(service.system_time, '%Y-%m-%d')+"-RB.txt";
        self.filetestB=self.symbol+service.time_to_string(service.system_time, '%Y-%m-%d')+"-RBOOK.txt";
        self.filetestC=self.symbol+service.time_to_string(service.system_time, '%Y-%m-%d')+"-RBCT-Book.txt";
        print(self.symbol, service.time_to_string(service.system_time, '%Y-%m-%d'), self.filetest);
        self.dataBook =[[],[],[],[],[],[],[],[],[]];
        self.bb1=[]; self.bb2=[]; self.bb3=[]; self.pendingCycle=[]; self.cxlComplete=[]; self.adjustmentOne=[]; self.venue=1; self.procPL2=0; self.procPL21=0;
        self.mktSpread=self.__class__.plSpr;                                # params['plRoute']     
        self.mkOffer=self.__class__.pxChk;                                  # params['mkSpread']        
        self.unrlRoll=self.__class__.plUnrlRTE;                             # RISK * params['plRiskBp'] 
        self.orderECN=self.__class__.orderType;                             # 1/0
        self._atr, self._avol, self._beta, self._prev_close = md.stat.atr, md.stat.avol, md.stat.beta, md.stat.prev_close;
        self.riskUnit=self.__class__.bpRisk;
        self.quvantity=int(self.riskUnit/md.stat.prev_close);
        self.riskAllowance=int(self.riskUnit);
        self.cycle=self.__class__.cycl;
        self.dayTimer=self.__class__.lclTimeFreq;
        self.plCond=0;
        self.offerGeneric=self.__class__.askRTE;
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
        self.hopHZ=0;
        self.chkhtz=0;
        self.ID_R3=[];
        
        #limit BP
        self.limitBP=0;
        self.order_quantity_max=account.buying_power/self.arrSymbol;
        self.plFlip=self.order_quantity_max/1000;
        
        
        # COUNTER.
        self.allocator=0; self.allocated=[0];                           
        self.safetySymbol=640;
        self.benchMarkA=self.__class__.BENCHMARK_A;
        self.chkTrajectoryQ=[0.00]; self.qqqPrior=(md[self.benchMarkA].stat.prev_close); self.qqqBid=(md[self.benchMarkA].L1.bid); self.chkTrajectoryQ.append( ((self.qqqBid-self.qqqPrior)/self.qqqPrior)); self.tkrQQQ=0.00; self.dfQ=0.00;
        self.benchMarkB=self.__class__.BENCHMARK_B;
        self.chkTrajectoryS=[0.00]; self.spyPrior=(md[self.benchMarkB].stat.prev_close); self.spyBid=(md[self.benchMarkB].L1.bid); self.chkTrajectoryS.append( ((self.spyBid-self.spyPrior)/self.spyPrior)); self.tkrSPY=0.00; self.dfS=0.00;
        self.tkrRate=[0.00]; self.trajectoryBook=[0.00]; self.trajectoryBid=[0.00]; self.trajectoryAsk=[0.00]; self.trajectoryLast=[0.00]; self.trajectorySpread=[0.00]; self.pxTrajectory=[0.00];self.rtTrajectory=[0.00];self.rtTrajectoryHop=[0.00];
        self.midPrice=0.00; self.pxChg=0.00;
        self.trajectorySpread[0]=(md.L1.ask-md.L1.bid);
        self.liquid_time = md.market_open_time + service.time_interval(minutes=21)
        self.illiquid_time = md.market_close_time - service.time_interval(minutes=45)
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=10), repeat_interval=service.time_interval(seconds=self.dayTimer), timer_id="Allocate")
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=10), repeat_interval=service.time_interval(seconds=self.dayTimer+30), timer_id="Orderbook")
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=5), repeat_interval=service.time_interval(seconds=int(self.dayTimer+20)), timer_id="Review")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=45), timer_id = "eod_1")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=12), timer_id = "eod_2")
        pass;
        
    def on_timer(self, event, md, order, service, account):

        if(account[self.symbol].unrealized_pl.entry_pl>self.plFlip):
            clsUnitRisk = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=self.postUnit*10, user_key=1912, allow_multiple_pending=40);
            pass;
            

        if(event.timer_id=="Review"):
            self.itr+=1;
            self.RBCT.append(0);
            self.RBCT_PRIME.append([0.00,0.00,0.00,0.00]);
            self.chkHop.append([0.00,0.00,0.00]);
            self.midPrice=0.00; self.pxChg=0.00;
            self.gates.append([0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00]);
            self.ID_RB1.append([0.00,0.00,0.00,0.00,0,0,0,0,0,0,0]);
            self.demand.append([self.demandGate, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0]);
            self.supply.append([self.supplyGate, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0]);
            
            self.qqqBid=(md[self.benchMarkA].L1.bid);
            self.spyBid=(md[self.benchMarkB].L1.bid);
            #CHK data integrity here - then run chkMktSystem Review.
            self.chkMktSystem=1;
            self.midPrice=((md.L1.ask+md.L1.bid+md.L1.last)/3);
            self.pxChg=((self.midPrice - self._prev_close)/ self._prev_close);
            self.trajectoryBook.append(self.midPrice);
            self.tkrRate.append(self.pxChg);
            self.trajectoryBid.append(md.L1.bid);
            self.trajectoryAsk.append(md.L1.ask);
            self.trajectoryLast.append(md.L1.last);
            self.trajectorySpread.append(md.L1.ask-md.L1.bid);
            self.chkTrajectoryQ.append(((md[self.benchMarkA].L1.bid) - self.qqqPrior) /self.qqqPrior );
            self.chkTrajectoryS.append(((md[self.benchMarkB].L1.bid) - self.spyPrior) /self.spyPrior );
            self.dfQ=self.pxChg-self.chkTrajectoryQ[-1];
            self.dfS=self.pxChg-self.chkTrajectoryS[-1];
            self.pxTrajectory.append(self.midPrice);
            self.rtTrajectory.append(0.00);
            self.rtTrajectoryHop.append(0.00);
            self.ID_R3.append([0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]);
             
            # CHK PX RATE CHG.
            
            if(len(self.demand)>10 and len(self.supply)>10):
                if(self.trajectoryBook[-1]<self.trajectoryBook[-2]):
                    self.chkMin=self.trajectoryBook[-1];
                    self.chkMinPt+=1;
                    pass;
                if(self.trajectoryBook[-1]>self.trajectoryBook[-2]):
                    self.chkMax=self.trajectoryBook[-1];
                    self.chkMaxPt+=1;
                    pass;
                     
                    
                self.demand[-1][5]=self.trajectoryBid[-10:]+self.trajectoryLast[-10:]+self.trajectoryBook[-10:];
                self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4] = ktgChk.percentile(self.demand[-1][5], [ 25, 50, 75, 100]);
                self.demand[-1][6]=(self.demand[-1][1]+self.demand[-1][2]+self.demand[-1][3]+self.demand[-1][4])/4;
                self.demand[-1][7]=self.itr;
                #print(self.demand[-1]);
                self.supply[-1][5]=self.trajectoryAsk[-10:]+self.trajectoryLast[-10:]+self.trajectoryBook[-10:];
                self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4] = ktgChk.percentile(self.supply[-1][5], [ 25, 50, 75, 100]);
                self.supply[-1][6]=(self.supply[-1][1]+self.supply[-1][2]+self.supply[-1][3]+self.supply[-1][4])/4;
                self.supply[-1][7]=self.itr;
                #print(self.supply[-1]);
                pass;
            elif(len(self.demand)>3 and len(self.supply)>3):
                self.demand[-1][5]=self.trajectoryBid[-4:]+self.trajectoryLast[-4:]+self.trajectoryBook[-4:];
                self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4] = ktgChk.percentile(self.demand[-1][5], [ 25, 50, 75, 100]);
                self.demand[-1][6]=(self.demand[-1][1]+self.demand[-1][2]+self.demand[-1][3]+self.demand[-1][4])/4;
                self.demand[-1][7]=self.itr;
                # print(self.demand[-1]);
                self.supply[-1][5]=self.trajectoryAsk[-4:]+self.trajectoryLast[-4:]+self.trajectoryBook[-4:];
                self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4] = ktgChk.percentile(self.supply[-1][5], [ 25, 50, 75, 100]);
                self.supply[-1][6]=(self.supply[-1][1]+self.supply[-1][2]+self.supply[-1][3]+self.supply[-1][4])/4;
                self.supply[-1][7]=self.itr;
                # print(self.supply[-1]);
                pass;
            
            
            if(len(self.pxTrajectory)>2):
                self.chkHop[-1][-1]=self.chkHop[-2][1];
                self.pxTrajectory[-1]=(self.midPrice-self.trajectoryBook[-2]);
                if(self.trajectoryBook[-2]!=0 and self.rtTrajectory[-2]!=0):
                    self.rtTrajectory[-1]=self.pxTrajectory[-1]/self.trajectoryBook[-2];
                    self.rtTrajectoryHop[-1]=self.rtTrajectory[-1]/self.rtTrajectory[-2];
                    pass;
                else:
                    # self.trajectoryBook[-1]=0.00001;
                    self.rtTrajectory[-1]=0.00001;
                    self.rtTrajectoryHop[-1]=0.000001;
                    pass;
                    
                if(self.rtTrajectoryHop[-1]>self.rtTrajectoryHop[-2]):
                    self.chkHop[-1][0]=1;
                    self.chkHop[-1][1]=self.chkHop[-1][1]+1;
                    
                    self.chkHop[-1][2]=self.chkHop[-1][1]-self.chkHop[-2][1];
                
                
                    
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
            else:
                self.pxTrajectory[-1]=0;
                pass;
            
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
            else:
                self.gates[-1][6]=self.gates[-1][5];
                pass;
            
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
            self.allocated.append(self.allocator);
           
            self.ID_R1.append(self.allocated[-1]/self.itr);
            
            if(len(self.ID_R1)>1):
                if(self.ID_R1[-2]==0):
                    self.ID_R3[-1][0]=self.ID_R1[-1];
                    pass;
                else:
                    if(self.ID_R1[-1]>0 and self.ID_R1[-1]!=0):
                        self.ID_R3[-1][0]=self.ID_R1[-1]-self.ID_R1[-2]/self.ID_R1[-1];
                        pass;
                    else:
                        self.ID_R3[-1][0]=0;
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

            if(len(self.chkHop)>3):
                if(self.RBCT[-1]>self.RBCT[-2] and self.RBCT[-2]==0 and self.chkHop[-1][1]>0):
                    self.RBCT_PRIME[-1][0]=self.RBCT_PRIME[-2][0]+self.chkHop[-1][2];
                    pass;
                    
                if(self.RBCT[-1]>1):
                    self.RBCT_PRIME[-1][1]=2;
                    self.RBCT_PRIME[-1][2]=self.chkHop[-1][0];
                    pass;
                elif(self.RBCT[-1]==1):
                    self.RBCT_PRIME[-1][1]=1;
                    pass;
                elif(self.RBCT_PRIME[-1][2]>0):
                    print(self.RBCT_PRIME[-2][2]);
                    print(self.chkHop[-1][0]);
                    self.RBCT_PRIME[-1][2]=(self.RBCT_PRIME[-2][2]+self.chkHop[-1][0]);
                    pass;
                if(self.RBCT_PRIME[-1][2]>self.RBCT_PRIME[-2][2]):
                    self.RBCT_PRIME[-1][3]=1;
                    pass;
                else:
                    self.RBCT_PRIME[-1][3]=0;
                    pass;
                pass;
            
            
            service.write_file(self.filetestC,'{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(self.itr, self.symbol, service.time_to_string(service.system_time), service.time_to_string(service.system_time), md.L1.bid,  md.L1.ask,  md.L1.last,self.midPrice, self.pxChg, self.tkrRate[-1],  self.chkTrajectoryQ[-1], self.chkTrajectoryS[-1], self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1], self.trajectoryLast[-1], self.trajectorySpread[-1], self.pxTrajectory[-1], self.allocated[-1], self.ID_RB1[-1][0], self.ID_RB1[-1][1], self.ID_RB1[-1][4], self.ID_RB1[-1][5], self.ID_RB1[-1][6], self.ID_RB1[-1][7], self.ID_RB1[-1][8], self.ID_RB1[-1][9], self.ID_RB1[-1][10], self.safetySymbol, self.allocator, self.sizeAgg,self.gates[-1][0], self.gates[-1][1], self.gates[-1][2], self.gates[-1][3], self.gates[-1][4], self.gates[-1][5], self.gates[-1][6], self.gates[-1][7], self.gates[-1][8], self.gates[-1][9], self.gates[-1][10], self.demand[-1][1], self.demand[-1][2], self.demand[-1][3], self.demand[-1][4], self.demand[-1][6], self.supply[-1][1], self.supply[-1][2], self.supply[-1][3], self.supply[-1][4], self.supply[-1][6], self.chkMin, self.chkMinPt, self.chkMax, self.chkMaxPt, self.ID_R1[-1], self.chkHop[-1][0], self.chkHop[-1][1], self.chkHop[-1][2], self.RBCT_PRIME[-1][0], self.RBCT_PRIME[-1][1], self.RBCT_PRIME[-1][2], self.RBCT_PRIME[-1][3], self.ID_R3[-1][0],self.ID_R3[-1][1],self.ID_R3[-1][2], self.ID_R3[-1][3],self.ID_R3[-1][4],self.ID_R3[-1][5],self.ID_R3[-1][6],self.ID_R3[-1][7],self.ID_R3[-1][8], self.ID_R3[-1][9], account.buying_power, account[self.symbol].position.shares, account[self.symbol].position.mtm_price, account[self.symbol].unrealized_pl.entry_pl,account[self.symbol].realized_pl.entry_pl,  account[self.symbol].pending.count_long, account[self.symbol].pending.shares_long,  account[self.symbol].pending.capital_long,  account[self.symbol].pending.count_short, account[self.symbol].pending.shares_short, account[self.symbol].pending.capital_short), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
            
            
            if(len(self.allocated)>5 and self.allocated[-2]>1):
                if(self.allocated[-1]>self.allocated[-2]>self.allocated[-3]):
                    self.safetySymbol=640; self.orderECN==1; self.quvantity+=1; return 1;
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
            
        if(self.allocator<0):
            print(self.symbol, service.time_to_string(service.system_time, '%Y-%m-%d '), service.time_to_string(service.system_time), 'GATE');
            print(self.midPrice, self.pxChg, self.tkrRate[-1], self.chkTrajectoryQ[-1], self.chkTrajectoryS[-1], self.trajectoryBook[-1], self.trajectoryBid[-1], self.trajectoryAsk[-1], self.trajectoryLast[-1], self.trajectorySpread[-1], self.pxTrajectory[-1], self.allocated[-1], self.allocator);
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
            self.safetySymbol=640;
            pass;
        else:
            return 0;
        
        def procPL_3(sprPam, qty):
            Bpx=md.L1.bid; Apx=md.L1.ask; Lpx=md.L1.last;
            if(sprPam==3): qbA=Apx-((Apx-Bpx)/sprPam); reRack=max(Lpx, qbA)+self.mkOffer;pass;
            elif(sprPam==4): qbA=Apx-((Apx-Bpx)/sprPam); reRack=max(Lpx, qbA)+self.mkOffer;pass;
            reRack=int(reRack*10000 + 0.001) / 10000.0;
            self.venue+=1;
            if(self.venue%2==1 and qty>0):
                newLevel = order.algo_sell(self.symbol, algorithm='09528d6b-7d4f-4cc2-8611-8bbecb33785c', intent='decrease', order_quantity=qty, price=reRack, user_key=112, allow_multiple_pending=40);
                self.sizeAgg-=qty;
                pass;
            elif(self.venue%2==0 and qty>0):
                newLevel = order.algo_sell(self.symbol, algorithm='f8328375-d95c-4c10-aa7e-0c7fecf13336', intent='decrease', order_quantity=qty, price=reRack, user_key=112, allow_multiple_pending=40);
                self.sizeAgg-=qty;
                pass;
            self.procPL21=0; self.procPL2=0;
            return self.sizeAgg, self.procPL21, self.procPL2;
                    
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
        
        
        if(event.timer_id=="Orderbook"):
        
            if(self.procPL21==3 or self.procPL2==4):
                chkPxA=0;
                sizeUP=0;
                for chkUnit in self.adjustmentOne:
                    if(chkUnit[3]==112):
                        sizeUP-=chkUnit[1];
                        pass;
                    self.adjustmentOne.pop(chkPxA); 
                    chkPxA+=1;
                
                if(account[self.symbol].position.shares>0):
                    if(self.procPL21==3): procPL_3(3, self.sizeAgg); return;
                    elif(self.procPL2==4): procPL_3(4, self.sizeAgg); return;
                    pass;
                    
            procPL_1 = procPL_1();
            return;
        
        if event.timer_id=="eod_1":
            if(len(account[self.symbol].pending.orders)>0):
                order.cancel(self.symbol);pass;
            else: return 1;
            
        if event.timer_id=="eod_2":
            if(account[self.symbol].position.shares>0):
                closeInventory = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=account[self.symbol].position.shares, user_key=113, allow_multiple_pending=40)
                return closeInventory;
            else: return 1;
                
        if(event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time and self.allocator>1 and self.RBCT_PRIME[-1][3]==1 and self.postUnit>0):
        
            if(self.ID_RB1[-1][6]==1):
                self.marketDepth[0][0]+=1;
                postBB = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=self.postUnit, user_key=212, allow_multiple_pending=40);
                postB = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.postUnit, price=self.demand[-1][self.demandGate], user_key=212, allow_multiple_pending=40);
                pass;
            elif(self.ID_RB1[-1][8]==1):
                self.marketDepth[1][0]+=1;
                postCC = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=self.postUnit, user_key=212, allow_multiple_pending=40);
                postC = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.postUnit, price=self.demand[-1][self.demandGate], user_key=212, allow_multiple_pending=40);
                pass;
            elif(self.ID_RB1[-1][10]==1):
                self.marketDepth[2][0]+=1;
                postD = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=self.postUnit, price=self.demand[-2][self.demandGate], user_key=212, allow_multiple_pending=40);
                postDD = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=self.postUnit, user_key=212, allow_multiple_pending=40);
                pass;
            pass;
            

        if(event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time and self.allocator>1 and self.ID_R3[-1][9]==0):
                
            if(account[self.symbol].position.shares>0):
                demitRisk = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=self.postUnit, user_key=113, allow_multiple_pending=40);
                return;
            
            if(account[self.symbol].position.shares<0):
                demitRisk =  order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=self.postUnit, user_key=114, allow_multiple_pending=40);
                return;
            
        if(event.timestamp>self.liquid_time and event.timestamp<self.illiquid_time and self.allocator>1 and self.ID_R3[-1][9]==1):
            if(account[self.symbol].position.shares<0):
                demitRisk = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=115, allow_multiple_pending=40);
                return;
                
            # LINE 538: RBCT_PRIME TO ALLOCATOR.
            print('RBCT_PRIME r3 ALLOCATOR.:', self.symbol, service.time_to_string(service.system_time), self.midPrice);
            
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
                            if(dmp>self.cycle and abs(account[self.symbol].position.capital_long)<self.riskAllowance*10 and len(account[self.symbol].pending.orders)<10 and self.quvantity>0):
                                if(len(account[self.symbol].pending.orders)>6):
                                    self.orderECN=1;
                                    pass;
                                    
                                if(self.orderECN==1 and abs(account[self.symbol].position.capital_long)<self.riskAllowance*5):
                                    self.orderECN=0;
                                    zeroPx = min(md.L1.bid, md.L1.last, md.L1.ask) + 0.01;
                                    bidQty = int(self.quvantity)+1;
                                    maxQty = self.order_quantity_max;
                                    if(maxQty<1):
                                        #print('\n\n\t\t\t MAX CAP:', self.order_quantity_max);
                                        maxQty=1;
                                        pass;

                                    riskUnitZero = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=bidQty+1, price=zeroPx, user_key=111, allow_multiple_pending=40);
                                    # onePx = md.L1.ask + 0.01;
                                    # riskUnitOnePx = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=bidQty, price=onePx, user_key=111, allow_multiple_pending=40);
                                    riskUnitOne = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=min(self.quvantity, maxQty), user_key=111, allow_multiple_pending=40);
                                    return riskUnitOne;
                                    
                                else:
                                    maxQty = self.order_quantity_max;
                                    if(maxQty<1):
                                        #print('\n\n\t\t\t MAX CAP:', self.order_quantity_max);
                                        maxQty=1;
                                        pass;
                                    rPx=mkPx=min(min(idxBar.open[:-6]), min(idxBar.close[-6:]), min(idxBar.bvwap[-6:]))-(random.randint(0, 50)/10000);
                                    rPx=int((rPx*10000) + 0.001) / 10000.0;
                                    mkPx=min(min(idxBar.open[:-6]), min(idxBar.close[:-6]), min(idxBar.bvwap[:-6]))-(random.randint(0, 50)/10000);
                                    mkPx=int((mkPx*10000) + 0.001) / 10000.0;
                                    lmtOrd = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=min(self.quvantity, maxQty), price=mkPx, user_key=111, allow_multiple_pending=40);
                                    return lmtOrd;
                            else: return 0;
                        else: return 0;
                    else: return 0;
                else: return 0;
            else: return 0;
        else: return 0;
    def on_cancel(self, event, md, order, service, account):
        if(event.user_tag==112 and self.safetySymbol!=750):
            self.sizeAgg+=abs(event.shares);
            confirmed=[event.symbol, event.shares, event.price, event.user_tag];
            self.adjustmentOne.append(confirmed);
            return confirmed, self.sizeAgg;
        return 8;
    def on_fill(self, event, md, order, service, account):
        
        if(event.intent in ["increase", "init"] and service.instruction_id == event.instruction_id):
            if(event.user_tag==111):
                exitPrice=event.price*self.offerGeneric;
                # print(self.symbol, event.shares, exitPrice, self.demand[-1][6], self.demand[-1][5], self.demand[-1][4]); 
                offerInventory = order.algo_sell(event.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=event.shares, price=exitPrice, user_key=112, allow_multiple_pending=40)
                return offerInventory;
            elif(event.user_tag==212):
                 
                exitPrice=event.price*1.0036;
                #print(self.symbol, event.shares, exitPrice, self.supply[-1][6], self.supply[-1][5], self.supply[-1][4], self.supply[-1][3]); 
                packThree = order.algo_sell(event.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=event.shares, price=self.supply[-1][self.supplyGate], user_key=112, allow_multiple_pending=40)
                return packThree;
            else: return 1;
        
        if(event.intent in ["decrease", "exit"] and service.instruction_id == event.instruction_id):
            if(event.user_tag==112):
                if(abs(event.shares)==1):
                    self.marketDepth[0][1]+=1;
                    pass;
                elif(abs(event.shares)==2):
                    self.marketDepth[1][1]+=1;
                    pass;
                elif(abs(event.shares)==3):
                    self.marketDepth[2][1]+=1;
                    pass;
                return self.marketDepth;
        else: 
            return 0;
