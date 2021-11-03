import SemanticChecker as sc
import time

# Receive parameters (Elem_memory, Elem_Stack)
dict = {"<num>,S": "EXPR", "<identificador>,S": "EXPR", "<string>,S": "EXPR", "<if>,S": "EXPR", "<for>,S": "EXPR", "$,S": "EXPR",
        "<num>,EXPR": "EXPR' EXPR", "<identificador>,EXPR": "EXPR' EXPR", "<string>,EXPR": "EXPR' EXPR", "<if>,EXPR": "EXPR_IF EXPR", "<for>,EXPR": "EXPR_FOR EXPR",  "<}>,EXPR": "E",  "$,EXPR": "E",
        "<num>,EXPR'": "EXPR_CALC", "<identificador>,EXPR'": "EXPR_CALC", "<string>,EXPR'": "EXPR_CONCAT",
        "<num>,EXPR_CALC": "VAL_CAL EXPR_CALC'", "<identificador>,EXPR_CALC": "VAL_CAL EXPR_CALC'",
        "<+>,EXPR_CALC'": "OPERAD VAL_CAL EXPR_CALC'", "<->,EXPR_CALC'": "OPERAD VAL_CAL EXPR_CALC'", "<*>,EXPR_CALC'": "OPERAD VAL_CAL EXPR_CALC'", "</>,EXPR_CALC'": "OPERAD VAL_CAL EXPR_CALC'", "<=>,EXPR_CALC'": "<=> <identificador>",
        "<string>,EXPR_CONCAT": "VAL_CONCAT EXPR_CONCAT'",
        "<+>,EXPR_CONCAT'": "<+> VAL_CONCAT EXPR_CONCAT'", "<=>,EXPR_CONCAT'": "<=> <identificador>",
        "<+>,OPERAD": "<+>", "<->,OPERAD": "<->", "<*>,OPERAD": "<*>", "</>,OPERAD": "</>",
        "<if>,EXPR_IF": "<if> <(> EXPR_BOOL <)> <{> EXPR <}>",
        "<num>,EXPR_BOOL": "VAL_CAL OP_BOOL VAL_CAL", "<identificador>,EXPR_BOOL": "VAL_CAL OP_BOOL VAL_CAL",
        "<==>,OP_BOOL": "<==>", "<>=>,OP_BOOL": "<>=>", "<>>,OP_BOOL": "<>>", "<<>,OP_BOOL": "<<>", "<<=>,OP_BOOL": "<<=>", "<!=>,OP_BOOL": "<!=>",
        "<for>,EXPR_FOR": "<for> VAL_CAL <{> EXPR <}>",
        "<num>,VAL_CAL": "<num>", "<identificador>,VAL_CAL": "<identificador>",
        "<string>,VAL_CONCAT": "<string>"}

# Receive parameters (Elem_memory, Elem_Stack)
dictErro = {"<num>,<identificador>": "Em vez de ser identificador está como um número!"
            }

grammar_error_msg = []
stack = ["$", "S"]
semantic_error_msg = []


def verify_grammar(memory, symbol_origin):

    memory.append("$")

    while len(stack) != 0 and len(grammar_error_msg) == 0 and len(semantic_error_msg) == 0:

        # Verify if first element of memory is <identificador>. If so, check whether <id> already was allocated
        if memory[0] == "<identificador>":
            if not sc.is_id_allocated(symbol_origin[0]):
                semantic_error_msg.append("Erro de semantica! Não há declaração de identificador: %s" % (symbol_origin[0]))

        # verify if first element of stack is blank (E). If blank, remove these simbols blank from Stack
        if stack[-1] == "E":
            stack.pop()

        # Verify if first element of stack and memory is same. If same, remove these symbols from Stack and memory
        elif stack[-1] == memory[0]:
            stack.pop()
            memory = memory[1:]
            symbol_origin = symbol_origin[1:]

        else:
            first_stack = stack.pop()
            try:
                derivation = dict[memory[0] + "," + first_stack]
                list_derivation = derivation.split(" ")
                for i in range(len(list_derivation)):
                    stack.append(list_derivation.pop())

                #if derivation is <=> <identification> then attribution occurred so reserve info in list
                if derivation == "<=> <identificador>":
                    sc.allocate_id_declared(symbol_origin[1])
            except:
                try:
                    grammar_error_msg.append("Erro de sintaxe! " + dictErro[memory[0] + "," + first_stack])
                except:
                    grammar_error_msg.append("Erro de sintaxe! Na há regra de derivação para o Symbolo Não Terminal %s e o Symbolo Terminal %s. " % (first_stack, memory[0]))

