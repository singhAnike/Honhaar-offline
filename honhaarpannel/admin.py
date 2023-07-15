from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Student, Batch, School, Setting, Match, Round, Question, StudentQuestion
class StudentAdmin(ImportExportModelAdmin):
    list_display = ('device_id', 'student_name', 'father_name', 'date_of_birth', 'batch', 'standard')
    search_fields = ('device_id', 'student_name', 'father_name')
    list_filter = ('batch',)

admin.site.register(Student, StudentAdmin)
admin.site.register(Batch)
admin.site.register(School)
admin.site.register(Setting)
admin.site.register(Match)
admin.site.register(Round)
admin.site.register(Question)
admin.site.register(StudentQuestion)