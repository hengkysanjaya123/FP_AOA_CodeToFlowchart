# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 16:02:05 2019

@author: Hengky Sanjaya
"""

import ply.lex as lex
reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'cin': 'CIN',
    'cout': 'COUT',
    'else if': 'ELSEIF',
    'operator': 'OPERATOR'
    ,'identifier': 'IDENTIFIER'
}

tokens = [
    # 'INT',
    # 'FLOAT',
    # 'NAME',
    # 'PLUS',
    # 'MINUS',
    # 'DIVIDE',
    # 'MULTIPLY',
    'EQUALS',
    'ID',
    'STRING',
    'LCURLY',
    'RCURLY',
    'LPAR',
    'RPAR',
    # 'AND',
    # 'OR',
    'SEMICOLON',
    'LEFTSHIFT',
    'RIGHTSHIFT'
  # 'EQEQ'
] + list(reserved.values())

# t_PLUS = r'\+'
# t_MINUS = r'\-'
# t_MULTIPLY = r'\*'
# t_DIVIDE = r'\/'
t_EQUALS = r'\='
# t_EQEQ = r'\=='
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_LPAR = r'\('
t_RPAR = r'\)'
# t_AND = r'\&&'
# t_OR = r'(\|\|)'
t_SEMICOLON = r';'
t_ignore = '\t '
# t_LEFTSHIFT = '<<'
# t_RIGHTSHIFT = '>>'
#t_NEWLINE = r'\n+'

# t_SPACE = r' '

def t_IDENTIFIER(t):
    r'int|string|char|bool|float'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    
    print(t.value,"t_IDENTIFIER reached")
    return t


def t_OPERATOR(t):
    r'&&|(\|\|)'
    t.type = reserved.get(t.value, 'OPERATOR')

#    print("reserved : ", reserved.get(t.value, 'OPERATOR'))

    return t

def t_ID(t):
    r'(if|else|then|while|cin|cout)'
    
    print(t.value, "t_ID reached")
    if t.value in reserved:
        t.type = reserved.get(t.value, 'STRING')
#        print("reserved : ", reserved.get(t.value, 'STRING'))
        return t
    else:
        return t

def t_LEFTSHIFT(t):
    r'<<'
    t.type = reserved.get(t.value, 'LEFTSHIFT')
    return t

def t_RIGHTSHIFT(t):
    r'>>'
    t.type = reserved.get(t.value, 'RIGHTSHIFT')
    return t

def t_STRING(t):
    r'[a-zA-Z_0-9"<> ][a-zA-Z_=*+-/_0-9"<> ]*'
    
    if t.value in reserved:
        t.type = reserved.get(t.value, 'STRING')

    return t

# def t_FLOAT(t):
#     r'\d+\.\d+'
#     t.value = float(t.value)
#     return t
#
# def t_INT(t):
#     r'\d+'
#     t.value = int(t.value)
#     return t

# def t_NAME(t):
#     r'[a-zA-Z_][a-zA-z_0-9]*'
#     t.type = 'NAME'
#     return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    print('t.lexer.lineno : ',t.lexer.lineno)
    # t.lexer.lineno += 1
    # len(t.value)


def t_error(t):
    print("Illegal characters!", t)
    t.lexer.skip(1)

def t_COMMENT(t):
    r'\//.*'
    pass
    # No return value. Token discarded

# Build the lexer
def build_lexer():
    lexer = lex.lex()
    return lexer
