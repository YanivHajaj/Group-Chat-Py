# client
import socket
import threading

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345  # The port used by the server
#FORMAT = 'utf-8'
#ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT


def receive_messages(client_socket):
    #Receive messages from the server and print them to the console
    while True:
        # Receive a message from the server
        message = client_socket.recv(1024).decode('utf-8')
        name = client_socket.recv(1024).decode('utf-8')
        # If the message is empty, the server has closed the connection
        if not message:
            break
        
        # Print the message to the console
        print(f'message from $$${name}$$$: {message}')

def send_messages(client_socket):
    #Read messages from the console and send them to the server#
    while True:
        # Read a message from the console
        message = input()
        
        # Send the message to the server
        client_socket.send(message.encode('utf-8'))
        
        # If the message is "exit", close the connection
        if message == 'exit':
            print('goodBye :)')   
            exit(0)

def main():
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((HOST, PORT))
    
    print('connecting to the server')

    #************************************************
    print("Choose an option:")
    print("1. Join an existing group")
    print("2. Create a new group")
    print("3. Disconnect from the server")
    option = input()
    client_socket.send(option.encode('utf-8'))
    
    if option == "1": 
        # Join an existing group
        #################################################
        isCorrect=0
        print("please enter your name")
        name = input()
        client_socket.send(name.encode('utf-8'))
        while(1):
            print('enter desired group (positive number)')
            groupID = input()
            if(int(groupID)>0):
                break
        client_socket.send(groupID.encode('utf-8'))
        while(1):
            print('enter password (positive number)')
            password = input()
            client_socket.send(password.encode('utf-8'))
            isCorrect = int(client_socket.recv(1024).decode('utf-8'))
            if((int(password)>0) and (isCorrect==1) ):
                    break
            print('the password incorrect (or not a positive number)')
        #client_socket.send(password.encode('utf-8'))
        print(f'you acepted by the server with the nickname: ***{name}***')
        print(f'your group number:{groupID}')
        print('~~ start send massages to your group mates :) ~~')
        #################################################
    
    elif option == "2":
        # create new group
        #################################################
        print("please enter your name")
        name = input()
        client_socket.send(name.encode('utf-8'))
        #while(1):
        #    print('enter new group ID (positive number)')
        #    groupID = input()
        #    if(int(groupID)>0):
        #            break
        #client_socket.send(groupID.encode('utf-8'))
        while(1):
            print('enter password for new group (positive number)')
            password = input()
            if(int(password)>0):
                    break
        client_socket.send(password.encode('utf-8'))
        
        gruopAssigned = client_socket.recv(1024).decode('utf-8')
        print(f'you acepted by the server with the nickname: ***{name}***')
        
        print(f'your group number assigned by server :{gruopAssigned}')
        print('~~ start send massages to your group mates :) ~~')
        #################################################
    
    elif option == "3":
        # Disconnect from the server
        client_socket.close()
        print('goodBye :)')
        exit(0)
    #************************************************


    


    # Start a new thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    
    # Start a new thread to send messages
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()
    
    # Wait for the threads to finish
    receive_thread.join()
    send_thread.join()
    
    # Close the client socket
    client_socket.close()

if __name__ == '__main__':
    main()