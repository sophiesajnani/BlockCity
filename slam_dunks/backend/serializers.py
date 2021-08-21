from rest_framework import serializers
from .models import User, Team, Venue, Match, City, School
import random

class UserSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        exclude = ['date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active', 'is_superuser']
        read_only_fields = ['id', 'phone', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    #def update(self, instance, validated_data):
    #    return instance

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

    def create(self, validated_data):
        city = City(
            name=validated_data['city']
        )
        city.save()
        return city

class VenueSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(queryset=City.objects.all(), slug_field='city')
    class Meta:
        model = Venue
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    """
    city = serializers.SlugRelatedField(queryset=City.objects.all(), slug_field='city')
    team1 = serializers.SlugRelatedField(queryset=Team.objects.all(), slug_field='team1')
    team2 = serializers.SlugRelatedField(queryset=Team.objects.all(), slug_field='team2')
    venue = serializers.SlugRelatedField(queryset=Venue.objects.all(), slug_field='venue')
    winner = serializers.SlugRelatedField(queryset=Team.objects.all(), slug_field='winner')
    """

    class Meta:
        model = Match
        fields = '__all__'

    def create(self, validated_data):
        c=validated_data['city']
        match = Match(
            city=City.objects.get(name=c),
            team1=Team.objects.get(name=validated_data['team1']),
            team2=Team.objects.get(name=validated_data['team2']),
            upcoming=validated_data['upcoming'],
            past=validated_data['past'],
            refree=validated_data['refree'],
            date=validated_data['date'],
            tie=validated_data['tie'],
            winner=Team.objects.get(name=validated_data['winner']),
        )
        venues = Venue.objects.filter(city=c)
        venue = random.choice(venues)
        match.venue = venue
        match.save()
        return match

class SchoolSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(queryset=City.objects.all(), slug_field='city')

    class Meta:
        model = School
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    school = serializers.SlugRelatedField(queryset=School.objects.all(), slug_field='school')
    captain = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='captain')

    class Meta:
        model = Team
        exclude = ['xp']

    """
    def update(self, instance, validated_data)
    Updating team info in views using generics
    """
