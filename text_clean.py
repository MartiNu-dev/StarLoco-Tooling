import re


def _fix_mojibake_once(text: str) -> str:
    try:
        return text.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def clean_text(value) -> str:
    if value is None:
        return ""

    text = str(value)

    # Fix common UTF-8 -> latin-1/cp1252 mojibake patterns.
    if any(token in text for token in ("Ã", "â", "œ", "�", "├", "┬")):
        previous = None
        current = text
        for _ in range(3):
            if current == previous:
                break
            previous = current
            current = _fix_mojibake_once(current)
        text = current

    return text


def clean_multiline(value) -> str:
    text = clean_text(value)
    return re.sub(r"\r\n?", "\n", text)
