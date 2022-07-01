#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import socket
import time
import os
import signal

import threading
import pickle

from UX import UX

class Register:
    
    def __init__(self):
        
        self.HOST = '127.0.0.1'
        self.PORT = int(sys.argv[1])
        
        sys.stdout.write('\x1b]2;DATABASE REGISTER UNIT\x07')
    
    def on_new_client(self, conn,addr):
        while True:
            data = conn.recv(2048)
            res = pickle.loads(data)
            
            if not data: break
            else:
                if 'state' in res:  os.kill(os.getppid(), signal.SIGHUP)
                else:  UX.done_msg(*res)
        
            conn.sendall(data)
        conn.close()
    
    def main(self):
        ServerSocket = socket.socket()
        
        while True:
            try:
                ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                ServerSocket.bind((self.HOST, self.PORT))
                break
            except socket.error:pass
            time.sleep(1)
        
        ServerSocket.listen(5)
        
        while True:
            Client, address = ServerSocket.accept()      
            threading.Thread(target=self.on_new_client, args=(Client, address)).start()
            
        ServerSocket.close()


if __name__ == '__main__':
    rg = Register()
    rg.main()