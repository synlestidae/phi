import sys
import subprocess
import os
from subprocess import check_output
from concurrent import futures

def get_whos_in():
  if sys.platform == "win32" or sys.platform == "cygwin":
    return parse_windows_arp_result(get_windows_arp_entries())
  elif sys.platform.startswith("linux2"):
    return parse_linux_arp_entries(get_linux_arp_entries())
  raise EnvironmentError
  
def get_windows_arp_entries():
  #First need to ping eveyrone on the network
  with futures.ThreadPoolExecutor(max_workers=16) as executor:
    devnull = open(os.devnull, 'wb')
    for result in executor.map(lambda n : do_win_ping(ping_closure(subprocess.call, devnull), n), range(1,255)):
      print "Exit for %d was %d" % result
  print check_output("arp -a")#.split("\r\n")

def do_win_ping(call, n):
  command = ["ping", "-n", "1", "-w", "50", ("192.168.1.%d" % int(n))]
  return (n, call(command))

def ping_closure(call, devnull):
  return lambda command: call(command, stdout=devnull, shell=False)

def get_linux_arp_entries():
  check_output("arp -a").split("\r\n")

def parse_windows_arp_result(lines):
  pass 
def parse_linux_arp_result(lines):
  pass

get_windows_arp_entries()
