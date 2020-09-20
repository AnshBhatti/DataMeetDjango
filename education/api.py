from .serializers import *
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework import generics
from .aws import get_emotion
import requests
from .models import *
from django.contrib.auth.models import User

class RegistrationAPI(generics.GenericAPIView):
    serializer_class=CreateUserSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        items = User.objects.filter(username=user.username,first_name=user.first_name,last_name=user.last_name).count()
        if items>1:
            c = Teacher.objects.filter(teacher_name=user.first_name+' '+user.last_name).count()
            word="student"
            if c>0:
                word="teacher"
            user.delete()
            return Response({
                "status": word.capitalize() +" has already registered. Please login using "+word+" login"
            })
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class AddSession(generics.GenericAPIView):
    serializer_class=TeacherSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item=serializer.save()
        objects=Teachers.objects.filter(teacher_name=item.teacher_name)
        if objects.count()==0:
            return Response({
                "status": "Failed. Please enter a valid teacher name"
            })
        for a in range(len(objects)):
            if objects[a].sessions!=item.sessions:
                objects[a].delete()
        return Response({
            "status": "Session added"
        })

class StudentAddSession(generics.GenericAPIView):
    serializer_class=SchoolSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item=serializer.save()
        objects=School.objects.filter(student_first=item.student_first,student_last=item.student_last)[0]
        item.teacher_first=objects.teacher_first
        item.teacher_last=objects.teacher_last
        item.schoolname=objects.schoolname
        if objects.total!=0:
            objects.delete()
        return Response({
            "status": "Session added"
        })

class FrameAPI(generics.GenericAPIView):
    serializer_class=FrameSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        frame=serializer.save()
        names=frame.student_name.split()
        li=get_emotion(frame.image)
        frame.confusion=li[0]
        frame.happy=li[1]
        frame.sad=li[2]
        frame.surprised=li[3]
        student=School.objects.filter(student_first=names[0],student_last=names[1])[0]
        if frame.teacher_name=="None":
            frame.teacher_name=student.teacher_first+' '+student.teacher_last
        student.confusion+=li[0]
        student.happy+=li[1]
        student.sad+=li[2]
        student.surprised+=li[3]
        student.total+=1
        student.save()
        frame.save()
        frames=Frame.objects.filter(teacher_name=frame.teacher_name)
        for a in range(len(frames)):
            if frames[a].timestamp+60<frame.timestamp:
                frames[a].delete()
        return Response({
            "Status": "Frame submitted"
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class=LoginUserSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "student": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class TeacherLoginAPI(generics.GenericAPIView):
    serializer_class=LoginTeacherSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "teacher": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class SchoolAPI(generics.GenericAPIView):
    serializer_class=SchoolSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item=serializer.save()
        if Teachers.objects.filter(teacher_name=item.teacher_first+' '+item.teacher_last).count()==0:
            item.delete()
            return Response({
                "Status":"Student class registration unsuccessful, please add a valid teacher."
            })
        return Response(serializer.data)

class TeacherAPI(generics.GenericAPIView):
    serializer_class=TeacherSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)