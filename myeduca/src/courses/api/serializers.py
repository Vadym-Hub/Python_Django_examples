from rest_framework import serializers
from ..models import Subject, Course, Module, Content


class SubjectSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Subject"""
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']


class ModuleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Module"""
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Course"""
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview',
                  'created', 'owner', 'modules']


class ItemRelatedField(serializers.RelatedField):
    """
    Создаем свой класс для формирования ответа на запросы
    к API для обобщенной связи с несколькими моделями
    """
    def to_representation(self, value):
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Content"""
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    """Сериализатор формирует данные входящего в модуль содержимого"""
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']


class CourseWithContentsSerializer(serializers.ModelSerializer):
    """Розширенный сериализатор для модели Course"""
    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug',
                  'overview', 'created', 'owner', 'modules']
