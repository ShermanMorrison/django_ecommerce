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


def sign_in(request):
    user = None
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            results = User.objects.filter(email=form.cleaned_data['email'])
            if len(results) == 1:
                print "Found him!"
                if results[0].check_password(form.cleaned_data['password']):
                    print "We good!"
                    request.session['user'] = results[0].pk
                    return HttpResponseRedirect('/')
                print "No good"
            else:
                form.addError('Incorrect email address or password')
        else:
            form.addError('Invalid email address or password')
    else:
        form = SigninForm()

    print form.non_field_errors()

    return render_to_response(
        'sign_in.html',
        {
            'form': form,
            'user': user
        },
        context_instance=RequestContext(request)
    )


def sign_out(request):
    del request.session['user']
    return HttpResponseRedirect('/')

#
# def edit(request):
#     return HttpResponseRedirect('/')


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
                print request.session['user']
                return HttpResponseRedirect('/')
    else:
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


def edit(request):
    uid = request.session.get('user')

    if uid is None:
        return HttpResponseRedirect('/')

    print "uid = " + str(uid)
    user = User.objects.get(pk=uid)

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            customer = stripe.Customer.retrieve(user.stripe_id)
            customer.card = form.cleaned_data['stripe_token']
            customer.save()

            user.last_4_digits = form.cleaned_data['last_4_digits']
            user.stripe_id = customer.id
            user.save()

            return HttpResponseRedirect('/')

    else:
        form = CardForm()

    return render_to_response(
        'edit.html',
        {
            'form': form,
            'publishable': settings.STRIPE_PUBLISHABLE,
            'soon': soon(),
            'months': range(1, 12),
            'years': range(2011, 2036)
        },
        context_instance=RequestContext(request)
    )
















