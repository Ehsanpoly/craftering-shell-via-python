import sys




def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        
        if command == "exit":
            exit()
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()