from django.db import models
class School(models.Model):
    school_name = models.CharField(max_length=100)
    def __str__(self):
        return self.school_name
class Batch(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=100)
    def __str__(self):
        return self.batch_name
class Student(models.Model):
    device_id=models.IntegerField()
    student_name=models.CharField(max_length=100)
    father_name=models.CharField(max_length=100)
    date_of_birth=models.DateField()
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    standard=models.IntegerField()
    def __str__(self):
        return self.student_name
class Setting(models.Model):
    round_one_introduction = models.FileField(null=True, blank=True)
    round_one_sponsor = models.FileField(null=True, blank=True)
    round_one_instruction = models.FileField(null=True, blank=True)
    round_two_introduction = models.FileField(null=True, blank=True)
    round_two_sponsor = models.FileField(null=True, blank=True)
    round_two_instruction = models.FileField(null=True, blank=True)
    round_three_introduction = models.FileField(null=True, blank=True)
    round_three_sponsor = models.FileField(null=True, blank=True)
    round_three_instruction = models.FileField(null=True, blank=True)
class Match(models.Model):
    match_name=models.CharField(max_length=100)
    school=models.ForeignKey(School, on_delete=models.CASCADE)
    def __str__(self):
        return self.match_name
class Round(models.Model):
    round_name=models.CharField(max_length=100)
    match=models.ForeignKey(Match, on_delete=models.CASCADE)
    order=models.IntegerField()
    def __str__(self):
        return(self.round_name)
class Question(models.Model):
    round=models.ForeignKey(Round, on_delete=models.CASCADE)
    question_text=models.TextField()
    solution=models.TextField()
    options=models.CharField(max_length=100)
    correct_option=models.PositiveIntegerField()
    topic_name=models.CharField(max_length=100)
    topic_code=models.IntegerField()
    def __str__(self):
        return(self.question_text)
class StudentQuestion(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    correct=models.BooleanField()
    duration=models.FloatField()
    class Meta:
        unique_together = ('student', 'question')