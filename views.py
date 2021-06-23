from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
import random
import smtplib
import pandas as pd
from django.core.files.storage import FileSystemStorage
from twilio.rest import Client
from django.contrib.auth.models import AnonymousUser, User
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

data={}
data["name"] = "None"
data["fee"] = "100"
data["time"] = "1"
data["marks"] = "0"
data["total"] = "3"

    
passval, useremail = "", ""
def examinerHome(request):
    ob12 = User.objects.get(email = "admin@admin.com")
    payc = examscore.objects.all()
    oe = QPExams.objects.all()
    ou = User.objects.all()
    return render(request, 'adminWeb/index.html', {"name": ob12.first_name, "excount": str(oe.count()), "paycount": str(payc.count()), "usercount": str(ou.count()-1)})

def examinerAddExam(request):
    ob12 = User.objects.get(email = "admin@admin.com")
    ob = exams.objects.all()
    print("Count: ", ob.count())
    payc = examscore.objects.all()
    oe = QPExams.objects.all()
    return render(request, 'adminWeb/addExam.html', {"exams":ob, "name": ob12.first_name, "excount": str(oe.count()), "paycount": str(payc.count())})

def examinerUpdateExam(request):
    ob12 = User.objects.get(email = "admin@admin.com")
    ob = exams.objects.all()
    return render(request, 'adminWeb/updateQuestionPaper.html', {"exams":ob, "name":ob12.first_name})

def examinerGetValues(request):
    exam = request.GET.get("exam")
    ob=exams.objects.get(name = str(exam))
    data={}
    data["name"] = ob.name
    data["fee"] = ob.fee
    data["time"] = ob.timeDuration
    data["typ"] = ob.Type
    data["diff"] = ob.Difficulty
    print (data)
    return JsonResponse(data,safe=False)

def examinerGetAllValues(request):
    exam = request.GET.get("exam")
    try:
        ob=QPExams.objects.get(name = str(exam))
        data={}
        data["name"] = ob.name
        data["fee"] = ob.fee
        data["time"] = ob.timeDuration
        data["rules"] = ob.rules
        data["que"] = ob.que
        data["opt1"] = ob.opt1
        data["opt2"] = ob.opt2
        data["opt3"] = ob.opt3
        data["opt4"] = ob.opt4
        data["ans"] = ob.ans
        data["typ"] = ob.Type
        data["diff"] = ob.Difficulty
        print (data)
    except:
        ob=exams.objects.get(name = str(exam))
        data={}
        data["name"] = ob.name
        data["fee"] = ob.fee
        data["time"] = ob.timeDuration
        data["rules"] = ""
        data["que"] = ""
        data["opt1"] = ""
        data["opt2"] = ""
        data["opt3"] = ""
        data["opt4"] = ""
        data["ans"] = ""
        print (data)
    return JsonResponse(data,safe=False)

def examinerCheckResult(request):
    global data
    ans = request.GET.get("ans")
    
    ex = request.GET.get("ex")
    ob=QPExams.objects.get(name = ex)
    data={}
    data["name"] = ob.name
    data["fee"] = ob.fee
    data["time"] = ob.timeDuration
    ans = ans.split(";")
    answers = str(ob.ans).split(";")
    print(answers, ans)
    m=0
    for i in range(len(ans)-1):
        a1 = ans[i].replace("'","")
        a1 = a1.replace("(","")
        a1 = a1.replace(")","")
        a2 = answers[i].replace("'","")
        a2 = a2.replace("(","")
        a2 = a2.replace(")","")
        
        if a1==a2:
            m+=1
    data["marks"] = str(m)
    data["total"] = str(len(ans)-1)
    print (data)
    return JsonResponse(data,safe=False)

