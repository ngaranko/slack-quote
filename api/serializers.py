from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage


def in_channel_response(text=None, sub_text=None, image=None, path=None):
    response = {
        'response_type':'in_channel',
        'text': text
    }

    attachment = {}

    if sub_text:
        attachment['text'] = sub_text

    if image:
        attachment['image_url'] = path + str(image)
        attachment['thumb_url'] = path + str(image)

    if attachment:
        response['attachments'] = [attachment]

    return response
