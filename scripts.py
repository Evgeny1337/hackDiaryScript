from datacenter.models import Schoolkid, Mark, Chastisement, Subject, Lesson
import random


def get_random_phrase(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            phrases = file.readlines()
            phrases = [phrase.strip() for phrase in phrases]
            if phrases:
                return random.choice(phrases)
            else:
                return
    except FileNotFoundError:
        return


def fixed_mark(name):
    schoolkid = Schoolkid.objects.get(full_name__contains=name)
    if schoolkid:
        bad_marks = Mark.objects.filter(
            schoolkid=schoolkid, points__range=(0, 3))
        for bad_mark in bad_marks:
            bad_mark.points = 5
            bad_mark.save()
    else:
        print('Такого ученика несуществует')


def remove_chastisements(name):
    schoolkid = Schoolkid.objects.get(full_name__contains=name)
    if schoolkid:
        chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
        for chastisement in chastisements:
            chastisement.delete()
    else:
        print('Такого ученика несуществует')


def create_commendation(name, subject):
    schoolkid = Schoolkid.objects.get(full_name__contains=name)
    if (schoolkid):
        subject = Subject.objects.filter(title=subject, year_of_study=6)[0]
        lesson = Lesson.objects.filter(
            year_of_study=6, group_letter='А', subject=subject).order_by('date').reverse()
        chastisement = get_random_phrase(
            './project/commendation.txt').split('.')[1]
        if chastisement:
            Chastisement.objects.create(
                text=chastisement, created=lesson[0].date, schoolkid=schoolkid, subject=subject, teacher=lesson[0].teacher)
        else:
            print('Заполните файл commendation.txt с похвалой')
    else:
        print('Такого ученика несуществует')
