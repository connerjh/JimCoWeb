from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from . import jimcodb

def index(request):

    print(request.user)

    if request.user.is_authenticated:

        print('User Id {}: '.format(request.user.username))

        user = jimcodb.get_individual_by_user(request.user.username)

        print('User {}: '.format(user['UserName']))

        context = {
            'UserId': user['UserName'],
            'FullName': user['FirstName'] + " " + user['LastName'],
        }
        template = loader.get_template('portal/index.html')
        return HttpResponse(template.render(context, request))

    else:

        return HttpResponseRedirect('/login/')

def ccp(request):

        template = loader.get_template('portal/ccp.html')
        return HttpResponse(template.render({}, request))




