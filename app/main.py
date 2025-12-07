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
<<<<<<< HEAD
    while True:
        sys.stdout.write("$ ")
<<<<<<< HEAD
<<<<<<< HEAD
        command = input().strip()
 
        if not command:
            continue
=======
        command = input()
<<<<<<< HEAD
<<<<<<< HEAD
        if command == "exit":
            break
        print(f"{command}: command not found")
    sys.exit()
>>>>>>> origin/autofix-d4d6c55a-3fe1-4982-a92f-b7910dbb042a
=======
        
        if command == "exit":
            sys.exit(0)
        
        print(f"{command}: command not found")
>>>>>>> origin/autofix-1033e50b-13e7-4f34-8923-0ebd39a87659
=======
        
        if command == "exit":
            exit()
        else:
            print(f"{command}: command not found")
>>>>>>> origin/autofix-1c812e58-5f6d-4e24-96c4-42bf8f24c4bc

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

    
=======
        command = input()
        if command == "exit":
            sys.exit(0)
        print(f"{command}: command not found")
=======
    sys.stdout.write("$ ")
    command = input()
    print(f"{command}: command not found")
>>>>>>> origin/autofix-beea1e22-aa50-49fc-bab5-65a9d078c494


>>>>>>> origin/autofix-34b55e0e-d9c5-4d57-8cfb-b150ff721a02
if __name__ == "__main__":
    main()