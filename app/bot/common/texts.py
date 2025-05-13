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
        "profile_btn": "Профиль",
        "my_objects_btn": "Мои объекты",
        "material_remainder_btn": "Остаток материалов",
        "material_order_btn": "Заказ материалов",
        "info_btn": "Информация",
        "instructions": "Инструкции по использованию бота",
        "rules": "Правила использования",
        'profile_info': (
            "👤 *Профиль*\n\n"
            "🆔 Telegram ID: `{telegram_id}`\n"
            "📧 Username: @{username}\n"
            "👨‍💼 ФИО: {full_name}\n"
            "📱 Телефон: {phone}\n"
            "📊 Статус: {role}"
        ),
        'tools_list_btn': 'Инструменты',
        'language_select_btn': 'Выбор языка',
        'rules_btn': 'Правила',
        'no_tools': 'За вами не закреплено ни одного инструмента',
        'tools_list_header': '🛠 *Список закрепленных инструментов:*',
        'tool_item': '*{name}*\n📝 Описание: _{description}_',
        'no_description': 'Описание отсутствует',
        'lang_has_changed': 'Язык бота был изменен',
        'no_objects': 'У вас нет доступных объектов',
        'objects_list_header': '🏗 *Ваши объекты:*',
        'object_item': '🔹 *{name}*\n📝 _{description}_',
        'navigation_btn': '📍 Навигация',
        'documentation_btn': '📄 Документация',
        'notify_object_btn': '📢 Оповестить объект',
        'object_photo_btn': '📸 Фото с объекта',
        'object_checks_btn': '🧾 Учет чеков',
        'no_navigation': 'Навигация для этого объекта не добавлена',
        'enter_notification': 'Введите сообщение для отправки всем участникам объекта',
        'notification_format': (
            '📢 *Уведомление с объекта* {object_id}\n\n'
            '👤 *Отправитель:* {sender_name}\n'
            '📧 Username: {username}\n\n'
            '💬 *Сообщение:*\n_{message}_'
        ),
        'notification_sent': '✅ Уведомление отправлено всем участникам объекта',
        'send_object_photo': '📸 Отправьте фотографию с объекта',
        'enter_photo_description': '📝 Введите описание к фотографии',
        'object_photo_format': (
            '📸 *Фото с объекта #{object_id}*\n\n'
            '👤 *Отправитель:* {worker_name}\n'
            '📧 Username: {username}\n\n'
            '📝 *Описание:*\n_{description}_'
        ),
        'photo_sent': '✅ Фото успешно отправлено',
        'send_photo_only': '❌ Пожалуйста, отправьте фотографию',
        'send_check_photo': '📸 Отправьте фото чека',
        'enter_check_description': '📝 Введите описание чека',
        'enter_check_amount': '💰 Введите сумму чека (только цифры)',
        'invalid_amount': '❌ Неверный формат суммы. Введите число, например: 1234.56',
        'check_format': (
            '🧾 *Чек с объекта #{object_id}*\n\n'
            '👤 *Отправитель:* {worker_name}\n'
            '📧 Username: {username}\n\n'
            '📝 *Описание:* _{description}_\n'
            '💰 *Сумма:* {amount} руб.'
        ),
        'check_saved': '✅ Чек успешно сохранен',
        },
    'az':{
        'start': 'Salam, {name}! Mən botam',
        'language_select': 'Dil seçin:',
        'language_ru': 'Rus',
        'language_az': 'Azərbaycan',
        'language_tg': 'Tacik',
        'request_contact': 'Zəhmət olmasa, aşağıdakı düyməni istifadə edərək telefon nömrənizi paylaşın.',
        'username_instruction': """
        Botdan istifadə etmək üçün istifadəçi adı yaratmalısınız. Təlimatlara əməl edərək yaradın

        *Telegramda istifadəçi adı necə yaradılır:*

        1. Telegram parametrlərini açın
        2. "Profili redaktə et" düyməsini basın
        3. "İstifadəçi adı" sahəsini basın 
        4. İstədiyiniz istifadəçi adını düşünün və daxil edin
        5. Yadda saxlamaq üçün ✓ işarəsini basın

        İstifadəçi adı yaratdıqdan sonra aşağıdakı "Yoxla" düyməsini basın.""",
        'check': 'Yoxla',
        'create_username': 'İstifadəçi adı yarat',
        'has_no_username': 'İstifadəçi adı yaratmaq üçün təlimatlara əməl edin',
        'share_contact_btn': 'Əlaqə paylaş 📱',
        'no_contact': 'Klaviaturadan istifadə edin',
        'cancel': 'Ləğv et',
        'confirm': 'Təsdiq et',
        'its_no_contact': 'Zəhmət olmasa klaviaturadakı düyməni istifadə edin',
        'reques_docs': 'Sənədlərin şəkillərini çata yükləyin. Bütün sənədləri yüklədikdən sonra "Dayandır" düyməsini basın',
        'stop_upload_btn': 'Dayandır',
        'i_got_acquainted_btn': 'Tanış oldum',
        'i_got_acquainted': 'Hər şeylə tanış olduqdan sonra "Tanış oldum" düyməsini basın',
        'reques_fio': 'ASA daxil edin',
        'ru': 'Rus',
        'az': 'Azərbaycan',
        'tg': 'Tacik',
        'photo_received': 'Şəkil qəbul edildi. Ümumi yüklənib: {count}',
        'photos_saved': 'Bütün şəkillər ({count}) uğurla yadda saxlanıldı!',
        'no_photos': 'Heç bir şəkil yükləməmisiniz',
        'solve_example': 'İnsan olduğunuzu təsdiqləmək üçün nümunəni həll edin:\n{example}',
        'verification_success': 'Yoxlama uğurla keçdi! Qeydiyyat tamamlandı.',
        'wrong_answer': 'Yanlış cavab. Başqa nümunəni həll etməyə cəhd edin:\n{example}',
        'not_a_number': 'Zəhmət olmasa rəqəm daxil edin.',
        'report_accepted': 'Hesabat qəbul edildi',
        'report_error': 'Mesajı göndərərkən xəta baş verdi.',
        'profile_btn': 'Profil',
        'my_objects_btn': 'Mənim obyektlərim',
        'material_remainder_btn': 'Material qalığı',
        'material_order_btn': 'Material sifarişi',
        'info_btn': 'Məlumat',
        'instructions': 'Botdan istifadə təlimatları',
        'rules': 'İstifadə qaydaları',
        'profile_info': (
            "👤 *Profil*\n\n"
            "🆔 Telegram ID: `{telegram_id}`\n"
            "📧 İstifadəçi adı: @{username}\n"
            "👨‍💼 ASA: {full_name}\n"
            "📱 Telefon: {phone}\n"
            "📊 Status: {role}"
        ),
        'tools_list_btn': 'Alətlər',
        'language_select_btn': 'Dil seçimi',
        'rules_btn': 'Qaydalar',
        'no_tools': 'Sizə heç bir alət təhkim edilməyib',
        'tools_list_header': '🛠 *Təhkim edilmiş alətlərin siyahısı:*',
        'tool_item': '*{name}*\n📝 Təsvir: _{description}_',
        'no_description': 'Təsvir yoxdur',
        'lang_has_changed': 'Bot dili dəyişdirildi',
        'no_objects': 'Əlçatan obyektləriniz yoxdur',
        'objects_list_header': '🏗 *Sizin obyektləriniz:*',
        'object_item': '🔹 *{name}*\n📝 _{description}_',
        'navigation_btn': '📍 Naviqasiya',
        'documentation_btn': '📄 Sənədlər',
        'notify_object_btn': '📢 Obyekti xəbərdar et',
        'object_photo_btn': '📸 Obyektdən şəkil',
        'object_checks_btn': '🧾 Çeklərin uçotu',
        'no_navigation': 'Bu obyekt üçün naviqasiya əlavə edilməyib'
        
    },
    'tg':{
        'start': 'Салом, {name}! Ман бот ҳастам',
        'language_select': 'Забонро интихоб кунед:',
        'language_ru': 'Русӣ',
        'language_az': 'Озарбойҷонӣ',
        'language_tg': 'Тоҷикӣ',
        'request_contact': 'Лутфан, тавассути тугмаи зерин рақами телефони худро мубодила кунед.',
        'username_instruction': """
        Барои истифодаи бот шумо бояд номи корбарӣ созед. Дастурамалҳоро пайравӣ карда, онро эҷод кунед

        *Чӣ тавр дар Telegram номи корбарӣ сохтан мумкин аст:*

        1. Танзимоти Telegramро кушоед
        2. "Тағйир додани профил"-ро пахш кунед
        3. Майдони "Номи корбарӣ"-ро пахш кунед
        4. Номи корбарии дилхоҳро фикр карда, ворид кунед
        5. Барои нигоҳ доштан аломати ✓-ро пахш кунед

        Пас аз сохтани номи корбарӣ, тугмаи "Санҷидан"-ро дар поён пахш кунед.""",
        'check': 'Санҷидан',
        'create_username': 'Сохтани номи корбарӣ',
        'has_no_username': 'Барои сохтани номи корбарӣ дастурамалҳоро пайравӣ кунед',
        'share_contact_btn': 'Мубодилаи тамос 📱',
        'no_contact': 'Аз клавиатура истифода баред',
        'cancel': 'Бекор кардан',
        'confirm': 'Тасдиқ',
        'its_no_contact': 'Лутфан, аз тугмаи дар клавиатура истифода баред',
        'reques_docs': 'Суратҳои ҳуҷҷатҳоро ба чат бор кунед. Вақте ки ҳамаи ҳуҷҷатҳоро бор кардед, тугмаи "Қатъ кардан"-ро пахш кунед',
        'stop_upload_btn': 'Қатъ кардан',
        'i_got_acquainted_btn': 'Ман шинос шудам',
        'i_got_acquainted': 'Агар бо ҳама чиз шинос шуда бошед, тугмаи "Ман шинос шудам"-ро пахш кунед',
        'reques_fio': 'Ному насаб-ро ворид кунед',
        'ru': 'Русӣ',
        'az': 'Озарбойҷонӣ',
        'tg': 'Тоҷикӣ',
        'photo_received': 'Сурат қабул шуд. Ҳамагӣ бор шудааст: {count}',
        'photos_saved': 'Ҳамаи суратҳо ({count}) бомуваффақият нигоҳ дошта шуданд!',
        'no_photos': 'Шумо ягон сурат бор накардаед',
        'solve_example': 'Барои тасдиқи инсон буданатон, масъаларо ҳал кунед:\n{example}',
        'verification_success': 'Санҷиш бомуваффақият анҷом ёфт! Бақайдгирӣ анҷом ёфт.',
        'wrong_answer': 'Ҷавоби нодуруст. Кӯшиш кунед масъалаи дигарро ҳал кунед:\n{example}',
        'not_a_number': 'Лутфан рақам ворид кунед.',
        'report_accepted': 'Ҳисобот қабул шуд',
        'report_error': 'Ҳангоми фиристодани паём хато рух дод.',
        'profile_btn': 'Профил',
        'my_objects_btn': 'Объектҳои ман',
        'material_remainder_btn': 'Бақияи масолеҳ',
        'material_order_btn': 'Фармоиши масолеҳ',
        'info_btn': 'Маълумот',
        'instructions': 'Дастурамал оид ба истифодаи бот',
        'rules': 'Қоидаҳои истифода',
        'profile_info': (
            "👤 *Профил*\n\n"
            "🆔 Telegram ID: `{telegram_id}`\n"
            "📧 Номи корбарӣ: @{username}\n"
            "👨‍💼 Ному насаб: {full_name}\n"
            "📱 Телефон: {phone}\n"
            "📊 Мақом: {role}"
        ),
        'tools_list_btn': 'Асбобҳо',
        'language_select_btn': 'Интихоби забон',
        'rules_btn': 'Қоидаҳо',
        'no_tools': 'Ба шумо ягон асбоб вобаста карда нашудааст',
        'tools_list_header': '🛠 *Рӯйхати асбобҳои вобасташуда:*',
        'tool_item': '*{name}*\n📝 Тавсиф: _{description}_',
        'no_description': 'Тавсиф вуҷуд надорад',
        'lang_has_changed': 'Забони бот тағйир дода шуд',
        'no_objects': 'Шумо объектҳои дастрас надоред',
        'objects_list_header': '🏗 *Объектҳои шумо:*',
        'object_item': '🔹 *{name}*\n📝 _{description}_',
        'navigation_btn': '📍 Навигатсия',
        'documentation_btn': '📄 Ҳуҷҷатҳо',
        'notify_object_btn': '📢 Огоҳ кардани объект',
        'object_photo_btn': '📸 Сурат аз объект',
        'object_checks_btn': '🧾 Баҳисобгирии чекҳо',
        'no_navigation': 'Барои ин объект навигатсия илова нашудааст',
        'document_item': '*Тип документа:* _{type}_',
        
        
    }
}