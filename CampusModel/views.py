from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render,redirect
from . import models
from .models import student_select
import json
from django.db.models import Q

# Create your views here.
#登入
def login(request):
	message = ""
	if request.method == "POST":
		studentid = request.POST.get('studentid', None)                     #得到填写的学生id
		password = request.POST.get('password', None)                       #得到填写的密码
		message = "You have to input all the information！"
		#print(studentid)

		if studentid and password:
			studentid = studentid.strip()
			try:
				student = models.student.objects.get(sid=studentid)         #从数据库里取出此用户的信息
				if student.password == password:                            #如果此用户密码与输入密码相同
					request.session['student_name'] = student.name          #将用户的基本信息存于session以便调用
					request.session['student_id'] = student.sid
					request.session['student_faculty'] = student.faculty
					request.session['student_grade'] = student.grade
					return redirect('/index/')                              #允许进入系统
				else:
					message = "Wrong password！"                            #密码不对，修改提示信息
			except:
				message = "The user do not exist！"                         #取不到该用户信息，用户不存在
	return render(request, 'login.html',{"message": message})               #阻拦用户进入系统，要求重新填写

#登出
def logout(request):
	# if not request.session.get('is_login', None):
	# 	return redirect("/index/")
	#request.session.flush()
	#del request.session['student_name']
	return redirect("/login/")

#主界面
def index(request):
    return render(request,'index.html')

#查看课程
def view_course(request):
	course_faculty = request.session.get('student_faculty')
	course_grade = request.session.get('student_grade')
	# courses_compulsory = models.course.objects.filter(grade=course_grade,faculty=course_faculty,category="C")
	# courses_elective = models.course.objects.filter(grade=course_grade,faculty=course_faculty,category="E*").exclude(faculty="general",category="E*")
	courses_compulsory = models.course.objects.filter(Q(faculty=course_faculty,category="C")|Q(faculty='general',category="C"))
	courses_elective = models.course.objects.filter(faculty=course_faculty,category="E*").exclude(faculty="general",category="E*")
	courses_general = models.course.objects.filter(faculty='general').exclude(category="C")
	res= {'courses_compulsory': courses_compulsory,'courses_elective':courses_elective,'courses_general':courses_general}
	return render(request, 'view_course.html',res)

#查找课程
def search_result(request):
	error_msg = ""
	if request.method == 'POST' and request.POST:
		search_input = request.POST.get('course_name',None)
		
		if search_input:
			course_result = models.course.objects.filter(Q(name__icontains=search_input)|Q(teacher__icontains=search_input)|Q(cid__icontains=search_input)|Q(faculty__icontains=search_input))
			if course_result:
				data = {'course_result':course_result,'error_msg': error_msg}
				return render(request,'search_result.html',data)
			else:
				error_msg = "Not found!"
				return render(request,'search_result.html',{'error_msg': error_msg})
		error_msg = "You have not input any key words!"	
	return render(request,'search_result.html',{'error_msg': error_msg})

#选择课程
def select_course(request):
	return render(request,'select_course.html')

#开始选课
def start_select(request):
	course_faculty = request.session.get('student_faculty')                                   #学生所属学院
	course_grade = request.session.get('student_grade')					                      #学生年级
	course_result = models.course.objects.filter(faculty=course_faculty, grade=course_grade)  #从数据库里拿出匹配该学生学院年级的课程

	#print("test")

	student_id = request.session.get('student_id')                                            #学生id
	# queryres = models.course.objects.filter(student_select="CN101")
	queryset = student_select.objects.filter(sid=student_id)                                  #从选课表中找到该学生选的课

		
	if request.method == 'POST' and request.POST:
		operation = request.POST.get('operation')
		if operation == 'add':                                                                #进行加课操作
			course_cid = request.POST.get('course_id')
			student_id = request.session.get('student_id')

			for i in queryset:
				course_select = models.course.objects.get(cid=course_cid)                     #学生希望选择的课程
				course_select_time = course_select.time                                       #学生希望选择的课程的时间
				#print(course_select_time[0:9])
				course_selected = models.course.objects.get(cid=i.cid)                        #学生已经选择的课程
				#print(course_cid)
				#print(i.cid)
				if course_select == course_selected :
					msg2="You have already selected this course!"
					print(msg2)
					res = { 'msg2':msg2}
					# return render(request,'start_select.html',res)
					return HttpResponse(json.dumps(res),content_type='application/json')
				course_selected_time = course_selected.time                                   #学生已经选择的课程的时间
				#print(course_selected_time[0:9])
				if course_select_time[0:9] == course_selected_time[0:9] :                     #如果存在两个时间相等，则学生不被允许选择
					msg2="Course time conflict!"
					print(msg2)
					res = { 'msg2':msg2}
					return HttpResponse(json.dumps(res),content_type='application/json')

			student_id2 = models.student.objects.get(sid=student_id)
			course_cid2 = models.course.objects.get(cid=course_cid)

			student_select.objects.create(sid=student_id2,cid=course_cid2)                    #创建一条新的选课数据
			msg2="Select successfully!"
			print(msg2)
			res = { 'msg2':msg2}
			return HttpResponse(json.dumps(res),content_type='application/json')
				# res_success = {'queryset':queryset,'course_result':course_result,'msg2':'msg2'}
				# return render(request,'start_select.html',res_success)
		else:                                                                                 #删课操作
			course_cid = request.POST.get('course_id')
			student_id = request.session.get('student_id')
			data = student_select.objects.filter(cid=course_cid,sid=student_id)
			if data:
				data.delete()
				msg2 = "You have delete this course successfully!"
				print(msg2)
				res = { 'msg2':msg2}
				return HttpResponse(json.dumps(res),content_type='application/json')
			else:
				msg2 = "You have not select this course yet."
				print(msg2)
				res = { 'msg2':msg2}
				return HttpResponse(json.dumps(res),content_type='application/json')
				# return render(request,'start_select.html',{'queryset':queryset,'crouse_result':course_result})
			# res = {'queryset':queryset,'course_result':course_result}
			# return render(request,'start_select.html',res)
	data = {'queryset':queryset,'course_result': course_result}
	print("test")
	return render(request,'start_select.html',data)


#忘记密码
def forgot_password(request):
	return render(request, 'forgot_password.html')

#修改密码
def reset_password(request):
	studentid = request.session.get('student_id')                                 #得到学生id
	passwordfirst = request.POST.get('passwordfirst', None)               		  #得到两次输入的密码
	passwordagain = request.POST.get('passwordagain', None)
	message = ""
	pwd_message = ""

	if passwordfirst and passwordagain:											  # 如果两次密码有值
		student = models.student.objects.get(sid=studentid)                       # 拿出当前学生的信息
		if passwordfirst == passwordagain:                                        # 如果两次密码相等
			if len(passwordfirst) ==  6:										  # 如果密码长度为6则修改密码为此密码
				student.password = passwordagain
				student.save()
				pwd_message = "You have changed your password just now!"
				return render(request, 'index.html', {"pwd_message": pwd_message})
				# return redirect('/index/',{"pwd_message": pwd_message})
			else:
				message = "The password need 6 characters!"                       # 密码长度不为6，发送错误信息
		else:
			message = "Your entered password not the same with the first one!"    # 两次密码不相等，发出错误提醒
	return render(request, 'reset_password.html',{"message": message})

#查看成绩/计算成绩
def view_grade(request):
	return render(request,'grade.html')

def calculate_grade(request):
	return render(request, 'calculate_grade.html')

def discussion_room(request):
	return render(request,'discussion_room.html')

def classroom(request):
	return render(request,'classroom.html')