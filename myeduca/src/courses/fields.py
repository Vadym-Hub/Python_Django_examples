"""Свои типы полей"""

from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    """
    Собственное поле сортировки (для определения порядка для содержимого курсов).
    Наследуэмся от PositiveIntegerField и реализовуем две дополнительные функции:
    1) автоматическое назначение порядкового номера, если он не был задан
        явно. Когда создается новый объект и пользователь не указывает порядок,
        поле будет заполняться автоматически, основываясь на том, сколько
        объектов уже создано для модуля. Например, если уже есть два объекта
        с порядковыми номерами 1 и 2, то новому будет присвоен 3;
    2) сортировка объектов по порядку номеров. Модули курсов и содержимое
        модулей всегда будут возвращаться отсортированными внутри своего
        родительского объекта.
    """

    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # Значение пусто.
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # Фильтруем объекты с такими же значениями полей, перечисленных в "for_fields".
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                # Получаем заказ последнего объекта.
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(OrderField, self).pre_save(model_instance, add)
