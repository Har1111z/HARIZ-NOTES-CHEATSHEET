import os
import sys

flag=open('flag.txt', 'r').read()
Banned=['Banned','import','breakpoint','os','pdb','sys', '__builtins__', 'global', 'globals', 'flag', 'try', 'eval','exec','open','write','read','txt','.__','print','raise']

print("=== Welcome to the HARIZJAIL 1.0 ===")
print("=== Level: EASIER ===")
while True:
    sys.stdout.write(">>")
    o=sys.stdin.readline()
    if any(wrong in o for wrong in Banned):
        print("banned")
        continue
    if any(i in o for i in ['exit']):
        print("EXITED")
        break
    if o=='':
        continue
    try:
        exec(o)
        print("code runned successfully")
    except Exception as E:
        print(E)
        print('error\n')