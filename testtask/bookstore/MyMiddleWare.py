from bookstore.models import Requests
from django.utils.deprecation import MiddlewareMixin
import requests
from django.contrib.auth.models import User
import json


class SaveRequestMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            user = User.objects.get(username=request.user)
        except:
            user = None
        uri = request.build_absolute_uri()
        post = None
        if request.POST and uri != 'http://127.0.0.1:8000/accounts/login/':
            post = self.dumps(request.POST)
        Requests(
            path=request.path,
            method=request.method,
            user=user,
            post= post,
        ).save()

    def dumps(self,value):
        return json.dumps(value, default=lambda o: None)