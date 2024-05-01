import datetime
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from main.forms import ProgressForm
from main.models import Progress
import json

@login_required(login_url='/login')
def show_main(request):
    progresses = Progress.objects.filter(user=request.user)
    context = {
        'name': request.user.username,
        'class': 'XII-Science-3',
        'number': '20',
        'progresses': progresses,
        'last_login': request.COOKIES['last_login'],
    }
    return render(request, "main.html", context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def create_progress(request):
    form = ProgressForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        progress = form.save(commit=False)
        progress.user = request.user
        progress.save()
        return redirect('main:show_main')
    context = {'form': form}
    return render(request, "create_progress.html", context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def show_xml(request):
    data = Progress.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Progress.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Progress.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Progress.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def edit_progress(request, id):
    progress = Progress.objects.get(pk = id)
    form = ProgressForm(request.POST or None, instance=progress)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))
    context = {'form': form}
    return render(request, "edit_progress.html", context)

def delete_progress(request, id):
    progress = Progress.objects.get(pk = id)
    progress.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
def add_progress_ajax(request):
    if request.method == 'POST':
        subject = request.POST.get("subject")
        start_Study = request.POST.get("start_Study")
        progress = request.POST.get("progress")
        catatan = request.POST.get("catatan")
        user = request.user

        new_progress = Progress(subject=subject, start_Study=start_Study, progress=progress, catatan=catatan, user=user)
        new_progress.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def create_progress_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)

        new_progress = Progress.objects.create(
            user = request.user,
            subject = data["subject"],
            start_Study = data["startStudy"],
            progress = int(data["progress"]),
            catatan = data["catatan"]
        )

        new_progress.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
