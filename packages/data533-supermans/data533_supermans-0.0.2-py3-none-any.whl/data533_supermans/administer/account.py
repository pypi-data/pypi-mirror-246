# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 21:28:46 2023

@author: Administrator
"""
from data533_supermans.administer import inventory
from data533_supermans.administer.inventory import rollback2
# import customer as c
from datetime import datetime as dt
import sqlite3 
import random


def eliminate(Transaction_class,member_class):
    today=dt.today()
    diff=(today-Transaction_class.transaction_time).days
    if diff>30:
        member_class.account_credits=0
        return f"You account_credits become {member_class.account_credits}"
    else:
        return f"You account_credits will be eliminated in {30-diff} days. Come to Superman."

def promotion(member_class):#账户充钱
    if member_class.account_credits>100000:
        member_class.deposit=round(member_class.deposit*1.01,1)
        # deposit_account[member_class.id]=member_class.deposit
        return f"Congratulation! You gain {member_class.deposit} in your account"
    elif member_class.account_credits>50000:
        member_class.deposit=round(member_class.deposit*1.008,1)
        # deposit_account[member_class.id]=member_class.deposit
        return f"Congratulation! You gain {member_class.deposit} in your account"
    elif member_class.account_credits>10000:
        member_class.deposit=round(member_class.deposit*1.001,1)
        # deposit_account[member_class.id]=member_class.deposit
        return f"Congratulation! You gain {member_class.deposit} in your account"
    else:
        return "Nothing change about the deposit"


    

def promotion1(cus_list):#分配

    
    gift={}
    items=rollback2(inventory.inventory_informa.store)
    
    probability_1 = 0.5
    probability_2 = 0.3
    probability_3 = 0.2
    
#The first is best,The second is worst, The last is median.   
    for n,i in enumerate(cus_list):
        m=n+1
        random.seed(m*2)
        rand_num = random.random()
    
        # 根据概率分布确定随机数的范围
        if rand_num < probability_1:
           present=items[0]
           gift[i]=present   
        elif rand_num < probability_1 + probability_2:
            present=items[1]
            gift[i]=present   
        else:
           present=items[2]
           gift[i]=present   
           
    return gift




        
    

    