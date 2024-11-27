from datacenter.models import Schoolkid, Mark, Chastisement, Subject, Lesson,Commendation
import random


def get_schoolkid(name):
    return Schoolkid.objects.filter(full_name__contains=name).first()

def get_random_phrase(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            phrases = file.readlines()
            phrases = [phrase.strip().split('.')[1] for phrase in phrases]
            return random.choice(phrases) if phrases else None
    except FileNotFoundError:
        return None


def fixed_mark(name):
    schoolkid = get_schoolkid(name)
    if schoolkid:
        Mark.objects.filter(
            schoolkid=schoolkid, points__range=(0, 3)).update(points=5)
    else:
        print('Такого ученика несуществует')


def remove_chastisements(name):
    schoolkid = get_schoolkid(name)
    if schoolkid:
        Chastisement.objects.filter(schoolkid=schoolkid).delete()
    else:
        print('Такого ученика несуществует')


def create_commendation(name, subject):
    schoolkid = get_schoolkid(name)
    if (schoolkid):
        subject = Subject.objects.filter(title=subject, year_of_study=schoolkid.year_of_study).first()
        lesson = Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter, subject=subject).order_by('-date')
        сommendation = get_random_phrase(
            './project/commendation.txt')
        if сommendation:
            Commendation.objects.create(
                text=сommendation, created=lesson[0].date, schoolkid=schoolkid, subject=subject, teacher=lesson[0].teacher)
        else:
            print('Заполните файл commendation.txt с похвалой')
    else:
        print('Такого ученика несуществует')
