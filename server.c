#include<stdio.h>
#include<string.h>    
#include<stdlib.h>    
#include<sys/socket.h>
#include<arpa/inet.h> 
#include<unistd.h>    
#include<pthread.h> 
struct node
{
	char pos[2048];
	int id;
	struct node *child, *parent;
};
struct node* root;
void *connection_handler(void *);
int main(int argc , char *argv[])
{
    int socket_desc , client_sock , c;
    struct sockaddr_in server , client;
    socket_desc = socket(AF_INET , SOCK_STREAM , 0);
    if (socket_desc == -1)
    {
        printf("Could not create socket");
    }
    puts("Socket created");
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons( 2311 );
    if( bind(socket_desc,(struct sockaddr *)&server , sizeof(server)) < 0)
    {
        perror("bind failed. Error");
        return 1;
    }
    puts("bind done");
    listen(socket_desc , 3);
    puts("Waiting for incoming connections...");
    c = sizeof(struct sockaddr_in);
    puts("Waiting for incoming connections...");
    c = sizeof(struct sockaddr_in);
	pthread_t thread_id;
    while( (client_sock = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c)) )
    {
        puts("Connection accepted");
        if( pthread_create( &thread_id , NULL ,  connection_handler , (void*) &client_sock) < 0)
        {
            perror("could not create thread");
            return 1;
        }
        puts("Handler assigned");
    }
    if (client_sock < 0)
    {
        perror("accept failed");
        return 1;
    } 
    return 0;
}

void *connection_handler(void *socket_desc)
{
	struct node *this;
	if(root == NULL)
		{
			root = malloc(sizeof(struct node));
			this = root;
		}
	else
		{
			struct node *temp =root;
			while(temp->child!= NULL)
				{
					temp = temp->child;
				}
			temp->child = malloc(sizeof(struct node));
			this = temp->child;
			this->parent =temp;
		}
    int sock = *(int*)socket_desc;
    int read_size;
    char *message , client_message[2000];
	struct node *t;
    int i;
    char mes[2048];
    while( (read_size = recv(sock , client_message , 2000 , 0)) > 0 )
    {
	if(client_message[0]=='p')
		{
		strcpy(this->pos, &client_message[1]);
		t=root;
		for(; t==this;i++)
			t=t->child;
		this->id=i;
		client_message[read_size] = '\0';
		strcpy(mes,"p");
		t=this->parent;
		while(t!=NULL){
			if(mes[1]!='\0')		
				strcat(mes, ",");
	        	strcat(mes, t->pos);
			t=t->parent;		
			}
		t=this->child;
		while(t!=NULL){
			if(mes[1]!='\0')
				strcat(mes, ",");
	        	strcat(mes, t->pos);
			t=t->child;		
			}
		write(sock , mes , strlen(mes));
		}
	memset(client_message, 0, 2000);
    }
    if(read_size == 0)
    {
        puts("Client disconnected");
		if(this == root){
			root =this->child;
			if(this->child!=NULL)
				this->child->parent=NULL;
		}		
		else
		{
			this->parent->child =this->child;
			if(this->child!=NULL)
				this->child->parent =this->parent;
		}
	free(this);
        fflush(stdout);
    }
    else if(read_size == -1)
    {
	if(this == root){
			root =this->child;
			if(this->child!=NULL)
				this->child->parent=NULL;
		}		
		else
		{
			this->parent->child =this->child;
			if(this->child!=NULL)
				this->child->parent =this->parent;
		}
	free(this);
        perror("recv failed");
    }    
    return 0;
} 
