import pygame
import string
import copy
import os
import sys

# file directory
base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

print('===== debugging logs =====')

onesym = 0
variable = ''

screenWidth = 1100
screenHeight = 700

# Steps List
steps = []
# Formatting of things inside list:
# (operation, step type, pre-change char1, p1, c2, p2 post-change char1, p1, c2, p2)

# Color Palette
# Note: Col1 was adjusted from research due to difference from
# how it was meant to look. It was made darker.
col1 = (32, 42, 84)
col2 = (87, 86, 147)
col3 = (123, 102, 157)
col4 = (231, 196, 238)
col5 = (255, 255, 255)
col6 = (255, 241, 184)

# Font
fontF = os.path.join(base, 'SpaceMono-Regular.ttf')
fontBoldF = os.path.join(base, 'SpaceMono-Bold.ttf')

# Parsing the characters
def parse(chars):
    parsedL = []
    parsedR = []
    parsed = []
    equalPassed = False
    alphabet = list(string.ascii_lowercase + string.ascii_uppercase)
    numbers = list(string.digits)
    for char in chars:
        if char == ' ':
            pass
        elif char == '+':
            parsed.append('+')
        elif char == '-':
            parsed.append('-')
        elif char == '/':
            parsed.append('/')
        elif char == '*':
            parsed.append('*')
        elif char in alphabet:
            parsed.append('var')
            global variable
            variable = char
        elif char in numbers:
            parsed.append('const')
        elif char == '(':
            parsed.append('(')
        elif char == ')':
            parsed.append(')')
        elif char == '=':
            parsed.append('=')
            equalPassed = True
        else:
            pass
        if equalPassed == False:
            parsedL.append(parsed[0])
        else:
            if parsed[0] != '=':
                parsedR.append(parsed[0])
        parsed = []
    print(parsedL)
    print(parsedR)
    return parsedL, parsedR

def separate(chars):
    equalPassed = False
    charL = []
    charR = []
    for char in chars:
        if char == '=':
            equalPassed = True
        elif equalPassed == False:
            charL.append(char)
        else:
            charR.append(char)
    print(charL)
    print(charR)
    return charL, charR

def combine(parsed, t, onesym):
    index = 0
    oplistP = []
    oplistN = []
    sublistP = []
    sublistN = []
    addend = 0
    subIndex = 0
    while index < len(parsed):
        sep = parsed[index]
        if t == 1:
            oplistP.append(parsed1[index])
            oplistN.append(char1[index])
            if sep == 'const':
                sublistP.append(parsed1[index])
                sublistN.append(char1[index])
                subIndex = 1
                remainConst = True
                while remainConst:
                    if index+subIndex < len(parsed):
                        if parsed1[index+subIndex] == 'const':
                            sublistP.append(parsed1[index+subIndex])
                            sublistN.append(char1[index+subIndex])
                            subIndex += 1
                        else:
                            remainConst = False
                    else:
                        remainConst = False
                if len(sublistP) > 1:
                    oplistP.pop()
                    oplistN.pop()
                    num = ''
                    subIndex2 = 0
                    for const in sublistP:
                        num += str(sublistN[subIndex2])
                        subIndex2 += 1
                    oplistP.append('const')
                    oplistN.append(num)
                index += (subIndex - 1)
                subIndex = 0
                
        if t == 2:
            oplistP.append(parsed2[index])
            oplistN.append(char2[index])
            if sep == 'const':
                sublistP.append(parsed2[index])
                sublistN.append(char2[index])
                subIndex = 1
                remainConst = True
                while remainConst:
                    if index+subIndex < len(parsed):
                        if parsed2[index+subIndex] == 'const':
                            sublistP.append(parsed2[index+subIndex])
                            sublistN.append(char2[index+subIndex])
                            subIndex += 1
                        else:
                            remainConst = False
                    else:
                        remainConst = False
                if len(sublistP) > 1:
                    oplistP.pop()
                    oplistN.pop()
                    num = ''
                    subIndex2 = 0
                    for const in sublistP:
                        num += str(sublistN[subIndex2])
                        subIndex2 += 1
                    oplistP.append('const')
                    oplistN.append(num)
                index += (subIndex - 1)
                subIndex = 0
        index += 1
        sublistN = []
        sublistP = []
    print('oplistP:', oplistP)
    print('oplistN:', oplistN)
    index = 0
    addend = 0
    subIndex = 0
    oplistP2 = []
    oplistN2 = []
    print('Length:', len(oplistP))
    while index < len(oplistP):
        print(index)
        sep = oplistP[index]
        print('Sep:', sep)
        if sep == 'const':
            print('Const')
            if index+1 < len(oplistP):
                if oplistP[index+1] == 'var':
                    oplistP2.append('const*var')
                    addend = str(oplistN[index]) + '*' + str(oplistN[index+1])
                    oplistN2.append(addend)
                    index += 1
                elif index+2 < len(oplistP):
                    if oplistP[index+1] == '+' or \
                            oplistP[index+1] == '-' or \
                            oplistP[index+1] == '*' or \
                            oplistP[index+1] == '/':
                        addend = 'const' + oplistP[index+1] + oplistP[index+2]
                        oplistP2.append(addend)
                        addend = oplistN[index] + oplistN[index+1] + oplistN[index+2]
                        oplistN2.append(addend)
                        index += 2
                        print('Index:', index)
                        if index+1 == len(oplistP):
                            index += 1
                else:
                    oplistP2.append(oplistP[index])
                    oplistN2.append(oplistN[index])
                    index += 1
            else:
                oplistP2.append(oplistP[index])
                oplistN2.append(oplistN[index])
                index += 1
        elif sep == 'var':
            print('Var')
            if index+1 < len(oplistP):
                if oplistP[index+1] == '+' or \
                        oplistP[index+1] == '-' or \
                        oplistP[index+1] == '*' or \
                        oplistP[index+1] == '/':
                    addend = 'var' + oplistP[index+1] + oplistP[index+2]
                    oplistP2.append(addend)
                    addend = oplistN[index] + oplistN[index+1] + oplistN[index+2]
                    oplistN2.append(addend)
                    index += 2
                    if index+1 == len(oplistP):
                        index += 1
                else:
                    oplistP2.append(oplistP[index])
                    oplistN2.append(oplistN[index])
                    index += 1
            else:
                oplistP2.append(oplistP[index])
                oplistN2.append(oplistN[index])
                index += 1
        elif sep != 'const' and sep != 'var':
            print('Neither')
            if index+1 < len(oplistP):
                if oplistP[index+1] != 'const' and oplistP[index+1] != 'var':
                    oplistP2.append(oplistP[index])
                    oplistN2.append(oplistN[index])
            index += 1
        else:
            index += 1
        print('oplistN2:', oplistN2)
        print('oplistP2:', oplistP2)
    print(oplistP, oplistP2)
    print(oplistN, oplistN2)
    print('parsed:', parsed)
    if len(oplistP2) == 1:
        if t == 1:
            onesym += 1
        else:
            onesym += 2
    return oplistP2, oplistN2, onesym

