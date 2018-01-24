
import sys
#string format variables
if sys.platform.startswith("linux"):
    s_bold="\033[1m"
    s_uline="\033[4m"
    s_end="\033[0m"
else:
    s_bold=""
    s_uline=""
    s_end=""

class LoadCase:
    """Load case representig loads

    :param str loadCaseName: string
    :param str memberOfLoadGroup: string
    """
    loadCaseName=None
    loadCaseDescription=None
    memberOfLoadGroup=None
    loadCaseMatrix=None

    def __init__(self,loadCaseName="LC1",loadCaseDescription="",memberOfLoadGroup=None,loadCaseMatrix=[]):
        self.loadCaseName=loadCaseName
        self.loadCaseDescription=loadCaseDescription
        self.memberOfLoadGroup=memberOfLoadGroup
        self.loadCaseMatrix=loadCaseMatrix

    def change(self,loadCaseName=None,loadCaseDescription=None,memberOfLoadGroup=None,loadCaseMatrix=None):
        self.loadCaseName=loadCaseName
        self.loadCaseDescription=loadCaseDescription
        self.memberOfLoadGroup=memberOfLoadGroup


class LoadGroup:
    """Load group representig group of load

    with specific properties
    TODO if load case is permanent can't be exclusive
    """
    loadGroupName=None
    loadGroupDescription=None
    loadGroupType=None              #standard, exclusive
    loadGroupActing=None            #permanent load, variable load,
    loadGroupLoadFactorFav=None
    loadGroupLoadFactorUnfav=None
    loadGroupCombinationFactorPsi0=None
    loadGroupCombinationFactorPsi1=None
    loadGroupCombinationFactorPsi2=None
    loadGroupContainedLoadCases=None


    def __init__(self,loadGroupName="LG1",loadGroupDescription="",loadGroupType="Standard",loadGroupActing="Permanent",loadGroupLoadFactorFav=1.0,loadGroupLoadFactorUnfav=1.35,loadGroupCombinationFactorPsi0=1.0,loadGroupCombinationFactorPsi1=1.0,loadGroupCombinationFactorPsi2=1.0,loadGroupContainedLoadCases=[]):
        self.loadGroupName=loadGroupName
        self.loadGroupDescription=loadGroupDescription
        self.loadGroupType=loadGroupType
        self.loadGroupActing=loadGroupActing
        self.loadGroupLoadFactorFav=loadGroupLoadFactorFav
        self.loadGroupLoadFactorUnfav=loadGroupLoadFactorUnfav
        self.loadGroupCombinationFactorPsi0=loadGroupCombinationFactorPsi0
        self.loadGroupCombinationFactorPsi1=loadGroupCombinationFactorPsi1
        self.loadGroupCombinationFactorPsi2=loadGroupCombinationFactorPsi2
        self.loadGroupContainedLoadCases=loadGroupContainedLoadCases

    def change(self,loadGroupName=None,loadGroupDescription=None,loadGroupType=None,loadGroupActing=None,loadGroupLoadFactorFav=None,loadGroupLoadFactorUnfav=None,loadGroupCombinationFactorPsi0=None,loadGroupCombinationFactorPsi1=None,loadGroupCombinationFactorPsi2=None,loadGroupContainedLoadCases=None):
        self.loadGroupName=loadGroupName
        self.loadGroupDescription=loadGroupDescription
        self.loadGroupType=loadGroupType
        self.loadGroupActing=loadGroupActing
        self.loadGroupLoadFactorFav=loadGroupLoadFactorFav
        self.loadGroupLoadFactorUnfav=loadGroupLoadFactorUnfav
        self.loadGroupCombinationFactorPsi0=loadGroupCombinationFactorPsi0
        self.loadGroupCombinationFactorPsi1=loadGroupCombinationFactorPsi1
        self.loadGroupCombinationFactorPsi2=loadGroupCombinationFactorPsi2
        self.loadGroupContainedLoadCases=loadGroupContainedLoadCases

    def __iter__(self):
        return iter(self.__list)


