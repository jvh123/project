from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.forms.forms import NON_FIELD_ERRORS
from django.conf import settings
from django.core.urlresolvers import reverse
from .forms import SubscrpberForm
from .models import Subscrpber
# Create your views here.
def subscriber_new(request,template='subscribers/subscriber_new.html'):
    if request.method=='POST':
        form=SubscrpberForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email=form.cleaned_data['email']
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            user=User(username=username,email=email,first_name=first_name,last_name=last_name)
            user.set_password(password)
            user.save()
            call_number=form.cleaned_data['call_number']
            event1=form.cleaned_data['event1']
            event2 = form.cleaned_data['event2']
            event3 = form.cleaned_data['event3']
            email_check = form.cleaned_data['email_check']
            sub=Subscrpber(call_number=call_number,event1=event1,
                           event2=event2,event3=event3,email_check=email_check,user_rec=user)
            sub.save()
            #자동인증
            a_u=authenticate(username=username,password=password)
            if a_u is not None:
                if a_u.is_active:
                    login(request,a_u)
                    return HttpResponseRedirect(reverse('main'))
                else:
                    return HttpResponseRedirect(
                        reverse('django.contrib.auth.views.login')
                    )
            else:
                return HttpResponseRedirect(reverse('sub_new'))
    else:
        form = SubscrpberForm()
    return render(request,template,{'form':form})