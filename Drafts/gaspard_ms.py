# https://youtu.be/g8p22U-5yVA?t=42
from cloudquant.interfaces import Strategy, Event
import ktgfunc

class Gr8Script4bb0b98126b74dc69548d1a3825b6b23(Strategy):
    __script_name__ = 'gaspard'

    bpRisk=50000; cycl=5; askRTE=1.0026; bpMaxLoss=-bpRisk*0.20; plUnrlRTE=bpRisk*0.0010; plUpperBand=bpRisk*.01; plLowerBand=-bpRisk*.01; plBandMult=bpRisk*.01; 

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol == 'MSFT'

    def on_start(self, md, order, service, account):
        self.itr=0;
        self.dataPt=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.dataBookMS =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.dataBookMSB =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.dataBookMSC =[[],[],[],[],[],[],[],[],[],[],[],[],[]]
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=45), repeat_interval=service.time_interval(seconds=3), timer_id="Allocate")
        # ATR over 10 days based on an underlying 250 days of TR (True Range). USE TA Lib# 21 day avg vol.
        self._atr, self._avol, self._beta, self._prev_close = md.stat.atr, md.stat.avol, md.stat.beta, md.stat.prev_close;
        
        
    def on_timer(self, event, md, order, service, account):

        bidPx=md.L1.bid;
        askPx=md.L1.ask;
        lstPx=md.L1.last;
        hiPx = md.L1.daily_high;
        loPx= md.L1.daily_low;
        midPX=bidPx+((askPx-bidPx)/2);
        mdRange=loPx+((hiPx-loPx)/2);
        lstBid=lstPx+(lstPx-bidPx);
        lstAsk=lstPx+(lstPx-askPx);
        lstMid=lstPx+(lstPx-midPX);
        self.dataPt.append([self.symbol, 0, self.itr, md.L1.exchange, md.L1.ask_exchange, md.L1.bid_exchange, lstPx, bidPx, askPx, hiPx, loPx,  self._prev_close, md.L1.closing_trade, self._atr, hiPx-loPx, askPx-bidPx, midPX, mdRange,lstBid,lstAsk,lstMid])

        barA=md.bar.minute(start=-32, end=None, include_empty=False, include_extended=True, bar_size=1, today_only=True)
        barPoints=[0.00] * 221
        rangeMS = min(len(barA.timestamp), len(barA.askvol), len(barA.bidvol), len(barA.bvwap), len(barA.close), len(barA.count), len(barA.high), len(barA.low), len(barA.open), len(barA.spread), len(barA.volume))
        
        for idx in range(0, rangeMS, 1):
            self.dataBookMS.append(barPoints);
            self.dataBookMS[idx][0]=self.symbol;
            self.dataBookMS[idx][1]=32;
            self.dataBookMS[idx][2]=self.itr;
            self.dataBookMS[idx][3]=barA.timestamp[idx];
            self.dataBookMS[idx][4]= barA.askvol[idx];
            self.dataBookMS[idx][5]=barA.bidvol[idx]; 
            self.dataBookMS[idx][6]=barA.bvwap[idx];
            self.dataBookMS[idx][7]=barA.close[idx];
            self.dataBookMS[idx][8]=barA.open[idx];
            self.dataBookMS[idx][9]=barA.high[idx];
            self.dataBookMS[idx][10]=barA.low[idx];
            self.dataBookMS[idx][11]=barA.count[idx];
            self.dataBookMS[idx][12]=barA.spread[idx];
            self.dataBookMS[idx][13]=barA.volume[idx];
            self.dataBookMS[idx][14]=barA.high[idx]-barA.low[idx];
            self.dataBookMS[idx][15]=barA.close[idx]-barA.open[idx];
            self.dataBookMS[idx][16]=max(barA.bvwap[idx], barA.close[idx], barA.open[idx], barA.high[idx]);
            self.dataBookMS[idx][17]=self.dataPt[-1][7];
            self.dataBookMS[idx][28]=self.dataPt[-1][6];
            self.dataBookMS[idx][39]=self.dataPt[-1][8];
            self.dataBookMS[idx][51]=self.dataPt[-1][16];
            self.dataBookMS[idx][62]=self.dataPt[-1][15];
            self.dataBookMS[idx][73]=self.dataPt[-1][9];
            self.dataBookMS[idx][84]=self.dataPt[-1][10];
            self.dataBookMS[idx][95]=self.dataPt[-1][14];        
            self.dataBookMS[idx][106]=self.dataPt[-1][17];  
            self.dataBookMS[idx][117]=self.dataPt[-1][18];  
            self.dataBookMS[idx][128]=self.dataPt[-1][19];
            self.dataBookMS[idx][139]=self.dataPt[-1][20];
            
            if(idx>9):
                chkBid=[];chkLst=[];chkAsk=[];chkMid=[];chkSpr=[];chkHi=[];chkLo=[];chkHL=[];mdRange=[];lastBid=[];lastAsk=[];lastMid=[];
                chkBid.append(self.dataPt[-1][7]);
                self.dataBookMS[idx][18]=self.dataPt[-2][7];chkBid.append(self.dataPt[-2][7]);
                self.dataBookMS[idx][19]=self.dataPt[-3][7];chkBid.append(self.dataPt[-3][7]);
                self.dataBookMS[idx][20]=self.dataPt[-4][7];chkBid.append(self.dataPt[-4][7]);
                self.dataBookMS[idx][21]=self.dataPt[-5][7];chkBid.append(self.dataPt[-5][7]);
                self.dataBookMS[idx][22]=self.dataPt[-6][7];chkBid.append(self.dataPt[-6][7]);
                self.dataBookMS[idx][23]=self.dataPt[-7][7];chkBid.append(self.dataPt[-7][7]);
                self.dataBookMS[idx][24]=self.dataPt[-8][7];chkBid.append(self.dataPt[-8][7]);
                self.dataBookMS[idx][25]=self.dataPt[-9][7];chkBid.append(self.dataPt[-9][7]);
                self.dataBookMS[idx][26]=max(chkBid)
                self.dataBookMS[idx][27]=min(chkBid)
                chkLst.append(self.dataPt[-1][6]);
                self.dataBookMS[idx][29]=self.dataPt[-2][6];chkLst.append(self.dataPt[-2][6]);
                self.dataBookMS[idx][30]=self.dataPt[-3][6];chkLst.append(self.dataPt[-3][6]);
                self.dataBookMS[idx][31]=self.dataPt[-4][6];chkLst.append(self.dataPt[-4][6]);
                self.dataBookMS[idx][32]=self.dataPt[-5][6];chkLst.append(self.dataPt[-5][6]);
                self.dataBookMS[idx][33]=self.dataPt[-6][6];chkLst.append(self.dataPt[-6][6]);
                self.dataBookMS[idx][34]=self.dataPt[-7][6];chkLst.append(self.dataPt[-7][6]);
                self.dataBookMS[idx][35]=self.dataPt[-8][6];chkLst.append(self.dataPt[-8][6]);
                self.dataBookMS[idx][36]=self.dataPt[-9][6];chkLst.append(self.dataPt[-9][6]);
                self.dataBookMS[idx][37]=max(chkLst)
                self.dataBookMS[idx][38]=min(chkLst)
                chkAsk.append(self.dataPt[-1][8]);
                self.dataBookMS[idx][40]=self.dataPt[-2][8];chkAsk.append(self.dataPt[-2][8]);
                self.dataBookMS[idx][41]=self.dataPt[-3][8];chkAsk.append(self.dataPt[-3][8]);
                self.dataBookMS[idx][42]=self.dataPt[-4][8];chkAsk.append(self.dataPt[-4][8]);
                self.dataBookMS[idx][43]=self.dataPt[-5][8];chkAsk.append(self.dataPt[-5][8]);
                self.dataBookMS[idx][44]=self.dataPt[-6][8];chkAsk.append(self.dataPt[-6][8]);
                self.dataBookMS[idx][45]=self.dataPt[-7][8];chkAsk.append(self.dataPt[-7][8]);
                self.dataBookMS[idx][46]=self.dataPt[-8][8];chkAsk.append(self.dataPt[-8][8]);
                self.dataBookMS[idx][47]=self.dataPt[-9][8];chkAsk.append(self.dataPt[-9][8]);
                self.dataBookMS[idx][48]=max(chkAsk)
                self.dataBookMS[idx][49]=min(chkAsk)
                #self.dataBookMS[idx][50]=000;
                chkMid.append(self.dataPt[-1][16])
                self.dataBookMS[idx][52]=self.dataPt[-2][16];chkMid.append(self.dataBookMS[idx][52]);
                self.dataBookMS[idx][53]=self.dataPt[-3][16];chkMid.append(self.dataBookMS[idx][53]);
                self.dataBookMS[idx][54]=self.dataPt[-4][16];chkMid.append(self.dataBookMS[idx][54]);
                self.dataBookMS[idx][55]=self.dataPt[-5][16];chkMid.append(self.dataBookMS[idx][55]);
                self.dataBookMS[idx][56]=self.dataPt[-6][16];chkMid.append(self.dataBookMS[idx][56]);
                self.dataBookMS[idx][57]=self.dataPt[-7][16];chkMid.append(self.dataBookMS[idx][57]);
                self.dataBookMS[idx][58]=self.dataPt[-8][16];chkMid.append(self.dataBookMS[idx][58]);
                self.dataBookMS[idx][59]=self.dataPt[-9][16];chkMid.append(self.dataBookMS[idx][59]);
                self.dataBookMS[idx][60]=max(chkMid)
                self.dataBookMS[idx][61]=min(chkMid)
                chkSpr.append(self.dataPt[-1][15]);
                self.dataBookMS[idx][63]=self.dataPt[-2][15];chkSpr.append(self.dataBookMS[idx][63]);
                self.dataBookMS[idx][64]=self.dataPt[-3][15];chkSpr.append(self.dataBookMS[idx][64]);
                self.dataBookMS[idx][65]=self.dataPt[-4][15];chkSpr.append(self.dataBookMS[idx][65]);
                self.dataBookMS[idx][66]=self.dataPt[-5][15];chkSpr.append(self.dataBookMS[idx][66]);
                self.dataBookMS[idx][67]=self.dataPt[-6][15];chkSpr.append(self.dataBookMS[idx][67]);
                self.dataBookMS[idx][68]=self.dataPt[-7][15];chkSpr.append(self.dataBookMS[idx][68]);
                self.dataBookMS[idx][69]=self.dataPt[-8][15];chkSpr.append(self.dataBookMS[idx][69]);
                self.dataBookMS[idx][70]=self.dataPt[-9][15];chkSpr.append(self.dataBookMS[idx][70]);
                self.dataBookMS[idx][71]=max(chkSpr)
                self.dataBookMS[idx][72]=min(chkSpr)
                chkHi.append(self.dataPt[-1][9])
                self.dataBookMS[idx][74]=self.dataPt[-2][9];chkHi.append(self.dataBookMS[idx][74]);
                self.dataBookMS[idx][75]=self.dataPt[-3][9];chkHi.append(self.dataBookMS[idx][75]);
                self.dataBookMS[idx][76]=self.dataPt[-4][9];chkHi.append(self.dataBookMS[idx][76]);
                self.dataBookMS[idx][77]=self.dataPt[-5][9];chkHi.append(self.dataBookMS[idx][77]);
                self.dataBookMS[idx][78]=self.dataPt[-6][9];chkHi.append(self.dataBookMS[idx][78]);
                self.dataBookMS[idx][79]=self.dataPt[-7][9];chkHi.append(self.dataBookMS[idx][79]);
                self.dataBookMS[idx][80]=self.dataPt[-8][9];chkHi.append(self.dataBookMS[idx][80]);
                self.dataBookMS[idx][81]=self.dataPt[-9][9];chkHi.append(self.dataBookMS[idx][81]);
                self.dataBookMS[idx][82]=max(chkHi)
                self.dataBookMS[idx][83]=min(chkHi)
                chkLo.append(self.dataPt[-1][10]);
                self.dataBookMS[idx][85]=self.dataPt[-2][10];chkLo.append(self.dataPt[-2][10]);
                self.dataBookMS[idx][86]=self.dataPt[-3][10];chkLo.append(self.dataPt[-3][10]);
                self.dataBookMS[idx][87]=self.dataPt[-4][10];chkLo.append(self.dataPt[-4][10]);
                self.dataBookMS[idx][88]=self.dataPt[-5][10];chkLo.append(self.dataPt[-5][10]);
                self.dataBookMS[idx][89]=self.dataPt[-6][10];chkLo.append(self.dataPt[-6][10]);
                self.dataBookMS[idx][90]=self.dataPt[-7][10];chkLo.append(self.dataPt[-7][10]);
                self.dataBookMS[idx][91]=self.dataPt[-8][10];chkLo.append(self.dataPt[-8][10]);
                self.dataBookMS[idx][92]=self.dataPt[-9][10];chkLo.append(self.dataPt[-9][10]);
                self.dataBookMS[idx][93]=max(chkLo)
                self.dataBookMS[idx][94]=min(chkLo)
                chkHL.append(self.dataPt[-1][14]);
                self.dataBookMS[idx][96]=self.dataPt[-2][14];chkHL.append(self.dataPt[-2][14]);
                self.dataBookMS[idx][97]=self.dataPt[-3][14];chkHL.append(self.dataPt[-3][14]);
                self.dataBookMS[idx][98]=self.dataPt[-4][14];chkHL.append(self.dataPt[-4][14]);
                self.dataBookMS[idx][99]=self.dataPt[-5][14];chkHL.append(self.dataPt[-5][14]);
                self.dataBookMS[idx][100]=self.dataPt[-6][14];chkHL.append(self.dataPt[-6][14]);
                self.dataBookMS[idx][101]=self.dataPt[-7][14];chkHL.append(self.dataPt[-7][14]);
                self.dataBookMS[idx][102]=self.dataPt[-8][14];chkHL.append(self.dataPt[-8][14]);
                self.dataBookMS[idx][103]=self.dataPt[-9][14];chkHL.append(self.dataPt[-9][14]);
                self.dataBookMS[idx][104]=max(chkHL)
                self.dataBookMS[idx][105]=min(chkHL)
                mdRange.append(self.dataPt[-1][17]);
                self.dataBookMS[idx][107]=self.dataPt[-2][17];mdRange.append(self.dataPt[-2][17]);
                self.dataBookMS[idx][108]=self.dataPt[-3][17];mdRange.append(self.dataPt[-3][17]);
                self.dataBookMS[idx][109]=self.dataPt[-4][17];mdRange.append(self.dataPt[-4][17]);
                self.dataBookMS[idx][110]=self.dataPt[-5][17];mdRange.append(self.dataPt[-5][17]);
                self.dataBookMS[idx][111]=self.dataPt[-6][17];mdRange.append(self.dataPt[-6][17]);
                self.dataBookMS[idx][112]=self.dataPt[-7][17];mdRange.append(self.dataPt[-7][17]);
                self.dataBookMS[idx][113]=self.dataPt[-8][17];mdRange.append(self.dataPt[-8][17]);
                self.dataBookMS[idx][114]=self.dataPt[-9][17];mdRange.append(self.dataPt[-9][17]);
                self.dataBookMS[idx][115]=max(mdRange)
                self.dataBookMS[idx][116]=min(mdRange)
                lastBid.append(self.dataPt[-1][18])
                self.dataBookMS[idx][118]=self.dataPt[-2][18];lastBid.append(self.dataPt[-2][18]);
                self.dataBookMS[idx][119]=self.dataPt[-3][18];lastBid.append(self.dataPt[-3][18]);
                self.dataBookMS[idx][120]=self.dataPt[-4][18];lastBid.append(self.dataPt[-4][18]);
                self.dataBookMS[idx][121]=self.dataPt[-5][18];lastBid.append(self.dataPt[-5][18]);
                self.dataBookMS[idx][122]=self.dataPt[-6][18];lastBid.append(self.dataPt[-6][18]);
                self.dataBookMS[idx][123]=self.dataPt[-7][18];lastBid.append(self.dataPt[-7][18]);
                self.dataBookMS[idx][124]=self.dataPt[-8][18];lastBid.append(self.dataPt[-8][18]);
                self.dataBookMS[idx][125]=self.dataPt[-9][18];lastBid.append(self.dataPt[-9][18]);
                self.dataBookMS[idx][126]=max(lastBid)
                self.dataBookMS[idx][127]=min(lastBid)
                lastAsk.append(self.dataPt[-1][19])
                self.dataBookMS[idx][129]=self.dataPt[-2][19];lastAsk.append(self.dataPt[-2][19]);
                self.dataBookMS[idx][130]=self.dataPt[-3][19];lastAsk.append(self.dataPt[-3][19]);
                self.dataBookMS[idx][131]=self.dataPt[-4][19];lastAsk.append(self.dataPt[-4][19]);
                self.dataBookMS[idx][132]=self.dataPt[-5][19];lastAsk.append(self.dataPt[-5][19]);
                self.dataBookMS[idx][133]=self.dataPt[-6][19];lastAsk.append(self.dataPt[-6][19]);
                self.dataBookMS[idx][134]=self.dataPt[-7][19];lastAsk.append(self.dataPt[-7][19]);
                self.dataBookMS[idx][135]=self.dataPt[-8][19];lastAsk.append(self.dataPt[-8][19]);
                self.dataBookMS[idx][136]=self.dataPt[-9][19];lastAsk.append(self.dataPt[-9][19]);
                self.dataBookMS[idx][137]=max(lastAsk)
                self.dataBookMS[idx][138]=min(lastAsk)
                lastMid.append(self.dataPt[-1][20])
                self.dataBookMS[idx][140]=self.dataPt[-2][20];lastMid.append(self.dataPt[-2][20]);
                self.dataBookMS[idx][141]=self.dataPt[-3][20];lastMid.append(self.dataPt[-3][20]);
                self.dataBookMS[idx][142]=self.dataPt[-4][20];lastMid.append(self.dataPt[-4][20]);
                self.dataBookMS[idx][143]=self.dataPt[-5][20];lastMid.append(self.dataPt[-5][20]);
                self.dataBookMS[idx][144]=self.dataPt[-6][20];lastMid.append(self.dataPt[-6][20]);
                self.dataBookMS[idx][145]=self.dataPt[-7][20];lastMid.append(self.dataPt[-7][20]);
                self.dataBookMS[idx][146]=self.dataPt[-8][20];lastMid.append(self.dataPt[-8][20]);
                self.dataBookMS[idx][147]=self.dataPt[-9][20];lastMid.append(self.dataPt[-9][20]);
                self.dataBookMS[idx][148]=max(lastMid)
                self.dataBookMS[idx][149]=min(lastMid)
                
                # PUT IN COMP.
                if(self.dataPt[-1][20]==self.dataBookMS[idx][148]):
                    self.dataBookMS[idx][150]=1;
                elif(self.dataPt[-1][20]==self.dataBookMS[idx][149]):
                    self.dataBookMS[idx][151]=-1;                  
                if(self.dataPt[-1][19]==self.dataBookMS[idx][137]):
                    self.dataBookMS[idx][152]=1;
                elif(self.dataPt[-1][19]==self.dataBookMS[idx][138]):
                    self.dataBookMS[idx][153]=-1;
                if(self.dataPt[-1][18]==self.dataBookMS[idx][126]):
                    self.dataBookMS[idx][154]=1;
                elif(self.dataPt[-1][18]==self.dataBookMS[idx][127]):
                    self.dataBookMS[idx][155]=-1;
                if(self.dataPt[-1][17]==self.dataBookMS[idx][115]):
                    self.dataBookMS[idx][156]=1;
                elif(self.dataPt[-1][17]==self.dataBookMS[idx][116]):
                    self.dataBookMS[idx][157]=-1;
                if(self.dataPt[-1][14]==self.dataBookMS[idx][104]):
                    self.dataBookMS[idx][158]=1;
                elif(self.dataPt[-1][14]==self.dataBookMS[idx][105]):
                    self.dataBookMS[idx][159]=-1;
                if(self.dataPt[-1][10]==self.dataBookMS[idx][93]):
                    self.dataBookMS[idx][160]=1;
                elif(self.dataPt[-1][10]==self.dataBookMS[idx][94]):
                    self.dataBookMS[idx][161]=-1; 
                if(self.dataPt[-1][9]==self.dataBookMS[idx][82]):
                    self.dataBookMS[idx][162]=1;
                elif(self.dataPt[-1][9]==self.dataBookMS[idx][83]):
                    self.dataBookMS[idx][163]=-1;
                if(self.dataPt[-1][15]==self.dataBookMS[idx][71]):
                    self.dataBookMS[idx][164]=1;
                elif(self.dataPt[-1][15]==self.dataBookMS[idx][72]):
                    self.dataBookMS[idx][165]=-1;
                if(self.dataPt[-1][16]==self.dataBookMS[idx][60]):
                    self.dataBookMS[idx][166]=1;
                elif(self.dataPt[-1][16]==self.dataBookMS[idx][61]):
                    self.dataBookMS[idx][167]=-1;
                if(self.dataPt[-1][8]==self.dataBookMS[idx][48]):
                    self.dataBookMS[idx][168]=1;
                elif(self.dataPt[-1][8]==self.dataBookMS[idx][49]):
                    self.dataBookMS[idx][169]=-1;
                if(self.dataPt[-1][6]==self.dataBookMS[idx][37]):
                    self.dataBookMS[idx][170]=1;
                elif(self.dataPt[-1][6]==self.dataBookMS[idx][38]):
                    self.dataBookMS[idx][171]=-1;
                if(self.dataPt[-1][7]==self.dataBookMS[idx][26]):
                    self.dataBookMS[idx][172]=1;
                elif(self.dataPt[-1][7]==self.dataBookMS[idx][27]):
                    self.dataBookMS[idx][173]=-1;

                chkA=[0,0,0,0,0,0,0];
                for idx in range(-1, -10, -1):
                    if(self.dataPt[idx][6]>self.dataPt[idx][7]):
                        chkA[0]+=1;
                    if(self.dataPt[idx][6]>self.dataPt[idx][9]):
                        chkA[1]+=1;
                    if(self.dataPt[idx][6]>self.dataPt[idx][16]):
                        chkA[2]+=1;
                    if(self.dataPt[idx][6]>self.dataPt[idx][17]):
                        chkA[3]+=1;
                    if(self.dataPt[idx][6]>self.dataPt[idx][18]):
                        chkA[4]+=1;
                    if(self.dataPt[idx][6]>self.dataPt[idx][19]):
                        chkA[5]+=1;
                    if(self.dataPt[idx][6]>self.dataPt[idx][20]):
                        chkA[6]+=1;
                iA=0;
                for idA in range(174, 181, 1):
                    self.dataBookMS[idA]=chkA[iA];
                    iA+=1;
                    
                    
                chkB=[0,0,0,0,0,0,0,0,0,0];
                for idx in range(-1, -10, -1):
                    if(self.dataPt[idx][6]>self.dataPt[idx-1][6]):
                        chkB[0]+=1;
                    if(self.dataPt[idx][7]>self.dataPt[idx-1][7]):
                        chkB[1]+=1;
                    if(self.dataPt[idx][8]>self.dataPt[idx-1][8]):
                        chkB[2]+=1;
                    if(self.dataPt[idx][14]>self.dataPt[idx-1][14]):
                        chkB[3]+=1;
                    if(self.dataPt[idx][15]>self.dataPt[idx-1][15]):
                        chkB[4]+=1;
                    if(self.dataPt[idx][16]>self.dataPt[idx-1][16]):
                        chkB[5]+=1;
                    if(self.dataPt[idx][17]>self.dataPt[idx-1][17]):
                        chkB[6]+=1;
                    if(self.dataPt[idx][18]>self.dataPt[idx-1][18]):
                        chkB[7]+=1;  
                    if(self.dataPt[idx][19]>self.dataPt[idx-1][19]):
                        chkB[8]+=1;
                    if(self.dataPt[idx][20]>self.dataPt[idx-1][20]):
                        chkB[9]+=1;     
                        
                idB=0;
                for idBin in range(181, 191, 1):
                    self.dataBookMS[idBin]=chkB[idB];
                    idB+=1;
                
                chkC=[[0,0,0,0,0,0]] * 10
                chkC[0][0]=self.dataPt[-1][6];
                chkC[0][1]=self.dataPt[-1][6]-self.dataPt[-2][6];
                chkC[0][2]=(chkC[0][1]/chkC[0][0]);
                chkC[1][0]=self.dataPt[-1][7];
                chkC[1][1]=self.dataPt[-1][7]-self.dataPt[-2][7];
                chkC[1][2]=(chkC[1][1]/chkC[1][0]);
                chkC[2][0]=self.dataPt[-1][8];
                chkC[2][1]=self.dataPt[-1][8]-self.dataPt[-2][8];
                chkC[2][2]=(chkC[2][1]/chkC[2][0]);
                chkC[3][0]=self.dataPt[-1][14];
                chkC[3][1]=self.dataPt[-1][14]-self.dataPt[-2][14];
                chkC[3][2]=(chkC[3][1]/chkC[3][0]);
                chkC[4][0]=self.dataPt[-1][15];
                chkC[4][1]=self.dataPt[-1][15]-self.dataPt[-2][15];
                chkC[4][2]=(chkC[4][1]/chkC[4][0]); 
                chkC[5][0]=self.dataPt[-1][16];
                chkC[5][1]=self.dataPt[-1][16]-self.dataPt[-2][16];
                chkC[5][2]=(chkC[5][1]/chkC[5][0]);   
                chkC[6][0]=self.dataPt[-1][17];
                chkC[6][1]=self.dataPt[-1][17]-self.dataPt[-2][17];
                chkC[6][2]=(chkC[6][1]/chkC[6][0]);                   
                chkC[7][0]=self.dataPt[-1][18];
                chkC[7][1]=self.dataPt[-1][18]-self.dataPt[-2][18];
                chkC[7][2]=(chkC[7][1]/chkC[7][0]);
                chkC[8][0]=self.dataPt[-1][19];
                chkC[8][1]=self.dataPt[-1][19]-self.dataPt[-2][19];
                chkC[8][2]=(chkC[8][1]/chkC[8][0]);
                chkC[9][0]=self.dataPt[-1][20];
                chkC[9][1]=self.dataPt[-1][20]-self.dataPt[-2][20];
                chkC[9][2]=(chkC[9][1]/chkC[9][0]);
            
                idC=0;
                for idCin in range(191, 201, 1):
                    self.dataBookMS[idCin]=chkC[idC][2];
                    idC+=1;
                    
                for idx in range(-1, -10, -1):
                    chkC[0][3]+=self.dataPt[idx][6];
                    chkC[0][4]+=(self.dataPt[idx][6]-self.dataPt[idx-1][6]);
                    chkC[0][5]+=(chkC[0][4]/chkC[0][3]);
                    chkC[1][3]+=self.dataPt[idx][7];
                    chkC[1][4]+=(self.dataPt[idx][7]-self.dataPt[idx-1][7]);
                    chkC[1][5]+=(chkC[1][4]/chkC[1][3]);
                    chkC[2][3]+=self.dataPt[idx][8];
                    chkC[2][4]+=(self.dataPt[idx][8]-self.dataPt[idx-1][8]);
                    chkC[2][5]+=(chkC[2][4]/chkC[2][3]);
                    chkC[3][3]+=self.dataPt[idx][14];
                    chkC[3][4]+=(self.dataPt[idx][14]-self.dataPt[idx-1][14]);
                    chkC[3][5]+=(chkC[3][4]/chkC[3][3]);
                    chkC[4][3]+=self.dataPt[idx][15];
                    chkC[4][4]+=(self.dataPt[idx][15]-self.dataPt[idx-1][15]);
                    chkC[4][5]+=(chkC[4][4]/chkC[4][3]);
                    chkC[5][3]+=self.dataPt[idx][16];
                    chkC[5][4]+=(self.dataPt[idx][16]-self.dataPt[idx-1][16]);
                    chkC[5][5]+=(chkC[5][4]/chkC[5][3]);
                    chkC[6][3]+=self.dataPt[idx][17];
                    chkC[6][4]+=(self.dataPt[idx][17]-self.dataPt[idx-1][17]);
                    chkC[6][5]+=(chkC[6][4]/chkC[6][3]);
                    chkC[7][3]+=self.dataPt[idx][18];
                    chkC[7][4]+=(self.dataPt[idx][18]-self.dataPt[idx-1][18]);
                    chkC[7][5]+=(chkC[7][4]/chkC[7][3]);
                    chkC[8][3]+=self.dataPt[idx][19];
                    chkC[8][4]+=(self.dataPt[idx][19]-self.dataPt[idx-1][19]);
                    chkC[8][5]+=(chkC[8][4]/chkC[8][3]);
                    chkC[9][3]+=self.dataPt[idx][20];
                    chkC[9][4]+=(self.dataPt[idx][20]-self.dataPt[idx-1][20]);
                    chkC[9][5]+=(chkC[9][4]/chkC[9][3]

                idD=0;
                for iDc in range(201, 211, 1):
                    self.dataBookMS[iDc]=chkC[idD][5];
                    idD+=1;
                
                iE=0;
                for chkRate in range(211, 221, 1):
                    if(chkC[iE][2]>chkC[iE][5]):
                        self.dataBookMS[chkRate]=1;
                    iE+=1;
                    
        self.itr+=1;
        #barB=md.bar.minute(start=-20, end=None, include_empty=False, include_extended=True, bar_size=2, today_only=True)        
        #rangeMSB = min(len(barB.timestamp), len(barB.askvol), len(barB.bidvol), len(barB.bvwap), len(barB.close), len(barB.count), len(barB.high), len(barB.low), len(barB.open), len(barB.spread), len(barB.volume))
        #for idxB in range(0, rangeMSB, 1):
        #    self.dataBookMSB.append([self.symbol, 20,  self.itr, barB.timestamp[idxB], barB.askvol[idxB], barB.bidvol[idxB], barB.bvwap[idxB], barB.close[idxB], barB.open[idxB], barB.high[idxB], barB.low[idxB], barB.count[idxB], barB.spread[idxB], barB.volume[idxB], barB.high[idxB]-barB.low[idxB], barB.close[idxB]-barB.open[idxB], max(barB.bvwap[idxB], barB.close[idxB], barB.open[idxB], barB.high[idxB]) , self.dataPt[-1][7]])
        #    if(idxB!=0):
        #        self.dataBookMSB[idxB][17]=self.dataBookMSB[idxB][whatever] and self.dataBookMSB[idxB-1][whatever] 
        

    def on_finish(self, md, order, service, account):
        filenameDT=self.symbol+"-DT.txt"
        strLoop=self.symbol+"\n"
        for aLoop in self.dataBookMS:
            for diLoop in aLoop:
                strLoop+=diLoop+", "
            strLoop=self.symbol+"\n"
            
        service.write_file(filenameDT, '{}'.format(strLoop))

        #filenameMS=self.symbol+"-A1.txt"
        #for hLoop in self.dataBookMS:
        #    for diLoop in hLoop:
        #        service.write_file(filenameMS, '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(diLoop[0],diLoop[1],diLoop[2],diLoop[3],diLoop[4],diLoop[5],diLoop[6],diLoop[7],diLoop[8],diLoop[9],diLoop[10],diLoop[11],diLoop[12],diLoop[13],diLoop[14],diLoop[15],diLoop[16],diLoop[17]))

        #filenameMSC=self.symbol+"-A2.txt"
        #for loopLoop in self.dataBookMSB:
        #    for diLoop in loopLoop:
        #       service.write_file(filenameMSC, '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(diLoop[0],diLoop[1],diLoop[2],diLoop[3],diLoop[4],diLoop[5],diLoop[6],diLoop[7],diLoop[8],diLoop[9],diLoop[10],diLoop[11],diLoop[12],diLoop[13],diLoop[14],diLoop[15],diLoop[16],diLoop[17]))
