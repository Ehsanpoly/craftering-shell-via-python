import sys




def main():
    while True:
         # TODO: Uncomment the code below to pass the first stage
        
        sys.stdout.write("$ ")
        command = input().strip()
        # pass
        if command == "exit":
            sys.exit(0)
        
        if command.startswith("echo"):
            parts = command.split(" ", 1)

            if len(parts) == 1:
                print("")
            else:
                print(parts[1])
            continue
        
        if command.startswith("type"):
            parts = command.split(" ", 1)

            if len(parts) == 1:
                print("")
            elif parts[1] == dir(__builtins__):
                print(f"type {command} is a shell buitlin")  
            else:
                print("invalid_command: not found")      


        print(f"{command}: command not found")

    

if __name__ == "__main__":
    main()