def examinerRulesQP(request):
    ob12 = User.objects.get(email = "admin@admin.com")
    e = request.GET.get("exam")
    typ = request.GET.get("typ")
    lvl = request.GET.get("lvl")
    print(typ)
    print(lvl)
    e = e.replace("(", "")
    e = e.replace("'", "")
    e = e.replace(")", "")
    t = request.GET.get("time")
    t = t.replace("(", "")
    t = t.replace("'", "")
    t = t.replace(")", "")
    f = request.GET.get("fee")
    f = f.replace("(", "")
    f = f.replace("'", "")
    f = f.replace(")", "")
    rules = request.GET.get("rules")
    rules = rules.replace("(", "")
    rules = rules.replace("'", "")
    rules = rules.replace(")", "")
    rules = rules.replace("\n",";")
    que = request.GET.get("que")
    que = que.replace("(", "")
    que = que.replace("'", "")
    que = que.replace(")", "")
    que = que.replace("\n",";")
    opt1 = request.GET.get("opt1")
    opt1 = opt1.replace("(", "")
    opt1 = opt1.replace("'", "")
    opt1 = opt1.replace(")", "")
    opt1 = opt1.replace("\n",";")
    opt2 = request.GET.get("opt2")
    opt2 = opt2.replace("(", "")
    opt2 = opt2.replace("'", "")
    opt2 = opt2.replace(")", "")
    opt2 = opt2.replace("\n",";")
    opt3 = request.GET.get("opt3")
    opt3 = opt3.replace("(", "")
    opt3 = opt3.replace("'", "")
    opt3 = opt3.replace(")", "")
    opt3 = opt3.replace("\n",";")
    opt4 = request.GET.get("opt4")
    opt4 = opt4.replace("(", "")
    opt4 = opt4.replace("'", "")
    opt4 = opt4.replace(")", "")
    opt4 = opt4.replace("\n",";")
    ans = request.GET.get("answers")
    ans = ans.replace("(", "")
    ans = ans.replace("'", "")
    ans = ans.replace(")", "")
    ans = ans.replace("\n",";")
    print("Exam: ",e)
    print("Time: ",t)
    print("Fee: ",f)
    print("Rules: ",rules)
    print("Que: ",que)
    print("Opt1: ",opt1)
    print("Opt2: ",opt2)
    print("Opt3: ",opt3)
    print("Opt4: ",opt4)
    print("Ans: ",ans)
    qlist=que.split(";")
    qlist = list(filter(None, qlist))
    anslist=ans.split(";")
    anslist = list(filter(None, anslist))
    opt1list=opt1.split(";")
    opt1list = list(filter(None, opt1list))
    opt2list=opt2.split(";")
    opt2list = list(filter(None, opt2list))
    opt3list=opt3.split(";")
    opt3list = list(filter(None, opt3list))
    opt4list=opt4.split(";")
    opt4list = list(filter(None, opt4list))
    print("anslist",anslist)
    print("opt1list",opt1list)
    print("opt2list",opt2list)
    
    k=0
    for i in range(len(qlist)):
        allopt=[]
        allopt.append(opt1list[i])
        allopt.append(opt2list[i])
        allopt.append(opt3list[i])
        allopt.append(opt4list[i])
        print(allopt)
        print(anslist[i])
        if (anslist[i] not in allopt):
            k=1
            break
            
    if(k==0) :           
        try:
            ob=QPExams(
                name = e,
                fee = f,
                timeDuration = t,
                rules = rules,
                que = que,
                opt1 = opt1,
                opt2 = opt2,
                opt3 = opt3,
                opt4 = opt4,
                ans = ans,
                Type=typ,
                Difficulty=lvl
                ).save()
            data={}
            data["res"] = "Successfully Added"
        except Exception as ex:
            ob=QPExams.objects.get(name = e)
            ob.fee = f
            ob.timeDuration = t
            ob.rules = rules
            ob.que = que
            ob.opt1 = opt1
            ob.opt2 = opt2
            ob.opt3 = opt3
            ob.opt4 = opt4
            ob.ans = ans
            Type=typ
            Difficulty=lvl
            ob.save()
            data = {}
            print("Exception: ",ex)
            data["res"] = "Question Paper Updated"
        print (data)
        return JsonResponse(data,safe=False)
    else:
        data={}
        data["res"] = "Answer Should be in options!!"
        print (data)
        return JsonResponse(data,safe=False)
        
