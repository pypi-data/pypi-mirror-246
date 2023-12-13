#!/usr/bin/env python3

# A simple socket-based client and server program, with optional
# encryption and serialization, deliberately avoiding the complexity
# and overhead of SSL/TLS, for adapting for your particular needs.

# It can run as either the client or the server, and can use either
# UDP or TCP.  As a client, it sends a request to the server and waits
# for a response.  As a server, it responds to client requests by
# applying a user-supplied function to data read from files.  It
# specifically doesn't use any kind of handshake or back-and-forth
# protocol: for each request, one message goes from client to server,
# and one message from server to client.  If using encryption, two
# pre-shared key pairs are needed: one with the private key on the
# server, to decrypt the request; and one with the private key on the
# client, to decrypt the reply.

# The data-handling part handles re-reading files when they change,
# and is biased towards reading CSV files, as that is what I wanted
# for my original application of this; it also handles JSON files, or
# you can provide your own function to read anything you like.

# The query and result don't have to be strings; JSON or pickle
# serialization are available in the package.

# I wrote this in this form because I couldn't find any single example
# that did all the pieces of what I wanted.  I hope it is of
# "exemplary" quality for people to base their programs on, but I'm
# awaiting feedback on that.

# Example application scenario: the program runs as a server on my
# home server (a Raspberry Pi) and reads a CSV file containing an
# inventory of my possessions, with shelf/box/cupboard numbers, and a
# CSV file describing the locations, and tells me where something
# should be.  An Android app (which I haven't yet written) will fetch
# completions as I enter the name of something I'm trying to find, and
# then tell me where the thing is supposedly stored; or will scan the
# asset tag barcode (yes, I'm that nerdy) on something I'm holding,
# and tell me which box or shelf I should return it to.

# For the smaller examples I built this from, see:
# - https://docs.python.org/3.2/library/socketserver.html
# - https://stackoverflow.com/questions/28426102/python-crypto-rsa-public-private-key-with-large-file/28427259

import argparse
import base64
import csv
import decouple
import io
import json
import os
import pickle
import socket
import socketserver
import stat
import sys
import threading
import types
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random

################################
# Handling the underlying data #
################################

def read_csv_as_dicts(filename, keyfield, row_modifier):
    """Read a CSV file, producing a dictionary for each row.

    The rows are held in a dictionary, with the named column as the
    key (by default, the column called 'Name').

    If a row_modifier argument is given, it is applied to each row,
    and the result of that is stored instead of the row.  The indexing
    column name refers to this modified row rather than the original.

    """
    if keyfield is None:
        keyfield ='Name'
    with io.open(filename, 'r', encoding='utf-8') as instream:
        return ({modified_row[keyfield]: modified_row
                 for modified_row in [row_modifier(row)
                                      for row in csv.DictReader(instream)]}
                if row_modifier is not None
                else {row[keyfield]: row
                      for row in csv.DictReader(instream)})

def read_csv_as_lists(filename, keycolumn, row_modifier):
    """Read a CSV file, producing a list for each row.

    The rows are held in a dictionary, taking the specified column (0 by
    default) for the keys.

    If a row_modifier argument is given, it is applied to each row,
    and the result of that is stored instead of the row.  The indexing
    column number refers to this modified row rather than the
    original.

    """
    if keycolumn is None:
        keycolumn = 0
    with io.open(filename, 'r', encoding='utf-8') as instream:
        return ({modified_row[keycolumn]: modified_row
                 for modified_row in [row_modifier(row)
                                      for row in csv.reader(instream)]}
                if row_modifier is not None
                else {row[keycolumn]: row
                      for row in csv.reader(instream)})

def read_json(filename, _k, _m):
    """Read a JSON file."""
    with io.open(filename, 'r', encoding='utf-8') as instream:
        return json.load(instream)

class badReaderDescription(Exception):

    """An exception for when the description of how to read a file is not understood."""

    def __init__(self, filename, reader_description):
        self.filename = filename
        self.reader_description = reader_description

