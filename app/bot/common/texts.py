from app.bot.common.utils import escape_html


def get_text(text_code: str, lang: str = "ru", **kwargs) -> str:
    text = ""
    match lang:
        case "ru":
            text = TEXTS_TRANSLITE["ru"].get(text_code, text_code)
        case "az":
            text = TEXTS_TRANSLITE["az"].get(text_code, text_code)
        case "tg":
            text = TEXTS_TRANSLITE["tg"].get(text_code, text_code)
        case _:
            text = TEXTS_TRANSLITE["ru"].get(text_code, text_code)
    escaped_kwargs = {key: escape_html(value) for key, value in kwargs.items()}

    return text.format(**escaped_kwargs)


def get_all_texts(text_code: str) -> list[str]:
    __languages = ["ru", "az", "tg"]
    result = []
    for lang in __languages:
        result.append(TEXTS_TRANSLITE[lang].get(text_code, text_code))
    return result


TEXTS_TRANSLITE = {
    "ru": {
        "start": "Привет, {name}! Я бот",
        "language_select": "Выберите язык:",
        "language_ru": "Русский",
        "language_az": "Азербайджанский",
        "language_tg": "Таджикский",
        "request_contact": "Пожалуйста, поделитесь своим номером телефона, с помощью кнопки ниже.",
        "username_instruction": """
Для использования бота необходимо создать юзернейм. Создайте его следуя инструкциям

<b>Как создать username в Telegram:</b>

1. Откройте настройки Telegram
2. Нажмите на "Изменить профиль"
3. Нажмите на поле "Username"
4. Придумайте и введите желаемый username
5. Нажмите галочку ✓ для сохранения

После создания username нажмите кнопку "Проверить" ниже.""",
        "check": "Проверить",
        "create_username": "Создать username",
        "has_no_username": "Следуйте инструкциям, чтобы создать юзернейм",
        "share_contact_btn": "Поделиться контактом 📱",
        "no_contact": "Используйте клавиатуру",
        "cancel": "Отмена",
        "confirm": "Подтвердить",
        "its_no_contact": "Пожалуйста используйте кнопку на клавиатуре",
        "reques_docs": "Скидывайте фотографии документов в чат. Когда загрузите все документы нажмите кнопку 'Прекратить'",
        "stop_upload_btn": "Прекратить",
        "i_got_acquainted_btn": "Я ознакомился",
        "i_got_acquainted": "Если ознакомились со всем нажмите на кнопку 'Я ознакомился'",
        "reques_fio": "Введите ФИО",
        "ru": "Русский",
        "az": "Айзербаджанский",
        "tg": "Таджитский",
        "photo_received": "Фото получено. Всего загружено: {count}",
        "photos_saved": "Все фотографии ({count}) успешно сохранены!",
        "no_photos": "Вы не загрузили ни одной фотографии",
        "solve_example": "Для подтверждения что вы человек, решите пример:\n{example}",
        "verification_success": "Верификация пройдена успешно! Регистрация завершена.",
        "wrong_answer": "Неверный ответ. Попробуйте решить другой пример:\n{example}",
        "not_a_number": "Пожалуйста, введите число.",
        "report_accepted": "Отчет принят",
        "report_error": "Произошла ошибка при пересылке сообщения.",
        "profile_btn": "Профиль",
        "my_objects_btn": "Мои объекты",
        "material_remainder_btn": "Остаток материалов",
        "material_order_btn": "Заказ материалов",
        "info_btn": "Информация",
        "instructions": "Инструкции по использованию бота",
        "rules": "Правила использования",
        "profile_info": (
            "👤 <b>Профиль</b>\n\n"
            "🆔 Telegram ID: <code>{telegram_id}</code>\n"
            "📧 Username: @{username}\n"
            "👨‍💼 ФИО: {full_name}\n"
            "📱 Телефон: {phone}\n"
            "📊 Статус: {role}"
        ),
        "tools_list_btn": "Инструменты",
        "language_select_btn": "Выбор языка",
        "rules_btn": "Правила",
        "no_tools": "За вами не закреплено ни одного инструмента",
        "tools_list_header": "🛠 <b>Список закрепленных инструментов:</b>",
        "tool_item": "<b>{name}</b>\n📝 Описание: <i>{description}</i>",
        "no_description": "Описание отсутствует",
        "lang_has_changed": "Язык бота был изменен",
        "no_objects": "У вас нет доступных объектов",
        "objects_list_header": "🏗 <b>Ваши объекты:</b>",
        "object_item": "🔹 <b>{name}</b>\n📝 <i>{description}</i>",
        "navigation_btn": "📍 Навигация",
        "documentation_btn": "📄 Документация",
        "notify_object_btn": "📢 Оповестить объект",
        "object_photo_btn": "📸 Фото с объекта",
        "object_checks_btn": "🧾 Учет чеков",
        "no_navigation": "Навигация для этого объекта не добавлена",
        "enter_notification": "Введите сообщение для отправки всем участникам объекта",
        "notification_format": (
            "📢 <b>Уведомление с объекта {object_id}</b>\n\n"
            "👤 <b>Отправитель:</b> {sender_name}\n"
            "📧 Username: {username}\n\n"
            "💬 <b>Сообщение:</b>\n<i>{message}</i>"
        ),
        "notification_sent": "✅ Уведомление отправлено всем участникам объекта",
        "send_object_photo": "📸 Отправьте фотографию с объекта",
        "enter_photo_description": "📝 Введите описание к фотографии",
        "object_photo_format": (
            "📸 <b>Фото с объекта #{object_id}</b>\n\n"
            "👤 <b>Отправитель:</b> {worker_name}\n"
            "📧 Username: {username}\n\n"
            "📝 <b>Описание:</b>\n<i>{description}</i>"
        ),
        "photo_sent": "✅ Фото успешно отправлено",
        "send_photo_only": "❌ Пожалуйста, отправьте фотографию",
        "send_check_photo_and_description": "📸 Отправьте фото и описание чека",
        "enter_check_amount": "💰 Введите сумму чека (только цифры)",
        "invalid_amount": "❌ Неверный формат суммы. Введите число, например: 1234.56",
        "check_format": (
            "🧾 <b>Чек с объекта #{object_id}</b>\n\n"
            "👤 <b>Отправитель:</b> {worker_name}\n"
            "📧 Username: {username}\n\n"
            "📝 <b>Описание:</b> <i>{description}</i>\n"
            "💰 <b>Сумма:</b> {amount} руб."
        ),
        "check_saved": "✅ Чек успешно сохранен",
        "enter_material_order": "📝 Опишите какие материалы вам нужны",
        "enter_delivery_date": "📅 Укажите желаемую дату доставки (формат: ДД.ММ.ГГГГ)",
        "date_must_be_future": "❌ Дата доставки должна быть в будущем",
        "invalid_date": "❌ Некорректная дата",
        "invalid_date_format": (
            "❌ Неверный формат даты\n\n"
            "Используйте формат: ДД.ММ.ГГГГ\n"
            "Например: 25.05.2024"
        ),
        "material_order_format": (
            "🛍 <b>Заказ материалов</b>\n\n"
            "👤 <b>Заказчик:</b> {worker_name}\n"
            "📧 Username: {username}\n\n"
            "📝 <b>Требуемые материалы:</b>\n<i>{description}</i>\n"
            "📅 <b>Желаемая дата:</b> <i>{delivery_date}</i>"
        ),
        "order_saved": "✅ Заказ материалов успешно отправлен",
        "send_material_photo": "📸 Отправьте фото материала",
        "enter_material_description": "📝 Введите описание материала",
        "enter_storage_location": "📍 Укажите место хранения материала",
        "material_remainder_format": (
            "📦 <b>Остаток материала</b>\n\n"
            "📝 <b>Описание:</b> <i>{description}</i>\n"
            "📍 <b>Место хранения:</b> <i>{location}</i>"
        ),
        "material_saved": "✅ Информация о материале сохранена",
            "transfer_tool_invalid_format": "Неверный формат команды. Используйте: /transfer_tool <ID инструмента> <получатель> <описание>",
        "transfer_tool_invalid_tool_id": "ID инструмента должно быть числом.",
        "transfer_tool_not_found": "Инструмент с указанным ID не найден.",
        "transfer_tool_format": (
            "Передача инструмента:\n"
            "Инструмент: {tool_name} (ID: {tool_id})\n"
            "Получатель: {recipient}\n"
            "Отправитель: {sender}\n"
            "Описание: {description}"
        ),
        "transfer_tool_request_sent": "Запрос на передачу инструмента отправлен.",
        "accept_tool_btn": "получить инструмент",
        "transfer_tool_receive_prompt": "Вам передают инструмент {tool_name}. Нажмите кнопку ниже, чтобы получить его.",
        "transfer_tool_recipient_not_found": "Не удалось найти пользователя с таким именем.",
        "transfer_tool_invalid_recipient": "Получатель должен быть указан через @username или telegram_id.",
        "tool_received_confirmation": "Инструмент получен!",
        "objects_btn": "Объекты",
        "report_empty_text": "Пожалуйста, введите текст отчета после команды /report",
        "report_format": (
            "Новый отчет от {sender} ({username}):\n\n"
            "{report}"
        ),
        "report_sent_confirmation": "Ваш отчет отправлен.",
        "foreman_workers_btn": "Рабочие",
        "foreman_documentation_btn": "Документация",
        "foreman_photos_btn": "Фото с объекта",
        "foreman_handover_btn": "Сдача объекта",
        "foreman_procurement_btn": "Закупка",
        "foreman_receipts_btn": "Учет чеков",
        "foreman_material_balance_btn": "Остаток материала",
        "foreman_info_btn": "Информация",
        "foreman_tools_list_btn": "Перечень инструментов",
        "foreman_mass_mailing_btn": "Рассылка по объекту",
        "foreman_offsite_accounting_btn": "Учёт вне объекта",
        "foreman_export_xlsx_btn": "Выгрузка xlsx по объекту",
        "select_object_prompt": "Пожалуйста, выберите объект для просмотра списка рабочих",
        "no_objects": "Объектов не найдено",
        'back_btn': 'Назад',
        "no_object_members": "Для выбранного объекта нет закрепленных рабочих.",
        "worker_info_format": (
            "Телеграм ID: {telegram_id}\n"
            "Username: {username}\n"
            "ФИО: {full_name}\n"
            "Телефон: {phone}\n"
            "Статус: {status}\n"
            "Объект: {object_name}"
        ),
        'select_object_action': 'Выберите действие с объектом',
        'no_object_documents': 'Для данного объекта не добавлено ни одной документации',
        'document_info_format':(
            'Тип документа: {document_type}\n'
            'Закреплен за объектом: {object_name}\n'
        ),
        "enter_handover_description": "Введите описание сдачи объекта:",
        "object_not_found": "Объект не найден",
        "handover_format": (
            "🏗 <b>Сдача объекта</b>\n\n"
            "🏢 Объект: {object_name} (ID: {object_id})\n"
            "👤 Прораб: {foreman_name}\n"
            "📧 Username: {username}\n\n"
            "📝 <b>Описание:</b>\n"
            "{description}"
        ),
        "handover_sent": "✅ Информация о сдаче объекта успешно отправлена",
        'own_expense_true_btn': 'За свой счет - ✔',
        'own_expense_false_btn': 'За свой счет - ❌',
        "expense_sheet_name": "Отчет по расходам",
        "date_column": "Дата",
        "description_column": "Описание",
        "amount_column": "Сумма",
        "expense_type_column": "Тип расхода",
        "user_column": "Пользователь",
        "own_expense": "За свой счет",
        "company_expense": "За счет компании",
        "total_amount": "Итого:",
        "prev_page_btn": "Предыдущая",
        "next_page_btn": "Следующая",
        "mock_data_cleared": "Все тестовые данные удалены",
        "invalid_photo_format": "Пожалуйста, отправьте фотографию",
        "no_workers_found": "Нет доступных рабочих в базе данных",
        "expense_report_caption": "Отчет по расходам\nПериод: {start_date} - {end_date}\nТип: {expense_type}",
        "no_expenses_found": "За указанный период расходов не найдено",
        "all_expenses_btn": "Все расходы",
        "own_expenses_btn": "За свой счёт",
        "company_expenses_btn": "За счет компании",
        "enter_start_date": "📅 Введите начальную дату отчетного периода (формат: ДД.ММ.ГГГГ)",
        "enter_end_date": "📅 Введите конечную дату отчетного периода (формат: ДД.ММ.ГГГГ)",
        "select_expense_type": "Выберите тип расходов для выгрузки:",
        "invalid_date_format": "❌ Неверный формат даты. Используйте формат ДД.ММ.ГГГГ (например: 25.12.2024)",
        "no_expenses_found": "❌ За указанный период расходов не найдено",
        "expense_report_caption": (
            "📊 Отчет по расходам\n"
            "📅 Период: {start_date} - {end_date}\n"
            "💰 Тип расходов: {expense_type}"
        ),
        "report_processing": "⏳ Формирование отчета...",
        "report_generation_error": "❌ Ошибка при формировании отчета",
        "all_expenses": "Все расходы",
        "own_expenses": "За свой счет",
        "company_expenses": "За счет компании",
        "excel_date_column": "Дата",
        "excel_description_column": "Описание",
        "excel_amount_column": "Сумма",
        "excel_expense_type_column": "Тип расхода",
        "excel_user_column": "Пользователь",
        "excel_total_row": "ИТОГО:",
        "excel_sheet_name": "Отчет по расходам",
        'reminder_out_btn': 'Учет чеков вне объектов',
        "tools_list_caption": "📊 Отчет по инструментам\n💼 Тип: {tool_status}",
        "select_tool_status": "Выберите тип инструментов для выгрузки:",
        "all_tools": "Все инструменты",
        'in_work_tools': 'Инструменты в работе',
        "free_tools": "Свободные инструменты",
        "repair_tools": "Инструменты в ремонте",
        "no_tools_found": "❌ Инструменты не найдены",
        "excel_tool_name": "Наименование",
        "excel_tool_description": "Описание",
        "excel_tool_status": "Статус",
        "excel_tool_user": "Закреплен за",
        "excel_tool_date": "Дата назначения",
        "excel_tools_sheet_name": "Перечень инструментов",

    },
    "az": {  
        "start": "Salam, {name}! Mən botam",
        "language_select": "Dil seçin:",
        "language_ru": "Rus",
        "language_az": "Azərbaycan",
        "language_tg": "Tacik",
        "request_contact": "Zəhmət olmasa, aşağıdakı düymə ilə telefon nömrənizi paylaşın.",
        "username_instruction": """
        Botdan istifadə etmək üçün istifadəçi adı yaratmaq lazımdır. Təlimatlara əməl edərək istifadəçi adınızı yaradın

        <b>Telegram-da istifadəçi adı necə yaradılır:</b>

        1. Telegram tənzimləmələrini açın
        2. "Profilinizi dəyişin" düyməsinə basın
        3. "Username" sahəsinə klikləyin
        4. İstədiyiniz istifadəçi adını daxil edin
        5. Təsdiq üçün ✓ düyməsinə basın

        İstifadəçi adı yaradıldıqdan sonra aşağıdakı "Doğrula" düyməsinə basın.""",
        "check": "Doğrula",
        "create_username": "İstifadəçi adı yarat",
        "has_no_username": "İstifadəçi adı yaratmaq üçün təlimatlara əməl edin",
        "share_contact_btn": "Əlaqəni paylaş 📱",
        "no_contact": "Klaviyaturadan istifadə edin",
        "cancel": "Ləğv et",
        "confirm": "Təsdiq et",
        "its_no_contact": "Zəhmət olmasa, klaviaturadakı düymədən istifadə edin",
        "reques_docs": "Çatda sənəd şəkillərini göndərin. Bütün sənədləri yüklədikdən sonra 'Dayandır' düyməsinə basın",
        "stop_upload_btn": "Dayandır",
        "i_got_acquainted_btn": "Məlumat əldə etdim",
        "i_got_acquainted": "Bütün təlimatları oxuduqdan sonra 'Məlumat əldə etdim' düyməsinə basın",
        "reques_fio": "Tam adınızı daxil edin",
        "ru": "Rus",
        "az": "Azərbaycan",
        "tg": "Tacik",
        "photo_received": "Şəkil alındı. Ümumi yüklənən sayı: {count}",
        "photos_saved": "Bütün şəkillər ({count}) uğurla qeyd edildi!",
        "no_photos": "Heç bir şəkil yükləməmisiniz",
        "solve_example": "İnsan olduğunuzu təsdiqləmək üçün hesabı həll edin:\n{example}",
        "verification_success": "Doğrulama uğurla tamamlandı! Qeydiyyat tamamlandı.",
        "wrong_answer": "Səhv cavab. Zəhmət olmasa, başqa hesabı həll edin:\n{example}",
        "not_a_number": "Zəhmət olmasa, ədəd daxil edin.",
        "report_accepted": "Hesabat qəbul edildi",
        "report_error": "Mesaj göndərilərkən xəta baş verdi.",
        "profile_btn": "Profil",
        "my_objects_btn": "Mənim obyektlərim",
        "material_remainder_btn": "Material qalığı",
        "material_order_btn": "Material sifarişi",
        "info_btn": "Məlumat",
        "instructions": "Botdan istifadə təlimatları",
        "rules": "İstifadə qaydaları",
        "profile_info": (
            "👤 <b>Profil</b>\n\n"
            "🆔 Telegram ID: <code>{telegram_id}</code>\n"
            "📧 İstifadəçi adı: @{username}\n"
            "👨‍💼 Ad, Soyad: {full_name}\n"
            "📱 Telefon: {phone}\n"
            "📊 Vəzifə: {role}"
        ),
        "tools_list_btn": "Alətlər",
        "language_select_btn": "Dil seçimi",
        "rules_btn": "Qaydalar",
        "no_tools": "Sizə heç bir alət təyin edilməyib",
        "tools_list_header": "🛠 <b>Təyin olunmuş alətlərin siyahısı:</b>",
        "tool_item": "<b>{name}</b>\n📝 Təsvir: <i>{description}</i>",
        "no_description": "Təsvir yoxdur",
        "lang_has_changed": "Botun dili dəyişdirildi",
        "no_objects": "Sizin heç bir obyektiniz yoxdur",
        "objects_list_header": "🏗 <b>Sizin obyektləriniz:</b>",
        "object_item": "🔹 <b>{name}</b>\n📝 <i>{description}</i>",
        "navigation_btn": "📍 Naviqasiya",
        "documentation_btn": "📄 Sənədləşmə",
        "notify_object_btn": "📢 Obyekti xəbərdar et",
        "object_photo_btn": "📸 Obyektdən şəkil",
        "object_checks_btn": "🧾 Çeklərin uçotu",
        "no_navigation": "Bu obyekt üçün naviqasiya əlavə edilməyib",
        "enter_notification": "Bütün obyekt iştirakçılarına göndərmək üçün mesaj daxil edin",
        "notification_format": (
            "📢 <b>Obyektdən xəbərdarlıq {object_id}</b>\n\n"
            "👤 <b>Göndərən:</b> {sender_name}\n"
            "📧 İstifadəçi adı: {username}\n\n"
            "💬 <b>Mesaj:</b>\n<i>{message}</i>"
        ),
        "notification_sent": "✅ Obyekt iştirakçılarına xəbərdarlıq göndərildi",
        "send_object_photo": "📸 Obyektdən şəkil göndərin",
        "enter_photo_description": "📝 Şəkil üçün təsvir daxil edin",
        "object_photo_format": (
            "📸 <b>Obyektdən şəkil #{object_id}</b>\n\n"
            "👤 <b>Göndərən:</b> {worker_name}\n"
            "📧 İstifadəçi adı: {username}\n\n"
            "📝 <b>Təsvir:</b>\n<i>{description}</i>"
        ),
        "photo_sent": "✅ Şəkil uğurla göndərildi",
        "send_photo_only": "❌ Zəhmət olmasa, şəkil göndərin",
        "send_check_photo_and_description": "📸 Çekin şəklini və təsvirini göndərin",
        "enter_check_amount": "💰 Çekin məbləğini daxil edin (yalnız rəqəmlər)",
        "invalid_amount": "❌ Məbləğ formatı səhvdir. Məsələn: 1234.56",
        "check_format": (
            "🧾 <b>Obyektdən çek #{object_id}</b>\n\n"
            "👤 <b>Göndərən:</b> {worker_name}\n"
            "📧 İstifadəçi adı: {username}\n\n"
            "📝 <b>Təsvir:</b> <i>{description}</i>\n"
            "💰 <b>Məbləğ:</b> {amount} AZN"
        ),
        "check_saved": "✅ Çek uğurla qeyd edildi",
        "enter_material_order": "📝 Lazım olan materialları təsvir edin",
        "enter_delivery_date": "📅 İstədiyiniz çatdırılma tarixini daxil edin (format: G.GG.AAAA)",
        "date_must_be_future": "❌ Çatdırılma tarixi gələcəkdə olmalıdır",
        "invalid_date": "❌ Tarix yanlışdır",
        "invalid_date_format": (
            "❌ Tarix formatı səhvdir\n\n"
            "G.GG.AAAA formatını istifadə edin\n"
            "Məsələn: 25.05.2024"
        ),
        "material_order_format": (
            "🛍 <b>Material sifarişi</b>\n\n"
            "👤 <b>Sifarişçi:</b> {worker_name}\n"
            "📧 İstifadəçi adı: {username}\n\n"
            "📝 <b>Lazım olan materiallar:</b>\n<i>{description}</i>\n"
            "📅 <b>İstədiyiniz tarix:</b> <i>{delivery_date}</i>"
        ),
        "order_saved": "✅ Material sifarişi göndərildi",
        "send_material_photo": "📸 Materialın şəklini göndərin",
        "enter_material_description": "📝 Materialın təsvirini daxil edin",
        "enter_storage_location": "📍 Materialın saxlanma yerini daxil edin",
        "material_remainder_format": (
            "📦 <b>Material qalığı</b>\n\n"
            "📝 <b>Təsvir:</b> <i>{description}</i>\n"
            "📍 <b>Saxlanma yeri:</b> <i>{location}</i>"
        ),
        "material_saved": "✅ Material məlumatı yadda saxlanıldı",
        "transfer_tool_invalid_format": "Əmr formatı səhvdir. Belə istifadə edin: /transfer_tool <ALƏTİN ID-si> <alıcı> <təsvir>",
        "transfer_tool_invalid_tool_id": "Alətin ID-si rəqəm olmalıdır.",
        "transfer_tool_not_found": "Göstərilən ID ilə alət tapılmadı.",
        "transfer_tool_format": (
            "Alətin ötürülməsi:\n"
            "Alət: {tool_name} (ID: {tool_id})\n"
            "Alıcı: {recipient}\n"
            "Göndərən: {sender}\n"
            "Təsvir: {description}"
        ),
        "transfer_tool_request_sent": "Alətin ötürülməsi üçün sorğu göndərildi.",
        "accept_tool_btn": "aləti qəbul et",
        "transfer_tool_receive_prompt": "Sizə {tool_name} aləti ötürülür. Qəbul etmək üçün aşağıdakı düyməyə basın.",
        "transfer_tool_recipient_not_found": "Belə istifadəçi tapılmadı.",
        "transfer_tool_invalid_recipient": "Alıcı @istifadəçi_adı və ya telegram_id ilə göstərilməlidir.",
        "tool_received_confirmation": "Alət alındı!",
        "objects_btn": "Obyektlər",
        "report_empty_text": "Zəhmət olmasa, /report əmri sonrası hesabat mətni daxil edin",
        "report_format": (
            "Yeni hesabat göndərildi {sender} ({username}):\n\n"
            "{report}"
        ),
        "report_sent_confirmation": "Hesabatınız göndərildi.",
        "foreman_workers_btn": "İşçilər",
        "foreman_documentation_btn": "Sənədləşmə",
        "foreman_photos_btn": "Obyektdən şəkillər",
        "foreman_handover_btn": "Obyekti təhvil ver",
        "foreman_procurement_btn": "Alqı-satqı",
        "foreman_receipts_btn": "Çeklərin uçotu",
        "foreman_material_balance_btn": "Material balansı",
        "foreman_info_btn": "Məlumat",
        "foreman_tools_list_btn": "Alətlərin siyahısı",
        "foreman_mass_mailing_btn": "Obyekt üzrə kütləvi göndərmə",
        "foreman_offsite_accounting_btn": "Obyektdən kənar uçot",
        "foreman_export_xlsx_btn": "Obyektdən xlsx ixrac",
        "select_object_prompt": "Əməkdaşların siyahısını görmək üçün obyekt seçin",
        "no_objects": "Obyekt tapılmadı",
        "back_btn": "Geri",
        "no_object_members": "Seçilmiş obyekt üçün heç bir işçi təyin edilməyib.",
        "worker_info_format": (
            "Telegram ID: {telegram_id}\n"
            "İstifadəçi adı: {username}\n"
            "Ad, Soyad: {full_name}\n"
            "Telefon: {phone}\n"
            "Vəzifə: {status}\n"
            "Obyekt: {object_name}"
        ),
        "select_object_action": "Obyektlə bağlı əməliyyatı seçin",
        "no_object_documents": "Bu obyekt üçün heç bir sənəd əlavə edilməyib",
        "document_info_format": (
            "Sənəd növü: {document_type}\n"
            "Təyin olunan obyekt: {object_name}\n"
        ),
        "enter_handover_description": "Obyekti təhvil vermə haqqında təsviri daxil edin:",
        "object_not_found": "Obyekt tapılmadı",
        "handover_format": (
            "🏗 <b>Obyekti təhvil vermə</b>\n\n"
            "🏢 Obyekt: {object_name} (ID: {object_id})\n"
            "👤 İşəgötürən: {foreman_name}\n"
            "📧 İstifadəçi adı: {username}\n\n"
            "📝 <b>Təsvir:</b>\n"
            "{description}"
        ),
        "handover_sent": "✅ Obyektin təhvil verilməsi uğurla göndərildi",
        "own_expense_true_btn": "Öz vəsaitləri - ✔",
        "own_expense_false_btn": "Öz vəsaitləri - ❌",
        "expense_sheet_name": "Xərc hesabatı",
        "date_column": "Tarix",
        "description_column": "Təsvir",
        "amount_column": "Məbləğ",
        "expense_type_column": "Xərc növü",
        "user_column": "İstifadəçi",
        "own_expense": "Öz vəsaitləri",
        "company_expense": "Şirkət vəsaitləri",
        "total_amount": "Ümumi:",
        "prev_page_btn": "Əvvəlki",
        "next_page_btn": "Növbəti",
        "mock_data_cleared": "Bütün test məlumatları silindi",
        "invalid_photo_format": "Zəhmət olmasa, şəkil göndərin",
        "no_workers_found": "Bazada işçi tapılmadı",
        "expense_report_caption": "Xərc hesabatı\nMüddət: {start_date} - {end_date}\nNöv: {expense_type}",
        "no_expenses_found": "Göstərilən dövrdə xərc tapılmadı",
        "all_expenses_btn": "Bütün xərclər",
        "own_expenses_btn": "Öz xərc",
        "company_expenses_btn": "Şirkət xərc",
        "enter_start_date": "📅 Hesabat dövrünün başlanğıc tarixini daxil edin (format: G.GG.AAAA)",
        "enter_end_date": "📅 Hesabat dövrünün son tarixini daxil edin (format: G.GG.AAAA)",
        "select_expense_type": "Çıxarış üçün xərc növünü seçin:",
        "invalid_date_format": "❌ Tarix formatı səhvdir. G.GG.AAAA formatını istifadə edin (məsələn: 25.12.2024)",
        "no_expenses_found": "❌ Göstərilən dövrdə xərc tapılmadı",
        "expense_report_caption": (
            "📊 Xərc hesabatı\n"
            "📅 Müddət: {start_date} - {end_date}\n"
            "💰 Xərc növü: {expense_type}"
        ),
        "report_processing": "⏳ Hesabat hazırlanır...",
        "report_generation_error": "❌ Hesabat hazırlanarkən xəta baş verdi",
        "all_expenses": "Bütün xərclər",
        "own_expenses": "Öz xərc",
        "company_expenses": "Şirkət xərc",
        "excel_date_column": "Tarix",
        "excel_description_column": "Təsvir",
        "excel_amount_column": "Məbləğ",
        "excel_expense_type_column": "Xərc növü",
        "excel_user_column": "İstifadəçi",
        "excel_total_row": "CƏMİ:",
        "excel_sheet_name": "Xərc hesabatı",
        "reminder_out_btn": "Obyektdən kənar çeklərin uçotu"

    },
    "tg": {
        "start": "Салом, {name}! Ман ботам",
        "language_select": "Забонро интихоб кунед:",
        "language_ru": "Русӣ",
        "language_az": "Азербаёнӣ",
        "language_tg": "Тоҷикӣ",
        "request_contact": "Лутфан, бо тугмаи зерини зерин, нумӯи телефонӣ худро мубодила кунед.",
        "username_instruction": """
    Барои истифодаи бот, зарурати эҷоди номи корбарӣ вуҷуд дорад. Илтимос, дастурҳоро риоя кунед:

    <b>Чӣ тавр дар Telegram номи корбариро эҷод мекунем:</b>

    1. Танзимоти Telegram-ро кушоед
    2. Ба "Тағйир додани профил" пахш кунед
    3. Ба майдони "Username" пахш кунед
    4. Номи дилхоҳро ворид кунед
    5. Барои сабт, тугмаи ✓-ро пахш кунед

    Пас аз эҷод, тугмаи "Санҷидан" -ро пахш кунед.
    """,
        "check": "Санҷидан",
        "create_username": "Эҷоди номи корбарӣ",
        "has_no_username": "Барои эҷоди номи корбарӣ, илтимос дастурҳоро риоя кунед",
        "share_contact_btn": "Шарики телефон 📱",
        "no_contact": "Аз клавиатура истифода кунед",
        "cancel": "Инкор",
        "confirm": "Тасдиқ кунед",
        "its_no_contact": "Лутфан, аз тугмаи клавиатура истифода баред",
        "reques_docs": "Лутфан, ҳуҷҷатҳо ва аксҳоро дар чат фиристед. Пас аз фиристодани ҳамаи ҳуҷҷатҳо, тугмаи 'Прекирати' -ро пахш кунед.",
        "stop_upload_btn": "Прекирати",
        "i_got_acquainted_btn": "Ман огоҳ шудам",
        "i_got_acquainted": "Агар ҳамаи дастурҳоро фаҳмидед, тугмаи 'Ман огоҳ шудам' -ро пахш кунед",
        "reques_fio": "Ному насабро ворид кунед",
        "ru": "Русӣ",
        "az": "Азербаёнӣ",
        "tg": "Тоҷикӣ",
        "photo_received": "Акс қабул шуд. Умумӣ: {count}",
        "photos_saved": "Ҳама аксҳо ({count}) муваффақона сабт шуданд!",
        "no_photos": "Шумо ҳеҷ акси фиристода накардаед",
        "solve_example": "Барои тасдиқи шахсият, лутфан, масъалаеро ҳал кунед:\n{example}",
        "verification_success": "Тасдиқ муваффақ шуд! Рӯйхати сабт ба хубӣ анҷом ёфт.",
        "wrong_answer": "Ҷавоби нодуруст. Лутфан, масъалаи дигареро ҳал кунед:\n{example}",
        "not_a_number": "Лутфан, рақамро ворид кунед.",
        "report_accepted": "Ҳисобот қабул шуд",
        "report_error": "Дар фиристодани паём хатогӣ рӯй дод",
        "profile_btn": "Профил",
        "my_objects_btn": "Объектҳои ман",
        "material_remainder_btn": "Миқдори моддаҳо",
        "material_order_btn": "Фармоиши моддаҳо",
        "info_btn": "Маълумот",
        "instructions": "Дастурҳои истифодаи бот",
        "rules": "Қоидаҳои истифода",
        "profile_info": (
            "👤 <b>Профил</b>\n\n"
            "🆔 Telegram ID: <code>{telegram_id}</code>\n"
            "📧 Username: @{username}\n"
            "👨‍💼 Ному насаб: {full_name}\n"
            "📱 Телефон: {phone}\n"
            "📊 Ҳолат: {role}"
        ),
        "tools_list_btn": "Абзорҳо",
        "language_select_btn": "Интихоби забон",
        "rules_btn": "Қоидаҳо",
        "no_tools": "Барои шумо ҳеҷ абзоре муайн нашудааст",
        "tools_list_header": "🛠 <b>Рӯйхати абзорҳои муайншаванда:</b>",
        "tool_item": "<b>{name}</b>\n📝 Шарҳ: <i>{description}</i>",
        "no_description": "Шарҳи мавҷуд нест",
        "lang_has_changed": "Забони бот иваз шуд",
        "no_objects": "Шумо объектҳои дастрас надоред",
        "objects_list_header": "🏗 <b>Объектҳои шумо:</b>",
        "object_item": "🔹 <b>{name}</b>\n📝 <i>{description}</i>",
        "navigation_btn": "📍 Навигатсия",
        "documentation_btn": "📄 Документация",
        "notify_object_btn": "📢 Огоҳ кардани объект",
        "object_photo_btn": "📸 Акс аз объект",
        "object_checks_btn": "🧾 Ҳисоботи чекҳо",
        "no_navigation": "Барои ин объект навигатсия илова нашудааст",
        "enter_notification": "Лутфан, паёми барои фиристодани ба ҳамаи аъзои объектро ворид кунед",
        "notification_format": (
            "📢 <b>Огоҳнома аз объект {object_id}</b>\n\n"
            "👤 <b>Фиристанда:</b> {sender_name}\n"
            "📧 Username: {username}\n\n"
            "💬 <b>Паём:</b>\n<i>{message}</i>"
        ),
        "notification_sent": "✅ Огоҳнома ба ҳамаи аъзои объект фиристода шуд",
        "send_object_photo": "📸 Лутфан, акс аз объектро фиристед",
        "enter_photo_description": "📝 Тасвири аксро ворид кунед",
        "object_photo_format": (
            "📸 <b>Акс аз объект #{object_id}</b>\n\n"
            "👤 <b>Фиристанда:</b> {worker_name}\n"
            "📧 Username: {username}\n\n"
            "📝 <b>Тасвир:</b>\n<i>{description}</i>"
        ),
        "photo_sent": "✅ Акс муваффақона фиристода шуд",
        "send_photo_only": "❌ Лутфан, танҳо акс фиристед",
        "send_check_photo_and_description": "📸 Лутфан, акс ва тасвири чекро фиристед",
        "enter_check_amount": "💰 Лутфан, миқдори чекро (фақат рақам) ворид кунед",
        "invalid_amount": "❌ Формати миқдор нодуруст. Масалан: 1234.56",
        "check_format": (
            "🧾 <b>Чек аз объект #{object_id}</b>\n\n"
            "👤 <b>Фиристанда:</b> {worker_name}\n"
            "📧 Username: {username}\n\n"
            "📝 <b>Тасвир:</b> <i>{description}</i>\n"
            "💰 <b>Миқдор:</b> {amount} руб."
        ),
        "check_saved": "✅ Чек муваффақона сабт шуд",
        "enter_material_order": "📝 Лутфан, талаботи моддаҳоро ворид кунед",
        "enter_delivery_date": "📅 Лутфан, таърихи дилхоҳ барои расондани моддаҳоро (Формат: ДД.ММ.ЙЙЙЙ) ворид кунед",
        "date_must_be_future": "❌ Таърих бояд дар оянда бошад",
        "invalid_date": "❌ Таърих нодуруст аст",
        "invalid_date_format": (
            "❌ Формати таърих нодуруст\n\n"
            "Формат: ДД.ММ.ЙЙЙЙ\n"
            "Масалан: 25.05.2024"
        ),
        "material_order_format": (
            "🛍 <b>Фармоиши моддаҳо</b>\n\n"
            "👤 <b>Фармоишкунанда:</b> {worker_name}\n"
            "📧 Username: {username}\n\n"
            "📝 <b>Талаботи моддаҳо:</b>\n<i>{description}</i>\n"
            "📅 <b>Таърихи дилхоҳ:</b> <i>{delivery_date}</i>"
        ),
        "order_saved": "✅ Фармоиши моддаҳо муваффақона фиристода шуд",
        "send_material_photo": "📸 Лутфан, акс аз моддаҳоро фиристед",
        "enter_material_description": "📝 Тасвири моддаҳоро ворид кунед",
        "enter_storage_location": "📍 Лутфан, маҳали нигоҳдориро ворид кунед",
        "material_remainder_format": (
            "📦 <b>Қолишхои моддаҳо</b>\n\n"
            "📝 <b>Тасвир:</b> <i>{description}</i>\n"
            "📍 <b>Ҷойгиршавӣ:</b> <i>{location}</i>"
        ),
        "material_saved": "✅ Маълумоти моддаҳо сабт шуд",
        "transfer_tool_invalid_format": "Формати фармон нодуруст. Истифода кунед: /transfer_tool <ID абзор> <гирифтор> <тасвир>",
        "transfer_tool_invalid_tool_id": "ID абзор бояд рақам бошад.",
        "transfer_tool_not_found": "Абзоре бо ин ID ёфт нашуд.",
        "transfer_tool_format": (
            "Интиқоли абзор:\n"
            "Абзор: {tool_name} (ID: {tool_id})\n"
            "Гирифтор: {recipient}\n"
            "Фиристанда: {sender}\n"
            "Тасвир: {description}"
        ),
        "transfer_tool_request_sent": "Дархости интиқоли абзор фиристода шуд.",
        "accept_tool_btn": "Абзорро қабул кунед",
        "transfer_tool_receive_prompt": "Ба шумо абзоре интиқол дода мешавад: {tool_name}. Лутфан, тугмаи зерини қабул кунед.",
        "transfer_tool_recipient_not_found": "Истифодабарандаи зикршуда ёфт нашуд.",
        "transfer_tool_invalid_recipient": "Гирифтор бояд бо @username ё telegram_id зикршуда бошад.",
        "tool_received_confirmation": "Абзор қабул шуд!",
        "objects_btn": "Объектҳо",
        "report_empty_text": "Лутфан, матни ҳисоботро пас аз фармони /report ворид кунед",
        "report_format": (
            "Ҳисоботи нав аз {sender} ({username}):\n\n"
            "{report}"
        ),
        "report_sent_confirmation": "Ҳисоботи шумо фиристода шуд.",
        "foreman_workers_btn": "Коргон",
        "foreman_documentation_btn": "Документация",
        "foreman_photos_btn": "Аксҳо аз объект",
        "foreman_handover_btn": "Гузоштани объект",
        "foreman_procurement_btn": "Харидани моддаҳо",
        "foreman_receipts_btn": "Ҳисоботи чекҳо",
        "foreman_material_balance_btn": "Баланс моддаҳо",
        "foreman_info_btn": "Маълумот",
        "foreman_tools_list_btn": "Рӯйхати абзорҳо",
        "foreman_mass_mailing_btn": "Почтаи ҷамъӣ барои объект",
        "foreman_offsite_accounting_btn": "Ҳисоботи берун аз объект",
        "foreman_export_xlsx_btn": "Икспорти xlsx барои объект",
        "select_object_prompt": "Лутфан, барои дидани рӯйхати коргон, объектро интихоб кунед",
        "no_objects": "Объектҳо ёфт нашуд",
        "back_btn": "Бозгаштан",
        "no_object_members": "Барои интихобшуда ҳеҷ коргари муайян набуд.",
        "worker_info_format": (
            "Telegram ID: {telegram_id}\n"
            "Username: {username}\n"
            "Ному насаб: {full_name}\n"
            "Телефон: {phone}\n"
            "Ҳолат: {status}\n"
            "Объект: {object_name}"
        ),
        "select_object_action": "Лутфан, амалияи объектро интихоб кунед",
        "no_object_documents": "Барои ин объект ҳеҷ ҳуҷҷате замима нашудааст",
        "document_info_format": (
            "Навъи ҳуҷҷат: {document_type}\n"
            "Объекти муайян: {object_name}\n"
        ),
        "enter_handover_description": "Лутфан, тасвири гузоштани объектро ворид кунед:",
        "object_not_found": "Объект ёфт нашуд",
        "handover_format": (
            "🏗 <b>Гузоштани объект</b>\n\n"
            "🏢 Объект: {object_name} (ID: {object_id})\n"
            "👤 Роҳбари объект: {foreman_name}\n"
            "📧 Username: {username}\n\n"
            "📝 <b>Тасвир:</b>\n"
            "{description}"
        ),
        "handover_sent": "✅ Маълумоти гузоштани объект муваффақона фиристода шуд",
        "own_expense_true_btn": "Аз ҳисоби худ - ✔",
        "own_expense_false_btn": "Аз ҳисоби худ - ❌",
        "expense_sheet_name": "Ҳисоби хароҷот",
        "date_column": "Таърих",
        "description_column": "Тасвир",
        "amount_column": "Миқдор",
        "expense_type_column": "Навъи хароҷот",
        "user_column": "Истифодабаранда",
        "own_expense": "Аз ҳисоби худ",
        "company_expense": "Аз ҳисоби ширкат",
        "total_amount": "Ҳамагӣ:",
        "prev_page_btn": "Сафҳаи қаблӣ",
        "next_page_btn": "Сафҳаи баъдӣ",
        "mock_data_cleared": "Ҳама маълумоти озмоишӣ тоза шуд",
        "invalid_photo_format": "Лутфан, аксро фиристед",
        "no_workers_found": "Ҳеҷ коргари дастрас дар пойгоҳи додаҳо ёфт нашуд",
        "expense_report_caption": "Ҳисоби хароҷот\nМуҳлати: {start_date} - {end_date}\nНав: {expense_type}",
        "no_expenses_found": "Дар давраи зикршуда хароҷот ёфт нашуд",
        "all_expenses_btn": "Ҳама хароҷот",
        "own_expenses_btn": "Ҳароҷоти шахсӣ",
        "company_expenses_btn": "Ҳароҷоти ширкат",
        "enter_start_date": "📅 Лутфан, таърихи оғози давраи ҳисоботро (Формат: ДД.ММ.ЙЙЙЙ) ворид кунед",
        "enter_end_date": "📅 Лутфан, таърихи поёни давраи ҳисоботро (Формат: ДД.ММ.ЙЙЙЙ) ворид кунед",
        "select_expense_type": "Лутфан, навъи хароҷотро барои ҳисобот интихоб кунед:",
        "invalid_date_format": "❌ Формати таърих нодуруст. Масалан: 25.12.2024 (Формат: ДД.ММ.ЙЙЙЙ)",
        "no_expenses_found": "❌ Дар давраи зикршуда хароҷот ёфт нашуд",
        "expense_report_caption": (
            "📊 Ҳисоби хароҷот\n"
            "📅 Муҳлат: {start_date} - {end_date}\n"
            "💰 Навъи хароҷот: {expense_type}"
        ),
        "report_processing": "⏳ Ҳисобот дар ҳолати истеҳсол...",
        "report_generation_error": "❌ Дар истеҳсоли ҳисобот хатогӣ рӯй дод",
        "all_expenses": "Ҳама хароҷот",
        "own_expenses": "Ҳароҷоти шахсӣ",
        "company_expenses": "Ҳароҷоти ширкат",
        "excel_date_column": "Таърих",
        "excel_description_column": "Тасвир",
        "excel_amount_column": "Миқдор",
        "excel_expense_type_column": "Навъи хароҷот",
        "excel_user_column": "Истифодабаранда",
        "excel_total_row": "ҶАМ:",
        "excel_sheet_name": "Ҳисоби хароҷот",
        "reminder_out_btn": "Ҳисоби чекҳои берун аз объект",
        
    },
}