def examinerUpdQP(request):
    ob12 = User.objects.get(email = "admin@admin.com")
    e = request.GET.get("exam")
    typ=request.GET.get("typ")
    lvl=request.GET.get("lvl")
    e = e.replace("(", "")
    e = e.replace("'", "")
    e = e.replace(")", "")
    t = request.GET.get("time")
    t = t.replace("(", "")
    t = t.replace("'", "")
    t = t.replace(")", "")
    f = request.GET.get("fee")
    f = f.replace("(", "")
    f = f.replace("'", "")
    f = f.replace(")", "")
    rules = request.GET.get("rules")
    rules = rules.replace("(", "")
    rules = rules.replace("'", "")
    rules = rules.replace(")", "")
    rules = rules.replace("\n",";")
    que = request.GET.get("que")
    que = que.replace("(", "")
    que = que.replace("'", "")
    que = que.replace(")", "")
    que = que.replace("\n",";")
    opt1 = request.GET.get("opt1")
    opt1 = opt1.replace("(", "")
    opt1 = opt1.replace("'", "")
    opt1 = opt1.replace(")", "")
    opt1 = opt1.replace("\n",";")
    opt2 = request.GET.get("opt2")
    opt2 = opt2.replace("(", "")
    opt2 = opt2.replace("'", "")
    opt2 = opt2.replace(")", "")
    opt2 = opt2.replace("\n",";")
    opt3 = request.GET.get("opt3")
    opt3 = opt3.replace("(", "")
    opt3 = opt3.replace("'", "")
    opt3 = opt3.replace(")", "")
    opt3 = opt3.replace("\n",";")
    opt4 = request.GET.get("opt4")
    opt4 = opt4.replace("(", "")
    opt4 = opt4.replace("'", "")
    opt4 = opt4.replace(")", "")
    opt4 = opt4.replace("\n",";")
    ans = request.GET.get("answers")
    ans = ans.replace("(", "")
    ans = ans.replace("'", "")
    ans = ans.replace(")", "")
    ans = ans.replace("\n",";")
    print("Exam: ",e)
    print("Time: ",t)
    print("Fee: ",f)
    print("Rules: ",rules)
    print("Que: ",que)
    print("Opt1: ",opt1)
    print("Opt2: ",opt2)
    print("Opt3: ",opt3)
    print("Opt4: ",opt4)
    print("Ans: ",ans)
    qlist=que.split(";")
    qlist = list(filter(None, qlist))
    anslist=ans.split(";")
    anslist = list(filter(None, anslist))
    opt1list=opt1.split(";")
    opt1list = list(filter(None, opt1list))
    opt2list=opt2.split(";")
    opt2list = list(filter(None, opt2list))
    opt3list=opt3.split(";")
    opt3list = list(filter(None, opt3list))
    opt4list=opt4.split(";")
    opt4list = list(filter(None, opt4list))
    print("anslist",anslist)
    print("opt1list",opt1list)
    print("opt2list",opt2list)
    
    k=0
    for i in range(len(qlist)):
        allopt=[]
        allopt.append(opt1list[i])
        allopt.append(opt2list[i])
        allopt.append(opt3list[i])
        allopt.append(opt4list[i])
        print(allopt)
        print(anslist[i])
        if (anslist[i] not in allopt):
            k=1
            break
            
    if(k==0) :
            print(rules)
            print(que)
            print(opt1)
            print(opt2)
            print(opt3)
            print(opt4)
            ob1=exams.objects.get(name = e)
            ob1.fee=f
            ob1.timeDuration=t
            ob1.save()
            ob=QPExams.objects.get(name = e)
            ob.fee = f
            ob.timeDuration = t
            ob.rules = rules
            ob.que = que
            ob.opt1 = opt1
            ob.opt2 = opt2
            ob.opt3 = opt3
            ob.opt4 = opt4
            ob.ans = ans
            ob.Type=typ
            ob.Difficulty=lvl
            ob.save()
            data = {}
            data["res"] = "Question Paper Updated"
            print (data)
            return JsonResponse(data,safe=False)
    else:
        data={}
        data["res"] = "Answer Should be in options!!"
        print (data)
        return JsonResponse(data,safe=False)
def mcq(request):
    name= request.POST.get("name")
    etime = request.POST.get("time")
    efee = request.POST.get("fee")
    ob = QPExams.objects.get(name = name)
    rules = str(ob.rules).split(";")
    que = str(ob.que).split(";")
    opt1 = str(ob.opt1).split(";")
    opt2 = str(ob.opt2).split(";")
    opt3 = str(ob.opt3).split(";")
    opt4 = str(ob.opt4).split(";")
    ans = str(ob.ans).split(";")
    val = []
    for i in range(len(que)-1):
        val.append([que[i], opt1[i], opt2[i], opt3[i], opt4[i], ans[i]])
    
    user_data=User.objects.get(email=request.session["user"])
    return render(request, 'qp/mcq.html', {"data":ob, "rules":rules[:-1], "questions":";".join(que), "que":val, "exam":name, "name":user_data.first_name})

def admineditExam(request):
    print("Editing")
    name= request.POST.get("name")
    etime = request.POST.get("time")
    efee = request.POST.get("fee")
    etyp = request.POST.get("etyp")
    elvl = request.POST.get("elvl")
    
    ob = exams.objects.get(name = name)
    ob.name = name
    ob.timeDuration = etime
    ob.fee = efee
    ob.Type=etyp
    ob.Difficulty=elvl
    ob.save()
    return HttpResponse("<script>alert('Successfully edited the Exam');window.location.href=/examinerAddExam/;</script>")

def admindeleteExam(request):
    print("Editing")
    name= request.POST.get("name")
    etime = request.POST.get("time")
    efee = request.POST.get("fee")
    
    ob = exams.objects.get(name = name)
    ob1 = QPExams.objects.get(name = name)
    ob.delete()
    ob1.delete()
    return HttpResponse("<script>alert('Successfully deleted the Exam');window.location.href=/examinerAddExam/;</script>")


