from django import dispatch
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import *


# @login_required
# def redirect_admin(request):
#     if request.user.is_superuser:
#         return redirect('/admin/')
    

# Create your views here.
class IndexView(View):
    def get(self, request):
        context = {'message':'HOLA MUNDO'}
        return render(request, 'base/index.html', context)


class SigninView(View):
    template_name = 'login/signin.html'
    users_to_signin =  User.objects.all()[:3]

    def get(self, request):
        form = AuthenticationForm()
        context = {
            'form': form,
            'users_to_signin': self.users_to_signin
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        print(form)
        print(request.POST)
        print(request.POST['username'])
        print(form.cleaned_data.get('username'))
        print(request.POST['password'])
        print(form.is_valid())
        if form.is_valid():
            authenticated_user = authenticate(
                request, 
                username=form.cleaned_data.get('username'), 
                password=form.cleaned_data.get('password'))
                # username=request.POST['username'], 
                # password=request.POST['password'])
            if authenticated_user is not None:
                login(request, authenticated_user)
                # authenticated_user.save()
                return redirect('index')
            else:
                form.add_error(None, "Invalid username or password")

            form.add_error('password', "Incorrect password")
        return render(request, self.template_name, {'form': form})


from django.http import HttpResponse

def debug_view(request):
    if request.user.is_authenticated:
        return HttpResponse(f"User: {request.user.username}, Is staff: {request.user.is_staff}")
    else:
        return HttpResponse("User is not authenticated")
    
class SignupView(View):
    template_name = 'login/signup.html'

    def get(self, request):
        # form = UserCreationForm()
        form = CustomUserAndProfileForm()
        # form_profile = CustomProfileCreationForm()
        context = {
            'form': form,
            # 'form_profile': form_profile
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = CustomUserAndProfileForm(request.POST)
        
        print(request.POST)
        print(form)
        
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user)
            return redirect('index')
        else:
            return render(request, self.template_name, {'form': form})
        
        # if not form.is_valid():
        #     return render(request, 'base/signup.html', {'form': form})

        # user = User.objects.create_user(
        #     # username=form.cleaned_data['username'],
        #     # email=form.cleaned_data['email'],
        #     # password=form.cleaned_data['password']
        #     username=form.cleaned_data.get('username'),
        #     email=form.cleaned_data.get('email'),
        #     password=form.cleaned_data.get('password')
        # )
        # print(user)

        # profile = Profile.objects.get_or_create(
        #     # rut=form.cleaned_data['rut'],
        #     # phone=form.cleaned_data['phone']
        #     rut=form.cleaned_data.get('rut'),
        #     phone=form.cleaned_data.get('phone')
        # )
        # print(profile)
        # user.save()
        # profile.save()
        # login(request, user)

        # return redirect('index')

@method_decorator(login_required, name='dispatch')
class SignOutView(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect('signin')



# TICKETS

class TicketListView(View):
    template_name = 'tickets/tickets.html'
    def get(self, request):
        tickets = Ticket.objects.all()
        context = {
            'tickets': tickets,
            'is_update_view': False
        }
        return render(request, self.template_name, context)
    


# @method_decorator(login_required, name='dispatch')

class CreateTicketView(View):
    template_name = 'tickets/ticket_create.html'
    def get(self, request):
        form = OpeningTicketForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = OpeningTicketForm(request.POST)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            opening_agent = request.user.profile
            ticket = form.save(commit=False)
            ticket.opening_agent = opening_agent
            form.save()
            return redirect('tickets')
        else:
            form.add_error(None, "There was an error with your submission")  
            context = {
                'form': form
            }
            return render(request, self.template_name, context)
        


class UpdateTicketView(View):
    template_name = 'tickets/ticket_update.html'
    # template_name = 'tickets/tickets.html'
    def get_ticket(self, id):
        return get_object_or_404(Ticket, id=id)
    
    def get(self, request, id):
        ticket = self.get_ticket(id)
        form = UpdateTicketForm(instance=ticket)
        context = {
            'form': form,
            'ticket': ticket,
            'is_update_view': True
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        ticket = self.get_ticket(id)
        form = UpdateTicketForm(request.POST, instance=ticket)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            # opening_agent = request.user.profile
            # ticket = form.save(commit=False)
            # ticket.opening_agent = opening_agent
            form.save()
            return redirect('tickets')
        else:
            form.add_error(None, "There was an error with your submission")  
            context = {
                'form': form,
                'ticket': ticket,
                'is_update_view': True
            }
            return render(request, self.template_name, context)




# HTMX
class SearchTicketsView(View):
    template_name = 'tickets/partials/ticket_search_result.html'
    def get(self, request):
        query = request.GET.get('ticket-search', '').strip()
        print(f"Query: '{query}'")
        
        if query:
            if query.isdigit():
                tickets = Ticket.objects.filter(id=query)
                print(f"Tickets found: {tickets}")
            else:
                tickets = Ticket.objects.none()
        else:
            tickets = Ticket.objects.all()  # Devuelve todos los tickets si la consulta está vacía
            print("Query was empty, returning all tickets")
        
        print(f"Tickets to render: {tickets}")
        return render(request, self.template_name, {'tickets': tickets})
    
    # def post(self, request):
    #     print(f"Received POST request with data: {request.POST}")
    #     query = request.POST.get('ticket-search','').strip()
    #     print(f"query: ", query)

    #     if query:
    #         if query.isdigit():
    #             tickets = Ticket.objects.filter(id=query)
    #             print("ticket", {tickets})
    #         else:
    #             tickets = Ticket.objects.none()
    #     else:
    #         tickets = Ticket.objects.all()
    #     print(f"Tickets to render: {tickets}")
    #     return render(request, self.template_name, {'tickets':tickets})
