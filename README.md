# Client_Server Network Programming - CSCK541 - October 2022 A - Masoud Naseri and Kim Wa Yeung

These sets of programmes explore (i) serialisation using json and pickle, (ii) creating text files, (iii) encrypting and decrypting text files, and (iv) creating a Client-Server programme using which the serialised data and the encrypted text file can be sent by Client to the Server on a local machine.
## Table of Contents
* [Change History](#change-history)
* [Overview of the programme](#overview-of-the-programme)
* [Install](#install)
* [Usage](#usage)
* [Tests](#tests)
* [Questions and comments](#questions-and-comments)
* [Contributing](#contributing)
* [Copyright](#copyright)

## Change history

November 2022:
* Initial version created on 19 December 2022.

## Overview of the programme
This programme package consists of three source codes:

1. **`Main_Code.py`:** This programme can be run as a standalone code. 
It receives some data about a hypothetical student who is enrolled in course and has received three grades for his/her modules A, B, and C. 
These inputs are used to create a dictionary. The dictionary is further serialised using json and pickle.
The json-serialised dictionary, which has a string type, is further written into a text file. 
The text file is then encrypted using cryptography library, which is built on top of the AES algorithm. The encrypted content
is saved in a new file. The encrypted data are further decrypted using the same key (i.e., symmetric encryption).
The decrypted data re finally saved in a separate file. 
  
2. **`Server_Code.py`:** This programme is the Server part of a Client-Server socket programme. 
Some information about a student is received from Client. This information includes some dictionaries serialised using json and pickle.
It also includes receiving an encrypted text file, whose content will be saved in a separate file, and will then be decrypted. 
The content of the text file is basically a json-string which is the serialised dictionary containing student's information.
3. **`Client_Code.py`:** This programme is the Client part of a Client-Server socket programme. 
It explores sending some information to a server on the same machine. The data are created and prepared using by calling
some functions from Main_Code.py module. In particular, this programme generates a dictionary containing some data of a student.
The dictionary is later serialised using pickle and json. The pickled and json serialised dictionaries are then sent to
the server. The json serialised dictionary is also used to generate a text file. The text file is then sent to sever after 
being encrypted. The content of the text file is basically the json serialised dictionary.

## Install
The required packages that must be installed prior to running the programme can be found in `requirements.txt`. 
After changing the directory to the one where `requirements.txt` is located, the packages can be installed by running 
the following command in the shell terminal: 
`pip install -r requirements.txt`

## Usage
To execute the programme, change the directory to `/src` on your shell terminal and execute

- `python -m Main_Code`

To execute the Client-Server code, change the directory to `/src` on your shell terminal, and then first execute 
- `python -m Server_Code`

Open a separate shell terminal, and change the directory to `/src`, and then execute
- `python -m Client_Code`

These programmes create `.txt` files in the same directory. The encryption key will be saved as `file_key.key` in the
same directory. 

## Tests 
There are seven basic unit tests in this programme run on the `Main_Code.py` source code. 
The source codes of the tests can be found in `/test/Unit_Tests.py`. In order to run the tests, change directory to `/test/` 
and execute the below command in your shell terminal:

`python -m unittest Unit_Tests`

You can run the tests with more detail (i.e., higher verbosity) by passing in the -v flag as given below:

`python -m unittest -v Unit_Tests`
  
## Questions and comments
Please send email to <a href = "mailto: naseri.masoud@outlook.com">Masoud Naseri</a> and/or 
to <a href = "mailto: K.Yeung7@liverpool.ac.uk">Kim Wa Yeung</a> if there is any question or comment about the codes. 

## Contributing
By developing this programme, the following key contributions are made:
  - The name of the text files correspond to the name of the student, whose information are saved in the text files. 
  - The name of the encrypted files, decrypted files, and those received by the server correspond to the name of the student and whether they are encrypted/decrypted files. 
  - Seven basic unit tests are run on all the functions.  
  - The `__doc__` properties of all modules are generated as `html` files according to PEP-8 standard using
    - `pydoc -w Main_Code` 
    - `pydoc -w Server_Code` 
    - `pydoc -w Client_Code`
  - A one-to-one dialogue exists between the Client and Server, where sending and receiving the data are confirmed by exchanging confirmation messages.
  - While some `try... except...` blocks are used inside some functions, some more high-level exceptions are defined for when the function is called. 

## Copyright
Copyright 2022 "Masoud Naseri" and "Kim Wa Yeung" Licensed under the MIT License, (the "License");
you may not use this file except in compliance with the License.
