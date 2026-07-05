import contextlib
import io
import string
import sys

FLAG = "MRSM26{placeholder}"


def _make_error_class(flag):
    class _MariError(Exception):
        """."""
        def __str__(self):
            return flag          # captured in closure — survives del
        __repr__ = object.__repr__
    return _MariError


_MariError = _make_error_class(FLAG)
del _make_error_class

MAX_INPUT  = 512
MAX_OUTPUT = 65536

BAD_WORDS = [
    "import", "os", "system", "eval", "exec", "open",
    "read", "write", "popen", "subprocess", "pty",
    "compile", "globals", "locals", "vars",
    "getattr", "setattr", "delattr", "hasattr",
    "__loader__", "__spec__", "linecache", "builtins",
    "flag", "FLAG",
]

MSG_BADWORD = "[blocked: unauthorized input detected]\n"
MSG_ERROR   = "[error]\n"
MSG_EMPTY   = "[no output]\n"


def run(code):
    buf = io.StringIO()
    safe_builtins = {
        "print":      print,
        "str":        str,
        "repr":       repr,
        "type":       type,
        "isinstance": isinstance,
        "dir":        dir,
        "len":        len,
        "Exception":  Exception,
    }
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, {
                "__builtins__": safe_builtins,
                "_MariError":   _MariError,
            })
    except Exception:
        return MSG_ERROR

    output = buf.getvalue()
    if len(output) > MAX_OUTPUT:
        output = output[:MAX_OUTPUT] + "\n  [transmission truncated]\n"
    return output


def main():
    print("Mariposa Protocol 7")
    print("_MariError is in scope.")
    print()

    while True:
        sys.stdout.write(">>> ")
        sys.stdout.flush()
        data = sys.stdin.buffer.readline(MAX_INPUT)
        if not data:
            break
        code = data.decode().strip()
        code = "".join(c for c in code if c in string.printable)

        code_lower = code.lower()
        for bad in BAD_WORDS:
            if bad.lower() in code_lower:
                sys.stdout.write(MSG_BADWORD)
                sys.stdout.flush()
                return

        result = run(code)
        sys.stdout.write(result if result else MSG_EMPTY)
        sys.stdout.flush()


if __name__ == "__main__":
    main()