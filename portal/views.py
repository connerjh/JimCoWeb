from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
import jimcodb

def index(request):

    print(request.user)

    if request.user.is_authenticated:

        user = jimcodb.get_individual_by_user(request.user)

        template = loader.get_template('portal/index.html')
        return HttpResponse(template.render({}, request))

    else:

        return HttpResponseRedirect('/login/')



