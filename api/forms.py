from django import forms


class SlackPOSTForm(forms.Form):

    token_id = forms.CharField(max_length=255, required=False)
    team_id = forms.CharField(max_length=255)
    team_domain = forms.CharField(max_length=255)
    channel_id = forms.CharField(max_length=255)
    channel_name = forms.CharField(max_length=255)
    user_id = forms.CharField(max_length=255)
    command = forms.CharField(max_length=255)
    text = forms.CharField(max_length=255)
    response_url = forms.CharField(max_length=255)
    english = forms.BooleanField(required=False, initial=False)

    def clean_english(self):
        return '--english' in self.cleaned_data.get('text', '').split(' ')
