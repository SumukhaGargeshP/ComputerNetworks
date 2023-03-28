#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netdb.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>

/*
  Use the `getaddrinfo` and `inet_ntop` functions to convert a string host and
  integer port into a string dotted ip address and port.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <host> <port>", argv[0]);
    return -1;
  }
  char* host = argv[1];
  long port = atoi(argv[2]);
  char p[20];
  int s;
  struct addrinfo hints,*result,*addr;
  sprintf(p,"%ld",port);

  memset(&hints, 0, sizeof(hints));
  hints.ai_family = PF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_flags = AI_PASSIVE;
  hints.ai_protocol = IPPROTO_TCP;

  s = getaddrinfo(host,p,&hints,&result);
  if (s != 0) {
    fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(s));
    exit(EXIT_FAILURE);
  }

  addr = result;
  void* raw_addr;
  char buff[254];
  for(;addr!=NULL;){
    if (addr->ai_family == AF_INET) { // Address is IPv4
    struct sockaddr_in* tmp = (struct sockaddr_in*)addr->ai_addr; // Cast addr into AF_INET container
    raw_addr = &(tmp->sin_addr); // Extract the address from the container
    printf("IPv4 %s\n",inet_ntop(AF_INET,raw_addr,buff,500));
    }
    else { // Address is IPv6
    struct sockaddr_in6* tmp = (struct sockaddr_in6*)addr->ai_addr; // Cast addr into AF_INET6 container
    raw_addr = &(tmp->sin6_addr); // Extract the address from the container
    printf("IPv6 %s\n",inet_ntop(AF_INET6,raw_addr,buff,500));
    }
    addr = addr->ai_next;
  }

  return 0;
}