class LinearCombination:
    """Linear combination

    with specific properties without PSI factors for variable load cases

    :param dir linearCombinationIncludedLoadCases: dir of LC-s objects
    returns Combination key for all internal forces max or min
    """
    linearCombinationName=None
    linearCombinationDescription=None
    loadCasesIntoLComb=None

    def __init__(self,linearCombinationName="LCO1",linearCombinationDescription="",loadCasesIntoLComb=[]):
        self.linearCombinationName=linearCombinationName
        self.linearCombinationDescription=linearCombinationDescription
        self.loadCasesIntoLComb=loadCasesIntoLComb

    def change(self,linearCombinationName=None,linearCombinationDescription=None,loadCasesIntoLComb=None):
        self.linearCombinationName=linearCombinationName
        self.linearCombinationDescription=linearCombinationDescription
        self.loadCasesIntoLComb=loadCasesIntoLComb

    def makeCombination(self,extreme):  #extreme max or min
        #print included combinations list
        strTemp=""
        for i in self.loadCasesIntoLComb:
                strTemp += (i.loadCaseName+",")
        print("Included load case in linear combination:"+ strTemp[0:(len(strTemp)-1)])

        #main iteration for all internal forces
        for internalForce in [0,1,2]:
            tempVarloadcases={"Variable_Standard":[]} #dir contains variable LC + the extrem of Exclusive Variable LC
            #string storing combination key
            combKey=""
            # work out if there is any exclusive load groups and make lists for them
            for i in self.loadCasesIntoLComb:
                #permanent load cases are processes immediately and are added into combkey variable
                if i.memberOfLoadGroup.loadGroupActing == "Permanent":
                    #condition for max and min and determining favorable and unfavorable internal forces - Permanent load cases
                    if extreme == "max":
                        if i.loadCaseMatrix[internalForce]>0:
                            combKey += (i.loadCaseName + "*" + s_bold+str(i.memberOfLoadGroup.loadGroupLoadFactorUnfav)+s_end+ "+")
                        else:
                            combKey += (i.loadCaseName + "*" + s_bold+str(i.memberOfLoadGroup.loadGroupLoadFactorFav)+ s_end+"+")
                    elif extreme == "min":
                        if i.loadCaseMatrix[internalForce]<=0:
                            combKey += (i.loadCaseName + "*" + s_bold+str(i.memberOfLoadGroup.loadGroupLoadFactorUnfav)+ s_end+"+")
                        else:
                            combKey += (i.loadCaseName + "*" +s_bold+str(i.memberOfLoadGroup.loadGroupLoadFactorFav)+ s_end+"+")
                    else:
                        print("Something is wrong with argument extreme: max min (permanent load cases)")
                #variable load cases are sorted by properties "standard" or "Exclusive"
                elif i.memberOfLoadGroup.loadGroupActing == "Variable":
                    #Standard load cases are stored in dir tempVarloadcases under "Variable_standard" key
                    if i.memberOfLoadGroup.loadGroupType == "Standard":
                        tempVarloadcases.get("Variable_Standard").append(i)
                    #exclusive load cases are stored in dir tempVarloadcases under loadGroupName key
                    elif i.memberOfLoadGroup.loadGroupType == "Exclusive":
                        if tempVarloadcases.get(i.memberOfLoadGroup.loadGroupName)==None:
                            tempVarloadcases[i.memberOfLoadGroup.loadGroupName]=[i]
                        else:
                            tempVarloadcases.get(i.memberOfLoadGroup.loadGroupName).append(i)
                else:
                    print("Something is wrong with load case Type assignments")
            #searching the extreme loadcase from exclusives for loadGroup
            for i in tempVarloadcases:
                tempValueMax=None
                tempLCMax=None
                if i!="Variable_Standard":
                    for j in tempVarloadcases[i]:
                        if tempValueMax==None:
                            tempValueMax=j.loadCaseMatrix[internalForce]
                            tempLCMax=j
                        else:
                            if tempValueMax<j.loadCaseMatrix[internalForce]:
                                tempValueMax=j.loadCaseMatrix[internalForce]
                                tempLCMax=j
                            else:
                                tempValueMax=tempValueMax
                    # the extreme loadcase from variable cases is added into Variable_Standard list
                    tempVarloadcases.get("Variable_Standard").append(tempLCMax)

            #condition for max and min and determining favorable and unfavorable internal forces - Variable load cases with extremes from Exclusives LC
            for i in tempVarloadcases.get("Variable_Standard"):
                if extreme == "max":
                    if i.loadCaseMatrix[internalForce]>0:
                        combKey += (i.loadCaseName + "*" + s_bold+str(i.memberOfLoadGroup.loadGroupLoadFactorUnfav)+ s_end+"+")
                    else:
                        combKey += (i.loadCaseName + "*" + s_bold+str(i.memberOfLoadGroup.loadGroupLoadFactorFav)+ s_end+"+")
                elif extreme == "min":
                    if i.loadCaseMatrix[internalForce]<=0:
                        combKey += (i.loadCaseName + "*" + s_bold+str(i.memberOfLoadGroup.loadGroupLoadFactorUnfav)+ s_end+"+")
                    else:
                        combKey += (i.loadCaseName + "*" + s_bold+str(i.memberOfLoadGroup.loadGroupLoadFactorFav)+ s_end+"+")
                else:
                    print("Something is wrong with argument extreme: max min (Variable load cases)")
            #the output of the combination key
            if extreme == "max":
                print("Combination key (max) for internal force labelled as '"+ str(internalForce) +"': " + combKey[0:(len(combKey)-1)])
            elif extreme == "min":
                print("Combination key (min) for internal force labelled as '"+ str(internalForce) +"': " + combKey[0:(len(combKey)-1)])
            else:
                print("Something is wrong with argument extreme: max min (print com bkey)")

