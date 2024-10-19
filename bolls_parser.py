import requests
import re
from bs4 import BeautifulSoup
from itertools import zip_longest
from tkinter import *
from threading import Thread
from tkinter.ttk import Progressbar
import time

def get_adv():

    all_adv=[]

    k=1

    url=[
        f"https://www.olx.ua/uk/hobbi-otdyh-i-sport/sport-otdyh/futbol/q-%D0%BC'%D1%8F%D1%87/?page={k}",
        f"https://rozetka.com.ua/ua/balls/c82790/page={k};22004=7373/",
        f"https://prom.ua/ua/Futbolnye-myachi;{k}.html"
    ]

    for count in range(len(url)):

        data=[]

        r=requests.get(url[count])
        soup = BeautifulSoup(r.text, 'lxml')
        total=[soup.findAll('a',class_='css-1mi714g'),soup.findAll('a',class_='pagination__link ng-star-inserted'),[250]]

        tegs=['div','li','div']
        classes=['css-1sw7q4x','catalog-grid__cell catalog-grid__cell_type_slim ng-star-inserted','l-GwW js-productad']
        sites=['-'*30+'OLX'+'-'*30+'\n','-'*30+'ROZETKA'+'-'*30+'\n','-'*30+'PROM'+'-'*30+'\n']

        name=[['h6', "css-16v5mdi er34gjf0"],['a',"goods-tile__heading ng-star-inserted"],['span','_3Trjq htldP _7NHpZ h97_n']]
        cost=[['p', "css-10b0gli er34gjf0"],['span','goods-tile__price-value'],['span','yzKb6']]
        #loc_date=[['p', "css-veheph er34gjf0"],['-','-'],['-','-']]
        stan=[['span', "css-3lkihg"],['div','goods-tile__availability goods-tile__availability--available ng-star-inserted'],['span',"_3Trjq aXB7S NSmdF"]]

        n=1

        if count==2:
            total=1
        else:
            total=1#total[count][-1].text

        data.append(sites[count])

        for i in range(int(total)):  

            url=[
            f"https://www.olx.ua/uk/hobbi-otdyh-i-sport/sport-otdyh/futbol/q-%D0%BC'%D1%8F%D1%87/?page={k}",
            f"https://rozetka.com.ua/ua/balls/c82790/page={k};22004=7373/",
            f"https://prom.ua/ua/Futbolnye-myachi;{k}.html"
            ]
            
            r=requests.get(url[count])
            soup = BeautifulSoup(r.text, 'lxml')
        
            names=soup.findAll(name[count][0],class_=name[count][1])
            costs=soup.findAll(cost[count][0],class_=cost[count][1])
            stans=soup.findAll(stan[count][0],class_=stan[count][1])

            for i,j,u in zip_longest(names,costs,stans):
                if i:i=i.text
                if j:
                    if count==1:
                        j=re.sub('\xa0',' ',j.text)
                    else:
                        j=j.text
                if u:u=u.text
                
                if i and j:
                    data.append(f'{n}) {i,j,u}\n')
                
                n+=1
            k+=1
        
        all_adv.append(data)
    return all_adv

total=70

def loading_data():

    global load_text,finish_text,progressbar,root,total
    root=Tk()
    root.title('Loading...')
    root.geometry('400x400+400+100')

    load_text=Label(text='Wait, the data is loadings...')
    finish_text=Label(text='The loading has been finished.Click to the botton to continue.')
    
    load_text.place(x=100,y=100)
    
    mainloop()

def progress():
    global progressbar
    progressbar=Progressbar(orient='horizontal',mode='determinate')
    progressbar.configure(maximum=total)
    progressbar.place(x=100,y=150,width=200,height=30)
    for i in range(total):
        progressbar.configure(value=i)
        root.update_idletasks()
        time.sleep(0.5)

def adv1():
    global adv
    adv=get_adv()
    print('COMPLITED')
    load_text.config(text='')
    finish_text.place(x=40,y=100)
    progressbar.destroy()

th1=Thread(target=loading_data,daemon=True)
th2=Thread(target=adv1,daemon=True)
th3=Thread(target=progress,daemon=True)

th1.start();th2.start();th3.start()
th1.join();th2.join();th3.join()

def open_window():

    roof=Tk()
    roof.geometry('754x473+400+100')
    roof.resizable(width=False,height=False)
    roof.title('Advenced Bools Parser')

    roof.image=PhotoImage(file='Adveced_Bolls_Parser\images\logo.png')
    roof.iconphoto(False,PhotoImage(file='Adveced_Bolls_Parser\images\ico.png'))

    bg_logo=Label(roof,image=roof.image)
    bg_logo.grid(row=0,column=0)

    my_text='Welcome to my program!The goal is parsing of sites OLX,Prom and Rozetka. If you will see some advertisements \nmy mission have been complited sucsessfully:)'

    greeting=Label(text=my_text)

    adverts_var = StringVar(value=adv[0])
    adverts_var1 = StringVar(value=adv[1])
    adverts_var2 = StringVar(value=adv[2])

    listbox = Listbox(listvariable=adverts_var)

    scroll=Scrollbar(command=listbox.yview)

    olx_butt=Button(text='OLX',command=lambda: listbox.config(listvariable=adverts_var))
    prom_butt=Button(text='PROM',command=lambda: listbox.config(listvariable=adverts_var2))
    rozetka_butt=Button(text='ROZETKA',command=lambda: listbox.config(listvariable=adverts_var1))

    listbox["yscrollcommand"]=scroll.set

    greeting.place(x=100,y=20,width=604)
    listbox.place(x=100,y=95,width=604,height=350)

    olx_butt.place(x=100,y=65,width=80,height=25)
    prom_butt.place(x=195,y=65,width=80,height=25)
    rozetka_butt.place(x=290,y=65,width=80,height=25)

    scroll.place(x=700,y=95,height=350)

    mainloop()

open_window()