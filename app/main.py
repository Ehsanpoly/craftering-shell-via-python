import sys




def main():
    while True:
         # TODO: Uncomment the code below to pass the first stage
        
        sys.stdout.write("$ ")
        command = input()
        # pass
        if command == "exit":
            sys.exit(0)
        if command == "echo":
            print(input())

            
        print(f"{command}: command not found")

    

if __name__ == "__main__":
    main()