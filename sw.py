
import csv
import re

from pprint import pprint

from tools import d6, nd6


grList = ['','靈巧','敏捷','力量','生命','智力','精神']
#abandon, using bcdice

def gr():
    a,b = d6(),d6()
    
    return f'[{a},{b}]->({grList[a]} or {grList[b]})'


def ht_list_gen():
    path = 'sw_htlist.csv'
    mat = []
    with open(path, mode='r', encoding='utf-8') as f:
        rd = csv.reader(f)
        for row in rd:
            val = [int(x) for x in row[1:]]
            mat.append(val)
    return mat
ht_list = ht_list_gen()

def ht_list_match(k,roll):
    if roll == 2:
        return 0
    else:
        return ht_list[k][roll-3]
    
def roll_descr_gen(k,crit,perm_add, f_add,f_fix, extra):
    l = [crit,perm_add,f_add,f_fix,extra]
    rt= f'Key[{k}]'
    if crit:
        rt += f'@{crit}'
    if perm_add:
        rt += f'#{perm_add}'
    if f_add:
        rt += f'$+{f_add}'
    if f_fix:
        rt += f'${f_fix}'
    if extra:
        rt += f'+{extra}'
    rt += ":\n"
    return rt

def roll_dm(k,crit=13,perm_add=0, f_add=0,f_fix=0, extra=0)-> str:
    roll_descr = roll_descr_gen(k,crit,perm_add, f_add, f_fix, extra)
    

    #-sec1:First roll
    roll_ls = []
    roll_sum_ls = []
    dmg_ls = []
    
    #first roll start.
    a,b = d6(),d6()
    if a+b == 2:
        return roll_descr + f'2d: [(1, 1)] > 自動失敗'
    roll_ls.append((a,b))
    if f_fix:
        roll_first = f_fix
    else:
        roll_first = a + b + f_add + perm_add
    if roll_first >= 12:
        roll_first = 12
    roll_sum_ls.append(roll_first)

    
    if roll_first < crit:
        # End event #1 no crit first roll
        kdmg = ht_list_match(k, roll_first)
        return roll_descr + f'2d: [{roll_ls[0]}] = {roll_sum_ls[0]} > {kdmg} + {extra} > {kdmg+extra}'
    
    dmg_ls.append(ht_list_match(k,roll_first))
    
    #-sec2: Crit events
    while True:
        a,b = d6(),d6()
        roll_ls.append((a,b))
        if a+b == 2:
            roll_sum_ls.append(2)
            dmg_ls.append(0)
            break
        roll_sum = a + b + perm_add
        if roll_sum >= 12:
            roll_sum = 12
        roll_sum_ls.append(roll_sum)
        dmg_ls.append(ht_list_match(k,roll_sum))
        if a+b+perm_add < crit:
            break
    roll_ls_str = [str(i) for i in roll_ls]
    roll_sum_str = [str(i) for i in roll_sum_ls]
    dmg_ls_str = [str(i) for i in dmg_ls]

    return roll_descr + f'2d: [{" ".join(roll_ls_str)}] = {",".join(roll_sum_str)} > {",".join(dmg_ls_str)} + {extra} > {len(dmg_ls)-1}回轉 > {sum(dmg_ls)+extra}'
     
def comment_parse(comm):
    pattern = r"[Kk](\d+)(?:@(\d+))?(?:#(\d+))?(?:\$(\d+))?(?:\$\+(\d+))?(?:\+(\d+))?"

    match = re.match(pattern, comm)
    crit, perm_add, f_add, f_fix, extra = 13,0,0,0,0
    if match:
        groups = match.groups()
        print(groups)
        k = int(groups[0])
        crit = int(groups[1]) if groups[1] is not None else 13
        perm_add,f_fix, f_add, extra = [int(t) if t is not None else 0 for t in groups[2:]]

        if k < 0 or k > 100:
            raise ValueError('k value out of range')
        if crit < 3 and crit != 0:
            raise ValueError('Illegal Crit.')
        if perm_add < 0 or perm_add > 10:
            raise ValueError('Illegal perm_add.')
        if f_add < 0 or f_add > 12:
            raise ValueError('Illegal f_add')
        if f_fix != 0 and f_fix < 3 or f_fix > 12:
            raise ValueError('Illegal f_fix')
        if extra < 0:
            raise ValueError('extra damage cant be negative.')
        return roll_dm(k,crit,perm_add,f_add,f_fix,extra)
    else:
        print('Bad format')
        raise ValueError('Value out of range.')

if __name__ == '__main__':
    print(comment_parse('K100@7#1$1'))
    