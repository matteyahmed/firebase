from django.contrib.auth import authenticate

from rest_framework import serializers

from core.models import Person

from rest_framework import serializers


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('username', 'password')
        extra_kwargs = {'password':{'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return Person.objects.create(**validated_data)
    

class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        attrs['user'] = user
        return