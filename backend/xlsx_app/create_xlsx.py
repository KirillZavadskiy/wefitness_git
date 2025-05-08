from openpyxl import Workbook

from backend.models.core_models import User


async def create_progress_xlsx(user: User):
    wb = Workbook()
    sheet = wb.active
    sheet.column_dimensions["A"].width = 20
    sheet.column_dimensions["B"].width = 20
    sheet.column_dimensions["C"].width = 20
    sheet.column_dimensions["D"].width = 20
    
    sheet["A1"] = f"{user.username}"
    sheet["A3"] = "Выбранная программа по изменению тела:"
    if user.progresses.change_body_programs.program_name:
        sheet["A4"] = f"{user.progresses.change_body_programs.program_name}"
        sheet["A6"] = "Стартовый вес, кг"
        sheet["A7"] = f"{user.progresses.start_value}"
        sheet["B6"] = "Текущий вес, кг"
        sheet["B7"] = f"{user.progresses.current_value}"
        sheet["C6"] = "Цель, кг"
        sheet["C7"] = f"{user.progresses.target_value}"
        sheet["D6"] = "Прогресс, %"
        sheet["D7"] = f"{user.progresses.value}"

    else:
        sheet["A4"] = "Программа не выбрана"
    sheet["A9"] = "Ваши баллы за посещение WeFitness:"
    sheet["A10"] = f"{user.points}"
    file_name = "my_progress.xlsx"
    wb.save(file_name)
    # with NamedTemporaryFile() as tmp:
    #     wb.save(tmp.name)
    #     tmp.seek(0)
    #     stream = tmp.read()
    # tmp.name = file_name
    return file_name
