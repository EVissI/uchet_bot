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
            'Тип документа: {document_type}\n',
            'Закреплен за объектом: {object_name}\n',
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
    },
    "az": {},
    "tg": {},
}
