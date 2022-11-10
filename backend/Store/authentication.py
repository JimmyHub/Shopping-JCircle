import jwt
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from user.models import UserProfile


class TokenExAuthentication(TokenAuthentication):
    model = UserProfile

    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return None
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):

        try:
            token_de = jwt.decode(token, key=123456, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(_('Token Expired.'))
        except Exception:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        model = self.get_model()
        try:
            user = model.objects.get(username=token_de['username'])
            # token = model.objects.select_related('user').get(token=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        return (user, token)
