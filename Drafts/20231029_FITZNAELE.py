# Editor
# tricolumnFitzneale   BDincer   10/27/2023 12:33:56 PM   QA-2.0.239
# N-00006   qabdincer/d1c248
# Voodoo=9e6b50d6-dee3-4314-a43b-49e9ae8088b6 Buy Market GS SOR
# Voodoo=09528d6b-7d4f-4cc2-8611-8bbecb33785c Sell Limit NASD SCAN at Script Price
# Voodoo=8fa5330d-b32d-4083-86eb-d9a61a637b8b Sell Market GS SOR
# Voodoo=398a38ee-b614-4678-90a6-dbf40d2a54b9 Sell Market BATS
# Voodoo=5fc61945-3498-47da-abf6-b5dabdc9f4ac Sell Market NASD
# Voodoo=8fdee8fe-b772-46bd-b411-5544f7a0d917 Sell Market ARCA
# Voodoo=1f9b553d-30bf-40a3-8868-ebe70b5079b2 Buy Market NASD

from cloudquant.interfaces import Strategy
import time, datetime, random, io, csv

class Gr8Scripte26cb7cc28424c93ad4a500576ab1541(Strategy):
    __script_name__ = 'tricolumnFitzneale'
    
    FITZ_BBS='SHORTBOOK888.txt';
    FITZ_CLOCK=45;
    MAX_ACCOUNT_LOSS_FITZ=4000;
    MAX_SYMBOL_LOSS_FITZ =1000;
    FITZ_IDX=0;
    LOG_ACCOUNT_PERFORMANCE=0.00;

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        return md.stat.prev_close>20.00 and (md.stat.avol * md.stat.prev_close > 100000001) and md.stat.exchange in ["Q","Z","A","P","N","T","J","K"];
        
    def __init__(self, **params):
        
        if('FITZ_BBS' in params):
            self.__class__.FITZ_BBS=params['FITZ_BBS'];
            self.__class__.FITZ_TIMER=params['FITZ_TIMER'];
            self.__class__.MAX_ACCOUNT_LOSS_FITZ=params['MAX_ACCOUNT_LOSS_FITZ'];
            self.__class__.MAX_SYMBOL_LOSS_FITZ=params['MAX_SYMBOL_LOSS_FITZ'];
            pass;

    def on_start(self, md, order, service, account):
    
        # NEW RISK SETTINGS OBJECTS
        self.account_risk_setting={'pending_notional': 750000, 'pending_long_notional': 750000, 'pending_short_notional': 750000, 'position_notional': 750000, 'position_long_notional': 750000, 'position_short_notional': 750000}
        self.symbol_risk_settings={'pending_notional': 375750, 'pending_long_notional': 375750, 'pending_short_notional': 375750, 'position_notional': 375750, 'position_long_notional': 375750, 'position_short_notional': 375750}
    
        ## SYSTEM LOGS.
        self.fileSystemLOG_TF = service.time_to_string(service.system_time, '%Y-%m-%d')+'FITZ_SYSTEM_LOG'+self.__class__.FITZ_BBS;
        
        # PARAMETERS.
        self.shortSTAT=0;
        self.FITZ_CLOCK = self.__class__.FITZ_TIMER;
        self.FITZ_PROMPTER = service.time_to_string(service.system_time, '%Y-%m-%d')+self.__class__.FITZ_BBS;

        # ALLOCATION HOURS.
        self.liquid_time = md.market_open_time + service.time_interval(minutes=30)
        self.illiquid_time = md.market_close_time - service.time_interval(hours=2)
        
        if(self.symbol=='CASH'):
            service.write_file(self.fileSystemLOG_TF,'{},{},{},{},{},{},{},{}'.format('STAT', 'symbol', 'DATE-TIME','MAX_ACCOUNT_LOSS_FITZ','MAX_SYMBOL_LOSS_FITZ','FITZ_BBS','FITZ_TIMER','FILE_PROMPTER'), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
            pass;
        service.write_file(self.fileSystemLOG_TF,'{},{},{},{},{},{},{},{}'.format(self.shortSTAT, self.symbol, service.time_to_string(service.system_time), self.__class__.MAX_ACCOUNT_LOSS_FITZ, self.__class__.MAX_SYMBOL_LOSS_FITZ, self.__class__.FITZ_BBS, self.__class__.FITZ_TIMER, self.FITZ_PROMPTER), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });

        # SYSTEM TIMERS
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes=10), repeat_interval=service.time_interval(seconds=self.FITZ_CLOCK), timer_id="Observe")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=45), timer_id = "eod_1")
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes=12), timer_id = "eod_2")
        pass;

    def on_timer(self, event, md, order, service, account):
        
        # [1].  CHECK THE PERFORMANCE OF THE ACCOUNT AND SYMBOL.
        #       In Production: account performance uses an unknown value to determine the current symbol value.
        #       (?) Possibly uses a logic of Last Price and Ask Price.
        
        symbolPerformanceShort = account[self.symbol].unrealized_pl.entry_pl + account[self.symbol].realized_pl.entry_pl;
        accountPerformance = account.realized_entry_pl+account.unrealized_entry_pl
        if(self.symbol=='CASH'):
            self.__class__.LOG_ACCOUNT_PERFORMANCE=account.realized_entry_pl+account.unrealized_entry_pl;
            return;

        # [2].  MAX ACCOUNT LOSS PARAMETER.
        #       [1].    CANCELS ALL PENDING ORDER.
        #       [2].    CLOSE THE POSITION.
        #       [3].    TERMINATE THE SERVICE ON THE SYMBOL.
        
        if(account.realized_entry_pl+account.unrealized_entry_pl<-self.__class__.MAX_ACCOUNT_LOSS_FITZ or symbolPerformanceShort<-self.__class__.MAX_SYMBOL_LOSS_FITZ):
            self.shortSTAT==1;
            if(len(account[self.symbol].pending.orders)>0):
                cancel_pending_symbol_orders = order.cancel(self.symbol);
                service.write_file(self.fileSystemLOG_TF,'{},{},{},{},{},{},{},{},{},{}'.format(self.shortSTAT, self.symbol, service.time_to_string(service.system_time), self.__class__.MAX_ACCOUNT_LOSS_FITZ, self.__class__.MAX_SYMBOL_LOSS_FITZ, self.__class__.FITZ_BBS, self.__class__.FITZ_TIMER, self.FITZ_PROMPTER, symbolPerformanceShort, accountPerformance), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                return cancel_pending_symbol_orders;
            elif(account[self.symbol].position.shares<0):
                self.shortSTAT=1;
                CLOSE_POSITION = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=888, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                service.write_file(self.fileSystemLOG_TF,'{},{},{},{},{},{},{},{},{},{}'.format(self.shortSTAT, self.symbol, service.time_to_string(service.system_time), self.__class__.MAX_ACCOUNT_LOSS_FITZ, self.__class__.MAX_SYMBOL_LOSS_FITZ, self.__class__.FITZ_BBS, self.__class__.FITZ_TIMER, self.FITZ_PROMPTER, symbolPerformanceShort, accountPerformance), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                return CLOSE_POSITION;
            elif(len(account[self.symbol].pending.orders)==0 and account[self.symbol].position.shares==0):
                service.write_file(self.fileSystemLOG_TF,'{},{},{},{},{},{},{},{},{},{}'.format('TERMINATE SYMBOL', self.symbol, service.time_to_string(service.system_time), self.__class__.MAX_ACCOUNT_LOSS_FITZ, self.__class__.MAX_SYMBOL_LOSS_FITZ, self.__class__.FITZ_BBS, self.__class__.FITZ_TIMER, self.FITZ_PROMPTER, symbolPerformanceShort, accountPerformance), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                service.terminate();
                return 0;
            pass;
            
        # [3].  CHECK THE PERFORMANCE OF THE SYMBOL.
        if(account[self.symbol].position.shares<0 or self.shortSTAT==1 and event.timestamp>self.liquid_time):
            risk77bps = account[self.symbol].position.mtm_price * -0.0077;
            risk77px1 = account[self.symbol].position.mtm_price - md.L1.bid;
  
            # [1. SHORT- DEMIT THE POSITION AND LOCK IT DOWN]
            if(risk77px1 < risk77bps or self.shortSTAT==1):
                if(len(account[self.symbol].pending.orders)>0):
                    order.cancel(self.symbol);
                    pass;
                elif(account[self.symbol].position.shares<0):
                    self.shortSTAT=1;
                    CLOSE_POSITION = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=888, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                    pass;
                pass;
            pass;

            # [2. SHORT- CAPTURE P&L IN EXCESS OF THE SPREAD]
            chkSPR = (md.L1.ask-md.L1.bid)/2;
            if( account[self.symbol].position.mtm_price-md.L1.ask > chkSPR and account[self.symbol].position.shares<0 and event.timestamp>self.liquid_time):
                chk77_SHORT = int( abs(account[self.symbol].position.shares) * 0.16)
                CAPTURE_SHORT_PL = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=max(1,chk77_SHORT), user_key=666, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                pass;
            pass;    
    
        # [4]
        if event.timer_id=="eod_1":
            if(len(account[self.symbol].pending.orders)>0):
                order.cancel(self.symbol);
                pass;
            return 0;
        if event.timer_id=="eod_2":
            if(account[self.symbol].position.shares<0):
                CLOSE_EOD_POSITION = order.algo_buy(self.symbol, algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[self.symbol].position.shares), user_key=888, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                return CLOSE_EOD_POSITION;
            elif(account[self.symbol].position.shares>0):
                closeLongPos = order.algo_sell(self.symbol, algorithm='09528d6b-7d4f-4cc2-8611-8bbecb33785c', intent='exit', user_key=1, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);
                return closeLongPos;
            return 1;
            
        # [5].  [CHECKS IF THE SYMBOL HAS BEEN LOCKED DOWN FOR THE REST OF THE SESSION.]
        if(self.shortSTAT==1):
            return;

        # [6]
        if(event.timestamp>self.liquid_time):
        
            looking_for_eboftf = service.read_file(self.FITZ_PROMPTER, path = {'FORWARD': '/mnt/userdata/bdincer/','PRODUCTION': '/mnt/userdata/bdincer/'});
            prompterSHORT = csv.DictReader(io.StringIO(looking_for_eboftf));
            i=0;

            for row in prompterSHORT:
                i+=1;

                if(i>self.__class__.FITZ_IDX):
                    self.__class__.FITZ_IDX+=1;
                    if(row['CODE']=='666'):
                        sor_unitB1 = order.algo_sell(row['TICKER'], algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=int(row['CODE_QTY']), user_key=661, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                        bat_unitB1 = order.algo_sell(row['TICKER'], algorithm='398a38ee-b614-4678-90a6-dbf40d2a54b9', intent='increase', order_quantity=int(row['CODE_QTY']), user_key=662, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                        ndq_unitB1 = order.algo_sell(row['TICKER'], algorithm='5fc61945-3498-47da-abf6-b5dabdc9f4ac', intent='increase', order_quantity=int(row['CODE_QTY']), user_key=663, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                        arc_unitB1 = order.algo_sell(row['TICKER'], algorithm='8fdee8fe-b772-46bd-b411-5544f7a0d917', intent='increase', order_quantity=int(row['CODE_QTY']), user_key=664, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                        pass;
                    elif(row['CODE']=='888.555'):
                        if(account[row['TICKER']].position.capital_short!=0):
                            CLOSE_POSITION = order.algo_buy(row['TICKER'], algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=abs(account[row['TICKER']].position.shares), user_key=888, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                            pass;
                        pass;
                    elif(row['CODE']=='1407.151'):
                        # THIS CODE WILL REDUCE THE POSITION.
                        if(account[row['TICKER']].position.capital_short!=0):
                            REDUCE_POSITION151 = order.algo_buy(row['TICKER'], algorithm='9e6b50d6-dee3-4314-a43b-49e9ae8088b6', intent='decrease', order_quantity=min(abs(account[row['TICKER']].position.shares), abs(int(row['CODE_QTY']))), user_key=1408, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                            pass;
                        pass;
                    elif(row['CODE']=='1407.555'):
                        # THIS CODE WILL REDUCE THE POSITION.
                        if(account[row['TICKER']].position.capital_short!=0):
                            REDUCE_POSITION555 = order.algo_buy(row['TICKER'], algorithm='1f9b553d-30bf-40a3-8868-ebe70b5079b2', intent='decrease', order_quantity=min(abs(account[row['TICKER']].position.shares), abs(int(row['CODE_QTY']))), user_key=1407, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                            pass;
                        pass;
                    elif(row['CODE']=='1407.666'):
                        if(account[row['TICKER']].position.capital_short!=0):
                            REDUCE_POSITION1407 = order.algo_sell(row['TICKER'], algorithm='8fa5330d-b32d-4083-86eb-d9a61a637b8b', intent='increase', order_quantity=min(abs(account[row['TICKER']].position.shares), abs(int(row['CODE_QTY']))), user_key=666, allow_multiple_pending=10, account_risk_settings=self.account_risk_setting, symbol_risk_settings=self.symbol_risk_settings);  
                            pass;
                        pass;
                    
                    service.write_file(self.fileSystemLOG_TF,'{},{},{},{},{},{},{}'.format(i, self.__class__.FITZ_IDX, row['TICKER'], row['MIDPX'], row['CODE'], event.timestamp, self.illiquid_time), mode = 'append', path = {'FORWARD': '/mnt/userdata/bdincer/', 'PRODUCTION': '/mnt/userdata/bdincer/' });
                    pass;
                pass;
            return 1;
        return 0;
        
        

    @classmethod
    def using_extra_symbols(cls, symbol, md, service, account):
        return symbol in ['SPY', 'QQQ'];
        return False 

    def _on_feedback(self, md, service, account):
        return '%s, %s, %s, %s, %s, %s, %s' % (account.unrealized_entry_pl+account.realized_entry_pl, account.unrealized_entry_pl, account.realized_entry_pl, self.__class__.MAX_ACCOUNT_LOSS_FITZ, account.unrealized_mtm_pl, account.entry_pl, account.realized_entry_pl)
