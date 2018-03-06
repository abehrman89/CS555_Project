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
    MARR = 'N/A'
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
    #user story 42
    try:
        date_format(date)
    except ValueError:
        print("Error US42: " + date + " is an invalid date.")
        return False
    return True

def dbeforecurrent(date):
    #user story 1
    if dateverify(date):
        today = datetime.date.today()
        tobetested = date_format(date)
        if tobetested>today:
            print("Error US01: " + date + " is after today's date.")
        return tobetested<today

def datecheck(indi, fam):
    for key,value in indi.items():
        if value.BIRT != "N/A" and value.BIRT != "":
            dbeforecurrent(value.BIRT)
        if value.DEAT != "N/A" and value.DEAT !="":
            dbeforecurrent(value.DEAT)
        
    for key,value in fam.items():
        if value.MARR != "N/A" and value.MARR != "":
            dbeforecurrent(value.MARR)
        if value.DIV != "N/A" and value.DIV != "":
            dbeforecurrent(value.DIV)

def deceasedlist(indi):
    dlist = []
    for key,value in indi.items():
        if value.DEAT != "N/A" and value.DEAT !="":
            dlist.append(value.NAME + ", " + value._id)
    print("List of the deceased: " + str(dlist))
    return dlist

def us03(person):
    death = date_format(person.DEAT)
    birth = date_format(person.BIRT)
    if birth < death:
        return True
    print('Error US03: Birth date of ' + person.NAME + ' (' + person._id + ') occurs after their date of death.')
    return False

def us02(person, family):
    birth = date_format(person.BIRT)
    marriage = date_format(family.MARR)
    if birth < marriage:
        return True
    print ('Error US02: Birth date of ' + person.NAME + ' (' + person._id + ') occurs after the date they were married.')
    return False

def us04(family):
    marriage = date_format(family.MARR)
    divorce = date_format(family.DIV)
    if marriage < divorce:
        return True
    print('Error US04: Marriage date of ' + family._id + ' occurs after the divorce date.')
    return False

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
                if make_indiv == True:
                    if person.BIRT != 'N/A' and person.DEAT != 'N/A': us03(person)
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
                    if family.MARR != 'N/A':
                        us02(people[family.HUSB], family)
                        us02(people[family.WIFE], family)
                        if family.DIV != 'N/A': us04(family)
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
                        if tag == 'DATE': person.BIRT = text
                        born = False
                        continue
                    if died == True:
                        if tag == 'DATE': person.DEAT = text
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
                        if tag == 'DATE': family.MARR = text
                        married = False
                        continue
                    if divorced == True:
                        if tag == 'DATE': family.DIV = text
                        divorced = False
                        continue
                    if tag == 'HUSB': family.HUSB = text
                    elif tag == 'WIFE': family.WIFE = text
                    elif tag == 'CHIL': family.CHIL.append(text)
                    elif tag == 'MARR': married = True
                    elif tag == 'DIV': divorced = True
    
    return people, families

def main():
    ppl, fam = gedcom("MyFamilyTreeGEDCOM.txt")
    datecheck(ppl, fam)
    print_people(ppl)
    print_family(fam)
    deceasedlist(ppl)

main()
