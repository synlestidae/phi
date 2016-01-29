import sys
import subprocess
import os
import re
from subprocess import check_output
from concurrent import futures

def get_whos_in():
  if sys.platform == "win32" or sys.platform == "cygwin":
    return process_windows(windows_arp_entries())
  elif sys.platform.startswith("linux2"):
    return parse_linux_arp_entries(get_linux_arp_entries())
  raise EnvironmentError
  
def windows_arp_entries():
  #First need to ping eveyrone on the network
  with futures.ThreadPoolExecutor(max_workers=8) as executor:
    for result in executor.map(lambda n : do_win_ping(n), range(1,255)):
      yield result
  

def do_win_ping(n):
  command = ["nmap", "-PR", "-sn", "192.168.1.%d" % n]
  return ("192.168.1.%d" % n, check_output(command))

def ping_closure(call, devnull):
  return lambda command: call(command, stdout=devnull, shell=False)

def get_linux_arp_entries():
  with open(os.devnull, 'w') as FNULL:
  	lines = check_output("./arpscan", stdout=FNULL, stderr=subprocess.STDOUT).split("\r\n")

def process_windows(entries_generator):
  ip = None
  mac = None
  for entry in entries_generator:
    if "Host is up" in entry[1]:
      ip = entry[0]
      for line in entry[1].split("\r\n"):
        if "MAC Address" in line:
          mac = re.split("\\s+", line)[2];
      yield ArpDevice(ip, mac)


def parse_linux_arp_entries(lines):
  for line in lines:
  	if re.match("^\\d+\\.\\d+\\.\\d+\\.\\d+\\s+([A-Ba-b0-9]*)+") is not None:
  		bits = re.split("\\s+", line)
  		yield ArpDevice(bits[0], bits[1])

class ArpDevice:
  def __init__(self, ip_string, mac_string):
    self.ip_string = ip_string
    self.mac_string = mac_string

for w in get_whos_in():
	print w.ip_string, w.mac_string