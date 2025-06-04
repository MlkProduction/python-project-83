import validators

import validators
def validate(urls):
    errors = {}
    urls = urls.get('url', '')

    if not validators.url(urls):
        errors = "Попробуйте начать с 'https://' и закончить на '.com/'"

    if len(urls) > 255:
        errors = "Чувак(иха), это слишком длинно, напиши сайт нормально, вот так: начни с 'https://' 'тут тельце' и закончи на '.com/', например https://google.com/"
        

    return errors

