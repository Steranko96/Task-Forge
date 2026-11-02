from django.http import HttpResponse

def app_health_check(request):
       return HttpResponse('health check', content_type='text/plain', status=200)
