import time
import psutil
import configparser
import os
import csv
import datetime

command = 'cls'
os.system(command)
config = configparser.ConfigParser()
config.read('config.ini')
PROCESS = config['TASK']['process']
POLLING_TIME = config['TASK']['polling_time']

filename = "logs.csv"
process = psutil.Process(int(PROCESS))
process_name = psutil.Process(int(PROCESS)).name
def display_usage(cpu_usage, mem_usage, syscpu_usage, sysmem_usage, bars=50):

	cpu_percent = (cpu_usage/100.0)
	cpu_bar = '█' * int(cpu_percent * bars) + '-' * (bars - int(cpu_percent * bars))
	mem_percent = (mem_usage / 100.0)
	mem_bar = '█' * int(mem_percent * bars) + '-' * (bars - int(mem_percent * bars))
	syscpu_percent = (syscpu_usage / 100.0)
	syscpu_bar = '█' * int(syscpu_percent * bars) + '-' * (bars - int(syscpu_percent * bars))
	sysmem_percent = (sysmem_usage / 100.0)
	sysmem_bar = '█' * int(sysmem_percent * bars) + '-' * (bars - int(sysmem_percent * bars))

	print(f"Process name:"+ str(process_name),end="\n")
	print(f"Process Power Usage:    |{cpu_bar}| {cpu_usage:.2f}%   ", end="\n")
	print(f"Process Memory Usage: |{mem_bar}| {mem_usage:.2f}%   ", end="\n")
	print(f"System CPU Usage:  |{syscpu_bar}| {syscpu_usage:.2f}%   ", end="\n")
	print(f"System Memory Usage:  |{sysmem_bar}| {sysmem_usage:.2f}%   ", end="\n")


while True:
	display_usage(process.cpu_percent(), process.memory_percent(), psutil.cpu_percent(), psutil.virtual_memory().percent, 30)
	time.sleep(int(POLLING_TIME))

	with open(filename, "a") as csvfile:
		date_now = datetime.datetime.now()
		fieldname = ['Date','Process Power', 'Process memory', 'System CPU', 'System memory']
		writer = csv.DictWriter(csvfile, fieldnames=fieldname)
		writer.writerow({"Date":str(date_now),
						 "Process Power":str(process.cpu_percent()),
						 "Process memory":str(process.memory_percent()), 
						 "System CPU":str(psutil.cpu_percent()), 
						 "System memory": str(psutil.virtual_memory().percent)})
	os.system(command)