def preprocess_file_readers(files):
    """Convert the file reader descriptions into a more convenient form."""
    reader_functions = {}
    reader_keys = {}
    reader_modifiers = {}
    for filename, reader in files.items():
        filename = os.path.basename(filename)
        row_modifier = None
        if reader is None:
            reader = read_json
            key = None
        elif isinstance(reader, str):
            key = reader
            reader = read_csv_as_dicts
        elif isinstance(reader, int):
            key = reader
            reader = read_csv_as_lists
        elif type(reader) == tuple:
            if isinstance(reader[0], types.FunctionType):
                key = reader[1]
                reader = reader[0]
            elif isinstance(reader[1], types.FunctionType):
                key = reader[0]
                row_modifier = reader[1]
                if isinstance(key, str):
                    reader = read_csv_as_dicts
                elif isinstance(key, int):
                    reader = read_csv_as_lists
                else:
                    raise(badReaderDescription, filename, reader)
            else:
                raise(badReaderDescription, filename, reader)
        else:
            key = None
        reader_functions[filename] = reader
        reader_keys[filename] = key
        reader_modifiers[filename] = row_modifier
    return (reader_functions, reader_keys, reader_modifiers)

class simple_data_server():

    """A pair of TCP and UDP servers for accessing data from some files.

    The servers use the same underlying function and data, and this class
    provides a place to hold the description of the files used for the
    data.

    The function `client_server_main' is provided as an easy way to use
    this class.

    The user specifies a function for getting the result, and a
    description of the files to read to get the data.  If the files have
    changed since the previous use, they are re-read before the user
    function is called.

    The file description is a dictionary binding filenames to indications
    of how to read the file:

      - a string, meaning to read the file as CSV and produce a dictionary
        of row dictionaries, using the string to select the column to use
        for the keys in the outer dictionary

      - an integer, meaning to read the file as CSV and produce a
        dictionary of row lists, with the number selecting the column
        to use for the dictionary keys

      - a tuple of a string or an integer (treated as above) and a
        function, which is applied to each row as it is read, and the
        return value of which is stored in the resulting dictionary;
        the indexing string or number refers to the modified row,
        allowing indexing on a value constructed from the file data in
        the case of the raw data not having a suitable field for
        indexing it by

      - a tuple of a function and a value to pass as the second argument of
        the function, the first argument being the filename

      - None, meaning to read the file as JSON

    The user-supplied query function is called with two arguments:

      - the data from the TCP or UDP input

      - a dictionary binding the basename of each filename to the data
        read from that file

    It should return the data to send back over TCP or UDP.

    The user function can call:

        get_server().set_reply_key(filename, passphrase)

    to change the key used for the reply.  Leaving this to the user
    function allows the application to have its own way of allowing
    multiple users; for example, if JSON serialization is used, it
    could be a field in the dictionary holding the query.

    The servers are accessed via the threads that hold them, and the
    server structure attached to the threads holds the query function,
    for reasons explained in the docstring of the `service_thread'
    class.

    Four versioning bytes are included in the protocol, in case someone
    produces incompatible versions later.  For now, only the encryption
    scheme and serialization scheme are used.

    """

    def __init__(self,
                 host, port,
                 user_get_result, files,
                 query_key=None, reply_key=None):
        # Network
        self.host = host
        self.port = port
        # Data
        self.files_readers = files
        # Set the "time last read" for each file to the epoch, so that
        # the data will be read the first time check_data_current is
        # called:
        self.files_timestamps = {filename: 0
                                 for filename in files.keys()}
        self.files_data = {os.path.basename(filename): None
                           for filename in files.keys()}
        (self.file_reader_functions,
         self.file_reader_keys,
         self.file_reader_modifiers) = preprocess_file_readers(files)
        self.user_get_result = user_get_result
        # Encryption
        self.query_key = query_key
        self.reply_key = reply_key
        # The service threads
        self.udp_server = service_thread(
            args=[socketserver.UDPServer((self.host, self.port),
                                         MyUDPHandler)],
            server=self)
        self.tcp_server = service_thread(
            args=[socketserver.TCPServer((self.host, self.port),
                                         MyTCPHandler)],
            server=self)

    def start(self):
        """Start the server threads."""
        self.udp_server.start()
        self.tcp_server.start()

    def check_data_current(self):
        """Check for the data files changing, re-reading if necessary."""
        for filename, timestamp in self.files_timestamps.items():
            now_timestamp = os.path.getctime(filename)
            if now_timestamp > timestamp:
                basename = os.path.basename(filename)
                self.files_data[basename] = self.file_reader_functions[basename](
                    filename,
                    self.file_reader_keys[basename],
                    self.file_reader_modifiers[basename])
                self.files_timestamps[filename] = now_timestamp

    def get_result(self, data_in,
                   protocol_version=ord('0'),
                   encryption_scheme=ord('p'),
                   representation_scheme=ord('t'),
                   application_version=ord('0')):
        """Return the result corresponding to the input argument.

        This calls the user-supplied get_result function, using
        encryption if specified.  (The user function doesn't handle
        any of the encryption itself.)
        """
        return encrypt(
            serialize_to_bytes(
                self.user_get_result(
                    deserialize_from_bytes(
                        decrypt(data_in,
                                self.query_key,
                                encryption_scheme),
                        representation_scheme),
                    self.files_data),
                representation_scheme),
            self.reply_key,
            encryption_scheme)

    def process_request(self, incoming):
        # I hoped I could use: bytes(incoming[:4], 'utf-8')
        (protocol_version, encryption_scheme, representation_scheme,
         application_version) = (incoming[:4]
                                 if type(incoming) == bytes
                                 else (ord(incoming[0]),
                                       ord(incoming[1]),
                                       ord(incoming[2]),
                                       ord(incoming[3])))
        incoming = incoming[4:].strip()
        self.check_data_current()
        return (bytes((protocol_version, encryption_scheme,
                       representation_scheme, application_version))
                + self.get_result(
                    incoming,
                    protocol_version, encryption_scheme,
                    representation_scheme, application_version))

    def set_reply_key(self, key_filename, key_passphrase):
        """Select the key to be used for the reply.
        Use as:
        get_server().set_reply_key(filename, passphrase)
        from within your get_result function.
        """
        self.reply_key = read_key(key_filename, key_passphrase)

