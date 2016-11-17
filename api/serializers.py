
def buttons(buttons):
    return {
        "attachment_type": "default",
        "actions": [
            {
                "name": button,
                "text": button ,
                "type": "button",
                "value": button
            } for button in buttons
            ]
    }


def in_channel_response(text=None, sub_text=None, image=None, path=None):
    response = {
        'response_type': 'in_channel',
        'text': text,
        'attachments': []
    }

    attachment = {}

    if sub_text:
        attachment['text'] = sub_text

    if image:

        attachment['image_url'] = path + str(image)
        attachment['thumb_url'] = path + str(image)

        if not attachment.get('text'):
            # If there is no attachment text, image does not get shown
            attachment['text'] = ' '

    if attachment:
        response['attachments'].append(attachment)

    response['attachments'].append(buttons(['Up vote', 'Down vote']))

    return response