def op(a):
    ops = []
    scores = []
    index = 1000
    for op in a:
        score = 0
        for i in op:
            if i == '+' or i == '*' or i == '/' or i == '-':
                sym = i
        ops.append(sym)
        if sym == '+' or sym == '-':
            score = index+1000
            scores.append(score)
        elif sym == '*' or sym == '/':
            score = index+2000
            scores.append(score)
        index -= 1
    print(ops, scores)
    return ops, scores

def recombine(c, p):
    index = 0
    halt = False
    equation = ''
    for i in c:
        opPassed = False
        if index == len(c)-1:
            if '+' in c[0] or '-' in c[0] or '/' in c[0] or '*' in c[0]:
                pass
            else:
                equation += i
                halt = True
        if not halt:
            for char in i:
                if char == '+' or char == '-' or char == '/' or char == '*':
                    if char == '*':
                        if 'var' in p[index]:
                            if p1[index][1] != 'v':
                                pass
                            else:
                                equation += char
                        else:
                            equation += char
                    else:
                        equation += char
                    opPassed = True
                else:
                    if not opPassed or len(c) == index+1:
                        if char != '1':
                            equation += char
                        elif '*' in p[index]:
                            if 'var' in p[index]:
                                if p[index][1] != 'v':
                                    pass
                                else:
                                    equation += char
                            else:
                                equation += char
                        else:
                            equation += char
        index += 1
    return(equation)

