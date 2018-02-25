class Individual:
    _id = ''
    NAME = ''
    SEX = ''
    BIRT = ''
    DEAT = ''
    FAMC = []
    FAMS = []

class Family:
    _id = ''
    MARR = ''
    DIV = ''
    HUSB = ''
    WIFE = ''
    CHIL = []

fam = open("families.txt", "w+")
ind = open("individuals.txt", "w+")

tags = {0:["INDI", "FAM", "HEAD", "TRLR", "NOTE"], 
        1:["NAME", "SEX", "BIRT", "DEAT","FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"], 
        2:["DATE"]}

make_indiv = False
make_fam = False
born = False
died = False
married = False
divorced = False

with open("testing.txt") as f:
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
                indi_string = ''
                indi_famc = ''
                indi_fams = ''
                indi_famc = '{' + " ".join(individual.FAMC) + '}'
                indi_fams = '{' + " ".join(individual.FAMS) + '}'
                indi_string = (individual._id + ',' + individual.NAME + ',' + individual.SEX + ',' + individual.BIRT 
                                + ',' + individual.DEAT + ',' + indi_famc + ',' + indi_fams)
                ind.write(indi_string + '\n')
                make_indiv = False
            if tag == 'INDI' and make_indiv == False:
                make_indiv = True
                individual = Individual()
                individual._id = text
                individual.FAMC = []
                Individual.FAMS = []
                continue
            if make_fam == True:
                fam_string = ''
                fam_chil = ''
                fam_chil = '{' + " ".join(family.CHIL) + '}'
                fam_string = family._id + ',' + family.MARR + ',' + family.DIV + ',' + family.HUSB + ',' + family.WIFE + ',' + fam_chil
                fam.write(fam_string + '\n')
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
                    if tag == 'DATE': individual.BIRT = text
                    born = False
                    continue
                if died == True:
                    if tag == 'DATE': individual.DEAT = text
                    died = False
                    continue
                if tag == 'NAME': individual.NAME = text
                elif tag == 'SEX': individual.SEX = text
                elif tag == 'BIRT': born = True
                elif tag == 'DEAT': died = True
                elif tag == 'FAMC': individual.FAMC.append(text)
                elif tag == 'FAMS': individual.FAMS.append(text)
        
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

fam.close()
ind.close()
print 'done'