def get_server():
    """Return the server under which you are running."""
    return threading.current_thread().server

#############################
# encryption and decryption #
#############################

# See longer.py for versions of these two functions with more
# intermediate variables, if you find that more readable.

def hybrid_encrypt(plaintext, asymmetric_key):
    """Encrypt the plaintext, using a randomly generated symmetric key.

    The symmetric key is encrypted with the given asymmetric_key, and
    that encrypted key is returned, with the encrypted input appended.
    """
    symmetric_key = Random.new().read(32)
    initialization_vector = Random.new().read(AES.block_size)
    return ((asymmetric_key.publickey().encrypt(initialization_vector + symmetric_key, 32)[0]) # asymmetrically encrypted symmetric iv and key
            + (initialization_vector
               + (AES.new(symmetric_key, AES.MODE_CFB, initialization_vector)
                  .encrypt(plaintext))) # symmetrically encrypted payload
            )

def hybrid_decrypt(ciphertext, asymmetric_key):
    """Use the asymmetric key to decrypt a symmetric key.

    The asymmetric key is at the start of the ciphertext.  That key is
    then used to decrypt the rest of the ciphertext.
    """
    symmetric_key_and_iv = asymmetric_key.decrypt(
        ciphertext[:128]        # asymmetrically encrypted symmetric iv and key
    )[:48]
    return AES.new(symmetric_key_and_iv[AES.block_size:], # symmetric_key
                   AES.MODE_CFB,
                   symmetric_key_and_iv[:AES.block_size] # initialization vector
                   ).decrypt(
                       ciphertext[128:] # symmetrically encrypted payload
                   )[16:].decode()

def hybrid_encrypt_base64(plaintext, asymmetric_key):
    """As for hybrid_encrypt but the output is base64-encoded."""
    return base64.b64encode(hybrid_encrypt(plaintext, asymmetric_key))

def hybrid_decrypt_base64(ciphertext, asymmetric_key):
    """As for hybrid_decrypt but the input is base64-encoded."""
    return hybrid_decrypt(base64.b64decode(ciphertext), asymmetric_key)

def null_encrypt(plaintext, _):
    """A function for not encrypting at all."""
    return plaintext

def null_decrypt(ciphertext, _):
    """A function for not decrypting at all."""
    return ciphertext

class UnknownEncryptionType(Exception):

    """An exception for when the encryption type requested is unsupported."""

    def __init__(self, encryption_type):
        self.encryption_type = encryption_type

encryptors = {ord('0'): null_encrypt,
              ord('p'): null_encrypt,
              # don't expect this to work, while we still use readline:
              # ord('h'): hybrid_encrypt,
              ord('H'): hybrid_encrypt_base64
              }
