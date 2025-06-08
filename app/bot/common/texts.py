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
        'reminder_delete_canceled':'Удаление остатков отменено',
        'reminder_deleted':'Остатки деактивированны',
        'reminder_not_found':'Остатки не были найденны',
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
        "tool_item": "<b>{name}</b>\nid:<code>{tool_id}</code>\n📝 Описание: <i>{description}</i>",
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
        "no_users_found": "❌ Пользователи не найдены",
        "no_objects_found": "❌ Объекты не найдены",
        "no_members_found": "❌ На объекте нет участников",
        "select_object_for_notification": "📋 Выберите объект для рассылки уведомления:",
        "enter_notification_text": "📝 Введите текст уведомления для рассылки:",
        "sending_notifications_status": "📤 Отправка уведомлений... {sent}/{total}",
        "notifications_sent_status": "✅ Рассылка завершена\n\n📊 Всего: {total}\n✅ Успешно: {success}\n❌ Не доставлено: {failed}",
        "admin_notify_all_users_inline_btn": "📢 Всем пользователям",
        "admin_notify_object_inline_btn": "🏗 По объекту",
        "admin_notify_all_user_w8_message": "📝 Введите текст для рассылки всем пользователям:",
                "transfer_tool_force_format": (
            "🔄 Принудительная передача инструмента\n"
            "🛠 Инструмент: {tool_name} (ID: {tool_id})\n"
            "👤 Получатель: {recipient}\n"
            "👨‍💼 Администратор: {admin}\n"
            "📝 Описание: {description}"
        ),
        "transfer_tool_force_complete": "✅ Инструмент принудительно передан",
        "transfer_tool_force_received": "🔄 Администратор {admin} передал вам инструмент: {tool_name}",
        "transfer_tool_admin_format": (
            "Формат команды:\n"
            "/transfer_tool <инструмент_ID> <получатель> <описание>\n"
            "Для принудительной передачи (только админы):\n"
            "/transfer_tool <инструмент_ID> <получатель> -f <описание>"
        ),
        "admin_notify": "Выберите тип рассылки:",
        "create_object_name": "📝 Введите название объекта:",
        "operation_cancelled": "❌ Операция отменена",
        "caption_required": "❌ Необходимо добавить описание к фото в подписи",
        "select_document_type": "Выберите тип документа:",
        "doc_type_estimate": "📊 Смета",
        "doc_type_technical": "📋 Техническое задание", 
        "doc_type_contacts": "📞 Контакты заказчика",
        "create_object_success": "✅ Объект успешно создан",
        "notification_sent_to_all": "✅ Уведомление отправлено всем пользователям",
        "create_object_no_documents": "❌ Документы не были загружены",
        "create_object_description": "📝 Введите описание объекта:",
        "pagination_error": "❌ Ошибка при обновлении страницы",
        "objects_list": "📋 Список объектов:",
        "object_name": "Объект: {name}",
        "updated_success": "✅ Данные успешно обновлены",
        "error_occurred": "❌ Произошла ошибка",
                "document_upload_complete": "✅ Загрузка документов завершена",
        "document_type_selected": "✅ Тип документа выбран",
        "document_saved": "✅ Документ сохранен",
        "upload_more_documents": "📤 Загрузите следующий документ или нажмите 'Завершить'",
        "foreman_panel": "👨‍💼 Панель прораба",
        "object_members_header": "👥 Участники объекта:",
        "member_item_format": (
            "👤 {full_name}\n"
            "📱 {phone}\n"
            "📧 @{username}"
        ),
        "admin_panel": "👨‍💼 Панель администратора",
        "object_control": "🏗 Управление объектами",
        "user_control": "👥 Управление пользователями",
        "create_object_btn": "➕ Создать объект",
        "edit_object_btn": "✏️ Редактировать объект",
        "delete_object_btn": "🗑 Удалить объект",
        "access_denied": "❌ Доступ запрещен",
        "invalid_input": "❌ Неверный ввод",
        "action_cancelled": "❌ Действие отменено",
        "try_again": "🔄 Попробуйте снова",
        "processing": "⏳ Обработка...",
        "saving_data": "💾 Сохранение данных...",
        "loading_data": "📥 Загрузка данных...",
        "tool_status_active": "✅ В работе",
        "tool_status_free": "🆓 Свободен",
        "tool_status_repair": "🔧 В ремонте",
        "tool_transfer_success": "✅ Инструмент успешно передан",
        "object_active": "✅ Активен",
        "object_completed": "🏁 Завершен",
        "object_suspended": "⏸ Приостановлен",
        "confirm_action": "Подтвердите действие:",
        "confirm_delete": "❗️ Подтвердите удаление",
        "confirm_cancel": "❗️ Подтвердите отмену",
        "tmc_template_instruction": (
        "📝 Инструкция по заполнению:\n\n"
        "1. Наименование* - название инструмента\n"
        "2. Количество* - число единиц\n"
        "3. Описание - дополнительная информация\n"
        "4. Статус - свободный/занят/в ремонте\n"
        "5. File ID - ID фото инструмента\n\n"
        "* - обязательные поля"),
        "tmc_template_sheet": "Шаблон инструментов",
        "excel_tool_quantity": "Количество*", 
        "excel_tool_file_id": "File ID фото",
        "tmc_enter_name": "📝 Введите наименование инструмента",
        "tmc_enter_quantity": "🔢 Введите количество инструментов",
        "tmc_enter_description": "📝 Введите описание инструмента (необязательно)",
        "tmc_upload_complete": "✅ Добавлено инструментов: {name} x{count}",
        "tmc_file_error": "❌ Ошибка при обработке файла",
        "tmc_invalid_quantity": "❌ Количество должно быть положительным числом",
        "tmc_save_error": "❌ Ошибка при сохранении инструментов",
        "materials_sheet_name": "Остатки материалов",
        "excel_material_id": "ID",
        "excel_material_description": "Описание",
        "excel_material_location": "Место хранения",
        "no_materials_found": "❌ Материалы не найдены",
        "materials_export_complete": "✅ Выгружено материалов: {count}",
        "materials_export_error": "❌ Ошибка при выгрузке материалов",
        "material_card_format": (
            "📦 Материал #{id}\n\n"
            "📝 Описание: {description}\n"
            "📍 Место хранения: {location}\n"
        ),

        "send_photo_for_file_id": "📸 Отправьте фото для получения File ID",
        "file_id_generated": "✅ File ID сгенерирован:\n{file_id}",
        "file_id_generation_error": "❌ Ошибка при генерации File ID",
        "stop_btn": "⛔️ Прекратить",
        "generate_file_id_btn": "🆔 Получить File ID",
        "materials_excel_btn": "📊 Выгрузить остатки",
        "bulk_transfer_btn": "📦 Массовая передача",
        "template_error": "❌ Ошибка при создании шаблона",
        "template_instruction": "📝 Заполните шаблон согласно инструкции и загрузите обратно",
            "bulk_transfer_instruction": "📝 Инструкция по массовой передаче инструментов",
        "bulk_transfer_report": (
            "📊 Отчет о передаче:\n\n"
            "✅ Успешно:\n{success}\n\n"
            "❌ Ошибки:\n{failed}"
        ),
        "bulk_transfer_no_file": "❌ Файл не загружен",
        "bulk_transfer_complete": "✅ Передача инструментов завершена",
        "check_out_object_format": (
            "🧾 <b>Чек вне объекта</b>\n\n"
            "👤 <b>Отправитель:</b> {worker_name}\n"
            "📧 Username: {username}\n\n"
            "📝 <b>Описание:</b> <i>{description}</i>\n"
            "💰 <b>Сумма:</b> {amount} руб."
        ),

        "choose_reminder": (
        "📦 <b>Информация о материале:</b>\n\n"
        "📝 <b>Описание:</b> <i>{description}</i>\n"
        "📍 <b>Место хранения:</b> <i>{storage_location}</i>\n"
        ),
        "send_file": "📤 Отправьте файл",
        "file_processing": "⏳ Обработка файла...",
        "file_error": "❌ Ошибка при обработке файла",
        "enter_new_photo": "📸 Отправьте новое фото",
        "reminder_photo_updated": "✅ Фото материала обновлено",
        "reminder_description_updated": "✅ Описание материала обновлено",
        "reminder_location_updated": "✅ Место хранения обновлено",

        "excel_bulk_transfer_sheet": "Массовая передача",
        "excel_bulk_transfer_tool_id": "ID инструмента*",
        "excel_bulk_transfer_recipient": "Получатель*",
        "excel_bulk_transfer_description": "Описание",

        "invalid_recipient": "❌ Неверно указан получатель",
        "invalid_tool_id": "❌ Неверный ID инструмента",
        "tool_not_found": "❌ Инструмент не найден",
        "recipient_not_found": "❌ Получатель не найден",
        "success_transfer": "✅ Успешно передано",
        "out_object_check_saved": "✅ Чек сохранен и отправлен в группу",
        "profic_accounting_btn": "💰 Учет прибыли",
        "select_object_for_profic": "📋 Выберите объект для учета:",
        "select_payment_type": "💳 Выберите тип операции:",
        "enter_payment_amount": "💰 Введите сумму:",
        "enter_payment_purpose": "📝 Введите назначение платежа:",
        "invalid_amount": "❌ Неверный формат суммы. Введите число, например: 1234.56",
        "profic_saved": "✅ {type} на сумму {amount} руб. добавлен",
        "profic_save_error": "❌ Ошибка при сохранении операции",
        "reminder_out_object_btn": "📦 Остатки вне объекта",
        "instrument_control_btn": "🛠 Управление инструментами",
        "material_remainder_control_btn": "📦 Управление остатками материала",
        "reminder_btn": "🔔 Остатки",
        "object_control_btn": "🏗 Управление объектами",
        "notify_btn": "📢 Уведомления",
        "cancel_btn": "❌ Отмена",
        "add_worker_to_object_btn": "👥 Добавить рабочего",
        "bulk_transfer_btn": "📦 Массовая передача",
        "user_tools_list_btn": "📋 Список инструментов",
        "change_reminder_btn": "✏️ Изменить остатки",
        "deactivate_reminder_btn": "❌ Деактивировать остатки",
        "create_material_reminder_btn": "➕ Создать остатки",
        "excel_view_btn": "📊 Excel выгрузка",
        "change_deactivate_btn": "✏️ Изменить/Деактивировать",
        "add_worker_to_object_text": "📋 Выберите объект, куда нужно добавить рабочего:",
        "add_worker_to_object_w8_ids": (
            "🏗 Объект: <b>{object_name}</b>\n\n"
            "📝 Введите Telegram ID рабочих через запятую (например: 123456789, 987654321)"
        ),
        "no_valid_user_ids": "❌ Не найдено корректных Telegram ID",
        "no_valid_users_found": "❌ Не найдено пользователей с указанными ID",
        "members_added_successfully": (
            "📊 Результат добавления рабочих:\n\n"
            "✅ Успешно добавлено: {success_count}\n"
            "❌ Не добавлено: {failed_count}\n\n"
            "❗️ Причины отказа:\n"
            "{failed_reasons}"
        ),
        "enter_new_description": "📝 Введите новое описание",
        "reminder_deactivated": "✅ Напоминание деактивировано",
        "reminder_updated": "✅ Напоминание обновлено",
        "object_control_title": "🏗 Управление объектами",
        "object_deleted": "✅ Объект удален",
        "object_updated": "✅ Данные объекта обновлены",
        "added_to_object_notification": (
        "👋 Вас добавили на новый объект!\n\n"
        "🏗 <b>Объект:</b> {object_name}\n"
        "ℹ️ Теперь вы можете видеть этот объект в разделе 'Мои объекты'"),
        "create_object_documents": "📸 Загрузите фотографии документов по объекту.\n\nКогда загрузите все документы, нажмите 'Прекратить'",
        "create_object_document_has_received": "✅ Документ получен. Продолжайте загрузку или нажмите 'Прекратить'",
        "create_object_document_no_received": "❌ Пожалуйста, отправьте фотографию документа",
        "doc_type_select": "🔍 Выберите тип документа:",
        "doc_type_контакты заказчика": "📞 Контакты заказчика",
        "doc_type_смета": "📊 Смета",
        "doc_type_техническое задание": "📋 Техническое задание",
        "doc_type_other": "📄 Другое",
        "create_object_uploading": "📤 Загрузка документов...",
        "create_object_saving": "💾 Сохранение объекта...",
        "create_object_complete": "✅ Объект успешно создан",
        "create_object_error": "❌ Ошибка при создании объекта",
        "continue_btn": "➡️ Продолжить",
        "stop_upload_btn": "🛑 Прекратить загрузку",
        "upload_without_docs_btn": "📄 Создать без документов",
        "no_users_tg_id": "❌ Укажите ID пользователя: /user_tools_xlsx <user_id>",
        "tg_id_must_be_number": "❌ ID пользователя должен быть числом",
        "create_object_w8_documents": "🗂 Загрузите документы по объекту или нажмите 'Создать без документов'",
        "upload_document_first": "❌ Сначала загрузите документ",
        "tmc_upload_btn": "📤TMC",
        "tmc_upload_instruction": "📝 Загрузите заполненный файл Excel с инструментами",
        "invalid_file_type": "❌ Неверный формат файла. Загрузите файл Excel (.xlsx)",
        "tools_export_btn": "📊 Экспорт инструментов",
        "enter_reminder_description": "📝 Введите описание материала/инструмента",
        "enter_reminder_location": "📍 Введите место хранения",
        "reminder_created": "✅ Напоминание создано",
        "object_data_header": "🏗 Информация об объекте:",
        "object_data_format": (
            "📝 Название: {name}\n"
            "ℹ️ Описание: {description}\n"
            "📅 Создан: {created_at}\n"
            "👤 Создатель: {creator}"
        ),
        "handover_confirmation": "❓ Подтвердите сдачу объекта",
        "handover_cancelled": "❌ Сдача объекта отменена",
        "notification_to_user": "📬 Новое уведомление от {sender}",
        "notification_failed": "❌ Ошибка отправки уведомления",
        "page_info": "Страница {current} из {total}",
        "no_more_pages": "❌ Больше страниц нет",
        "back_to_menu": "◀️ Вернуться в меню",
        "operation_in_progress": "⏳ Операция выполняется...",
        "data_not_found": "❌ Данные не найдены",
        "setup_complete": "✅ Настройка завершена",
        "setup_cancelled": "❌ Настройка отменена",
        "document_delete_confirm": "❓ Подтвердите удаление документа",
        "document_deleted": "✅ Документ удален",
        "document_download_error": "❌ Ошибка при скачивании документа",
        "tmc_upload_start": "📤 Выберите способ добавления инструментов:",
        "tmc_upload_stopped": "✅ Загрузка инструментов остановлена",
        "tmc_invalid_file": "❌ Некорректный файл",
        "no_valid_tools": "❌ В файле нет корректных данных об инструментах",
        "tmc_bulk_upload_complete": "✅ Загружено инструментов: {success}\n❌ Ошибок: {errors}",
        "return_to_tools_control": "🔄 Возврат к управлению инструментами",
        "tmc_manual_btn": "✍️ Ручной ввод",
        "tmc_template_btn": "📄 Скачать шаблон",
        "download_template_btn": "📥 Скачать шаблон",
        "start_transfer_btn": "🔄 Начать передачу",
        "tool_status_all": "🔍 Все инструменты",
        "yes_btn": "✅ Да",
        "no_btn": "❌ Нет",
        "accounting_type_income": "📈 Поступление",
        "accounting_type_expense": "📉 Расход",
        "change_description_material_reminder_btn": "✏️ Изменить описание",
        "change_photo_material_reminder_btn": "📸 Изменить фото",
        "change_storage_location_material_reminder_btn": "📍 Изменить место хранения",
        'user_tools_list':'Список инструментов закрепленных за {full_name}',
        "excel_material_file_id": "File ID фото"
    },
    "az": {  
    },
    "tg": {
        
    },
}
