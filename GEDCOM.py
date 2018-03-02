from prettytable import PrettyTable
import datetime

class Person:
    _id = ''
    NAME = ''
    SEX = ''
    BIRT = 'N/A'
    DEAT = 'N/A'
    FAMC = []
    FAMS = []

class Family:
    _id = ''
    MARR = ''
    DIV = 'N/A'
    HUSB = ''
    WIFE = ''
    CHIL = []

def print_people(d):
    table = PrettyTable()
    table.field_names = ['ID', 'NAME', 'SEX', 'BIRTHDAY', 'DEATH', 'FAMC', 'FAMS']
    for key in d:
        table.add_row([d[key]._id, d[key].NAME, d[key].SEX, d[key].BIRT, d[key].DEAT, d[key].FAMC, d[key].FAMS])
    print(table)

def print_family(d):
    table = PrettyTable()
    table.field_names = ['ID', 'MARRIED', 'DIVORCED', 'HUSBAND ID', 'WIFE ID', 'CHILDREN']
    for key in d:
        table.add_row([d[key]._id, d[key].MARR, d[key].DIV, d[key].HUSB, d[key].WIFE, d[key].CHIL])
    print(table)

def date_format(date):
    months = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 
                'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}
    split_date = date.split(' ')
    d = int(split_date[0])
    m = months[split_date[1]]
    y = int(split_date[2])
    date = datetime.date(y, m, d)
    return date

def dateverify(date):
    try:
        date_format(date)
    except ValueError:
        return False
    return True

def us03(birth, death):
    return birth < death

def gedcom(file_name):
    tags = {0:["INDI", "FAM", "HEAD", "TRLR", "NOTE"], 
            1:["NAME", "SEX", "BIRT", "DEAT","FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"], 
            2:["DATE"]}

    make_indiv = False
    make_fam = False
    born = False
    died = False
    married = False
    divorced = False
    valid = False
    
    people = {}
    families = {}

    with open(file_name) as f:
        for line in f:
            line = line.rstrip()
            splitline = line.split(' ')
            level = int(splitline[0])
            tag = splitline[1]
            temptext = splitline[2:]
            text = ''

            for i, n in enumerate(temptext):
                text = text + n
                if i + 1 != len(temptext): 
                    text = text + ' '
            
            if text == 'INDI' or text == 'FAM':
                tag, text = text, tag
            
            if level == 0:
                if make_indiv == True and valid == True:
                    people[person._id] = person
                make_indiv = False
                if tag == 'INDI' and make_indiv == False:
                    make_indiv = True
                    person = Person()
                    person._id = text
                    person.FAMC = []
                    person.FAMS = []
                    continue
                if make_fam == True:
                    families[family._id] = family
                    make_fam = False
                if tag == 'FAM' and make_fam == False:
                    make_fam = True
                    family = Family()
                    family._id = text
                    family.CHIL = []
                    continue

            if make_indiv == True:
                if level in tags and tag in tags[level]:
                    if born == True:
                        if tag == 'DATE' and dateverify(text): person.BIRT = text
                        born = False
                        continue
                    if died == True:
                        if tag == 'DATE' and dateverify(text): 
                            person.DEAT = text
                            birth = date_format(person.BIRT)
                            death = date_format(person.DEAT)
                        valid = us03(birth, death)
                        died = False
                        continue
                    if tag == 'NAME': person.NAME = text
                    elif tag == 'SEX': person.SEX = text
                    elif tag == 'BIRT': born = True
                    elif tag == 'DEAT': died = True
                    elif tag == 'FAMC': person.FAMC.append(text)
                    elif tag == 'FAMS': person.FAMS.append(text)
            
            if make_fam == True:
                if level in tags and tag in tags[level]:
                    if married == True:
                        if tag == 'DATE' and dateverify(text): family.MARR = text
                        married = False
                        continue
                    if divorced == True:
                        if tag == 'DATE' and dateverify(text): family.DIV = text
                        divorced = False
                        continue
                    if tag == 'HUSB': family.HUSB = text
                    elif tag == 'WIFE': family.WIFE = text
                    elif tag == 'CHIL': family.CHIL.append(text)
                    elif tag == 'MARR': married = True
                    elif tag == 'DIV': divorced = True
    
    return people, families

def main():
    ppl, fam = gedcom("testing.txt")
    print_people(ppl)
    print_family(fam)
    print(dateverify("3 FEB 2018"))

main()
