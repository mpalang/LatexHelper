# -*- coding: utf-8 -*-

import re
 
file='//tsclient/I/Literatur/Literatur.txt'

f=open(file,'r')

txtfile=f.read()

content=txtfile.split('@')

list=[]

for c in content:
    if len(c)>5:
        lines=c.splitlines()
        for line in lines:
            if 'author' in line:
                a=re.split('{|}', line)[1]
                a=a.split(',')[0]
            if 'year' in line:
                y=re.split('{|}',line)[1]
        list.append(a+y)
        #list.sort()


        

        
               

        # with open('//tsclient/I/Literatur/Literatur.bib','a') as of:
        #     of.write('\n'.join(el))
        
    
f.close()

