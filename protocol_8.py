import contextlib
import io
import string
import sys

FLAG = "MRSM26{placeholder}"


def _make_generator(secret_bytes):
    """Generator that holds the secret in a local variable forever."""
    _secret = secret_bytes   # lives in gi_frame.f_locals
    while True:
        yield ""             # yields nothing useful


_mari_gen = _make_generator(FLAG.encode())
del _make_generator

MAX_INPUT  = 512
MAX_OUTPUT = 65536

BAD_WORDS = [
    "import", "os", "system", "eval", "exec", "open",
    "read", "write", "popen", "subprocess", "pty",
    "compile", "globals", "locals", "vars",
    "setattr", "delattr", "hasattr",
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
        "bytes":      bytes,
        "bytearray":  bytearray,
        "list":       list,
        "dict":       dict,
        "next":       next,
        "iter":       iter,
        "type":       type,
        "dir":        dir,
        "len":        len,
        "enumerate":  enumerate,
        "zip":        zip,
        "map":        map,
        "filter":     filter,
        "range":      range,
        "chr":        chr,
        "ord":        ord,
        "hex":        hex,
    }
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, {
                "__builtins__": safe_builtins,
                "_mari_gen":    _mari_gen,
            })
    except Exception as e:
        return MSG_ERROR

    output = buf.getvalue()
    if len(output) > MAX_OUTPUT:
        output = output[:MAX_OUTPUT] + "\n  [transmission truncated]\n"
    return output


def main():
    print("Mariposa Protocol 8")
    print("_mari_gen is in scope.")
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