def solveTilVar(p, c, o, s):
    sb = s
    sortedScore = []
    hsl = []
    print(sb)
    for i in sb:
        hs = 0
        index = 0
        indexS = 0
        for score in sb:
            if score > hs and score not in hsl:
                hs = score
                indexS = index
            index += 1
        hsl.append(hs)
        sortedScore.append((hs, indexS))
    print(sortedScore)
    cont = []
    rl = []
    indexSS = 0
    d1 = -10
    d2 = -10
    breakBool = False
    vAdjustment = 0
    limit = len(p)
    iterations = 0
    indexSave = 727000
    addSubOnly = False
    stepsSTV = []
    for i in sortedScore:
        if i[0] > 2000 and 'var' not in p[i[1]]:
            addSubOnly = True
            break
    while indexSS < len(sortedScore):
        step = []
        prev_len = len(p)
        if addSubOnly == True:
            if indexSave != 727000:
                ss = sortedScore[indexSave+1]
            else:
                ss = sortedScore[indexSS]
        else:
            ss = sortedScore[indexSS]
        indexSave = indexSS
        v = ss[1] - vAdjustment
        print(p, c, o, s, ss)
        print(sortedScore)
        print('indexSS', indexSS, vAdjustment)
        iterations += 1
        if len(p) >= indexSS:
            print(v)
            if 'var' not in p[v]:
                step = []
                step.append('solveTilVar')
                if p == pc1:
                    step.append(copy.deepcopy(c))
                    step.append(copy.deepcopy(p))
                    step.append(copy.deepcopy(cc2))
                    step.append(copy.deepcopy(pc2))
                if p == pc2:
                    step.append(copy.deepcopy(c))
                    step.append(copy.deepcopy(p))
                    step.append(copy.deepcopy(cc1))
                    step.append(copy.deepcopy(pc1))
                print('Step Part 1:', step)
                lastchar = True
                print(v)
                toDo = c[v]
                opPassed = False
                a1 = ''
                a2 = ''
                op = ''
                for char in toDo:
                    if char != '+' and char != '-' and char != '*' and char != '/':
                        if not opPassed:
                            a1 += str(char)
                        else:
                            a2 += str(char)
                    else:
                        opPassed = True
                        op = char
                if indexSS == d1:
                    a1 = rl
                elif indexSS == d2:
                    a2 = rl
                print('test')
                print(toDo, char, a1, a2)
                print('a1:', a1, 'a2:', a2, 'op:', op)
                if op == '+':
                    result = float(a1)+float(a2)
                    step.insert(0, '+')
                elif op == '-':
                    result = float(a1)-float(a2)
                    step.insert(0, '-')
                elif op == '*':
                    result = float(a1)*float(a2)
                    step.insert(0, '*')
                elif op == '/':
                    result = float(a1)/float(a2)
                    step.insert(0, '/')
                print('Step Part 2:', step)
                rl = result
                d1 = indexSS+1
                d2 = indexSS-1
                indexSS += 1
                print('indexSS', indexSS)

                v += 1
                if v > indexSS:
                    vAdjustment += 1
                print(v)
                
                if v < len(p):
                    last_char = False
                    print('pass')
                    p.pop(v)
                    ch1 = c[v]
                    opPass = False
                    ch1s = ''
                    ch1u = ''
                    ch1o = ''
                    for char in ch1:
                        if char == '+' or char == '-' or char == '*' or char == '/':
                            opPass = True
                            ch1o = char
                        elif opPass == True:
                            ch1s += char
                        else:
                            ch1u += char
                    print(c[v])
                    c.pop(v)
                    print('ch1', c)
                    ch1i = str(rl) + ch1o + ch1s
                    c.insert(v, ch1i)
                    print('ch1', c, ch1i)

                ch2 = c[v-2]
                print(ch2)
                opPass = False
                ch2s = ''
                ch2u = ''
                ch2o = ''
                for char in ch2:
                    print('asd', char)
                    if char == '+' or char == '-' or char == '*' or char == '/':
                        opPass = True
                        ch2o = char
                        print('fgh')
                    elif opPass == False:
                        ch2s += char
                    else:
                        ch2u += char
                c.pop(v-2)
                print('ch2', c)
                ch2i = ch2s + ch2o + str(rl)
                c.insert(v-2, ch2i)
                print(ch2u, 'a', ch2o, 'b', str(rl))
                print('ch2', c, ch2i)

                print('h')
                c.pop(v-1)
                # if lastchar == True:
                indexSS -= 1
                print(indexSS)
                # replace the operation with the result in n and p, for
                # a1 in n[index+1][index of the right side], 'const' in p[index+1][iols] and 
                # a2 in n[index-1][index of the left side], 'const' in p[index+1][iors]
                # do this by detecting the index in this loop
                if p == pc1:
                    step.append(copy.deepcopy(c))
                    step.append(copy.deepcopy(p))
                    step.append(copy.deepcopy(cc2))
                    step.append(copy.deepcopy(pc2))
                if p == pc2:
                    step.append(copy.deepcopy(c))
                    step.append(copy.deepcopy(p))
                    step.append(copy.deepcopy(cc1))
                    step.append(copy.deepcopy(pc1))
                print('Step Part 3:', step)
                stepsSTV.append(copy.deepcopy(step))
                print('Updated Steps:', stepsSTV)
                if len(p) == prev_len:
                    p.pop(v-1)
                    if len(p) <= 2:
                        breakBool = True
            else:
                print('b')
                # cont.append(c[ss[1]])
                indexSS += 1
        else:
            print('a')
            indexSS += 1
        if breakBool == True:
            print(f"\033[1mcond1!\033[0m")
            break
        if iterations > limit + 1:
            print(f"\033[1mcond2!\033[0m")
            break
    print(rl, p, c)
    return p, c, o, s, stepsSTV

    # check s for highest score 
    # make a new tuple list of (score, index) when doing this.
    # check if that score is related to a variable
    # if yes, skip and find next highest
    # if no, then calculate that

