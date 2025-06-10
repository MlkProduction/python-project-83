import validators

def validate(data):
    errors = ''
    url = data.get('url', '').strip()

    if not validators.url(url):
        errors = 'Некорректный URL'

    if len(url) > 255:
        errors = 'URL слишком длинный (максимум 255 символов)'

    return errors