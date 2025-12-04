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
            parts = command.split("", 1)

            if len(parts) == 1:
                print("")
            else:
                print(parts[1])
            continue



        print(f"{command}: command not found")

    

if __name__ == "__main__":
    main()