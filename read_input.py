import pandas as pd
from med import character_alignment

# Định nghĩa class VanBia
class VanBia:
    def __init__(self, id, name, sinoNom, vietnamese):
        self.id = id
        self.name = name
        self.sinoNom = sinoNom
        self.vietnamese = vietnamese

    def __repr__(self):
        return f"VanBia(id={self.id}, name={self.name}, sinoNom={self.sinoNom[:20]}..., vietnamese={self.vietnamese[:20]}...)"

# Đọc file Excel
file_path = 'input.xlsx'
df = pd.read_excel(file_path)

# Tạo danh sách các đối tượng VanBia
list_vanbia = []

for index, row in df.iterrows():
    if pd.isna(row['ID']) or row['ID'] == '':
        break
    vanbia = VanBia(
        id=row['ID'],
        name=row['Tên văn bia'],
        sinoNom=row['SinoNom'],
        vietnamese=row['Quốc ngữ']
    )
    list_vanbia.append(vanbia)

# Tách câu
if True:
    for vb in list_vanbia:
        print(vb.id)
        x = vb.vietnamese.replace("\n", ".").replace('…','').replace('…,','').replace('."','"')
        x = x.split(".")
        x = [i.strip() for i in x]
        x = list(filter(None, x))
        x = list(filter(lambda a: a != ' ', x))

        i = 0
        while i < len(x):
            if i+1 < len(x) and x[i + 1][0].islower():
                x[i] = x[i] + ' ' + x[i + 1]
                x.pop(i + 1)
                i -= 1
            else:
                x[i] = x[i].strip() + '|'
            i += 1

        vb.vietnamese = ' '.join(x)
        vb.sinoNom = vb.sinoNom.replace("\n", "")

        # Batch alignment
        batch_size = 50
        sinoNom = ''
        quocNgu = ''

        vb.vietnamese = vb.vietnamese.split(' ')
        vb.vietnamese = [i.strip() for i in vb.vietnamese]
        vb.vietnamese = list(filter(None, vb.vietnamese))
        vb.vietnamese = list(filter(lambda a: not all([not c.isalpha() for c in a]), vb.vietnamese))

        while len(vb.sinoNom) > 0:
            sinoNom_batch = vb.sinoNom[:batch_size]
            vietnamese_batch = vb.vietnamese[:batch_size]

            # Dóng hàng từng batch nhỏ
            sinoNom_, quocNgu_ = character_alignment(sinoNom_batch, vietnamese_batch)

            sinoNom += sinoNom_
            quocNgu += quocNgu_ + ' '

            # Cắt văn bản theo số ký tự thực tế sau dóng hàng
            vb.sinoNom = vb.sinoNom[sinoNom_batch:]
            vb.vietnamese = vb.vietnamese[vietnamese_batch:] 

        #sinoNom, quocNgu = character_alignment(vb.sinoNom, vb.vietnamese)

        # ghép lại thành câu
        quocNgu_sentence = quocNgu.split("|")
        quocNgu_sentence = [i.strip() for i in quocNgu_sentence]
        quocNgu_sentence = [i.split(" ") for i in quocNgu_sentence]
        sentence_len_list = [len(i) for i in quocNgu_sentence]

        # tách câu chữ hán
        sinoNom_sentence = []
        start = 0
        for length in sentence_len_list:
            sinoNom_ = ''.join(sinoNom[start:start + length])
            sinoNom_sentence.append(sinoNom_)
            start += length

        vb.sinoNom = sinoNom_sentence
        vb.vietnamese = quocNgu_sentence
        vb.sinoNom = [i for i in vb.sinoNom if i != '']
        vb.vietnamese = [i for i in vb.vietnamese if i != '']



