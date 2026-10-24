def validate_prompt(text):

    if not text:
        raise ValueError(
            "Prompt vuoto"
        )

    if len(text) > 5000:
        raise ValueError(
            "Prompt troppo lungo"
        )

    return text