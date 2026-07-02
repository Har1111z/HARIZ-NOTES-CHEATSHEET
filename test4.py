import sys

def main():
    print("=== Welcome to the HARIZJAIL 2.0 ===")
    print("=== Level: Easy ===")
    print("Extract the contents of 'flag.txt'.")
    
    # A simple keyword blocklist
    blacklist = ["import", "os", "sys", "open", "read", "flag","eval","exec","attr","input","＿",'.__', 'print']
    print("blocked: ", blacklist)
    
    sandbox_globals = {}
    while True:
        user_input = input(">>> ")
        
        # Check the blocklist
        for word in blacklist:
            if word in user_input:
                print(f"BANNED WORD DETECTED: {word}")
                return
                
        # Executed in a standard environment, but we hide output by wrapping it
        # We also pass a custom dict so you can store variables across lines if needed
        try:
            exec(user_input, sandbox_globals)
            print("Command executed successfully (Output hidden).")
        except Exception as e:
            print(f"Execution Error: {e}")

if __name__ == "__main__":
    main()