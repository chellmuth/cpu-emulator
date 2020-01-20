$ pipenv install # or however you want to install the requirements in the Pipfile

### Run the webapp
$ FLASK_APP=webapp.py flask run

### View a binary
$ python hexdump.py FILE

### Assemble a binary
$ python assembler.py program.txt # writes to out.o

### Disassemble a binary
$ python disassembler.py out.o