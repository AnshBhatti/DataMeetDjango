from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def valid_teacher(first,last):
    c=Teachers.objects.all().filter(teacher_name=first+' '+last).count()
    if c>0:
        return True
    return False
    

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self, data):
        user = authenticate(**data)
        result = valid_teacher(user.first_name,user.last_name)
        if user and user.is_active and not result:
            return user
        elif result:
            raise serializers.ValidationError("Teacher must sign in from teacher's login page.")
        else:
            raise serializers.ValidationError("Unable to log in with provided credentials.")

class LoginTeacherSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self, data):
        user = authenticate(**data)
        result = valid_teacher(user.first_name,user.last_name)
        if user and user.is_active and result:
            return user
        elif not result:
            raise serializers.ValidationError("Student must sign in from student's login page.")    
        raise serializers.ValidationError("Unable to log in with provided credentials.")

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name','email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        first_name = validated_data['first_name'],
                                        last_name = validated_data['last_name'],
                                        password = validated_data['password'])
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name','email', 'username')

class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = ('student_name','teacher_name','image','timestamp','confusion','happy','sad','surprised')

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionQueries
        fields = ('teacher_name','school_name','confusion','surprised','happy','sad','session')

class EmotionSerializer1(serializers.ModelSerializer):
    class Meta:
        model = EmotionQueries1
        fields = ('teacher_name','confusion','surprised','happy','sad')

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('student_first',
        'student_last',
        'teacher_first',
        'teacher_last',
        'schoolname',
        'confusion',
        'surprised',
        'happy',
        'sad',
        'total',
        'session')

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teachers
        fields = ('teacher_name','school_name','sessions')