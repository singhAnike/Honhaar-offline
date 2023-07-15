from rest_framework import serializers
from .models import Match, Round, Question

class QuestionSerializer(serializers.ModelSerializer):
    question_id=serializers.IntegerField(source='id')
    class Meta:
        model = Question
        fields = ['question_id','question_text', 'solution', 'options', 'correct_option']

class RoundSerializer(serializers.ModelSerializer):
    order_id=serializers.IntegerField(source='id')
    class Meta:
        model = Round
        fields = ['order_id','round_name', 'order']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        questions = Question.objects.filter(round=instance)
        representation['questions'] = QuestionSerializer(questions, many=True).data
        return representation

class MatchSerializer(serializers.ModelSerializer):
    match_id= serializers.IntegerField(source='id')
    class Meta:
        model = Match
        fields = ['match_id', 'match_name']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        rounds = Round.objects.filter(match=instance)
        representation['rounds'] = RoundSerializer(rounds, many=True).data
        return representation

