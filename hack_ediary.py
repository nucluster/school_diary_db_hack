from datacenter.models import Chastisement, Mark, Schoolkid, Commendation, Lesson, Subject, Teacher
from random import choice


def fix_marks(schoolkid_name):
    schoolkid = Schoolkid.objects.filter(full_name__contains=schoolkid_name)
    if len(schoolkid) == 1:
        print('Исправлены оценки 2 и 3:', Mark.objects.filter(schoolkid=schoolkid[0], points__in=[2, 3]).update(points=choice([4,5])))
    elif len(schoolkid) == 0:
        print(f'Ученика с именем {schoolkid_name} нет в базе данных.')
    else:
        print(f'Найдено {len(schoolkid)} учеников с именем {schoolkid_name}:', *schoolkid, sep='\n')


def remove_chastisements(schoolkid_name):
    schoolkid = Schoolkid.objects.filter(full_name__contains=schoolkid_name)
    if len(schoolkid) == 1:
        print('Удалены замечания:', Chastisement.objects.filter(schoolkid=schoolkid[0]).delete())
    elif len(schoolkid) == 0:
        print(f'Ученика с именем {schoolkid_name} нет в базе данных.')
    else:
        print(f'Найдено {len(schoolkid)} учеников с именем {schoolkid_name}:', *schoolkid, sep='\n')


def get_random_commendation_phrase():
    with open('commendation_phrases.txt', 'rt') as f:
        phrases = [line.rstrip('\n') for line in f]
    return choice(phrases)


def create_commendation(schoolkid_name, subject_title, date):
    schoolkid = Schoolkid.objects.filter(full_name__contains=schoolkid_name)
    if len(schoolkid) == 0:
        print(f'Ученика с именем {schoolkid_name} нет в базе данных.')
    elif len(schoolkid) > 1:
        print(f'Найдено {len(schoolkid)} учеников с именем {schoolkid_name}:', *schoolkid, sep='\n')
    else:
        subject = Subject.objects.filter(title__contains=subject_title, year_of_study=schoolkid[0].year_of_study)
        if len(subject) == 0:
            print(f'Предмета {subject_title} нет в базе данных или у данного ученика.')
        elif len(subject) > 1:
            print(f'Найдено {len(subject)} предметов с названием {subject_title}:', *subject, sep='\n')
        else:
            lesson = Lesson.objects.filter(date=date, subject=subject[0], year_of_study=schoolkid[0].year_of_study, group_letter=schoolkid[0].group_letter)
            if len(lesson) == 0:
                print(
                    f'По предмету {subject[0].title} {subject[0].year_of_study} класс на дату: {date} у ученика {schoolkid[0].full_name} не было занятий')
            else:
                marks = Mark.objects.filter(created=date, schoolkid=schoolkid[0], subject=subject[0])
                if len(marks) >= 1:
                    print(Commendation.objects.create(text=get_random_commendation_phrase(), created=date, schoolkid=schoolkid[0],
                                                      subject=subject[0], teacher=lesson[0].teacher))
                else:
                    print('Невозможно добавить похвалу, нет оценок')