class CombinationMSU:
    """combination

    with specific properties with PSI factors for variable load cases ---- See EN 1990, 6.4.3.2 (6.10)

    :param dir linearCombinationIncludedLoadCases: dir of LC-s objects
    returns Combination key for all internal forces max or min
    """
    linearCombinationName=None
    linearCombinationDescription=None
    loadCasesIntoComb=None


    def __init__(self,linearCombinationName="CO1",linearCombinationDescription="",loadCasesIntoComb=[]):
        self.linearCombinationName=linearCombinationName
        self.linearCombinationDescription=linearCombinationDescription
        self.loadCasesIntoComb=loadCasesIntoComb

    def change(self,linearCombinationName=None,linearCombinationDescription=None,loadCasesIntoComb=None):
        self.linearCombinationName=linearCombinationName
        self.linearCombinationDescription=linearCombinationDescription
        self.loadCasesIntoComb=loadCasesIntoComb

    def makeCombination(self,extreme):  #extreme max or min

        #print included combinations list
        strTemp=""
        for i in self.loadCasesIntoComb:
                strTemp += (i.loadCaseName+",")
        print("Included load case in combination MSU:"+ strTemp[0:(len(strTemp)-1)])

        #main iteration for all internal forces
        for internalForce in [0,1,2]:
            tempVarloadcases={"Variable_Standard":[]} #dir contains variable LC + the extrem of Exclusive Variable LC
            #string storing combination key
            combKey=""
            # work out if there is any exclusive load groups and make lists for them
            for i in self.loadCasesIntoComb:
                #permanent load cases are processes immediately and are added into combkey variable
                if i.memberOfLoadGroup.loadGroupActing == "Permanent":
                    #condition for max and min and determining favorable and unfavorable internal forces - Permanent load cases
                    if extreme == "max":
                        if i.loadCaseMatrix[internalForce]>0:
                            combKey += (i.loadCaseName + "*" + s_bold + str(i.memberOfLoadGroup.loadGroupLoadFactorUnfav)+ s_end + "+")
                        else:
                            combKey += (i.loadCaseName + "*" + s_bold + str(i.memberOfLoadGroup.loadGroupLoadFactorFav)+ s_end + "+")
                    elif extreme == "min":
                        if i.loadCaseMatrix[internalForce]<=0:
                            combKey += (i.loadCaseName + "*" + s_bold + str(i.memberOfLoadGroup.loadGroupLoadFactorUnfav)+ s_end + "+")
                        else:
                            combKey += (i.loadCaseName + "*" + s_bold + str(i.memberOfLoadGroup.loadGroupLoadFactorFav)+ s_end + "+")
                    else:
                        print("Something is wrong with argument extreme: max min (permanent load cases)")
                #variable load cases are sorted by properties "standard" or "Exclusive"
                elif i.memberOfLoadGroup.loadGroupActing == "Variable":
                    #Standard load cases are stored in dir tempVarloadcases under "Variable_standard" key
                    if i.memberOfLoadGroup.loadGroupType == "Standard":
                        tempVarloadcases.get("Variable_Standard").append(i)
                    #exclusive load cases are stored in dir tempVarloadcases under loadGroupName key
                    elif i.memberOfLoadGroup.loadGroupType == "Exclusive":
                        if tempVarloadcases.get(i.memberOfLoadGroup.loadGroupName)==None:
                            tempVarloadcases[i.memberOfLoadGroup.loadGroupName]=[i]
                        else:
                            tempVarloadcases.get(i.memberOfLoadGroup.loadGroupName).append(i)
                else:
                    print("Something is wrong with load case Type assignments")
            #searching the extreme loadcase from exclusives for loadGroup
            for i in tempVarloadcases:
                tempValueMax=None
                tempLCMax=None
                if i!="Variable_Standard":
                    for j in tempVarloadcases[i]:
                        if tempValueMax==None:
                            tempValueMax=j.loadCaseMatrix[internalForce]
                            tempLCMax=j
                        else:
                            if tempValueMax<j.loadCaseMatrix[internalForce]:
                                tempValueMax=j.loadCaseMatrix[internalForce]
                                tempLCMax=j
                            else:
                                tempValueMax=tempValueMax
                    # the extreme loadcase from variable cases is added into Variable_Standard list
                    tempVarloadcases.get("Variable_Standard").append(tempLCMax)
            #work out leading load case
            #isLeadingLoadCase=LC12


            isLeadingLoadCase=None
            theExtreme=0
            for i in tempVarloadcases.get("Variable_Standard"):
                if isLeadingLoadCase==None:
                    isLeadingLoadCase=i
                    if extreme == "max":
                        for j in tempVarloadcases.get("Variable_Standard"):
                            if j.loadCaseMatrix[internalForce]>0:
                                if i==j:
                                    theExtreme += j.loadCaseMatrix[internalForce]*j.memberOfLoadGroup.loadGroupLoadFactorUnfav
                                else:
                                    theExtreme += j.loadCaseMatrix[internalForce]*j.memberOfLoadGroup.loadGroupLoadFactorUnfav*j.memberOfLoadGroup.loadGroupCombinationFactorPsi0
                            elif j.loadCaseMatrix[internalForce]<=0:
                                if i==j:
                                    theExtreme += j.loadCaseMatrix[internalForce]*j.memberOfLoadGroup.loadGroupLoadFactorFav
                                else:
                                    theExtreme += j.loadCaseMatrix[internalForce]*j.memberOfLoadGroup.loadGroupLoadFactorFav*j.memberOfLoadGroup.loadGroupCombinationFactorPsi0
                            else:
                                print("Something is wrong with argument extreme: max min (variable standard load cases)")
                    elif extreme == "min":
                        for j in tempVarloadcases.get("Variable_Standard"):
                            if j.loadCaseMatrix[internalForce]>0:
                                if i==j:
                                    theExtreme += j.loadCaseMatrix[internalForce]*j.memberOfLoadGroup.loadGroupLoadFactorFav
                                else:
                                    theExtreme += j.loadCaseMatrix[internalForce]*j.memberOfLoadGroup.loadGroupLoadFactorFav*j.memberOfLoadGroup.loadGroupCombinationFactorPsi0
                            elif j.loadCaseMatrix[internalForce]<=0:
                                if i==j:
                                    theExtreme += j.loadCaseMatrix[internalForce]*j.memberOfLoadGroup.loadGroupLoadFactorUnfav
                                else:
                                    theExtreme += j.loadCaseMatrix[internalForce]*j.memberOfLoadGroup.loadGroupLoadFactorUnfav*j.memberOfLoadGroup.loadGroupCombinationFactorPsi0
                            else:
                                print("Something is wrong with argument extreme: max min (variable standard load cases)")
                    else:
                        print ("Something is wrong with argument extreme: max min (variable standard load cases)")

                else:
                    if extreme == "max":
                        theExtreme_temp=0
                        for j in tempVarloadcases.get("Variable_Standard"):
                            if j.loadCaseMatrix[internalForce]>0:
                                if i==j:
                                    theExtreme_temp += j.loadCaseMatrix[internalForce]*j.memberOfLoadGroup.loadGroupLoadFactorUnfav
                                else:
                                    theExtreme_temp += j.loadCaseMatrix[internalForce]*j.memberOfLoadGroup.loadGroupLoadFactorUnfav*j.memberOfLoadGroup.loadGroupCombinationFactorPsi0
                            elif j.loadCaseMatrix[internalForce]<=0:
                                if i==j:
                                    theExtreme_temp += j.loadCaseMatrix[internalForce]*j.memberOfLoadGroup.loadGroupLoadFactorFav
                                else:
                                    theExtreme_temp += j.loadCaseMatrix[internalForce]*j.memberOfLoadGroup.loadGroupLoadFactorFav*j.memberOfLoadGroup.loadGroupCombinationFactorPsi0
                            else:
                                print("Something is wrong with argument extreme: max min (permanent load cases)")
                    elif extreme == "min":
                        theExtreme_temp=0
                        for j in tempVarloadcases.get("Variable_Standard"):
                            if j.loadCaseMatrix[internalForce]>0:
                                if i==j:
                                    theExtreme_temp += j.loadCaseMatrix[internalForce]*j.memberOfLoadGroup.loadGroupLoadFactorFav
                                else:
                                    theExtreme_temp += j.loadCaseMatrix[internalForce]*j.memberOfLoadGroup.loadGroupLoadFactorFav*j.memberOfLoadGroup.loadGroupCombinationFactorPsi0
                            elif j.loadCaseMatrix[internalForce]<=0:
                                if i==j:
                                    theExtreme_temp += j.loadCaseMatrix[internalForce]*j.memberOfLoadGroup.loadGroupLoadFactorUnfav
                                else:
                                    theExtreme_temp += j.loadCaseMatrix[internalForce]*j.memberOfLoadGroup.loadGroupLoadFactorUnfav*j.memberOfLoadGroup.loadGroupCombinationFactorPsi0
                            else:
                                print("Something is wrong with argument extreme: max min (variable standard load cases)")
                    else:
                        print("Something is wrong with argument extreme: max min (variable standard load cases)")

                        #assign the extremem load case
                    if extreme == "max":
                        if theExtreme_temp>theExtreme:
                            isLeadingLoadCase=j
                    elif extreme == "min":
                        if theExtreme_temp<=theExtreme:
                            isLeadingLoadCase=j
                    else:
                        print ("Something is wrong with max min")

            #condition for max and min and determining favorable and unfavorable internal forces - Variable load cases with extremes from Exclusives LC
            for i in tempVarloadcases.get("Variable_Standard"):
                if extreme == "max":
                    if i.loadCaseMatrix[internalForce]>0 and i!=isLeadingLoadCase:
                        combKey += (i.loadCaseName + "*" + s_bold + str(i.memberOfLoadGroup.loadGroupLoadFactorUnfav)+ s_end+ "*" + s_uline+str(i.memberOfLoadGroup.loadGroupCombinationFactorPsi0) + s_end + "+")
                    elif i.loadCaseMatrix[internalForce]>0 and i==isLeadingLoadCase:
                        combKey += (i.loadCaseName + "*" + s_bold + str(i.memberOfLoadGroup.loadGroupLoadFactorUnfav)+ s_end+ "+")
                    elif i.loadCaseMatrix[internalForce]<=0 and i!=isLeadingLoadCase:
                        combKey += (i.loadCaseName + "*" + s_bold + str(i.memberOfLoadGroup.loadGroupLoadFactorFav)+ s_end+ "*" + s_uline+str(i.memberOfLoadGroup.loadGroupCombinationFactorPsi0) + s_end + "+")
                    elif i.loadCaseMatrix[internalForce]<=0 and i==isLeadingLoadCase:
                        combKey += (i.loadCaseName + "*" + s_bold + str(i.memberOfLoadGroup.loadGroupLoadFactorFav)+ s_end+ "+")
                    else:
                        print("Something is wrong with argument extreme: max min (Variable load cases)")
                elif extreme == "min":
                    if i.loadCaseMatrix[internalForce]<=0 and i!=isLeadingLoadCase:
                        combKey += (i.loadCaseName + "*" + s_bold + str(i.memberOfLoadGroup.loadGroupLoadFactorUnfav)+ s_end+ "*" + s_uline+str(i.memberOfLoadGroup.loadGroupCombinationFactorPsi0) + s_end + "+")
                    elif i.loadCaseMatrix[internalForce]<=0 and i==isLeadingLoadCase:
                        combKey += (i.loadCaseName + "*" + s_bold + str(i.memberOfLoadGroup.loadGroupLoadFactorUnfav)+ s_end+ "+")
                    elif i.loadCaseMatrix[internalForce]>0 and i!=isLeadingLoadCase:
                        combKey += (i.loadCaseName + "*" + s_bold + str(i.memberOfLoadGroup.loadGroupLoadFactorFav)+ s_end+ "*" + s_uline+str(i.memberOfLoadGroup.loadGroupCombinationFactorPsi0) + s_end + "+")
                    elif i.loadCaseMatrix[internalForce]>0 and i==isLeadingLoadCase:
                        combKey += (i.loadCaseName + "*" + s_bold + str(i.memberOfLoadGroup.loadGroupLoadFactorFav)+ s_end+ "+")
                    else:
                        print("Something is wrong with argument extreme: max min (Variable load cases)")
                else:
                    print("Something is wrong with argument extreme: max min (Variable load cases)")
            #the output of the combination key
            if extreme == "max":
                print("Combination key (max) for internal force labelled as '"+ str(internalForce) +"': " + combKey[0:(len(combKey)-1)])
            elif extreme == "min":
                print("Combination key (min) for internal force labelled as '"+ str(internalForce) +"': " + combKey[0:(len(combKey)-1)])
            else:
                print("Something is wrong with argument extreme: max min (print com bkey)")


