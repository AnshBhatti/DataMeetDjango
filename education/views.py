from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from .serializers import *
from rest_framework.generics import ListAPIView

# Create your views here.

def index(request):
    return HttpResponse("<h1>Hello World</h1>")

class SchoolView(ListAPIView):
    #queryset=School.objects.all()
    def get_queryset(self):
        return School.objects.filter(teacher_first=' '.join(self.kwargs["t_first"].split('_')),teacher_last=' '.join(self.kwargs["t_last"].split('_')))
    serializer_class=SchoolSerializer

class TeacherView(ListAPIView):
    #queryset=Teachers.objects.all()
    def get_queryset(self):
        return Teachers.objects.filter(school_name=' '.join(self.kwargs["t_name"].split('_')))
    serializer_class=TeacherSerializer

class AverageEmotionView(ListAPIView):
    def get_queryset(self):
        d={"confusion":0,"happy":0,"sad":0,"surprised":0}
        first=' '.join(self.kwargs["t_first"].split('_'))
        last=' '.join(self.kwargs["t_last"].split('_'))
        students=School.objects.filter(teacher_first=first,teacher_last=last)
        teacher=Teachers.objects.filter(teacher_name=first+' '+last)[0]
        sess_id=teacher.sessions
        n=0
        l=list(d.keys())
        for student in students:
            if student.total>0:
                n+=1
                arr=[student.confusion,student.happy,student.sad,student.surprised]
                for i in range(len(arr)):
                    d[l[i]]+=arr[i]/(student.total)
        n=max(1,n)
        items=EmotionQueries.objects.filter(teacher_name=first+' '+last,school_name=student.schoolname).delete()
        emotion=EmotionQueries(teacher_name=first+' '+last,
        school_name=student.schoolname,
        confusion=d["confusion"]/n*100,
        happy=d["happy"]/n*100,
        sad=d["sad"]/n*100,
        surprised=d["surprised"]/n*100,
        session=sess_id)
        emotion.save()
        return EmotionQueries.objects.filter(teacher_name=first+' '+last,session=sess_id)
    serializer_class=EmotionSerializer

class RealTimeFrameView(ListAPIView):
    def get_queryset(self):
        d={"confusion":0,"happy":0,"sad":0,"surprised":0}
        first=' '.join(self.kwargs["t_first"].split('_'))
        last=' '.join(self.kwargs["t_last"].split('_'))
        frames=Frame.objects.filter(teacher_name=first+' '+last)
        n=max(1,frames.count())
        l=list(d.keys())
        for frame in frames:
            arr=[frame.confusion,frame.happy,frame.sad,frame.surprised]
            for i in range(len(arr)):
                d[l[i]]+=arr[i]
        items=EmotionQueries1.objects.filter(teacher_name=first+' '+last).delete()
        emotion=EmotionQueries1(teacher_name=first+' '+last,
        confusion=d["confusion"]/n,
        happy=d["happy"]/n,
        sad=d["sad"]/n,
        surprised=d["surprised"]/n*100)
        emotion.save()
        return EmotionQueries1.objects.filter(teacher_name=first+' '+last)
    serializer_class=EmotionSerializer1