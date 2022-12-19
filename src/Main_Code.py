"""This programme receives some data about a student, his/her module's grades and course name.
These data are then stored in a dictionary and serialised using json and pickle methods.
These are defined in separate functions.
This programme also creates a text file.
The text file can be created by passing a json dictionary as text where the filename corresponds to the name of
the student.
Alternatively, one can load a DOCX-reading file, and re-write th content in a text file.
In either case, the text file is encrypted using cryptography library, which is built on top of the AES algorithm.
This is done by passing the name of the file to the encryption function.
The encrypted file will then be decrypted using the same key (i.e., symmetric encryption) and its content will be stored
in a sepa|rate file.
Finally, the file contents will be printed out on screen as well.

Please note that, while this programme can be run on its own and perform the above-mentioned tasks, its functions can be
called from within a Server-Client code.
"""

import json
import pickle
from cryptography.fernet import Fernet
import sys


def receive_data():
    """
    Receive data from user including name of the student, name of the course, and his/her grades for Modules A, B and C
    :return: grade_module_A, grade_module_B, grade_module_C, fullname, course_name
    """
    name = input('Name of the student: ')
    course = input('Name of the course: ')

    while True:
        # Ensure the suer enters a value, not a string
        try:
            grade_moduleA = float(input('Grade for Module A: '))
        # Print an error message and repeat the loop until a floating value is entered by the user
        except ValueError:
            print("Oops! You did not enter a valid Grade A. Try again...")
            continue
        # Ensure the grade is between 0 and 100
        if 0 <= grade_moduleA <= 100:
            break
        else:
            print("The range must be 0 to 100 for Grade A. Try again...")

    while True:
        # Ensure the suer enters a value, not a string
        try:
            grade_moduleB = float(input('Grade for Module B: '))
        # Print an error message and repeat the loop until a floating value is entered by the user
        except ValueError:
            print("Oops! You did not enter a valid Grade B. Try again...")
            continue
        # Ensure the grade is between [0,100]
        if 0 <= grade_moduleB <= 100:
            break
        else:
            print("The range must be 0 to 100 for Grade B. Try again...")

    while True:
        # Ensure the suer enters a value, not a string
        try:
            grade_moduleC = float(input('Grade for Module C: '))
        # Print an error message and repeat the loop until a floating value is entered by the user
        except ValueError:
            print("Oops! You did not enter a valid Grade C. Try again...")
            continue
        # Ensure the grade is between [0,100]
        if 0 <= grade_moduleC <= 100:
            break
        else:
            print("The range must be 0 to 100 for Grade C. Try again...")

    return name, course, grade_moduleA, grade_moduleB, grade_moduleC


def create_dict(name, course, grade_A, grade_B, grade_C):
    """
    Create a dictionary and populate it with a set of values received as function arguments.
    :param name: Full name of the student, type: str
    :param course: Name of the course of the student, type: str
    :param grade_A: Grade of Module A of the student, type: float
    :param grade_B: Grade of Module B of the student, type: float
    :param grade_C: Grade of Module C of the student, type: float
    :return: A module dictionary created for the respective student
    """
    dictionary = {}
    dictionary['Full Name'] = name
    dictionary['Programme'] = course
    dictionary['Grades'] = {}
    dictionary['Grades']['Module A'] = grade_A
    dictionary['Grades']['Module B'] = grade_B
    dictionary['Grades']['Module C'] = grade_C
    dictionary['GPA'] = round((grade_A + grade_B + grade_C) / 3, 2)
    print(f'\nModule dictionary for {name} created ...')
    return dictionary


def json_dict(data):
    """
    Serialise the data using json and return it
    :param data: Data that should be serialised
    :return: Serialised data using json
    """
    json_dictionary = json.dumps(data, indent=4)
    print('Serialisation using json successful ...')
    return json_dictionary


def pickle_dict(data):
    """
    Serialise the data using pickle and return it
    :param data: Data that should be serialised
    :return: Serialised data using pickle
    """
    pickled_dictionary = pickle.dumps(data)
    print('Serialisation using pickle successful ...')
    return pickled_dictionary


def create_text_file_from_json(content):
    """
    Create a text file and write the "content" in the file. The name of the file is extracted from the passed content
    :param content: A json-serialised dictionary
    :return: filename, Type: str
    """
    # Convert json string to a dictionary for reading the full name of the student
    try:
        dictionary = json.loads(content)
    except TypeError:
        print('The json.loads de-serialisation should receive string. The passed argument is converted to string...')
        content = str(content)
        dictionary = json.loads(content)

    # Read the full name of the student and create a text file for the corresponding student
    try:
        student_name = dictionary['Full Name']
    except KeyError:
        print('The argument returned by jason.loads does not have a correct dictionary format... '
              'Terminating the programme...')
        raise

    filename = student_name + '.txt'
    # Create a text file containing the module grades for the corresponding student
    with open(filename, 'w') as f:
        f.write(f'The module grades for {student_name} are given below:\n')
        f.write(content,)
    print('Text file using json-dictionary data created ...')
    return filename


