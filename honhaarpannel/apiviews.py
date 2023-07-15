from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from honhaarpannel.serializers import MatchSerializer


from honhaarpannel.models import School, Batch, Student, Setting, Match, Round, Question
from honhaarpannel.services.commands import create_school, update_school, delete_school, create_batch, update_batch, delete_batch, create_student, update_student, delete_student , create_setting, update_setting, delete_setting, create_match, update_match, delete_match, create_round, update_round, delete_round, create_question, update_question, delete_question
from honhaarpannel.services.queries import get_schools, get_batchs, get_students, get_settings, get_matchs, get_rounds, get_questions

# SchoolApi view
class SchoolApi(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = School
            fields = ['school_name']

    class OutputSerializer(serializers.ModelSerializer):
        school_id = serializers.IntegerField(source="id")
        class Meta:
            model = School
            fields = ['school_id', 'school_name']
    
    def get(self, request, *args, **kwargs):
        if 'school_id' in kwargs:
            school = get_object_or_404(School, id=kwargs['school_id'])
            serializer = self.OutputSerializer(school)
            return Response(serializer.data, status=status.HTTP_200_OK)
        schools = get_schools()
        serializer = self.OutputSerializer(schools, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        school = create_school(**serializer.validated_data)
        output_serializer = self.OutputSerializer(school)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, school_id, *args, **kwargs):
        school = get_object_or_404(School, id=school_id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        school = update_school(school=school, **serializer.validated_data)
        output_serializer = self.OutputSerializer(school)
        return Response(output_serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, school_id, *args, **kwargs):
        school = get_object_or_404(School, id=school_id)
        delete_school(school=school)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# SchoolBatch Api view
class SchoolBatchApi(APIView):
    class InputSerializer(serializers.ModelSerializer):
        school_id= serializers.PrimaryKeyRelatedField(queryset= School.objects.all())
        class Meta:
            model = Batch
            fields = ['school_id', 'batch_name']
    class OutputSerializer(serializers.ModelSerializer):
        batch_id = serializers.IntegerField(source="id")
        
        class Meta:
            model = Batch
            fields = ['batch_id', 'school_id', 'batch_name']
    def get(self, request, *args, **kwargs):
        school_id = request.GET.get('school_id')
        
        if 'school_id' in request.GET:
                batches = Batch.objects.filter(school_id=school_id)
                serializer = self.OutputSerializer(batches, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        batchs = get_batchs()
        serializer=self.OutputSerializer(batchs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        school= serializer.validated_data.pop(
            'school_id') if 'school_id' in serializer.validated_data else None
        batch = create_batch(school=school, **serializer.validated_data)
        return Response(self.OutputSerializer(batch).data, status=status.HTTP_201_CREATED)
    
    def put(self, request, batch_id, *args, **kwargs):
        batch = get_object_or_404(Batch, id=batch_id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        school= serializer.validated_data.pop(
            'school_id') if 'school_id' in serializer.validated_data else None
        batch = update_batch(batch=batch,school=school, **serializer.validated_data)
        return Response(self.OutputSerializer(batch).data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, batch_id, *args, **kwargs):
        batch = get_object_or_404(Batch, id=batch_id)
        delete_batch(batch=batch)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Batch api view
class BatchApi(APIView):
    class InputSerializer(serializers.ModelSerializer):
        school_id= serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
        class Meta:
            model = Batch
            fields = ['school_id', 'batch_name']
    class OutputSerializer(serializers.ModelSerializer):
        batch_id = serializers.IntegerField(source="id")

        class Meta:
            model = Batch
            fields = ['batch_id', 'school', 'batch_name']
    def get(self, request, *args, **kwargs):
        if 'batch_id' in self.kwargs:
            batch = get_object_or_404(Batch, id=self.kwargs['batch_id'])
            serializer = self.OutputSerializer(batch)
            return Response(serializer.data, status=status.HTTP_200_OK)
        batchs = get_batchs()
        serializer=self.OutputSerializer(batchs, many=True)
        return Response(serializer.data)
       
    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        school= serializer.validated_data.pop(
            'school_id') if 'school_id' in serializer.validated_data else None      
        batch = create_batch(school=school, **serializer.validated_data)
        return Response(self.OutputSerializer(batch).data, status=status.HTTP_201_CREATED)
    
    def put(self, request, batch_id, *args, **kwargs):
        batch = get_object_or_404(Batch, id=batch_id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        school= serializer.validated_data.pop(
            'school_id') if 'school_id' in serializer.validated_data else None 
        batch = update_batch(batch=batch,school=school, **serializer.validated_data)
        return Response(self.OutputSerializer(batch).data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, batch_id, *args, **kwargs):
        batch = get_object_or_404(Batch, id=batch_id)
        delete_batch(batch=batch)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Student api view
class StudentApi(APIView):
    class InputSerializer(serializers.ModelSerializer):
        batch_id= serializers.PrimaryKeyRelatedField(queryset= Batch.objects.all())
        class Meta:
            model = Student
            fields = ['device_id', 'student_name', 'father_name', 'date_of_birth', 'batch_id']
    class OutputSerializer(serializers.ModelSerializer):
        student_id = serializers.IntegerField(source="id")        
        class Meta:
            model = Student
            fields = ['student_id', 'device_id', 'student_name', 'father_name', 'date_of_birth', 'batch_id']
    def get(self, request, *args, **kwargs):
        if 'student_id' in self.kwargs:
            student = get_object_or_404(Student, id=self.kwargs['student_id'])
            serializer = self.OutputSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        students = get_students()
        serializer=self.OutputSerializer(students, many=True)
        return Response(serializer.data)
       
    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        batch= serializer.validated_data.pop(
            'batch_id') if 'batch_id' in serializer.validated_data else None
        student = create_student(batch=batch, **serializer.validated_data)
        return Response(self.OutputSerializer(student).data, status=status.HTTP_201_CREATED)
    
    def put(self, request, student_id, *args, **kwargs):
        student = get_object_or_404(Student, id=student_id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        batch= serializer.validated_data.pop(
            'batch_id') if 'batch_id' in serializer.validated_data else None
        student = update_student(student=student,batch=batch, **serializer.validated_data)
        return Response(self.OutputSerializer(student).data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, student_id, *args, **kwargs):
        student = get_object_or_404(Student, id=student_id)
        delete_student(student=student)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# studentBatch api view
class StudentBatchApi(APIView):
    class InputSerializer(serializers.ModelSerializer):
        batch_id= serializers.PrimaryKeyRelatedField(queryset= Batch.objects.all())
        class Meta:
            model = Student
            fields = ['device_id', 'student_name', 'father_name', 'date_of_birth', 'batch_id']
    class OutputSerializer(serializers.ModelSerializer):
        student_id = serializers.IntegerField(source="id")        
        class Meta:
            model = Student
            fields = ['student_id', 'device_id', 'student_name', 'father_name', 'date_of_birth', 'batch_id']
    def get(self, request, *args, **kwargs):
        batch_id=request.GET.get('batch_id')
        if 'batch_id' in request.GET:
            batches = Student.objects.filter(batch=batch_id)
            serializer = self.OutputSerializer(batches, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        students = get_students()
        serializer=self.OutputSerializer(students, many=True)
        return Response(serializer.data)
       
    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        batch= serializer.validated_data.pop(
            'batch_id') if 'batch_id' in serializer.validated_data else None
        student = create_student(batch=batch, **serializer.validated_data)
        return Response(self.OutputSerializer(student).data, status=status.HTTP_201_CREATED)
    
    def put(self, request, student_id, *args, **kwargs):
        student = get_object_or_404(Student, id=student_id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        batch= serializer.validated_data.pop(
            'batch_id') if 'batch_id' in serializer.validated_data else None
        student = update_student(student=student,batch=batch, **serializer.validated_data)
        return Response(self.OutputSerializer(student).data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, student_id, *args, **kwargs):
        student = get_object_or_404(Student, id=student_id)
        delete_student(student=student)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Setting api view 
class SettingApi(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Setting
            fields = ['round_one_introduction', 'round_one_sponsor', 'round_one_instruction', 'round_two_introduction', 'round_two_sponsor', 'round_two_instruction', 'round_three_introduction', 'round_three_sponsor', 'round_three_instruction']
    class OutputSerializer(serializers.ModelSerializer):
        setting_id = serializers.IntegerField(source="id")

        class Meta:
            model = Setting
            fields = ['setting_id', 'round_one_introduction', 'round_one_sponsor', 'round_one_instruction', 'round_two_introduction', 'round_two_sponsor', 'round_two_instruction', 'round_three_introduction', 'round_three_sponsor', 'round_three_instruction']
    def get(self, request, *args, **kwargs):
        if 'setting_id' in self.kwargs:
            setting = get_object_or_404(Setting, id=self.kwargs['setting_id'])
            serializer = self.OutputSerializer(setting)
            return Response(serializer.data, status=status.HTTP_200_OK)
        settings = get_settings()
        serializer=self.OutputSerializer(settings, many=True)
        return Response(serializer.data)
        
    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        setting = create_setting(**serializer.validated_data)
        return Response(self.OutputSerializer(setting).data, status=status.HTTP_201_CREATED)
    def put(self, request, setting_id, *args, **kwargs):
        setting = get_object_or_404(Setting, id=setting_id)
       
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        setting = update_setting(setting=setting, **serializer.validated_data)
        return Response(self.OutputSerializer(setting).data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, setting_id, *args, **kwargs):
        setting = get_object_or_404(Setting, id=setting_id)
        delete_setting(setting=setting)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Match api view
class MatchApi(APIView):
    class InputSerializer(serializers.ModelSerializer):
        school_id= serializers.PrimaryKeyRelatedField(queryset= School.objects.all())
        class Meta:
            model = Match
            fields = ['match_name', 'school_id']
    class OutputSerializer(serializers.ModelSerializer):
        match_id = serializers.IntegerField(source="id")
        class Meta:
            model = Match
            fields = ['match_id', 'match_name', 'school_id']
   
    def get(self, request, *args, **kwargs):
        if 'match_id' in self.kwargs:
            match = get_object_or_404(Match, id=self.kwargs['match_id'])            
            serializer = self.OutputSerializer(match)
            return Response(serializer.data, status=status.HTTP_200_OK)
        matches = get_matchs()
        serializer = self.OutputSerializer(matches, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        school= serializer.validated_data.pop(
            'school_id') if 'school_id' in serializer.validated_data else None
        match = create_match(school=school, **serializer.validated_data)
        return Response(self.OutputSerializer(match).data, status=status.HTTP_201_CREATED)
    
    def put(self, request, match_id, *args, **kwargs):
        match = get_object_or_404(Match, id=match_id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        school= serializer.validated_data.pop(
            'school_id') if 'school_id' in serializer.validated_data else None
        match = update_match(match=match, school=school, **serializer.validated_data)
        return Response(self.OutputSerializer(match).data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, match_id, *args, **kwargs):
        match = get_object_or_404(Match, id=match_id)
        delete_match(match=match)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# schoolmatch api view
class SchoolMatchApi(APIView):
    class InputSerializer(serializers.ModelSerializer):
        school_id= serializers.PrimaryKeyRelatedField(queryset= School.objects.all())
        class Meta:
            model = Match
            fields = ['match_name', 'school_id']
    class OutputSerializer(serializers.ModelSerializer):
        match_id = serializers.IntegerField(source="id")
        class Meta:
            model = Match
            fields = ['match_id', 'match_name', 'school_id']
   
    def get(self, request, *args, **kwargs):
        if 'school_id' in self.kwargs:
            matches = Match.objects.filter(school=self.kwargs['school_id'])
            serializer = self.OutputSerializer(matches, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        matches = get_matchs()
        serializer = self.OutputSerializer(matches, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        school= serializer.validated_data.pop(
            'school_id') if 'school_id' in serializer.validated_data else None
        match = create_match(school=school, **serializer.validated_data)
        return Response(self.OutputSerializer(match).data, status=status.HTTP_201_CREATED)
    
    def put(self, request, match_id, *args, **kwargs):
        match = get_object_or_404(Match, id=match_id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        school= serializer.validated_data.pop(
            'school_id') if 'school_id' in serializer.validated_data else None
        match = update_match(match=match, school=school, **serializer.validated_data)
        return Response(self.OutputSerializer(match).data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, match_id, *args, **kwargs):
        match = get_object_or_404(Match, id=match_id)
        delete_match(match=match)
        return Response(status=status.HTTP_204_NO_CONTENT)


# Round api view
class RoundApi(APIView):
    class InputSerializer(serializers.ModelSerializer):
        match_id= serializers.PrimaryKeyRelatedField(queryset=Match.objects.all())
        class Meta:
            model = Round
            fields = ['round_name', 'match_id', 'order']
    class OutputSerializer(serializers.ModelSerializer):
        round_id = serializers.IntegerField(source="id")

        class Meta:
            model = Round
            fields = ['round_id', 'round_name', 'match_id', 'order']
    def get(self, request, *args, **kwargs):
       
        if 'round_id' in self.kwargs:
            round = get_object_or_404(Round, id=self.kwargs['round_id'])
            serializer = self.OutputSerializer(round)
            return Response(serializer.data, status=status.HTTP_200_OK)
        rounds = get_rounds()
        serializer=self.OutputSerializer(rounds, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        match= serializer.validated_data.pop(
            'match_id') if 'match_id' in serializer.validated_data else None
        round = create_round(match=match, **serializer.validated_data)
        return Response(self.OutputSerializer(round).data, status=status.HTTP_201_CREATED)
    
    def put(self, request, round_id, *args, **kwargs):
        round = get_object_or_404(Round, id=round_id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        match= serializer.validated_data.pop(
            'match_id') if 'match_id' in serializer.validated_data else None
        round = update_round(round=round,match=match, **serializer.validated_data)
        return Response(self.OutputSerializer(round).data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, round_id, *args, **kwargs):
        round = get_object_or_404(Round, id=round_id)
        delete_round(round=round)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Questions api view
class QuestionApi(APIView):
    class InputSerializer(serializers.ModelSerializer):
        round_id=serializers.PrimaryKeyRelatedField(queryset=Round.objects.all())
        class Meta:
            model = Question
            fields = ['round_id', 'question_text', 'solution', 'options', 'correct_option']
    class OutputSerializer(serializers.ModelSerializer):
        question_id = serializers.IntegerField(source="id")

        class Meta:
            model = Question
            fields = ['question_id', 'round_id', 'question_text', 'solution', 'options', 'correct_option']
    def get(self, request, *args, **kwargs):
        if 'question_id' in self.kwargs:
            question = get_object_or_404(Question, id=self.kwargs['question_id'])
            serializer = self.OutputSerializer(question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        question = get_questions()
        serializer=self.OutputSerializer(question, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        round= serializer.validated_data.pop(
            'round_id') if 'round_id' in serializer.validated_data else None 
        question = create_question(round=round, **serializer.validated_data)
        return Response(self.OutputSerializer(question).data, status=status.HTTP_201_CREATED)
    def put(self, request, question_id, *args, **kwargs):
        question = get_object_or_404(Question, id=question_id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        round= serializer.validated_data.pop(
            'round_id') if 'round_id' in serializer.validated_data else None
        question = update_question(question=question,round=round, **serializer.validated_data)
        return Response(self.OutputSerializer(question).data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, question_id, *args, **kwargs):
        question = get_object_or_404(Question, id=question_id)
        delete_question(question=question)
        return Response(status=status.HTTP_204_NO_CONTENT)

class MatchesDetailsApi(APIView):
    def get(self, request, *args, **kwargs):
        if 'match_id' in self.kwargs:
            match = get_object_or_404(Match, id=self.kwargs['match_id'])
            serializer = MatchSerializer(match)
            return Response(serializer.data, status=status.HTTP_200_OK)
        matches = Match.objects.all()
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
