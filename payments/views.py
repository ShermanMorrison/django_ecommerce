# Create your views here.
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from payments.forms import SigninForm, CardForm, UserForm
from payments.models import User
import django_ecommerce.settings as settings
import stripe
import datetime

stripe.api_key = settings.STRIPE_SECRET


def soon():
    soon = datetime.date.today() + datetime.timedelta(days=30)
    return {'month': soon.month, 'year': soon.year}


def sign_in():
    return HttpResponseRedirect('/')


def sign_out():
    return HttpResponseRedirect('/')


def edit():
    return HttpResponseRedirect('/')


def register(request):
    print "USERFORM = " + str(UserForm)
    user = None
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():

            # subscription billing

            print "YO!"
            print "STRIPE_PUBLISHABLE = " + str(settings.STRIPE_PUBLISHABLE)
            print "stripe_token = " + form.cleaned_data['stripe_token']
            customer = stripe.Customer.create(
                email=form.cleaned_data['email'],
                description=form.cleaned_data['name'],
                card=form.cleaned_data['stripe_token'],
                plan="gold",
            )



            user = User(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                last_4_digits=form.cleaned_data['last_4_digits'],
                stripe_id=customer.id,
            )

            user.set_password(form.cleaned_data['password'])

            try:
                user.save()
            except IntegrityError:
                print "Already a member bro!"
                form.addError(user.email + ' is already a member')
            else:
                print "Save user payment profile"
                request.session['user'] = user.pk
                return HttpResponseRedirect('/')
    else:
        print "Form wasn't valid bro!"
        form = UserForm()

    return render_to_response(
        'register.html',
        {
            'form': form,
            'months': range(1, 12),
            'publishable': settings.STRIPE_PUBLISHABLE,
            'soon': soon(),
            'user': user,
            'years': range(2011, 2036),
        },
        context_instance=RequestContext(request)
    )





















