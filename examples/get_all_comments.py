# -*- coding: utf-8 -*-
import aura

api = aura.API(aura.CookieSession('Session_id', 'yandexuid'))

post_id = 651792411028856

comments = []

c = True
i = 0
while c:
    c = api.post.comments[post_id](page=i)
    comments.extend(c)
    i += 1

# Полученных комментариев может быть меньше, чем на счетчике,
# так как ответы на комментарии хранятся в `subcomments`

for comment in comments:
    print(comment.text.replace('\n', ' // '))

    for subcomment in comment.subcomments:
        print('\t', subcomment.text.replace('\n', ' // '))

