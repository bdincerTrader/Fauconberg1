@slyoung69


If the symbols in the scope are in "bear" territory, the program doesn't allocate.

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/a5a77712-6ce8-4830-8923-c941de511672)



I thought there was a data issue yesterday.
- I dropped a line of Code in there to automatically buy 1 Share of every ticker in the universe of the System; turned it off after.
- If the symbols in the scope are in "bear" territory, the program doesn't allocate. ****

GTG. 100%

##### LINE 160
*** MAINTAINS A FRESH ORDER BOOK
cancels the pending book it it approaches 30 orders.


##### LINE 224
*** WILL  CLOSE THE POSITION AND DE-LIST THE SYMBOL IF IT TURNS INTO A ( - ) or [ - ]
IF self.safetySymbol=750.. There's no coming back (it is unsubscribed for the remainder of the session).


##### LINE 267

*** MAKES SURE self.limitBP>0 and len(account[self.symbol].pending.orders)<30

    self.limitBP =   self.order_quantity_max  -   account[self.symbol].position.capital_long  -  account[self.symbol].pending.capital_long;

    self.order_quantity_max = % of account BP (parameter accountBP/maxSymbolTrade);

*** I can adjust this later to dynamically adjust, in case the [ + ] grows at a certain rate.


##### LINE 290
*** Runs the same risk check as # LINE 267 before submitting any orders.

-------------

EXAMPLE, LIMIT BP.

HASH: 4424ad0c39f5fa5c0be97862df577cc1
    limitBP= $3,000,000
    accountBP=$15,000,000
    maxSymbolTrade=5

/s/ BD.



--

***** 

## LONG ONLY SYSTEM.


If the symbols in the scope are in "bear" territory, the program doesn't allocate.

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/a5a77712-6ce8-4830-8923-c941de511672)



****** NO ORDERS 8/16 OR 8/17 (AS OF CURRENT)

   
### QQQ

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/f95f7686-877d-4395-8a1f-f3d6763f92bd)


### SPY
![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/6196a24c-c272-4d31-8ae5-bee5e804c06c)


### SETS
    
tickerItrA=['FNGU','TMO','ELV','DDS','GS','TSLA','NFLX','INSP','PANW','PLPC','FIVE','FICO','ZBRA','ASML','SMCI','TMV','URI','FNGU','SPOT','MSCI','EQIX','MSTR','MELI','PH','ACN','ADBE','ADSK','ALB','ALGN','ALNY','AMD','AMP','AMT','ANET','ANSS','AON','APD','ARGX','ASML','AVGO','AZO','BA','BDX','BIDU','BIIB','BILL','BKNG','BLK','MPWR','BURL','CAR','CAT','CDNS','CELH','CHTR','CI','CMG','CMI','COIN','COST','CRWD','CSL','CTAS','CVNA'];
    
tickerItrB = ['GS','MPWR','TMO','ELV','DDS','ORLY','MSCI','EQIX','MSTR','MELI','BKNG','PH','INSP','PANW','PLPC','FIVE','AVGO','URI','FNGU','SPOT','TFX','WING','GWW','LLY','MSCI','URI','FSLR','SWAV','GUSH','REGN','PANW','FIVE','FICO','ZBRA','ASML','SMCI','TMV','LRCX','ACLS','FCNCA','CMG','GS','MPWR','TMO','ELV','DDS','ORLY','MSCI','EQIX','MSTR','MELI','BKNG','PH','INSP','PANW','PLPC','FIVE','AVGO','URI','FNGU','SPOT','TFX','WING','GWW','LLY','MSCI','URI','FSLR','SWAV','GUSH','REGN','PANW','FIVE','FICO','ZBRA','ASML','SMCI','TMV','LRCX','ACLS','FCNCA','CMG'];
    
