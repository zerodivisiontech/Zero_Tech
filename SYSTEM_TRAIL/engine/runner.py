import io
from contextlib import redirect_stdout


def run_player_code(code: str) -> tuple[bool, str]:
    """
    Runs player code and captures printed output.
    Returns (success, output_or_error_message).
    """
    buffer = io.StringIO()

    try:
        with redirect_stdout(buffer):
            exec(code, {})
        output = buffer.getvalue().rstrip()
        return True, output
    except Exception as e:
        return False, f"Error: {e}"