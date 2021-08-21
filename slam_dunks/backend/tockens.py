from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class GetToken(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(GetToken, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
