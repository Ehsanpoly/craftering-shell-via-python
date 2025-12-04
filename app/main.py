import sys
import shutil


BUILTINs = {
    "exit": buitlin_exit,
    "echo": builtin_echo,
    "type": builtin_type,
}


def builtin_exit(args):
    sys.exit(0)

def builtin_echo(args):
    print(" ".join)

def builtin_type(args):
    if not args:
        print("")
        return        

    target = args[0]

    if target in BUILTINs:
        print(f"{target} is in builtin\n")
        return
    
    path = shutil.which(target)
    if path:
        print(f"{target} is {path} ")
        return

    print(f"{target}: not found")    


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
            print(f"Running external:{path}")
            continue

        print(f"{command}: command not found")

    

if __name__ == "__main__":
    main()