def solve(p1, c1, o1, s1, p2, c2, o2, s2):
    stepsSolve = []
    # find the constant related to the variables
    opl1 = []
    sub = ()
    index = 0
    scoreIndex = 1000
    for i in p1:
        if 'var' in i:
            for char in i:
                if char == '+' or char == '-' or char == '*' or char == '/':
                    sub = (char, index)
                    opl1.append(sub)
        index += 1
    opl2 = []
    index = 0
    for i in p2:
        if 'var' in i:
            for char in i:
                if char == '+' or char == '-' or char == '*' or char == '/':
                    sub = (char, index)
                    opl2.append(sub)
        index += 1
    # indp1/indp2 is everything in p separated.
    indp1 = []
    current = ''
    for i in p1:
        if i != '+' and i != '-' and i != '*' and i != '/':
            current += i
        else:
            indp1.append(current)
            current = ''
    indp2 = []
    current = ''
    for i in p2:
        if i != '+' and i != '-' and i != '*' and i != '/':
            current += i
        else:
            indp2.append(current)
            current = ''
    sortIndex = 0
    print('process0', opl1, opl2, sortIndex)
    for i in opl1:
        print('process1', c1, c2, p1, p2)
        if i[0] == '*' or i[0] == '/':
            print('process2')
            if len(opl1) >= sortIndex+2:
                print('process3')
                if opl1[sortIndex+1][0] == '+' or opl1[sortIndex+1][0] == '-':
                    print('process4')
                    save = i
                    opl1.pop(sortIndex)
                    opl1.append(save)
                    break
        sortIndex += 1
    sortIndex = 0
    for i in opl2:
        if i[0] == '*' or i[0] == '/':
            if len(opl2) >= sortIndex+2:
                if opl2[sortIndex+1][0] == '+' or opl2[sortIndex+1][0] == '-':
                    save = i
                    opl2.pop(sortIndex)
                    opl2.append(save)
                    break
        sortIndex += 1
    print('opl', opl1, opl2)
    for i in opl1:
        step = []
        print('iteration1', i[0], indp2)
        i0 = i[0]
        step.append(copy.deepcopy(i0))
        step.append('solve')
        step.append(copy.deepcopy(c1))
        step.append(copy.deepcopy(p1))
        step.append(copy.deepcopy(c2))
        step.append(copy.deepcopy(p2))
        print('Step Part 1:', step)
        if i[0] == '+' or i[0] == '-' and 'const' in indp2:
            opSolve = i[0]
            opPassed = False
            constA = ''
            if p1[i[1]][0] != 'v':
                for char in c1[i[1]]:
                    if not opPassed:
                        constA += str(char)
                    elif char == '+' or char == '-':
                        opPassed = True
            if p1[i[1]][0] == 'v':
                for char in c1[i[1]]:
                    if opPassed:
                        constA += str(char)
                    elif char == '+' or char == '-':
                        opPassed = True
            for j in opl2:
                if j[0] == '+' or j[0] == '-':
                    opPassed = False
                    constB = ''
                    popIndex = 0
                    ind = 0
                    popLen = 0
                    if p2[j[1]][0] != 'v':
                        for char in c2[j[1]]:
                            if not opPassed:
                                constB += str(char)
                                popLen += 1
                            elif char == '+' or char == '-':
                                opPassed = True
                    if p2[j[1]][0] == 'v':
                        for char in c2[j[1]]:
                            if opPassed:
                                constB += str(char)
                                popLen += 1
                            elif char == '+' or char == '-':
                                opPassed = True
                                popIndex = ind
                            ind += 1
                    jVal = j[1]
            if len(opl2) == 0:
                constB = c2[0]
                popIndex = 1
                popLen = len(c2[0])
                jVal = 0
            if opSolve == '+':
                constR = float(constB)-float(constA)
            elif opSolve == '-':
                constR = float(constB)+float(constA)
            if popIndex == 0:
                c2[jVal] = c2[jVal][popLen:]
            else:
                c2[jVal] = c2[jVal][:-popLen]
            if popIndex == 0:
                c2[jVal] = str(constR) + c2[jVal]
            else:
                c2[jVal] += str(constR)
            c1.pop(i[1])
            p1.pop(i[1])
        if i[0] == '*':
            print('*')
            jList = []
            opSolve = i[0]
            opPassed = False
            constA = ''
            if p1[i[1]][0] != 'v':
                for char in c1[i[1]]:
                    if char == '*':
                        opPassed = True
                    elif not opPassed:
                        constA += str(char)
                    print('char1: ', char, opPassed)
            if p1[i[1]][0] == 'v':
                for char in c1[i[1]]:
                    if char == '*':
                        opPassed = True
                    elif opPassed:
                        constA += str(char)
                    print('char2: ', char, opPassed)
            for j in opl2:
                opPassed = False
                constB = ''
                popIndex = 0
                ind = 0
                popLen = 0
                if p2[j[1]][0] != 'v':
                    for char in c2[j[1]]:
                        if not opPassed:
                            constB += str(char)
                            popLen += 1
                        elif char == '+' or char == '-' or char == '*' or char == '/':
                            opPassed = True
                if p2[j[1]][0] == 'v':
                    for char in c2[j[1]]:
                        if opPassed:
                            constB += str(char)
                            popLen += 1
                        elif char == '+' or char == '-' or char == '*' or char == '/':
                            opPassed = True
                            popIndex = ind
                        ind += 1
                jVal = j[1]
                jList.append((constB, popLen, popIndex, jVal))
            if len(jList) == 0:
                print('c2:', c2)
                constB = c2[0]
                popIndex = 1
                popLen = len(c2[0])
                jVal = 0
                jList.append((constB, popLen, popIndex, jVal))
            print(jList)
            for k in jList:
                constR = float(k[0])/float(constA)
                if k[2] == 0:
                    c2[k[3]] = c2[k[3]][k[1]:]
                else:
                    c2[k[3]] = c2[k[3]][:-k[1]]
                if k[2] == 0:
                    c2[k[3]] = str(constR) + c2[k[3]]
                else:
                    c2[k[3]] += str(constR)
            var = False
            if 'var' in p1[i[1]]:
                var = True
            c1.pop(i[1])
            if not var:
                c1.insert(i[1], '1')
            else:
                insert = '1*' + variable
                print('insert', insert)
                c1.insert(i[1], insert)
            var = False
            if 'var' in p1[i[1]]:
                var = True
            p1.pop(i[1])
            if not var:
                p1.insert(i[1], 'const')
            else:
                p1.insert(i[1], 'const*var')

        if i[0] == '/':
            print('/')
            jList = []
            opSolve = i[0]
            opPassed = False
            constA = ''
            if p1[i[1]][0] != 'v':
                for char in c1[i[1]]:
                    if char == '/':
                        opPassed = True
                    elif not opPassed:
                        constA += str(char)
                    print('char1: ', char, opPassed)
            if p1[i[1]][0] == 'v':
                for char in c1[i[1]]:
                    if char == '/':
                        opPassed = True
                    elif opPassed:
                        constA += str(char)
                    print('char2: ', char, opPassed)
            for j in opl2:
                opPassed = False
                constB = ''
                popIndex = 0
                ind = 0
                popLen = 0
                if p2[j[1]][0] != 'v':
                    for char in c2[j[1]]:
                        if not opPassed:
                            constB += str(char)
                            popLen += 1
                        elif char == '+' or char == '-' or char == '*' or char == '/':
                            opPassed = True
                if p2[j[1]][0] == 'v':
                    for char in c2[j[1]]:
                        if opPassed:
                            constB += str(char)
                            popLen += 1
                        elif char == '+' or char == '-' or char == '*' or char == '/':
                            opPassed = True
                            popIndex = ind
                        ind += 1
                jVal = j[1]
                jList.append((constB, popLen, popIndex, jVal))
            if len(jList) == 0:
                print('c2:', c2)
                constB = c2[0]
                popIndex = 1
                popLen = len(c2[0])
                jVal = 0
                jList.append((constB, popLen, popIndex, jVal))
            print(jList)
            for k in jList:
                constR = float(k[0])*float(constA)
                if k[2] == 0:
                    c2[k[3]] = c2[k[3]][k[1]:]
                else:
                    c2[k[3]] = c2[k[3]][:-k[1]]
                if k[2] == 0:
                    c2[k[3]] = str(constR) + c2[k[3]]
                else:
                    c2[k[3]] += str(constR)
            var = False
            if 'var' in p1[i[1]]:
                var = True
            c1.pop(i[1])
            if not var:
                c1.insert(i[1], '1')
            else:
                insert = '1*' + variable
                print('insert', insert)
                c1.insert(i[1], insert)
            var = False
            if 'var' in p1[i[1]]:
                var = True
            p1.pop(i[1])
            if not var:
                p1.insert(i[1], 'const')
            else:
                p1.insert(i[1], 'const*var')
        step.append(copy.deepcopy(c1))
        step.append(copy.deepcopy(p1))
        step.append(copy.deepcopy(c2))
        step.append(copy.deepcopy(p2))
        print('Step Part 2:', step)
        stepsSolve.append(copy.deepcopy(step))
        print('Updated Step:', stepsSolve)
