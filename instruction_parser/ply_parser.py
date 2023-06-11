
import ply.lex as lex
import ply.yacc as yacc

# import sys
# sys.path.append('instruction_parser/')
from command import Add, AddTags, Delete, DeleteTags, Get, List

# Define the lexer tokens
tokens = (
    'FILENAME',
    'WORD',
)

# Define the lexer rules
def t_FILENAME(t):
    r'[^\s/]+'
    return t

def t_WORD(t):
    r'[a-zA-Z0-9_-]+'
    return t

# Define the parser rules
def p_input(p):
    'input : instruction'
    p[0] = p[1]

def p_instruction(p):
    '''instruction : add_inst
                   | query_inst
                   | add_tags_inst
                   | delete_tags_inst'''
    p[0] = p[1]

def p_add_inst(p):
    'add_inst : ADD file_list tag_list'
    file_list = p[2]
    tag_list = p[3]
    p[0] = Add.execute(file_list, tag_list)

def p_query_inst(p):
    'query_inst : inst tag_query'
    command = p[1]
    tag_query = p[2]
    p[0] = command.execute(tag_query)

def p_add_tags_inst(p):
    'add_tags_inst : ADD_TAGS tag_query tag_list'
    tag_query = p[2]
    tag_list = p[3]
    p[0] = AddTags.execute(tag_query, tag_list)

def p_delete_tags_inst(p):
    'delete_tags_inst : DELETE_TAGS tag_query tag_list'
    tag_query = p[2]
    tag_list = p[3]
    p[0] = DeleteTags.execute(tag_query, tag_list)

def p_inst(p):
    '''inst : DELETE
            | LIST
            | GET'''
    if p[1] == 'DELETE':
        p[0] = Delete
    elif p[1] == 'LIST':
        p[0] = List
    elif p[1] == 'GET':
        p[0] = Get

def p_file_list(p):
    '''file_list : FILENAME
                 | FILENAME file_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_tag_list(p):
    '''tag_list : WORD
                | WORD tag_list'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_tag_query(p):
    '''tag_query : WORD
                 | WORD tag_query'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

# Build the lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

# Example usage
input_str = 'add -f file1.txt -t tag1 tag2'
result = parser.parse(input_str)