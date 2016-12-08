
def buttons(buttons):
    return {
        "attachment_type": "default",
        "actions": [
            {
                "name": button,
                "text": button,
                "type": "button",
                "value": button
            } for button in buttons
        ]
    }


def in_channel_response(quote, path=None):
    response = {
        'response_type': 'in_channel',
        'text': str(quote),
        'attachments': []
    }

    attachment = {}

    if quote.context:
        attachment['text'] = quote.context

    if quote.image:

        attachment['image_url'] = path + str(quote.image)
        attachment['thumb_url'] = path + str(quote.image)

        if not attachment.get('text'):
            # If there is no attachment text, image does not get shown
            attachment['text'] = ' '

    if attachment:
        response['attachments'].append(attachment)
        
    if text_english:
        attachment['text'] = quote.text_english
    
    if context_english:
        attachment['text'] = quote.context_english

    if quote.tile.exists():
        response['attachments'].append({
            'text': ' ',
            'image_url': path + str(quote.tile.get().image),
            'thumb_url': path + str(quote.tile.get().image)
        })

    # Does not work, temporary disabled due wrong implementation for Slack. Message after clicking button:
    # Darn - that didn't work. Only Slack Apps can add interactive elements to messages.
    # Manage your apps here: https://api.slack.com/apps/
    # response['attachments'].append(buttons(['Up vote', 'Down vote']))

    return response
