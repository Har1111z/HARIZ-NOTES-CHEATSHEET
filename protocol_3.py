import contextlib
import io
import string
import sys

MAX_INPUT = 512

_FLAG_CLASS = type("flag_goes_here", (object,), {})

BAD_WORDS = [
    "import", "os", "system", "eval", "exec", "open",
    "read", "write", "popen", "subprocess", "pty",
    "compile", "local", "vars", "dir",
    "getattr", "setattr", "delattr", "hasattr",
    "__loader__", "__spec__", "linecache", "builtins",
]
#not blocked: __self__, print, sys


def run(code):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, {"__builtins__": {"print": print}})
    except Exception:
        return "[error]\n"
    return buf.getvalue()


while True:
    sys.stdout.write(">>> ")
    sys.stdout.flush()
    data = sys.stdin.buffer.readline(MAX_INPUT)
    if not data:
        break
    code = data.decode().strip()
    code = "".join(c for c in code if c in string.printable)

    code_lower = code.lower()
    if any(bad in code_lower for bad in BAD_WORDS):
        print("[blocked]")
        break

    result = run(code)
    sys.stdout.write(result if result else "[empty]\n")
    sys.stdout.flush()