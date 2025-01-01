from read_input import list_vanbia
from xlsxwriter import Workbook
from med import compare_character

def output_file(output_file_name, list_vanbia):
    workbook = Workbook(output_file_name)
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})
    red = workbook.add_format({'color': 'red'})
    blue = workbook.add_format({'color': 'blue'})
    black = workbook.add_format({'color': 'black'})

    worksheet.write('A1', 'ID', bold)
    worksheet.write('B1', 'Tên văn bia', bold)
    worksheet.write('C1', 'SinoNom', bold)
    worksheet.write('D1', 'Quốc ngữ', bold)

    setColumnWidth = [15, 55, 100, 100]
    for i in range(len(setColumnWidth)):
        worksheet.set_column(i, i, setColumnWidth[i])

    row = 1
    col = 0
    
    for vb in list_vanbia:
        for i in range(len(vb.sinoNom)):
            worksheet.write(row, col, vb.id)
            worksheet.write(row, col + 1, vb.name)
            sinoNom_format_pair = []
            quocNgu_format_pair = []
            for sinoNom_char, quocNgu_char in zip(vb.sinoNom[i], vb.vietnamese[i]):
                nom_char = compare_character(sinoNom_char, quocNgu_char)
                if len(nom_char) == 0:
                    sinoNom_format_pair.extend((red, sinoNom_char))
                    quocNgu_format_pair.extend((red, quocNgu_char + ' '))
                elif len(nom_char) > 1:
                    sinoNom_format_pair.extend((blue, sinoNom_char))
                    quocNgu_format_pair.extend((blue, quocNgu_char + ' '))
                else:
                    sinoNom_format_pair.extend((black, sinoNom_char))
                    quocNgu_format_pair.extend((black, quocNgu_char + ' '))
            if len(sinoNom_format_pair) < 4:
                sinoNom_format_pair.extend((black, ' '))
            if len(quocNgu_format_pair) < 4:
                quocNgu_format_pair.extend((black, ' '))
            worksheet.write_rich_string(row, col + 2, *sinoNom_format_pair)
            worksheet.write_rich_string(row, col + 3, *quocNgu_format_pair)
            row += 1
    workbook.close()

output_file('output.xlsx', list_vanbia)