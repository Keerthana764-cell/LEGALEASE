import html


def sanitize_text(text: str) -> str:

    replacements = {

        "\u2018": "'",

        "\u2019": "'",

        "\u201c": '"',

        "\u201d": '"',

        "\u2013": "-",

        "\u2014": "-",

        "\u00a0": " ",

        "\u2022": "-",

        "\u200b": ""
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    # Remove control characters
    # except normal whitespace.

    text = "".join(

        char

        for char in text

        if char in "\n\r\t"
        or ord(char) >= 32
    )

    return text.strip()


def text_to_html(text: str) -> str:

    escaped = html.escape(
        sanitize_text(text)
    )

    return escaped.replace(
        "\n",
        "<br>"
    )