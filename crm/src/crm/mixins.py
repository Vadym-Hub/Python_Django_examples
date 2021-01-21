from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

from .models import Agent, Lead


class OrganisorAndLoginRequiredMixin(AccessMixin):
    """
    Класс проверяет, что текущий пользователь аутентифицирован
    и является организатором.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organisor:
            return redirect('crm:lead-list')
        return super().dispatch(request, *args, **kwargs)


class AgentInOrganisationMixin(object):
    """
    Возвращает агентов отфильтрованных по конкретной организации.
    """

    def get_queryset(self):
        organisation = self.request.user.organisation
        return Agent.objects.filter(organisation=organisation)


class LeadInOrganisationMixin(object):
    """
    Возвращает лидов отфильтрованных по конкретной организации.
    """

    def get_queryset(self):
        user = self.request.user
        # Инициализация запроса для лидов всей организации.
        if user.is_organisor:
            # Если запрос сделал глава организации.
            queryset = Lead.objects.filter(organisation=user.organisation)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # Фильтр для агента, который вошел в систему.
            queryset = queryset.filter(agent__user=user)
        return queryset
