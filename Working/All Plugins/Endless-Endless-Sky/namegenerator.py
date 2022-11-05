import random
import math


class Namegenerator:
    def __init__(self,faction=None) -> None:
        self.az = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()
        self.vowels = 'a e i o u'.split()
        self.seed = 0
        if faction != None:
            if faction.devmode:
                #random.seed(faction.devmodeseed)
                self.seed = faction.devmodeseed
                pass
        

    def completelyRandomNames(self,minlength=4,maxlength=7):
        if False:
            randname = []
            n = 0
            for i in range(random.randrange(minlength,maxlength)):
                randname.append(random.choice(list(self.az)))
                if(1 == random.randrange(1,3) or n == 2):
                    randname.append(random.choice(list(self.vowels)))
                n += 1
        wordlist = []
        for i in range(random.randrange(math.ceil(minlength/3),math.ceil(maxlength/3))):
            #random.seed(self.seed+i)
            wordlist.append(self.generateRandomShortWord())
        random.shuffle(wordlist)
        randnamestr = ""
        randnamestr = randnamestr.join(wordlist)
        randnamestr = randnamestr.capitalize()
        return randnamestr

    def generateNameFromRules(self,minlength=4,maxlength=7,wordlen=3,spacechance=.5,lang_charweight=None,seed=None):
        wordlist = []
        #if self.seed != 0:
            #random.seed(seed)
        loopcount = range(random.randrange(math.ceil(minlength/3),math.ceil(maxlength/3)))
        for i in loopcount:
            #random.seed(self.seed+i)
            wordlist.append(self.generateRandomShortWord(wordlen=wordlen,lang_charweight=lang_charweight))
            if random.random() <= spacechance:
                wordlist.append(" ")
        #random.shuffle(wordlist) #and i != 0 and i != len(loopcount)
        randnamestr = ""
        randnamestr = randnamestr.join(wordlist)
        while randnamestr.endswith(" ") or randnamestr.startswith(" "):
            randnamestr = randnamestr.removesuffix(" ")
            randnamestr = randnamestr.removeprefix(" ")
        randnamestr = randnamestr.capitalize()
        return randnamestr

    def generateRandomShortWord(self,wordlen=3,lang_charweight=None):
        randword = []
        vowelchance = .33
        for i in range(wordlen):
            #if self.seed != 0:
                #random.seed(self.seed+i)
            if random.random() < vowelchance:
                randword.append(random.choice(list(self.vowels)))
                vowelchance -= .33
            else:
                vowelchance += .33
                wordsel = random.choices(self.az,lang_charweight)
                randword.append(wordsel[0])
        finalstr = ""
        finalstr = finalstr.join(randword)
        return finalstr

    def generateInitials(self,string=''):
        inilist = []
        if string.count(' ') > 0:
            inilist = string.split()
        else:
            wordlen = round(len(string)/3)
            for a in range(len(string)):
                if a % wordlen == 0:
                    inilist.append(string[a])
        initOut = ''
        for n in inilist:
            initOut = initOut + n[0].upper() + '.'

        return initOut

    def randomfromExisting(self,refname,minlength=4,maxlength=6): #Very crude, improve later. todo
        name = list([c for c in refname])
        random.shuffle(name)
        newname = []
        i = 0
        while len(newname) < random.randrange((minlength),maxlength):
            #if self.seed != 0:
                #random.seed(self.seed+i)
            try:
                newname.append(name[i])
            except IndexError:
                newname.append(random.choice(list(self.az)))
            if len(newname) < minlength:
                newname.insert(random.randrange(len(newname)),random.choice(list(self.az)))
            if random.random() >= 0.3 and not (len(newname) < minlength):
                newname.pop(random.randrange(0,len(newname)))
            if random.random() >= 0.3:
                newname.insert(random.randrange(len(newname)),random.choice(list(self.az)))
            i += 1
        outname = ""
        for x in newname:
            outname += x
        outname = outname.casefold()
        outname = outname.capitalize()
        #print("name generated: ", outname)
        return outname

    def fromFileNames(self,filename):
        try:
            filein = open(filename, 'r')
        except FileNotFoundError:
            return False
        full = filein.readlines()
        filein.close()
        return full[random.randrange(len(full))]

    def fromESformatNames(self,filename):
        try:
            filein = open(filename, 'r')
        except FileNotFoundError:
            return False
        full = filein.readlines()
        filein.close()
        for line in full :
            if line.startswith("phrase"):
                nametype = line[6:]
        pass



def generate_namefile(faction,fileout=''):
    """
    namemodes 'pregen' 'parts'
    nametype  'civie' 'military'
    """
    if fileout == '':
        fileout = f'data/{faction.name}/{faction.name} names.txt'

    namegen = Namegenerator(faction)

    name_needed = 150

    filewrite = open(fileout,'w')
    
    
    minlen = 4
    maxlen = 16
    partscount = 3
    for mainloop in range(2):
        if mainloop == 1:
            filewrite.write(f'phrase "{faction.name} Military names"' + '\n')
            filewrite.write(f'\tword' + '\n')
            filewrite.write(f'\t\t"{faction.militaryinit}"' + '\n')
            namemode = faction.militnametype
        else:
            filewrite.write(f'phrase "{faction.name} names"' + '\n')
            namemode = faction.civienametype
        if namemode == 'pregen':
            filewrite.write(f'\tword' + '\n')
            for n in range(name_needed):
                name = namegen.generateNameFromRules(minlen,
                                                maxlen,
                                                wordlen=faction.lang_wordlen,
                                                spacechance=faction.lang_spacechance,
                                                lang_charweight=faction.lang_charweight)
                filewrite.write(f'\t\t"{name}"' + '\n')
        elif namemode == 'parts':
            
            for k in range(partscount):
                filewrite.write(f'\tword' + '\n')
                for n in range(round(name_needed/2)):
                    name = namegen.generateRandomShortWord(wordlen=faction.lang_wordlen,lang_charweight=faction.lang_charweight)
                    if k == 0:
                        name = name.capitalize()
                    if random.random() <= faction.lang_spacechance:
                        name = name + ' '
                    filewrite.write(f'\t\t"{name}"' + '\n')
    filewrite.close()

if False:
    namegen = Namegenerator()
    nametestlist =[]
    for n in range(50):
        nametestlist.append(namegen.generateNameFromRules(minlength=4,maxlength=7))
        print(nametestlist[n])