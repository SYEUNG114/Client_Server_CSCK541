"""This programme runs the server code of a Client-Server socket programming task
Some information about a student will be received from Client.
This includes dictionaries serialised using json and pickle.
This programme also receives an encrypted text file and then writes the file content into a file after decrypting them.
The content of the text file is basically a json-string which is the serialised dictionary containing student's information.
"""
import socket
import pickle
import Main_Code as mc
import sys


def receive_from_client():
    HOST = "localhost"
    PORT = 4444

    # Create server as a socket object and raise OSError is the socket cannot be created.
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Server was created successfully ...')  # Receive
    except OSError as msg:
        print('Could not create a server as a socket object ... Terminating the programme ...')
        sys.exit(1)

    # Bind the server to the client and raise OSError if the biding to the client is not successful
    try:
        server.bind((HOST, PORT))
        print(f'Server was successfully associated with the specific network {HOST} and the port number {PORT} ...')
    except OSError as msg:
        print('Could not bind to the client ... Terminating the programme ...')
        sys.exit(1)

    # Call listen method for the server to listen to "one" client
    try:
        server.listen()
        print('Server is listening to the client ...\n\n', end='')  # Receive
    except OSError as msg:
        server.close()
        print('Server could not listen to a client ... Terminating the programme ...')
        sys.exit(1)

    # Server will accept connections on all available IPv4 interfaces.
    client, address = server.accept()

    # Receive json-serialised dictionary from client and send a confirmation message
    try:
        # Receive json-serialised dictionary from client
        json_dict = client.recv(1024).decode()
        print('The json-serialised dictionary received successfully:\n', end='')
        print(json_dict)
        # Send a message to the client confirming receiving the json-serialised dictionary
        client.send('Message from server: The json dictionary was received ...'.encode())
    except:
        print('Failed to receive the json-serialised data or send the confirmation message to the client'
              ' ... Terminating the programme')
        sys.exit(1)

    # Receive pickle-serialised dictionary from client and send a confirmation message
    try:
        # Receive pickle-serialised dictionary from client
        pickled_dict = client.recv(1024)
        print('\nThe pickle-serialised dictionary was received successfully:\n', end='')
        print(pickle.loads(pickled_dict))
        # Send a message to the client confirming receiving the pickle-serialised dictionary
        client.send('Message from server: The pickled dictionary was received ...'.encode())
    except:
        print('Failed to receive the pickle-serialised data or send the confirmation message to the client'
              ' ... Terminating the programme')
        sys.exit(1)

    # Receive the name of the text file from client and send a confirmation message
    try:
        # Receive the name of the text file - This will be used to create the decrypted file
        original_filename = client.recv(1024).decode()
        print(f'\n\nThe name of the encrypted file is received successfully:"{original_filename}".')
        # Update the filename accordingly
        new_filename = original_filename.replace('.txt', '') + '_received' + '.txt'
        # Send a message to the client confirming receiving the filename
        client.send(f'Message from server: Filename was received "{original_filename}" ...'.encode())
    except:
        print('Failed to receive the filename or send the confirmation message to the client'
              ' ... Terminating the programme')
        sys.exit(1)

    # Receive the content of the encrypted textfile and send confirmation message to the client
    try:
        file_data = client.recv(1024).decode()
        print(f'The content of the encrypted text file was received successfully ...')
        # Send a message to the client confirming receiving the filename
        client.send(f'Message from server: The file contents were received ...'.encode())
    except:
        print('Failed to receive the content of the encrypted text file or send the confirmation message to the client'
              ' ... Terminating the programme')
        sys.exit(1)
        # print('This content of the file is:', file_data)

    # Open a text file with the updated filename and write the encrypted data as byte
    try:
        with open(new_filename, 'wb') as file:
            # Write the received encrypted data to the new text file.
            file.write(file_data.encode())
        # Send a message to the client confirming the re-construction of the encrypted file
        client.send(f'Message from server: The encrypted file was re-constructed successfully ...'.encode())
    except:
        print('Failed to re-construct the encrypted text file or send the confirmation mesage to the client'
              ' ... Terminating the programme')
        sys.exit(1)

    # Call "load_key" to read the encryption key and store it in a variable
    encrypted_file_key = mc.load_key()

    # Call "decrypt_text_file" to decrypt the text file and store the decrypted data in a separate file
    decrypted_student_data = mc.decrypt_text_file(new_filename, encrypted_file_key)
    print(f'The file is decrypted and saved as "{decrypted_student_data}". '
          f'The content of the file is printed below:\n\n', end='')

    # Open the decrypted file, and print its content on the screen.
    with open(decrypted_student_data, 'r') as reader:
        for line in reader:
            print(line, end='')
    print('\n')

    # Send a message to the client confirming the file was descrypted successfully
    client.send(f'Message from server: The file was decrypted successfully ...'.encode())  # Send

    # Close the server and the client
    client.close()
    server.close()


def main():
    receive_from_client()


if __name__ == '__main__':
    main()
