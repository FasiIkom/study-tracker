from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'Maul',
        'class': 'XII-Science-3',
        'subject': 'Biology',
        'start_date': '23 January 2023',
        'progress': '80' 
    }

    return render(request, "main.html", context)