# ==========================================================================
# opl2
    for i in opl2:
        step = []
        i0 = i[0]
        step.append(copy.deepcopy(i0))
        step.append('solve')
        step.append(copy.deepcopy(c1))
        step.append(copy.deepcopy(p1))
        step.append(copy.deepcopy(c2))
        step.append(copy.deepcopy(p2))
        print('Step Part 1:', step)
        print('iteration2', i[0], indp1)
        if i[0] == '+' or i[0] == '-' and 'const' in indp1:
            opSolve = i[0]
            opPassed = False
            constA = ''
            if p2[i[1]][0] != 'v':
                for char in c2[i[1]]:
                    if not opPassed:
                        constA += str(char)
                    elif char == '+' or char == '-':
                        opPassed = True
            if p2[i[1]][0] == 'v':
                for char in c2[i[1]]:
                    if opPassed:
                        constA += str(char)
                    elif char == '+' or char == '-':
                        opPassed = True
            print('opl Check', opl1, opl2)
            for j in opl1:
                if j[0] == '+' or j[0] == '-':
                    opPassed = False
                    constB = ''
                    popIndex = 0
                    ind = 0
                    popLen = 0
                    if p1[j[1]][0] != 'v':
                        for char in c1[j[1]]:
                            if not opPassed:
                                constB += str(char)
                                popLen += 1
                            elif char == '+' or char == '-':
                                opPassed = True
                    if p1[j[1]][0] == 'v':
                        for char in c1[j[1]]:
                            if opPassed:
                                constB += str(char)
                                popLen += 1
                            elif char == '+' or char == '-':
                                opPassed = True
                                popIndex = ind
                            ind += 1
                    jVal = j[1]
            if len(opl1) == 0:
                constB = c1[0]
                popIndex = 1
                popLen = len(c1[0])
                jVal = 0
            if opSolve == '+':
                constR = float(constB)-float(constA)
            elif opSolve == '-':
                constR = float(constB)+float(constA)
            if popIndex == 0:
                c1[jVal] = c1[jVal][popLen:]
            else:
                c1[jVal] = c1[jVal][:-popLen]
            if popIndex == 0:
                c1[jVal] = str(constR) + c1[jVal]
            else:
                c1[jVal] += str(constR)
            c2.pop(i[1])
            p2.pop(i[1])
        if i[0] == '*':
            print('*')
            jList = []
            opSolve = i[0]
            opPassed = False
            constA = ''
            if p2[i[1]][0] != 'v':
                for char in c2[i[1]]:
                    if char == '*':
                        opPassed = True
                    elif not opPassed:
                        constA += str(char)
                    print('char1: ', char, opPassed)
            if p2[i[1]][0] == 'v':
                for char in c2[i[1]]:
                    if char == '*':
                        opPassed = True
                    elif opPassed:
                        constA += str(char)
                    print('char2: ', char, opPassed)
            print('opl Check', opl1, opl2)
            for j in opl1:
                opPassed = False
                constB = ''
                popIndex = 0
                ind = 0
                popLen = 0
                if p1[j[1]][0] != 'v':
                    for char in c1[j[1]]:
                        if not opPassed:
                            constB += str(char)
                            popLen += 1
                        elif char == '+' or char == '-' or char == '*' or char == '/':
                            opPassed = True
                if p1[j[1]][0] == 'v':
                    for char in c1[j[1]]:
                        if opPassed:
                            constB += str(char)
                            popLen += 1
                        elif char == '+' or char == '-' or char == '*' or char == '/':
                            opPassed = True
                            popIndex = ind
                        ind += 1
                jVal = j[1]
                print('jList check', constB, popLen, popIndex, jVal)
                jList.append((constB, popLen, popIndex, jVal))
            if len(jList) == 0:
                constB = c2[0]
                popIndex = 1
                popLen = len(c1[0])
                jVal = 0
                jList.append((constB, popLen, popIndex, jVal))
            for k in jList:
                constR = float(k[0])/float(constA)
                if k[2] == 0:
                    c1[k[3]] = c1[k[3]][k[1]:]
                else:
                    c1[k[3]] = c1[k[3]][:-k[1]]
                if k[2] == 0:
                    c1[k[3]] = str(constR) + c1[k[3]]
                else:
                    c1[k[3]] += str(constR)
            var = False
            if 'var' in p2[i[1]]:
                var = True
            c1.pop(i[1])
            if not var:
                c2.insert(i[1], '1')
            else:
                insert = '1*' + variable
                c2.insert(i[1], insert)
            var = False
            if 'var' in p2[i[1]]:
                var = True
            p2.pop(i[1])
            if not var:
                p2.insert(i[1], 'const')
            else:
                p2.insert(i[1], 'const*var')

        if i[0] == '/':
            print('/')
            jList = []
            opSolve = i[0]
            opPassed = False
            constA = ''
            if p2[i[1]][0] != 'v':
                for char in c2[i[1]]:
                    if char == '/':
                        opPassed = True
                    elif not opPassed:
                        constA += str(char)
                    print('char1: ', char, opPassed)
            if p2[i[1]][0] == 'v':
                for char in c2[i[1]]:
                    if char == '/':
                        opPassed = True
                    elif opPassed:
                        constA += str(char)
                    print('char2: ', char, opPassed)
            print('opl Check', opl1, opl2)
            for j in opl1:
                opPassed = False
                constB = ''
                popIndex = 0
                ind = 0
                popLen = 0
                if p1[j[1]][0] != 'v':
                    for char in c1[j[1]]:
                        if not opPassed:
                            constB += str(char)
                            popLen += 1
                        elif char == '+' or char == '-' or char == '*' or char == '/':
                            opPassed = True
                if p1[j[1]][0] == 'v':
                    for char in c1[j[1]]:
                        if opPassed:
                            constB += str(char)
                            popLen += 1
                        elif char == '+' or char == '-' or char == '*' or char == '/':
                            opPassed = True
                            popIndex = ind
                        ind += 1
                jVal = j[1]
                print('jList check', constB, popLen, popIndex, jVal)
                jList.append((constB, popLen, popIndex, jVal))
            if len(jList) == 0:
                constB = c2[0]
                popIndex = 1
                popLen = len(c1[0])
                jVal = 0
                jList.append((constB, popLen, popIndex, jVal))
            for k in jList:
                constR = float(k[0])*float(constA)
                if k[2] == 0:
                    c1[k[3]] = c1[k[3]][k[1]:]
                else:
                    c1[k[3]] = c1[k[3]][:-k[1]]
                if k[2] == 0:
                    c1[k[3]] = str(constR) + c1[k[3]]
                else:
                    c1[k[3]] += str(constR)
            var = False
            if 'var' in p2[i[1]]:
                var = True
            c1.pop(i[1])
            if not var:
                c2.insert(i[1], '1')
            else:
                insert = '1*' + variable
                c2.insert(i[1], insert)
            var = False
            if 'var' in p2[i[1]]:
                var = True
            p2.pop(i[1])
            if not var:
                p2.insert(i[1], 'const')
            else:
                p2.insert(i[1], 'const*var')
        step.append(copy.deepcopy(c1))
        step.append(copy.deepcopy(p1))
        step.append(copy.deepcopy(c2))
        step.append(copy.deepcopy(p2))
        print('Step Part 2:', step)
        stepsSolve.append(copy.deepcopy(step))
        print('Updated Step:', stepsSolve)
    print('haj', p1, c1, p2, c2)
    return p1, c1, p2, c2, stepsSolve




    
    # if * or /, then do that to the coefficient of the variables (***const*** * var)
    # if + or -, then reverse the operation to the other side, unless:
    # other side does not have a constant
    # if const on only one side and variables on two sides, subtract coefficient
    # of one to the other.
    # make sure it ends up in from const = coef*var
    # const/coef = var.
    
