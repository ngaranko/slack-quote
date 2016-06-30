def in_channel_response(text=None, sub_text=None):
    response = {
        'response_type':'in_channel',
        'text': text
    }

    if sub_text:
        response['attachments'] = [{
            'text': sub_text
        }]

    return response