def write_key():
    """
    Generate a fresh Fernet key and save it in the file "file_key.key". This must be kept in a safe place.
    :return: None
    """
    key = Fernet.generate_key()
    with open("file_key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    """
    Load the key from the current directory named "key.key"
    :return: Key, Type: bytes
    """
    try:
        with open("file_key.key", "rb") as key_file:
            key = key_file.read()
    except FileNotFoundError:
        print('The key file does not exist... Terminating the programme...')
        raise
    return key


def encrypt_text_file(filename, key):
    """
    Given a filename and a key, encrypt the file and write it.
    :param filename: Name of the file that is to be encrypted, Type: str
    :param key: Encryption key, Type: bytes
    :return: Name of the encrypted file
    """

    # Open the file to read its content
    try:
        with open(filename, "rb") as reader:
            # Read all the date from the file
            data = reader.read()
    except FileNotFoundError:
        print('The file assigned to be encrypted does not exist... Terminating the programme...')
        raise

    # Initialize the Fernet class with the given "key"
    f = Fernet(key)
    # Encrypt the data of the file
    encrypted_data = f.encrypt(data)
    print('Encryption successful ...')
    # Write the encrypted file into a new file
    new_filename = filename.replace('.txt', '') + '_encrypted' + '.txt'
    with open(new_filename, "wb") as writer:
        writer.write(encrypted_data)
    print('Encrypted file created ...')
    return new_filename


def decrypt_text_file(filename, key):
    """
    Given a filename and key, decrypt the file and write it in a new file
    :param filename: Name of the file that is to be decrypted, Type: str
    :param key: Decryption key
    :return: Name of the decrypted file
    """

    try:
        with open(filename, "rb") as reader:
            # Read the encrypted data
            encrypted_data = reader.read()
    except FileNotFoundError:
        print('The file assigned to be decrypted does not exist... Terminating the programme...')
        raise

    # Initialize the Fernet class with the given "key"
    f = Fernet(key)
    # Decrypt the data
    decrypted_data = f.decrypt(encrypted_data)
    print('Decryption successful...')
    # Write the original data into a new file
    new_filename = filename.replace('_encrypted', '_decrypted')
    with open(new_filename, "wb") as writer:
        writer.write(decrypted_data)
    print('Decrypted file created ...')
    return new_filename


# Create main() to avoid running the whole codes when it is imported in other programmes.
def main():
    # Call "Receive_data" to receive the student's information from the user
    grade_module_A, grade_module_B, grade_module_C, fullname, course_name = receive_data()
    # Call "create_dict" to Create a dictionary using received inputs
    module_dictionary = create_dict(grade_module_A, grade_module_B, grade_module_C, fullname, course_name)
    # Call "json_dict" to serialise the dictionary using json
    module_dictionary_json = json_dict(module_dictionary)
    print(module_dictionary_json)
    # Call "create_text_file_from_json" to create a text file using json-serialised dictionary
    Student_data = create_text_file_from_json(module_dictionary_json)

    # Call "write_key" to generate an encryption key
    try:
        write_key()
    except OSError:
        print('The encryption key could not be generated ... Terminating the programme ...')
        sys.exit(1)

    # Call "load_key" to read the encryption key and store it in a variable
    try:
        module_file_key = load_key()
    except OSError:
        print('The encryption key could not be loaded ... Terminating the programme ...')
        sys.exit(1)

    # Call "encrypt_text_file" to encrypt the file
    try:
        encrypted_student_data = encrypt_text_file(Student_data, module_file_key)
    except:
        print('The file could not be encrypted ... Terminating the programme ...')
        sys.exit(1)

    # Call "decrypt_text_file" to decrypt the file and store the decrypted data in a separate file
    try:
        decrypted_student_data = decrypt_text_file(encrypted_student_data, module_file_key)
    except:
        print('The file could not be decrypted ... Terminating the programme ...')
        sys.exit(1)

    # Open the decrypted file, and print out its content on the screen.
    with open(decrypted_student_data, 'r') as reader:
        print('\nThe content of decrypted file:\n')
        for line in reader:
            print(line, end='')
    print('\n')


if __name__ == '__main__':
    main()
