import io
import string
import sys
import contextlib

MAX_INPUT  = 512
MAX_OUTPUT = 65536

BLACKLIST = [
    "import", "os", "sys", "exec",
    "open", "read", "write",
    "getattr", "setattr", "delattr", "hasattr",
    "globals", "locals", "vars", "dir",
    "compile", "breakpoint", "subprocess", "popen",
]


def scrub(code: str) -> str:
    """Strip blacklisted words repeatedly until nothing changes."""
    while True:
        cleaned = code
        for bad in BLACKLIST:
            cleaned = cleaned.replace(bad, "")
        if cleaned == code:
            return code
        code = cleaned


def run(code):
    buf = io.StringIO()
    safe_builtins = {
        "open": open,
        "eval": eval,
        "print": print,
    }

    try:
        with contextlib.redirect_stdout(buf):
            result = eval(code, {"__builtins__": safe_builtins})
    except Exception as e:
        return f"[error]\n{e}"

    output = buf.getvalue()

    if len(output) > MAX_OUTPUT:
        output = output[:MAX_OUTPUT] + "\n[truncated]\n"

    return output if output else "[empty]\n"


while True:
    sys.stdout.write(">>> ")
    sys.stdout.flush()
    data = sys.stdin.buffer.readline(MAX_INPUT)
    if not data:
        break
    code = data.decode().strip()
    code = "".join(c for c in code if c in string.printable)
    code = scrub(code)
    result = run(code)
    sys.stdout.write(result)
    sys.stdout.flush()