tickerItrC = ['ACN','ADBE','ADSK','ALB','ALGN','ALNY','AMD','AMP','AMT','ANET','ANSS','AON','APD','ARGX','ASML','AVGO','AZO','BA','BDX','BIDU','BIIB','BILL','BKNG','BLK','BRK.A','BURL','CAR','CAT','CDNS','CELH','CHTR','CI','CMG','CMI','COIN','COST','CRWD','CSL','CTAS','CVNA','DDOG','DE','DECK','DHR','DPST','DPZ','ELF','ELV','ENPH','EPAM','EQIX','ESS','FCNCA','FDS','FICO','FNGU','FSLR','GNRC','GS','GWW','HCA','HUBB','HUBS','HUM','ICLR','IDXX','IGV','ILMN','INSP','INTU','ISRG','IT','ITW','KLAC','LII','LIN','LLY','LMT','LPLA','LRCX','LULU','MA','MCK','MCO','MDB','MDY','MELI','META','MLM','MOH','MPWR','MSCI','MSFT','MSI','MSTR','MTD','NFLX','NOC','NOW','NVDA','NVR','NXPI','ODFL','OIH','ORLY','PANW','PAYC','PEN','PH','PODD','POOL','PSA','PXD','REGN','RETA','RGEN','RH','RMD','ROK','ROKU','ROP','SAIA','SBAC','SEDG','SHW','SIMO','SMCI','SN','SNOW','SNPS','SOXX','SPGI','SPOT','STE','SYK','TDG','TDY','TEAM','TMO','TSCO','TSLA','ULTA','UNH','UPST','URI','VGT','VRTX','W','WAT','WCC','WDAY','WSO','WST','ZBRA','ZS'];

tickerItrD = ['SAM','VMI','TYL','MUSA','BLD','BIO','RS','COO','NICE','EG','HII','KRTX','LAD','TFX','WIRE','JLL','CYBR','MEDP','GLOB','FCN','UTHR','SWAV','MKTX','MSGS','CRL','PCTY','RNR','ARCB','DUOL'];

tickerItrE=['ACN','ADBE','ADSK','ALB','ALGN','ALNY','AMD','AMP','AMT','ANET','ANSS','AON','APD','ARGX','ASML','AVGO','AZO','BA','BDX','BIDU','BIIB','BILL','BKNG','BLK','BRK.A','BURL','CAR','CAT','CDNS','CELH','CHTR','CI','CMG','CMI','COIN','COST','CRWD','CSL','CTAS','CVNA'];

tickerItrF=['DDOG','DE','DECK','DHR','DPST','DPZ','ELF','ELV','ENPH','EPAM','EQIX','ESS','FCNCA','FDS','FICO','FNGU','FSLR','GNRC','GS','GWW','HCA','HUBB','HUBS','HUM','ICLR','IDXX','IGV','ILMN','INSP','INTU','ISRG','IT','ITW','KLAC','LII','LIN','LLY','LMT','LPLA','LRCX'];

tickerItrG=['MPWR','TMO','ELV','DDS','ORLY','MSCI','EQIX','MSTR','MELI','BKNG','PH','INSP','PANW','PLPC','FIVE','AVGO','URI','FNGU','SPOT','TFX','WING','GWW','LLY','MSCI','GS','MPWR','TMO','ELV','DDS','ORLY','MSCI','EQIX','MSTR','MELI','BKNG','PH','INSP','PANW','PLPC','FIVE','AVGO','URI','FNGU','SPOT','TFX','WING','GWW','LLY','MSCI','URI','FSLR','SWAV','LULU','MA','MCK','MCO','MDB','MDY','MELI','META','MLM','MOH','MPWR','MSCI','MSFT','MSI','MSTR','MTD','NFLX','NOC','NOW','NVDA','NVR','NXPI','ODFL','OIH','ORLY','PANW','PAYC','PEN','PH','PODD','POOL','PSA','PXD','REGN','RETA','RGEN','RH','RMD','ROK','ROKU'];
    
tickerItrH=['ROP','SAIA','SBAC','SEDG','SHW','SIMO','SMCI','SN','SNOW','SNPS','SOXX','SPGI','SPOT','STE','SYK','TDG','TDY','TEAM','TMO','TSCO','TSLA','ULTA','UNH','UPST','URI','VGT','VRTX','W','WAT','WCC','WDAY','WSO','WST','ZBRA','ZS'];
     
### BACKTEST SUMMARY

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/25b76d2a-e805-4c4f-af45-a39132ece9cf)
