import contextlib
import io
import string
import sys

MAX_INPUT  = 512
MAX_OUTPUT = 65536

BAD_WORDS = [
    "import", "os", "system", "eval", "exec", "open",
    "read", "write", "popen", "subprocess", "pty",
    "compile", "globals", "locals", "vars",
    "getattr", "setattr", "delattr", "hasattr",
    "__loader__", "__spec__", "linecache", "builtins",
]


class _MariVault:
    """The flag is stored as an attribute on this class (server-side)."""
    pass


def run(code):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, {
                "__builtins__": {"print": print, "dir": dir},
                "_MariVault": _MariVault,
            })
    except Exception:
        return "[error]\n"

    output = buf.getvalue()
    if len(output) > MAX_OUTPUT:
        output = output[:MAX_OUTPUT] + "\n[truncated]\n"
    return output


while True:
    sys.stdout.write(">>> ")
    sys.stdout.flush()
    data = sys.stdin.buffer.readline(MAX_INPUT)
    if not data:
        break
    code = data.decode().strip()
    code = "".join(c for c in code if c in string.printable)

    if any(bad in code.lower() for bad in BAD_WORDS):
        print("[blocked]")
        break

    result = run(code)
    sys.stdout.write(result if result else "[empty]\n")
    sys.stdout.flush()