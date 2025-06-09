import validators

def validate(data):
    errors = {}
    url = data.get('url', '').strip()

    if not validators.url(url):
        errors['url'] = 'Некорректный URL'

    if len(url) > 255:
        errors['url'] = 'URL слишком длинный (максимум 255 символов)'

    return errors