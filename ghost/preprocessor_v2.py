#!/usr/bin/env python

import sys

labels = {}
functions_code = {}
functions_num = {}
functions_call = {}
variables = {}

ret_points = 0
funcs = 0
var_cnt = 0


def load_uncommented_code(filename):
    code = []
    inp = open(filename, 'rt') 
    for line in inp:
        semicolon = line.find(';')
        if semicolon != -1:
            line = line[:semicolon]
        line = ' '.join(line.split())
        if len(line) == 0:
            continue
        code.append(line)
    return code


def index_symbols(code):
    global ret_points
    global funcs

    new_code = []
    line_index = -1
    while line_index + 1 < len(code):
        line_index += 1
        line = code[line_index]
        if line[-1] == ':':  # function or label
            if line.startswith('function'):  # function
                name = line.split()[1].replace(':', '')
                line_index += 1
                start = line_index
                ret = False
                while line_index < len(code):
                    line = code[line_index]
                    if line.startswith('return'):
                        if line != 'return':
                            ret = True
                            code[line_index] = line.replace('return', 'mov A,')
                        break
                    line_index += 1
                if line_index == len(code):
                    raise Exception('Function ' + name + ' has no return command')
                if name in functions_code:
                    raise Exception('Function ' + name + ' redefined')
                functions_code[name] = code[start : line_index + 1 - int(not ret)]
                functions_call[name] = []
                functions_num[name] = funcs
                funcs += 1
            else:  # label
                new_code.append(line)
        elif line.startswith('call'):  # function invocation
            name = line.split()[1]
            ret_point_label = 'auto_ret_point_' + str(ret_points)
            ret_points += 1
            new_code.append('mov [%s_###], %s' % (name, ret_point_label))
            new_code.append('jeq ' + name + ', 0, 0')
            new_code.append(ret_point_label + ':')
            functions_call[name].append(ret_point_label)
        else:  # regular line
            new_code.append(line)

    return new_code


def insert_functions(code):
    for name in functions_code:
        func_code = index_symbols(functions_code[name])
        functions_code[name] = func_code
        if name in labels:
            raise Exception('Function name conflicts with label ' + name)

    for name in functions_code:
        labels[name + '_###'] = str(functions_num[name] + 200)
        if len(functions_call[name]) == 0:
            continue
        print 'Add function:', name
        code.append(name + ':')
        code.extend(functions_code[name])
        for call in functions_call[name]:
            code.append('jeq %s, [%s_###], %s' %(call, name, call))
    return code


def unlabel(code):
    global var_cnt

    new_code = []
    index = 0
    comment = ''
    for line in code:
        if line[-1] == ':':  # label
            name = line.split()[0].replace(':', '')
            labels[name] = index
            comment += ' ;' + name
        else:
            new_code.append(line + comment)
            comment = ''
            index += 1

    code = new_code
    new_code = []
    for line in code:
        new_line = line.replace(',', ' ')
        items = new_line.split()
        for item in set(items):
            if item.startswith('<') and item.endswith('>'):
                if item not in variables:
                    variables[item] = var_cnt
                    var_cnt += 1
                line = line.replace(item, '[%d]' % (variables[item] + 100))
                continue
            if item.startswith('[') and item.endswith(']'):
                item = item[1:-1]
            if item not in labels:
                continue
            line = line.replace(item, str(labels[item]))
            line = line + '; <- ' + item
        new_code.append(line)
    return new_code


def add_main_call(code):
    code.append('call main')
    code.append('int 0')
    code.append('hlt')


def save_code(code, filename):
    out = open(filename, 'wt')
    for line in code:
        print >> out, line


if __name__ == '__main__':
    code = load_uncommented_code(sys.argv[1])
    add_main_call(code)
    code = index_symbols(code)
    code = insert_functions(code)
    code = unlabel(code)
    save_code(code, sys.argv[2])

