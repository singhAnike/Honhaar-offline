from honhaarpannel.models import Student, School, Batch, Setting, Match, Round, Question
from django.core.files import File
import datetime
# school commads
def create_school(school_name:str) -> School:
    school = School.objects.create(
    school_name=school_name,
    )
    return school
def update_school(school: School, school_name:str) -> School:
    school.school_name=school_name
    school.save()
    return school
def delete_school(school: School) -> None:
    school.delete()
    return

# Batch commands 
def create_batch(school:School, batch_name:str) -> Batch:
    batch = Batch.objects.create(
    school=school,
    batch_name=batch_name,
    )
    return batch
def update_batch(batch: Batch, school:School, batch_name:str) -> Batch:
    batch.school=school
    batch.batch_name=batch_name
    batch.save()
    return batch
def delete_batch(batch: Batch) -> None:
    batch.delete()
    return

# student command 
def create_student(device_id:str, student_name:str, father_name:str, date_of_birth:datetime.date, batch:Batch) -> Student:
    student = Student.objects.create(
    device_id=device_id,
    student_name=student_name,
    father_name=father_name,
    date_of_birth=date_of_birth,
    batch=batch,
    )
    return student
def update_student(student: Student, device_id:str, student_name:str, father_name:str, date_of_birth:datetime.date, batch:Batch) -> Student:
    student.device_id=device_id
    student.student_name=student_name
    student.father_name=father_name
    student.date_of_birth=date_of_birth
    student.batch=batch
    student.save()
    return student
def delete_student(student: Student) -> None:
    student.delete()
    return

# setting commands
def create_setting(round_one_introduction:File=None, round_one_sponsor:File=None, round_one_instruction:File=None, round_two_introduction:File=None, round_two_sponsor:File=None,
                    round_two_instruction:File=None, round_three_introduction:File=None, round_three_sponsor:File=None, round_three_instruction:File=None) -> Setting:
    setting = Setting.objects.create(
    round_one_introduction=round_one_introduction,
    round_one_sponsor=round_one_sponsor,
    round_one_instruction=round_one_instruction,
    round_two_introduction=round_two_introduction,
    round_two_sponsor=round_two_sponsor,
    round_two_instruction=round_two_instruction,
    round_three_introduction=round_three_introduction,
    round_three_sponsor=round_three_sponsor,
    round_three_instruction=round_three_instruction,
    )
    return setting
def update_setting(setting: Setting, round_one_introduction:File=None, round_one_sponsor:File=None, round_one_instruction:File=None, round_two_introduction:File=None, round_two_sponsor:File=None,
                    round_two_instruction:File=None, round_three_introduction:File=None, round_three_sponsor:File=None, round_three_instruction:File=None) -> Setting:

    setting.round_one_introduction=round_one_introduction
    setting.round_one_sponsor=round_one_sponsor
    setting.round_one_instruction=round_one_instruction
    setting.round_two_introduction=round_two_introduction
    setting.round_two_sponsor=round_two_sponsor
    setting.round_two_instruction=round_two_instruction
    setting.round_three_introduction=round_three_introduction
    setting.round_three_sponsor=round_three_sponsor
    setting.round_three_instruction=round_three_instruction
    setting.save()
    return setting
def delete_setting(setting: Setting) -> None:
    setting.delete()
    return

# match commands
def create_match(match_name:str, school:School) -> Match:
    match = Match.objects.create(
    match_name=match_name,
    school=school,
    )
    return match
def update_match(match: Match, match_name:str, school:School) -> Match:
    match.match_name=match_name
    match.school=school
    match.save()
    return match
def delete_match(match: Match) -> None:
    match.delete()
    return

# Round commands
def create_round(round_name:str, match:Match, order:int) -> Round:
    round = Round.objects.create(
    round_name=round_name,
    match=match,
    order=order,
    )
    return round
def update_round(round: Round, round_name:str, match:Match, order:int) -> Round:
    round.round_name=round_name
    round.match=match
    round.order=order
    round.save()
    return round
def delete_round(round: Round) -> None:
    round.delete()
    return

# Questions commands
def create_question(round:Round, question_text:str, solution:str, options:str, correct_option:str) -> Question:
    question = Question.objects.create(
    round=round,
    question_text=question_text,
    solution=solution,
    options=options,
    correct_option=correct_option,
    )
    return question
def update_question(question: Question, round:Round, question_text:str, solution:str, options:str, correct_option:str) -> Question:
    question.round=round
    question.question_text=question_text
    question.solution=solution
    question.options=options
    question.correct_option=correct_option
    question.save()
    return question
def delete_question(question: Question) -> None:
    question.delete()
    return