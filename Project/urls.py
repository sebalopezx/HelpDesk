"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Helpdesk.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('redirect_admin/', redirect_admin, name='redirect_admin'),
    path('', IndexView.as_view(), name='index'),
    path('debug/', debug_view, name='debug'),
    # LOGIN
    path('signin/', SigninView.as_view(), name='signin'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('signout/', SignOutView.as_view(), name='signout'),
    # TICKETS
    path('tickets/', TicketListView.as_view(), name='tickets'),
    path('tickets/ticket_create/', CreateTicketView.as_view(), name='ticket_create'),
    path('tickets/ticket_update/<int:id>/', UpdateTicketView.as_view(), name='ticket_update'),


    # HTMX
    path('tickets/ticket-search/', SearchTicketsView.as_view(), name='ticket-search'),

]
