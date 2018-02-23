f = open("proj02test.txt")
textlist = f.read().split("\n")
tags = {0:["INDI", "FAM", "HEAD", "TRLR", "NOTE"], 1:["NAME", "SEX", "BIRT", "DEAT","FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"], 2:["DATE"]}
gedcom = []

for e in textlist:
    splitline = e.split(" ")
    if len(splitline) >=3:
        line = []
        templevel = splitline[0]
        temptag = splitline[1]
        temparglist = splitline[2:]
        temparg = ""

        for i,n in enumerate(temparglist):
            temparg = temparg + n
            if i+1 != len(temparglist):
                temparg = temparg + " "
        
        line.append(templevel)
        if temparg == "INDI" or temparg == "FAM":
            line.append(temparg)
            line.append(temptag)
        else:
            line.append(temptag)
            line.append(temparg)

        gedcom.append(line)

for i,line in enumerate(gedcom):
    validity = "Y"
    print("--> " + gedcom[i][0] + " " + gedcom[i][1] + " " + gedcom[i][2])
    if int(line[0]) not in tags:
        validity = "N"
    else:
        if line[1] not in tags[int(line[0])]:
            validity = "N"
    print("<-- " + gedcom[i][0] + "|" + gedcom[i][1] + "|" + validity + "|" + gedcom[i][2])