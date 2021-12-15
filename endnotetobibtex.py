# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 10:00:04 2021
@author: ml566
"""
#%%Import
import timeit
import re
import glob
import os
import sys
import pathlib
from pathlib import Path
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        #logging.FileHandler("Logging.log"),
        logging.StreamHandler(sys.stdout)
    ])

#%%
fp='Literatur.txt'
save_path=fp.replace('txt','bib')

#%% get Literature
def makeLib(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        content=f.read()
        
    #Sonderzeichen bearbeiten:
    content=content.replace(' & ', ' \& ')
    content=content.replace('\u2009','\u0020')
    #Split content in individual entries:
    content=content.split('\n@')
    Lib={}
    for n,v in enumerate(content):  
        if len(v)>5:
            v=v.lstrip('@')
            lines=v.splitlines()
            temp={}
            lines=[i for i in lines if not 'abstract =' in i]
            for i in lines:
                if 'type' in i:
                    temp['type']=re.split('{|}', i)[1]
            try:
                temp['type']
            except:
                logging.critical(f'{n}th element has no type:\n {v}')
                sys.exit()
            
            #Create Bibkey for different Types:
            DefaultTypes=['Journal Article','Book','Book Section']
            
            if temp['type'] in DefaultTypes:
                for i in lines:
                    if 'author' in i:
                        temp['authors']=re.split('{|}', i)[1].split(' and ')
                        temp['authors']=[re.split(', ',j) for j in temp['authors']]
                    elif 'year' in i:
                        temp['year']=re.split('{|}', i)[1]
                bibkey=temp['authors'][0][0]+temp['year']
                
            elif temp['type'] == 'Web Page':
                for i in lines:
                    if 'description' in i:
                        bibkey='Web_'+re.split('{|}', i)[1]
                    if 'title' in i:
                        i.replace('title','howpublished')
            else:
                logging.critical(f"Literaturetype {temp['type']} of {n}th element not known: \n {v}")
                sys.exit()
                        
            #replace special characters in Bibkey and check if already exists. If yes add second author to Bibkey and so on...
            bibkey=re.sub('é','e',bibkey)
            bibkey=re.sub('á','a',bibkey)
            bibkey=re.sub('ä','a',bibkey)
            bibkey=re.sub('ö','o',bibkey)
            bibkey=re.sub('ü','u',bibkey)
            bibkey=re.sub('-','',bibkey) 
            bibkey=re.sub(' ','',bibkey)
            logging.debug(bibkey)
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
            
            #And put everything back together. Add new field "ReferenceNumber" with Endnote RN:
            h=lines[0].split('{')
            h[1]=re.sub(',| ','',h[1])
            lines[0]='@'+h[0]+'{'+bibkey+','
            
            if 'ReferenceNumber' in lines[1]:
                lines[1]='   '+'ReferenceNumber = ' + '{' + h[1] + '}' + ','
            else:
                lines.insert(1,'   '+'ReferenceNumber = ' + '{' + h[1] + '}' + ',')
            
            contTemp='\n'.join(lines) 
            if '@@' in contTemp:
                contTemp.replace('@@','@')
            #contTemp.replace('inbook','incollection')   
            
            Lib[bibkey]=contTemp

    return Lib
    
def writeBib(save_path,Lib):
    with open('Literatur.bib','w', encoding='utf8') as of:
        of.write('\n'.join(Lib.values()))

#Excecute

 
Lib=makeLib(fp)

logging.info(f'{len(Lib)} References converted')
writeBib(save_path,Lib)
logging.info('Library saved to {}.'.format(Path(os.getcwd(),save_path)))
