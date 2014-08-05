

def read_code(file_name):
    f = open(file_name, 'rt')
    code = ''.join(f.readlines())
    return code

def write_to_file(file_name, code):
    f = open(file_name, 'wt')
    f.write(code)
    f.close()


