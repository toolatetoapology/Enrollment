from django.db import models

# Create your models here.
class student(models.Model):
    sid = models.CharField(primary_key=True,max_length=20)
    #sid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    faculty = models.CharField(max_length=20,default='IT')
    grade = models.IntegerField(default=1)
    password = models.CharField(max_length=10,default='123456')

    def __str__(self):
    	return self.sid

class course(models.Model):
	cid = models.CharField(primary_key=True,max_length=10)
	#cid = models.AutoField(primary_key=True)
	name = models.CharField(max_length=40)
	teacher = models.CharField(max_length=20)
	time = models.CharField(max_length=20,default='Wed-15:00-18:20')
	credit = models.IntegerField(default=4)
	faculty = models.CharField(max_length=10,default='IT') 
	grade = models.IntegerField(default=1)
	category = models.CharField(max_length=2,default='C')
	classroom = models.CharField(max_length=6,default='C408')
	def __str__(self):
		return self.cid

# class student_course(models.Model):
#     sid = models.CharField(primary_key=True,max_length=20)
#     course_id = models.CharField(max_length=10)

class student_select(models.Model):
	# user_group = models.ForeignKey('GroupInfos', to_field='uid', on_delete='CASCADE')
	sid = models.ForeignKey('student', on_delete='CASCADE')
	cid = models.ForeignKey('course', on_delete='CASCADE')
	class Meta:
		unique_together = (('sid','cid'),)
	grade = models.CharField(max_length=2)
	teacher = models.CharField(max_length=20)
	# def __str__(self):
	# 	return self.cid
	# def __str__(self):
	# 	return self.sid
	
