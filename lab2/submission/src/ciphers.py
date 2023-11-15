"""
CSCI-603 Lab 2: Ciphers

A program that encodes/decodes a message by applying a set of transformation 
operations.

The transformation operations are:
    shift - Sa[,n] changes letter at index a by moving it n letters fwd in the 
        alphabet. A negative
        value for n shifts the letter backward in the alphabet.
    rotate - R[n] rotates the string n positions to the right. A negative value 
        for n rotates the string
        to the left.
    duplicate - Da[,n] follows character at index a with n copies of itself.
    trade - Ta,b swap the places of the a-th and b-th characters.
    affine - Aa,b applies the affine cipher algorithm y = (ax + b) mod 26 using 
        a and b as keys.

All indices numbers (the subscript parameters) are 0-based.

author: Shreesh Tripathi, st4083
"""


def _shift_letter(letter: str, offset: int = 1) -> str:
    """
    Shifts a particular letter by a given offset

    :param letter: The letter to be shifted
    :param offset: The offset by which the letter should be shifted

    :return shifted_letter: Resulting letter
    """

    letter_ord_base = ord(letter) - ord('A')
    letter_ord_base_shifted = (letter_ord_base + offset) % 26
    letter_ord_actual = letter_ord_base_shifted + ord('A')
    shifted_letter = chr(letter_ord_actual)
    return shifted_letter


def shift(message: str, letter_index: int, offset: int = 1) -> str:
    """
    Shifts letter at a given index in the message by a given offset

    :param message: The message containing the target letter
    :param letter_index: The index of target letter in message
    :param offset: The offset by which the target letter should be shifted

    :return out_message: Resulting message after the target letter is shifted 
        by offset
    """

    letter = message[letter_index]
    shifted_letter = _shift_letter(letter, offset)
    left_side = message[:letter_index]
    right_side = message[letter_index + 1:]
    out_message = left_side + shifted_letter + right_side
    return out_message


def rotate(message: str, k_times: int = 1) -> str:
    """
    Rotate message for the given number of times

    :param message: The message to be rotated
    :param k_times: Number of times the message should be rotated

    :return out_message: rotated message after k_times rotations
    """

    for _ in range(k_times % len(message)):
        message = message[-1] + message[:len(message) - 1]
    out_message = message
    return out_message


def duplicate(message: str, letter_index: int, k_times: int = 1) -> str:
    """
    Duplicates letter at a given index in the message, k number of times
    :param message: The message containing the target letter
    :param letter_index: Index of the target letter in the message
    :param k_times: The number of times target letter should be duplicated
    :return out_message: Resulting message after the target letter has been 
        duplicated
    """

    for _ in range(k_times):

        left_side = message[:letter_index]
        letter = message[letter_index]
        right_side = message[letter_index + 1:]

        message = left_side + letter + letter + right_side

    out_message = message
    return out_message


def remove_duplicate(message: str, letter_index: int, k_times: int = 1) -> str:
    """
    Remove instances of letter at a given index in the message, k times

    :param message: The message containing the target letter
    :param letter_index: Index of the target letter in the message
    :param k_times: Number of times the instance of letter should be removed

    :return out_message: Result after k instances of letter have been removed
    """

    for _ in range(k_times):
        message = message[:letter_index] + message[letter_index + 1:]
    out_message = message
    return out_message


def trade_ij(message: str, index_i: int, index_j: int) -> str:
    """
    Trade letters at index i and j in the given message

    :param message: Message containing letters letter_i and letter_j
    :param index_i: Index at which letter_i is present
    :param index_j: Index at which letter_j is present

    :return traded_message: Result after letters at index i & j have been traded
    """

    letter_i = message[index_i]
    letter_j = message[index_j]

    left = message[:index_i]
    middle = message[index_i + 1:index_j]
    right = message[index_j + 1:]

    traded_message = left + letter_j + middle + letter_i + right
    return traded_message


