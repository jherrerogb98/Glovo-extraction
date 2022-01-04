#!/usr/bin/env python
# coding: utf-8

# In[38]:


import pandas as pd
import numpy as np
import re
import sys
from itertools import chain
import copy


# In[39]:


orders=pd.read_csv('glovo 2502.csv',sep=';')


# In[40]:


headers=['FECHA','HORA','LOCAL','CANAL','EMP','BEB','AP','1P','2P','EA10','EA12','EA15','EA20','B6','B12',
         'OT','space1','1-C','2-CP','3-PC','4-AT','5-JQ','6-AR','7-PA','8-PP','9-QC','10-MO','11-CB','12-CA','13-ES','14-CS','15-CH',
         '16-SM','17-AL','18-BT','19-CQ','20-HU','21-CO','22-PT','space2','P1-C','P2-PC','P3-ha','P4-CA','P5-ES','space3 ','AG','AGG','CC',
         'CCL','CCZ','FN','FL','TR','AQ','AQ0','RD','NE','CV','CV0','HE33','QU','AL','1906','V-MC','VB','VT','space4','CH',
         'OL','PI','BBQ','GUA','ENS']

final_orders=pd.DataFrame(columns=headers)
print(final_orders)


# In[41]:


dict_cont={'Empanada criolla original':{
    'count':0, 'name':'1-C'},
    'Empanada criolla picante':{
    'count':0, 'name':'2-CP'},
    'Empanada de pollo al chimichurri con limón':{
    'count':0, 'name':'3-PC'},
    'Empanada con atún':{
    'count':0, 'name':'4-AT'},
    'Empanada con jamón y queso':{
    'count':0, 'name':'5-JQ'},
     'Empanada árabe':{
    'count':0, 'name':'6-AR'},
     'Empanada al pastor':{
    'count':0, 'name':'7-PA',},
     'Pulled pork BBQ':{
    'count':0, 'name':'8-PP'},
     'Empanada con queso de cabra':{
    'count':0, 'name':'9-QC'},
    'Empanada caprese':{
    'count':0, 'name':'12-CA'},
    'Empanada con espinaca':{
    'count':0, 'name':'13-ES'},
    'Empanada original criolla de soja':{
    'count':0, 'name':'14-CS'},
    'Empanada de chocolate':{
    'count':0, 'name':'15-CH'},
    'Empanada strudel de manzana':{
    'count':0, 'name':'16-SM'},
    'Alfajor de maicena con dulce de leche y coco rallado':{
    'count':0, 'name':'17-AL'},
    'Chistorra y queso':{
    'count':0, 'name':'19-CQ'},
     'Empanada humita':{
     'count':0,'name':'20-HU'},
     'Empanada de cochinita pibil':{
    'count':0, 'name':'21-CO'},
    'Empanada pollo thai':{
    'count':0, 'name':'22-PT'},
    'Agua (330 ml.)':{'count':0, 'name':'AG'},
    'gas':{'count':0, 'name':'AGG'},
    'Coca-Cola Sabor Original lata 330ml.':{'count':0, 'name':'CC'},
    'Coca Cola light (330 ml.)':{'count':0, 'name':'CCL'},
    'Coca-Cola Zero Azúcar lata 330ml.':{'count':0, 'name':'CCZ'},
    'Fanta Naranja lata 330ml.':{'count':0, 'name':'FN'},
    'Fanta Limón lata 330ml.':{'count':0, 'name':'FL'},
    'Aquarius':{'count':0, 'name':'AQ'},
    'Aquarius zero':{'count':0, 'name':'AQ0'},    
    'Nestea':{'count':0, 'name':'NE'},
    'Cerveza Mahou   (33 cl.)':{'count':0, 'name':'CV'},
    'Cerveza estrella galicia':{'count':0, 'name':'CV'},   #sin menu  Cerveza Estrella Galicia (330 ml.)
    'Cerveza Mahou sin alcohol (330 ml.)':{'count':0, 'name':'CV0'},
    'Cerveza Quilmes (330 ml.)':{'count':0, 'name':'QU'}}

