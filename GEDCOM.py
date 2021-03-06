from prettytable import PrettyTable
import datetime
#testline
class Person:
    _id = ''
    NAME = ''
    SEX = ''
    BIRT = 'N/A'
    DEAT = 'N/A'
    FAMC = []
    FAMS = []
    AGE = 'N/A'

class Family:
    _id = ''
    MARR = 'N/A'
    DIV = 'N/A'
    HUSB = ''
    WIFE = ''
    CHIL = []

def print_people(d):
    table = PrettyTable()
    table.field_names = ['ID', 'NAME', 'SEX', 'BIRTHDAY', 'AGE', 'DEATH', 'FAMC', 'FAMS']
    for key in d:
        table.add_row([d[key]._id, d[key].NAME, d[key].SEX, d[key].BIRT, d[key].AGE, d[key].DEAT, d[key].FAMC, d[key].FAMS])
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
    #user story 41
    if len(split_date) < 3:
        if split_date[0] in months:
            d = 1
            m = months[split_date[0]]
            y = int(split_date[1])
        if len(split_date) == 1:
            d = 1
            m = 1
            y = int(split_date[0])
    else:
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
    #user story 29
    dlist = []
    didlist = []
    for key,value in indi.items():
        if value.DEAT != "N/A" and value.DEAT !="":
            dlist.append(value.NAME + ", " + value._id)
            didlist.append(value._id)
    print("US 29: List of the deceased: " + str(dlist))
    return didlist

def deceasedidlist(indi):
    didlist = []
    for key,value in indi.items():
        if value.DEAT != "N/A" and value.DEAT !="":
            didlist.append(value._id)
    return didlist

def livingmarriedlist(indi, fam):
    #user story 30
    llist = []
    mlist = []
    lmlist = []
    for key,value in indi.items():
        if value.DEAT == "N/A":
            llist.append(value._id)
    for key,value in fam.items():
        if value.MARR != "N/A" and value.DIV == "N/A" and (value.HUSB not in deceasedidlist(indi) and value.WIFE not in deceasedidlist(indi)):
            mlist.append(value.HUSB)
            mlist.append(value.WIFE)
    for i in llist:
        if i in mlist:
            lmlist.append(i)
    print("US 30: List of living and married: " + str(lmlist))
    return lmlist

def singlelist(indi, fam):
    #user story 31
    otlist = []
    mlist = []
    sotlist = []
    for key,value in indi.items():
        if value.AGE != "N/A":
            if int(value.AGE) >= 30:
                otlist.append(value._id)
    for key,value in fam.items():
        if value.MARR != "N/A" and value.DIV == "N/A" and (value.HUSB not in deceasedidlist(indi) and value.WIFE not in deceasedidlist(indi)):
            mlist.append(value.HUSB)
            mlist.append(value.WIFE)
    for i in otlist:
        if i not in mlist:
            sotlist.append(i)
    print("US 31: List of single and over 30: " + str(sotlist))
    return sotlist

def childcheck(fam):
    #user story 15
    for key,value in fam.items():
        if len(value.CHIL) >= 15:
            print("Error US15: Family " + value._id + " has 15 or more children.")
            return False
    return True

def findage(date):
    #user story 27
    return int((datetime.date.today() - date_format(date)).days/365.25)

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

def us05(person, family):
    marriage = date_format(family.MARR)
    death = date_format(person.DEAT)
    if marriage < death:
        return True
    print ('Error US05: Date of death of ' + person.NAME + ' (' + person._id + ') occurs before the date they were married.')
    return False

def us06(person, family):
    divorce = date_format(family.DIV)
    death = date_format(person.DEAT)
    if divorce < death:
        return True
    print ('Error US06: Date of death of ' + person.NAME + ' (' + person._id + ') occurs before the date they were divorced.')
    return False

def us07(person):
    today = datetime.date.today()
    if person.DEAT != 'N/A' and person.BIRT != 'N/A':
        if dateverify(person.DEAT) and dateverify(person.BIRT):
            death = date_format(person.DEAT)
            birth = date_format(person.BIRT)
            if (abs((death - birth).days) / 365.25) >= 150:
                print ('Error US07: Date of death of ' + person.NAME + ' (' + person._id + ') is greater than 150 years after birth.')
                return False
            return True

    if person.BIRT != 'N/A':
        if dateverify(person.BIRT):
            birth = date_format(person.BIRT)
            if (abs((birth - today).days) / 365.25) >= 150:
                print ('Error US07: Date of birth of ' + person.NAME + ' (' + person._id + ') is not in the last 150 years.')
                return False
            return True

def us10(person, family):
    marriage_age = (date_format(family.MARR) - date_format(person.BIRT)).days/365.25
    if marriage_age < 14:
        print ('Error US10: ' + person.NAME + ' (' + person._id + ') is under 14 years old and should not be married.')
        return False
    return True

def us21(person, family):
    if person.SEX == 'M':
        if person._id != family.HUSB:
            print ('Error US21: ' + person.NAME + ' (' + person._id + ') not male but they are the family husband.')
            return False
        return True
    if person.SEX == 'F':
        if person._id != family.WIFE:
            print ('Error US21: ' + person.NAME + ' (' + person._id + ') not female but they are the family wife.')
            return False
        return True

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
                    us07(person)
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
                    if family.HUSB != '': us21(people[family.HUSB], family)
                    if family.WIFE != '': us21(people[family.WIFE], family)
                    if family.MARR != 'N/A':
                        us02(people[family.HUSB], family)
                        us02(people[family.WIFE], family)
                        us10(people[family.HUSB], family)
                        us10(people[family.WIFE], family)
                        if family.DIV != 'N/A': 
                            us04(family)
                            if people[family.HUSB].DEAT != 'N/A': us06(people[family.HUSB], family)
                            if people[family.WIFE].DEAT != 'N/A': us06(people[family.WIFE], family)
                        if people[family.HUSB].DEAT != 'N/A': us05(people[family.HUSB], family)
                        if people[family.WIFE].DEAT != 'N/A': us05(people[family.WIFE], family)                         
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
                        if tag == 'DATE':
                            person.BIRT = text
                            if dateverify(text) and dbeforecurrent(text):
                                person.AGE = findage(text)
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
    ppl, fam = gedcom("fulltesting.txt")
    datecheck(ppl, fam)
    childcheck(fam)
    print_people(ppl)
    print_family(fam)
    deceasedlist(ppl)
    livingmarriedlist(ppl, fam)
    singlelist(ppl, fam)

main()