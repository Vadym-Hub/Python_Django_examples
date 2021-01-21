from django.contrib import admin

from .models import User, Lead, Agent, Organisation


admin.site.register(User)
admin.site.register(Organisation)
admin.site.register(Lead)
admin.site.register(Agent)