decryptors = {ord('0'): null_decrypt,
              ord('p'): null_decrypt,
              # don't expect this to work, while we still use readline:
              # ord('h'): hybrid_decrypt,
              ord('H'): hybrid_decrypt_base64
              }

def encrypt(plaintext, key, encryption_scheme):
    """Encrypt plaintext with a key in a specified way.

    This encapsulates the lookup and calling of encryption functions.
    """
    if encryption_scheme not in encryptors:
        raise(UnknownEncryptionType(encryption_scheme))
    return encryptors[encryption_scheme](plaintext, key)

def decrypt(ciphertext, key, encryption_scheme):
    """Decrypt ciphertext with a key in a specified way.

    This encapsulates the lookup and calling of decryption functions.
    """
    if encryption_scheme not in decryptors:
        raise(UnknownEncryptionType(encryption_scheme))
    return decryptors[encryption_scheme](ciphertext, key)

############################################
# Data representation within the plaintext #
############################################

# The serializers return not only the serialized data but also the
# serialization scheme used, so the automatic serializer can pick a
# suitable scheme and inform its caller which one it picked.

def text_serializer(data):
    """Serialize a string as bytes."""
    if not isinstance(data, str):
        data = str(data)
    return bytes(data, 'utf-8'), ord('t')

def text_deserializer(data):
    """Deserialize a string from bytes."""
    return data.decode('utf-8')

def json_serializer(data):
    """Serialize data as JSON."""
    return bytes(json.dumps(data), 'utf-8'), ord('j')

def json_deserializer(data):
    """Deserialize data from JSON."""
    return json.loads(data.decode('utf-8'))

def pickle_serializer(data):
    """Serialize data by pickling."""
    return pickle.dumps(data), ord('p')

def automatic_serializer(data):
    """Serialize data in the most convenient way.
    If it is a string, convert it to a bytestring.

    If it can be represented in JSON, use that, as that's compatible
    with non-Python programs at the other end.

    If it can't be represented in JSON, fall back to Python's pickle
    serialization.
    """
    if isinstance(data, str):
        return text_serializer(data)
    try:
        return json_serializer(data)
    except TypeError:
        return pickle_serializer(data)

class UnknownRepresentationType(Exception):

    """An exception for unsupported representation types."""

    def __init__(self, represention_type):
        self.representation_type = representation_type

serializers = {ord('t'): text_serializer,
               ord('j'): json_serializer,
               ord('p'): pickle_serializer,
               ord('a'): automatic_serializer
               }
deserializers = {ord('t'): text_deserializer,
                 ord('j'): json_deserializer,
                 ord('p'): pickle.loads
                 }

def serialize_to_bytes_flexibly(data, representation_scheme):
    """Convert a data structure into a transmissable form.
Return the serialized data and a code for the representation used."""
    if representation_scheme not in serializers:
        raise(UnknownRepresentationType(representation_scheme))
    return serializers[representation_scheme](data)

def serialize_to_bytes(data, representation_scheme):
    result, _ = serialize_to_bytes_flexibly(data, representation_scheme)
    return result

def deserialize_from_bytes(data, representation_scheme):
    """Convert a serialized data structure into its usable form."""
    if representation_scheme not in deserializers:
        raise(UnknownRepresentationType(representation_scheme))
    return deserializers[representation_scheme](data)

#################################################
# Tying the query handler to the server classes #
#################################################

class service_thread(threading.Thread):

    """A wrapper for threads, that passes in a service function.

    The rationale for it is that the application-specific handlers
    passed to `socketserver.TCPServer' and `socketserver.UDPServer'
    are classes rather than class instances, so, as the instantiation
    of them is done out of our control, we can't pass in a query
    function argument.  However, in our query handler, we can find
    what the current thread is, so we use the server attached to that
    thread (this class) as somewhere to store the function.
    """

    def __init__(self,
                 server,
                 **rest):
        super().__init__(target=run_server,
                         **rest)
        self.server = server

