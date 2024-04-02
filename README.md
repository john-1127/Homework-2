# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

profitable path: tokenB->tokenA->tokenD->tokenC->tokenB

swap1:

    amountBIn: 5

    amountAOut: 5.655321988655322

swap2:

    amountAIn: 5.655321988655322

    amountDOut: 2.458781317097934

swap3:

    amountDIn: 2.458781317097934

    amountCOut: 5.088927293301516

swap4:

    amountCIn: 5.088927293301516

    amountBOut: 20.129888944077447

final reward: 20.129888944077447

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

在AMM中，資產價格是通過代幣儲備量的函數來確定的。例如，Uniswap使用以下公式來保持代幣儲備的恆定乘積: x*y = k。其中x和y分別是兩種代幣的儲備量，而k是常數。當進行交易時，這些儲備量會改變，進而改變代幣的價格。如果交易量大，那麼儲備量的變化也大，導致價格和初始價格相比有較大的滑動，從而產生slippage。

Uniswap V2通過允許用戶設定交易的最小接受量來解決或減輕slippage issue。用戶在提交交易前可以指定一個最小接收量（amountOutMin）。如果交易因為市場波動導致實際接收的代幣量低於這個閾值，那麼交易將會失敗，從而保護用戶不會因高滑點而進行不利的交易。

function as an example: if amountOut < amountOunMin: transaction failed.

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

在Uniswap V2中，當首次向新的流動性池提供流動性時，會從提供者獲得的流動性代幣中扣除最小流動性1000單位。

理由：
1. 避免除以零的錯誤：AMM模型中，價格是通過代幣儲備量的比例來計算的。Uniswap利用的是恆定乘積公式x*y = k。如果池中任一代幣的儲備量為零，可能會導致除以零的錯誤。通過保證池子中始終存在一定數量的流動性，可以避免這類問題的發生。

2. 設置初始價格：首次為流動性池鑄造流動性代幣時，扣除的最小流動性有助於設定初始的代幣價格。這使得流動性提供者必須根據他們期望的初始價格比率來存入代幣，從而簡化了價格的初始設置過程。

3. 擁有權的標記：被永久鎖定在合約中的這1000單位流動性代幣，實際上作為一種標記，表示該池已經被初始化。這種機制還確保了合約地址的一致性和唯一性，因為流動性代幣的首次鑄造是根據提供的資金計算出來的。

4. 增加安全性：這種方式要求即使是小額的流動性提供者也必須認真考慮初始價格，因為他們無法回收這1000單位的流動性代幣。這一機制避免了輕率地添加和移除流動性，這可能會對池子的價格穩定性產生影響。

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

1. 公平性：通過這種方式，確保新加入的流動性提供者獲得的流動性代幣數量與其所提供的資金相對於池中已有資金的比例公平相符。這樣避免了早期和晚期流動性提供者之間的不公平情況。

2. 維持價格穩定：按比例鑄造流動性代幣可以保證池中資金的比例不會因為新加入的流動性而改變，這有助於維持交易對的價格穩定。如果新的流動性沒有按現有比例加入，將會立即影響價格，可能導致臨時的市場不穩定或被套利。

3. 防止slippage與Arbitrage：此方法還有助於防止大量流動性突然加入或退出時造成的市場slippage，因為任何新增的流動性都必須與現有流動性保持一定的比例關係。這樣可以減少因比例失衡而導致的arbitreage opportunity，保護流動性提供者的利益。

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

這種攻擊發生於當攻擊者發現一個即將進行的大額交易時，他們會在該交易之前和之後，快速進行兩筆交易，從而利用受害者交易引起的市場價格波動賺取利潤。

可能的影響：
成本增加：交易可能會以比預期更高的價格執行，因為攻擊者的前置交易已經推高了價格。
slippage加劇：此攻擊會增加slippage。
資金損失：攻擊者從中獲利，這些利潤往往直接來自於此交易成本的增加，意即可能會因為攻擊而蒙受直接的資金損失。
