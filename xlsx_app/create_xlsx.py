from openpyxl import Workbook

from models.core_models import User


async def create_progress_xlsx(user: User):
    wb = Workbook()
    sheet = wb.active

    sheet["A1"] = f"{user.username}"
    sheet["A3"] = "Выбранная программа по изменению тела:"
    if user.progresses.change_body_programs.program_name:
        sheet["A4"] = f"{user.progresses.change_body_programs.program_name}"
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
