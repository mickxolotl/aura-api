# -*- coding: utf-8 -*-
import aura

api = aura.API(aura.CookieSession('Session_id', 'yandexuid'))

post_id = api.user.addpost_new(background=aura.utils.Colors.RED, text='Test Post', keywords=['python'],
                               age='16,85', gender=2, increase_coverage=0,attachments=[''], geo=0)
