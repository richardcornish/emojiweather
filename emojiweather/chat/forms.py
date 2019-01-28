from django import forms


class ChatForm(forms.Form):
    channel_id = forms.CharField(required=False)
    channel_name = forms.CharField(required=False)
    command = forms.CharField(required=False)
    response_url = forms.CharField(required=False)
    team_domain = forms.CharField(required=False)
    team_id = forms.CharField(required=False)
    text = forms.CharField(required=False)
    token = forms.CharField(required=False)
    user_id = forms.CharField(required=False)
    user_name = forms.CharField(required=False)