pygame.init()

# window set-up
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Algebra Calculator")
# Edit this before publishing
try:
    icon = pygame.image.load(os.path.join(base, 'Algebra Calculator Icon.png'))
    pygame.display.set_icon(icon)
except FileNotFoundError:
    print('\033[1;31mERROR! Icon File not found.')

# Font for Pygame
font = pygame.font.Font(fontF, 26)
fontSmall = pygame.font.Font(fontF, 15)
fontBold = pygame.font.Font(fontBoldF, 30)
fontTitle = pygame.font.Font(fontBoldF, 60)
fontSubtitle = pygame.font.Font(fontBoldF, 42)
fontLarge = pygame.font.Font(fontF, 36)

# Title
titleS = fontTitle.render('Algebra Calculator', True, col5)
title = titleS.get_rect(topleft=(25, 0))

# Input Text Subtitle
subtitleS = fontSubtitle.render('Input your equation below:', True, col5)
subtitle = subtitleS.get_rect(topleft=(25, 80))

# Keybind Indicators
backspaceS = fontSmall.render('<< Press BACKSPACE to go back', True, col5)
backspace = backspaceS.get_rect(bottomleft=(15, 692))
enterS = fontSmall.render('Press ENTER to continue >>', True, col5)
enter = enterS.get_rect(bottomright=(1090, 692))

