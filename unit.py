from threading import Thread
from requests import get
import re, uuid
import time
import sys
import os
import signal

import socket, pickle
import subprocess

from cassandra.cluster import Cluster

class ExitCommand(Exception): pass

def signal_handler(signal, frame):
    raise ExitCommand()

class CassandraDB:

    def __init__(self, server_config=[]):
        self.connection()

    def connection(self):
        while True:
            try:
                cluster = Cluster(contact_points=["127.0.0.1"], port=9042)
                session = cluster.connect()
                self.cluster = cluster
                self.session = session
                break
            except: print('WAITING FOR UNITS NETWORK')
            time.sleep(1)
    
    def new_instance(self):
        self.session.execute("""CREATE KEYSPACE IF NOT EXISTS units WITH replication = {'class' : 'SimpleStrategy', 'replication_factor':1};""")
        self.session.execute("""CREATE TABLE IF NOT EXISTS units.unit(
            ip varchar,
            macc varchar,
            state varchar,
            info list<int>,
            PRIMARY KEY (ip, macc)
        )""")
        
        self.session.execute("""CREATE TABLE IF NOT EXISTS units.datagroup(
            source varchar, 
            state varchar,
            manager varchar,
            PRIMARY KEY ((manager, state), source)
        )""")
        
    def get_unit(self, ip, macc):
        result = self.session.execute(f"""SELECT * FROM units.unit WHERE ip='{ip}' and macc='{macc}' ALLOW FILTERING;""")
        return result.current_rows
    
    def push_unit(self, ip, macc):
        self.session.execute(
            f"""INSERT INTO units.unit (ip,macc,state,info) VALUES(
                '{ip}', '{macc}', 'WATING',[] )""")
        
class Unit:
    
    def __init__(self, register=False):
        
        self.HOST = '127.0.0.1'
        self.PORT = 1234
        
        self.ip = self.get_ip()
        self.macc = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        
        self.database = CassandraDB()
        self.register = register
        
        self.client = None
        
        self.validate()
        
        sys.stdout.write('\x1b]2;{sys.argv[1]]}\x07')
    
    def __del__(self):
        self.remove_register()
    
    @staticmethod
    def get_ip(): return get('https://api.ipify.org').content.decode('utf8')
    
    def get_unit_info(self): return self.database.get_unit(self.ip, self.macc)
    
    def validate(self):
        if len(self.get_unit_info())<1:
            self.database.push_unit(self.ip, self.macc)
    
    def register_init(self):
        subprocess.Popen([f"gnome-terminal -- python3 register.py {self.PORT}"], shell=True)
        
        self.client = socket.socket()
        
        while True:
            try: 
                self.client.connect((self.HOST, self.PORT))
                break
            except socket.error: pass
        
    def remove_register(self):
        if self.register: 
            self.register_handler({'state': 'OFF'})
            self.client.close()

    def register_handler(self, msg):
        
        if self.client:
            self.client.send(pickle.dumps(msg))
            self.client.recv(2048)
        
    def listening(self):
        
        while True:
            state = self.get_unit_info()[0].state

            if state == 'OFF':
                os.kill(os.getpid(), signal.SIGUSR1)
                
            time.sleep(1)
                
    def working(self, work, args): work(*args)
    
    def start(self, target, args=()):
        
        if self.get_unit_info()[0].state == 'ON':
            
            if self.register:
                self.register_init()
            
            signal.signal(signal.SIGUSR1, signal_handler)
            Thread(target=self.listening, name='state', daemon=True).start()
            
            try: self.working(target, args)
            except ExitCommand: pass
            finally: self.__del__()
        
        else: print('UNIT STATE IS NOT [ON]')