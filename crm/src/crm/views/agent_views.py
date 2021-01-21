import random

from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views import generic

from ..models import Agent, Lead
from ..forms import AgentModelForm, AgentAssignToLeadForm
from ..mixins import OrganisorAndLoginRequiredMixin, AgentInOrganisationMixin


class AgentListView(OrganisorAndLoginRequiredMixin, AgentInOrganisationMixin, generic.ListView):
    """
    Обработчик вывода списка всех агентов из одной организации.
    """
    template_name = 'crm/agents/agent_list.html'
    paginate_by = 20


class AgentCreateView(OrganisorAndLoginRequiredMixin, AgentInOrganisationMixin, generic.CreateView):
    """
    Обработчик вывода формы для создания агентов конкретной организации.
    """
    template_name = 'crm/agents/agent_create_form.html'
    form_class = AgentModelForm
    success_url = reverse_lazy('crm:agent-list')

    random_password = random.randint(0, 1000000)  # Для автоматической установки пароля.

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f'{self.random_password}')
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.organisation
        )
        # Отправка email.
        send_mail(
            subject='Вы приглашены стать агентом организации',
            message='Вас добавлено в систему CRM. '
                    f'Ваш никнейм: "{user.username}" пароль: "{self.random_password}".'
                    'Пожалуйста, пройдите авторизацию, чтобы начать работать.',
            from_email='admin@test.com',  # если не указать используется DEFAULT_FORM_EMAIL setting.
            recipient_list=[user.email]  # Куда отправить.
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin, AgentInOrganisationMixin, generic.DetailView):
    """
    Обработчик вывода информации про одного агента из организации.
    """
    template_name = 'crm/agents/agent_detail.html'
    context_object_name = 'agent'


class AgentUpdateView(OrganisorAndLoginRequiredMixin, AgentInOrganisationMixin, generic.UpdateView):
    """
    Обработчик вывода формы для редактирования агента конкретной организации.
    """
    template_name = 'crm/agents/agent_update_form.html'
    form_class = AgentModelForm
    success_url = reverse_lazy('crm:agent-list')


class AgentDeleteView(OrganisorAndLoginRequiredMixin, AgentInOrganisationMixin, generic.DeleteView):
    """
    Обработчик удаления конкретного агента организацией.
    """
    template_name = 'crm/agents/agent_confirm_delete.html'
    context_object_name = 'agent'
    success_url = reverse_lazy('crm:agent-list')


class AgentAssignToLeadView(OrganisorAndLoginRequiredMixin, AgentInOrganisationMixin, generic.FormView):
    """
    Обработчик назначения агента конкретному лиду.
    """
    template_name = 'crm/agents/agent_assign_to_lead_form.html'
    form_class = AgentAssignToLeadForm
    success_url = reverse_lazy('crm:lead-list')

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AgentAssignToLeadView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AgentAssignToLeadView, self).form_valid(form)
