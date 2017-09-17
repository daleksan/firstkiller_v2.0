# -*- coding: utf-8 -*-

ALIVE = u'Жив'
DEAD = u'Мертв'

KILLER_STATUS_CHOICES = (
    (ALIVE, u'Жив'),
    (DEAD, u'Мертв'),
)

NEW_GAME = u'Новая Игра'
REGISTRATION_IN_PROGRESS = u'Идет Регистрация'
REGISTRATION_END = u'Регистрация Завершена'
GAME_BEGIN = u'Игра Началась'
GAME_END = u'Игра Закончилась'

GAME_STATUS_CHOICES = (
    (NEW_GAME, u'Новая Игра'),
    (REGISTRATION_IN_PROGRESS, u'Идет Регистрация'),
    (REGISTRATION_END, u'Регистрация Завершена'),
    (GAME_BEGIN, u'Игра Началась'),
    (GAME_END, u'Игра Закончилась'),
)