#make default LC and LG
LG1=LoadGroup()
loadGroups=[LG1]
LC1=LoadCase(memberOfLoadGroup=LG1,loadCaseMatrix=[-10,-5,457])
LG1.loadGroupContainedLoadCases.append("LC1")

##test load cases and groups
LG2=LoadGroup("LG2","", "Exclusive", "Variable", 1.0, 1.35, 0.9, 1.0, 1.0, [])
loadGroups.append(LG2)

LG3=LoadGroup("LG3","", "Exclusive", "Variable", 1.0, 1.35, 0.8, 1.0, 1.0, [])
loadGroups.append(LG3)

LG4=LoadGroup("LG4","", "Standard", "Variable", 1.0, 1.35, 0.65, 1.0, 1.0, [])
loadGroups.append(LG4)

LC2=LoadCase("LC2", "",LG1, [1.018,-5.145,45.7])
LG1.loadGroupContainedLoadCases.append("LC2")

LC3=LoadCase("LC3","", LG1, [10.40,5.48,-0.457])
LG1.loadGroupContainedLoadCases.append("LC3")

LC4=LoadCase("LC4","", LG2, [-5,-5,-4])
LG2.loadGroupContainedLoadCases.append("LC4")

LC5=LoadCase("LC5","", LG2, [1,-5,4])
LG2.loadGroupContainedLoadCases.append("LC5")

