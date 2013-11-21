from django.shortcuts import render

# Create your views here.
def show(request, user_id):
	return render(request, 'account.html')