from honhaarpannel.models import Student, Batch, School, Setting, Match, Round, Question

def get_schools() -> School:
    return School.objects.all()

def get_batchs() -> Batch:
    return Batch.objects.all()

def get_students() -> Student:
    return Student.objects.all()

def get_settings() -> Setting:
    return Setting.objects.all()

def get_matchs() -> Match:
    return Match.objects.all()

def get_rounds() -> Round:
    return Round.objects.all()

def get_questions() -> Question:
    return Question.objects.all()