# Editor
# switchBox4-ARCA   BDincer   10/27/2023 12:27:26 PM   QA-2.0.239
# N-00006   qabdincer/d1c248
# Voodoo=8fa5330d-b32d-4083-86eb-d9a61a637b8b Sell Market GS SOR
# Voodoo=103d9b43-937a-4590-9f54-1476f3545cf1 Buy Market BATS
# Voodoo=9e6b50d6-dee3-4314-a43b-49e9ae8088b6 Buy Market GS SOR
# Voodoo=5fc61945-3498-47da-abf6-b5dabdc9f4ac Sell Market NASD
# Voodoo=4ad20d14-aacb-4850-9efe-cfa92d154304 Buy Limit NASD SCAN at Script Price
# Voodoo=7a6228ad-dc9d-4377-8b2e-99e8ebb90152 Buy Limit BATS at Script Price
# Voodoo=97a91492-1033-4a96-a546-9bff6df73b08 Buy Limit ARCA at Script Price
# Voodoo=09528d6b-7d4f-4cc2-8611-8bbecb33785c Sell Limit NASD SCAN at Script Price
# Voodoo=c982d0cd-9be5-4a35-b89f-1f66b2495ec4 Sell Limit ARCA at Script Price
# Voodoo=f8328375-d95c-4c10-aa7e-0c7fecf13336 Sell Limit BATS at Script Price

# BLACKLIST IS DEPRECATED: THIS IS AUTOMATICALLY ADMINISTERED USING THE ' self.longSTAT ' VARIABLE.
from cloudquant.interfaces import Strategy
import time, random, io, csv

