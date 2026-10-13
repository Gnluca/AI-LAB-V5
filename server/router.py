def select_model(prompt):

    text = prompt.lower()

    coding_words = [
        "python",
        "fastapi",
        "sqlite",
        "javascript",
        "html",
        "bug",
        "errore",
        "codice"
    ]

    for word in coding_words:

        if word in text:
            return "qwen-coder"

    fast_words = [
        "breve",
        "veloce",
        "rapido"
    ]

    for word in fast_words:

        if word in text:
            return "nimble"

    return "llama3.1"