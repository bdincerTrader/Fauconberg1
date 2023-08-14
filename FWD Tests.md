
2023-08-14

#### MAX CAPITAL SET TO 5% ACCOUNT BP FOR EACH SYMBOL.



![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/347de91c-fb86-4242-81b7-8ddb17f0ce99)


![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/e918d9ce-69e6-498c-958d-1f7a97a7e5cc)


** PENDING ORDER MAX ERROR ADJUSTED.


#### RESTART SYSTEM.

** I PUT THESE GATES UP TO AVOID THE FAILED PENDING ORDER CHECK ERROR.

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

	

The only errors/rejects I saw in BD_Fauconberg were the Max Capital errors 
    
- Max cap for an order in QA account is 100K. 
- I am running the algo on 252 symbols simultaneously in FWD testing.

** Unit Allocation parameter/ single symbols (limits ttl exposure).
--

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/620a3d72-7d3e-4fce-b021-e830cfdaac84)

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/32a3038d-6f9b-4808-b6f5-f5b5678de32e)

![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/246cf8c1-00cc-4d36-aea2-66b9d65faa2a)


![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/b4526fb4-12bf-4322-8f42-70323863c030)


![image](https://github.com/bdincerTrader/Fauconberg1/assets/127531384/b5fe5629-7998-49de-b3eb-c9d252519a75)





