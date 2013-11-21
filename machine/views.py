from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    #messages.success(request, "Skadoosh! You've updated your profile!")
    #messages.info(request, 'Yo! There are new comments on your photo!')
    #messages.error(request, 'Doh! Something went wrong.')
    #messages.warning(request, 'Uh-oh. Your account expires in 3 days.')
	return render(request, 'machine.html')