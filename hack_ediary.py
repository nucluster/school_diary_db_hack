from datacenter.models import (
    Schoolkid, Lesson, Subject, Mark, Chastisement, Commendation
)
from random import choice


def get_obj(klass, *args, **kwargs):
    try:
        obj = klass.objects.get(*args, **kwargs)
    except klass.DoesNotExist:
        print(f'Объекта класса {klass} с заданными параметрами нет в базе '
              f'данных.')
        return None
    except klass.MultipleObjectsReturned:
        print(f'В базе данных найдено много объектов класса {klass} с '
              f'заданными параметрами.')
        return None
    return obj


def fix_marks(schoolkid_name):
    schoolkid = get_obj(Schoolkid, full_name__contains=schoolkid_name)
    if not schoolkid:
        return
    total_fix_marks = Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=[2, 3]).update(points=choice([4, 5]))
    return f'Исправлены оценки 2 и 3 ученика {schoolkid.full_name} на 4 ' \
           f'и 5 в количестве: {total_fix_marks}'


def remove_chastisements(schoolkid_name):
    schoolkid = get_obj(Schoolkid, full_name__contains=schoolkid_name)
    if not schoolkid:
        return
    total_removed_chastisements = Chastisement.objects.filter(
        schoolkid=schoolkid).delete()[0]
    return f'Удалены замечания ученика {schoolkid.full_name} в количестве: ' \
           f'{total_removed_chastisements} '


def get_random_commendation_phrase():
    with open('commendation_phrases.txt', 'rt', encoding='utf-8') as file:
        phrases = file.read().splitlines()
    return choice(phrases)


def create_commendation(schoolkid_name, subject_title, date):
    schoolkid = get_obj(Schoolkid, full_name__contains=schoolkid_name)
    if not schoolkid:
        return
    subject = get_obj(Subject,
                      title__contains=subject_title,
                      year_of_study=schoolkid.year_of_study)
    if not subject:
        return
    lesson = get_obj(Lesson,
                     date=date,
                     subject=subject,
                     year_of_study=schoolkid.year_of_study,
                     group_letter=schoolkid.group_letter)
    if not lesson:
        return
    marks = Mark.objects.filter(created=date, schoolkid=schoolkid,
                                subject=subject)
    if len(marks) >= 1:
        return Commendation.objects.create(
            text=get_random_commendation_phrase(),
            created=date,
            schoolkid=schoolkid,
            subject=subject,
            teacher=lesson.teacher)
    else:
        print('Невозможно добавить похвалу, нет оценок')
