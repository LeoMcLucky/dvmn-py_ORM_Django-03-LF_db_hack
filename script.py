import random
from datacenter.models import Schoolkid, Lesson, Mark, Commendation, Chastisement
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def fix_marks(schoolkid):
    """Исправить все плохие оценки (2 и 3 на 5)."""
    Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=[2, 3]
    ).update(points=5)
    print("Исправлены все плохие оценки")


def remove_chastisements(schoolkid):
    """Удалить все замечания у ученика."""
    Chastisement.objects.filter(schoolkid=schoolkid).delete()
    print("Удалены все замечания")


def create_commendation(schoolkid, subject):
    """Добавить похвалу по предмету."""

    praises = [
        "Молодец!",
        "Отлично!",
        "Хорошо!",
        "Гораздо лучше, чем я ожидал!",
        "Ты меня приятно удивил!",
        "Великолепно!",
        "Прекрасно!",
        "Ты меня очень обрадовал!",
        "Именно этого я давно ждал от тебя!",
        "Сказано здорово – просто и ясно!",
        "Ты, как всегда, точен!",
        "Очень хороший ответ!",
        "Талантливо!",
        "Ты сегодня прыгнул выше головы!",
        "Я поражен!",
        "Уже существенно лучше!",
        "Потрясающе!",
        "Замечательно!",
        "Прекрасное начало!",
        "Так держать!",
        "Ты на верном пути!",
        "Здорово!",
        "Это как раз то, что нужно!",
        "Я тобой горжусь!",
        "С каждым разом у тебя получается всё лучше!",
        "Мы с тобой не зря поработали!",
        "Я вижу, как ты стараешься!",
        "Ты растешь над собой!",
        "Ты многое сделал, я это вижу!",
        "Теперь у тебя точно все получится!"
    ]
    lesson = Lesson.objects.filter(
        group_letter=schoolkid.group_letter,
        year_of_study=schoolkid.year_of_study,
        subject__title=subject
    ).order_by('-date').first()

    if not lesson:
        print(f"Не удалось найти урок по предмету {subject}")
        return

    Commendation.objects.create(
        text=random.choice(praises),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher
    )
    print("Добавлена похвала")


def get_schoolkid(name):
    """Найти ученика по ФИО (или части ФИО)."""
    try:
        return Schoolkid.objects.get(full_name__contains=name)
    except ObjectDoesNotExist as err:
        print("Ученик не найден. Проверьте ФИО.", f"Ошибка: {err}")
    except MultipleObjectsReturned as err:
        print("Найдено несколько учеников с таким именем. Уточните ФИО.",
              f"Ошибка: {err}")
        return None


def fix_everything(name, subject_title):
    """
    Полностью исправить дневник ученика:
    - исправить плохие оценки
    - удалить замечания
    - добавить похвалу по предмету
    """
    schoolkid = get_schoolkid(name)
    if not schoolkid:
        return

    fix_marks(schoolkid)
    remove_chastisements(schoolkid)
    create_commendation(schoolkid, subject_title)
    print(f"Всё исправлено для {schoolkid.full_name}.")
