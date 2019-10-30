# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 16:05:38 2019

@author: Hengky Sanjaya
"""

import ply.yacc as yacc
import timeit
from plytoken import *

# ----------------------------------------------------------------------------------------------
# parser yacc part

print_status_p = False


def p_statement(p):
    '''
    statement : s1 s2
            | empty
    '''

    try:
        if (p[2] == None):
            p[0] = [p[1]]
        else:
            p[0] = [p[1], p[2]]

        if (print_status_p):
            print("P_STATEMENT : ", p[0])
    except IndexError:
        pass


def p_s1(p):
    '''
    s1 : var_declaration_statement
          | if_expression
          | io_statement
          | loop_expression
          | STRING SEMICOLON
          | empty
    '''
    p[0] = p[1]

    if (print_status_p):
        print("p_s1 : ", p[0])


def p_s2(p):
    '''
    s2 : statement
    '''
    p[0] = p[1]

    if (print_status_p):
        print("p_s2 : ", p[0])


def p_io_statement(p):
    '''
    io_statement : CIN RIGHTSHIFT STRING SEMICOLON
                 | COUT LEFTSHIFT STRING SEMICOLON
    '''

    p[0] = (p[1], p[2], p[3], p[4])

    if (print_status_p):
        print("IO STATEMENT : ", p[0])


def p_var_declaration_statement(p):
    '''
    var_declaration_statement : IDENTIFIER STRING SEMICOLON
    '''

    p[0] = (p[1], p[2], p[3])

    if (print_status_p):
        print("VAR DECLARATION : ", p[0])


def p_loop_expression(p):
    '''
    loop_expression : WHILE condition LCURLY statement RCURLY
                    | FOR forcondition LCURLY statement RCURLY
    '''

    p[0] = (p[1], p[2], p[3], p[4], p[5])

    if (print_status_p):
        print("Loop Expression", p[0])


# def p_STRING(p):
#     '''
#     string : expression SEMICOLON
#            | condition
#            | empty
#     '''
#     print(p[1])
#     print(run(p[1]))

def p_condition(p):
    '''
    condition : LPAR expression RPAR
    '''
    p[0] = ("CONDITION", p[1], p[2], p[3])

    if (print_status_p):
        print("CONDITION ", p[0])


def p_forcondition(p):
    '''
    forcondition : LPAR expression SEMICOLON expression SEMICOLON expression RPAR
                | LPAR IDENTIFIER expression SEMICOLON expression SEMICOLON expression RPAR
    '''
    if(p[2]) == 'IDENTIFIER':
        print("masuk")
        p[0] = ("FOR CONDITION", p[1], (p[2] + ' ' + p[3] + p[4] + ' ' + p[5] + p[6] + ' ' + p[7]), p[8])
    else:
        print("enter not identifier")
        p[0] = ("FOR CONDITION", p[1], (p[2]  + ' '+ p[3]+' '+ p[4] + p[5]+' ' + p[6] +' '+ p[7]))


def p_if_expression(p):
    '''
    if_expression : IF condition LCURLY statement RCURLY else_expression
                | IF condition LCURLY statement RCURLY elseif_expression
    '''
    if str.lower(p[1]) == 'if':
        if (p[6] == None):
            p[0] = (p[1], p[2], p[3], p[4], p[5])
        else:
            p[0] = (p[1], p[2], p[3], p[4], p[5], [p[6]])
    #        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])
    else:
        p[0] = p[1]

    if (print_status_p):
        print("IF EXPRESSION ", p[0])


def p_elseif_expression(p):
    '''
    elseif_expression : ELSE IF condition LCURLY statement RCURLY elseif_expression
                        | ELSE IF condition LCURLY statement RCURLY else_expression
                      | empty
    '''

    try:
        if str.lower(p[1]) == 'else' and str.lower(p[2]) == 'if':
            if (p[7] == None):
                p[0] = ("ELSE IF", p[3], p[4], p[5], p[6])
            else:
                p[0] = ("ELSE IF", p[3], p[4], p[5], p[6], [p[7]])
        #            p[0] = ("ELSE IF", p[3], p[4], p[5], p[6], p[7])
        else:
            p[0] = p[1]

        #        if(print_status_p):
        print("ELSE IF EXPRESSION", p[0], "\n")

    except:
        pass


def p_else_expression(p):
    '''
    else_expression : ELSE LCURLY statement RCURLY
                    | empty
    '''

    try:
        if str.lower(p[1]) == 'else':
            p[0] = (p[1], p[2], p[3], p[4])
        else:
            p[0] = p[1]

        #        if(print_status_p):
        print("ELSE EXPRESSION", p[0])
    except:
        pass


def p_expression_string_id(p):
    '''
    expression : STRING
               | ID
               | empty

    '''
    p[0] = p[1]

    if (print_status_p):
        print("EXPRESSION STRING ID", p[0])


# Passes Empty
def p_empty(p):
    'empty : '
    pass


#
# def p_empty(p):
#    '''
#    empty :
#    '''
#    pass
##    p[0] = None


error_logger = []
def p_error(p):
    global error_logger

    print("Syntax error at line ", str(p))
    error_logger.append("Syntax error at line "+ str(p))

    return error_logger

    # return p
#    # Read ahead looking for a terminating ";"
#
#
#    # Return SEMI to the parser as the next lookahead token
#    return tok


# import logging
# log = logging.getLogger('ply')

def testToken(code):
    lexer = build_lexer()
    lexer.input(code)
    while True:
        tok = lexer.token()
        if not tok:
            break

        print("token : ",tok)

    return lexer
# parser = yacc.yacc(errorlog=yacc.NullLogger())

def create_new_parser():
    error_logger.clear()
    parser = yacc.yacc(errorlog=yacc.NullLogger())

    return parser

# print("error test : ", parser.errorok)
# parser = yacc.yacc(errorlog=log)
# print("log : ", yacc.NullLogger.me)

# print("error_logger (plyparser.py)")


s1 = """
while(b == 5){
    while(a < 10000){
        if(a == 0){
            if(b == c){
                cout << "test";
            }
        }    
    }
}


"""

s2 = """
int b = 10;
int c = 15;

while(b == 5){
    while(a < 10000){
        if(a == 0){
            if(b == c){
                cout << "test";
            }
        }    
    }
}

"""

s3 = """
int b = 10;
int c = 15;
int d = 20;
"""

s4 = """
int k = 2;
int c = 5;
while(a < b){
        return True;
}

"""



# testToken()

# s = """
# abc;
# bca;
# """
# result = parser.parse(s2)
# print("\n")


# print(res[1][1][0])
# for i in res[1][1]:
#    print(i,"\n")

# print("result : ",res)