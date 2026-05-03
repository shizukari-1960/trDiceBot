import re
from tools import dn,eval_eq

def roll_inf(comm:str) -> str:
    comm = comm.split(' ')[0]
    com = comm.split('+',1)
    pl = 0
    if len(com) > 1:
        try:
            pl = eval_eq(com[1])
        except:
            return 'Bad format.'
    
    pattern = r"\.(\d+)wd(\d+)?"
    match = re.search(pattern,com[0], re.IGNORECASE)

    #EX:.47wd7+773
    #EX:.4wd

    if match:
        wd, ad = match.groups()
        ad = 10 if ad == None else ad
        wd, ad = int(wd), int(ad)
        
        diceLt = []
        diceLt.append([dn(10) for i in range(wd)])
        
        while True:
            dice_add_set = diceLt[-1]
            temp = [dn(10) for i in dice_add_set if i >= ad]
            if not temp:
                break
            diceLt.append(temp)
        
        
        success = 0
        for dset in diceLt:
            success += len([i for i in dset if i>=8])
        
        return f'{comm} : {diceLt} > {success + int(pl)}成功'
        
        

        



            

    else:
        return None


if __name__ == '__main__':
    for i in range(10):

        print(roll_inf('.7Wd+17-4*(21*7*0.14-4125+15.03**2)'))