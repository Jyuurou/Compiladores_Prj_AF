dict = {"tasu": "<+>", "hiku": "<->", "kakeru": "<*>", "waru": "</>", "onaji": "<==>", "hidariga": "<>>",
        "ijou": "<>=>", "migiga": "<<>", "ika": "<<=>", "chigau": "<!=>",
        "=": "<=>", "{": "<{>", "}": "<}>", "(": "<(>", ")": "<)>",
        "moshi": "<if>", "kai": "<for>"}

lexical_error_msg = []
struct_token = ""
symbol_origin = []
memory = []
count_line = 1


def verify_if_identifier(item):
    global lexical_error_msg

    if item[0].isalpha():
        return True

    return False


def verify_if_string(item):
    global lexical_error_msg

    # Check if there are 2 double quotations, if not, return False
    if item.count('"') > 0 and not item.count('"') % 2 == 0:
        lexical_error_msg.append("Está faltando 1 aspas duplas na: " + str(item))
        return False

    # Check if there are the double quotations in each edge
    if item.count('"') >= 2:
        if item[0] == '"' and item[len(item)-1] == '"':
            return True
        else:
            lexical_error_msg.append("Aspas duplas está em posição errada na: " + str(item))
            return False

    return False


def verify_if_numeric(item):
    global lexical_error_msg
    is_numeric = False

    # Verify whether item is numeric
    if item.isnumeric():
        is_numeric = True

    # If numeric, verify whether item is int, if not then return false
    if is_numeric:
        if item.isdigit():
            return True
        else:
            lexical_error_msg.append("Só é permitido número inteiro e não: " + str(item))

    return False


def verify_lexical(listTxt):
    listTxt = listTxt.split(" ")
    global count_line
    global symbol_origin
    index = 0
    position_index = 0

    # verify if each simbol is some kind of tag reserved in dictionary
    for i in listTxt:
        symbol_origin.append(i)

        if i in dict:
            memory.append(dict[i])
        else:
            # verify if the item is string
            if verify_if_string(i):
                memory.append("<string>")
            # verify if the item is numeric
            elif verify_if_numeric(i):
                memory.append("<num>")
            # se o elemento anterior for delimitador e o próximo dele for um alphanumerico que começa com alfabeto considera como identificador
            elif (listTxt[index - 1] == "=" and verify_if_identifier(i)) or verify_if_identifier(i):
                memory.append("<identificador>")
            else:
                memory.append("<incognita>")
                lexical_error_msg.append("Erro na linha %i, posição %i. Símbolo: '%s' " % (count_line, position_index, i))
        index+=1
        position_index+=1

    count_line+=1