dict_cont_menu_emp={'Empanada criolla original':{
    'count':0, 'name':'1-C'},
    'Empanada criolla picante':{
    'count':0, 'name':'2-CP'},
    'Empanada de pollo con chimichurri al limón':{
    'count':0, 'name':'3-PC'},
    'Empanada de atún':{
    'count':0, 'name':'4-AT'},
    'Empanada de jamón y queso':{
    'count':0, 'name':'5-JQ'},
     'Empanada árabe':{
    'count':0, 'name':'6-AR'},
     'Empanada pastor':{
    'count':0, 'name':'7-PA',},
     'Empanada de pulled pork':{
    'count':0, 'name':'8-PP'},
     'Empanada con queso de cabra':{
    'count':0, 'name':'9-QC'},
    'Empanada caprese':{
    'count':0, 'name':'12-CA'},
    'Empanada con espinaca':{
    'count':0, 'name':'13-ES'},
    'Empanada original criolla de soja':{
    'count':0, 'name':'14-CS'},
    'Empanada de chocolate':{
    'count':0, 'name':'15-CH'},
    'Empanada de strudel de manzana':{
    'count':0, 'name':'16-SM'},
    'Alfajor de maicena con dulce de leche y coco rallado':{
    'count':0, 'name':'17-AL'},
    'Empanada de chistorra y queso':{
    'count':0, 'name':'19-CQ'},
     'Empanada humita':{
     'count':0,'name':'20-HU'},
     'Empanada de cochinita':{
    'count':0, 'name':'21-O'},
    'Empanada pollo thai':{
    'count':0, 'name':'22-PT'},
    'Agua cabreiroá (50 cl.)':{
    'count':0, 'name':'AG'},
    'Agua cabreiroá con gas (50 cl.)':{
    'count':0, 'name':'AGG'},
    'Agua':{
    'count':0,'name':'AG'},
    'Coca-Cola Sabor Original lata 330ml.':{
    'count':0, 'name':'CC'},
    'Coca Cola light (330 ml.)':{
    'count':0, 'name':'CCL'},
    'Coca-Cola Zero Azúcar lata 330ml.':{
    'count':0, 'name':'CCZ'},
    'Fanta Naranja lata 330ml.':{
    'count':0, 'name':'FN'},
    'Fanta Limón lata 330ml.':{
    'count':0, 'name':'FL'},
    'Aquarius':{'count':0, 'name':'AQ'},
    'Aquarius zero':{'count':0, 'name':'AQ0'},
    'Nestea':{'count':0, 'name':'NE'},
    'Nestea Té Negro Limón lata 330ml.':{'count':0,'name':'NE'},
    'Cerveza Mahou   (33 cl.)':{'count':0, 'name':'CV'},
    'Cerveza estrella galicia':{'count':0, 'name':'CV'},#sin menu  Cerveza Estrella Galicia (330 ml.)
    'Cerveza estrella galicia':{'count':0, 'name':'CVP'},                 
    'Cerveza Mahou sin alcohol (330 ml.)':{'count':0, 'name':'CV0'},
    'Cerveza Quilmes (330 ml.)':{'count':0, 'name':'QU'}}

dict_menu={'Menú aperitivo':{'count':0,'name':"AP"},
    'Menú 1 persona':{'count':0,'name':"1P"},
    'Menú 2 personas':{'count':0,'name':'2P'},
    'Entre amigos 10 empanadas':{'count':0,'name':'EA10'},
    'Entre amigos 15 empanadas':{'count':0,'name':'EA15'},
    'Entre amigos 20 empanadas':{'count':0,'name':'EA20'}}


# In[42]:


no_menu_orders=orders.copy(deep=True)

#no_menu_orders
no_menu_orders=no_menu_orders.astype("str")

#for order in no_menu_orders['DESCRIPTION']:
  
for i in range(len(orders['DESCRIPTION'])):    
    
    if (' - ') in no_menu_orders['DESCRIPTION'][i]:
        no_menu_orders['DESCRIPTION'][i]='0'

menu_orders=orders.copy(deep=True)

for i in range(len(orders['DESCRIPTION'])):    
    search_for=['Menú','Entre amigos','Aperitivo']
    if any(c in menu_orders['DESCRIPTION'][i] for c in search_for):
            menu_orders['DESCRIPTION'][i]=menu_orders['DESCRIPTION'][i]
    else:
            menu_orders['DESCRIPTION'][i]='0'


# In[43]:


#cuenta las empanadas que se venden sueltas

def process_nomenu(line):
    
    dict_copia=copy.deepcopy(dict_cont)
    for product in line:
        
        product=product.split("x")
        if len(product)!=2:
            continue
        product[0]=product[0].strip()
        product[1]=product[1].strip()
        if product[1] in dict_copia:
            
            dict_copia[product[1]]["count"]+=int(product[0])
            
        else:
            print("no aparece")        
    return dict_copia
    
    
    
    
def extract_column_count(line,column_name):
    
    for key in line:
        value=line[key]
        if value["name"]==column_name:
            return int(value['count'])
    return 0

row_num=0

