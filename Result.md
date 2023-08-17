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
