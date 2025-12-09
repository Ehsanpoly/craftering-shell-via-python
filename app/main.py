import sys
import shutil
import subprocess
import os
import shlex


# ------------------------------
# Builtins
# ------------------------------

def builtin_exit(args):
    sys.exit(0)


def builtin_cd(args):
    if not args:
        path = os.path.expanduser("~")
    else:
        path = os.path.expanduser(args[0])

    try:
        os.chdir(path)
    except FileNotFoundError:
        print(f"cd: {args[0]}: No such file or directory")
    except NotADirectoryError:
        print(f"cd: {args[0]}: Not a directory")
    except PermissionError:
        print(f"cd: {args[0]}: Permission denied")


def builtin_pwd(args):
    print(os.getcwd())


def builtin_echo(args):
    print(" ".join(args))
    # return " ".join(args) + "\n"


def builtin_type(args):
    if not args:
        print("")
        return

    target = args[0]

    if target in BUILTINs:
        print(f"{target} is a shell builtin")
        return

    path = shutil.which(target)
    if path:
        print(f"{target} is {path}")
        return

    print(f"{target}: not found")


BUILTINs = {
    "exit": builtin_exit,
    "echo": builtin_echo,
    "type": builtin_type,
    "pwd": builtin_pwd,
    "cd": builtin_cd,
}


# ------------------------------
# Redirection parser
# ------------------------------

def parse_redirection(parts):
    """
    Detects:
       cmd arg1 arg2 > file
       cmd arg1 1> file
    Returns: (clean_parts, output_file)
    """
    stdout_file = None
    stderr_file = None
    clean_parts = []
    out_file = None

    i = 0
    while i < len(parts):
        tok = parts[i]

        if tok in [">", "1>"]:
            if i + 1 < len(parts):
                stdout_file = parts[i + 1]
                i += 2
                continue
            if tok == "2>":
                stderr_file = parts[i + 1]
            
            else:
                break  # invalid syntax → ignore

        clean_parts.append(tok)
        i += 1

    return clean_parts, stdout_file, stderr_file


# ------------------------------
# Main shell loop
# ------------------------------

def main():
    while True:
        sys.stdout.write("$ ")
        command = input().strip()

        if not command:
            continue

        # parts = command.split()
        parts = shlex.split(command)
        parts, stdout_file, stderr_file = parse_redirection(parts)

        if not parts:
            continue

        cmd = parts[0]
        args = parts[1:]

        # Builtins
        if cmd in BUILTINs:
            
            save_stdout = sys.stdout
            save_stderr = sys.stderr
            
            try:

                if stdout_file:
                    sys.stdout = open(stdout_file, "w")

                if stderr_file:
                        sys.stderr = open(stderr_file , "w")
                                
                BUILTINs[cmd](args)

            finally:
                sys.stdout = save_stdout
                sys.stderr = save_stderr
            continue    
        

        # External commands
        path = shutil.which(cmd)
        if path:
            stdout_target = open(stdout_file, "w") if stdout_file else None
            stderr_target = open(stderr_file, "w") if stderr_file else None

            subprocess.run([path] + args,
                            stdout=stdout_target, 
                            stderr=stderr_target)

        # Unknown
        print(f"{command}: command not found", file=sys.stderr)


if __name__ == "__main__":
    main()