def adminmcq(request):
    name= request.POST.get("name")
    etime = request.POST.get("time")
    efee = request.POST.get("fee")
    ob = QPExams.objects.get(name = name)
    rules = str(ob.rules).split(";")
    que = str(ob.que).split(";")
    opt1 = str(ob.opt1).split(";")
    opt2 = str(ob.opt2).split(";")
    opt3 = str(ob.opt3).split(";")
    opt4 = str(ob.opt4).split(";")
    ans = str(ob.ans).split(";")
    val = []
    for i in range(len(que)-1):
        val.append([que[i], opt1[i], opt2[i], opt3[i], opt4[i], ans[i]])
    
    user_data=User.objects.get(email=request.session["user"])
    return render(request, 'qp/mcq.html', {"data":ob, "rules":rules[:-1], "questions":";".join(que), "que":val, "exam":name, "name":user_data.first_name})


def otppage(request):
    print(request.session["otp"])
    return render(request, 'users/otppage.html', {})

def verifyotp(request):
    global useremail, passval
    if request.method=="POST":
        p=request.POST.get("password")
        print(request.session["otp"], request.session["user"], p)
        
        if str(request.session["otp"])==str(p):
             return HttpResponse("<script>alert('Welcome User');window.location.href=/userhome/;</script>")

            
        return HttpResponse("<script>alert('Please give correct otp');window.location.href=/loginpage/;</script>")

def examinerExamsScored(request):
    exlst=[]
    ap=exams.objects.all()
    ap1=examscore.objects.all()
    for i in ap1:
        if i.name not in exlst:
            exlst.append(i.name)
    print(exlst)
    payc = examscore.objects.all()
    oe = QPExams.objects.all()
    ap2=User.objects.filter(is_superuser=0)
    return render(request,'adminWeb/examScore.html',{"exams":ap, "exams1": ap1, "excount": str(oe.count()), "paycount": str(payc.count()), "usr": ap2,"exlst":exlst})

def examinerViewUser(request):
    ap=exams.objects.all()
    ap1=User.objects.filter(is_superuser=0)
    payc = examscore.objects.all()
    oe = QPExams.objects.all()
    return render(request,'adminWeb/viewUsers.html',{"exams":ap, "users": ap1, "excount": str(oe.count()), "paycount": str(payc.count())})