LC6=LoadCase("LC6","", LG2, [-8,5,7])
LG2.loadGroupContainedLoadCases.append("LC6")

LC7=LoadCase("LC7","", LG3, [5,-5,-7])
LG3.loadGroupContainedLoadCases.append("LC7")

LC8=LoadCase("LC8","", LG3, [8,18,-2.6])
LG3.loadGroupContainedLoadCases.append("LC8")

LC9=LoadCase("LC9","", LG3, [3,-50,45.7])
LG3.loadGroupContainedLoadCases.append("LC9")

LC10=LoadCase("LC10","", LG1, [1.0,-5.014,14.57])
LG1.loadGroupContainedLoadCases.append("LC10")

LC11=LoadCase("LC11","", LG4, [0.03,-15.4,4.57])
LG4.loadGroupContainedLoadCases.append("LC11")

LC12=LoadCase("LC12","", LG4, [-16,3.4,-4])
LG4.loadGroupContainedLoadCases.append("LC12")

'''' print(LG1.loadGroupContainedLoadCases)
print(LG2.loadGroupContainedLoadCases)
print(LG3.loadGroupContainedLoadCases)
print(LC1.memberOfLoadGroup.loadGroupName)
print(LC2.memberOfLoadGroup.loadGroupName)
print(LC3.memberOfLoadGroup.loadGroupName)
print(LC4.memberOfLoadGroup.loadGroupName)
print(LC5.memberOfLoadGroup.loadGroupName)
print(LC6.memberOfLoadGroup.loadGroupName)
print(LC7.memberOfLoadGroup.loadGroupName)
print(LC8.memberOfLoadGroup.loadGroupName)
print(LC9.memberOfLoadGroup.loadGroupName)
print(LC10.memberOfLoadGroup.loadGroupName)'''

lincomb=LinearCombination("linComb","popis",[LC1,LC2,LC10,LC3,LC4,LC5,LC6])
lincomb.makeCombination("max")
lincomb.makeCombination("min")
comb=CombinationMSU("comb","popis",[LC1,LC2,LC3,LC4,LC5,LC6,LC7,LC8,LC9,LC11,LC12])
comb.makeCombination("max")
comb.makeCombination("min")

