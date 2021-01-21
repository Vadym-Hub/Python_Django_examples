from django.urls import path
from . import views


app_name = 'crm'

urlpatterns = [
    #  URL регистрации организации
    path('org-signup/', views.OrganisationCreateView.as_view(), name='organisation-create'),
    # path('landing/', views.LandingPageView.as_view(), name='landing-page'),

    path('', views.LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', views.LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', views.LeadDeleteView.as_view(), name='lead-delete'),
    path('<int:pk>/status/', views.LeadStatusUpdateView.as_view(), name='lead-status-update'),
    path('create/', views.LeadCreateView.as_view(), name='lead-create'),
    path('status/', views.LeadStatusListView.as_view(), name='status-list'),

    path('agent/', views.AgentListView.as_view(), name='agent-list'),
    path('agent/<int:pk>/', views.AgentDetailView.as_view(), name='agent-detail'),
    path('agent/<int:pk>/update/', views.AgentUpdateView.as_view(), name='agent-update'),
    path('agent/<int:pk>/delete/', views.AgentDeleteView.as_view(), name='agent-delete'),
    path('agent/create/', views.AgentCreateView.as_view(), name='agent-create'),
    path('agent/<int:pk>/assign-agent/', views.AgentAssignToLeadView.as_view(), name='assign-agent'),
]
