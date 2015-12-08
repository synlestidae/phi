import sys
from subprocess import check_output
def get_whos_in():
    if sys.platform == "win32" or sys.platform == "cygwin":
        return parse_windows_arp_result(get_windows_arp_entries())
    elif sys.platform.startswith("linux2"):
        return parse_linux_arp_entries(get_linux_arp_entries())
    raise EnvironmentError
        
def get_windows_arp_entries():
    check_output("arp -a").split("\r\n")
def get_linux_arp_entries():

def parse_windows_arp_result(lines):
   pass 
def parse_linux_arp_result(lines):
    pass
