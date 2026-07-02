import os
import sys
import random
print("=== Welcome to the HARIZJAIL EVOLVED===")
print("=== Level: MID ===")
BANNED=['flag','open','txt','breakpoint','pdb','import','BANNED','globals','locals','exec','eval','os','read','write','builtins', 'random','char']
BACKGROUNDBLOCK=['.__','{','[','getattr','setattr','delattr','class']
print('+OMEWELCOMEWELCOMEWELCOMEWELC+')
print(f'Banned :{BANNED}')
MAXBANNED=random.randint(1,5)
while MAXBANNED > 0:
    sys.stderr.write('>>>>>>>>>>>>')
    sys.stdout.write("-->>")
    o=sys.stdin.readline()
    if any(wrong in o for wrong in BANNED):
        print("banned")
        MAXBANNED-=1
        continue
    if any(wrong in o for wrong in BACKGROUNDBLOCK):
        print("code runned successfully")
        continue
    if any(i in o for i in ['exit']):
        print("EXITED")
        break
    try:
        exec(o)
        print("code runned successfully")
    except Exception as E:
        print(E,'[error]')
print("YOU'VE REACHED THE MAX BANNED LIMIT")