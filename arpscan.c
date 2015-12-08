#include <stdio.h>
#include <stdlib.h>

int main() {
  setuid(0);
  system("arp-scan --retry 3 --interface wlan0 --localnet");
}
