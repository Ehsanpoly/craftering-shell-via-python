import sys
import shutil
import subprocess
import os

def builtin_exit(args):
    sys.exit(0)

def builtin_cd(args):
    if not args:
        print("")
        return
    
    # if not args:
    #     path = os.path.expanduser("~")

    else:
        path = args[0]
        path = os.path.expanduser(path)    

    # route = args[0]
    try:
        os.chdir(path) 

    except FileNotFoundError:
        print(f"cd: {args[0]}: No such file or directory")

    except NotADirectoryError:
        print(f"cd: {args[0]}: No a directory")

    except PermissionError:
        print(f"cd: {args[0]}: Permission denied")    

def builtin_pwd(args):
    if not args:
        # print(os.getcwd())
        return os.getcwd() + "\n"    

def builtin_echo(args):
    # print(" ".join(args))
    return " ".join(args) + "\n"

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
        print(f"{target} is {path} ")
        return

    print(f"{target}: not found") 


def parse_redirection(parts):
    if ">" not in parts:
        return parts, None
    
    idx = parts.index(">")
    if idx == len(parts) - 1:
        return parts, None
    
    filename = parts[idx + 1]
    cmd_parts = parts[:idx]
    return cmd_parts, filename


BUILTINs = {
    "exit": builtin_exit,
    "echo": builtin_echo,
    "type": builtin_type,
    "pwd": builtin_pwd,
    "cd": builtin_cd,
}

def main():
    while True:
        sys.stdout.write("$ ")
        command = input().strip()
 
        if not command:
            continue

        parts = command.split()

        parts , out_file = parse_redirection(parts)
        if not parts:
            continue
        
        cmd = parts[0]
        args = parts[1:]

        if cmd in BUILTINs:
            if cmd in ("cd", "exit"):
                BUILTINs[cmd](args)
                continue

            output = BUILTINs[cmd](args) or ""

            if out_file:
                with open(out_file, "w") as f:
                    f.write(output)

            else:
                print(output, end="")
            continue                

        path = shutil.which(cmd)
        
        if path:
            # print(f"Running external:{path}")
            result = subprocess.run([cmd] + args, executable = path, 
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, 
                                    text=True)
            output = result.stdout

            if out-file:
                with open(out_file, "w") as f:
                    f.write(output)
            else:
                print(output, end="")
            continue            

        print(f"{command}: command not found")

    
if __name__ == "__main__":
    main()