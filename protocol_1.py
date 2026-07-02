import contextlib
import io
import string
import sys

MAX_INPUT = 512
BLACKLIST = ["import", "os", "sys", "eval", "exec", "open", "read",
             "write", "getattr", "setattr", "delattr", "builtins",
             "locals", "vars", "dir", "compile", "globals"]

WRONG_PATH = ["__class__", "__base__", "__subclasses__", "__mro__",
               "__builtins__", "__dict__", "__module__",
              "__init__", "__func__", ".__", '__globals__']
def run(code):
    buf = io.StringIO()

    try:
        with contextlib.redirect_stdout(buf):
            exec(code)
    except Exception as e:
        return f"[error]\n {e}"

    output = buf.getvalue()

    if any(leak in output for leak in ["<_io.", "TextIOWrapper", "BufferedReader"]):
        return "[error]\n"

    return output


while True:
    sys.stdout.write(">>> ")
    sys.stdout.flush()
    data = sys.stdin.buffer.readline(MAX_INPUT)
    if not data:
        break
    code = data.decode().strip()
    code = "".join(c for c in code if c in string.printable)

    if any(trap in code for trap in WRONG_PATH):
        print("[blocked]")
        break

    for bad in BLACKLIST:
        code = code.replace(bad, "")

    result = run(code)
    sys.stdout.write(result if result else "[empty]\n")
    sys.stdout.flush()
#a=string.ascii_letters;b=string.punctuation;c=string.digits;print(a[15]+a[17]+a[8]+a[13]+a[19]+b[7]+c[2]+b[8])
#.encode(), .decode()
#(_ for _ in ()).gi_frame.f_globals[]
#(_ for _ in ()).gi_frame.f_builtins
#(_ for _ in ()).gi_frame.f_buibuiltinsltins