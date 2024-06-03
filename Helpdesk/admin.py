from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from .forms import *

# MODELOS ADMIN
# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False

# class UserAdmin(BaseUserAdmin):
#     inlines = (ProfileInline,)

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
# admin.site.register(Profile)


class PriorityAdmin(admin.ModelAdmin):
    list_display= [
        'id',
        'priority',
    ]
admin.site.register(Priority, PriorityAdmin)

class StatusAdmin(admin.ModelAdmin):
    list_display= [
        'id',
        'status',
    ]
admin.site.register(Status, StatusAdmin)    

class TypeAdmin(admin.ModelAdmin):
    list_display= [
        'id',
        'type',
    ]
admin.site.register(Type, TypeAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    list_display= [
        'id',
        'department',    
        ]
admin.site.register(Department, DepartmentAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'rut',
        'phone', 
        'department',
    ]
admin.site.register(Profile, ProfileAdmin)

    
class TicketAdmin(admin.ModelAdmin):
    # form = TicketAdminForm
    list_display=[
        'id',
        'customer',
        'get_opening_agent', 
        'get_closure_agent',
        'issue',
        'solution',
        'priority', 
        'type', 
        'status',
        'observation',
        'solution',
        'opening_date', 
        'closing_date', 
    ]
    # # Obtiene los agentes de apertura y cierre 
    # def get_opening_agents(self, obj):
    #     return "\n".join([p.user.username for p in obj.opening_agent.all()])
    
    # def get_closure_agents(self, obj):
    #     return "\n".join([p.user.username for p in obj.closure_agent.all()])

    # get_opening_agents.short_description = 'Agente apertura'
    # get_closure_agents.short_description = 'Agente Cierre'


    def get_opening_agent(self):
        return ", ".join([str(agent) for agent in self.opening_agent.all()])
    get_opening_agent.short_description = 'Opening Agent'

    def get_closure_agent(self):
        return ", ".join([str(agent) for agent in self.closure_agent.all()])
    get_closure_agent.short_description = 'Closure Agent'


admin.site.register(Ticket, TicketAdmin)

