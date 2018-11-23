#!/usr/bin/env python3

"""
=============================================================================

                                    MINISH

                        basic command-line interpreter

1 - REPL - a read-eval-print loop - Link with PATH:
    |   -> prompt "intek-sh$ " -> parse input with format <command> + < *args>
        -> parse $PATH string to have directories -> call subprocess
        -> wait for it to finish -> display the prompt again
        -> error message if the command notfound or no permission to execute it.

2 - Built-in Functions:
    cd [directory]
    |-> cd .. | cd /home | cd .. OR ../.. | cd dir1/dir2..

    printenv [variable]
    export [variables...]
    unset [variable]
    exit [exit_code]

=============================================================================
"""
import os, sys, subprocess

def parse():
    parser = argparse.ArgumentParser(prog='basic command-line interpreter',\
    usage=usage)
    parser.add_argument('command')
    parser.add_argument('args', nargs='*')
    return parser.parse_args()


# def get_path_value():
#     # with open('path', 'w') as f:
#         # path_value = os.system('echo $PATH')
#         # f.write(str(path_value))
#     os.system('echo $PATH > path')
#     with open('path', 'r') as f:
#         paths = f.read()
#         paths = paths.split(':')
#     paths_dict = dict()
#     # for path in paths:
#     #     m = os.listdir(path)
#     #     print(m)

def cd(args):
    # if len(args) == 0:
    #     try:
    #         home = os.environ['HOME']
    #         os.chdir(home)
    #     except KeyError:
    #         print('bash: cd: HOME not set')
    #         return
    # else:
    #     print('Args:', args)
    #     args = args[0]
    #     if args == '' or '~' or '/home':
    #         try:
    #             home = os.environ['HOME']
    #             os.chdir(home)
    #         except KeyError:
    #             print('bash: cd: HOME not set')
    #     else:
    #         try:
    #             os.chdir(args)
    #         except FileNotFoundError as error:
    #             print('bash: cd: %s: No such file or directory' % (args))

    if len(args) > 0:
        args = args[0]
    if args == [] or args == '~' or args == '/home':
        try:
            home = os.environ['HOME']
            os.chdir(home)
        except KeyError:
            print('bash: cd: HOME not set')
    else:
        try:
            os.chdir(args)
        except FileNotFoundError as error:
            print('bash: cd: %s: No such file or directory' % (args))


def printenv(args):
    for i in args:
        try:
            print(os.environ[i])
        except KeyError:
            return

def export(args):
    args=args[0].split('=')
    os.environ[args[0]] = args[1]

def unset(args):
    for i in args:
        try:
            del os.environ[i]
        except KeyError as e:
            print('bash: unset: `%s\': not a valid identifier' % (i))

def execute(command, args):
    try:
        subprocess.run(command)
    except Exception as e:
        print('Dinh chuong:', e)

def input_parse():
    input_ = input('intek-sh$ ')
    input_ = input_.split(' ')
    input_ = [x for x in input_ if x]
    command = input_[0]
    input_.pop(0)
    args = [x for x in input_ if x]
    return command, args

def main():
    built_ins = ('cd', 'printenv', 'export', 'unset')
    while True:
        command, args = input_parse()
        if command in built_ins:
            exec('%s(args)' % (command))
        elif 'exit' in command:
            return
        else:
            execute(command, args)


if __name__ == '__main__':
    main()
