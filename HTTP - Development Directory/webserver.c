#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>

char webpage[] =
"HTTP/1.1 200 OK\r\n"
"Content-Type: text/html; charset=UTF-8\r\n\r\n"
"<!DOCTYPE html>\r\n"
"<html><head><title>Server setup</title>\r\n"
"<style>body {background-color: #FFFFFF}</style></head>\r\n"
"<body><center><h1>Server header</h1></body></html>\r\n";

int main (int argc, char *argv[])
{
	struct sockaddr_in file_descriptor_for_webserver, file_descriptor_for_request;
	socklen_t webserver_block_size = sizeof(struct sockaddr_in);
	socklen_t request_block_size  = sizeof(struct sockaddr_in);
	char connection_buffer[2048];
	int connection_buffer_size = sizeof(connection_buffer) / sizeof(char);
	int on = 1;

	int _socket_frame_ = socket(AF_INET, SOCK_STREAM, 0);
	if (_socket_frame_ < 0)
	{
		perror("socket");
		exit(1);
	}

	setsockopt(_socket_frame_, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(int));

	/* Good inline ASM practice would be to get the address of the struct and XOR it to its block ending */
	for (int i = 0; i < 8; i++)
	{
		file_descriptor_for_webserver.sin_zero[i] = file_descriptor_for_webserver.sin_zero[i] ^ file_descriptor_for_webserver.sin_zero[i];
	}
	file_descriptor_for_webserver.sin_family = AF_INET;
	file_descriptor_for_webserver.sin_addr.s_addr = INADDR_ANY;
	file_descriptor_for_webserver.sin_port = htons(8080);

	int _bind_ = bind(_socket_frame_, (struct sockaddr*) &file_descriptor_for_webserver, webserver_block_size);
	if (_bind_ == -1)
	{
		perror("bind");
		close(_socket_frame_);
		exit(1);
	}

	int _listen_ = listen(_socket_frame_, 10);
	if (_listen_ == -1)
	{
		perror("listen");
		close(_socket_frame_);
		exit(1);
	}
	else
	{
		printf("\n\n---/ Connection details (new/%s, %i): /---\n\n", inet_ntoa(file_descriptor_for_request.sin_addr),
									     ntohs(file_descriptor_for_request.sin_port));
		fflush(stdout);
	}	

	int request_count = 0;

	while(1)
	{
		
		int _file_descriptor_for_longest_in_que_ = accept(_socket_frame_, (struct sockaddr*) &file_descriptor_for_request, &request_block_size);
		if (_file_descriptor_for_longest_in_que_ == -1)
		{
			perror("Connection failed..\n");
			fflush(stdout);
			continue;
		}
		else
		{
			request_count++;
			printf("Someone requested data %i times.\n", request_count);
			fflush(stdout);
		}
		
		if (!fork())
		{
		
			close(_socket_frame_); /* Drop previous process and continue from an "isolated" socket */
			memset(connection_buffer, 0, connection_buffer_size);
			read(_file_descriptor_for_longest_in_que_, connection_buffer, connection_buffer_size - 1);
			printf("%s\n", connection_buffer);

			if (!strncmp(connection_buffer, "GET /favicon.ico", 16))
			{
				// Other code goes here
				write(_file_descriptor_for_longest_in_que_, "Not implemented", sizeof("Not implemented"));
				close(_file_descriptor_for_longest_in_que_);
				printf("Method not implemented.\n");
				printf("\n\n---/ Connection details (%s, %i): /---\n\n", inet_ntoa(file_descriptor_for_request.sin_addr),
											 ntohs(file_descriptor_for_request.sin_port));
				fflush(stdout);
				exit(0);
			}
			else
			{
				write(_file_descriptor_for_longest_in_que_, webpage, sizeof(webpage) - 1);
				close(_file_descriptor_for_longest_in_que_);
				printf("Sent webpage data.\n");
				printf("\n\n---/ Connection details (%s, %i): /---\n\n", inet_ntoa(file_descriptor_for_request.sin_addr),
											 ntohs(file_descriptor_for_request.sin_port));
				fflush(stdout);
				exit(0);
			}
		}

		close(_file_descriptor_for_longest_in_que_);
	}

	return 0;
}
