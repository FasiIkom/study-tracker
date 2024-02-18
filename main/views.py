from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from main.forms import ProgressForm
from main.models import Progress

def show_main(request):
    progresses = Progress.objects.all()
    context = {
        'name': 'Maul',
        'class': 'XII-Science-3',
        'number': '20',
        'progresses': progresses
    }

    return render(request, "main.html", context)

def create_progress(request):
    form = ProgressForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_progress.html", context)

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