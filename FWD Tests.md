
2023-08-14

#### MAX CAPITAL SET TO 5% ACCOUNT BP FOR EACH SYMBOL.



![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/347de91c-fb86-4242-81b7-8ddb17f0ce99)



** PENDING ORDER MAX ERROR ADJUSTED.


#### RESTART SYSTEM.

** GATES UP TO AVOID THE FAILED PENDING ORDER CHECK ERROR.

account[self.symbol].pending.count_long<37


	LINE 275:  IF	account[self.symbol].pending.count_long<32
	     RETURN
		CANCEL BIDS/ REDUCE RISK


	LINE 326:  IF    account[self.symbol].pending.count_long>38 
	     RETURN
		CANCEL BIDS/ REDUCE RISK

##### ADJUSTED MKT SPREAD [ 1.0036 ]

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/f10d58cd-9b0d-45ce-bc6c-566c8bb78100)

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/b95d9d8f-a39b-428f-80d9-27a87d116af8)

##### RESTART SYSTEM.
**  SELF TRADE ERROR ADJUSTED.

	askRTE PARAM.
	adjustED TO 57bps
![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/3df5dbd2-0857-4a64-ba31-3fea7c4c3a83)

	self.chkHtz

##### RESTART SYSTEM.
**  SELF TRADE ERROR ADJUSTED.

BD_Fauconberg

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/4a8f63df-d4df-475b-bd37-64c457bd6649)


### MAX PENDING ORDER ISSUE ADJUSTED


        #ADDED THIS TO CUT DOWN THE ORDER BOOK [STALE ORDERS]

        if(account[self.symbol].pending.count_long>36):
           adjustBIDS=account[self.symbol].pending.orders; 
           ctPend=len(adjustBIDS);
           while(ctPend>0):
               ctPend-=1; pendingUnit=adjustBIDS[ctPend];
               if(pendingUnit.shares>0):
                   discharge = order.cancel(order_id=pendingUnit.order_id);
                   pass;
           return;

##### RESTART SYSTEM.

**  PENDING ORDER MAX ERROR.
**  MAX CAP ALLOCATION ERROR.
**  SELF TRADE ERROR ADJUSTED.

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/56aba6fb-84ed-47df-a07b-f572c5172c15)


![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/2daf4173-0a91-4c87-b852-56774bd176f7)


![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/3a9be267-ee8b-4479-9b58-fdafa2182bee)


![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/bcec2e22-8368-4f23-9d2f-14c72086a112)

##### CLEAR
--

The only errors/rejects I saw in BD_Fauconberg were the Max Capital errors 
    
- Max Cap / Order set to %/Symbol relative to BP. 
- 252 symbols simultaneously in FWD testing.

** Unit Allocation parameter/ single symbols (limits ttl exposure).
--

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/620a3d72-7d3e-4fce-b021-e830cfdaac84)

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/32a3038d-6f9b-4808-b6f5-f5b5678de32e)

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/246cf8c1-00cc-4d36-aea2-66b9d65faa2a)


![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/b4526fb4-12bf-4322-8f42-70323863c030)


![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/b5fe5629-7998-49de-b3eb-c9d252519a75)


If the symbols in the scope are in "bear" territory, the program doesn't allocate.

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/a5a77712-6ce8-4830-8923-c941de511672)


@slyoung69

I thought there was a data issue yesterday.
I dropped a line of Code in there to automatically buy 1 Share of every ticker in the universe of the System; turned it off after.
- If the symbols in the scope are in "bear" territory, the program doesn't allocate.

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