def affine_encrypt(message: str, a: int, b: int) -> str:
    """
    Perform affine encryption to each letter of the message string
    E(x) = (a * i + b) % m

    :param message: Message to be encrypted
    :param a: parameter 'a' in affine operation equation
    :param b: parameter 'b' in affine operation equation

    :return out_message: Encrypted message using affine operation
    """

    out_message = ""
    m = 26

    for letter in message:
        i = ord(letter) - ord('A')
        E_x = (a * i + b) % m
        out_letter = chr(E_x + ord('A'))
        out_message += out_letter
    return out_message


def _mod_mul_inv(a: int) -> int:
    """
    Find the modular multiplicative inverse of 'a'
    Where a * a_inv % m = 1

    :param a: Input variable 'a'

    :return a_inv: Modular multiplicative inverse of 'a'
    """

    for a_inv in range(26):
        if a * a_inv % 26 == 1:
            return a_inv
    return -1


def affine_decrypt(message: str, a: int, b: int) -> str:
    """
    Perform affine decryption to each letter of the message string
    D(y) = a_inv * (y - b) % m
    a_inv is found using the helper function _mod_mul_inv(a)
    y = E(x) = 0 index value of letter x after encryption
    m = 26

    :param message: Message to be decrypted
    :param a: parameter 'a' in affine operation equation
    :param b: parameter 'b' in affine operation equation

    :return out_message: Decrypted message using affine operation
    """

    out_message = ""
    a_inv = _mod_mul_inv(a)
    m = 26

    for letter in message:
        y = ord(letter) - ord('A')
        D_y = (a_inv * (y - b) % m)
        out_letter = chr(D_y + ord('A'))
        out_message += out_letter

    return out_message


def _sanitize_array(ops_arr: list) -> list:
    """
    Sanitize the operations array in the following manner: 
    A. Normalize forms
    1. If Shift command is of the form ["S", ["i"]] then convert to 
        ["S", ["i,j"]] where j = 1
    2. If Duplicate command is of the form ["D", ["i"]] then convert to 
        ["D, ["i,j"]] where j = 1
    3. If Rotate command is of the form ["R", [""]] then convert to
        ["R", ["i"]] where i = 1

    B. Parse and convert parameters to correct data type for encryption engine
    1. If Rotate command then convert ["R", ["i"]] -> ["R", [i]]
    2. If Shift, Duplicate, Trade or Affine command then convert 
        ["X", ["i,j"]] -> ["X", [i,j]]

    :param ops_array: Operations array of the form [operation, [params]] 
        to be sanitized

    :return sanitized_ops_arr: Resulting operations array after 
        sanitization steps A and B
    """

    # Normalize form
    # [ "R", [ "" ] ] -> [ "R", [ "1" ] ]
    # [ "X", [ "i" ] ] -> [ "X", [ "i,1" ] ]
    for op in ops_arr:
        command = op[0]
        parameter_str = op[1][0]

        if command == 'S' or command == 'D':
            if not ',' in parameter_str:
                op[1][0] += ',1'

        if command == 'R' and len(parameter_str) == 0:
            op[1][0] = '1'

    # Parse and convert parameters to correct data type
    for op in ops_arr:
        command = op[0]
        parameter_str = op[1][0]

        if command == 'R':  # For Rotate
            op[1] = [int(op[1][0])]

        else:  # For Shift, Duplicate, Trade, Affine
            params = op[1][0].split(',')
            op[1] = [int(params[0]), int(params[1])]

    sanitized_ops_arr = ops_arr

    return sanitized_ops_arr