class MyTCPHandler(socketserver.StreamRequestHandler):

    """The TCP handler for the simple_data_server class.

    It uses the `service_thread' class to determine what to do with the
    data.
    """

    def __init__(self,
                 *rest):
        super().__init__(*rest)
        self.allow_reuse_address = True

    def handle(self):
        """Handle a TCP request.

        The user-supplied 'getter' function is used to go from the
        input to the output.
        """
        self.wfile.write(
            get_server().process_request(
                # This probably shouldn't be a readline, but I'm not
                # sure how else to decide that we've read the lot when
                # using TCP.  Since we are b64-encoding the query,
                # it's safe for us to put a newline at the end of it.
                self.rfile.readline().strip().decode('utf-8')))

class MyUDPHandler(socketserver.BaseRequestHandler):

    """The UDP handler for the simple_data_server class.

    It uses the `service_thread' class to determine what to do with the
    data.
    """

    def __init__(self,
                 *rest):
        super().__init__(*rest)
        self.allow_reuse_address = True

    def handle(self):
        """Handle a UDP request.

        The user-supplied 'getter' function is used to go from the
        input to the output.
        """
        reply_socket = self.request[1]
        reply_socket.sendto(
            get_server().process_request(
                self.request[0]),
            self.client_address)

########################
# High-level functions #
########################

def run_server(server):
    server.serve_forever()

def run_servers(host, port, getter, files,
                query_key=None,
                reply_key=None):
    """Run TCP and UDP servers.

    They each apply the getter argument to the incoming queries, using
    the specified files.
    """
    simple_data_server(host, port,
                       getter, files,
                       query_key=query_key,
                       reply_key=reply_key).start()

def get_response(query, host, port, tcp=False,
                 query_key=None, reply_key=None,
                 protocol_version=ord('0'),
                 encryption_scheme=ord('H'),  # hybrid encryption, b64 encoding
                 representation_scheme=ord('a'),  # auto choose serialization
                 application_version=ord('0')):
    """Send your query to the server, and return its result.

    This is the core of a client suitable for the simple_data_server
    class.

    The input and output may be anything that the given representation
    scheme can represent.  For 't', this is text; for 'j', anything
    that can be represented as JSON, and for 'p', any
    pickle-serializable Python data.
    """
    query, representation_scheme = serialize_to_bytes_flexibly(
        query, representation_scheme)
    if query_key:
        query = encrypt(query, query_key, encryption_scheme)
    else:
        encryption_scheme = ord('p')
    query = (bytes((protocol_version,
                    encryption_scheme,
                    representation_scheme,
                    application_version))
             + query
             # because we use readline:
             + bytes("\n", 'utf-8'))
    if tcp:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        more = True
        received = b""
        sock.connect((host, int(port)))
        sock.sendall(query)
        while more:
            now_received = sock.recv(1024)
            if now_received == b"":
                more = False
            else:
                received += now_received
        sock.close()
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(query, (host, int(port)))
        received = sock.recv(1024)
    (protocol_version, encryption_scheme,
     representation_scheme, application_version) = received[:4]
    return deserialize_from_bytes(decrypt(received[4:],
                                          reply_key,
                                          encryption_scheme),
                                  representation_scheme)

def read_key(filename, passphrase=None):
    """Wrap importKey with file opening, for easy use in comprehensions."""
    with open(filename) as reply_stream:
        return RSA.importKey(reply_stream.read(),
                             passphrase=passphrase)

def client_server_add_arguments(parser, port=9999, with_short=False):
    """Add the argparse arguments for the server.

    The optional argument 'port' specifies the default port to use.
    If the argument 'with_short' is given and non-False, add short
    options too; otherwise make them something less likely to clash
    with non-demo applications.
    """
    parser.add_argument('--host', '-H' if with_short else '-SH',
                        default="127.0.0.1",
                        help="""The server to handle the query.""")
    parser.add_argument('--port', '-P' if with_short else '-SP',
                        default=port,
                        help="""The port on which to send the query.""")
    parser.add_argument("--tcp", "-t" if with_short else '-St',
                        action='store_true',
                        help="""Use a TCP connection the server.
                        Otherwise, UDP will be used.
                        Only applies when running as a client;
                        the server always does both.""")
    parser.add_argument("--query-key", "-q" if with_short else '-Sqk',
                        help="""The key files for decrypting the queries.
                        These are public keys, so may be visible to
                        all users.""")
    parser.add_argument("--reply-key", "-r" if with_short else '-Srk',
                        default=None,
                        help="""The key file for encrypting the replies.
                        This is a private key, so should be kept unreadable
                        to everyone except the server user.
                        Without this, replies are sent in plaintext.""")

