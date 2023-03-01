SHEDULE_URLS = {
    'pgups': [
        {
            'url': "https://rasp.pgups.ru/schedule/group",
            'args' : ['a', {'target': '_blank', 'class': 'btn btn-sm btn-secondary btn-pill mr-1 mb-2'}],
        }
    ]
}


user_study_data_template = {
    'university': None,
    'course': None,
    'faculty': None,
    'group': None,
}

week_type = -1

week_day_names = {
    'сегодня': 0,
    'завтра': 1,
    'послезавтра': 2,
    'пн': 0,
    'вт': 1,
    'ср': 2,
    'чт': 3,
    'пт': 4,
    'сб': 5,
}