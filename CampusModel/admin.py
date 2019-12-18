from django.contrib import admin
from CampusModel.models import student,course,student_select
 
# Register your models here.

class studentAdmin(admin.ModelAdmin):
    list_display = ['sid','name','faculty','grade']

class courseAdmin(admin.ModelAdmin):
	list_display = ['cid','name','teacher','time','credit','faculty','grade','category','classroom']
	list_editable = ['teacher','time','classroom']

class studentselectAdmin(admin.ModelAdmin):
	list_display = ['sid','cid']

admin.site.register(student,studentAdmin)
admin.site.register(course,courseAdmin)
admin.site.register(student_select,studentselectAdmin)