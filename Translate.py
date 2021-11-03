from collections import deque

dict = {"tasu": "<+>", "hiku": "<->", "kakeru": "<*>", "waru": "</>", "onaji": "<==>", "hidariga": "<>>",
        "ijou": "<>=>", "migiga": "<<>", "ika": "<<=>", "chigau": "<!=>",
        "=": "<=>", "{": ":", "}": "<}>", "(": "", ")": "",
        "moshi": "<if>", "kai": "<for i in range(>"}

struct_translated = ""


# Receive whole symbols of the memory and separate in expression blocks
def separate_expr_block(memory):
    list_of_blocks = []

    queue = deque(memory)
    count_open_brace = 0

    while len(queue) > 0:
        list_temp = []

        # Take first symbol
        first_symbol = queue.popleft()
        list_temp.append(first_symbol)

        # verifica se, o primeiro simbolo é "For" ou "If", se sim, pega os símbolos até o "}".
        if first_symbol == "kai" or first_symbol == "moshi":
            while True:
                # Remove "(" and ")" from list because in Python don't exist these symbols
                if queue[0] == "(" or queue[0] == ")":
                    queue.popleft()

                list_temp.append(queue.popleft())

                # Verify the count of de open brace "{" and close brace "}" in the middle.
                if list_temp[-1] == "{":
                    count_open_brace += 1
                elif list_temp[-1] == "}":
                    count_open_brace -= 1
                    if count_open_brace == 0:
                        break

        # If not, this is EXPR expression, so add symbols into the list till the end of the EXPR expression
        else:
            while True:
                list_temp.append(queue.popleft())
                if list_temp[-2] == "=":
                    break

        list_of_blocks.append(list_temp)

    return list_of_blocks


# Function to reorder and translate Jipang expression to Python expression
def translate_expr(expr_in_list):
    global struct_translated
    length = len(expr_in_list)
    convert_times = 2

    if "\t" in expr_in_list[-1]:
        convert_times = 3

    # reorder and translated original symbol to python symbol
    for count in range(length):
        if count < convert_times:
            # reverse the sequence of list's elements
            symbol = expr_in_list[length-1-count]
        else:
            symbol = expr_in_list[count-convert_times]

        # translate to python symbol if necessary
        if symbol in dict:
            struct_translated += dict[symbol].replace("<", "", 1).replace(">", "", 1) + " "
        else:
            struct_translated += symbol + " " if not ("\t" in symbol) else symbol

    struct_translated += "\n"


# Function to reorder and translate Jipang If or Else expression to Python If or Else sexpression
def translate_if_for(expr_in_list):
    global struct_translated
    length = len(expr_in_list)
    tab = ["\t"]

    if "\t" in expr_in_list[0]:
        tab[0] = expr_in_list[0]+"\t"

    for count in range(length):

        # Process manualy translation of "for x" to "for i range x"
        if expr_in_list[count] == "kai":
            expr_in_list[count] = "for i in"
            expr_in_list[count+1] = "range(" + expr_in_list[count+1] + ")"

        # Road symbol to struct_translated. Translate symbol to python symbol if necessary
        symbol = expr_in_list[count]
        if symbol in dict:
            struct_translated += dict[symbol].replace("<", "", 1).replace(">", "", 1) + " "
        else:
            struct_translated += symbol + " " if not ("\t" in symbol) else symbol

        if expr_in_list[count] == "{":
            struct_translated += "\n"
            block_intern = expr_in_list[count+1:-1]
            block_intern.append(tab[0])
            translate_process(block_intern)
            break


# The primary function to start the Translation Process of the Jipang Code to Python Code
def translate_process(memory):

    global struct_translated

    # Check is this code block has tab, if yes, then put tab in evidence
    tab = []
    if any("\t" in string for string in memory):
        tab.append(memory.pop(-1))

    # Call separate expr method
    blocks_list = separate_expr_block(memory)

    for block in blocks_list:

        if block[0] == "kai" or block[0] == "moshi":
            if len(tab) > 0:
                block = tab + block
            translate_if_for(block)
        else:
            if len(tab) > 0:
                block.append(tab[0])
            translate_expr(block)




