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
        'reminder_delete_canceled': 'Удаление остатков отменено',
        'reminder_deleted': 'Остатки деактивированны',
        'reminder_not_found': 'Остатки не были найденны',
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
        "no_objects": "У вас нет доступных объектов",
        "back_btn": "Назад",
        "no_object_members": "Для выбранного объекта нет закрепленных рабочих.",
        "worker_info_format": (
            "Телеграм ID: {telegram_id}\n"
            "Username: {username}\n"
            "ФИО: {full_name}\n"
            "Телефон: {phone}\n"
            "Статус: {status}\n"
            "Объект: {object_name}"
        ),
        "select_object_action": "Выберите действие с объектом",
        "no_object_documents": "Для данного объекта не добавлено ни одной документации",
        "document_info_format": (
            "Тип документа: {document_type}\n"
            "Закреплен за объектом: {object_name}\n"
        ),
        "enter_handover_description": "Введите описание сдачи объекта:",
        "object_not_found": "Объект не найден",
        "handover_format": (
            "🏗 <b>Сдача объекта</b>\n\n"
            "🏢 Объект: {object_name} (ID: {object_id})\n"
            "👤 Прораб: {foreman_name}\n"
            "📧 Username: {username}\n\n"
            "📝 <b>Описание:</b>\n{description}"
        ),
        "handover_sent": "✅ Информация о сдаче объекта успешно отправлена",
        "own_expense_true_btn": "За свой счет - ✔",
        "own_expense_false_btn": "За свой счет - ❌",
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
        "reminder_out_btn": "Учет чеков вне объектов",
        "tools_list_caption": "📊 Отчет по инструментам\n💼 Тип: {tool_status}",
        "select_tool_status": "Выберите тип инструментов для выгрузки:",
        "all_tools": "Все инструменты",
        "in_work_tools": "Инструменты в работе",
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
        "create_object_btn": "Создать объект",
        "edit_object_btn": "✏️ Редактировать объект",
        "delete_object_btn": "Удалить объект",
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
            "* - обязательные поля"
        ),
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
        "reminder_out_object_btn": "Остатки вне объекта",
        "instrument_control_btn": "Управление инструментами",
        "material_remainder_control_btn": "Управление остатками материала",
        "reminder_btn": "Остатки",
        "object_control_btn": "Управление объектами",
        "notify_btn": "Уведомления",
        "cancel_btn": "❌ Отмена",
        "add_worker_to_object_btn": "Добавить рабочего",
        "bulk_transfer_btn": "Массовая передача",
        "user_tools_list_btn": "Список инструментов",
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
            "ℹ️ Теперь вы можете видеть этот объект в разделе 'Мои объекты'"
        ),
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
        "tmc_upload_btn": "TMC",
        "tmc_upload_instruction": "📝 Загрузите заполненный файл Excel с инструментами",
        "invalid_file_type": "❌ Неверный формат файла. Загрузите файл Excel (.xlsx)",
        "tools_export_btn": "Экспорт инструментов",
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
        'user_tools_list': 'Список инструментов закрепленных за {full_name}',
        "excel_material_file_id": "File ID фото",
        "finance_report_btn": "Финансовый отчет",
        "report_by_objects_btn": "📊 По объектам",
        "report_no_objects_btn": "📋 Вне объектов",
        "this_month_btn": "📅 За последние 30 дней",
        "all_time_btn": "📆 За все время",
        "custom_period_btn": "⚙️ Указать период",
        "select_report_type": "Выберите тип отчета:",
        "select_period": "Выберите период отчета:",
        "enter_period": "Введите период в формате ДД.ММ.ГГГГ-ДД.ММ.ГГГГ\nНапример: 01.01.2025-09.06.2025",
        "invalid_period_format": "❌ Неверный формат периода. Попробуйте еще раз.",
        "generating_report": "⏳ Формирую отчет...",
        "report_ready": "✅ Отчет готов!",
        "export_error": "❌ Ошибка при формировании отчета",
        "select_object": "Выберите объект:",
        "financial_report": "Финансовый отчет",
        "financial_report_title": "Финансовый отчет по операциям",
        "date_column": "Дата",
        "transaction_type": "Тип операции",
        "object_column": "Объект",
        "description_column": "Описание",
        "amount_column": "Сумма",
        "user_column": "Пользователь",
        "check_expense": "Расход по чеку",
        "total_income": "Итого доходы:",
        "total_expense": "Итого расходы:",
        "total_profit": "Итого прибыль:",
    },
    "az": {
        "reminder_delete_canceled": "Qalıqların silinməsi ləğv edildi",
        "reminder_deleted": "Qalıqlar deaktiv edildi",
        "reminder_not_found": "Qalıqlar tapılmadı",
        "start": "Salam, {name}! Mən botam",
        "language_select": "Dil seçin:",
        "language_ru": "Rus dili",
        "language_az": "Azərbaycan dili",
        "language_tg": "Tacik dili",
        "request_contact": "Zəhmət olmasa, aşağıdakı düymə ilə telefon nömrənizi paylaşın.",
        "username_instruction": """
Botdan istifadə etmək üçün istifadəçi adı yaratmalısınız. Təlimatlara əməl edin

<b>Telegram-da istifadəçi adı necə yaradılır:</b>

1. Telegram parametrlərini açın
2. Profilinizi düzəldin
3. "İstifadəçi adı" sahəsini seçin
4. İstədiyiniz istifadəçi adını daxil edin
5. Saxlamaq üçün ✓ işarəsinə toxunun

İstifadəçi adını yaratdıqdan sonra aşağıdakı "Yoxla" düyməsinə basın.""",
        "check": "Yoxla",
        "create_username": "İstifadəçi adı yarat",
        "has_no_username": "İstifadəçi adı yaratmaq üçün təlimatlara əməl edin",
        "share_contact_btn": "Əlaqəni paylaş 📱",
        "no_contact": "Klaviaturadan istifadə edin",
        "cancel": "Ləğv et",
        "confirm": "Təsdiq et",
        "its_no_contact": "Zəhmət olmasa, klaviaturadakı düymədən istifadə edin",
        "reques_docs": "Söhbətə sənəd şəkilləri göndərin. Bütün sənədləri yüklədikdən sonra 'Dayandır' düyməsinə basın.",
        "stop_upload_btn": "Dayandır",
        "i_got_acquainted_btn": "Məlumat aldım",
        "i_got_acquainted": "Bütün məlumatları aldınızsa, 'Məlumat aldım' düyməsinə basın",
        "reques_fio": "Ad, soyad və ata adınızı daxil edin",
        "ru": "Rus dili",
        "az": "Azərbaycan dili",
        "tg": "Tacik dili",
        "photo_received": "Şəkil alındı. Ümumi yüklənib: {count}",
        "photos_saved": "Bütün şəkillər ({count}) uğurla saxlanıldı!",
        "no_photos": "Heç bir şəkil yükləməmisiniz",
        "solve_example": "İnsan olduğunuzu təsdiqləmək üçün nümunəni həll edin:\n{example}",
        "verification_success": "Təsdiq uğurla başa çatdı! Qeydiyyat tamamlandı.",
        "wrong_answer": "Səhv cavab. Başqa nümunəni həll edin:\n{example}",
        "not_a_number": "Zəhmət olmasa, ədəd daxil edin.",
        "report_accepted": "Hesabat qəbul edildi",
        "report_error": "Mesajın göndərilməsində xəta baş verdi.",
        "profile_btn": "Profil",
        "my_objects_btn": "Mənim obyektlərim",
        "material_remainder_btn": "Material qalıqları",
        "material_order_btn": "Material sifarişi",
        "info_btn": "Məlumat",
        "instructions": "Botu istifadə etmək üçün təlimat",
        "rules": "İstifadə qaydaları",
        "profile_info": (
            "👤 <b>Profil</b>\n\n"
            "🆔 Telegram ID: <code>{telegram_id}</code>\n"
            "📧 İstifadəçi adı: @{username}\n"
            "👨‍💼 Ad, Soyad: {full_name}\n"
            "📱 Telefon: {phone}\n"
            "📊 Status: {role}"
        ),
        "tools_list_btn": "Alətlər",
        "language_select_btn": "Dil seçimi",
        "rules_btn": "Qaydalar",
        "no_tools": "Sizə heç bir alət təyin edilməyib",
        "tools_list_header": "🛠 <b>Təyin edilmiş alətlər siyahısı:</b>",
        "tool_item": "<b>{name}</b>\nid:<code>{tool_id}</code>\n📝 Təsvir: <i>{description}</i>",
        "no_description": "Təsvir yoxdur",
        "lang_has_changed": "Botun dili dəyişdirildi",
        "no_objects": "Sizin üçün heç bir obyekt mövcud deyil",
        "objects_list_header": "🏗 <b>Sizin obyektləriniz:</b>",
        "object_item": "🔹 <b>{name}</b>\n📝 <i>{description}</i>",
        "navigation_btn": "📍 Naviqasiya",
        "documentation_btn": "📄 Sənədlər",
        "notify_object_btn": "📢 Obyekti xəbərdar et",
        "object_photo_btn": "📸 Obyektdən şəkil",
        "object_checks_btn": "🧾 Çek qeydi",
        "no_navigation": "Bu obyekt üçün naviqasiya əlavə edilməyib",
        "enter_notification": "Bütün obyekt iştirakçılarına göndəriləcək mesajı daxil edin",
        "notification_format": (
            "📢 <b>{object_id} obyektindən xəbərdarlıq</b>\n\n"
            "👤 <b>Göndərən:</b> {sender_name}\n"
            "📧 İstifadəçi adı: {username}\n\n"
            "💬 <b>Mesaj:</b>\n<i>{message}</i>"
        ),
        "notification_sent": "✅ Bütün iştirakçılara xəbərdar edildi",
        "send_object_photo": "📸 Obyektdən şəkil göndərin",
        "enter_photo_description": "📝 Şəkilə təsvir əlavə edin",
        "object_photo_format": (
            "📸 <b>Obyektdən şəkil #{object_id}</b>\n\n"
            "👤 <b>Göndərən:</b> {worker_name}\n"
            "📧 İstifadəçi adı: {username}\n\n"
            "📝 <b>Təsvir:</b>\n<i>{description}</i>"
        ),
        "photo_sent": "✅ Şəkil uğurla göndərildi",
        "send_photo_only": "❌ Zəhmət olmasa, yalnız şəkil göndərin",
        "send_check_photo_and_description": "📸 Çeki və təsvirini göndərin",
        "enter_check_amount": "💰 Çek məbləğini daxil edin (yalnız rəqəmlər)",
        "invalid_amount": "❌ Məbləğin formatı yanlışdır. Məsələn: 1234.56",
        "check_format": (
            "🧾 <b>{object_id} obyektindən çek</b>\n\n"
            "👤 <b>Göndərən:</b> {worker_name}\n"
            "📧 İstifadəçi adı: {username}\n\n"
            "📝 <b>Təsvir:</b> <i>{description}</i>\n"
            "💰 <b>Məbləğ:</b> {amount} AZN"
        ),
        "check_saved": "✅ Çek uğurla saxlanıldı",
        "enter_material_order": "📝 Lazım olan materialları təsvir edin",
        "enter_delivery_date": "📅 Çatdırılma tarixini daxil edin (format: GG.AA.İİİİ)",
        "date_must_be_future": "❌ Çatdırılma tarixi gələcəkdə olmalıdır",
        "invalid_date": "❌ Tarix yanlışdır",
        "invalid_date_format": (
            "❌ Tarix formatı yanlışdır\n\n"
            "Format: GG.AA.İİİİ\n"
            "Məsələn: 25.05.2024"
        ),
        "material_order_format": (
            "🛍 <b>Material sifarişi</b>\n\n"
            "👤 <b>Sifarişçi:</b> {worker_name}\n"
            "📧 İstifadəçi adı: {username}\n\n"
            "📝 <b>Tələb olunan materiallar:</b>\n<i>{description}</i>\n"
            "📅 <b>Çatdırılma tarixi:</b> <i>{delivery_date}</i>"
        ),
        "order_saved": "✅ Material sifarişi uğurla göndərildi",
        "send_material_photo": "📸 Materialın şəkilini göndərin",
        "enter_material_description": "📝 Material təsvirini daxil edin",
        "enter_storage_location": "📍 Saxlanma yerini daxil edin",
        "material_remainder_format": (
            "📦 <b>Material qalıqları</b>\n\n"
            "📝 <b>Təsvir:</b> <i>{description}</i>\n"
            "📍 <b>Saxlanma yeri:</b> <i>{location}</i>"
        ),
        "material_saved": "✅ Material məlumatı saxlanıldı",
        "transfer_tool_invalid_format": "Əmr formatı yanlışdır. İstifadə edin: /transfer_tool <alət_ID> <qəbul edən> <təsvir>",
        "transfer_tool_invalid_tool_id": "Alət ID rəqəm olmalıdır.",
        "transfer_tool_not_found": "Daxil edilmiş alət tapılmadı.",
        "transfer_tool_format": (
            "Alətin ötürülməsi:\n"
            "Alət: {tool_name} (ID: {tool_id})\n"
            "Qəbul edən: {recipient}\n"
            "Göndərən: {sender}\n"
            "Təsvir: {description}"
        ),
        "transfer_tool_request_sent": "Alətin ötürülməsi üçün sorğu göndərildi.",
        "accept_tool_btn": "alıb",
        "transfer_tool_receive_prompt": "{tool_name} aləti sizə göndərildi. Almaq üçün düyməyə toxunun.",
        "transfer_tool_recipient_not_found": "Belə bir istifadəçi tapılmadı.",
        "transfer_tool_invalid_recipient": "Qəbul edən @istifadəçi adı və ya telegram_id ilə qeyd olunmalıdır.",
        "tool_received_confirmation": "Alət alındı!",
        "objects_btn": "Obyektlər",
        "report_empty_text": "Zəhmət olmasa, /report əmri sonrası hesabat mətni daxil edin.",
        "report_format": (
            "Yeni hesabat {sender} ({username})-dən:\n\n"
            "{report}"
        ),
        "report_sent_confirmation": "Hesabatınız göndərildi.",
        "foreman_workers_btn": "İşçilər",
        "foreman_documentation_btn": "Sənədlər",
        "foreman_photos_btn": "Obyektdən şəkillər",
        "foreman_handover_btn": "Obyekti təhvil ver",
        "foreman_procurement_btn": "Alqı-satqı",
        "foreman_receipts_btn": "Çek qeydi",
        "foreman_material_balance_btn": "Material balansı",
        "foreman_info_btn": "Məlumat",
        "foreman_tools_list_btn": "Alətlər siyahısı",
        "foreman_mass_mailing_btn": "Obyekt üzrə kütləvi göndərmə",
        "foreman_offsite_accounting_btn": "Obyektdən kənar uçot",
        "foreman_export_xlsx_btn": "Obyekt üzrə xlsx ixrac",
        "select_object_prompt": "Xahiş edirik, işçilərin siyahısı üçün obyekt seçin",
        "no_objects": "Sizin üçün obyekt yoxdur",
        "back_btn": "Geri",
        "no_object_members": "Seçilmiş obyekt üçün işçi təyin edilməyib",
        "worker_info_format": (
            "Telegram ID: {telegram_id}\n"
            "İstifadəçi adı: {username}\n"
            "Ad, Soyad: {full_name}\n"
            "Telefon: {phone}\n"
            "Status: {status}\n"
            "Obyekt: {object_name}"
        ),
        "select_object_action": "Obyektdə əməliyyat seçin",
        "no_object_documents": "Bu obyekt üçün sənəd əlavə edilməyib",
        "document_info_format": (
            "Sənəd növü: {document_type}\n"
            "Obyekt: {object_name}\n"
        ),
        "enter_handover_description": "Obyekti təhvil vermək üçün təsvir daxil edin:",
        "object_not_found": "Obyekt tapılmadı",
        "handover_format": (
            "🏗 <b>Obyekti təhvil vermə</b>\n\n"
            "🏢 Obyekt: {object_name} (ID: {object_id})\n"
            "👤 Başçı: {foreman_name}\n"
            "📧 İstifadəçi adı: {username}\n\n"
            "📝 <b>Təsvir:</b>\n{description}"
        ),
        "handover_sent": "✅ Obyekt təhvil verilməsi məlumatı göndərildi",
        "own_expense_true_btn": "Öz xərci - ✔",
        "own_expense_false_btn": "Öz xərci - ❌",
        "expense_sheet_name": "Xərc cədvəli",
        "date_column": "Tarix",
        "description_column": "Təsvir",
        "amount_column": "Məbləğ",
        "expense_type_column": "Xərc növü",
        "user_column": "İstifadəçi",
        "own_expense": "Öz xərci",
        "company_expense": "Şirkət xərci",
        "total_amount": "Cəmi:",
        "prev_page_btn": "Əvvəlki",
        "next_page_btn": "Növbəti",
        "mock_data_cleared": "Bütün test məlumatları silindi",
        "invalid_photo_format": "Zəhmət olmasa, şəkil göndərin",
        "no_workers_found": "Mövcud işçi tapılmadı",
        "expense_report_caption": "Xərc hesabatı\nDövr: {start_date} - {end_date}\nNöv: {expense_type}",
        "no_expenses_found": "Verilmiş dövrdə xərc tapılmadı",
        "all_expenses_btn": "Bütün xərclər",
        "own_expenses_btn": "Öz xərclərim",
        "company_expenses_btn": "Şirkət xərci",
        "enter_start_date": "📅 Hesabat dövrünün başlanğıc tarixini daxil edin (GG.AA.İİİİ formatında)",
        "enter_end_date": "📅 Hesabat dövrünün son tarixini daxil edin (GG.AA.İİİİ formatında)",
        "select_expense_type": "Xərc növünü seçin:",
        "invalid_date_format": "❌ Tarix formatı yanlışdır. Məsələn: 25.12.2024",
        "expense_report_caption": (
            "📊 Xərc hesabatı\n"
            "📅 Dövr: {start_date} - {end_date}\n"
            "💰 Xərc növü: {expense_type}"
        ),
        "report_processing": "⏳ Hesabat hazırlanır...",
        "report_generation_error": "❌ Hesabat hazırlanarkən xəta",
        "all_expenses": "Bütün xərclər",
        "own_expenses": "Öz xərclərim",
        "company_expenses": "Şirkət xərci",
        "excel_date_column": "Tarix",
        "excel_description_column": "Təsvir",
        "excel_amount_column": "Məbləğ",
        "excel_expense_type_column": "Xərc növü",
        "excel_user_column": "İstifadəçi",
        "excel_total_row": "CƏMİ:",
        "excel_sheet_name": "Xərc hesabatı",
        "reminder_out_btn": "Obyektdən kənar çek qeydi",
        "tools_list_caption": "📊 Alət hesabatı\n💼 Növ: {tool_status}",
        "select_tool_status": "Alət növünü seçin:",
        "all_tools": "Bütün alətlər",
        "in_work_tools": "İşləyən alətlər",
        "free_tools": "Boş alətlər",
        "repair_tools": "Təmir alətləri",
        "no_tools_found": "❌ Alətlər tapılmadı",
        "excel_tool_name": "Ad",
        "excel_tool_description": "Təsvir",
        "excel_tool_status": "Status",
        "excel_tool_user": "Təyinatlı",
        "excel_tool_date": "Təyinat tarixi",
        "excel_tools_sheet_name": "Alətlər siyahısı",
        "no_users_found": "❌ İstifadəçi tapılmadı",
        "no_objects_found": "❌ Obyekt tapılmadı",
        "no_members_found": "❌ Obyektdə iştirakçı yoxdur",
        "select_object_for_notification": "📋 Bildiriş üçün obyekt seçin:",
        "enter_notification_text": "📝 Bildiriş mətnini daxil edin:",
        "sending_notifications_status": "📤 Göndərilir... {sent}/{total}",
        "notifications_sent_status": "✅ Bildiriş göndərildi\n\n📊 Ümumi: {total}\n✅ Uğurlu: {success}\n❌ Uğursuz: {failed}",
        "admin_notify_all_users_inline_btn": "📢 Bütün istifadəçilər",
        "admin_notify_object_inline_btn": "🏗 Obyekt üzrə",
        "admin_notify_all_user_w8_message": "📝 Bütün istifadəçilərə göndərmək üçün mətn daxil edin:",
        "transfer_tool_force_format": (
            "🔄 Məcburi alət ötürülməsi\n"
            "🛠 Alət: {tool_name} (ID: {tool_id})\n"
            "👤 Qəbul edən: {recipient}\n"
            "👨‍💼 Administrator: {admin}\n"
            "📝 Təsvir: {description}"
        ),
        "transfer_tool_force_complete": "✅ Alət məcburi ötürüldü",
        "transfer_tool_force_received": "🔄 Administrator {admin} sizə {tool_name} alətini ötürdü",
        "transfer_tool_admin_format": (
            "Əmr formatı:\n"
            "/transfer_tool <alət_ID> <qəbul edən> <təsvir>\n"
            "Məcburi ötürmə (yalnız adminlər üçün):\n"
            "/transfer_tool <alət_ID> <qəbul edən> -f <təsvir>"
        ),
        "admin_notify": "Göndərmə növünü seçin:",
        "create_object_name": "📝 Obyekt adını daxil edin:",
        "operation_cancelled": "❌ Əməliyyat ləğv olundu",
        "caption_required": "❌ Şəkilə təsvir əlavə edilməlidir",
        "select_document_type": "Sənəd növünü seçin:",
        "doc_type_estimate": "📊 Qiymət təklifi",
        "doc_type_technical": "📋 Texniki şərt",
        "doc_type_contacts": "📞 Müştəri əlaqələri",
        "create_object_success": "✅ Obyekt uğurla yaradıldı",
        "notification_sent_to_all": "✅ Bütün istifadəçilərə bildiriş göndərildi",
        "create_object_no_documents": "❌ Sənədlər yüklənmədi",
        "create_object_description": "📝 Obyekt təsvirini daxil edin:",
        "pagination_error": "❌ Səhifə yenilənərkən xəta",
        "objects_list": "📋 Obyektlərin siyahısı:",
        "object_name": "Obyekt: {name}",
        "updated_success": "✅ Məlumatlar uğurla yeniləndi",
        "error_occurred": "❌ Xəta baş verdi",
        "document_upload_complete": "✅ Sənəd yükləndi",
        "document_type_selected": "✅ Sənəd növü seçildi",
        "document_saved": "✅ Sənəd saxlanıldı",
        "upload_more_documents": "📤 Növbəti sənədi yükləyin və ya 'Dayandır' düyməsinə basın",
        "foreman_panel": "👨‍💼 Başçı paneli",
        "object_members_header": "👥 Obyekt iştirakçıları:",
        "member_item_format": (
            "👤 {full_name}\n"
            "📱 {phone}\n"
            "📧 @{username}"
        ),
        "admin_panel": "👨‍💼 Administrator paneli",
        "object_control": "🏗 Obyektlərin idarəsi",
        "user_control": "👥 İstifadəçilərin idarəsi",
        "create_object_btn": "Obyekt yarat",
        "edit_object_btn": "✏️ Obyekti düzəlt",
        "delete_object_btn": "Obyekti sil",
        "access_denied": "❌ Giriş icazəsi yoxdur",
        "invalid_input": "❌ Yanlış daxil edilib",
        "action_cancelled": "❌ Əməliyyat ləğv olundu",
        "try_again": "🔄 Yenidən cəhd edin",
        "processing": "⏳ Emal olunur...",
        "saving_data": "💾 Məlumat saxlanılır...",
        "loading_data": "📥 Məlumat yüklənir...",
        "tool_status_active": "✅ İşləyir",
        "tool_status_free": "🆓 Boş",
        "tool_status_repair": "🔧 Təmir olunur",
        "tool_transfer_success": "✅ Alət uğurla ötürüldü",
        "object_active": "✅ Aktiv",
        "object_completed": "🏁 Tamamlandı",
        "object_suspended": "⏸ Dayandırıldı",
        "confirm_action": "Əməliyyatı təsdiqləyin:",
        "confirm_delete": "❗️ Silinməni təsdiqləyin",
        "confirm_cancel": "❗️ Ləğvi təsdiqləyin",
        "tmc_template_instruction": (
            "📝 Doldurma təlimatı:\n\n"
            "1. Ad* - alətin adı\n"
            "2. Say* - ədəd\n"
            "3. Təsvir - əlavə məlumat\n"
            "4. Status - boş/təyin edilmiş/təmirdə\n"
            "5. File ID - alətin şəkil ID-si\n\n"
            "* - məcburi sahədir"
        ),
        "tmc_template_sheet": "Alət şablonu",
        "excel_tool_quantity": "Say*",
        "excel_tool_file_id": "Şəkil File ID",
        "tmc_enter_name": "📝 Alət adını daxil edin",
        "tmc_enter_quantity": "🔢 Alət sayını daxil edin",
        "tmc_enter_description": "📝 Alət təsvirini (isteğe bağlı) daxil edin",
        "tmc_upload_complete": "✅ {name} alətindən {count} ədəd əlavə edildi",
        "tmc_file_error": "❌ Fayl işlənərkən xəta baş verdi",
        "tmc_invalid_quantity": "❌ Say müsbət ədəd olmalıdır",
        "tmc_save_error": "❌ Alətlərin saxlanılmasında xəta",
        "materials_sheet_name": "Material qalıqları",
        "excel_material_id": "ID",
        "excel_material_description": "Təsvir",
        "excel_material_location": "Saxlanma yeri",
        "no_materials_found": "❌ Material tapılmadı",
        "materials_export_complete": "✅ {count} material ixrac edildi",
        "materials_export_error": "❌ Material ixracında xəta",
        "material_card_format": (
            "📦 Material #{id}\n\n"
            "📝 Təsvir: {description}\n"
            "📍 Saxlanma yeri: {location}\n"
        ),
        "send_photo_for_file_id": "📸 File ID əldə etmək üçün şəkil göndərin",
        "file_id_generated": "✅ File ID əldə edildi:\n{file_id}",
        "file_id_generation_error": "❌ File ID yaradılarkən xəta",
        "stop_btn": "⛔️ Dayandır",
        "generate_file_id_btn": "🆔 File ID əldə et",
        "materials_excel_btn": "📊 Material ixracı",
        "bulk_transfer_btn": "📦 Kütləvi ötürmə",
        "template_error": "❌ Şablon yaradılarkən xəta",
        "template_instruction": "📝 Təlimata uyğun şablonu doldurun və yenidən yükləyin",
        "bulk_transfer_instruction": "📝 Kütləvi alət ötürülməsi təlimatı",
        "bulk_transfer_report": (
            "📊 Ötürmə hesabatı:\n\n"
            "✅ Uğurlu:\n{success}\n\n"
            "❌ Xətalar:\n{failed}"
        ),
        "bulk_transfer_no_file": "❌ Fayl yüklənmədi",
        "bulk_transfer_complete": "✅ Alət ötürülməsi tamamlandı",
        "check_out_object_format": (
            "🧾 <b>Obyektdən kənar çek</b>\n\n"
            "👤 <b>Göndərən:</b> {worker_name}\n"
            "📧 İstifadəçi adı: {username}\n\n"
            "📝 <b>Təsvir:</b> <i>{description}</i>\n"
            "💰 <b>Məbləğ:</b> {amount} AZN"
        ),
        "choose_reminder": (
            "📦 <b>Material haqqında məlumat:</b>\n\n"
            "📝 <b>Təsvir:</b> <i>{description}</i>\n"
            "📍 <b>Saxlanma yeri:</b> <i>{storage_location}</i>\n"
        ),
        "send_file": "📤 Fayl göndərin",
        "file_processing": "⏳ Fayl işlənir...",
        "file_error": "❌ Fayl işlənərkən xəta",
        "enter_new_photo": "📸 Yeni şəkil göndərin",
        "reminder_photo_updated": "✅ Materialın şəkli yeniləndi",
        "reminder_description_updated": "✅ Materialın təsviri yeniləndi",
        "reminder_location_updated": "✅ Saxlanma yeri yeniləndi",
        "excel_bulk_transfer_sheet": "Kütləvi ötürmə",
        "excel_bulk_transfer_tool_id": "Alət ID*",
        "excel_bulk_transfer_recipient": "Qəbul edən*",
        "excel_bulk_transfer_description": "Təsvir",
        "invalid_recipient": "❌ Qəbul edən düzgün qeyd edilməyib",
        "invalid_tool_id": "❌ Alət ID səhvdir",
        "tool_not_found": "❌ Alət tapılmadı",
        "recipient_not_found": "❌ Qəbul edən tapılmadı",
        "success_transfer": "✅ Uğurla ötürüldü",
        "out_object_check_saved": "✅ Çek saxlanıldı və qrupa göndərildi",
        "profic_accounting_btn": "💰 Mənfəət uçotu",
        "select_object_for_profic": "📋 Mənfəət üçün obyekt seçin:",
        "select_payment_type": "💳 Əməliyyat növünü seçin:",
        "enter_payment_amount": "💰 Məbləği daxil edin:",
        "enter_payment_purpose": "📝 Ödənişin məqsədini daxil edin:",
        "invalid_amount": "❌ Məbləğin formatı yanlışdır. Məsələn: 1234.56",
        "profic_saved": "✅ {type} üçün {amount} AZN əlavə edildi",
        "profic_save_error": "❌ Əməliyyatın saxlanılmasında xəta",
        "reminder_out_object_btn": "Obyektdən kənar qalıqlar",
        "instrument_control_btn": "Alətlərin idarəsi",
        "material_remainder_control_btn": "Material qalıqları idarəsi",
        "reminder_btn": "Qalıqlar",
        "object_control_btn": "Obyektlərin idarəsi",
        "notify_btn": "Bildiriş",
        "cancel_btn": "❌ Ləğv et",
        "add_worker_to_object_btn": "İşçi əlavə et",
        "bulk_transfer_btn": "Kütləvi ötürmə",
        "user_tools_list_btn": "Alətlər siyahısı",
        "change_reminder_btn": "✏️ Qalıqları dəyiş",
        "deactivate_reminder_btn": "❌ Qalıqları deaktiv et",
        "create_material_reminder_btn": "➕ Material qalıqları yarat",
        "excel_view_btn": "📊 Excel baxışı",
        "change_deactivate_btn": "✏️ Dəyiş/Deaktiv et",
        "add_worker_to_object_text": "📋 İşçi əlavə etmək üçün obyekt seçin:",
        "add_worker_to_object_w8_ids": (
            "🏗 Obyekt: <b>{object_name}</b>\n\n"
            "📝 İşçilərin Telegram ID-lərini vergül ilə daxil edin (məsələn: 123456789, 987654321)"
        ),
        "no_valid_user_ids": "❌ Düzgün Telegram ID tapılmadı",
        "no_valid_users_found": "❌ Daxil edilmiş ID-lərlə uyğun istifadəçi tapılmadı",
        "members_added_successfully": (
            "📊 İşçilərin əlavə olunma nəticəsi:\n\n"
            "✅ Uğurla əlavə edildi: {success_count}\n"
            "❌ Əlavə edilmədi: {failed_count}\n\n"
            "❗️ Xəta səbəbləri:\n{failed_reasons}"
        ),
        "enter_new_description": "📝 Yeni təsvir daxil edin",
        "reminder_deactivated": "✅ Qalıqlar deaktiv edildi",
        "reminder_updated": "✅ Qalıqlar yeniləndi",
        "object_control_title": "🏗 Obyektlərin idarəsi",
        "object_deleted": "✅ Obyekt silindi",
        "object_updated": "✅ Məlumatlar yeniləndi",
        "added_to_object_notification": (
            "👋 Sizə yeni obyekt əlavə edildi!\n\n"
            "🏗 <b>Obyekt:</b> {object_name}\n"
            "ℹ️ İndi bu obyekt 'Mənim obyektlərim' bölməsində görünəcək"
        ),
        "create_object_documents": "📸 Obyektə aid sənəd şəkillərini yükləyin.\n\nBütün sənədləri yüklədikdən sonra 'Dayandır' düyməsinə basın",
        "create_object_document_has_received": "✅ Sənəd alındı. Yükləməyə davam edin və ya 'Dayandır' düyməsinə basın",
        "create_object_document_no_received": "❌ Zəhmət olmasa, sənədin şəklini göndərin",
        "doc_type_select": "🔍 Sənəd növünü seçin:",
        "doc_type_контакты заказчика": "📞 Müştəri əlaqələri",
        "doc_type_смета": "📊 Qiymət təklifi",
        "doc_type_техническое задание": "📋 Texniki şərt",
        "doc_type_other": "📄 Digər",
        "create_object_uploading": "📤 Sənədlər yüklənir...",
        "create_object_saving": "💾 Obyekt saxlanılır...",
        "create_object_complete": "✅ Obyekt uğurla yaradıldı",
        "create_object_error": "❌ Obyekt yaradılarkən xəta baş verdi",
        "continue_btn": "➡️ Davam et",
        "stop_upload_btn": "🛑 Yükləməni dayandır",
        "upload_without_docs_btn": "📄 Sənədsiz yarat",
        "no_users_tg_id": "❌ İstifadəçi ID daxil edin: /user_tools_xlsx <user_id>",
        "tg_id_must_be_number": "❌ İstifadəçi ID rəqəm olmalıdır",
        "create_object_w8_documents": "🗂 Obyektə aid sənədləri yükləyin və ya 'Sənədsiz yarat' düyməsinə basın",
        "upload_document_first": "❌ Əvvəlcə sənəd yükləyin",
        "tmc_upload_btn": "TMC",
        "tmc_upload_instruction": "📝 Alət məlumatlarını ehtiva edən Excel faylını yükləyin",
        "invalid_file_type": "❌ Fayl formatı yanlışdır. Excel (.xlsx) fayl göndərin",
        "tools_export_btn": "Alətlər ixracı",
        "enter_reminder_description": "📝 Material/alət təsvirini daxil edin",
        "enter_reminder_location": "📍 Saxlanma yerini daxil edin",
        "reminder_created": "✅ Qalıqlar yaradıldı",
        "object_data_header": "🏗 Obyekt haqqında məlumat:",
        "object_data_format": (
            "📝 Ad: {name}\n"
            "ℹ️ Təsvir: {description}\n"
            "📅 Yaradılma tarixi: {created_at}\n"
            "👤 Yaradıcı: {creator}"
        ),
        "handover_confirmation": "❓ Obyekti təhvil verməyi təsdiqləyin",
        "handover_cancelled": "❌ Obyekt təhvili ləğv olundu",
        "notification_to_user": "📬 {sender} tərəfindən yeni bildiriş",
        "notification_failed": "❌ Bildiriş göndərilərkən xəta",
        "page_info": "Səhifə {current} / {total}",
        "no_more_pages": "❌ Daha səhifə yoxdur",
        "back_to_menu": "◀️ Menyuga qayıt",
        "operation_in_progress": "⏳ Əməliyyat davam edir...",
        "data_not_found": "❌ Məlumat tapılmadı",
        "setup_complete": "✅ Quraşdırma tamamlandı",
        "setup_cancelled": "❌ Quraşdırma ləğv olundu",
        "document_delete_confirm": "❓ Sənədin silinməsini təsdiqləyin",
        "document_deleted": "✅ Sənəd silindi",
        "document_download_error": "❌ Sənəd endirilərkən xəta baş verdi",
        "tmc_upload_start": "📤 Alət əlavə etmək üsulunu seçin:",
        "tmc_upload_stopped": "✅ Alətlər yüklənməsi dayandırıldı",
        "tmc_invalid_file": "❌ Fayl uyğunsuzdur",
        "no_valid_tools": "❌ Faylda düzgün alət məlumatı yoxdur",
        "tmc_bulk_upload_complete": "✅ Alətlər yükləndi: {success}\n❌ Xətalar: {errors}",
        "return_to_tools_control": "🔄 Alət idarəsinə qayıt",
        "tmc_manual_btn": "✍️ Əl ilə daxil et",
        "tmc_template_btn": "📄 Şablonu yüklə",
        "download_template_btn": "📥 Şablonu yüklə",
        "start_transfer_btn": "🔄 Ötürməyə başla",
        "tool_status_all": "🔍 Bütün alətlər",
        "yes_btn": "✅ Bəli",
        "no_btn": "❌ Xeyr",
        "accounting_type_income": "📈 Gəlir",
        "accounting_type_expense": "📉 Xərc",
        "change_description_material_reminder_btn": "✏️ Təsviri dəyiş",
        "change_photo_material_reminder_btn": "📸 Şəkili dəyiş",
        "change_storage_location_material_reminder_btn": "📍 Saxlanma yerini dəyiş",
        "user_tools_list": "Alətlər siyahısı - {full_name}",
        "excel_material_file_id": "Şəkil File ID",
        "finance_report_btn": "Maliyyə hesabatı",
        "report_by_objects_btn": "📊 Obyektlər üzrə",
        "report_no_objects_btn": "📋 Obyektsiz",
        "this_month_btn": "📅 Son 30 gün",
        "all_time_btn": "📆 Bütün vaxt",
        "custom_period_btn": "⚙️ Dövr təyin et",
        "select_report_type": "Hesabat növünü seçin:",
        "select_period": "Hesabat dövrünü seçin:",
        "enter_period": "Dövrü daxil edin (GG.AA.İİİİ-GG.AA.İİİİ formatında)\nMəsələn: 01.01.2025-09.06.2025",
        "invalid_period_format": "❌ Dövr formatı yanlışdır. Yenidən cəhd edin.",
        "generating_report": "⏳ Hesabat hazırlanır...",
        "report_ready": "✅ Hesabat hazırdır!",
        "export_error": "❌ Hesabat hazırlanarkən xəta",
        "select_object": "Obyekt seçin:",
        "financial_report": "Maliyyə hesabatı",
        "financial_report_title": "Əməliyyatlara görə maliyyə hesabatı",
        "date_column": "Tarix",
        "transaction_type": "Əməliyyat növü",
        "object_column": "Obyekt",
        "description_column": "Təsvir",
        "amount_column": "Məbləğ",
        "user_column": "İstifadəçi",
        "check_expense": "Çek xərc",
        "total_income": "Ümumi gəlir:",
        "total_expense": "Ümumi xərc:",
        "total_profit": "Ümumi mənfəət:"
    },
    "tg": {
         "reminder_delete_canceled": "Бекор кардани нест кардани бақияҳо",
    "reminder_deleted": "Бақияҳо ғайрифаъол карда шуданд",
    "reminder_not_found": "Бақияҳо ёфт нашуданд",
    "start": "Салом, {name}! Ман бот ҳастам",
    "language_select": "Забонро интихоб кунед:",
    "language_ru": "Русӣ",
    "language_az": "Озарбойҷонӣ",
    "language_tg": "Тоҷикӣ",
    "request_contact": "Лутфан, рақами телефони худро тавассути тугмаи зерин мубодила кунед.",
    "username_instruction": """
Барои истифодаи бот шумо бояд номи корбарӣ созед. Дастурҳоро пайравӣ кунед

<b>Чӣ тавр дар Telegram номи корбарӣ сохтан мумкин аст:</b>

1. Танзимоти Telegram-ро кушоед
2. "Тағйир додани профил"-ро пахш кунед
3. Дар майдони "Номи корбарӣ" пахш кунед
4. Номи корбарии дилхоҳро дохил кунед
5. Барои нигоҳ доштан аломати ✓-ро пахш кунед

Пас аз сохтани номи корбарӣ, тугмаи "Санҷидан"-ро дар поён пахш кунед.""",
    "check": "Санҷидан",
    "create_username": "Сохтани номи корбарӣ",
    "has_no_username": "Барои сохтани номи корбарӣ дастурҳоро пайравӣ кунед",
    "share_contact_btn": "Мубодилаи тамос 📱",
    "no_contact": "Аз клавиатура истифода баред",
    "cancel": "Бекор кардан",
    "confirm": "Тасдиқ кардан",
    "its_no_contact": "Лутфан, аз тугмаи дар клавиатура истифода баред",
    "reques_docs": "Расмҳои ҳуҷҷатҳоро ба чат фиристед. Вақте ки ҳамаи ҳуҷҷатҳоро бор кардед, тугмаи 'Қатъ'-ро пахш кунед.",
    "stop_upload_btn": "Қатъ",
    "i_got_acquainted_btn": "Ман шинос шудам",
    "i_got_acquainted": "Агар бо ҳама чиз шинос шудед, тугмаи 'Ман шинос шудам'-ро пахш кунед",
    "reques_fio": "ФИО-ро дохил кунед",
    "ru": "Русӣ",
    "az": "Озарбойҷонӣ",
    "tg": "Тоҷикӣ",
    "photo_received": "Расм қабул шуд. Ҳамагӣ бор карда шуд: {count}",
    "photos_saved": "Ҳамаи расмҳо ({count}) бомуваффақият нигоҳ дошта шуданд!",
    "no_photos": "Шумо ягон расм бор накардед",
    "solve_example": "Барои тасдиқи он, ки шумо инсон ҳастед, мисолро ҳал кунед:\n{example}",
    "verification_success": "Тасдиқ бомуваффақият анҷом ёфт! Бақайдгирӣ анҷом ёфт.",
    "wrong_answer": "Ҷавоби нодуруст. Мисоли дигарро ҳал кунед:\n{example}",
    "not_a_number": "Лутфан, рақамро дохил кунед.",
    "report_accepted": "Ҳисобот қабул карда шуд",
    "report_error": "Ҳангоми фиристодани паём хато рух дод.",
    "profile_btn": "Профил",
    "my_objects_btn": "Объектҳои ман",
    "material_remainder_btn": "Бақияи масолеҳ",
    "material_order_btn": "Фармоиши масолеҳ",
    "info_btn": "Маълумот",
    "instructions": "Дастурҳо оид ба истифодаи бот",
    "rules": "Қоидаҳои истифода",
    "profile_info": (
        "👤 <b>Профил</b>\n\n"
        "🆔 Telegram ID: <code>{telegram_id}</code>\n"
        "📧 Номи корбарӣ: @{username}\n"
        "👨‍💼 ФИО: {full_name}\n"
        "📱 Телефон: {phone}\n"
        "📊 Мақом: {role}"
    ),
    "tools_list_btn": "Асбобҳо",
    "language_select_btn": "Интихоби забон",
    "rules_btn": "Қоидаҳо",
    "no_tools": "Ба шумо ягон асбоб вобаста карда нашудааст",
    "tools_list_header": "🛠 <b>Рӯйхати асбобҳои вобасташуда:</b>",
    "tool_item": "<b>{name}</b>\nid:<code>{tool_id}</code>\n📝 Тавсиф: <i>{description}</i>",
    "no_description": "Тавсиф вуҷуд надорад",
    "lang_has_changed": "Забони бот тағйир дода шуд",
    "no_objects": "Шумо объектҳои дастрас надоред",
    "objects_list_header": "🏗 <b>Объектҳои шумо:</b>",
    "object_item": "🔹 <b>{name}</b>\n📝 <i>{description}</i>",
    "navigation_btn": "📍 Навигатсия",
    "documentation_btn": "📄 Ҳуҷҷатҳо",
    "notify_object_btn": "📢 Огоҳ кардани объект",
    "object_photo_btn": "📸 Расм аз объект",
    "object_checks_btn": "🧾 Баҳисобгирии чекҳо",
    "no_navigation": "Барои ин объект навигатсия илова нашудааст",
    "enter_notification": "Паёмро барои фиристодан ба ҳамаи иштирокчиёни объект дохил кунед",
    "notification_format": (
        "📢 <b>Огоҳинома аз объекти {object_id}</b>\n\n"
        "👤 <b>Фиристанда:</b> {sender_name}\n"
        "📧 Номи корбарӣ: {username}\n\n"
        "💬 <b>Паём:</b>\n<i>{message}</i>"
    ),
    "notification_sent": "✅ Огоҳинома ба ҳамаи иштирокчиёни объект фиристода шуд",
    "send_object_photo": "📸 Расмро аз объект фиристед",
    "enter_photo_description": "📝 Тавсифи расмро дохил кунед",
    "object_photo_format": (
        "📸 <b>Расм аз объекти #{object_id}</b>\n\n"
        "👤 <b>Фиристанда:</b> {worker_name}\n"
        "📧 Номи корбарӣ: {username}\n\n"
        "📝 <b>Тавсиф:</b>\n<i>{description}</i>"
    ),
    "photo_sent": "✅ Расм бомуваффақият фиристода шуд",
    "send_photo_only": "❌ Лутфан, танҳо расмро фиристед",
    "send_check_photo_and_description": "📸 Расм ва тавсифи чекро фиристед",
    "enter_check_amount": "💰 Маблағи чекро дохил кунед (танҳо рақамҳо)",
    "invalid_amount": "❌ Формати маблағ нодуруст аст. Масалан: 1234.56",
    "check_format": (
        "🧾 <b>Чек аз объекти #{object_id}</b>\n\n"
        "👤 <b>Фиристанда:</b> {worker_name}\n"
        "📧 Номи корбарӣ: {username}\n\n"
        "📝 <b>Тавсиф:</b> <i>{description}</i>\n"
        "💰 <b>Маблағ:</b> {amount} сомонӣ"
    ),
    "check_saved": "✅ Чек бомуваффақият нигоҳ дошта шуд",
    "enter_material_order": "📝 Масолеҳи лозимиро тавсиф кунед",
    "enter_delivery_date": "📅 Санаи дилхоҳи расониданро нишон диҳед (формат: РР.ММ.СССС)",
    "date_must_be_future": "❌ Санаи расонидан бояд дар оянда бошад",
    "invalid_date": "❌ Санаи нодуруст",
    "invalid_date_format": (
        "❌ Формати санаи нодуруст\n\n"
        "Формат: РР.ММ.СССС\n"
        "Масалан: 25.05.2024"
    ),
    "material_order_format": (
        "🛍 <b>Фармоиши масолеҳ</b>\n\n"
        "👤 <b>Фармоишгар:</b> {worker_name}\n"
        "📧 Номи корбарӣ: {username}\n\n"
        "📝 <b>Масолеҳи лозима:</b>\n<i>{description}</i>\n"
        "📅 <b>Санаи дилхоҳ:</b> <i>{delivery_date}</i>"
    ),
    "order_saved": "✅ Фармоиши масолеҳ бомуваффақият фиристода шуд",
    "send_material_photo": "📸 Расми масолеҳро фиристед",
    "enter_material_description": "📝 Тавсифи масолеҳро дохил кунед",
    "enter_storage_location": "📍 Ҷойи нигоҳдории масолеҳро нишон диҳед",
    "material_remainder_format": (
        "📦 <b>Бақияи масолеҳ</b>\n\n"
        "📝 <b>Тавсиф:</b> <i>{description}</i>\n"
        "📍 <b>Ҷойи нигоҳдорӣ:</b> <i>{location}</i>"
    ),
    "material_saved": "✅ Маълумот дар бораи масолеҳ нигоҳ дошта шуд",
    "transfer_tool_invalid_format": "Формати фармон нодуруст аст. Истифода баред: /transfer_tool <ID асбоб> <гиранда> <тавсиф>",
    "transfer_tool_invalid_tool_id": "ID асбоб бояд рақам бошад.",
    "transfer_tool_not_found": "Асбоб бо ID нишондодашуда ёфт нашуд.",
    "transfer_tool_format": (
        "Интиқоли асбоб:\n"
        "Асбоб: {tool_name} (ID: {tool_id})\n"
        "Гиранда: {recipient}\n"
        "Фиристанда: {sender}\n"
        "Тавсиф: {description}"
    ),
    "transfer_tool_request_sent": "Дархост барои интиқоли асбоб фиристода шуд.",
    "accept_tool_btn": "қабул кардани асбоб",
    "transfer_tool_receive_prompt": "Ба шумо асбоби {tool_name} мефиристанд. Барои гирифтан тугмаи зеринро пахш кунед.",
    "transfer_tool_recipient_not_found": "Корбар бо чунин ном ёфт нашуд.",
    "transfer_tool_invalid_recipient": "Гиранда бояд тавассути @username ё telegram_id нишон дода шавад.",
    "tool_received_confirmation": "Асбоб қабул карда шуд!",
    "objects_btn": "Объектҳо",
    "report_empty_text": "Лутфан, матни ҳисоботро пас аз фармони /report дохил кунед",
    "report_format": (
        "Ҳисоботи нав аз {sender} ({username}):\n\n"
        "{report}"
    ),
    "report_sent_confirmation": "Ҳисоботи шумо фиристода шуд.",
    "foreman_workers_btn": "Коргарон",
    "foreman_documentation_btn": "Ҳуҷҷатҳо",
    "foreman_photos_btn": "Расмҳо аз объект",
    "foreman_handover_btn": "Супоридани объект",
    "foreman_procurement_btn": "Харид",
    "foreman_receipts_btn": "Баҳисобгирии чекҳо",
    "foreman_material_balance_btn": "Тавозуни масолеҳ",
    "foreman_info_btn": "Маълумот",
    "foreman_tools_list_btn": "Рӯйхати асбобҳо",
    "foreman_mass_mailing_btn": "Паёмҳои оммавӣ аз рӯи объект",
    "foreman_offsite_accounting_btn": "Баҳисобгирии берун аз объект",
    "foreman_export_xlsx_btn": "Содироти xlsx аз рӯи объект",
    "select_object_prompt": "Лутфан, объектро барои дидани рӯйхати коргарон интихоб кунед",
    "back_btn": "Бозгашт",
    "no_object_members": "Барои объекти интихобшуда коргарон вобаста карда нашудаанд",
    "worker_info_format": (
        "Telegram ID: {telegram_id}\n"
        "Номи корбарӣ: {username}\n"
        "ФИО: {full_name}\n"
        "Телефон: {phone}\n"
        "Мақом: {status}\n"
        "Объект: {object_name}"
    ),
    "select_object_action": "Амали объектро интихоб кунед",
    "no_object_documents": "Барои ин объект ягон ҳуҷҷат илова нашудааст",
    "document_info_format": (
        "Намуди ҳуҷҷат: {document_type}\n"
        "Ба объект вобаста: {object_name}\n"
    ),
    "enter_handover_description": "Тавсифи супоридани объектро дохил кунед:",
    "object_not_found": "Объект ёфт нашуд",
    "handover_format": (
        "🏗 <b>Супоридани объект</b>\n\n"
        "🏢 Объект: {object_name} (ID: {object_id})\n"
        "👤 Прораб: {foreman_name}\n"
        "📧 Номи корбарӣ: {username}\n\n"
        "📝 <b>Тавсиф:</b>\n{description}"
    ),
    "handover_sent": "✅ Маълумот дар бораи супоридани объект бомуваффақият фиристода шуд",
    "own_expense_true_btn": "Аз ҳисоби худ - ✔",
    "own_expense_false_btn": "Аз ҳисоби худ - ❌",
    "expense_sheet_name": "Ҳисоботи хароҷот",
    "date_column": "Сана",
    "description_column": "Тавсиф",
    "amount_column": "Маблағ",
    "expense_type_column": "Намуди хароҷот",
    "user_column": "Корбар",
    "own_expense": "Аз ҳисоби худ",
    "company_expense": "Аз ҳисоби ширкат",
    "total_amount": "Ҳамагӣ:",
    "prev_page_btn": "Саҳифаи қаблӣ",
    "next_page_btn": "Саҳифаи навбатӣ",
    "mock_data_cleared": "Ҳамаи маълумоти санҷишӣ нест карда шуд",
    "invalid_photo_format": "Лутфан, расмро фиристед",
    "no_workers_found": "Коргарони дастрас дар пойгоҳи додаҳо нестанд",
    "expense_report_caption": "Ҳисоботи хароҷот\nДавра: {start_date} - {end_date}\nНамуд: {expense_type}",
    "no_expenses_found": "Барои давраи нишондодашуда хароҷот ёфт нашуд",
    "all_expenses_btn": "Ҳамаи хароҷот",
    "own_expenses_btn": "Аз ҳисоби худ",
    "company_expenses_btn": "Аз ҳисоби ширкат",
    "enter_start_date": "📅 Санаи оғози давраи ҳисоботиро дохил кунед (формат: РР.ММ.СССС)",
    "enter_end_date": "📅 Санаи охири давраи ҳисоботиро дохил кунед (формат: РР.ММ.СССС)",
    "select_expense_type": "Намуди хароҷотро барои содирот интихоб кунед:",
    "invalid_date_format": "❌ Формати сана нодуруст аст. Масалан: 25.12.2024",
    "expense_report_caption": (
        "📊 Ҳисоботи хароҷот\n"
        "📅 Давра: {start_date} - {end_date}\n"
        "💰 Намуди хароҷот: {expense_type}"
    ),
    "report_processing": "⏳ Таҳияи ҳисобот...",
    "report_generation_error": "❌ Ҳангоми таҳияи ҳисобот хато рух дод",
    "all_expenses": "Ҳамаи хароҷот",
    "own_expenses": "Аз ҳисоби худ",
    "company_expenses": "Аз ҳисоби ширкат",
    "excel_date_column": "Сана",
    "excel_description_column": "Тавсиф",
    "excel_amount_column": "Маблағ",
    "excel_expense_type_column": "Намуди хароҷот",
    "excel_user_column": "Корбар",
    "excel_total_row": "ҲАМАГӢ:",
    "excel_sheet_name": "Ҳисоботи хароҷот",
    "reminder_out_btn": "Баҳисобгирии чекҳои берун аз объектҳо",
    "tools_list_caption": "📊 Ҳисоботи асбобҳо\n💼 Намуд: {tool_status}",
    "select_tool_status": "Намуди асбобҳоро барои содирот интихоб кунед:",
    "all_tools": "Ҳамаи асбобҳо",
    "in_work_tools": "Асбобҳои дар кор",
    "free_tools": "Асбобҳои озод",
    "repair_tools": "Асбобҳои дар таъмир",
    "no_tools_found": "❌ Асбобҳо ёфт нашуданд",
    "excel_tool_name": "Номгӯй",
    "excel_tool_description": "Тавсиф",
    "excel_tool_status": "Ҳолат",
    "excel_tool_user": "Вобаста ба",
    "excel_tool_date": "Санаи таъин",
    "excel_tools_sheet_name": "Рӯйхати асбобҳо",
    "no_users_found": "❌ Корбарон ёфт нашуданд",
    "no_objects_found": "❌ Объектҳо ёфт нашуданд",
    "no_members_found": "❌ Дар объект иштирокчиён нестанд",
    "select_object_for_notification": "📋 Объектро барои фиристодани огоҳинома интихоб кунед:",
    "enter_notification_text": "📝 Матни огоҳиномаро барои фиристодан дохил кунед:",
    "sending_notifications_status": "📤 Фиристода истодааст... {sent}/{total}",
    "notifications_sent_status": "✅ Фиристодан анҷом ёфт\n\n📊 Ҳамагӣ: {total}\n✅ Бомуваффақият: {success}\n❌ Нарасида: {failed}",
    "admin_notify_all_users_inline_btn": "📢 Ба ҳамаи корбарон",
    "admin_notify_object_inline_btn": "🏗 Аз рӯи объект",
    "admin_notify_all_user_w8_message": "📝 Матнро барои фиристодан ба ҳамаи корбарон дохил кунед:",
    "transfer_tool_force_format": (
        "🔄 Интиқоли маҷбурии асбоб\n"
        "🛠 Асбоб: {tool_name} (ID: {tool_id})\n"
        "👤 Гиранда: {recipient}\n"
        "👨‍💼 Маъмур: {admin}\n"
        "📝 Тавсиф: {description}"
    ),
    "transfer_tool_force_complete": "✅ Асбоб маҷбуран интиқол дода шуд",
    "transfer_tool_force_received": "🔄 Маъмур {admin} ба шумо асбоби {tool_name}-ро интиқол дод",
    "transfer_tool_admin_format": (
        "Формати фармон:\n"
        "/transfer_tool <ID_асбоб> <гиранда> <тавсиф>\n"
        "Барои интиқоли маҷбурӣ (танҳо барои маъмурон):\n"
        "/transfer_tool <ID_асбоб> <гиранда> -f <тавсиф>"
    ),
    "admin_notify": "Намуди фиристоданро интихоб кунед:",
    "create_object_name": "📝 Номи объектро дохил кунед:",
    "operation_cancelled": "❌ Амалиёт бекор карда шуд",
    "caption_required": "❌ Ба расм тавсиф илова кардан лозим аст",
    "select_document_type": "Намуди ҳуҷҷатро интихоб кунед:",
    "doc_type_estimate": "📊 Смета",
    "doc_type_technical": "📋 Супориши техникӣ",
    "doc_type_contacts": "📞 Тамосҳои фармоишгар",
    "create_object_success": "✅ Объект бомуваффақият сохта шуд",
    "notification_sent_to_all": "✅ Огоҳинома ба ҳамаи корбарон фиристода шуд",
    "create_object_no_documents": "❌ Ҳуҷҷатҳо бор карда нашуданд",
    "create_object_description": "📝 Тавсифи объектро дохил кунед:",
    "pagination_error": "❌ Хато ҳангоми навсозии саҳифа",
    "objects_list": "📋 Рӯйхати объектҳо:",
    "object_name": "Объект: {name}",
    "updated_success": "✅ Маълумот бомуваффақият навсозӣ карда шуд",
    "error_occurred": "❌ Хато рух дод",
    "document_upload_complete": "✅ Боркунии ҳуҷҷатҳо анҷом ёфт",
    "document_type_selected": "✅ Намуди ҳуҷҷат интихоб шуд",
    "document_saved": "✅ Ҳуҷҷат нигоҳ дошта шуд",
    "upload_more_documents": "📤 Ҳуҷҷати навбатиро бор кунед ё 'Анҷом'-ро пахш кунед",
    "foreman_panel": "👨‍💼 Панели прораб",
    "object_members_header": "👥 Иштирокчиёни объект:",
    "member_item_format": (
        "👤 {full_name}\n"
        "📱 {phone}\n"
        "📧 @{username}"
    ),
    "admin_panel": "👨‍💼 Панели маъмур",
    "object_control": "🏗 Идоракунии объектҳо",
    "user_control": "👥 Идоракунии корбарон",
    "create_object_btn": "Сохтани объект",
    "edit_object_btn": "✏️ Таҳрири объект",
    "delete_object_btn": "Нест кардани объект",
    "access_denied": "❌ Дастрасӣ манъ аст",
    "invalid_input": "❌ Вуруди нодуруст",
    "action_cancelled": "❌ Амал бекор карда шуд",
    "try_again": "🔄 Боз кӯшиш кунед",
    "processing": "⏳ Коркард...",
    "saving_data": "💾 Нигоҳдории маълумот...",
    "loading_data": "📥 Боркунии маълумот...",
    "tool_status_active": "✅ Дар кор",
    "tool_status_free": "🆓 Озод",
    "tool_status_repair": "🔧 Дар таъмир",
    "tool_transfer_success": "✅ Асбоб бомуваффақият интиқол дода шуд",
    "object_active": "✅ Фаъол",
    "object_completed": "🏁 Анҷомёфта",
    "object_suspended": "⏸ Боздошташуда",
    "confirm_action": "Амалро тасдиқ кунед:",
    "confirm_delete": "❗️ Нест карданро тасдиқ кунед",
    "confirm_cancel": "❗️ Бекор карданро тасдиқ кунед",
     "tmc_template_instruction": (
    "📝 Дастурамал оид ба пур кардан:\n\n"
    "1. Ном* - номи асбоб\n"
    "2. Миқдор* - шумораи воҳидҳо\n"
    "3. Тавсиф - маълумоти иловагӣ\n"
    "4. Ҳолат - озод/банд/дар таъмир\n"
    "5. File ID - ID расми асбоб\n\n"
    "* - майдонҳои ҳатмӣ"
    ),
    "tmc_template_sheet": "Шаблони асбобҳо",
    "excel_tool_quantity": "Миқдор*",
    "excel_tool_file_id": "File ID расм",
    "tmc_enter_name": "📝 Номи асбобро дохил кунед",
    "tmc_enter_quantity": "🔢 Миқдори асбобҳоро дохил кунед",
    "tmc_enter_description": "📝 Тавсифи асбобро дохил кунед (ихтиёрӣ)",
    "tmc_upload_complete": "✅ Илова карда шуд: {name} x{count}",
    "tmc_file_error": "❌ Ҳангоми коркарди файл хато рух дод",
    "tmc_invalid_quantity": "❌ Миқдор бояд адади мусбат бошад",
    "tmc_save_error": "❌ Ҳангоми нигоҳдории асбобҳо хато рух дод",
    "materials_sheet_name": "Бақияҳои масолеҳ",
    "excel_material_id": "ID",
    "excel_material_description": "Тавсиф",
    "excel_material_location": "Ҷойи нигоҳдорӣ",
    "no_materials_found": "❌ Масолеҳ ёфт нашуд",
    "materials_export_complete": "✅ Содироти масолеҳ: {count}",
    "materials_export_error": "❌ Ҳангоми содироти масолеҳ хато рух дод",
    "material_card_format": (
        "📦 Масолеҳ #{id}\n\n"
        "📝 Тавсиф: {description}\n"
        "📍 Ҷойи нигоҳдорӣ: {location}\n"
    ),
    "send_photo_for_file_id": "📸 Барои гирифтани File ID расм фиристед",
    "file_id_generated": "✅ File ID сохта шуд:\n{file_id}",
    "file_id_generation_error": "❌ Ҳангоми сохтани File ID хато рух дод",
    "stop_btn": "⛔️ Қатъ",
    "generate_file_id_btn": "🆔 Гирифтани File ID",
    "materials_excel_btn": "📊 Содироти бақияҳо",
    "bulk_transfer_btn": "📦 Интиқоли оммавӣ",
    "template_error": "❌ Ҳангоми сохтани шаблон хато рух дод",
    "template_instruction": "📝 Шаблонро мувофиқи дастурамал пур кунед ва дубора бор кунед",
    "bulk_transfer_instruction": "📝 Дастурамал оид ба интиқоли оммавии асбобҳо",
    "bulk_transfer_report": (
        "📊 Ҳисобот оид ба интиқол:\n\n"
        "✅ Бомуваффақият:\n{success}\n\n"
        "❌ Хатоҳо:\n{failed}"
    ),
    "bulk_transfer_no_file": "❌ Файл бор карда нашудааст",
    "bulk_transfer_complete": "✅ Интиқоли асбобҳо анҷом ёфт",
    "check_out_object_format": (
        "🧾 <b>Чек берун аз объект</b>\n\n"
        "👤 <b>Фиристанда:</b> {worker_name}\n"
        "📧 Номи корбарӣ: {username}\n\n"
        "📝 <b>Тавсиф:</b> <i>{description}</i>\n"
        "💰 <b>Маблағ:</b> {amount} сомонӣ"
    ),
    "send_file": "📤 Файлро фиристед",
    "file_processing": "⏳ Коркарди файл...",
    "file_error": "❌ Ҳангоми коркарди файл хато рух дод",
    "enter_new_photo": "📸 Расми навро фиристед",
    "reminder_photo_updated": "✅ Расми масолеҳ нав карда шуд",
    "reminder_description_updated": "✅ Тавсифи масолеҳ нав карда шуд",
    "reminder_location_updated": "✅ Ҷойи нигоҳдорӣ нав карда шуд",
    "excel_bulk_transfer_sheet": "Интиқоли оммавӣ",
    "excel_bulk_transfer_tool_id": "ID асбоб*",
    "excel_bulk_transfer_recipient": "Гиранда*",
    "excel_bulk_transfer_description": "Тавсиф",
    "invalid_recipient": "❌ Гиранда нодуруст нишон дода шудааст",
    "invalid_tool_id": "❌ ID асбоб нодуруст аст",
    "tool_not_found": "❌ Асбоб ёфт нашуд",
    "recipient_not_found": "❌ Гиранда ёфт нашуд",
    "success_transfer": "✅ Бомуваффақият интиқол дода шуд",
    "out_object_check_saved": "✅ Чек нигоҳ дошта ва ба гурӯҳ фиристода шуд",
    "profic_accounting_btn": "💰 Баҳисобгирии фоида",
    "select_object_for_profic": "📋 Барои баҳисобгирӣ объектро интихоб кунед:",
    "select_payment_type": "💳 Намуди амалиётро интихоб кунед:",
    "enter_payment_amount": "💰 Маблағро дохил кунед:",
    "enter_payment_purpose": "📝 Мақсади пардохтро дохил кунед:",
    "profic_saved": "✅ {type} ба маблағи {amount} сомонӣ илова карда шуд",
    "profic_save_error": "❌ Ҳангоми нигоҳдории амалиёт хато рух дод",
    "reminder_out_object_btn": "Бақияҳои берун аз объект",
    "instrument_control_btn": "Идоракунии асбобҳо",
    "material_remainder_control_btn": "Идоракунии бақияҳои масолеҳ",
    "reminder_btn": "Бақияҳо",
    "object_control_btn": "Идоракунии объектҳо",
    "notify_btn": "Огоҳиномаҳо",
    "cancel_btn": "❌ Бекор кардан",
    "add_worker_to_object_btn": "Илова кардани коргар",
    "bulk_transfer_btn": "Интиқоли оммавӣ",
    "user_tools_list_btn": "Рӯйхати асбобҳо",
    "change_reminder_btn": "✏️ Тағйир додани бақияҳо",
    "deactivate_reminder_btn": "❌ Ғайрифаъол кардани бақияҳо",
    "create_material_reminder_btn": "➕ Сохтани бақияҳо",
    "excel_view_btn": "📊 Намоиши Excel",
    "change_deactivate_btn": "✏️ Тағйир додан/Ғайрифаъол кардан",
    "tmc_upload_start": "📤 Усули илова кардани асбобҳоро интихоб кунед:",
    "tmc_manual_btn": "✍️ Воридоти дастӣ",
    "tmc_template_btn": "📄 Боргирии шаблон",
    "download_template_btn": "📥 Боргирии шаблон",
    "start_transfer_btn": "🔄 Оғози интиқол",
    "tool_status_all": "🔍 Ҳамаи асбобҳо",
    "yes_btn": "✅ Ҳа",
    "no_btn": "❌ Не",
    "accounting_type_income": "📈 Даромад",
    "accounting_type_expense": "📉 Хароҷот",
    "change_description_material_reminder_btn": "✏️ Тағйири тавсиф",
    "change_photo_material_reminder_btn": "📸 Тағйири расм",
    "change_storage_location_material_reminder_btn": "📍 Тағйири ҷойи нигоҳдорӣ",
    "user_tools_list": "Рӯйхати асбобҳои ба {full_name} вобасташуда",
    "excel_material_file_id": "File ID расм",
    "finance_report_btn": "Ҳисоботи молиявӣ",
    "report_by_objects_btn": "📊 Аз рӯи объектҳо",
    "report_no_objects_btn": "📋 Бе объект",
    "this_month_btn": "📅 30 рӯзи охир",
    "all_time_btn": "📆 Ҳамаи вақт",
    "custom_period_btn": "⚙️ Муайян кардани давра",
    "select_report_type": "Намуди ҳисоботро интихоб кунед:",
    "select_period": "Давраи ҳисоботро интихоб кунед:",
    "enter_period": "Давраро дохил кунед (дар шакли РР.ММ.СССС-РР.ММ.СССС)\nМасалан: 01.01.2025-09.06.2025",
    "invalid_period_format": "❌ Шакли давра нодуруст аст. Аз нав кӯшиш кунед.",
    "generating_report": "⏳ Ҳисобот тайёр мешавад...",
    "report_ready": "✅ Ҳисобот тайёр аст!",
    "export_error": "❌ Ҳангоми тайёр кардани ҳисобот хато рух дод",
    "select_object": "Объектро интихоб кунед:",
    "financial_report": "Ҳисоботи молиявӣ",
    "financial_report_title": "Ҳисоботи молиявӣ аз рӯи амалиётҳо",
    "date_column": "Сана",
    "transaction_type": "Намуди амалиёт",
    "object_column": "Объект",
    "description_column": "Тавсиф",
    "amount_column": "Маблағ",
    "user_column": "Истифодабаранда",
    "check_expense": "Хароҷоти чек",
    "total_income": "Даромади умумӣ:",
    "total_expense": "Хароҷоти умумӣ:",
    "total_profit": "Фоидаи умумӣ:"   
    },
}
