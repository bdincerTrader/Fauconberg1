from cloudquant.interfaces import Strategy, Event
import ktgfunc

class gaspardata(Strategy):
    __script_name__ = 'gaspardata'
    # https://www.youtube.com/watch?v=AsdG0HyLHP0   
    bpRisk=500001; cycl=5; askRTE=1.0026; bpMaxLoss=-bpRisk*0.20; plUnrlRTE=bpRisk*0.0010; plUpperBand=bpRisk*.01; plLowerBand=-bpRisk*.01; plBandMult=bpRisk*.01; 

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return symbol == 'MSCI'

    def on_start(self, md, order, service, account):
        self.itr=-1;
        self.idxLoop=-1;
        self.dataPt=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.dataBookMS =[]
        self.sections=[0.00] * 10
        self.dataBookSections =[]
        self.dataBookMSB =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.dataBookMSC =[[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.fileName=self.symbol+"1x1.txt"
        self.fileNameThree=self.symbol+"file3-1x1.txt"
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=5), repeat_interval=service.time_interval(minutes=1), timer_id="Allocate")
        # ATR over 10 days based on an underlying 250 days of TR (True Range). USE TA Lib# 21 day avg vol.
        self._atr, self._avol, self._beta, self._prev_close = md.stat.atr, md.stat.avol, md.stat.beta, md.stat.prev_close;

    def on_timer(self, event, md, order, service, account):
        self.idxLoop+=1;
        qualityCheck=0;
        bidPx=md.L1.bid;
        askPx=md.L1.ask;
        lstPx=md.L1.last;
        hiPx = md.L1.daily_high;
        loPx= md.L1.daily_low;
        midPX=max(askPx,bidPx);
        if(bidPx!=0 and askPx!=0):
            midPX=bidPx+((askPx-bidPx)/2);
        else:
            qualityCheck=1;
            
        mdRange=max(hiPx,loPx);
        if(hiPx!=0 and loPx!=0):
            mdRange=loPx+((hiPx-loPx)/2);
        else:
            qualityCheck=1;
            
        lstBid=max(lstPx,bidPx);
        if(lstPx!=0 and bidPx!=0):
            lstBid=lstPx+(lstPx-bidPx);
        else:
            qualityCheck=1;

        lstAsk=max(lstPx, askPx);
        if(lstPx!=0 and askPx!=0):
            lstAsk=lstPx+(lstPx-askPx);
        else:
            qualityCheck=1;
            
        lstMid=max(lstPx, midPX);
        if(lstPx!=0 and midPX!=0):
            lstMid=lstPx+(lstPx-midPX);
        else:
            qualityCheck=1;
            
        self.dataPt.append([self.symbol, qualityCheck, self.itr, md.L1.exchange, md.L1.ask_exchange, md.L1.bid_exchange, lstPx, bidPx, askPx, hiPx, loPx,  self._prev_close, md.L1.closing_trade, self._atr, hiPx-loPx, askPx-bidPx, midPX, mdRange,lstBid,lstAsk,lstMid])
        
        barA=md.bar.minute(start=-32, end=None, include_empty=False, include_extended=True, bar_size=1, today_only=True)
        barPoints=[0.00] * 221
        rangeMS = min(len(barA.timestamp), len(barA.askvol), len(barA.bidvol), len(barA.bvwap), len(barA.close), len(barA.count), len(barA.high), len(barA.low), len(barA.open), len(barA.spread), len(barA.volume))
        rangeM=rangeMS-1;
        rangeDT=len(self.dataPt[-1]);
        
        offset=-rangeM;
        for idx in range(0, rangeM, 1):
            self.dataBookMS.append(barPoints);
            self.dataBookSections.append(self.sections);
            self.itr+=1;
            #print(self.itr)
            #print(len(self.dataPt))
            #print(len(self.dataBookMS))
            self.dataBookMS[self.itr][0]=self.symbol;
            self.dataBookMS[self.itr][1]=idx+1;
            self.dataBookMS[self.itr][2]=self.itr;
            # print(self.dataBookMS[self.itr])

            print("STR3")
            str3=str(self.itr)+",";
            for units in self.dataBookMS[self.itr]:
                str3+=str(units)+",";
            str3+='\n';
            print(str3)
            service.write_file(self.fileNameThree,'{}'.format(str3))
            
            self.dataBookMS[self.itr][3]=barA.timestamp[idx];
            self.dataBookMS[self.itr][4]= barA.askvol[idx];
            self.dataBookMS[self.itr][5]=barA.bidvol[idx]; 
            self.dataBookMS[self.itr][6]=barA.bvwap[idx];
            self.dataBookMS[self.itr][7]=barA.close[idx];
            self.dataBookMS[self.itr][8]=barA.open[idx];
            self.dataBookMS[self.itr][9]=barA.high[idx];
            self.dataBookMS[self.itr][10]=barA.low[idx];
            self.dataBookMS[self.itr][11]=barA.count[idx];
            self.dataBookMS[self.itr][12]=barA.spread[idx];
            self.dataBookMS[self.itr][13]=barA.volume[idx];
            self.dataBookMS[self.itr][14]=barA.high[idx]-barA.low[idx];
            self.dataBookMS[self.itr][15]=barA.close[idx]-barA.open[idx];
            self.dataBookMS[self.itr][16]=max(barA.bvwap[idx], barA.close[idx], barA.open[idx], barA.high[idx]);
            #current
            self.dataBookMS[self.itr][17]=self.dataPt[-1][7];
            self.dataBookMS[self.itr][28]=self.dataPt[-1][6];
            self.dataBookMS[self.itr][39]=self.dataPt[-1][8];
            self.dataBookMS[self.itr][51]=self.dataPt[-1][16];
            self.dataBookMS[self.itr][62]=self.dataPt[-1][15];
            self.dataBookMS[self.itr][73]=self.dataPt[-1][9];
            self.dataBookMS[self.itr][84]=self.dataPt[-1][10];
            self.dataBookMS[self.itr][95]=self.dataPt[-1][14];
            self.dataBookMS[self.itr][106]=self.dataPt[-1][17];
            self.dataBookMS[self.itr][117]=self.dataPt[-1][18];
            self.dataBookMS[self.itr][128]=self.dataPt[-1][19];
            self.dataBookMS[self.itr][139]=self.dataPt[-1][20];
            
            
            
            if(self.idxLoop>10 and idx==rangeM-1):
                print('remove itr chk loop', idx, rangeM, len(self.dataBookMS), self.itr, len(self.dataPt))
                # print('databook start\n', self.dataBookMS[-1])
                chkBid=[];chkLst=[];chkAsk=[];chkMid=[];chkSpr=[];chkHi=[];chkLo=[];chkHL=[];mdRange=[];lastBid=[];lastAsk=[];lastMid=[];
                chkBid.append(self.dataPt[-1][7]);
                # print(self.dataBookMS[self.itr])
                
                
                
                self.dataBookMS[self.itr][18]=self.dataPt[-2][7];chkBid.append(self.dataPt[-2][7]);
                self.dataBookMS[self.itr][19]=self.dataPt[-3][7];chkBid.append(self.dataPt[-3][7]);
                self.dataBookMS[self.itr][20]=self.dataPt[-4][7];chkBid.append(self.dataPt[-4][7]);
                self.dataBookMS[self.itr][21]=self.dataPt[-5][7];chkBid.append(self.dataPt[-5][7]);
                self.dataBookMS[self.itr][22]=self.dataPt[-6][7];chkBid.append(self.dataPt[-6][7]);
                self.dataBookMS[self.itr][23]=self.dataPt[-7][7];chkBid.append(self.dataPt[-7][7]);
                self.dataBookMS[self.itr][24]=self.dataPt[-8][7];chkBid.append(self.dataPt[-8][7]);
                self.dataBookMS[self.itr][25]=self.dataPt[-9][7];chkBid.append(self.dataPt[-9][7]);
                self.dataBookMS[self.itr][26]=max(chkBid)
                self.dataBookMS[self.itr][27]=min(chkBid)
                chkLst.append(self.dataPt[-1][6]);
                self.dataBookMS[self.itr][29]=self.dataPt[-2][6];chkLst.append(self.dataPt[-2][6]);
                self.dataBookMS[self.itr][30]=self.dataPt[-3][6];chkLst.append(self.dataPt[-3][6]);
                self.dataBookMS[self.itr][31]=self.dataPt[-4][6];chkLst.append(self.dataPt[-4][6]);
                self.dataBookMS[self.itr][32]=self.dataPt[-5][6];chkLst.append(self.dataPt[-5][6]);
                self.dataBookMS[self.itr][33]=self.dataPt[-6][6];chkLst.append(self.dataPt[-6][6]);
                self.dataBookMS[self.itr][34]=self.dataPt[-7][6];chkLst.append(self.dataPt[-7][6]);
                self.dataBookMS[self.itr][35]=self.dataPt[-8][6];chkLst.append(self.dataPt[-8][6]);
                self.dataBookMS[self.itr][36]=self.dataPt[-9][6];chkLst.append(self.dataPt[-9][6]);
                self.dataBookMS[self.itr][37]=max(chkLst)
                self.dataBookMS[self.itr][38]=min(chkLst)
                chkAsk.append(self.dataPt[-1][8]);
                self.dataBookMS[self.itr][40]=self.dataPt[-2][8];chkAsk.append(self.dataPt[-2][8]);
                print('idx==rangeM')
                print(self.itr)
                print(self.dataPt[-2][8])
                print(self.dataPt[-3][8])
                
                self.dataBookMS[self.itr][41]=self.dataPt[-3][8];chkAsk.append(self.dataPt[-3][8]);
                self.dataBookMS[self.itr][42]=self.dataPt[-4][8];chkAsk.append(self.dataPt[-4][8]);
                self.dataBookMS[self.itr][43]=self.dataPt[-5][8];chkAsk.append(self.dataPt[-5][8]);
                self.dataBookMS[self.itr][44]=self.dataPt[-6][8];chkAsk.append(self.dataPt[-6][8]);
                self.dataBookMS[self.itr][45]=self.dataPt[-7][8];chkAsk.append(self.dataPt[-7][8]);
                self.dataBookMS[self.itr][46]=self.dataPt[-8][8];chkAsk.append(self.dataPt[-8][8]);
                self.dataBookMS[self.itr][47]=self.dataPt[-9][8];chkAsk.append(self.dataPt[-9][8]);
                self.dataBookMS[self.itr][48]=max(chkAsk)
                self.dataBookMS[self.itr][49]=min(chkAsk)
                self.dataBookMS[self.itr][50]=self.dataPt[-1][1];
                chkMid.append(self.dataPt[-1][16])
                self.dataBookMS[self.itr][52]=self.dataPt[-2][16];chkMid.append(self.dataPt[-2][16]);
                self.dataBookMS[self.itr][53]=self.dataPt[-3][16];chkMid.append(self.dataPt[-3][16]);
                self.dataBookMS[self.itr][54]=self.dataPt[-4][16];chkMid.append(self.dataPt[-4][16]);
                self.dataBookMS[self.itr][55]=self.dataPt[-5][16];chkMid.append(self.dataPt[-5][16]);
                self.dataBookMS[self.itr][56]=self.dataPt[-6][16];chkMid.append(self.dataPt[-6][16]);
                self.dataBookMS[self.itr][57]=self.dataPt[-7][16];chkMid.append(self.dataPt[-7][16]);
                self.dataBookMS[self.itr][58]=self.dataPt[-8][16];chkMid.append(self.dataPt[-8][16]);
                self.dataBookMS[self.itr][59]=self.dataPt[-9][16];chkMid.append(self.dataPt[-9][16]);
                self.dataBookMS[self.itr][60]=max(chkMid)
                self.dataBookMS[self.itr][61]=min(chkMid)
                chkSpr.append(self.dataPt[-1][15]);
                self.dataBookMS[self.itr][63]=self.dataPt[-2][15];chkSpr.append(self.dataPt[-2][15]);
                self.dataBookMS[self.itr][64]=self.dataPt[-3][15];chkSpr.append(self.dataPt[-3][15]);
                self.dataBookMS[self.itr][65]=self.dataPt[-4][15];chkSpr.append(self.dataPt[-4][15]);
                self.dataBookMS[self.itr][66]=self.dataPt[-5][15];chkSpr.append(self.dataPt[-5][15]);
                self.dataBookMS[self.itr][67]=self.dataPt[-6][15];chkSpr.append(self.dataPt[-6][15]);
                self.dataBookMS[self.itr][68]=self.dataPt[-7][15];chkSpr.append(self.dataPt[-7][15]);
                self.dataBookMS[self.itr][69]=self.dataPt[-8][15];chkSpr.append(self.dataPt[-8][15]);
                self.dataBookMS[self.itr][70]=self.dataPt[-9][15];chkSpr.append(self.dataPt[-9][15]);
                self.dataBookMS[self.itr][71]=max(chkSpr)
                self.dataBookMS[self.itr][72]=min(chkSpr)
                chkHi.append(self.dataPt[-1][9])
                self.dataBookMS[self.itr][74]=self.dataPt[-2][9];chkHi.append(self.dataPt[-2][9]);
                self.dataBookMS[self.itr][75]=self.dataPt[-3][9];chkHi.append(self.dataPt[-3][9]);
                self.dataBookMS[self.itr][76]=self.dataPt[-4][9];chkHi.append(self.dataPt[-4][9]);
                self.dataBookMS[self.itr][77]=self.dataPt[-5][9];chkHi.append(self.dataPt[-5][9]);
                self.dataBookMS[self.itr][78]=self.dataPt[-6][9];chkHi.append(self.dataPt[-6][9]);
                self.dataBookMS[self.itr][79]=self.dataPt[-7][9];chkHi.append(self.dataPt[-7][9]);
                self.dataBookMS[self.itr][80]=self.dataPt[-8][9];chkHi.append(self.dataPt[-8][9]);
                self.dataBookMS[self.itr][81]=self.dataPt[-9][9];chkHi.append(self.dataPt[-9][9]);
                self.dataBookMS[self.itr][82]=max(chkHi)
                self.dataBookMS[self.itr][83]=min(chkHi)
                chkLo.append(self.dataPt[-1][10]);
                self.dataBookMS[self.itr][85]=self.dataPt[-2][10];chkLo.append(self.dataPt[-2][10]);
                self.dataBookMS[self.itr][86]=self.dataPt[-3][10];chkLo.append(self.dataPt[-3][10]);
                self.dataBookMS[self.itr][87]=self.dataPt[-4][10];chkLo.append(self.dataPt[-4][10]);
                self.dataBookMS[self.itr][88]=self.dataPt[-5][10];chkLo.append(self.dataPt[-5][10]);
                self.dataBookMS[self.itr][89]=self.dataPt[-6][10];chkLo.append(self.dataPt[-6][10]);
                self.dataBookMS[self.itr][90]=self.dataPt[-7][10];chkLo.append(self.dataPt[-7][10]);
                self.dataBookMS[self.itr][91]=self.dataPt[-8][10];chkLo.append(self.dataPt[-8][10]);
                self.dataBookMS[self.itr][92]=self.dataPt[-9][10];chkLo.append(self.dataPt[-9][10]);
                self.dataBookMS[self.itr][93]=max(chkLo)
                self.dataBookMS[self.itr][94]=min(chkLo)
                chkHL.append(self.dataPt[-1][14]);
                self.dataBookMS[self.itr][96]=self.dataPt[-2][14];chkHL.append(self.dataPt[-2][14]);
                self.dataBookMS[self.itr][97]=self.dataPt[-3][14];chkHL.append(self.dataPt[-3][14]);
                self.dataBookMS[self.itr][98]=self.dataPt[-4][14];chkHL.append(self.dataPt[-4][14]);
                self.dataBookMS[self.itr][99]=self.dataPt[-5][14];chkHL.append(self.dataPt[-5][14]);
                self.dataBookMS[self.itr][100]=self.dataPt[-6][14];chkHL.append(self.dataPt[-6][14]);
                self.dataBookMS[self.itr][101]=self.dataPt[-7][14];chkHL.append(self.dataPt[-7][14]);
                self.dataBookMS[self.itr][102]=self.dataPt[-8][14];chkHL.append(self.dataPt[-8][14]);
                self.dataBookMS[self.itr][103]=self.dataPt[-9][14];chkHL.append(self.dataPt[-9][14]);
                self.dataBookMS[self.itr][104]=max(chkHL)
                self.dataBookMS[self.itr][105]=min(chkHL)
                mdRange.append(self.dataPt[-1][17]);
                self.dataBookMS[self.itr][107]=self.dataPt[-2][17];mdRange.append(self.dataPt[-2][17]);
                self.dataBookMS[self.itr][108]=self.dataPt[-3][17];mdRange.append(self.dataPt[-3][17]);
                self.dataBookMS[self.itr][109]=self.dataPt[-4][17];mdRange.append(self.dataPt[-4][17]);
                self.dataBookMS[self.itr][110]=self.dataPt[-5][17];mdRange.append(self.dataPt[-5][17]);
                self.dataBookMS[self.itr][111]=self.dataPt[-6][17];mdRange.append(self.dataPt[-6][17]);
                self.dataBookMS[self.itr][112]=self.dataPt[-7][17];mdRange.append(self.dataPt[-7][17]);
                self.dataBookMS[self.itr][113]=self.dataPt[-8][17];mdRange.append(self.dataPt[-8][17]);
                self.dataBookMS[self.itr][114]=self.dataPt[-9][17];mdRange.append(self.dataPt[-9][17]);
                self.dataBookMS[self.itr][115]=max(mdRange)
                self.dataBookMS[self.itr][116]=min(mdRange)
                lastBid.append(self.dataPt[-1][18])
                self.dataBookMS[self.itr][118]=self.dataPt[-2][18];lastBid.append(self.dataPt[-2][18]);
                self.dataBookMS[self.itr][119]=self.dataPt[-3][18];lastBid.append(self.dataPt[-3][18]);
                self.dataBookMS[self.itr][120]=self.dataPt[-4][18];lastBid.append(self.dataPt[-4][18]);
                self.dataBookMS[self.itr][121]=self.dataPt[-5][18];lastBid.append(self.dataPt[-5][18]);
                self.dataBookMS[self.itr][122]=self.dataPt[-6][18];lastBid.append(self.dataPt[-6][18]);
                self.dataBookMS[self.itr][123]=self.dataPt[-7][18];lastBid.append(self.dataPt[-7][18]);
                self.dataBookMS[self.itr][124]=self.dataPt[-8][18];lastBid.append(self.dataPt[-8][18]);
                self.dataBookMS[self.itr][125]=self.dataPt[-9][18];lastBid.append(self.dataPt[-9][18]);
                self.dataBookMS[self.itr][126]=max(lastBid)
                self.dataBookMS[self.itr][127]=min(lastBid)
                lastAsk.append(self.dataPt[-1][19])
                self.dataBookMS[self.itr][129]=self.dataPt[-2][19];lastAsk.append(self.dataPt[-2][19]);
                self.dataBookMS[self.itr][130]=self.dataPt[-3][19];lastAsk.append(self.dataPt[-3][19]);
                self.dataBookMS[self.itr][131]=self.dataPt[-4][19];lastAsk.append(self.dataPt[-4][19]);
                self.dataBookMS[self.itr][132]=self.dataPt[-5][19];lastAsk.append(self.dataPt[-5][19]);
                self.dataBookMS[self.itr][133]=self.dataPt[-6][19];lastAsk.append(self.dataPt[-6][19]);
                self.dataBookMS[self.itr][134]=self.dataPt[-7][19];lastAsk.append(self.dataPt[-7][19]);
                self.dataBookMS[self.itr][135]=self.dataPt[-8][19];lastAsk.append(self.dataPt[-8][19]);
                self.dataBookMS[self.itr][136]=self.dataPt[-9][19];lastAsk.append(self.dataPt[-9][19]);
                self.dataBookMS[self.itr][137]=max(lastAsk)
                self.dataBookMS[self.itr][138]=min(lastAsk)
                lastMid.append(self.dataPt[-1][20])
                self.dataBookMS[self.itr][140]=self.dataPt[-2][20];lastMid.append(self.dataPt[-2][20]);
                self.dataBookMS[self.itr][141]=self.dataPt[-3][20];lastMid.append(self.dataPt[-3][20]);
                self.dataBookMS[self.itr][142]=self.dataPt[-4][20];lastMid.append(self.dataPt[-4][20]);
                self.dataBookMS[self.itr][143]=self.dataPt[-5][20];lastMid.append(self.dataPt[-5][20]);
                self.dataBookMS[self.itr][144]=self.dataPt[-6][20];lastMid.append(self.dataPt[-6][20]);
                self.dataBookMS[self.itr][145]=self.dataPt[-7][20];lastMid.append(self.dataPt[-7][20]);
                self.dataBookMS[self.itr][146]=self.dataPt[-8][20];lastMid.append(self.dataPt[-8][20]);
                self.dataBookMS[self.itr][147]=self.dataPt[-9][20];lastMid.append(self.dataPt[-9][20]);
                self.dataBookMS[self.itr][148]=max(lastMid)
                self.dataBookMS[self.itr][149]=min(lastMid)
                
                
                # PUT IN COMP.
                if(self.dataPt[-1][20]==self.dataBookMS[self.itr][148]): self.dataBookMS[self.itr][150]=1;pass;
                elif(self.dataPt[-1][20]==self.dataBookMS[self.itr][149]): self.dataBookMS[self.itr][151]=-1;pass;
                
                if(self.dataPt[-1][19]==self.dataBookMS[self.itr][137]): self.dataBookMS[self.itr][152]=1;pass;
                elif(self.dataPt[-1][19]==self.dataBookMS[self.itr][138]): self.dataBookMS[self.itr][153]=-1;pass;
                
                if(self.dataPt[-1][18]==self.dataBookMS[self.itr][126]): self.dataBookMS[self.itr][154]=1;pass;
                elif(self.dataPt[-1][18]==self.dataBookMS[self.itr][127]): self.dataBookMS[self.itr][155]=-1;pass;
                
                if(self.dataPt[-1][17]==self.dataBookMS[self.itr][115]): self.dataBookMS[self.itr][156]=1;pass;
                elif(self.dataPt[-1][17]==self.dataBookMS[self.itr][116]): self.dataBookMS[self.itr][157]=-1;pass;
                
                if(self.dataPt[-1][14]==self.dataBookMS[self.itr][104]): self.dataBookMS[self.itr][158]=1;pass;
                elif(self.dataPt[-1][14]==self.dataBookMS[self.itr][105]): self.dataBookMS[self.itr][159]=-1;pass;
                
                if(self.dataPt[-1][10]==self.dataBookMS[self.itr][93]): self.dataBookMS[self.itr][160]=1;pass;
                elif(self.dataPt[-1][10]==self.dataBookMS[self.itr][94]): self.dataBookMS[self.itr][161]=-1;pass;
                
                if(self.dataPt[-1][9]==self.dataBookMS[self.itr][82]): self.dataBookMS[self.itr][162]=1;pass;
                elif(self.dataPt[-1][9]==self.dataBookMS[self.itr][83]): self.dataBookMS[self.itr][163]=-1;pass;
                
                if(self.dataPt[-1][15]==self.dataBookMS[self.itr][71]): self.dataBookMS[self.itr][164]=1;pass;
                elif(self.dataPt[-1][15]==self.dataBookMS[self.itr][72]): self.dataBookMS[self.itr][165]=-1;pass;
                
                if(self.dataPt[-1][16]==self.dataBookMS[self.itr][60]): self.dataBookMS[self.itr][166]=1;pass;
                elif(self.dataPt[-1][16]==self.dataBookMS[self.itr][61]): self.dataBookMS[self.itr][167]=-1;pass;
                
                if(self.dataPt[-1][8]==self.dataBookMS[self.itr][48]): self.dataBookMS[self.itr][168]=1;pass;
                elif(self.dataPt[-1][8]==self.dataBookMS[self.itr][49]): self.dataBookMS[self.itr][169]=-1;pass;
                    
                if(self.dataPt[-1][6]==self.dataBookMS[self.itr][37]): self.dataBookMS[self.itr][170]=1;pass;
                elif(self.dataPt[-1][6]==self.dataBookMS[self.itr][38]): self.dataBookMS[self.itr][171]=-1;pass;
                
                if(self.dataPt[-1][7]==self.dataBookMS[self.itr][26]): self.dataBookMS[self.itr][172]=1;pass;
                elif(self.dataPt[-1][7]==self.dataBookMS[self.itr][27]): self.dataBookMS[self.itr][173]=-1;pass;

                    
                chkA=[0,0,0,0,0,0,0];
                for idxA in range(-2, -10, -1):
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][7]): chkA[0]+=1;pass;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][9]): chkA[1]+=1;pass;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][16]): chkA[2]+=1;pass;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][17]): chkA[3]+=1;pass;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][18]): chkA[4]+=1;pass;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][19]): chkA[5]+=1;pass;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][20]): chkA[6]+=1;pass;
                iA=0;
                for idA in range(174, 181, 1):
                    self.dataBookMS[self.itr][idA]=chkA[iA];
                    iA+=1;
                    
                chkB=[0,0,0,0,0,0,0,0,0,0];
                for bIdx in range(-2, -10, -1):
                    if(self.dataPt[bIdx][6]>self.dataPt[bIdx-1][6]): chkB[0]+=1;pass;
                    if(self.dataPt[bIdx][7]>self.dataPt[bIdx-1][7]): chkB[1]+=1;pass;
                    if(self.dataPt[bIdx][8]>self.dataPt[bIdx-1][8]): chkB[2]+=1;pass;
                    if(self.dataPt[bIdx][14]>self.dataPt[bIdx-1][14]): chkB[3]+=1;pass;
                    if(self.dataPt[bIdx][15]>self.dataPt[bIdx-1][15]): chkB[4]+=1;pass;
                    if(self.dataPt[bIdx][16]>self.dataPt[bIdx-1][16]): chkB[5]+=1;pass;
                    if(self.dataPt[bIdx][17]>self.dataPt[bIdx-1][17]): chkB[6]+=1;pass;
                    if(self.dataPt[bIdx][18]>self.dataPt[bIdx-1][18]): chkB[7]+=1;pass;
                    if(self.dataPt[bIdx][19]>self.dataPt[bIdx-1][19]): chkB[8]+=1;pass;
                    if(self.dataPt[bIdx][20]>self.dataPt[bIdx-1][20]): chkB[9]+=1;pass;
                    
                idB=0;
                for idBin in range(181, 191, 1):
                    self.dataBookMS[self.itr][idBin]=chkB[idB];
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
                
                # SET THIS
                for idCin in range(191, 201, 1):
                    self.dataBookMS[self.itr][idCin]=chkC[idC][2];
                    idC+=1;
                    
                # AVERAGE RATE OF CHANGE OVER 8 TERMS.    
                for idTen in range(-2, -10, -1):
                    chkC[0][3]+=self.dataPt[idTen][6];
                    chkC[0][4]+=(self.dataPt[idTen][6]-self.dataPt[idTen-1][6]);
                    chkC[0][5]+=(chkC[0][4]/chkC[0][3]);
                    #self.dataBookSections[self.itr][0].append(chkC[0][5]);
                    chkC[1][3]+=self.dataPt[idTen][7];
                    chkC[1][4]+=(self.dataPt[idTen][7]-self.dataPt[idTen-1][7]);
                    chkC[1][5]+=(chkC[1][4]/chkC[1][3]);
                    #self.dataBookSections[self.itr][1].append(chkC[1][5]);
                    chkC[2][3]+=self.dataPt[idTen][8];
                    chkC[2][4]+=(self.dataPt[idTen][8]-self.dataPt[idTen-1][8]);
                    chkC[2][5]+=(chkC[2][4]/chkC[2][3]);
                    #self.dataBookSections[self.itr][2].append(chkC[2][5]);
                    chkC[3][3]+=self.dataPt[idTen][14];
                    chkC[3][4]+=(self.dataPt[idTen][14]-self.dataPt[idTen-1][14]);
                    chkC[3][5]+=(chkC[3][4]/chkC[3][3]);
                    #self.dataBookSections[self.itr][3].append(chkC[3][5]);
                    chkC[4][3]+=self.dataPt[idTen][15];
                    chkC[4][4]+=(self.dataPt[idTen][15]-self.dataPt[idTen-1][15]);
                    chkC[4][5]+=(chkC[4][4]/chkC[4][3]);
                    #self.dataBookSections[self.itr][4].append(chkC[4][5]);
                    chkC[5][3]+=self.dataPt[idTen][16];
                    chkC[5][4]+=(self.dataPt[idTen][16]-self.dataPt[idTen-1][16]);
                    chkC[5][5]+=(chkC[5][4]/chkC[5][3]);
                    #self.dataBookSections[self.itr][5].append(chkC[5][5]);
                    chkC[6][3]+=self.dataPt[idTen][17];
                    chkC[6][4]+=(self.dataPt[idTen][17]-self.dataPt[idTen-1][17]);
                    chkC[6][5]+=(chkC[6][4]/chkC[6][3]);
                    #self.dataBookSections[self.itr][6].append(chkC[6][5]);
                    chkC[7][3]+=self.dataPt[idTen][18];
                    chkC[7][4]+=(self.dataPt[idTen][18]-self.dataPt[idTen-1][18]);
                    chkC[7][5]+=(chkC[7][4]/chkC[7][3]);
                    #self.dataBookSections[self.itr][7].append(chkC[7][5]);
                    chkC[8][3]+=self.dataPt[idTen][19];
                    chkC[8][4]+=(self.dataPt[idTen][19]-self.dataPt[idTen-1][19]);
                    chkC[8][5]+=(chkC[8][4]/chkC[8][3]);
                    #self.dataBookSections[self.itr][8].append(chkC[8][5]);
                    chkC[9][3]+=self.dataPt[idTen][20];
                    chkC[9][4]+=(self.dataPt[idTen][20]-self.dataPt[idTen-1][20]);
                    chkC[9][5]+=(chkC[9][4]/chkC[9][3]);
                    #self.dataBookSections[self.itr][9].append(chkC[9][5]);
      
                idP=0;
                # SETS THE CUMULATIVE RATE IN BOX 201..210
                for iDc in range(201, 211, 1):
                    self.dataBookMS[self.itr][iDc]=chkC[idP][5];
                    idP+=1;
                
                # we can ping that in forecasting the next point.
                
                iE=0;
                # CHECKS IF THE CURRENT TERM IS THE MAX RATE AND ASSIGNS A VALUE 1
                for chkRate in range(211, 221, 1):
                    if(chkC[iE][2]>chkC[iE][5]): self.dataBookMS[self.itr][chkRate]=1;pass;
                    iE+=1;
                    
                print('end\t\t', self.dataBookMS[self.itr])
                print('earlier\t\t', self.dataBookMS[self.itr-3])
                hotex=self.itr;
                str0=str(self.itr)+",";
                for units in self.dataBookMS[self.itr]:
                    str0+=str(units)+",";
                str0+='\n';
                print(str0)
                service.write_file(self.fileName,'{}'.format(str0))  
                break;
            
            
            
            
            elif(self.idxLoop>40):
                
                chkBid=[];chkLst=[];chkAsk=[];chkMid=[];chkSpr=[];chkHi=[];chkLo=[];chkHL=[];mdRange=[];lastBid=[];lastAsk=[];lastMid=[];
                print('new HOTEX\n', self.dataPt[-1])
                #hoteX=max(-idx, -10)
                chkBid.append(self.dataPt[-1][7]);
                
                
                revolvers=[]
                for revolver in range(-1, offset, -1):
                    revolvers.append(revolver)
                
                print(self.itr, 'REVOLVERS\tREVOLVERS\tREVOLVERS\tREVOLVERS\tREVOLVERS\tREVOLVERS\tREVOLVERS\tREVOLVERS\t')
                print(revolvers)
                
                print(self.dataPt[-2+offset])
                print(len(self.dataPt))
                #idx
                iH=18;
                for hoteX in range(-2, -10, -1):
                    self.dataBookMS[self.itr][iH]=self.dataPt[hoteX+offset][7];
                    chkBid.append(self.dataPt[hoteX+offset][7]);
                    iH+=1;
                self.dataBookMS[self.itr][26]=max(chkBid);
                self.dataBookMS[self.itr][27]=min(chkBid);
                
                
                #THANK YOU.
                #
                #
                #
                self.dataBookMS[self.itr][18]=self.dataPt[-2+offset][7];chkBid.append(self.dataPt[-2+offset][7]);
                self.dataBookMS[self.itr][19]=self.dataPt[-3+offset][7];chkBid.append(self.dataPt[-3+offset][7]);
                self.dataBookMS[self.itr][20]=self.dataPt[-4+offset][7];chkBid.append(self.dataPt[-4+offset][7]);
                self.dataBookMS[self.itr][21]=self.dataPt[-5+offset][7];chkBid.append(self.dataPt[-5+offset][7]);
                self.dataBookMS[self.itr][22]=self.dataPt[-6+offset][7];chkBid.append(self.dataPt[-6+offset][7]);
                self.dataBookMS[self.itr][23]=self.dataPt[-7+offset][7];chkBid.append(self.dataPt[-7+offset][7]);
                self.dataBookMS[self.itr][24]=self.dataPt[-8+offset][7];chkBid.append(self.dataPt[-8+offset][7]);
                self.dataBookMS[self.itr][25]=self.dataPt[-9+offset][7];chkBid.append(self.dataPt[-9+offset][7]);
                self.dataBookMS[self.itr][26]=max(chkBid)
                self.dataBookMS[self.itr][27]=min(chkBid)
                
                chkLst.append(self.dataPt[-1+offset][6]);
                iH=28;
                for hoteX in range(-2, -11, -1):
                    self.dataBookMS[self.itr][iH]=self.dataPt[hoteX+offset][6];
                    chkLst.append(self.dataPt[hoteX+offset][6]);
                    iH+=1;
                self.dataBookMS[self.itr][37]=max(chkLst);
                self.dataBookMS[self.itr][38]=min(chkLst);
                
                print('idx==internals')
                print(self.itr)
                print(self.dataPt[-2+offset][8])
                print(self.dataPt[-3+offset][8])
                
                chkAsk.append(self.dataPt[-1+offset][8]);
                iH=39;
                for hoteX in range(-2, -11, -1):
                    self.dataBookMS[self.itr][iH]=self.dataPt[hoteX+offset][8];
                    chkAsk.append(self.dataPt[hoteX+offset][8]);
                    iH+=1;
                self.dataBookMS[self.itr][48]=max(chkAsk);
                self.dataBookMS[self.itr][49]=min(chkAsk);
                
                self.dataBookMS[self.itr][50]=self.dataPt[-1+offset][1];
                
                chkMid.append(self.dataPt[-1+offset][16]);
                iH=51;
                for hoteX in range(-2, -11, -1):
                    self.dataBookMS[self.itr][iH]=self.dataPt[hoteX+offset][16];
                    chkMid.append(self.dataPt[hoteX+offset][16]);
                    iH+=1;
                self.dataBookMS[self.itr][60]=max(chkMid);
                self.dataBookMS[self.itr][61]=min(chkMid);

                
                chkSpr.append(self.dataPt[-1+offset][15]);
                iH=62;
                for hoteX in range(-2, -11, -1):
                    self.dataBookMS[self.itr][iH]=self.dataPt[hoteX+offset][15];
                    chkSpr.append(self.dataPt[hoteX+offset][15]);
                    iH+=1;
                self.dataBookMS[self.itr][71]=max(chkSpr);
                self.dataBookMS[self.itr][72]=min(chkSpr);
                
                # bar data section
                #chkHi.append(self.dataBookMS[self.itr+offset][9]);
                #iH=73;
                #for hoteX in range(-2, -11, -1):
                #    self.dataBookMS[self.itr][iH]=self.dataBookMS[self.itr+offset][9];
                #    chkHi.append(self.dataBookMS[self.itr+offset][9]);
                #    iH+=1;
                #self.dataBookMS[self.itr][82]=max(chkHi);
                #self.dataBookMS[self.itr][83]=min(chkHi);
                #
                #chkLo.append(self.dataBookMS[self.itr+offset][10]);
                #iH=84;
                #for hoteX in range(-2, -11, -1):
                #    self.dataBookMS[self.itr][iH]=self.dataBookMS[self.itr+offset][10];
                #    chkLo.append(self.dataPt[hoteX+offset][10]);
                #    iH+=1;
                #self.dataBookMS[self.itr][93]=max(chkLo)
                #self.dataBookMS[self.itr][94]=min(chkLo)
                

                chkHi.append(self.dataPt[-1+offset][9]);
                iH=73;
                for hoteX in range(-2, -11, -1):
                    self.dataBookMS[self.itr][iH]=self.dataPt[hoteX+offset][9];
                    chkHi.append(self.dataPt[hoteX+offset][9]);
                    iH+=1;
                self.dataBookMS[self.itr][82]=max(chkHi);
                self.dataBookMS[self.itr][83]=min(chkHi);
                
                chkLo.append(self.dataPt[-1+offset][10]);
                iH=84;
                for hoteX in range(-2, -11, -1):
                    self.dataBookMS[self.itr][iH]=self.dataPt[hoteX+offset][10];
                    chkLo.append(self.dataPt[hoteX+offset][10]);
                    iH+=1;        
                self.dataBookMS[self.itr][93]=max(chkLo)
                self.dataBookMS[self.itr][94]=min(chkLo)
                    
                chkHL.append(self.dataPt[-1+offset][14]);
                iH=95;
                for hoteX in range(-2, -11, -1):
                    self.dataBookMS[self.itr][iH]=self.dataPt[hoteX+offset][14];
                    chkHL.append(self.dataPt[hoteX+offset][14]);
                    iH+=1;
                self.dataBookMS[self.itr][104]=max(chkHL);
                self.dataBookMS[self.itr][105]=min(chkHL);
                
                mdRange.append(self.dataPt[-1+offset][17]);
                iH=106;
                for hoteX in range(-2, -11, -1):
                    self.dataBookMS[self.itr][iH]=self.dataPt[hoteX+offset][17];
                    mdRange.append(self.dataPt[hoteX+offset][17]);
                    iH+=1;
                self.dataBookMS[self.itr][115]=max(mdRange);
                self.dataBookMS[self.itr][116]=min(mdRange);

                lastBid.append(self.dataPt[-1+offset][18]);
                iH=117;
                for hoteX in range(-2, -11, -1):
                    self.dataBookMS[self.itr][iH]=self.dataPt[hoteX+offset][18];
                    lastBid.append(self.dataPt[hoteX+offset][18]);
                    iH+=1;
                self.dataBookMS[self.itr][126]=max(lastBid);
                self.dataBookMS[self.itr][127]=min(lastBid);
                
                lastAsk.append(self.dataPt[-1+offset][19]);
                iH=128;
                for hoteX in range(-2, -11, -1):
                    self.dataBookMS[self.itr][iH]=self.dataPt[hoteX+offset][19];
                    lastAsk.append(self.dataPt[hoteX+offset][19]);
                    iH+=1;
                self.dataBookMS[self.itr][137]=max(lastAsk);
                self.dataBookMS[self.itr][138]=min(lastAsk);
                
                lastMid.append(self.dataPt[-1+offset][20])
                iH=139;
                for hoteX in range(-2, -11, -1):
                    self.dataBookMS[self.itr][iH]=self.dataPt[hoteX+offset][20];
                    lastMid.append(self.dataPt[hoteX+offset][20]);
                    iH+=1;
                self.dataBookMS[self.itr][148]=max(lastMid);
                self.dataBookMS[self.itr][149]=min(lastMid);
                
                # PUT IN COMP.
                if(self.dataPt[-1+offset][20]==self.dataBookMS[self.itr][148]): self.dataBookMS[self.itr][150]=1;pass;
                elif(self.dataPt[-1+offset][20]==self.dataBookMS[self.itr][149]): self.dataBookMS[self.itr][151]=-1;pass;
                
                if(self.dataPt[-1+offset][19]==self.dataBookMS[self.itr][137]): self.dataBookMS[self.itr][152]=1;pass; 
                elif(self.dataPt[-1+offset][19]==self.dataBookMS[self.itr][138]): self.dataBookMS[self.itr][153]=-1;pass;
                
                if(self.dataPt[-1+offset][18]==self.dataBookMS[self.itr][126]): self.dataBookMS[self.itr][154]=1;pass;
                elif(self.dataPt[-1+offset][18]==self.dataBookMS[self.itr][127]): self.dataBookMS[self.itr][155]=-1;pass;
                
                if(self.dataPt[-1+offset][17]==self.dataBookMS[self.itr][115]): self.dataBookMS[self.itr][156]=1;pass;
                elif(self.dataPt[-1+offset][17]==self.dataBookMS[self.itr][116]): self.dataBookMS[self.itr][157]=-1;pass;
                
                if(self.dataPt[-1+offset][14]==self.dataBookMS[self.itr][104]): self.dataBookMS[self.itr][158]=1;pass;
                elif(self.dataPt[-1+offset][14]==self.dataBookMS[self.itr][105]): self.dataBookMS[self.itr][159]=-1;pass;
                
                if(self.dataPt[-1+offset][10]==self.dataBookMS[self.itr][93]): self.dataBookMS[self.itr][160]=1;pass;
                elif(self.dataPt[-1+offset][10]==self.dataBookMS[self.itr][94]): self.dataBookMS[self.itr][161]=-1;pass;
                
                if(self.dataPt[-1+offset][9]==self.dataBookMS[self.itr][82]): self.dataBookMS[self.itr][162]=1;pass;
                elif(self.dataPt[-1+offset][9]==self.dataBookMS[self.itr][83]): self.dataBookMS[self.itr][163]=-1;pass;
                
                if(self.dataPt[-1+offset][15]==self.dataBookMS[self.itr][71]): self.dataBookMS[self.itr][164]=1;pass;
                elif(self.dataPt[-1+offset][15]==self.dataBookMS[self.itr][72]): self.dataBookMS[self.itr][165]=-1;pass;
                
                if(self.dataPt[-1+offset][16]==self.dataBookMS[self.itr][60]): self.dataBookMS[self.itr][166]=1;pass;
                elif(self.dataPt[-1+offset][16]==self.dataBookMS[self.itr][61]): self.dataBookMS[self.itr][167]=-1;pass;
                
                if(self.dataPt[-1+offset][8]==self.dataBookMS[self.itr][48]): self.dataBookMS[self.itr][168]=1;pass;
                elif(self.dataPt[-1+offset][8]==self.dataBookMS[self.itr][49]): self.dataBookMS[self.itr][169]=-1;pass;
                
                if(self.dataPt[-1+offset][6]==self.dataBookMS[self.itr][37]): self.dataBookMS[self.itr][170]=1;pass;
                elif(self.dataPt[-1+offset][6]==self.dataBookMS[self.itr][38]): self.dataBookMS[self.itr][171]=-1;pass;
                
                if(self.dataPt[-1+offset][7]==self.dataBookMS[self.itr][26]): self.dataBookMS[self.itr][172]=1;pass;
                elif(self.dataPt[-1+offset][7]==self.dataBookMS[self.itr][27]): self.dataBookMS[self.itr][173]=-1;pass;

                rangeF=max(-idx, -10)
                chkA=[0,0,0,0,0,0,0];
                for idxA in range(-2+offset, rangeF+offset, -1):
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][7]):
                        chkA[0]+=1;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][9]):
                        chkA[1]+=1;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][16]):
                        chkA[2]+=1;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][17]):
                        chkA[3]+=1;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][18]):
                        chkA[4]+=1;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][19]):
                        chkA[5]+=1;
                    if(self.dataPt[idxA][6]>self.dataPt[idxA][20]):
                        chkA[6]+=1;
                        
                iA=0;
                for idA in range(174, 181, 1):
                    self.dataBookMS[self.itr][idA]=chkA[iA];
                    iA+=1;

                chkB=[0,0,0,0,0,0,0,0,0,0];
                for bIdx in range(-2+offset, rangeF+offset+1, -1):
                    if(self.dataPt[bIdx][6]>self.dataPt[bIdx-1][6]): chkB[0]+=1;pass;
                    if(self.dataPt[bIdx][7]>self.dataPt[bIdx-1][7]): chkB[1]+=1;pass;
                    if(self.dataPt[bIdx][8]>self.dataPt[bIdx-1][8]): chkB[2]+=1;pass;
                    if(self.dataPt[bIdx][14]>self.dataPt[bIdx-1][14]): chkB[3]+=1;pass;
                    if(self.dataPt[bIdx][15]>self.dataPt[bIdx-1][15]): chkB[4]+=1;pass;
                    if(self.dataPt[bIdx][16]>self.dataPt[bIdx-1][16]): chkB[5]+=1;pass;
                    if(self.dataPt[bIdx][17]>self.dataPt[bIdx-1][17]): chkB[6]+=1;pass;
                    if(self.dataPt[bIdx][18]>self.dataPt[bIdx-1][18]): chkB[7]+=1;pass;
                    if(self.dataPt[bIdx][19]>self.dataPt[bIdx-1][19]): chkB[8]+=1;pass;
                    if(self.dataPt[bIdx][20]>self.dataPt[bIdx-1][20]): chkB[9]+=1;pass;
                    
                idB=0;
                for idBin in range(181, 191, 1):
                    self.dataBookMS[self.itr][idBin]=chkB[idB];
                    idB+=1;

                if(idx>2 and len(self.dataPt[-9+offset])>2):
                    chkC=[[0,0,0,0,0,0]] * 10;
                    chkC[0][0]=self.dataPt[-1+offset][6];
                    chkC[0][1]=self.dataPt[-1+offset][6]-self.dataPt[-2+offset][6];
                    chkC[0][2]=(chkC[0][1]/chkC[0][0]);
                    chkC[1][0]=self.dataPt[-1+offset][7];
                    chkC[1][1]=self.dataPt[-1+offset][7]-self.dataPt[-2+offset][7];
                    chkC[1][2]=(chkC[1][1]/chkC[1][0]);
                    chkC[2][0]=self.dataPt[-1+offset][8];
                    chkC[2][1]=self.dataPt[-1+offset][8]-self.dataPt[-2+offset][8];
                    chkC[2][2]=(chkC[2][1]/chkC[2][0]);
                    chkC[3][0]=self.dataPt[-1+offset][14];
                    chkC[3][1]=self.dataPt[-1+offset][14]-self.dataPt[-2+offset][14];
                    chkC[3][2]=(chkC[3][1]/chkC[3][0]);
                    chkC[4][0]=self.dataPt[-1+offset][15];
                    chkC[4][1]=self.dataPt[-1+offset][15]-self.dataPt[-2+offset][15];
                    chkC[4][2]=(chkC[4][1]/chkC[4][0]); 
                    chkC[5][0]=self.dataPt[-1+offset][16];
                    chkC[5][1]=self.dataPt[-1+offset][16]-self.dataPt[-2+offset][16];
                    chkC[5][2]=(chkC[5][1]/chkC[5][0]);   
                    chkC[6][0]=self.dataPt[-1+offset][17];
                    chkC[6][1]=self.dataPt[-1+offset][17]-self.dataPt[-2+offset][17];
                    chkC[6][2]=(chkC[6][1]/chkC[6][0]);                   
                    chkC[7][0]=self.dataPt[-1+offset][18];
                    chkC[7][1]=self.dataPt[-1+offset][18]-self.dataPt[-2+offset][18];
                    chkC[7][2]=(chkC[7][1]/chkC[7][0]);
                    chkC[8][0]=self.dataPt[-1+offset][19];
                    chkC[8][1]=self.dataPt[-1+offset][19]-self.dataPt[-2+offset][19];
                    chkC[8][2]=(chkC[8][1]/chkC[8][0]);
                    chkC[9][0]=self.dataPt[-1+offset][20];
                    chkC[9][1]=self.dataPt[-1+offset][20]-self.dataPt[-2+offset][20];
                    chkC[9][2]=(chkC[9][1]/chkC[9][0]);

                    idC=0;
                    # SET THIS
                    for idCin in range(191, 201, 1):
                        self.dataBookMS[self.itr][idCin]=chkC[idC][2];
                        idC+=1;

                    # AVERAGE RATE OF CHANGE OVER 8 TERMS.
                    for idTen in range(-2+offset, -9+offset, -1):
                        chkC[0][3]+=self.dataPt[idTen][6];
                        chkC[0][4]+=(self.dataPt[idTen][6]-self.dataPt[idTen-1][6]);
                        chkC[0][5]+=(chkC[0][4]/chkC[0][3]);
                        #self.dataBookSections[self.itr][0].append(chkC[0][5]);
                        chkC[1][3]+=self.dataPt[idTen][7];
                        chkC[1][4]+=(self.dataPt[idTen][7]-self.dataPt[idTen-1][7]);
                        chkC[1][5]+=(chkC[1][4]/chkC[1][3]);
                        #self.dataBookSections[self.itr][1].append(chkC[1][5]);
                        chkC[2][3]+=self.dataPt[idTen][8];
                        chkC[2][4]+=(self.dataPt[idTen][8]-self.dataPt[idTen-1][8]);
                        chkC[2][5]+=(chkC[2][4]/chkC[2][3]);
                        #self.dataBookSections[self.itr][2].append(chkC[2][5]);
                        chkC[3][3]+=self.dataPt[idTen][14];
                        chkC[3][4]+=(self.dataPt[idTen][14]-self.dataPt[idTen-1][14]);
                        chkC[3][5]+=(chkC[3][4]/chkC[3][3]);
                        #self.dataBookSections[self.itr][3].append(chkC[3][5]);
                        chkC[4][3]+=self.dataPt[idTen][15];
                        chkC[4][4]+=(self.dataPt[idTen][15]-self.dataPt[idTen-1][15]);
                        chkC[4][5]+=(chkC[4][4]/chkC[4][3]);
                        #self.dataBookSections[self.itr][4].append(chkC[4][5]);
                        chkC[5][3]+=self.dataPt[idTen][16];
                        chkC[5][4]+=(self.dataPt[idTen][16]-self.dataPt[idTen-1][16]);
                        chkC[5][5]+=(chkC[5][4]/chkC[5][3]);
                        #self.dataBookSections[self.itr][5].append(chkC[5][5]);
                        chkC[6][3]+=self.dataPt[idTen][17];
                        chkC[6][4]+=(self.dataPt[idTen][17]-self.dataPt[idTen-1][17]);
                        chkC[6][5]+=(chkC[6][4]/chkC[6][3]);
                        #self.dataBookSections[self.itr][6].append(chkC[6][5]);
                        chkC[7][3]+=self.dataPt[idTen][18];
                        chkC[7][4]+=(self.dataPt[idTen][18]-self.dataPt[idTen-1][18]);
                        chkC[7][5]+=(chkC[7][4]/chkC[7][3]);
                        #self.dataBookSections[self.itr][7].append(chkC[7][5]);
                        chkC[8][3]+=self.dataPt[idTen][19];
                        chkC[8][4]+=(self.dataPt[idTen][19]-self.dataPt[idTen-1][19]);
                        chkC[8][5]+=(chkC[8][4]/chkC[8][3]);
                        #self.dataBookSections[self.itr][8].append(chkC[8][5]);
                        chkC[9][3]+=self.dataPt[idTen][20];
                        chkC[9][4]+=(self.dataPt[idTen][20]-self.dataPt[idTen-1][20]);
                        chkC[9][5]+=(chkC[9][4]/chkC[9][3]);
                        #self.dataBookSections[self.itr][9].append(chkC[9][5]);

                    idP=0;
                    for iDc in range(201, 211, 1):
                        self.dataBookMS[self.itr][iDc]=chkC[idP][5];
                        idP+=1;

                    iE=0;
                    # CHECKS IF THE CURRENT TERM IS THE MAX RATE AND ASSIGNS A VALUE 1
                    for chkRate in range(211, 221, 1):
                        if(chkC[iE][2]>chkC[iE][5]):
                            self.dataBookMS[self.itr][chkRate]=1;
                        iE+=1;
                        
                        
                print(self.itr)        
                print('INTERNAL LOOP [self.itr]\t\t', self.dataBookMS[self.itr])
                print('CURRENT DATABOOK LOOP [-1]\t\t', self.dataBookMS[-1])
                print('CURRENT self.dataPt [-1]+offset', self.dataPt[-1+offset])
                print('CURRENT self.dataPt [-1]\t\t', self.dataPt[-1])
                
                # print('earlier\t\t', self.dataBookMS[self.itr-3])

                str4=str(self.itr)+",";
                for units in self.dataBookMS[self.itr]:
                    str4+=str(units)+",";
                #str4+='\n';
                print(str4)
                service.write_file(self.fileName,'{}'.format(str4));
                offset+=1;
        #barB=md.bar.minute(start=-20, end=None, include_empty=False, include_extended=True, bar_size=2, today_only=True)        
        #rangeMSB = min(len(barB.timestamp), len(barB.askvol), len(barB.bidvol), len(barB.bvwap), len(barB.close), len(barB.count), len(barB.high), len(barB.low), len(barB.open), len(barB.spread), len(barB.volume))
        #for idxB in range(0, rangeMSB, 1):
        #    self.dataBookMSB.append([self.symbol, 20,  self.itr, barB.timestamp[idxB], barB.askvol[idxB], barB.bidvol[idxB], barB.bvwap[idxB], barB.close[idxB], barB.open[idxB], barB.high[idxB], barB.low[idxB], barB.count[idxB], barB.spread[idxB], barB.volume[idxB], barB.high[idxB]-barB.low[idxB], barB.close[idxB]-barB.open[idxB], max(barB.bvwap[idxB], barB.close[idxB], barB.open[idxB], barB.high[idxB]) , self.dataPt[-1][7]])
        #    if(idxB!=0):
        #        self.dataBookMSB[idxB][17]=self.dataBookMSB[idxB][whatever] and self.dataBookMSB[idxB-1][whatever] 
        #
        #print(len(self.dataBookMS[self.itr]))#print("STR2")#str2=str(self.itr-1);#for units in self.dataBookMS[self.itr-1]: #    str2+=str(units)+","; #str2+='\n';#print(str2)

    def on_finish(self, md, order, service, account):
        filenameDT=self.symbol+"-DT.txt"
        #strLoop=self.symbol+"\n"
        #print('onFinish')
        #print(len(self.dataBookMS))
        #print('start\t', strLoop)
        #print(self.dataBookMS[-1])
        #print(self.dataBookMS[-2])
        #print(self.dataBookMS[-3])
        #for aLoop in self.dataBookMS:
        #    print('aloop\t', aLoop)
        #    if(type(aLoop)!='int'):
        #        for diLoop in aLoop:
        #            strLoop+=str(diLoop)+", "
        #    strLoop+="\n"
        #service.write_file(filenameDT, '{}'.format(strLoop))

