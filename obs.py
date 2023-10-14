from ast import If
from typing import Self
from cloudquant import Client
from cloudquant.interfaces import Strategy
    



class scr_Account():

  ACCOUNT_BASE=[]

  def on_start(self, md, order, service, account):
        # freeze account value locally and return the snapshot to avoid changes while calc. risk.
        self.get_account_var(md, account)
        
  def reset_Account_Values(self):
        ACCOUNT_BASE=[]
        base_VARS=[0.00] * 13
        for layer in 6:
          ACCOUNT_BASE.append(base_VARS)
        return ACCOUNT_BASE   

    # RETURN LONG POSITION MTM ALLOCATION VALUE
    def get_notional_symbol_long(self, account):
        return account[self.symbol].position.mtm_price*account[self.symbol].position.shares
    def get_notional_symbol_LONG(self, account, _TICKER):
        return account[_TICKER].position.mtm_price*account[_TICKER].position.shares
    # RETURN SHORT POSITION MTM ALLOCATION VALUE
    def get_notional_symbol_short(self, account):
        return abs(account[self.symbol].position.mtm_price*account[self.symbol].position.shares)
    def get_notional_symbol_SHORT(self, account, _TICKER):
        return abs(account[_TICKER].position.mtm_price*account[_TICKER].position.shares)
    # RETURN BETA EXPOSURE OF A LONG POSITION
    def get_beta_symbol_long(self, md, account):
        exp_LONG = self.get_notional_symbol_long(account)
        return exp_LONG*md.stat.beta
    def get_beta_symbol_LONG(self, md, account, _TICKER):
        exp_LONG  = self.get_notional_symbol_LONG(account, _TICKER)
        return exp_LONG*md[_TICKER].stat.beta
    # RETURN BETA EXPOSURE OF A POSITION
    def get_beta_symbol_short(self, md, account):
        exp_SHORT = self.get_notional_symbol_short(account)
        return exp_SHORT*md.stat.beta
    def get_beta_symbol_SHORT(self, md, account, _TICKER):
        exp_SHORT  = self.get_notional_symbol_SHORT(account, _TICKER)
        return exp_SHORT*md[_TICKER].stat.beta

    # Total Account PL.
    def get_acct_pl(self, account):
        return account.realized_entry_pl+account.unrealized_entry_pl
    # TTL SYMBOL PL.
    def get_symb_pl(self, account):
        return account[self.symbol].unrealized_pl.entry_pl + account[self.symbol].realized_pl.entry_pl
    # TTL SYMBOL PL.
    def get_symb_PL(self, account, _TICKER):
        return account[_TICKER].unrealized_pl.entry_pl + account[_TICKER].realized_pl.entry_pl


    # LONG POSITION PL.    
    def get_symb_long_pl_pts(self, md, account):
        return md.L1.bid - account[self.symbol].position.mtm_price
    def get_symb_long_pl_pct(self, md, account):
        return self.get_symb_long_pl_pts(md, account) / account[self.symbol].position.mtm_price
    
    # SHORT POSITION PL.    
    def get_symb_short_pl_pts(self, md, account):
        return md.L1.ask - account[self.symbol].position.mtm_price
    def get_symb_short_pl_pct(self, md, account):
        return self.get_symb_short_pl_pts(md, account) / account[self.symbol].position.mtm_price
    
    def get_account_var0(self, ACCOUNT_BASE):
        # [0][0]- HOLDS THE ABSOLUTE TOTAL NOTIONAL LONG AND SHORT POSITIONS (ENTRY VALUE.)
        ACCOUNT_BASE[0][0]=ACCOUNT_BASE[0][1]+ACCOUNT_BASE[0][2]
        # [0][3]- HOLDS THE WEIGHT OF LONG POSITIONS.
        ACCOUNT_BASE[0][3]=ACCOUNT_BASE[0][1]/ACCOUNT_BASE[0][0]
        # [0][4]- HOLDS THE WEIGHT OF SHORT POSITIONS.
        ACCOUNT_BASE[0][4]=ACCOUNT_BASE[0][2]/ACCOUNT_BASE[0][0]        
        # [0][7]- HOLDS THE NET BETA EXPOSURE. (LONG BETA + SHORT BETA)
        ACCOUNT_BASE[0][7]=ACCOUNT_BASE[0][5]+ACCOUNT_BASE[0][6]
        # [0][8]- BETA WEIGHTED LONG EXPOSURE ALLOCATION.
        ACCOUNT_BASE[0][8]=ACCOUNT_BASE[0][5]/ACCOUNT_BASE[0][1]
        # [0][9]- BETA WEIGHTED SHORT EXPOSURE ALLOCATION.
        ACCOUNT_BASE[0][9]=-ACCOUNT_BASE[0][6]/ACCOUNT_BASE[0][2]
        # [0][10]- NET LONG AND SHORT EXPOSURE ($LONG - $SHORT)
        ACCOUNT_BASE[0][10]=ACCOUNT_BASE[0][1]-ACCOUNT_BASE[0][2]
        # [0][11]- (BETA WEIGHTED NET RISK)
        ACCOUNT_BASE[0][11]=ACCOUNT_BASE[0][7]/ACCOUNT_BASE[0][10]
        # [0][12]- (ABSOLUTE WEIGHTED BETA RISK - BASIS OF TOTAL CAPITAL AT RISK)
        ACCOUNT_BASE[0][12]=ACCOUNT_BASE[0][7]/ACCOUNT_BASE[0][0]        
        return ACCOUNT_BASE

    def get_account_var(self, md, account):
        ACCOUNT_BASE=self.reset_Account_Values()

        # ITERATE ALL POSITIONS AND TOTAL UP LONG AND SHORT EXPOSURE PL.
        for TICKER in account.open_symbols:
            if(account[TICKER].position.shares>0):
                # VAR LONG.
                ACCOUNT_BASE[0][1]+=self.get_notional_symbol_LONG(account,TICKER)
                ACCOUNT_BASE[0][5]+=self.get_beta_symbol_LONG(account,TICKER)
                # PL
                ACCOUNT_BASE[1][1]+=account[TICKER].position.capital_long
                ACCOUNT_BASE[1][3]+=account[TICKER].position.shares
                ACCOUNT_BASE[1][5]+=self.get_symb_PL(account,TICKER)
                pass
            elif(account[TICKER].position.shares<0):
                # VAR SHORT.
                ACCOUNT_BASE[0][2]+=self.get_notional_symbol_SHORT(account,TICKER)
                ACCOUNT_BASE[0][6]-=self.get_beta_symbol_SHORT(account,TICKER)
                # PL
                ACCOUNT_BASE[1][2]+=abs(account[TICKER].position.capital_short)
                ACCOUNT_BASE[1][4]+=abs(account[TICKER].position.shares)
                ACCOUNT_BASE[1][6]+=self.get_symb_PL(account,TICKER)
                pass

        self.get_account_var0()

        ACCOUNT_BASE[1][0]=ACCOUNT_BASE[1][1]+ACCOUNT_BASE[1][2]
        # [1][0]- HOLDS THE ABSOLUTE TOTAL PL OF LONG AND SHORT POSITIONS.
        ACCOUNT_BASE[1][7]=self.get_acct_pl(account)
        ACCOUNT_BASE[1][8]=abs(ACCOUNT_BASE[1][5]/ACCOUNT_BASE[1][0])
        ACCOUNT_BASE[1][9]=abs(ACCOUNT_BASE[1][6]/ACCOUNT_BASE[1][0])
        ACCOUNT_BASE[1][10]=ACCOUNT_BASE[1][3]-ACCOUNT_BASE[1][4]


        
    # Account Holdings: Share Quantities.
    #   [0] - Total Account (Absolute) Shares.
    #   [1] - Total Long Share Quantity.
    #   [2] - Total Short Shares Quantity.
