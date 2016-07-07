from django.conf import settings


def in_channel_response(text=None, sub_text=None, image=None, path=None):
    response = {
        'response_type':'in_channel',
        'text': text
    }

    attachment = {}

    if sub_text:
        attachment['text'] = sub_text

    if image:
        attachment['image_url'] = settings.STATIC_URL + str(image)
        attachment['thumb_url'] = settings.STATIC_URL + str(image)

    if attachment:
        response['attachments'] = [attachment]

    return response
