"""This programme runs the Client code of a Client-Server socket programming task.
The data are created and prepared using the functions available in "Main_Code.py" module.
In particular, this programme generates a dictionary where some data of a student is stored.
The dictionary is later serialised using pickle and json.
The pickled serialised dictionary is then sent to the server.
The json serialised dictionary is used to generate a text file.
The content of the text file is basically the json serialised dictionary.
The file is encrypted before sending it to the server. The server later decrypt the file and store the content.
"""
import socket
import Main_Code as mc
import os
import sys


def send_to_server(my_text_file, json_data, pickle_data):
    """This function, sends the passed parameters to the server. While pickled data is sent to the server as a variable,
    json_data are stored in a text file. The file is encrypted and then sent to the server.
    After each set of data is sent to the server, the client receives a confirmation from the server.
    The confirmation messages are displayed on the screen.
    :param my_text_file:
    :param json_data: A dictionary that is serialised using json, Type: str
    :param pickle_data: A dictionary serialised using pickle, Type: byte
    :return: None
    """
    HOST = "localhost"
    PORT = 4444
    print('\n',end='')

    # Create server as a socket object and raise OSError is the socket cannot be created.
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('The Client was created successfully ...')  # Receive
    except OSError as msg:
        print('Could not create a client as a socket object ... Terminating the programme ...')
        sys.exit(1)

    # Create a connection to the server, raise OSError if the connection is failed
    try:
        client.connect((HOST, PORT))
        print(f'Connection to the network "{HOST}" via the port number {PORT} was made successfully ...\n\n', end='')
    except OSError as msg:
        print('Could not connect to the server ... Terminating the programme ...')
        sys.exit(1)

    # Send the json-serialised data to the server
    try:
        client.send(json_data.encode())
        print('Json dictionary was sent to the server successfully ...')
    except:
        print('Failed to send the json-serialised data ... Terminating the programme')
        sys.exit(1)
    # Receive confirmation message from the server whether the data has been received
    print(client.recv(1024).decode())

    # Send the pickle-serialised data to the server
    try:
        client.send(pickle_data)
        print('\nPickled dictionary was sent successfully ...')
    except:
        print('Failed to send the pickle-serialised data ... Terminating the programme')
        sys.exit(1)
    # Receive confirmation message from the server whether the data has been received
    print(client.recv(1024).decode())

    # Send the name of the text file to the server
    try:
        client.send(my_text_file.encode())
        print('\nThe filename was sent successfully ...')
    except:
        print('Failed to send the name of the text file ... Terminating the programme')
        sys.exit(1)
    # Receive confirmation message from the server whether the filename has been received
    print(client.recv(1024).decode())

    # Find the file size
    size = os.path.getsize(my_text_file)

    # Open the text file and read it as byte
    try:
        with open(my_text_file, 'rb') as file:
            # Send the content of the file to the server
            client.sendfile(file, offset=0, count=int(size))
            print(f'\nThe file "{my_text_file}" was sent successfully ...')
    except:
        print(f'Failed to open/send "{my_text_file}" data ... Terminating the programme')

    # Receive confirmation from the server whether the file content was received successfully
    print(client.recv(1024).decode())
    # Receive confirmation from the server whether the encrypted text file was re-constructed successfully
    print(client.recv(1024).decode())
    # Receive confirmation from the server whether the text file was decrypted successfully
    print(client.recv(1024).decode())

    # Close the client
    client.close()


def main():
    # Call "Receive_data" to receive the student's information from the user
    fullname, course_name, grade_module_A, grade_module_B, grade_module_C = mc.receive_data()
    # Call "create_dict" to Create a dictionary using received inputs
    module_dictionary = mc.create_dict(fullname, course_name, grade_module_A, grade_module_B, grade_module_C)
    # Call "pickle_dict" to serialise the dictionary using pickle
    pickled_module_dictionary = mc.pickle_dict(module_dictionary)
    # Call "json_dict" to serialise the dictionary using json
    json_module_dictionary = mc.json_dict(module_dictionary)

    try:
        # Call "create_text_file_from_json" to create a text file using json-serialised dictionary
        Student_data = mc.create_text_file_from_json(json_module_dictionary)
    except:
        print('The text file could not be created ... Terminating the programme ...')
        sys.exit(1)

    # Call "write_key" to generate an encryption key
    try:
        mc.write_key()
    except OSError:
        print('The encryption key could not be generated ... Terminating the programme ...')
        sys.exit(1)

    # Call "load_key" to read the encryption key and store it in a variable
    try:
        module_file_key = mc.load_key()
    except OSError:
        print('The encryption key could not be loaded ... Terminating the programme ...')
        sys.exit(1)

    # Call "encrypt_text_file" to encrypt the text file containing json-serialised dictionary
    try:
        encrypted_student_data = mc.encrypt_text_file(Student_data, module_file_key)
    except:
        print('The text file could not be encrypted ... Terminating the programme ...')
        sys.exit(1)

    # Call send_to_server to send the encrypted text file, and the serialised dictionaries to the server
    send_to_server(encrypted_student_data, json_module_dictionary, pickled_module_dictionary)


if __name__ == '__main__':
    main()
