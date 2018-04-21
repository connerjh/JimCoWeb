from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect


def index(request):

    print(request.user)

    if request.user.is_authenticated:

        template = loader.get_template('portal/index.html')
        return HttpResponse(template.render({}, request))

    else:

        return HttpResponseRedirect('/login/')



