from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#_______________________________________________________________________________________________________________________

class Tutor(User):
    class Meta():
        db_table = "Tutors"

    pass

    def __str__(self):              # __unicode__ on Python 2
        return self.first_name + ' ' + self.last_name
#_______________________________________________________________________________________________________________________

class Student(User):
    class Meta():
        db_table = "Students"

    pass

    def __str__(self):              # __unicode__ on Python 2
        return self.first_name + ' ' + self.last_name
#_______________________________________________________________________________________________________________________

class Topic(models.Model):
    class Meta():
        db_table = "Topics"

    topic_name = models.CharField(max_length=50)
    topic_description = models.CharField(max_length=100)

    def __str__(self):              # __unicode__ on Python 2
        return self.topic_name
#_______________________________________________________________________________________________________________________

class Question(models.Model):
    class Meta():
        db_table = "Questions"

    tutor_id = models.ForeignKey(Tutor)
    topic_id = models.ForeignKey(Topic)
    question_text = models.CharField(max_length=200)


    def __str__(self):              # __unicode__ on Python 2
        return self.question_text
#_______________________________________________________________________________________________________________________

class Answer(models.Model):
    class Meta():
        db_table = "Answers"

    question_id = models.ForeignKey(Question)
    answer_text = models.CharField(max_length=100)
    is_correct = models.IntegerField(default=0)

    def __str__(self):              # __unicode__ on Python 2
        return self.answer_text
#_______________________________________________________________________________________________________________________

class Result(models.Model):
    class Meta():
        db_table = "Results"

    student_id = models.ForeignKey(Student)
    topic_id = models.ForeignKey(Topic)
    mark = models.IntegerField(default=0)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.mark)
#_______________________________________________________________________________________________________________________



