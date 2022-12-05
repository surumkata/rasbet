from django.db import models

def change_url_language(html,language):
  if language != 'en':
    return f'{html}_{language}.html'
  else:
    return f'{html}.html'