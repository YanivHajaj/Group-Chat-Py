# serverrrr
import socket
import threading

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345  # The port used by the server
#FORMAT = 'utf-8'
#ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT

# A list to store all client sockets. used to send and receive data with the client
clients = []
groups = []
names = []
PasswordForGroups = []

# A list to store all client addresses. variable can be used to identify the client
addresses = []
for i in range(100): #init groups with 100 elemnts (-1)= no group/neme/passw, positive number=group/neme/passw
    groups.append(-1)
    PasswordForGroups.append(-1)
    names.append(-1)
    
# A lock to synchronize access to the lists
lock = threading.Lock()

def accept_client(server_socket):
    #Accept and handle a new client connection
    highestNewGroup=0
    while True:
        # Accept a new client connection
        # client_socket used to send and receive data with the client
        # client_address variable can be used to identify the client
        #the server_socket listen for calls
        client_socket, client_address = server_socket.accept()
        option = client_socket.recv(1024).decode('utf-8')
        
        #################################################11111
        # Join an existing group
        if option == "1": 
            isCorrect=0
            name = client_socket.recv(1024).decode('utf-8') #get the name of client
            GroupID = client_socket.recv(1024).decode('utf-8') #get the GroupID of client
            password = client_socket.recv(1024).decode('utf-8') #get the password of client
            while(isCorrect==0):
                for i in range(100): #init groups with 100 elemnts (-1)= no group, positive number=group
                    if(PasswordForGroups[i]==password) and (groups[i]==GroupID):
                        # Acquire the lock to access the lists
                        lock.acquire()
                        # Add the client socket and address to the lists
                        clients.append(client_socket) #add to client list
                        addresses.append(client_address) #add to address list
                        index = clients.index(client_socket) ##find the index of client_socket
                        groups[index] = GroupID #add to group list
                        PasswordForGroups[index] = password #add to password list
                        names[index] = name #add to name list
                        # Release the lock
                        lock.release()
                        print(f'Accepted connection from thread: {client_address[1]} to server: {client_address[0]} with nickname: ***{name}*** in group number:{GroupID}')
        
                        # Start a new thread to handle the client
                        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
                        client_thread.start()
                        isCorrect=1 #flag for password correction
                        break #stop the loop we found a groep and password
                client_socket.send(str(isCorrect).encode('utf-8'))
                if(isCorrect==0): #if not correct ask for diffrent passw
                    password = client_socket.recv(1024).decode('utf-8')
        #################################################11111

        #################################################22222
        # Create a new group
        elif option == "2":
            highestNewGroup+=1
            name = client_socket.recv(1024).decode('utf-8')
            #NewGroupID = client_socket.recv(1024).decode('utf-8')
            NewGroupID=highestNewGroup #first give new client group number 1 then increase
            #highestNewGroup=highestNewGroup+1 #increase highestNewGroup for new clients
            
            newpassword = client_socket.recv(1024).decode('utf-8')
            # Acquire the lock to access the lists
            lock.acquire()
            # Add the client socket and address to the lists
            clients.append(client_socket)
            addresses.append(client_address)
            index = clients.index(client_socket) ##find the index of client_socket
            groups[index] = str(NewGroupID)
            PasswordForGroups[index] = newpassword
            names[index] = name
            # Release the lock
            lock.release()
            

            client_socket.send(str(NewGroupID).encode('utf-8'))
            # Print a message to the server console
            # client_address[0] = IP address, client_address[1] = port number
           
            print(f'Accepted connection from thread: {client_address[1]} to server: {client_address[0]} with nickname: ***{name}*** in group number:{NewGroupID}')
            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
        #################################################22222


        #################################################33333
        elif option == "3":
            # Disconnect from the server
            client_socket.close()
            #break
        #************************************************
        #################################################33333

        
     
        


def handle_client(client_socket):
    #Receive messages from a client and broadcast them to all clients in the same group
    while True:
        # Receive a message from the client
        message = client_socket.recv(1024).decode('utf-8')
        
        # If the message is empty, the client has closed the connection
        if (message=='exit'):
            break
        
        # Print the message to the server console
        print(f'Received message from {client_socket.getpeername()} with nickname $$${names[clients.index(client_socket)]}$$$: {message}')
        
        # Broadcast the message to all clients
        broadcast(message, client_socket)
        
    # Remove the client socket and address from the lists
    lock.acquire()
    Index = clients.index(client_socket) ##find the index of client_socket
    groups[Index] = -1 #no group in this index
    clients.remove(client_socket)
    addresses.remove(client_socket.getpeername())
 
    lock.release()
    print(f'Closed connection from {client_socket.getpeername()}')
    # Close the client socket
    client_socket.close()
    
    # Print a message to the server console
    

def broadcast(message, sender_socket):
    #Send a message to all clients except the sender
    for client_socket in clients:
        IndexCurrent = clients.index(client_socket) ##find the index of client_socket
        IndexSender = clients.index(sender_socket) ##find the index of sender_socket
        if (client_socket != sender_socket) and (groups[IndexCurrent]==groups[IndexSender]):
            client_socket.send(message.encode('utf-8'))
            client_socket.send(names[clients.index(sender_socket)].encode('utf-8'))

def main():
    
    #  SOCK_STREAM Create a TCP socket AF_INET for IPv4 protocol
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print(f'Closed connection from {client_socket.getpeername()}')

    # Bind the socket to a local address and port
    server_socket.bind((HOST, PORT)) # serversocket.bind((host,port))
    
    # (enable listening) Start listening for incoming connections 
    server_socket.listen()
    
    print('Listening for connections...')
    
    # Start a new thread to accept incoming connections
    accept_thread = threading.Thread(target=accept_client, args=(server_socket,))
    accept_thread.start() #starts a new thread of execution.
    
    # Run the server indefinitely, waits for the thread to complete its execution
    accept_thread.join()


if __name__ == '__main__':
    main()