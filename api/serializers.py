from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
         model = User
         fields = ('first_name','last_name','email','password')
         extra_kawargs = {
              'first_name':{ 'required':True,"allow_blank":False},
              'last_name':{ 'required':True,"allow_blank":False},
              'email':{ 'required':True,"allow_blank":False},
              'password':{ 'required':True,"allow_blank":False,'min_lenght':4}
         }

class UserSerializer(serializers.ModelSerializer):
    # Inclure les champs de profil associés
    image = serializers.ImageField(source='profile.image', required=False)
    post = serializers.CharField(source='profile.post', required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'image', 'post') 


class DemChqDtlSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemChqDtl
        fields = '__all__'        



class VirestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Virest
        fields = '__all__'  # All fields from the Virest model will be serialized

class CptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cpt
        fields = '__all__'  # All fields from the Cpt model will be serialized


class GuichetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guichet
        fields = '__all__'  # All fields from the Cpt model will be serialized        



