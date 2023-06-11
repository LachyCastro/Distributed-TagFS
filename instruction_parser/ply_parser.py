
import ply.lex as lex
import ply.yacc as yacc

# import sys
# sys.path.append('instruction_parser/')
from command import Add, AddTags, Delete, DeleteTags, Get, List

# Define the lexer tokens
tokens = (
    'FILENAME',
    'WORD',
    'ADD',
    'ADD_TAGS',
    'DELETE_TAGS',
    'DELETE',
    'LIST',
    'GET',
    'F',
    'T',
    'Q'
)

# Define the lexer rules
def t_FILENAME(t):
    r'[^\s/]+\.[a-zA-Z0-9_-]+'
    return t

def t_WORD(t):
    r'[a-zA-Z0-9_-]+'
    return t

def t_F(t):
    r'-f'
    return t

def t_T(t):
    r'-t'
    return t

def t_Q(t):
    r'-q'
    return t

t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    raise Exception(f"Invalid token '{t.value[0]}' at line {t.lineno} (Index {t.lexpos}).")

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
    'add_inst : ADD F file_list T tag_list'
    file_list = p[3]
    tag_list = p[-1]
    p[0] = Add(file_list, tag_list)

def p_query_inst(p):
    'query_inst : inst Q tag_query'
    command = p[1]
    tag_query = p[-1]
    p[0] = command(tag_query)

def p_add_tags_inst(p):
    'add_tags_inst : ADD_TAGS Q tag_query T tag_list'
    tag_query = p[3]
    tag_list = p[-1]
    p[0] = AddTags(tag_query, tag_list)

def p_delete_tags_inst(p):
    'delete_tags_inst : DELETE_TAGS Q tag_query T tag_list'
    tag_query = p[3]
    tag_list = p[-1]
    p[0] = DeleteTags(tag_query, tag_list)

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