def check_private_key_privacy(args):
    """Check that the private key pointed to really is private."""
    private_key = args.query_key if args.server else args.reply_key
    if private_key:
        key_perms = os.stat(private_key).st_mode
        if key_perms & (stat.S_IROTH
                        | stat.S_IRGRP
                        | stat.S_IWOTH
                        | stat.S_IWGRP):
            print("Key file", private_key, "is open to misuse.")
            sys.exit(1)

def read_keys_from_files(args, query_passphrase, reply_passphrase):
    """Read a pair of keys from their files."""
    return ((read_key(args.query_key, query_passphrase)
             if args.query_key and len(args.query_key) > 0
             else None),
            (read_key(args.reply_key, reply_passphrase)
             if args.reply_key and len(args.reply_key) > 0
             else None))

def client_server_main(getter, files, verbose=False):
    """Run a simple client or server.

    The argument `getter' is a function to be used by the server to
    process the data it gets from the client.  It should take two
    arguments, a string and a dictionary binding basenames of filenames to
    the result of the reader functions for those file (see below), and
    return the result string.

    The argument `files' is a dictionary binding filenames to functions
    for reading them.  The reading functions may be functions of two args,
    one the filename and the other a key, or a tuple of the function and
    the key, or a string, in which case it is used as the key for a
    built-in reader function using csv.DictReader, or a number, in which
    case it is used as the key for a built-in reader function using
    csv.reader, or None, in which case the file is read as JSON.

    You may be able to use this directly as the 'main' function of
    your program, but you will probably have extra pieces you need, so
    some parts of it have been split out for you to call from your own
    'main'.

    See the documentation of the simple_data_server class, or the
    accompanying README.md, for a less terse description.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--gen-key",
                        help="""Generate a key in the specified file, and its
                        associated public key in that name + '.pub'.
                        Uses the 'query_passphrase' from the .env file unless
                        the '--server' argument is also given, in which case it
                        uses the 'reply_passphrase'.
                        No other action is done.""")
    parser.add_argument('--server', '-S',
                        action='store_true',
                        help="""Run as the server.
                        Otherwise, it will run as a client.
                        If given with --gen-key,
                        make it generate a key using the server passphrase.""")
    parser.add_argument('data', nargs='*', action='append',
                        help="""The data to send to the server.""")
    client_server_add_arguments(parser)
    args = parser.parse_args()
    query_passphrase = decouple.config('query_passphrase')
    reply_passphrase = decouple.config('reply_passphrase')
    if args.gen_key:
        passphrase = reply_passphrase if args.server else query_passphrase
        with open(args.gen_key, 'w') as keystream:
            with open(args.gen_key + ".pub", 'w') as pubkeystream:
                key = RSA.generate(1024, Random.new().read)
                keystream.write(str(key.exportKey(passphrase=passphrase),
                                    'utf-8'))
                pubkeystream.write(
                    str(key.publickey().exportKey(passphrase=passphrase),
                        'utf-8'))
        return None
    else:
        check_private_key_privacy(args)
        query_key, reply_key = read_keys_from_files(args,
                                                    query_passphrase,
                                                    reply_passphrase)

        if args.server:
            run_servers(args.host, int(args.port),
                        getter=getter,
                        files=files,
                        query_key=query_key,
                        reply_key=reply_key)
            return None
        else:
            text = " ".join(args.data[0])
            received = get_response(
                text,
                args.host, args.port, args.tcp,
                encryption_scheme=ord('H'
                                      if query_key and reply_key
                                      else 'p'),
                query_key=query_key,
                reply_key=reply_key)

            if verbose:
                print("Sent:     {}".format(text))
                print("Received: {}".format(received))
            return received

###########
# Example #
###########

demo_filename = "/var/local/demo/demo-main.csv"

def demo_getter(in_string, files_data):
    """A simple query program for CSV files.

    It uses the first column in the CSV file as the key, and returns
    the whole row.
    """
    return str(files_data[os.path.basename(demo_filename)]
               .get(in_string.strip().split()[0],
                    ["Unknown"]))

def main():
    client_server_main(demo_getter,
                       {demo_filename: 0},
                       verbose=True)

if __name__ == "__main__":
    main()
