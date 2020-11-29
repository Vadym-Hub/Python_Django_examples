from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'
    verbose_name = 'изображения'

    def ready(self):
        # Импортируем файл с описанной функцией-подписчиком на сигнал.
        import images.signals
