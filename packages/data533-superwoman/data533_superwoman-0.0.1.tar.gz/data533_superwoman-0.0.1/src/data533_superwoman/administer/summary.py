# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 21:08:10 2023

@author: Administrator
"""


from datetime import datetime as dt
from datetime import timedelta 


import customer.members as members
import customer.transactions as transactions


from administer import inventory
from administer.account import eliminate,promotion, promotion1

q1=members.member(id=1, name="Bob", email="Bob@gmail.com", phone="12345", address="kelowna")
q2=members.member(id=2, name="Nancy", email="Nancy@gmail.com", phone="678910", address="richmond")
q3=members.member(id=3, name="Maria", email="MA@gmail.com", phone="unknown", address="unknown")
q4=members.member(id=4, name="Mike", email="ME@gmail.com", phone="456788", address="Vancouver")
member_list=["q1","q2","q3","q4"]
q1.add_deposit(100000)
q2.add_deposit(50000)
q3.add_deposit(10000)
q4.add_deposit(100)
        
        
q1.add_credits(110000)
q2.add_credits(55000)
q3.add_credits(11000)
q4.add_credits(200)
p1=transactions.transaction(items_name="milk", items_value=3, transaction_time=dt.today()-timedelta(days=3))
p2=transactions.transaction(items_name="flower", items_value=99, transaction_time=dt.today()-timedelta(days=40))
transaction_list=["p1","p2"]



while True:
    judge_ini=int(input("""Which part do you want to refer?
              choose 1: Manage customer account
              choose 2: Go to the inventory
              else: Quit\n"""))
    if judge_ini==1:
        cus_judge=int(input("""What do you want to do?
                  choose 1: Purnishment:changing credits on unactive-customer
                  choose 2: Promotion 1:providing gifts for top 3 active-customer
                  choose 3: Promotion 2: increasing deposit according to credits
                  choose 4: Advertising: Announce close-due day items\n"""))
        if cus_judge==1:
            print("Here are the details for customer state:\n")
            print(eliminate(p2,q2))
            print(eliminate(p1,q1))
        elif cus_judge==2:
            print("Here is distribution of present:\n")
            print(promotion1(member_list[0:3]))
            
        elif cus_judge==3:
            print("Here increasing deposit list is:\n")
            for i in member_list:
                print(promotion(locals()[i]),"\n")
        else:
            print("Here expiry account list is:\n")
            print("In main inventory:",inventory.rollback2(inventory.inventory_informa.store))
            print("In sub inventory:",inventory.rollback2(inventory.extend_informa.Store))

        ifquit=int(input("If you have another operation, press any integer; Exiting interface presses 0.\n"))
        if ifquit==0:
            break
    elif judge_ini==2:
         while True:   
            judge=int(input("""What do you want to do?
                      choose 1: Add new items into main_inventory
                      choose 2: Update main_inventory
                      choose 3: Manage sub_inventory
                      else : Quit
                """))
            if judge==1:

                item=input("Please input your item name(str):")
                quantity=int(input("Please input your quantity(int):"))
                cost=float(input("Please input your cost(float):"))
                price=float(input("Please input your price(float):"))  
                expire=input("Please input your expire(20231123):\n")         
                locals()[item]=inventory.inventory_informa(item, quantity, cost, price, expire)
                print("The total profit of this %s is %f"%(locals()[item].item,locals()[item].profit,"\n"))
                continue
           
            elif judge==2:
                    u=inventory.inventory_informa("test",1000,3,6,"20231204")
                    #input
                    item=input("Please input your item name(str):")
                    quantity=int(input("Please input your quantity(int):"))
                    cost=float(input("Please input your cost(float):\n"))
                    print(u.update(item, quantity,cost))
                    u.delete("test")
                    
                    continue
            elif judge==3:
                while True:
                    invent_judge=int(input("""What do you want to do?
                              choose 1: Add new items
                              choose 2: Update sub_inventory
                              
                              else: Quit
                        """))
                        # choose 3: Combine inventory from main_inventory
                    if invent_judge==1:
                            # judge=1
                            # while judge:
                                item=input("Please input your item name(str):")
                                quantity=int(input("Please input your quantity(int):"))
                                cost=float(input("Please input your cost(float):"))
                                price=float(input("Please input your price(float):"))  
                                expire=input("Please input your expire(20231123):\n")       
                                locals()[item]=inventory.extend_informa(item, quantity, cost, price, expire)
                                print(locals()[item])
                                continue
                    elif invent_judge==2:
                        while True:
                            #initialize
                            u=inventory.extend_informa("test",1000,3,6,"20231204")
                            #input
                            item=input("Please input your item name(str):")
                            quantity=int(input("Please input your quantity(int):"))
                            cost=float(input("Please input your cost(float):\n"))
                            u.update(item, quantity,cost)
                            #delete
                            u.delete("test")
                            ifquit=int(input("If you have another operation, press any button; Exiting interface presses 0"))
                            if ifquit==0:
                                continue
                    else:
                        break
                        
            else:
                break