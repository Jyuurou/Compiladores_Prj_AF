import LexicalChecker as lc
import SintaxChecker as sc
import Translate as tl

fh = open("codigo.txt", "r")

# Step1: Lexical Check
for linhas in fh.readlines():
    lc.verify_lexical(linhas.replace("\n", "").replace("\t", "").strip())

if len(lc.lexical_error_msg) != 0:
    print("\nTem Erro Léxico: \n", lc.lexical_error_msg)
else:
    print("\nNão tem Erro Léxico!")

    # Step2: Sintax and Semantic Check
    sc.verify_grammar(lc.memory, lc.symbol_origin)

    if len(sc.grammar_error_msg) != 0:
        print("Erro de sintaxe: ", sc.grammar_error_msg)
    elif len(sc.semantic_error_msg) != 0:
        print("Erro de semantica: ", sc.semantic_error_msg)
    else:
        print("Não tem Erro Sintático e Semântico!\n")

        # Step3: Translate Jipang Code to Python Code
        tl.translate_process(lc.symbol_origin)
        print("Estrutura traduzida: \n")
        print(tl.struct_translated)