from django.db.models import TextChoices


class LimitationType(TextChoices):
    classes = "Классы"
    lists = "Списки"
    dicts = "Словари"
    strings = "Строки"
    imports = "Импорты"
    functions = "Функции"
    control_flow = "Циклы и условия"
