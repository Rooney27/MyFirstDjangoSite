from django.shortcuts import render
from django.views import View

# Create your views here.
class Home(View):
    def get(self, request):
        template_name = "main/main.html"
        return render(request, template_name)
