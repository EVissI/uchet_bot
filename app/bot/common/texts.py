def get_text(text_code:str, lang:str = 'ru',**kwargs) -> str:
    text = ''
    match lang:
        case 'ru':
            text = TEXTS_TRANSLITE['ru'].get(text_code,text_code)
        case 'az':
            text = TEXTS_TRANSLITE['az'].get(text_code,text_code)
        case 'tg':
            text = TEXTS_TRANSLITE['tg'].get(text_code,text_code)
        case _:
            text = TEXTS_TRANSLITE['ru'].get(text_code,text_code)
    return text.format(**kwargs)


def get_all_texts(text_code: str) ->list[str]:
    __languages = ['ru', 'az', 'tg']
    result = []
    for lang in __languages:
        result.append(TEXTS_TRANSLITE[lang].get(text_code,text_code))
    return result


TEXTS_TRANSLITE = {
    'ru': {
        'start': 'Привет, {name}! Я бот',
        'language_select': 'Выберите язык:',
        'language_ru': 'Русский',
        'language_az': 'Азербайджанский',
        'language_tg': 'Таджикский',
        'request_contact': 'Пожалуйста, поделитесь своим номером телефона, с помощью кнопки ниже.',
        'username_instruction': """
Для использования бота необходимо создать юзернейм. Создайте его следуя инструкциям

*Как создать username в Telegram:*

1. Откройте настройки Telegram
2. Нажмите на "Изменить профиль"
3. Нажмите на поле "Username"
4. Придумайте и введите желаемый username
5. Нажмите галочку ✓ для сохранения

После создания username нажмите кнопку "Проверить" ниже.""",
        'check': 'Проверить',
        'create_username': 'Создать username',
        'has_no_username': 'Следуйте инструкциям, чтобы создать юзернейм',
        'share_contact_btn': 'Поделиться контактом 📱',
        'no_contact': 'Используйте клавиатуру',
        'cancel': 'Отмена',
        'confirm': 'Подтвердить',
        'its_no_contact':'Пожалуйста используйте кнопку на клавиатуре',
        'reques_docs':'Скидывайте фотографии документов в чат. Когда загрузите все документы нажмите кнопку \'Прекратить\'',
        'stop_upload_btn':'Прекратить',
        'i_got_acquainted_btn':'Я ознакомился',
        'i_got_acquainted':'Если ознакомились со всем нажмите на кнопку \'Я ознакомился\'',
        'reques_fio':'Введите ФИО',
        'ru':'Русский',
        'az':'Айзербаджанский',
        'tg':'Таджитский',
        'photo_received': 'Фото получено. Всего загружено: {count}',
        'photos_saved': 'Все фотографии ({count}) успешно сохранены!',
        'no_photos': 'Вы не загрузили ни одной фотографии',
        'solve_example':'Для подтверждения что вы человек, решите пример:\n{example}',
        'verification_success': 'Верификация пройдена успешно! Регистрация завершена.',
        'wrong_answer': 'Неверный ответ. Попробуйте решить другой пример:\n{example}',
        'not_a_number': 'Пожалуйста, введите число.',
        "report_accepted": "Отчет принят",
        "report_error": "Произошла ошибка при пересылке сообщения.",
        "profile": "Профиль",
        "my_objects": "Мои объекты",
        "material_remainder": "Остаток материалов",
        "material_order": "Заказ материалов",
        "info": "Информация",
        "instructions": "Инструкции по использованию бота",
        "rules": "Правила использования",
        },
    'az':{
        
    },
    'tg':{
        
    }
}