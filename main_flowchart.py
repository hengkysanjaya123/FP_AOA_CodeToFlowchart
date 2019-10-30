import sys
from graphviz import Digraph
from plyparser import create_new_parser, testToken
from plyparser import error_logger
import os
# from plyparser import lexer

def draw_flowchart(source_code):
    s1 = """
    1 int b = 10;
    2 int c = 15;

    3 while(b == 5){
        3.1while(a < 10000){
            3.1.1if(a == 0){
                3.1.1.1if(b == c){
                    3.1.1.1.1cout << "test";
                3.1.1.1}
            3.1.1}    
        3.1}

        3.2cout << "coba";
    3}

    """

    s2 = """
    cout << "aaaa";
    int b = 10;
    int c = 15;

    while(b == 5){
        while(a < 10000){
            cout << "halo";
            if(a == 0){
                if(b == c){
                    cout << "test";
                    cout << "coba";
                }
            }
        }
        cout << "aaaa";
    }
    int d = 20;
    cout << "robert";
    """

    s3 = """
    if(a == b){
        cout << "test";
    }
    """
    s4 = """

    int a = 10;
    while(a < 100){
        cout << "test";

        if(a == 5){
           cout << "coba";
        }

        cout << "abc";
    }
    cout << "robert";
    """

    s5 = """

    int a = 10;
    int b = 5;
    if(a > b){
        cout << "test";
    }

    if(b == 5){
        cout << "semoga berhasil";
    }
    cout << "coba";
    """

    # s2 = """
    # int a = 10;
    # if(a > 0){
    #     cout << "test";
    # }
    # """
    # s2 = """
    #
    # """
    #
    # for i in range(20):
    #     s2 += 'string p'+ str(i)+' = "fsnjks'+str(i)+'";'
    #

    s2 = """
    int a = 10;
    while(a < 10){
        while(a <  5){
            if(a == b){
                while(a < 4){
                     cout << "test";
                }
                cout << "aaaaa";
            }
            cout << "test2";
        }
        cout << "bde";
    }
    cout << "abc";
    """
    s6 = """
    if(a == c){
        while(a < 10){
            cout << "test";
            cout << "halo";
        }
    }
    while(b < 5){
        if(a == b){
            cout << "aaaa";
        }
    }
    int c = 10;
    """

    print("\n")
    error_logger.clear()

    lexer = testToken(source_code)
    # for i in lexer:
    #     print(i)
    print("------------------------------------end of lexer part--------------------------------------------")
    parser = create_new_parser()
    result = parser.parse(source_code)

    if(len(error_logger) != 0 ):
        print("error (main_flowchart.py)", error_logger)
        return error_logger

    # print("result ", result)

    print("\n")

    print("result ", result, "\n")
    # print(len(result[0]))
    # print(result[0][0:])

    final_res = []

    # for i in result:
    closing_code = []

    def convert(p):
        print("p",p,"\n")
        if (isinstance(p, tuple)):
            size = len(p)

            if (size == 3 or size == 4 and p[-1] != '}'):
                # tuple doang ga ada array d dlmny
                final_res.append(p[0:])
            else:
                # klo misal ada array di dalam tuple
                final_res.append(p[0:3])
                #            print("p[3]",p[3],"\n")

                #            if(p[2] == "{"):
                #                closing_code.append("}")
                for i in range(3, len(p)):
                    print("p[i]", p[i])
                    if (p[i] != '}'):
                        convert(p[i])
                    else:
                        final_res.append('}')
        #            convert(p[3])

        #            if(p[2] == '{' or p[1] == '{'):
        #                print("wwwwwwww",p[1])
        #                final_res.append('}')

        elif (isinstance(p, list)):
            for a in p:
                convert(a)
        else:
            final_res.append(p)

    convert(result)
    print("final_res", final_res)

    def set_label(data):
        res = ''
        for i in data:
            res += str(i) + "."
        return res

    line = 1  # nentuin increment n linenya
    scope = [0]  # array utk simpan posisi nested
    position = 0  # utk nentuin jangkauan di scope
    new_indexing_result = []
    for i in final_res:
        data = i
        if(isinstance(i, tuple)):
            data = list(i)

        size = len(data)
        # pos = str(line) + "." + str(scope[position])

        scope[position] += 1
        # print("position", position)
        print("scope", scope)

        # print("data", data, size)
        label = set_label(scope[0:position + 1])
        if (data[-1] == '}'):
            scope[position] = 1
            position -= 1

            label = set_label(scope[0:position + 1])
            scope[position+1] = 0

        if (data[-1] == '{' or data[0]=='else'):
            scope.append(0)
            position += 1

        if (isinstance(i, tuple)):
            data.insert(0, label)
            new_indexing_result.append(data)
        else:
            new_indexing_result.append([label,i])

    print("scope", scope)

    for i in new_indexing_result:
        print("#", i)
    new_indexing_result2 = []
    for i in new_indexing_result:
        # new_indexing_result2.append(i)
        if i[1] == '}':
            continue
        else:
            new_indexing_result2.append(i)

    # for i in new_indexing_result2:
    #     print("#", i)
    # print(new_indexing_result)
    # print("final_res indexing",new_indexing_result)

    fc = Digraph(name="flowchart", strict=True)

    num = 0

    scope2 = []
    for i in new_indexing_result:
        scope2.append(i[0])

    source = []
    target = []

    last_statement_num = 0

    end_found = False

    def get_num(indexing):
        for i in range(0, len(new_indexing_result2)):
            # print(i[0], " ::: " , indexing)
            if (new_indexing_result2[i][0] == indexing):
                return i

        return -1

    for i in new_indexing_result:
        # print(end_found)
        if i[1] in {'int', 'string', 'bool', 'char', 'float'}:
            # fc.attr('node', shape='rectangle')
            fc.node(str(num), label=i[1]+' '+i[2], shape='rectangle', style='filled', color='#a29bfe')
            if num == 0:
                fc.attr('node', rankdir='LR')
                fc.node('start', shape='oval', style='filled', color='#55efc4')
                fc.edge('start', str(num))
            if num > 0:
                # check nunjuk arrownya mesti sesama sibling
                current_array = str(new_indexing_result2[num - 1][0]).split('.')
                current = current_array[0:len(current_array) - 2]

                dest_array = str(new_indexing_result2[num][0]).split('.')
                dest = dest_array[0:len(dest_array) - 2]
                # if(num -1 == 8 or num == 8):
                print(current, " :: ", dest)
                if (current == dest):
                    fc.edge(str(num - 1), str(num))

            num += 1

            if scope2[num - 1] == scope2[-1] and end_found == False:
                # print("innnnnnnnnnnnnnnnnn")
                fc.node(str(num), label='end', shape='oval', style='filled', color='#55efc4')
                fc.edge(str(num - 1), str(num))
                end_found = True

            last_statement_num = num

        if i[1] in {'while', 'for', 'if', 'ELSE IF'}:
            fc.attr('node', shape='diamond')

            if i[1] in {'while', 'for'}:
                fc.node(str(num), label=i[2][2], shape='diamond', style='filled', color='#fdcb6e')
            else:
                # if(i[1] == 'else'):
                #     fc.node(str(num), label=str(i[3][0][2]), shape='diamond', style='filled', color='#3498db')
                # else:
                fc.node(str(num), label=i[2][2], shape='diamond', style='filled', color='#3498db')

            # fc.node(str(num), label=i[2][2])

            if num > 0:
                # if (i[1] in {'while', 'for'}):
                #     fc.node(str(num), label=i[2][2], shape='diamond', style='filled', color='yellow')
                # else:
                #     fc.node(str(num), label=i[2][2], shape='diamond', style='filled', color='#3498db')  # blue

                fc.edge(str(num - 1), str(num))
            if num == 0:
                fc.attr('node', rankdir='LR')
                fc.node('start', shape='oval', style='filled', color='#55efc4')
                fc.edge('start', str(num))
            num += 1
            # print("rio : ",i)
            # print("scope: ", scope2[num-1], " : ",scope2[num])

            a = int(i[0][-2])

            if len(i[0]) > 2:
                if i[0][-2] == str(a):

                    for s in range(0, len(new_indexing_result2)):
                        if i[0][0:-2] + str(a + 1) + '.' in scope2:
                            if i[0][0:-2] + str(a + 1) + '.' == new_indexing_result2[s][0]:
                                fc.edge(str(num - 1), str(s), label='false')
                                # print("drawwwwwwwwww")
                                break
                        elif i[0][0:-2] + str(a + 1) + '.' not in scope2:
                            for j in range(num - 2, -1, -1):
                                if new_indexing_result2[j][1] in {'while', 'for'}:
                                    str_index = i[0]
                                    while str_index != '':
                                        str_index = str_index[0:-2]
                                        if str_index == new_indexing_result2[j][0]:
                                            fc.edge(str(num - 1), str(j), label='false')
                                            break
                                    break
                                else:
                                    for k in range(num, len(new_indexing_result2)):
                                        if new_indexing_result2[k][1] in {'while', 'for'}:
                                            fc.edge(str(num - 1), str(k), label='false')
                                            break
            elif len(i[0]) == 2:
                # print("robert: ", scope2[num-1][0:-1])
                deststr = str(int(i[0][0:-1]) + 1) + '.'
                dest = str(get_num(deststr))
                if (dest != '-1'):
                    print("robert : ", i[0], "to : ", dest)
                    fc.edge(str(num - 1), dest, label='false')

                # for s in range(0, len(new_indexing_result2)):
                #     if scope2[num-1] == new_indexing_result2[s][0]:
                #         for j in range(s+1, len(new_indexing_result2)):
                #             if len(new_indexing_result2[j][0]) == 2:
                #                 fc.edge(str(num-1), str(j), label='false')
                #                 break

                # gotofalse(scope2[num-1], new_indexing_result, scope2, num, new_indexing_result2, 1)
            print("endfoundddddddddd", end_found)

            print(i[0], "==", new_indexing_result[len(new_indexing_result) - 1][0])
            # if scope2[num -1] == scope2[-1] and end_found == False:
            #     print("innnnnnnnnnnnnnnnnn")
            #     fc.node('end', shape='oval')
            #     fc.edge(str(num - 1), 'end', label='false')
            #     end_found = True

            if i[0] == new_indexing_result[len(new_indexing_result) - 1][0] and end_found == False:
                print("innnnnnnnnnnnnnnnnn")
                fc.node('end', shape='oval', style='filled', color='#55efc4')
                fc.edge(str(num - 1), 'end', label='false')
                end_found = True


            elif scope2[num - 1][-2] != '1':
                fc.edge(str(num - 1), str(num))

            fc.edge(str(num - 1), str(num), label='true')

            last_statement_num = num

        if i[1] in {'cin', 'cout'}:
            fc.attr('node', shape='parallelogram', style='filled', color='#fab1a0')
            fc.node(str(num), label='print ' + i[3])

            if num > 0:
                fc.node(str(num), label='print ' + i[3], shape='parallelogram', style='filled', color='#fab1a0')

                # check nunjuk arrownya mesti sesama sibling
                current = new_indexing_result2[num - 1][0][0:-2]
                dest = new_indexing_result2[num][0][0:-2]
                if (current == dest):
                    fc.edge(str(num - 1), str(num))
            if num == 0:
                fc.attr('node', rankdir='LR')
                fc.node('start', shape='oval', style='filled', color='#55efc4')
                fc.edge('start', str(num))

            num += 1
            # if scope2[num-1] == scope2[-1]:
            #     fc.node(str(num), label='end', shape='oval')
            #     fc.edge(str(num - 1), str(num))

            last_statement_num = num

    print(fc.source)
    k = fc.body
    print(k)
    list_arrow = []
    for i in k:
        if '->' in i:
            list_arrow.append(i)

    print(list_arrow)
    source = []
    end = []
    text = ''
    for i in list_arrow:
        data = i.split('->')
        source.append(str.rstrip(str(data[0]).replace('\t', '')))
        end.append(str.rstrip(str(data[1]).split(' ')[1]))

    print(source)
    print(end)

    # buat panah balik loop nya
    for i in new_indexing_result2:
        indexing = i[0]
        if (len(indexing) > 2):
            # print("enter")
            new_indexing = indexing[0:-2] + str(int(indexing[-2][-1]) + 1) + '.'
            pos = get_num(new_indexing)
            # print("pos", pos)
            if (pos == -1):
                print("not found")

                s = str(get_num(indexing))
                dest = str(get_num(str(new_indexing_result2[int(s)][0][0:-2])))
                print(s)
                print(dest)
                next = int(s) + 1
                # nyari sampai ketemu while pertama yg paling dekat sama dia
                str_indexing = str(indexing)

                current_array = str_indexing.split('.')

                try:
                    # check next siblings of previous scope / parent exist or not
                    next_str_indexing = current_array[0:len(current_array) - 2]
                    next_str_indexing = str.join('.', next_str_indexing[0:-1]) + '.' + str(
                        int(next_str_indexing[-1]) + 1) + '.'
                    print("current str_indexing", str_indexing)
                    print("next_str_indexing", next_str_indexing)
                    print("get_num", get_num(next_str_indexing))

                    found = False
                    if (get_num(next_str_indexing) == -1):
                        while (str_indexing != ''):
                            str_indexing = str_indexing[0:-2]
                            # print("below")
                            # print(new_indexing_result2[get_num(str_indexing)][1])
                            if new_indexing_result2[get_num(str_indexing)][1] in {'while', 'for'}:
                                fc.edge(s, str(get_num(str_indexing)))
                                # print("IT IS HERE" + s + str(get_num(str_indexing)))
                                found = True
                                break
                except:
                    print("enter catch")

                if (found == False):

                    if (str(next) in end):
                        print("hello")
                        fc.edge(s, str(next))
                        found = True
                        #break

                    # print("next : ", next)
                    elif (str(next) not in end and end_found == False):
                        print("enter next")
                        fc.edge(s, 'end')
                    else:
                        if (str(next) in end):
                            print("hellooooooo")
                            fc.edge(s, str(next))
                        else:
                            if new_indexing_result2[int(s)][1] in {'if', 'while', 'for', 'ELSE IF', 'else'}:
                                fc.edge(s, 'end', label='false')
                            else:
                                fc.edge(s, 'end')

                if (new_indexing_result2[int(dest)][1] in {'while', 'for'}):
                    fc.edge(s, dest)

    # for s in end:
    #     if s not in source and s != 'end':
    #         print("masuk")
    #         print(s)
    #         # print(new_indexing_result2[int(s)][0][0:-3])
    #         dest = str(get_num(str(new_indexing_result2[int(s)][0][0:-2])))
    #         fc.edge(s,dest)

    k = fc.body
    print(k)
    list_arrow = []
    for i in k:
        if '->' in i:
            list_arrow.append(i)

    print(list_arrow)
    source = []
    end = []
    text = ''
    for i in list_arrow:
        data = i.split('->')
        source.append(str.rstrip(str(data[0]).replace('\t', '')))
        end.append(str.rstrip(str(data[1]).split(' ')[1]))

    if 'end' not in end and end_found == False:
        fc.node('1000', label='end', shape='oval', style='filled', color='#55efc4')
        print("last statement minus 1", last_statement_num - 1)
        fc.edge(str(last_statement_num - 1), '1000')
        end_found = True

    # fc.node("yellow", shape='rectangle', style='filled', color='yellow')

    # fc.clear()
    #
    # for i in range(1,50):
    #     fc.node(str(i), label=str(i), shape='oval')
    #     fc.edge(str(i), str(i+1))

    fc.view()


s = """
int a = 10;
int b = 5;
"""

s2 = """
while(a > b){
   cout << "Test";
}
"""

# draw_flowchart(s)
# draw_flowchart(s2)