def validate(urls):
    errors = {}
    url = urls.get('url', '')

    if not (url.startswith("https://") and url.endswith(".com/")):
        errors = "Попробуйте начать с 'https://' и закончить на '.com/'"

    if len(url) > 255:
        errors = "Чувак(иха), это слишком длинно"

    return errors