# Equation (Inputted by User)
current_equation = ''

input_screen = True
calc_done = False
onesym1 = False
onesym2 = False

stepIndex = 0

run = True
while run:
    equationTS = font.render(current_equation, True, col5)
    equationT = equationTS.get_rect(topleft=(25, 140))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if input_screen == True:
                    current_equation = current_equation[:-1]
                elif input_screen == False and stepIndex != 0:
                    stepIndex -= 1
                elif input_screen == False and stepIndex == 0:
                    stepIndex = 0
                    steps = []
                    input_screen = True
                    calc_done = False
            elif event.key == pygame.K_RETURN:
                if input_screen == True:
                    to_parse = current_equation
                    input_screen = False
                elif input_screen == False and stepIndex != len(steps)-1:
                    stepIndex += 1
                    printReset = False
                elif input_screen == False and stepIndex == len(steps)-1:
                    input_screen = True
                    steps = []
                    stepIndex = 0
                    calc_done = False
            else:
                current_letter = event.unicode
                current_equation += current_letter
    if input_screen == False and calc_done == False:
        charList = [*current_equation]
        print(charList)
        parsed1, parsed2 = parse(charList)
        char1, char2 = separate(charList)
        pc1, cc1, onesym = combine(parsed1, 1, onesym)
        pc2, cc2, onesym = combine(parsed2, 2, onesym)
        pc2debug = pc2
        cc2debug = cc2
        op1 = []
        op2 = []
        os1 = []
        os2 = []
        if onesym == 1 or onesym == 3:
            onesym1 = True
        if onesym1 != True:
            op1, os1 = op(pc1)
            print('check:', pc1, cc1)
            pc1, cc1, op1, os1, steps1 = solveTilVar(pc1, cc1, op1, os1)
            print('steps1', steps1)
            for step in steps1:
                print(step)
                steps.append(step)
            op1, os1 = op(pc1)
        print(pc2, cc2, onesym)
        if onesym == 2 or onesym == 3:
            onesym2 = True
        if onesym2 != True:
            op2, os2 = op(pc2)
            pc2, cc2, op2, os2, steps2 = solveTilVar(pc2, cc2, op2, os2)
            for step in steps2:
                steps.append(step)
            op2, os2 = op(pc2)
        print('PC2:', pc2debug)
        print('CC2:', cc2debug)
        print('pc1:', pc1)
        print('cc1:', cc1)
        print('pc2:', pc2)
        print('cc2:', cc2)
        p1, c1, p2, c2, steps3 = solve(pc1, cc1, op1, os1, pc2, cc2, op2, os2)
        for step in steps3:
            steps.append(step)
        print('Steps:', steps)
        print(p1, c1, p2, c2)
        e1 = recombine(c1, p1)
        e2 = recombine(c2, p2)
        print('Equations', e1, e2)
        if e1 == variable:
            finalEquation = e1 + '=' + e2
        else:
            finalEquation = e2 + '=' + e1
        print('Final Equation:', finalEquation)
        eq = copy.deepcopy(current_equation)
        stepIndex = 0
        calc_done = True
        printReset = False

    if input_screen == False and calc_done == True:
        # on screen, we need equation (top, small, pink), step # (bold, top, medium, white)
        # instruction (mid-high, medium, white), old equation (middle, large, white)
        # new equation (bold, mid-low, large, white - highlighted at changes)
        if printReset == False:
            print('StepIndex:', stepIndex)
            printReset = True
        inputtedT = 'Input: ' + eq
        inputtedS = fontSmall.render(inputtedT, True, col4)
        inputted = inputtedS.get_rect(topleft=(15, 10))
        
        stepNum = 'Step ' + str((stepIndex+1)) + ':'
        stepS = fontSubtitle.render(stepNum, True, col5)
        step = stepS.get_rect(topleft=(15, 24))

        # figure out the explanation for the step
        if steps[stepIndex][1] == 'solveTilVar':
            if steps[stepIndex][0] == '+':
                explanation = 'Add two constants together to simplify the equation.'
            if steps[stepIndex][0] == '-':
                explanation = 'Subtract two constants from one another to simplify the equation.'
            if steps[stepIndex][0] == '*':
                explanation = 'Multiply two constants together to simplify the equation.'
            if steps[stepIndex][0] == '/':
                explanation = 'Divide two constants from one another to simplify the equation.'
        elif steps[stepIndex][1] == 'solve':
            if steps[stepIndex][0] == '+':
                explanation = 'Use the subtraction property of equality.'
            if steps[stepIndex][0] == '-':
                explanation = 'Use the addition property of equality.'
            if steps[stepIndex][0] == '*':
                explanation = 'Use the division property of equality.'
            if steps[stepIndex][0] == '/':
                explanation = 'Use the multiplication property of equality.'        
        explanationTS = font.render(explanation, True, col5)
        explanationT = explanationTS.get_rect(topleft=(15, 75))

        stepE = steps[stepIndex]
        oldEquation1 = recombine(stepE[2], stepE[3])
        oldEquation2 = recombine(stepE[4], stepE[5])
        oldEquation = oldEquation1 + '=' + oldEquation2
        oldEquationTS = fontLarge.render(oldEquation, True, col5)
        oldEquationT = explanationTS.get_rect(topleft=(15, 125))

        newEquation1 = recombine(stepE[6], stepE[7])
        newEquation2 = recombine(stepE[8], stepE[9])
        newEquation = newEquation1 + '=' + newEquation2
        if len(steps)-1 == stepIndex:
            newEquationTS = fontSubtitle.render(newEquation, True, col6)
        else:
            newEquationTS = fontSubtitle.render(newEquation, True, col5)
        newEquationT = explanationTS.get_rect(topleft=(15, 170))
        # for step in steps, use recombine to get new/old equations.
        # check each character until there's a difference.
        # length of difference is old-new.
        # look at operation and step name to get instruction.
            
    screen.fill(col1)
    if input_screen == False:
        screen.blit(inputtedS, inputted)
        screen.blit(stepS, step)
        screen.blit(explanationTS, explanationT)
        screen.blit(oldEquationTS, oldEquationT)
        screen.blit(newEquationTS, newEquationT)
    if input_screen == True:
        screen.blit(titleS, title)
        screen.blit(subtitleS, subtitle)
        screen.blit(equationTS, equationT)
    screen.blit(backspaceS, backspace)
    screen.blit(enterS, enter)
    pygame.display.flip()

pygame.quit()