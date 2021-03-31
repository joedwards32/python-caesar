# python-caesar

python-caesar is a simple python project based around the trivial problem of solving caesar ciphers.

It is intended purely as a demonstration of basic software development in python3, including argument parsing and unit testing.

caesar.py can encrypt, decrypt and brute force caesar ciphers.

## Usage

To get help:

~~~
./caesar.py --help

usage: caesar.py [-h] [-m [{encrypt,decrypt,force}]] [-i INPUT_FILE]
                 [-o OUTPUT_FILE] [-s SHIFT]

Encrypt, decrypt or brute force using a simple Caesar cipher.

optional arguments:
  -h, --help            show this help message and exit
  -m [{encrypt,decrypt,force}], --mode [{encrypt,decrypt,force}]
                        Encrypt, decrypt or brute force input text.
  -i INPUT_FILE, --input-file INPUT_FILE
                        Input file, defaults to stdin
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Output file, defaults to stdout
  -s SHIFT, --shift SHIFT
                        Caesar shift value
~~~

To encrypt a string:

~~~
echo 'hello world' | ./caesar.py
~~~

To decrypt a string with a known shift value:

~~~
echo 'Vszz}.e}!zr' | ./caesar.py -m decrypt -s 14
~~~

To decrypt a string with an unknown shift value:

~~~
echo 'Vszz}.e}!zr' | ./caesar.py -m force
~~~

Files are also supported as input/output:

~~~
./caesar.py -m encrypt -s 14 -i words -o ciphered_words
./caesar.py -m decrypt -s 14 -i ciphered_words -o unciphered_words
~~~

## Limitations

Known limitations/opportunities for improvement:

* Brute forcing of large inputs is currently very inefficient. Caesar ciphers can be trivially broken with only a few lines of input. Using a generator function to itterate over an increasing amount of input until the cipher is solved would be better.

## Testing

Python Unittest and Coverage care used to support unit testing.

To run tests:

~~~
python3-coverage run -m unittest test_caesar.py
~~~

To report on coverage:

~~~
python3-coverage report
~~~

To generate an HTML report:

~~~
python3-coverage html
google-chrome htmlcov/index.html
~~~
