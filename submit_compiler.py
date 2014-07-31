
import sys

from p2l_compiler import P2LCompiler, read_code, write_to_file

def main():
    if len(sys.argv) > 1:
        code = read_code(sys.argv[1])
    else:
        code = read_code('p2l/1.lisp.py')
    # parseprint(code)
    # dump syntax tree to file
    # write_to_file('p2l_workdir/syntax_tree.py', dump(parse(code)))
    # write_to_file('p2l_workdir/input.py', code)

    p2l = P2LCompiler()
    p2l.use_submit_mode=True
    p2l.use_standard_library=True

    byte_code = p2l.compile_expr(code)
    # print
    # byte_code.show_without_source()

    # print 'Source:'
    # print byte_code.to_source()
    write_to_file('p2l_workdir/submit_code.gcc', byte_code.to_source())

    print
    print 'OK'

if __name__ == '__main__':
    main()
