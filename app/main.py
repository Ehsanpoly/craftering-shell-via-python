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
    clean = []
    out_file = None

    i = 0
    while i < len(parts):
        tok = parts[i]

        if tok in (">", "1>"):
            if i + 1 < len(parts):
                out_file = parts[i + 1]
                i += 2
                continue
            else:
                break  # invalid syntax → ignore

        clean.append(tok)
        i += 1

    return clean, out_file


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
        parts, out_file = parse_redirection(parts)

        if not parts:
            continue

        cmd = parts[0]
        args = parts[1:]

        # Builtins
        if cmd in BUILTINs:
            if out_file:
                with open(out_file, "w") as f:
                    save = sys.stdout
                    sys.stdout = f
                    BUILTINs[cmd](args)
                    sys.stdout = save
            else:
                BUILTINs[cmd](args)
            continue

        # External commands
        path = shutil.which(cmd)
        if path:
            if out_file:
                with open(out_file, "w") as f:
                    subprocess.run([path] + args, stdout=f)
            else:
                subprocess.run([path] + args)
            continue

        # Unknown
        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
