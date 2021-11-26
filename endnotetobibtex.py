# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 10:00:04 2021
@author: ml566
"""
#%%Import
import timeit
import re
import glob
from copy import deepcopy
import copy
import os
import sys
import pathlib
from pathlib import Path
#%%
 
fp='Literatur.txt'
save_path=fp.replace('txt','bib')

#%% get Literature

def getTxt(file_path):
    
    with open(file_path, 'r', encoding='utf8') as f:
        content=f.read().split('\n@')

    Lib={}
    for n,v in enumerate(content):  
        if len(v)>5:
            
            el=v.splitlines()
            temp={}

            for i in el:
                if 'type' in i:
                    temp['type']=re.split('{|}', i)[1]
            try:
                    temp['type']
            except:
                    print(v+'\n'+str(n))
                    sys.exit()
          
            if temp['type']=='Journal Article' or temp['type']=='Book':
                for i in el:
                    if 'author' in i:
                        temp['authors']=re.split('{|}', i)[1].split(' and ')
                        temp['authors']=[re.split(', ',j) for j in temp['authors']]
                    elif 'year' in i:
                        temp['year']=re.split('{|}', i)[1]
                        
            else:
                print('Error: Literaturetype not known.')
                sys.exit()
            
            # create Bibkey for .bib and check if same name exists already    
            
            bibkey=temp['authors'][0][0]+temp['year']
             #replace special characters
            bibkey=re.sub('-','',bibkey)
            bibkey=re.sub('é','e',bibkey)
            bibkey=re.sub('ä','a',bibkey)
            bibkey=re.sub('ö','o',bibkey)
            bibkey=re.sub('ü','u',bibkey)
            
            n=1
            while True:
                if bibkey in Lib.keys():
                    
                    try:                           
                        bibkey=bibkey.replace(temp['year'],'')
                        bibkey=bibkey+temp['authors'][n][0]+temp['year']
                        n=n+1
                    except:
                        print(bibkey)
                        sys.exit()
                else:
                    break
            
            print(bibkey)
            h=el[0].split('{')
            h[1]=re.sub(',| ','',h[1])
            el[0]='@'+h[0]+'{'+bibkey+','
            if 'ReferenceNumber' in el[1]:
                el[1]='   '+'ReferenceNumber = ' + '{' + h[1] + '}' + ','
            else:
                el.insert(1,'   '+'ReferenceNumber = ' + '{' + h[1] + '}' + ',')
            
            contTemp=''.join(el) 
            if '@@' in contTemp:
                contTemp.replace('@@','@')
            Lib[bibkey]=contTemp

    return Lib
      
def writeBib(save_path,Lib):
    with open('Literatur.bib','w', encoding='utf8') as of:
        of.write('\n'.join(Lib.values()))

#%%Excecute


Lib=getTxt(fp)
writeBib(save_path,Lib)
