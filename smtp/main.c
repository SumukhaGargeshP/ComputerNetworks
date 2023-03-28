#include <stdio.h>
#include <string.h>

int connect_smtp(const char* host, int port);
void send_smtp(int sock, const char* msg, char* resp, size_t len);



/*
  Use the provided 'connect_smtp' and 'send_smtp' functions
  to connect to the "lunar.open.sice.indian.edu" smtp relay
  and send the commands to write emails as described in the
  assignment wiki.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <email-to> <email-filepath>", argv[0]);
    return -1;
  }

  char* rcpt = argv[1];
  char* filepath = argv[2];
  FILE *fp;
  char mail[4096];
  fp = fopen(filepath , "r");
  char letter;
  int i = 0;
  for ( ; fscanf(fp, "%c", &letter) != EOF; ) {
    mail[i] = letter;
    i++;
  }
  fclose(fp);
  char response[4096];
  strcat(mail,"\r\n.\r\n");

  char mailfrom[1024] = "MAIL FROM: ";
  strcat(mailfrom,rcpt);
  strcat(mailfrom,"\n");
  char mailto[1024] = "RCPT TO: ";
  strcat(mailto,rcpt);
  strcat(mailto,"\n");

  int socket = connect_smtp("lunar.open.sice.indiana.edu", 25);
  send_smtp(socket, "HELO iu.edu\n", response, 4096);
  printf("%s\n", response);
  send_smtp(socket, mailfrom, response, 4096);
  printf("%s\n", response);
  send_smtp(socket, mailto, response, 4096);
  printf("%s\n", response);
  send_smtp(socket, "DATA\n", response, 4096);
  printf("%s\n", response);
  send_smtp(socket, mail, response, 4096);
  printf("%s\n", response);
  send_smtp(socket, "QUIT\n", response, 4096);
  printf("%s\n", response);
  return 0;
}
