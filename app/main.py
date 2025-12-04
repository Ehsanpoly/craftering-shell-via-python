import sys




def main():
    while True:
         # TODO: Uncomment the code below to pass the first stage
        
        sys.stdout.write("$ ")
        command = input()
        print(f"{command}: command not found")
        # pass
        sys.exit(1)

if __name__ == "__main__":
    main()
