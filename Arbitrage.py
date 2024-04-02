from itertools import permutations
from itertools import chain, combinations

liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}



def all_combinations(elements):
    return list(chain.from_iterable(combinations(elements, i) for i in range(1, len(elements)+1)))


def all_path(elements):
    results=[]
    all_combos = all_combinations(elements) 
    for combo in all_combos:
        a = permutations(combo) 
        for item in a:
            results.append(item)
    return results


def swap(token_in, token_out, amount_in, liquidity):
    amount_in_fee = amount_in * 0.997
    if (token_in, token_out) in liquidity:
        reserve_in, reserve_out = liquidity[(token_in, token_out)]
        k = reserve_in * reserve_out
        balance0 = reserve_in + amount_in_fee
        balance1 = k / balance0
        amount_out = reserve_out - balance1
        liquidity[token_in, token_out] = (reserve_in + amount_in, balance1)


    elif (token_out, token_in) in liquidity:
        reserve_out, reserve_in = liquidity[(token_out, token_in)]
        k = reserve_in * reserve_out
        balance0 = reserve_in + amount_in_fee
        balance1 = k / balance0
        amount_out = reserve_out - balance1
        liquidity[token_out, token_in] = (reserve_in + amount_in, balance1)
    else:
        return 0
    
    return amount_out


def find_best(liquidity, all_path, amount_in):
    result = 0
    best_path = ""
    for path in all_path: 
        liquidity_copy = dict(liquidity) 
        full_path = list(("tokenB",) + path + ("tokenB",))
        amount_out = 0
        amount_in_iter = amount_in
        for i in range(len(full_path) - 1):
            token_in = full_path[i]
            token_out = full_path[i+1]
            amount_in_iter = swap(token_in, token_out, amount_in_iter, liquidity_copy)
            amount_out = amount_in_iter
        if amount_out > result :
            result = amount_out
            best_path = path
    return result, best_path



path = all_path(["tokenA", "tokenC", "tokenD", "tokenE"])
result, path = find_best(liquidity, path, 5)
answer = "tokenB->"
for item in path:
    answer = answer + item + "->"
answer = answer + "tokenB"
print(f'{answer}, token balance={result}')
# print()
# amount_out = swap("tokenB", "tokenA", 5, liquidity)
# print(amount_out)
# print(liquidity)
# amount_out = swap("tokenA", "tokenD", amount_out, liquidity)
# print(amount_out)
# print(liquidity)
#
# amount_out = swap("tokenD", "tokenC", amount_out, liquidity)
# print(amount_out)
# print(liquidity)
#
# amount_out = swap("tokenC", "tokenB", amount_out, liquidity)
# print(amount_out)
# print(liquidity)
