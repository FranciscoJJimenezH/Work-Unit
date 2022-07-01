#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from termcolor import colored, cprint
from tabulate import tabulate
import datetime

class UX:
    @classmethod
    def title(cls,txt):
        print()
        a1, a2 = '-', f'||||| {colored(txt, "magenta")} |||||'
        for ax in range(0,len(a2)-10):
            a1+='-'
        print(a1), print(a2), print(a1)
    
    @classmethod
    def subtitle(cls, txt):
        print(f'{colored(f"---> {txt} <---","green", attrs=["bold"])}')
        
    @classmethod
    def description(cls,ticket, tt, duration, msg=None, e = []):
        print(f'--- {colored(ticket, "magenta")}/{colored(tt, "magenta")} ||| {colored(duration, "cyan")}', end=' ')
        
        if msg:
            print(colored(f'--> {msg}', "green", attrs=["bold"]))
        
        if e:
            print(f'{colored("ERRORS", "red")}')
            for ex in e:
                print(colored(f'\t{ex}', "red"))
        print()
     
    @classmethod
    def indexs(cls, indx, i1, sub_indx, i2, space=0):
        print()
        print() if space >=1 else None
        print(f'    + {indx}: {i1} {colored(sub_indx, "magenta")} {colored(i2, "cyan")}')
        print() if space ==2 else None
    
    @classmethod
    def done_msg(cls, D1, D2, info):
        _d1 = ''
        _d2 = ''
        for d1 in D1:
            _d1+=f'|{d1}|'
            
        for d2 in D2:
            _d2+=f'<{d2}>'
        cprint(f'-> {datetime.datetime.now()} {_d1} {_d2} {info}', "green", attrs=["bold"])
        
    @classmethod
    def error_msg(cls, d1, d2, e, info):
        # datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
        print()
        cprint(f'-> {datetime.datetime.now()}  |{d1}|  <<{d2}>>  {info}',"red")
        cprint(f'\t + Error: {e}',"red")
        print()
        
    @classmethod
    def finish_msg(cls, d1, d2):
        print()
        cprint(f'-> {datetime.datetime.now()}  |{d1}|  <<{d2}>>  PROCCESS FINISHED',"cyan")
        print()
      
    @classmethod
    def pttrn_vizualizer(cls,ly, main_data, sets):

        aaa = [[
            f'{colored("IDENTIFICADOR", "magenta")}',
            f'{colored("PATRON", "magenta")}',
            f'{colored("NUMERO DE PATRONES", "magenta")}'
            ]]
        print(tabulate(aaa,tablefmt='psql', numalign='center', headers='firstrow'))
        print()
        