def _parse_operations(operations: str, isDecodeMode: bool = False) -> list:
    """
    Parse the commands string to generate an operations array
    1. Separate all commands against the ";" delimiter
    2. Reverse the order of commands if mode == decode
    3. Convert the list of commands to an operations array
    4. Sanitize the operations array for the encryption/decryption engine
    5. Invert the operations parameters if mode == decode

    :param operations: String of ; delimited operations
    :param isDecodeMode: Boolean variable which indicates if the mode is set to 
        decode or encode

    :return ops_arr: Resulting operations array after parsing the 
        operations string
    """

    # Separate all operations
    operations = operations.split(';')

    # Reverse operations if mode == decode
    if isDecodeMode:
        operations.reverse()

    # Make array of operations
    ops_arr = []
    for op in operations:
        command = op[0]
        parameters = op[1:]
        ops_arr.append([command, [parameters]])

    # Sanitize operations array
    ops_arr = _sanitize_array(ops_arr)

    # Invert the operations parameters if mode == decode
    if isDecodeMode:
        for op in ops_arr:
            if op[0] == 'S':
                op[1] = [op[1][0], op[1][1] * -1]

            if op[0] == 'R':
                op[1][0] = op[1][0] * -1

    # print("\n\nOperations: {}\n\n".format(ops_arr))

    return ops_arr


def encrypt(message: str, operations: str) -> str:
    """
    Performs encryption operations on the message string

    :param message: Message to be encrypted
    :param operations: String of ; separated encryption operations

    :return encrypt_message: Encrypted message
    """

    # Convert operations string to operations array
    ops_arr = _parse_operations(operations, False)
    progress = []

    for op in ops_arr:
        command = op[0]
        params = op[1]
        if command == 'R':  # Rotate
            message = rotate(message, params[0])
            progress.append(message)

        if command == 'T':  # Trade
            message = trade_ij(message, params[0], params[1])
            progress.append(message)

        if command == 'D':  # Duplicate
            message = duplicate(message, params[0], params[1])
            progress.append(message)

        if command == 'S':  # Shift
            message = shift(message, params[0], params[1])
            progress.append(message)

        if command == 'A':  # Affine
            message = affine_encrypt(message, params[0], params[1])
            progress.append(message)

    # print("Encryption: ", progress)
    encrypt_message = message

    return encrypt_message


def decrypt(message: str, operations: str) -> str:
    """
    Performs decryption operations on the message string

    :param message: Message to be decrypted
    :param operations: String of ; separated encryption operations

    :return decrypted_message: Decrypted message
    """

    # Convert operations string to operations array
    ops_arr = _parse_operations(operations, True)
    progress = []

    for op in ops_arr:
        if op[0] == 'R':  # Rotate
            message = rotate(message, op[1][0])
            progress.append(message)

        if op[0] == 'T':  # Trade
            message = trade_ij(message, op[1][0], op[1][1])
            progress.append(message)

        if op[0] == 'D':  # Duplicate
            message = remove_duplicate(message, op[1][0], op[1][1])
            progress.append(message)

        if op[0] == 'S':  # Shift
            message = shift(message, op[1][0], op[1][1])
            progress.append(message)

        if op[0] == 'A':  # Affine
            message = affine_decrypt(message, op[1][0], op[1][1])
            progress.append(message)

    # print("Decrypt: ", progress)
    decrypted_message = message
    return decrypted_message

# Ciphers main function


def ciphers_menu() -> None:
    """
    Ciphers menu for user input

    :return: None
    """
    print("Welcome to Ciphers!")

    while True:

        # Input mode
        while True:
            prompt = "What do you want to do: (E)ncrypt, (D)ecrypt or (Q)uit? "
            mode = input(prompt).upper()

            if not mode in ['E', 'D', 'Q']:
                print("Please enter a valid mode.")
            else:
                break

        # Quit session
        if mode == 'Q':
            print("Goodbye!", end="")
            break

        # Take message input
        message = input("Enter the message: ").upper()

        # Which operation to perform
        operations = input("Enter the encrypting transformation operations: ")
        operations = operations.upper()

        # Encode or Decode
        output_message = None

        if mode == 'E':
            output_message = encrypt(message, operations)

        if mode == 'D':
            output_message = decrypt(message, operations)

        print("Generating output ...")
        print(output_message)


def main() -> None:
    """
    The main loop responsible for getting the input details from the user
        and printing in the standard output the results of encrypting or 
        decrypting the message applying the transformations

    :return: None
    """
    ciphers_menu()


if __name__ == '__main__':
    main()
