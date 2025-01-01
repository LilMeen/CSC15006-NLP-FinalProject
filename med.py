import pandas as pd

# define dictionary
quocNgu_sinoNom_dict_file_name = 'QuocNgu_SinoNom_Dic.xlsx'
sinoNom_similar_dict_file_name = 'SinoNom_similar_Dic.xlsx'

quocNgu_sinoNom_dict_data = pd.read_excel(quocNgu_sinoNom_dict_file_name)
sinoNom_similar_dict_data = pd.read_excel(sinoNom_similar_dict_file_name)

quocNgu_sinoNom_dict = {}
sinoNom_similar_dict = {}

for i in range(len(quocNgu_sinoNom_dict_data)):
    value = []
    if quocNgu_sinoNom_dict_data['QuocNgu'][i] in quocNgu_sinoNom_dict:
        value = quocNgu_sinoNom_dict[quocNgu_sinoNom_dict_data['QuocNgu'][i]]
    value.append(quocNgu_sinoNom_dict_data['SinoNom'][i])
    quocNgu_sinoNom_dict[quocNgu_sinoNom_dict_data['QuocNgu'][i]] = value

for i in range(len(sinoNom_similar_dict_data)):
    value = sinoNom_similar_dict_data['Top 20 Similar Characters'][i]
    value = value.removeprefix('[\'').removesuffix('\']').split('\', \'')
    sinoNom_similar_dict[sinoNom_similar_dict_data['Input Character'][i]] = value

def standarize_word(x):
    x = x.lower()
    x.strip()
    x = ''.join([i for i in x if i.isalpha()])
    return x

def compare_character(sinoNom, quocNgu):
    '''
    Compare character between SinoNom and Quoc Ngu

    Parameters
    ----------
    sinoNom: character
        The SinoNom character
    quocNgu: character
        The Quoc Ngu character

    Returns
    -------
        The set of matching character
    '''
    quocNgu = standarize_word(quocNgu)
    if sinoNom not in sinoNom_similar_dict:
        return {}
    if quocNgu.lower() not in quocNgu_sinoNom_dict:
        return {}
    if (len(sinoNom) == 0) or (len(quocNgu) == 0):
        return {}
    s2 = quocNgu_sinoNom_dict[quocNgu.lower()]
    if sinoNom in s2:
        return {sinoNom}
    s1 = sinoNom_similar_dict[sinoNom]
    s1.append(sinoNom)
    return set(s1).intersection(s2)


def character_alignment(sinoNom_sentence, quocNgu_sentence):
    '''
    Align character between SinoNom and Quoc Ngu

    Parameters
    ----------
    sinoNom_sentence: str
        The SinoNom sentence
    quocNgu_sentence: str
        The Quoc Ngu sentence

    Returns
    -------
        SinoNom sentence after alignment
    '''
    # quocNgu_sentence_ = quocNgu_sentence.split(' ')
    # quocNgu_sentence_ = [i.strip() for i in quocNgu_sentence_]
    # quocNgu_sentence_ = list(filter(None, quocNgu_sentence_))
    # quocNgu_sentence_ = list(filter(lambda a: not all([not c.isalpha() for c in a]), quocNgu_sentence_))

    def MED_levenshtein(s1, s2):
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        backtrace = [[None] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                value = 2
                if len(compare_character(s1[i - 1], s2[j - 1])) > 0:
                    value = 0  
                dp[i][j] = min(dp[i - 1][j - 1] + value, dp[i - 1][j] + 1, dp[i][j - 1] + 1)
                backtrace[i][j] = min((i - 1, j - 1), (i - 1, j), (i, j - 1), key=lambda x: dp[x[0]][x[1]])    

                if i - backtrace[i][j][0] == 1 and j - backtrace[i][j][1] == 1:
                    backtrace[i][j] = 'Match'
                elif i - backtrace[i][j][0] == 1 and j - backtrace[i][j][1] == 0:
                    backtrace[i][j] = 'Delete'
                elif i - backtrace[i][j][0] == 0 and j - backtrace[i][j][1] == 1:
                    backtrace[i][j] = 'Insert'
                
        backtrace_array = []
        while m > 0 and n > 0:
            backtrace_array.append(backtrace[m][n])
            if backtrace[m][n] == 'Match':
                m -= 1
                n -= 1
            elif backtrace[m][n] == 'Delete':
                m -= 1
            elif backtrace[m][n] == 'Insert':
                n -= 1

        return backtrace_array[::-1] 
    
    backtrace_array = MED_levenshtein(sinoNom_sentence, quocNgu_sentence)
    for i in range(len(backtrace_array)):
        if backtrace_array[i] == 'Delete':
            # sinoNom_sentence = sinoNom_sentence.replace(sinoNom_sentence[i], '', 1)
            quocNgu_sentence.insert(i, '󰠳')
        elif backtrace_array[i] == 'Insert':
            sinoNom_sentence = sinoNom_sentence[:i] + '󰠳' + sinoNom_sentence[i:]
    quocNgu_sentence = ' '.join(quocNgu_sentence)
    return sinoNom_sentence, quocNgu_sentence


