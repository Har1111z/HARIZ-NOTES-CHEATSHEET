import contextlib
import io
import sys

FLAG = "flag{placeholder}"

MAX_LEN = 15
ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyz ")


def run(code):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, {})
    except Exception:
        return None
    return buf.getvalue() or None


while True:
    sys.stdout.write(">>> ")
    sys.stdout.flush()
    data = sys.stdin.buffer.readline(256)
    if not data:
        break

    code = data.decode().strip()

    if len(code) > MAX_LEN:
        print("[too long]")
        continue
    if not set(code) <= ALLOWED_CHARS:
        print("[blocked]")
        continue

    result = run(code)

    if result is None:
        print("[error]")
    elif len(result) > 700:
        print(FLAG)
        break
    else:
        print("[too short]")