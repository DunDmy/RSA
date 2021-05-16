import sys


def get_bin(hex_n):

    # get the lenght of the string
    hex_len = len(hex_n) * 4
    # convert to bin
    bin_text = bin(int(hex_n, 16))[2:]
    # add leading 0
    if len(bin_text) < hex_len:
        bin_text = '0' * (hex_len - len(bin_text)) + bin_text
    return bin_text


# this function gets decimal value from the bin
def get_dec(bin_n):
    dec_n = int(bin_n,2)
    return dec_n


# this function gets a hex value from the bin
def get_dec_hex(bin_n):
    dec_n = int(bin_n,16)
    return dec_n


# this function gets from a plain text
def get_bins_from_plain(plaintext):
    text = list(plaintext)

    for char in range(0, len(text)):
        text[char] = hex(ord(text[char]))[2:]

    text = ''.join(text)
    text_dec = int(text, 16)

    return text_dec


def get_square_and_multiply(x, e):
    exp = e

    value = x
 
    for i in range(2, len(exp)):
        value = value * value
        #print (i,":\t",value,"(square)")
        if(exp[i:i+1]=='1'):
            value = value*x
            #print (i,":\t",value,"(multiply)")
    return value


# Repeated squares function
def get_exponentiation(value, exp, n):

    if (exp == 0):
        return 1
    if (exp == 1):
        return value % n
      
    t = get_exponentiation(value, int(exp / 2), n)
    t = (t * t) % n
      
    # if exponent is
    # even value
    if (exp % 2 == 0):
        return t
          
    # if exponent is
    # odd value
    else:
        return ((value % n) * t) % n


def encrypt(n, e, p):
    cipher_text = ''
    enc_blocks = []
    n_dec = get_dec(get_bin(n))
    e_dec = get_dec_hex(e)
    ciphertext = -1

    if (len(p) > 0):
        # get the first ASCII value
        ciphertext = ord(p[0])

    for i in range(1, len(p)):
        enc_blocks.append(ciphertext)
        ciphertext = 0
        ciphertext = ord(p[i])
        
    # add the last value
    enc_blocks.append(ciphertext)

    # encrypt values
    for i in range(len(enc_blocks)):
        enc_blocks[i] = str(get_exponentiation(enc_blocks[i], int(e_dec), int(n_dec)))

    # create a string from the numbers
    cipher_text = " ".join(enc_blocks)

    return cipher_text 


def decrypt(n, d, c):
    int_blocks = []
    plain_text = ''
    n_dec = get_dec(get_bin(n))
    d_dec = get_dec(get_bin(d))
    list_blocks = c.split(' ')
    block_size = len(list_blocks)    

    for s in list_blocks:
        int_blocks.append(int(s))

    # converts each int in the list to block_size number of characters
    # by default, each int represents two characters
    for i in range(len(int_blocks)):
        # decrypt values
        int_blocks[i] = get_exponentiation(int_blocks[i], int(d_dec), int(n_dec))
        tmp = ""
        # convert numbers back ASCII chars
        for c in range(block_size):
            tmp = chr(int_blocks[i])
        plain_text += tmp

    return plain_text


def RSA_encrypt(plaintext, publicKeyFileName, ciphertextFileName):
    n = publicKeyFileName[0]
    e = publicKeyFileName[1]

    cypher_text = encrypt(n, e, plaintext)
    cipher_writer = open(ciphertextFileName, "a")
    cipher_writer.writelines(str(cypher_text))
    cipher_writer.close()

    return 0


def RSA_decrypt(ciphertext, privateKeyFileName, plaintextFileName):
    n = privateKeyFileName[0]
    d = privateKeyFileName[1]

    plain_text = decrypt(n, d, ciphertext)
    cipher_writer = open(plaintextFileName, "a")
    cipher_writer.writelines(str(plain_text))
    cipher_writer.close()
    return 0


def main(argv):
    plain_text_file = ''
    ecryption_text_file = ''
    operation = argv[1]

    if operation == 'e':
        plain_text_file = argv[2]
    else:
        ecryption_text_file = argv[2]
    
    key_file = argv[3]
    output_file = argv[4]

    if operation == 'e':
        key_reader = open(key_file, 'r')
        output_writer = open(output_file, 'x')

        # get n and e
        n = key_reader.readline()
        key_reader.readline()
        e = key_reader.readline()


        # close files
        key_reader.close()
        output_writer.close()
        with open(plain_text_file, 'r') as reader:
            # handle a new line
            lines = (line.rstrip() for line in reader) 
            lines = list(line for line in lines if line)
            # read line
            for line in lines:
                RSA_encrypt(str(line), [n,e], output_file)

    elif operation == 'd':
        key_reader = open(key_file, 'r')
        output_writer = open(output_file, 'x')
        # get a key
        n = key_reader.readline()
        key_reader.readline()
        d = key_reader.readline()

        # close files
        key_reader.close()
        output_writer.close()

        with open(ecryption_text_file, 'r') as reader:
            # handle a new line
            lines = (line.rstrip() for line in reader) 
            lines = list(line for line in lines if line)
            # read line
            for line in lines:
                RSA_decrypt(line, [n, d], output_file)
    else:
        print("INVALID OPERATION!")


if __name__ == "__main__":
    main(sys.argv)
