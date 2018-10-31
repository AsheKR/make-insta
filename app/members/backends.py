import imghdr
import json

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class FacebookBackend:
    def authenticate(self, request, facebook_request_token):
        api_base_url = 'https://graph.facebook.com/v3.2'

        api_get_access_token_url = f'{api_base_url}/oauth/access_token'
        api_get_user_url = f'{api_base_url}/me'

        client_id = settings.FACEBOOK_APP_ID
        redirect_uri = 'http://localhost:8000/members/facebook_login'
        client_secret = settings.FACEBOOK_APP_SECRET
        code = facebook_request_token

        get_access_token_params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'client_secret': client_secret,
            'code': code,
        }

        access_token_response = requests.get(api_get_access_token_url, get_access_token_params)
        access_token_json = json.loads(access_token_response.content)
        access_token = access_token_json['access_token']

        get_user_params = {
            'access_token': access_token,
            'fields': ','.join([
                'id',
                'first_name',
                'last_name',
                'picture.type(large)',
            ]),
        }

        response = requests.get(api_get_user_url, get_user_params)
        data = response.json()

        facebook_id = data['id']
        first_name = data['first_name']
        last_name = data['last_name']
        url_img_profile = data['picture']['data']['url']

        img_reponse = requests.get(url_img_profile)
        img_extentions = imghdr.what('', h=img_reponse.content)
        in_memory_img = SimpleUploadedFile(f'{facebook_id}.{img_extentions}', img_reponse.content)

        try:
            user = User.objects.get(username=facebook_id)
            user.last_name = last_name
            user.first_name = first_name
            user.save()
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=facebook_id,
                first_name=first_name,
                last_name=last_name,
                img_profile=in_memory_img
            )
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None