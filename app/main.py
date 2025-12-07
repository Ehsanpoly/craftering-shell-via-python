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
    
    route = args[0]
    
    if not route.startswith("/"):
        print(f"cd: {route}: is not found")
        return
    try:
        os.chdir(route) 

    except FileNotFoundError:
        print(f"cd: {route}: No such file or directory")

    except NotADirectoryError:
        print(f"cd: {route}: No a directory")

    except PermissionError:
        print(f"cd: {route}: Permission denied")    

def builtin_pwd(args):
    if not args:
        print(os.getcwd())
        return    

def builtin_echo(args):
    print(" ".join(args))

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

BUILTINs = {
    "exit": builtin_exit,
    "echo": builtin_echo,
    "type": builtin_type,
    "pwd": builtin_pwd,
    "cd": builtin_cd,
}

def main():
    while True:
         # TODO: Uncomment the code below to pass the first stage
        
        sys.stdout.write("$ ")
        command = input().strip()
 
        if not command:
            continue

        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd in BUILTINs:
            BUILTINs[cmd](args)
            continue

        path = shutil.which(cmd)
        
        if path:
            # print(f"Running external:{path}")
            subprocess.run([cmd] + args, executable = path)
            continue

        print(f"{command}: command not found")

    
if __name__ == "__main__":
    main()