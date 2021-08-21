from rest_framework import generics
from .models import User, Team, School, Venue, City, Match
from .serializers import UserSerializer, TeamSerializer, SchoolSerializer, VenueSerializer, CitySerializer, MatchSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

# Create your views here.
class UserList(generics.ListCreateAPIView):
    """
    List all users, or create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete the data of a user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class MatchOver(generics.UpdateAPIView):
    queryset = Team.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TeamSerializer

    def Post(self, request, winner, pk):
        match = Match.objects.get(id=pk)
        team = Team.objects.get(id=winner)
        team.matches = team.matches + 1
        team.won = team.won + 1
        team.xp = team.xp + 1
        if team.xp > (10 + (5 * team.level)):
            team.level = team.level + 1
            team.xp = 0
        team.save()
        team1 = match.team1
        team2 = match.team2
        if team is team1:
            team2.matches = team2.matches + 1
            team2.save()
        else:
            team1.matches = team1.matches + 1
            team1.save()
        match.upcoming = False
        match.past = True
        match.winner = team
        match.save()
        venue = match.venue
        venue.matches = venue.matches + 1
        venue.save()
        return HttpResponse(status=204)

class Register(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def Post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            data = []
            if serializer.is_valid():
                user = serializer.save()
                """
                    Use Twilio to verify phone numbers
                """
                user.is_active = True
                user.save()
                token = Token.objects.get_or_create(user=user)[0].key
                data["message"] = "user registered successfully"
                data["phone number"] = account.number
                data["username"] = account.username
                data["token"] = token
            else:
                return HttpResponse(status=400)
            return Response(data)
        except IntegrityError as e:
            account=User.objects.get(username='')
            account.delete()
            raise ValidationError({"400": f'{str(e)}'})

        except KeyError as e:
            print(e)
            raise ValidationError({"400": f'Field {str(e)} missing'})

class Login(APIView):
    permission_classes = (AllowAny,)

    def Post(self, request):
        data = {}
        body = json.loads(request.body)
        country = body['country_code']
        phone = body['phone']
        password = body['password']
        try:
            user = User.objects.get(phone=phone)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})

        token = Token.objects.get_or_create(user=user)[0].key
        print(token)
        if not check_password(password, user.password):
            raise ValidationError({"message": "Incorrect Login credentials"})

        if user:
            if user.is_active:
                login(request, user)
                data["message"] = "Log in successfull"
                data["phone"] = user.phone

                result = {"data" : data, "token" : token}

                return Response(result)
            else:
                return HttpResponse("Account not active")
        else:
            return HttpResponse("Account Does not exist")

class Logout(APIView):
    permission_classes = (AllowAny,)

    def Get(self, request):
        request.user.auth_token.delete()

        logout(request)

        return HttpResponse(status=204)

class VenueList(generics.ListCreateAPIView):

    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = (AllowAny,)

class CityList(generics.ListCreateAPIView):

    queryset = City.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CitySerializer

class MatchList(generics.ListCreateAPIView):
    """
    Get a history of matches or upcoming matches or schedule a new one
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = (AllowAny,)
