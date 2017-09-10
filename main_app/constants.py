# -*- coding: utf-8 -*-

ALIVE = u'Жив'
DEAD = u'Мертв'

KILLER_STATUS_CHOICES = (
    (ALIVE, u'Жив'),
    (DEAD, u'Мертв'),
)

NEW = u'Новая'
OLD = u'Закончилась'
REGISTRATION = u'Идет Регистрация'

GAME_STATUS_CHOICES = (
	(NEW, u'Новая'),
    (REGISTRATION, u'Идет Регистрация'),
    (OLD, u'Закончилась'),
)