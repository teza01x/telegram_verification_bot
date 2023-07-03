import asyncio


async def data_clean(data):
    result = list()
    for j in [i for i in data]:
        if j == None:
            result.append('*' + ' ❌')
        else:
            result.append(j + ' ✅')

    return result[0], result[1], result[2], result[3]


async def clean_text(text, object):
    text = text.replace(object, '')
    lst = [i for i in text.split() if i != '']
    return lst[0], lst[1]


async def clean_text_admin(text, object):
    text = text.replace(object, '')
    lst = [i for i in text.split() if i != '']
    return lst[0]


async def clean_text_notification(text, object):
    text = text.replace(object, '')
    text = text.lstrip()
    return text