for order in no_menu_orders['DESCRIPTION']:
    splitted=order.split("\n")
    line=process_nomenu(splitted)
    #print(line)
    if line is None:
        continue
    i=0
    lista=[0]*len(final_orders.columns)
    for column in final_orders:
        count=extract_column_count(line,column)    
        lista[i]=count
        i= i+1
    final_orders.loc[row_num]=lista
    row_num+=1
final_orders.iloc[:,17:40]


# In[44]:


#cuenta las empanadas que se venden a la vez que menús en la misma factura

def process_menu(line):
    dict_copia=copy.deepcopy(dict_cont)
    for product in line:
        #print(product)
        product=product.split("x")
        if len(product)!=2:
                continue
        product[0]=product[0].strip()
        product[1]=product[1].strip()
            
        if product[1] in dict_copia:
            
            dict_copia[product[1]]["count"]+=int(product[0])
  
        else:
            print("no aparece")      
    return dict_copia


            
def extract_column_count(line,column_name):
    
    for key in line:
        value=line[key]
        if value["name"]==column_name:
            return int(value['count'])
    return 0

row_num=0

for order in menu_orders['DESCRIPTION']:
    
    splitted=order.split("\n")
    line=process_menu(splitted)
    if line is None:
        continue
    i=0
    lista=[0]*len(final_orders.columns)
    for column in final_orders:
        count=extract_column_count(line,column)    
        lista[i]=count
        i= i+1
    final_orders.loc[row_num]+=lista
    row_num+=1
final_orders.iloc[:,17:40]


# In[45]:


#cuenta los menús vendidos

def process_menu_count(line):
    
    dict_copia=copy.deepcopy(dict_menu)
    for product in line:
        product=product.split(" x ")
        
        list2=product[0]
        if len(product)>1:
            lista=re.split(r'-', product[1])
            #print(lista)
            lista.insert(0,list2)
           
            product=lista
            #print(product)
        if len(product)==1:
                continue
        product[0]=product[0].strip()
        product[1]=product[1].strip()
    
        if product[1] in dict_copia:
            
            dict_copia[product[1]]["count"]+=int(product[0])
  
        else:
            print("no aparece")
        
                    
    return dict_copia


            
def extract_column_count(line,column_name):
    
    for key in line:
        value=line[key]
        if value["name"]==column_name:
            return int(value['count'])
    return 0

row_num=0

for order in menu_orders['DESCRIPTION']:
    
    splitted=order.split("\n")
    line=process_menu_count(splitted)
    if line is None:
        continue
    i=0
    lista=[0]*len(final_orders.columns)
    #final_orders_menu=final_orders_emp.copy(deep=True)   
    for column in final_orders:
        count=extract_column_count(line,column)    
        lista[i]=count
        i= i+1
    final_orders.loc[row_num]+=lista
    row_num+=1
final_orders.iloc[:,0:40]


# In[46]:


#empanadas dentro de los menús
    
def process_menu_count_in_emp(line):
    dict_copia=copy.deepcopy(dict_cont_menu_emp)
    for product in line:
        
        product=product.split("x")
        
        if len(product)!=2:
            product[0]=product[0].strip()
        else:    
            product[0]=product[0].strip()
            product[1]=product[1].strip()
        
        if product[0] in dict_copia:
            
            if len(product)==1:
                dict_copia[product[0]]["count"]+=1
            elif len(product)!=1:
                dict_copia[product[0]]["count"]+=int(product[1]) if product[1].isnumeric()==True else 0
            else:
                print("no aparece")
        
    print(dict_copia)
    return(dict_copia)
        

            
def extract_column_count(line,column_name):
    
    for key in line:
        value=line[key]
        #print(value)
        if value["name"]==column_name:
            return int(value['count'])
    return 0

row_num=0

for order in menu_orders['DESCRIPTION']:

    
    splitted=re.split(r'\n|,| - ',order)
    #print(splitted)
    line=process_menu_count_in_emp(splitted)
    if line is None:
        continue
    i=0
    lista=[0]*len(final_orders.columns)
    for column in final_orders:
        count=extract_column_count(line,column)    
        lista[i]=count
        i= i+1
    #print(lista)
    final_orders.loc[row_num]+=lista
    row_num+=1
final_orders.iloc[:,17:40]


# In[ ]:





# In[47]:


final_orders.iloc[:,17:40]


# In[36]:


final_orders.to_csv(r'final_orders.csv', index = False)


# In[21]:


final_orders.iloc[:,0:30]


# In[860]:


final_orders.iloc[0:20,40:60]


# In[49]:


final_orders.to_csv('editado2502(3).csv')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