def reportForOne(request):
    try:
        name = request.POST.get("name")
        uname = request.POST.get("username")
        print("-->",name," * ",uname)
        payc = examscore.objects.get(name=name, username=uname)
        t = "Examination Name: "+str(payc.name)+"\n\n"+"Examination Fee: "+str(payc.fee)+"\n\n"+"Time Duration of Exam: "+str(payc.timeDuration)+"\n\n"+"Score Obtained in the Exam: "+str(payc.scr)+"\n\n"
        usr = User.objects.get(email=uname)
        filename = str(usr.first_name)+".txt"
        doj=str(usr.date_joined)
        split_string = doj.split(".", 1)
        substring = split_string[0]
        r = "User Details"+"\n\n"+"User Name: "+str(usr.first_name)+"\n\n"+"Email: "+str(usr.email)+"\n\n"+"Mobile: "+str(usr.last_name)+"\n\n"+"User Joined on: "+substring
        disp_cont=t+"\n\n"+r+"\n\n\t\tGenerated using Online Examination App"
        response = HttpResponse(disp_cont, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response
    except Exception as ex:
        print("Exception: "+str(ex))
        return HttpResponse("<script>alert('Some errors occured');window.location.href=/examinerExamsScored/;</script>")

def studReport(request):
    try:
        email = request.POST.get("usersel")
        print("-->",email)
        payc = examscore.objects.filter(username=email)
        t, r = "", ""
        for i in payc:
            usr = User.objects.get(email=i.username)
            doj=str(usr.date_joined)
            split_string = doj.split(".", 1)
            substring = split_string[0]
            t += "Examination Name: "+str(i.name)+"\n\n"+"Examination Fee: "+str(i.fee)+"\n\n"+"Time Duration of Exam: "+str(i.timeDuration)+"\n\n"+"Score Obtained in the Exam: "+str(i.scr)+"\n\n"
            t += "-------------------******************------------------------\n\n\n"
        r+= "User Details"+"\n\n"+"User Name: "+str(usr.first_name)+"\n\n"+"Email: "+str(usr.email)+"\n\n"+"Mobile: "+str(usr.last_name)+"\n\n"+"User Joined on: "+substring+"\n\n"
        r += "\n\n ------------------------------------------------------------------------- \n\n"
        disp_cont=r+"\n\n"+t+"\n\n\t\tGenerated using Online Examination App"
        filename = str(usr.first_name)+" report.txt"
        response = HttpResponse(disp_cont, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response
    except Exception as ex:
        print("Exception: "+str(ex))
        return HttpResponse("<script>alert('Some errors occured');window.location.href=/examinerExamsScored/;</script>")

def examReport(request):
    try:
        ex = request.POST.get("examsel")
        print("-->",ex)
        payc = examscore.objects.filter(name=ex)
        print(payc[0].name)
        t, r = "", ""
        t += "Examination Name: "+str(payc[0].name)+"\n\n"+"Examination Fee: "+str(payc[0].fee)+"\n\n"+"Time Duration of Exam: "+str(payc[0].timeDuration)+"\n\n"
        t += "-------------------******************------------------------\n\n\n"
        for i in payc:
            usr = User.objects.get(email=i.username)
            doj=str(usr.date_joined)
            split_string = doj.split(".", 1)
            substring = split_string[0]
            t+= "User Details"+"\n\n"+"User Name: "+str(usr.first_name)+"\n\n"+"Email: "+str(usr.email)+"\n\n"+"Mobile: "+str(usr.last_name)+"\n\n"+"User Joined on: "+substring+"\n\n"+"Score Obtained in the Exam: "+str(i.scr)+"\n\n"
            t += "\n\n ------------------------------------------------------------------------- \n\n"
        disp_cont=t+"\n\n"+r+"\n\n\t\tGenerated using Online Examination App"
        filename = str(ex)+" report.txt"
        response = HttpResponse(disp_cont, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response
    except Exception as ex:
        print("Exception: "+str(ex))
        return HttpResponse("<script>alert('Some errors occured');window.location.href=/examinerExamsScored/;</script>")


def reportForAll(request):
    try:
        payc = examscore.objects.all()
        t, r = "", ""
        for i in payc:
            t += "Examination Name: "+str(i.name)+"\n\n"+"Examination Fee: "+str(i.fee)+"\n\n"+"Time Duration of Exam: "+str(i.timeDuration)+"\n\n"+"Score Obtained in the Exam: "+str(i.scr)+"\n\n"
            
            usr = User.objects.get(email=i.username)
            doj=str(usr.date_joined)
            split_string = doj.split(".", 1)
            substring = split_string[0]
            t+= "User Details"+"\n\n"+"User Name: "+str(usr.first_name)+"\n\n"+"Email: "+str(usr.email)+"\n\n"+"Mobile: "+str(usr.last_name)+"\n\n"+"User Joined on: "+substring+"\n\n"
            t+= "\n\n ------------------------------------------------------------------------- \n\n"
            disp_cont=t+"\n\n"+r+"\n\n\t\tGenerated using Online Examination App"
        filename = "allreport.txt"
        response = HttpResponse(disp_cont, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response
    except Exception as ex:
        print("Exception: "+str(ex))
        return HttpResponse("<script>alert('Some errors occured');window.location.href=/examinerExamsScored/;</script>")




def examinerExamsPayments(request):
    ap=exams.objects.all()
    ap1=examscore.objects.all()
    payc = examscore.objects.all()
    oe = QPExams.objects.all()
    return render(request,'adminWeb/examPayment.html',{"exams":ap, "exams1": ap1, "excount": str(oe.count()), "paycount": str(payc.count())})

def userApproving(request):
    try:
        name = request.POST.get("name")
        em = request.POST.get("email")
        ob = User.objects.get(first_name = name,
                    email = em)
        ob.is_active = 1
        ob.save()
        return HttpResponse("<script>alert('Successfully Approved');window.location.href=/examinerViewUser/;</script>")
    except Exception as ex:
        print("Exception: ", ex)
        return HttpResponse("<script>alert('Some errors occured');window.location.href=/examinerViewUser/;</script>")


def userBlocking(request):
    try:
        name = request.POST.get("name")
        em = request.POST.get("email")
        ob = User.objects.get(first_name = name,
                    email = em)
        ob.is_active = 0
        ob.save()
        return HttpResponse("<script>alert('Successfully Blocked');window.location.href=/examinerViewUser/;</script>")
    except Exception as ex:
        print("Exception: ", ex)
        return HttpResponse("<script>alert('Some errors occured');window.location.href=/examinerViewUser/;</script>")


def examinerAdding(request):
    try:
        ename = request.POST.get("examname")
        etime = request.POST.get("time")
        efee = request.POST.get("fee")
        etyp = request.POST.get("etyp")
        elvl = request.POST.get("elvl")
        print(etyp,elvl)
        ob = exams(name = ename,
                    fee = efee,
                    timeDuration = etime,Type=etyp,Difficulty=elvl).save()
        return HttpResponse("<script>alert('Successfully Added');window.location.href=/examinerAddExam/;</script>")
    except Exception as ex:
        print("Exception: ", ex)
        return HttpResponse("<script>alert('Cannot add same exams twise');window.location.href=/examinerAddExam/;</script>")

def examinerAddQP(request):
    l1=[]
    l2=[]
    l3=[]
    ob12 = User.objects.get(email = "admin@admin.com")
    ob = exams.objects.all()
    ob2 = QPExams.objects.all()
    for i in ob:
        l1.append(i.name)
    for j in ob2:
        l2.append(j.name)
    print(l1,l2)
    for i in l1:
        if i not in l2:
            l3.append(i)
    print(l3)
    return render(request, 'adminWeb/addQuestionPaper.html', {"exams":ob, "name":ob12.first_name,"lex":l3})
def examinerUploadQP(request):
    l1=[]
    l2=[]
    l3=[]
    ob12 = User.objects.get(email = "admin@admin.com")
    ob = exams.objects.all()
    ob2 = QPExams.objects.all()
    for i in ob:
        l1.append(i.name)
    for j in ob2:
        l2.append(j.name)
    print(l1,l2)
    for i in l1:
        if i not in l2:
            l3.append(i)
    print(l3)
    return render(request, 'adminWeb/fileupload.html', {"exams":ob, "name":ob12.first_name,"lex":l3})
def uploadFile(request):
    s = request.FILES["img"]
    exname=request.POST.get("name")
    ob=exams.objects.get(name=exname)
    f=ob.fee
    td=ob.timeDuration
    tp=ob.Type
    diff=ob.Difficulty
    print(s.name,exname,f,td,tp,diff)
    fs = FileSystemStorage()
    fs.save(s.name, s)
    
    print("saved")
    import pandas as pd
    try:
        df = pd.read_csv(str(s.name))
        qst=df["Question"]
        opt1=df["opt1"]
        opt2=df["opt2"]
        opt3=df["opt3"]
        opt4=df["opt4"]
        ans=df["ans"]
        rule=df["rules"]
        qlst=[]
        o1=[]
        o2=[]
        o3=[]
        o4=[]
        an=[]
        rl=[]

        for i in range(len(qst)):
            qlst.append(qst[i])
            o1.append(opt1[i])
            o2.append(opt2[i])
            o3.append(opt3[i])
            o4.append(opt4[i])
            an.append(ans[i])
            rl.append(rule[i])
        rl = [x for x in rl if str(x) != 'nan']
        allqst=';'.join(qlst)
        allo1=';'.join(o1)
        allo2=';'.join(o2)
        allo3=';'.join(o3)
        allo4=';'.join(o4)
        allans=';'.join(an)
        allrule=';'.join(rl)
        print(allqst)
        print(allo1)
        print(allo2)
        print(allo3)
        print(allo4)
        print(allans)
        print(allrule)
        try:
                obe=QPExams(
                    name = exname,
                    fee = f,
                    timeDuration = td,
                    rules = allrule+";",
                    que = allqst+";",
                    opt1 = allo1+";",
                    opt2 = allo2+";",
                    opt3 = allo3+";",
                    opt4 = allo4+";",
                    ans = allans+";",
                    Type=tp,
                    Difficulty=diff
                    ).save()
                return HttpResponse("<script>alert('Successfully added');window.location.href=/examinerUploadQP/;</script>")
        except Exception as ex:
                print(ex)
                return HttpResponse("<script>alert('Exam already exist');window.location.href=/examinerUploadQP/;</script>")
    except Exception as ec:
        print(ec)
        return HttpResponse("<script>alert('Invalid File or incorrect File Format');window.location.href=/examinerUploadQP/;</script>")
        

def examinerUpdateQP(request):
    ob12 = User.objects.get(email = "admin@admin.com")
    ob = exams.objects.all()
    return render(request, 'adminWeb/updateQuestionPaper.html', {"exams":ob, "name":ob12.first_name})

def userAttemptQP(request):
    name= request.POST.get("name")
    etime = request.POST.get("time")
    efee = request.POST.get("fee")
    usernm = request.session["user"]
    obj1=payment.objects.get(name=usernm)
    amnt=obj1.amount
    print(amnt)
    print(efee,type(efee))
    blnc=amnt-int(efee)
    print(blnc,type(blnc))
    if(blnc<0):
        return HttpResponse("<script>alert('You Have no account balance to attempt this exam!!');window.location.href=/examsviews/;</script>")
    else:    
        print("UAQ-->",name,etime,efee)
        try:
            ob = examscore.objects.get(name = name, username = request.session["user"])
            return HttpResponse("<script>alert('Already attempted the exam');window.location.href=/examsviews/;</script>")
        except Exception as ex:
            
            print("Ex: ",ex)
            obj1.amount=blnc
            obj1.save()
            ob = QPExams.objects.get(name = name)
            rules = str(ob.rules).split(";")
            que = str(ob.que).split(";")
            opt1 = str(ob.opt1).split(";")
            opt2 = str(ob.opt2).split(";")
            opt3 = str(ob.opt3).split(";")
            opt4 = str(ob.opt4).split(";")
            ans = str(ob.ans).split(";")
            
            val = []
            for i in range(len(que)-1):
                val.append([que[i], opt1[i], opt2[i], opt3[i], opt4[i], ans[i]])
            
            user_data=User.objects.get(email=request.session["user"])
            print(user_data.first_name)
            return render(request, 'users/mcq.html', {"data":ob, "rules":rules[:-1], "questions":";".join(que), "exam":name, "que":val, "name":user_data.first_name,})
    
def login(request):
    return render(request,'users/login.html',{})

def loginpage(request):
    return render(request,'users/login.html',{})

def login_check(request):
    print ("login_check(request):")
    print(request.POST)
    if request.method=="POST":
        u=request.POST.get("username")
        p=request.POST.get("password")
        print ("in login page:",u,"::::",p)
        try:
            user_data=User.objects.get(email=u)
            request.session["user"] = u
            if user_data.is_superuser and p==user_data.password:
                
                return HttpResponse("<script>alert('Welcome Admin');window.location.href=/examinerHome/;</script>")
            if p==user_data.password:
                if user_data.is_active==0:
                    return HttpResponse("<script>alert('You have been blocked by the Admin');window.location.href=/loginpage/;</script>")
                    
                ranstr = ""
                for i in range(6):
                    ranstr += str(random.randrange(0,10))
                request.session["otp"] = ranstr
                print("OTP: ",ranstr)
                try:
                    account = "ACac19c9213f743e404c330c62651fb6ba"
                    token = "bd5af0945cbc28374039110919ef3d2d"
                    client = Client(account, token)

                    message = client.messages.create(to=user_data.last_name, from_="+18084270712", 
                                                     body="OTP: "+ranstr)
                    print(message)
                except Exception as ex:
                    print("Cannot send SMS ",ex)
                try:
##                    import smtplib
##                    server=smtplib.SMTP('smtp.gmail.com',587)
##                    server.ehlo()
##                    server.starttls()
##                    server.login("jobinthomasalummoottil@mca.ajce.in","jobinthomasalummoottil99")
##                    server.sendmail("jobinthomasalummoottil@mca.ajce.in",user_data.email,"OTP: "+ranstr)
##                    server.close()
                        subject = 'USER APPROVAL'
                        message = "Your OTP for verification is  :"+ranstr
                        print(ranstr)
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [user_data.email]
                        send_mail( subject, message, email_from, recipient_list )
                        print("email send successfully...")
                except:
                    print("Cannot send Email")
                return HttpResponse("<script>alert('OTP sent to your mobile and email');window.location.href=/otppage/;</script>")
            return HttpResponse("<script>alert('Please register first');window.location.href=/loginpage/;</script>")
        except Exception as ex:
            print("Exception: ",ex)
            return HttpResponse("<script>alert('Please register first');window.location.href=/loginpage/;</script>")


def certificateView(request):
    global data
    if(int(data["marks"])/int(data["total"])*100)>50.0:
        res = "Passed the Exam"
        desc = "Congratulations."
    else:
        res = "Failed the Exam"
        desc = "Better luck next time."
    scr = str(data["marks"])+"/"+str(data["total"])
    from datetime import datetime
    now = datetime.now()
    us=request.session["user"]
    obc=User.objects.get(email=us)
    usname=obc.first_name
    print("now =", now)
    dt = now.strftime("%d/%m/%Y")
    tm = now.strftime("%H:%M:%S")
    print("date and time =", dt, tm)
    ob=examscore(
            name = data["name"],
            fee = data["fee"],
            timeDuration = data["time"],
            scr = scr,
            username = request.session["user"],
            cdate = str(dt),
            ctime = str(tm)
            ).save()
    return render(request, 'users/certificate.html', {"res": res, "name": request.session["user"], "scr": "Score Obtained: "+scr, "desc": desc,"usname":usname})


    
def register(request):
    name= request.POST.get("name")
    email= request.POST.get("email")
    mob = request.POST.get("mob")
    password1= request.POST.get("password1")
    password2= request.POST.get("password2")
    print ("name,email,paswd",name,email,password1,password2,request)
    if password1!=password2:
        return HttpResponse("<script>alert('Password Not Same');window.location.href=/loginpage/;</script>")
    try:
        obj=User(
                first_name=name.upper(),email=email,username=email,password=password1, last_name=mob
                )
        obj.save()
        obj1=payment(name=email)
        obj1.save()
        print("registerd")
        return HttpResponse("<script>alert('Registration Successful');window.location.href=/loginpage/;</script>")
    except Exception as ex:
        print("Exception: ",ex)
        return HttpResponse("<script>alert('Error Occured. Duplicate Entry Found for Email');window.location.href=/loginpage/;</script>")

def reset_password(request):
    email= request.POST.get("email")
    try:
        user_data=User.objects.get(email=email)
##        email = EmailMessage('Password for your account', 'Your Account Password is '+str(user_data.password), to=[str(email)])
##        email.send()
        subject = 'Forgot Password'
        message = 'Your Account Password is '+str(user_data.password)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [str(email)]
        send_mail( subject, message, email_from, recipient_list )
        print("email send successfully...")
        return HttpResponse("<script>alert('Email Sent Successful');window.location.href=/loginpage/;</script>")
    except Exception as ex:
        print("Exception: ",ex)
        return HttpResponse("<script>alert('Error in Sending Email. Might need to Turn on App Access in Settings(GMail) or Not Registered yet');window.location.href=/loginpage/;</script>")

def userhome(request):
    return render(request,'users/user_home.html',{})

def showexam(request):
    etyp= request.POST.get("etyp")
    elvl= request.POST.get("elvl")
    print(etyp,elvl)
    if(etyp=="All" and elvl=="All"):
        
        ap=QPExams.objects.all()
        cnt=ap.count()
        if(cnt!=0):
            return render(request,'users/user_exams.html',{"exams":ap})
        else:
            return HttpResponse("<script>alert('No Exams Found');window.location.href=/examsviews/;</script>")
      
    elif(etyp=="All" and elvl!="All"):
        try:
            ap=QPExams.objects.filter(Difficulty=elvl)
            cnt=ap.count()
            if(cnt!=0):
                return render(request,'users/user_exams.html',{"exams":ap})
            else:
                return HttpResponse("<script>alert('No Exams Found');window.location.href=/examsviews/;</script>")
        except Exception as e:
            print(e)
            return HttpResponse("<script>alert('No Exams Found');window.location.href=/examsviews/;</script>")
    elif(etyp!="All" and elvl=="All"):
        try:
            ap=QPExams.objects.filter(Type=etyp)
            cnt=ap.count()
            if(cnt!=0):
                return render(request,'users/user_exams.html',{"exams":ap})
            else:
                return HttpResponse("<script>alert('No Exams Found');window.location.href=/examsviews/;</script>")
        except Exception as e:
            print(e)
            return HttpResponse("<script>alert('No Exams Found');window.location.href=/examsviews/;</script>")
    else:
        try:
            ap=QPExams.objects.filter(Type=etyp,Difficulty=elvl)
            cnt=ap.count()
            if(cnt!=0):
                return render(request,'users/user_exams.html',{"exams":ap})
            else:
                return HttpResponse("<script>alert('No Exams Found');window.location.href=/examsviews/;</script>")
        except Exception as e:
            print(e)
            return HttpResponse("<script>alert('No Exams Found');window.location.href=/examsviews/;</script>")
##    ap=QPExams.objects.all()
##    return render(request,'users/user_exams.html',{"exams":ap})
def examsviews(request):
    return render(request,'users/chooseexam.html',{})
def examsScored(request):
    usernm = request.session["user"]
    ap=examscore.objects.filter(username=usernm)
    return render(request,'users/user_exams_scores.html',{"exams":ap})

def userpay(request):
    usernm = request.session["user"]
    ob=payment.objects.get(name=usernm)
    print(ob.amount)
    return render(request,'users/user_payment.html',{"data":ob})
def addpay(request):
    usernm = request.session["user"]
    ob=payment.objects.get(name=usernm)
    amnt=ob.amount
    pay= request.GET.get("pay")
    total=int(pay)+amnt
    ob.amount=total
    ob.save()
    return HttpResponse("yes")
    

def adminexamsviews(request):
    ap=QPExams.objects.all()
    payc = examscore.objects.all()
    oe = QPExams.objects.all()
    return render(request,'adminWeb/viewExam.html',{"exams":ap, "excount": str(oe.count()), "paycount": str(payc.count())})



def payments(request):
    name= request.POST.get("name")
    etime = request.POST.get("time")
    efee = request.POST.get("fee")
    
    return render(request,'users/payments.html',{"name":name, "time":etime, "fee":efee})
