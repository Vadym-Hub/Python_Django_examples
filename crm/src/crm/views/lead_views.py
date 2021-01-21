from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from ..mixins import OrganisorAndLoginRequiredMixin, LeadInOrganisationMixin
from ..models import Lead
from ..forms import LeadModelForm, LeadStatusUpdateForm


class LeadListView(LoginRequiredMixin, generic.ListView):
    """
    Обработчик вывода списка лидов.
    Для всех зарегестрировынных пользователей.
    """
    template_name = 'crm/leads/lead_list.html'
    context_object_name = 'leads'
    paginate_by = 20

    def get_queryset(self):
        """
        Возвращает лидов отфильтрованных по конкретной организации
        и которые не имеют назначенных агентов.
        """
        user = self.request.user
        # Инициализация запроса для лидов всей организации.
        if user.is_organisor:
            # Если запрос сделал глава организации.
            queryset = Lead.objects.filter(organisation=user.organisation, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation, agent__isnull=False)
            # Фильтр для агента, который вошел в систему.
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.organisation, agent__isnull=True)
            context.update({
                'unassigned_leads': queryset
            })
        return context


class LeadDetailView(LoginRequiredMixin, LeadInOrganisationMixin, generic.DetailView):
    """
    Обработчик вывода одного лида.
    """
    template_name = 'crm/leads/lead_detail.html'
    context_object_name = 'lead'


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    """
    Обработчик вывода формы для создания лида и отправки email
    если лид успешно создан.
    """
    template_name = 'crm/leads/lead_create_form.html'
    form_class = LeadModelForm
    success_url = reverse_lazy('crm:lead-list')

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.organisation
        lead.save()
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, LeadInOrganisationMixin, generic.UpdateView):
    """
    Обработчик вывода формы для редактирования лида.
    """
    template_name = 'crm/leads/lead_update_form.html'
    form_class = LeadModelForm
    success_url = reverse_lazy('crm:lead-list')


class LeadDeleteView(OrganisorAndLoginRequiredMixin, LeadInOrganisationMixin, generic.DeleteView):
    """
    Обработчик удаления лида.
    """
    template_name = 'crm/leads/lead_confirm_delete.html'
    success_url = reverse_lazy('crm:lead-list')


class LeadStatusUpdateView(LoginRequiredMixin, LeadInOrganisationMixin, generic.UpdateView):
    """
    Обработчик обновления статуса лида.
    """
    template_name = 'crm/leads/lead_status_update_form.html'
    form_class = LeadStatusUpdateForm

    def get_success_url(self):
        return reverse('crm:lead-detail', kwargs={'pk': self.get_object().id})


class LeadStatusListView(LoginRequiredMixin, LeadInOrganisationMixin, generic.ListView):
    """
    Обработчик вывода подсчета лидов по статусу конкрктной организации.
    """
    template_name = 'crm/leads/lead_status_list.html'
    context_object_name = 'status_list'

    def get_context_data(self, **kwargs):
        context = super(LeadStatusListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.organisation)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)

        context.update({
            'new_lead_count': queryset.filter(status='new').count(),
            'contacted_lead_count': queryset.filter(status='contacted').count(),
            'converted_lead_count': queryset.filter(status='converted').count(),
            'unconverted_lead_count': queryset.filter(status='unconverted').count(),
            'lead_count': queryset.count(),
        })
        return context
