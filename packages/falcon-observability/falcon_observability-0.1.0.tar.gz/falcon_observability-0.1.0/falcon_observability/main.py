import datetime
import os
import sys
import threading

import requests
import streamlit as st

import time
import numpy as np
from streamlit_extras.mandatory_date_range import date_range_picker
import streamlit as st
from streamlit_monaco import st_monaco
import subprocess
import threading
import subprocess

class FalconObservability:
    def __init__(self,port):
        self.process = None
        self.port=port
        self.module_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this module
        self.status_code=False
        print('Setup Success')
    def status(self):
        return f'The service is currently {"On" if self.status_code else "Off"}'


    def __start__(self):
        command = f"streamlit run Home.py --server.port {self.port}"
        os.chdir(self.module_dir)

        # Start the subprocess with continuous output capture
        self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Continuously read and print output
        for line in iter(self.process.stdout.readline, ''):
            print(line, end='')

    def start(self):
        if not self.process or self.process.poll() is not None:
            thread = threading.Thread(target=self.__start__)
            thread.start()
            self.status_code = True

        else:
            print("Streamlit server is already running.")

    def kill_process_on_port(self,port):
        try:
            # For Unix-like systems
            if sys.platform != 'win32':
                command = f"lsof -t -i:{port}"
                pid = subprocess.check_output(command, shell=True).decode().strip()
                if pid:
                    print(f"Killing process on port {port} with PID: {pid}")
                    os.kill(int(pid), 9)
                else:
                    print(f"No process found running on port {port}.")
            # For Windows
            else:
                command = f"netstat -ano | findstr :{port}"
                lines = subprocess.check_output(command, shell=True).decode().split('\n')
                for line in lines:
                    if f":{port}" in line:
                        pid = line.strip().split()[-1]
                        print(f"Killing process on port {port} with PID: {pid}")
                        subprocess.check_output(f"taskkill /F /PID {pid}", shell=True)
                        break
                else:
                    print(f"No process found running on port {port}.")
        except Exception as e:
            print(f"Error: {e}")
    def stop(self):
        if self.process:
            # Attempt to terminate the process
            self.process.terminate()
            self.process.kill()
            self.kill_process_on_port(self.port)
            print("Server stopped.")
            self.status_code = False
            self.process = None
        else:
            print("No Streamlit server is running.")
    def check_port(self):
        return self.port

