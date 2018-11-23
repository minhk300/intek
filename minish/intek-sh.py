#!/usr/bin/env python3

"""
=============================================================================

                                    MINISH

                        basic command-line interpreter

1 - REPL - a read-eval-print loop - Link with PATH:
    |   -> prompt "intek-sh$ " -> parse input_ with format <command> + < *args>
        -> parse $PATH string to have directories -> call subprocess
        -> wait for it to finish -> display the prompt again
        -> error message if the command notfound or no permission to execute.

2 - Built-in Functions:
    cd [directory]
    |-> cd .. | cd /home | cd .. OR ../.. | cd dir1/dir2..

    printenv [variable]
    export [variables...]
    unset [variable]
    exit [exit_code]

=============================================================================
"""
import os
import subprocess


def cd(args):
    if len(args) > 0:
        args = args[0]
    if args == [] or args == '~' or args == '/home':
        try:
            home = os.environ['HOME']
            os.chdir(home)
        except KeyError:
            print('intek-sh: cd: HOME not set')
    else:
        try:
            os.chdir(args)
        except FileNotFoundError:
            print('intek-sh: cd: %s: No such file or directory' % (args))


def printenv(args):
    print('args:', args)
    if args == []:
        for i in os.environ:
            print(i + '=' + os.environ[i])
    else:
        for i in args:
            try:
                print(os.environ[i])
            except KeyError:
                return


def export(args):
    args = args[0].split('=')
    os.environ[args[0]] = args[1]


def unset(args):
    for i in args:
        try:
            del os.environ[i]
        except KeyError:
            print('intek-sh: unset: `%s\': not a valid identifier' % (i))


def exit(args):
    print('exit')
    if args and len(args[0]) > 1:
        print('intek-sh: exit:')
    flag = 0
    os._exit(0)


def check_path(command):
    paths = os.environ['PATH'].split(':')
    for i in paths:
        path = i + '/' + command
        if os.path.exists(path):
            return True
    else:
        print('intek-sh: %s: command not found' % (command))
        return False


def execute(command, args):
    if check_path(command):
        args.insert(0, command)
        try:
            subprocess.run(args)
        except Exception as e:
            return
    else:
        return


def args_parse(input_):
    input_ = input_.split(' ')
    input_ = [x for x in input_ if x]
    command = input_[0]
    input_.pop(0)
    args = [x for x in input_ if x]
    return command, args


def main():
    built_ins = ('cd', 'printenv', 'export', 'unset', 'exit')
    input_ = input('intek-sh$ ')
    flag = 1
    while flag == 1:
        try:
            while input_ == '':
                input_ = input('intek-sh$ ')
        except EOFError:
            return
        input_ = input_.split('\\n')
        for i in input_:
            command, args = args_parse(i)
            if command in built_ins:
                exec('%s(args)' % (command))
            else:
                execute(command, args)
        input_ = ''


if __name__ == '__main__':
    main()