class Gr8Scriptf6fd3016e01f42ca9b743a1888644643(Strategy):
    __script_name__ = 'switchBox4-ARCA'
       
    ARCA_IDX=0;
    FILE_ARCA='-LCL_Execution.txt'
    MAX_ARCA4_LOSS = 4000;
    MAX_ARCA4_SYMBOL_LOSS = 1000;
    ARCA4_CLOCK=30;
    LOG_ACCOUNT_PERFORMANCE_ARCA=0.00;
    
    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return md.stat.prev_close>75.00 and (md.stat.avol * md.stat.prev_close > 20000000) and md.stat.exchange in ["Q","Z","A","P","N","T","J","K"];

    def __init__(self, **params):
        if('FILE_ARCA' in params):
            self.__class__.FILE_ARCA=params['FILE_ARCA'];
            self.__class__.MAX_ARCA4_LOSS=params['MAX_ARCA4_LOSS'];
            self.__class__.MAX_ARCA4_SYMBOL_LOSS=params['MAX_ARCA4_SYMBOL_LOSS'];
            self.__class__.ARCA4_CLOCK=params['ARCA4_CLOCK'];
            pass;
    
    def on_start(self, md, order, service, account):
    
        # NEW RISK SETTINGS OBJECTS
        self.account_risk_setting={'pending_notional': 750000, 'pending_long_notional': 750000, 'pending_short_notional': 750000, 'position_notional': 750000, 'position_long_notional': 750000, 'position_short_notional': 750000}
        self.symbol_risk_settings={'pending_notional': 375750, 'pending_long_notional': 375750, 'pending_short_notional': 375750, 'position_notional': 375750, 'position_long_notional': 375750, 'position_short_notional': 375750}
    
        ## SYSTEM LOGS.
        self.fileSystemARCA_LOG = service.time_to_string(service.system_time, '%Y-%m-%d')+'FILE_ARCA'+self.__class__.FILE_ARCA;

        # ALLOCATION HOURS.
        self.liquid_time = md.market_open_time + service.time_interval(minutes=30)
        self.illiquid_time = md.market_close_time - service.time_interval(hours=2) 

        # SYMBOL PARAMETER/ VARIABLES.
        self.longSTAT=0;
        self.ARCA_CLOCK = self.__class__.ARCA4_CLOCK;
        self.fileSystemArca = service.time_to_string(service.system_time, '%Y-%m-%d')+self.__class__.FILE_ARCA;        
        
        # INSTANCE: ALLOCATION AND RELEASE VARIABLES.
        service.add_time_trigger(md.market_open_time - service.time_interval(hours=5) - service.time_interval(minutes=30), repeat_interval=service.time_interval(seconds=self.ARCA_CLOCK), timer_id="Analysis");
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=10), timer_id = "eod_1");
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=7), timer_id = "eod_2");

        print("TKR:{} \tTIMER: {}\tFILE: {}\tARCA4 MAX: {}\tTKR MAX: {}\tTRADE DATE: {}".format(self.symbol, self.ARCA_CLOCK, self.fileSystemArca, self.__class__.MAX_ARCA4_LOSS, self.__class__.MAX_ARCA4_SYMBOL_LOSS, service.time_to_string(service.system_time)));
        pass;
    
    def on_timer(self, event, md, order, service, account):

        # [1].  CHECK THE PERFORMANCE OF THE ACCOUNT AND SYMBOL.
        symbolPerformance = account[self.symbol].unrealized_pl.entry_pl + account[self.symbol].realized_pl.entry_pl
        accountPerformance = account.realized_entry_pl+account.unrealized_entry_pl
        
        if(self.symbol=='CASH'):
            self.__class__.LOG_ACCOUNT_PERFORMANCE_ARCA=account.realized_entry_pl+account.unrealized_entry_pl;
            return;
        ## account performance uses an unknown value to determine the current price, possible uses a logic of Last Price and Bid Price Combined?
        
        ## if the account performance is less than the MAX ACCOUNT LOSS PARAMETER, IT CANCELS ALL PENDING ORDER AND CLOSES THE POSITION.
        if(account.realized_entry_pl+account.unrealized_entry_pl<-self.__class__.MAX_ARCA4_LOSS or symbolPerformance<-self.__class__.MAX_ARCA4_SYMBOL_LOSS):
            self.longSTAT==1;
            if(len(account[self.symbol].pending.orders)>0 and event.timestamp>self.liquid_time):
                order.cancel(self.symbol);
                pass;
            elif(account[self.symbol].position.shares>0 and event.timestamp>self.liquid_time):
                CLOSE_LONG_POSITION = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=account[self.symbol].position.shares, user_key=889, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                pass;
            return 0;
            
        # [2].  [RISK CHECK ON TERMINATING THE CYCLE OF OPEN LONG POSITIONS. DOUBLE CHECK MARKET PRIOR TO SENDING MARKET ORDER.]
        if(account[self.symbol].position.shares>0 or self.longSTAT==1):
            risk77bpsLONG = account[self.symbol].position.mtm_price * - 0.0077;
            risk77px1LONG = md.L1.bid - account[self.symbol].position.mtm_price;
            # [1. LONG- DEMIT THE POSITION AND LOCK IT DOWN]
            if(risk77px1LONG < risk77bpsLONG or self.longSTAT==1):
                self.longSTAT=1;
                if(len(account[self.symbol].pending.orders)>0 and event.timestamp>self.liquid_time):
                    order.cancel(self.symbol);
                    pass;
                elif(account[self.symbol].position.shares>0 and event.timestamp>self.liquid_time):
                    CLOSE_LONG_POSITION = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=account[self.symbol].position.shares, user_key=889, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                    pass;
                pass;
            pass;
            
            # [2. LONG- CAPTURE P&L IN EXCESS OF THE SPREAD]
            if(risk77px1LONG > 0.05 and account[self.symbol].position.shares>0 and event.timestamp>self.liquid_time):
                chk77 = int(account[self.symbol].position.shares * 0.16)
                CAPTURE_LONG_PL = order.algo_sell(self.symbol, algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=max(1,chk77), user_key=888, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                pass;

        # END SESSION PROTOCOL.
        if(event.timer_id=="eod_1" or event.timer_id=="eod_2"): 
            eodChk = self.eod_functions(event, md, order, service, account); 
            return eodChk;
            
        
        # [3].  [CHECKS IF THE SYMBOL HAS BEEN LOCKED DOWN FOR THE REST OF THE SESSION.]
        if(self.longSTAT==1 and event.timestamp>self.liquid_time):
            return;

        # [4. LONG ALLOCATION LOOP]
        if(event.timestamp>self.liquid_time):
    
            temp_file_risk = service.read_file(self.fileSystemArca, path = {'FORWARD': '/mnt/userdata/bdincer/','PRODUCTION': '/mnt/userdata/bdincer/'})
            prompterLONG = csv.DictReader(io.StringIO(temp_file_risk))
            
            i=0;
            for row in prompterLONG:
                i+=1;
                if(i>self.__class__.ARCA_IDX):
                    self.__class__.ARCA_IDX+=1;
                    service.write_file(self.fileSystemARCA_LOG,'{},{},{},{},{}'.format(i, self.__class__.ARCA_IDX, row['TICKER'], row['MIDPX'], row['CODE']), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                    if(row['CODE']=='999'):
                        batUnitA1 = order.algo_buy(row['TICKER'], algorithm='103d9b43-937a-4590-9f54-1476f3545cf1', intent='increase', order_quantity=int(row['CODE_QTY']), user_key=999, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);   
                        sorUnitA1 = order.algo_buy(row['TICKER'], algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='increase', order_quantity=int(row['CODE_QTY']), user_key=998, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                        break;
                    elif(row['CODE']=='750.999'):
                        if(account[row['TICKER']].position.capital_long>0):
                            cls_0100 = order.algo_sell(row['TICKER'], algorithm='5fc61945-3498-47da-abf6-b5dabdc9f4ac', intent='decrease', order_quantity=account[row['TICKER']].position.shares, user_key=750, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                            pass;
                        pass;
                    elif(row['CODE']=='750.151'):
                        if(account[row['TICKER']].position.capital_long>0):
                            cls_0100 = order.algo_sell(row['TICKER'], algorithm='5fc61945-3498-47da-abf6-b5dabdc9f4ac', intent='decrease', order_quantity=min(account[row['TICKER']].position.shares, int(row['CODE_QTY'])), user_key=751, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                            pass;
                        pass;
                    elif(row['CODE']=='1809'):
                        if(account[row['TICKER']].position.capital_long>0):
                            cls_1809 = order.algo_sell(row['TICKER'], algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='decrease', order_quantity=int(row['CODE_QTY']), user_key=1809, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                            pass;
                        pass;
                    pass;
                pass;
            return;
        
        if(event.timestamp<self.liquid_time):

            if(md.L1.bid>md.L1.ask):
                buy_NQ1PF = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=100, price=md.L1.ask+0.01, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                buy_NQ2PF = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='increase', order_quantity=100, price=md.L1.ask+0.02, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);    
                buy_BATS1 = order.algo_buy(self.symbol, algorithm='7a6228ad-dc9d-4377-8b2e-99e8ebb90152', intent='increase', order_quantity=100, price=md.L1.ask+0.01, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                buy_BATS2 = order.algo_buy(self.symbol, algorithm='7a6228ad-dc9d-4377-8b2e-99e8ebb90152', intent='increase', order_quantity=100, price=md.L1.ask+0.02, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                buy_ARCA1 = order.algo_buy(self.symbol, algorithm='97a91492-1033-4a96-a546-9bff6df73b08', intent='increase', order_quantity=100, price=md.L1.ask+0.01, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                buy_ARCA2 = order.algo_buy(self.symbol, algorithm='97a91492-1033-4a96-a546-9bff6df73b08', intent='increase', order_quantity=100, price=md.L1.ask+0.02, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                service.write_file('UNIT_ST_MKT_ORDER_IMBALANCE.txt','{},{},{},{},{}'.format(event.timestamp, self.symbol, md.L1.bid, md.L1.ask, md.L1.last), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                pass;
            # CAPTURE PL IF THERE IS A SPREAD.
            if(account[self.symbol].position.mtm_price<md.L1.bid and account[self.symbol].position.shares!=0):
                chk_position_PL = self.pmt_functions(event, md, order, service, account);
                pass;
            # CLOSE POSTITION IF IT MOVES 9BPS VS. POS.
            if(account[self.symbol].position.mtm_price*1.0009>md.L1.ask and account[self.symbol].position.shares>20):
                chk_position_PL = self.pmt_functions(event, md, order, service, account);
                pass;
            # CHECK IF THE TRADE CYCLE IS COMPLETE.    
            if(account[self.symbol].position.shares==0 and account[self.symbol].pending.capital_short!=0):
                order.cancel(self.symbol)
                pass;
            
            pass;
        
        return;
        
    def pmt_functions(self, event, md, order, service, account):
        if(account[self.symbol].position.shares>200):
            sell_NQ1 = order.algo_sell(self.symbol, algorithm='09528d6b-7d4f-4cc2-8611-8bbecb33785c', intent='decrease', order_quantity=100, price=md.L1.ask-0.0001, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
            sell_NQ2 = order.algo_sell(self.symbol, algorithm='09528d6b-7d4f-4cc2-8611-8bbecb33785c', intent='decrease', order_quantity=100, price=md.L1.bid-0.0002, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
            pass;
            
        if(account[self.symbol].position.shares>200):
            sell_AK1 = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=100, price=md.L1.ask-0.0001, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
            sell_AK2 = order.algo_sell(self.symbol, algorithm='c982d0cd-9be5-4a35-b89f-1f66b2495ec4', intent='decrease', order_quantity=100, price=md.L1.bid-0.0002, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
            pass;
            
        if(account[self.symbol].position.shares>200):
            sell_BT1 = order.algo_sell(self.symbol, algorithm='f8328375-d95c-4c10-aa7e-0c7fecf13336', intent='decrease', order_quantity=100, price=md.L1.ask-0.0001, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
            sell_BT2 = order.algo_sell(self.symbol, algorithm='f8328375-d95c-4c10-aa7e-0c7fecf13336', intent='decrease', order_quantity=100, price=md.L1.bid-0.0002, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
            pass;
            
    def eod_functions(self, event, md, order, service, account):
        if(event.timer_id=="eod_1"):
            if(len(account[self.symbol].pending.orders)>0):
                order.cancel(self.symbol)
                return 1;
                
        elif(event.timer_id=="eod_2"):
            if(account[self.symbol].position.shares>0):
                closeLongPos = order.algo_sell(self.symbol, algorithm='09528d6b-7d4f-4cc2-8611-8bbecb33785c', intent='exit', user_key=3, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                return closeLongPos;
                    
            if(account[self.symbol].position.shares<0):
                closeShort = order.algo_buy(self.symbol, algorithm='4ad20d14-aacb-4850-9efe-cfa92d154304', intent='exit', user_key=4, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                return closeShort;
        return 0;



    @classmethod
    def using_extra_symbols(cls, symbol, md, service, account):
        return md.stat.prev_close>75.00 and md.stat.atr>5 and md.stat.avol>400000;
        return False 

    def _on_feedback(self, md, service, account):
        return '%s, %s, %s, %s' % (account.realized_entry_pl+account.unrealized_entry_pl, account.realized_entry_pl, account.unrealized_entry_pl, self.__class__.MAX_ARCA4_LOSS)
