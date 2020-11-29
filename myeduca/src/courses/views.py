from braces.views import JsonRequestResponseMixin, CsrfExemptMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.apps import apps
from django.views import generic
from django.views.generic.base import TemplateResponseMixin

from students.forms import CourseEnrollForm

from .forms import ModuleFormSet
from .models import Course, Module, Content, Subject


class OwnerMixin(object):
    """
    Переопределяем этот метод, так чтобы получать только
    объекты, владельцем которых является текущий пользователь
    (определяем владельца курса)
    """
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    """
    Переопределяем этот метод, чтобы автоматически заполнять
    поле owner сохраняемого объекта.
    """
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    """Указываем с каким конкретно курсом работаем"""
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('curses:manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """
    Указываем поля модели, из которых будет формироваться
    объект обработчиками CreateView и UpdateView
    """
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('courses:manage_course_list')
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, generic.ListView):
    """Обработчик вывода курсов владельцем курса"""
    template_name = 'courses/manage/course/list.html'


class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, generic.CreateView):
    """Обработчик для создания курса владельцу курса"""
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, generic.UpdateView):
    """Обработчик для обновления курса владельцем курса"""
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, generic.DeleteView):
    """Обработчик для удаления курса владельцем курса"""
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('courses:manage_course_list')
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, generic.View):
    """
    обрабатывает действия, связанные с набором форм по сохранению,
    редактированию и удалению модулей для конкретного курса
    """
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        """Позволяет избежать дублирования кода, который отвечает за формирование набора форм"""
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        """
        Если запрос отправлен с помощью GET, его обработка будет
        делегирована методу get() обработчика; если POST, то методу post().
        """
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        """Обрабатывает GET-запрос"""
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST-запросы"""
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('courses:manage_course_list')
        return self.render_to_response({'course': self.course, 'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, generic.View):
    """Обработчик, который позволят создать, изменить или удалить содержимое модуля"""
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        """Возвращает класс модели по переданному имени"""
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        """Создает форму в зависимости от типа содержимого"""
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        """Получает данные из запроса и создает соответствующие объекты модуля"""
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super(ContentCreateUpdateView, self).dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        """Формирует модельные формы для объектов Text, Video, Image или File"""
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        """
        Если форма заполнена корректно, создает новый объект, указав
        текущего пользователя, request.user, владельцем.
        """
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # Создаем новый объект.
                Content.objects.create(module=self.module, item=obj)
            return redirect('courses:module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})


class ContentDeleteView(generic.View):
    """Обработчик удаления контента модуля"""
    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('courses:module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, generic.View):
    """
    Обработчик получает из базы данных модуль по переданному ID
    и генерирует для него страницу подробностей.
    """
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, generic.View):
    """Обработчик, который получает новый порядок модулей курса в формате JSON"""
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, generic.View):
    """Обработчик, который получает новый порядок содержимого модуля в формате JSON"""
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,module__course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class CourseListView(TemplateResponseMixin, generic.View):
    """Обработчик отображения курсов"""
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(total_courses=Count('courses'))
        courses = Course.objects.annotate(total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': courses})


class CourseDetailView(generic.DetailView):
    """Обработчик, который выводит страницу курса"""
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        """
        Добавляем форму в контекст шаблона. Для записи пользователя на данный курс
        Объект формы содержит скрытое поле с ID курса, поэтому при нажатии кнопки
        на сервер будут отправлены данные курса и пользователя.
        """
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})
        return context
