import validators
def validate(urls):
    errors = {}
    urls = urls.get('url', '')

    if not validators.url(urls):
        errors = "Некорректный URL"

    if len(urls) > 255:
        errors = "Некорректный URL"
        

    return errors

