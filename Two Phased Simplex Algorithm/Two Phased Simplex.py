##### Two Phased Simplex Method Written in Python3 #####
##### As a Term Project For LinearOptimization Course #####


def SetUpTables(c, eqs, b):
    tables = []
    m = len(eqs)
    n = len(c)
    c.insert(0, 0.0)
    artificial = []
    sigma = [0.0]
    i = 0
    while (i < n):
        sigma.append(0.0)
        i += 1
    i = 0
    while (i < m):
        artificial.append(0.0)
        sigma.append(1.0)
        i += 1
    c.extend(artificial)
    tables.append(c)
    tables.append(sigma)
    i = 0
    for eq in eqs:
        eq.insert(0, b[i])
        eq.extend(artificial)
        eq[n + 1 + i] = 1.0
        tables.append(eq)
        i += 1
    i = 0
    for xi in tables:
        if (i > 1):
            j = 0
            for xij in xi:
                tables[1][j] -= xij
                j += 1
        i += 1
    return tables





def PivotDivider(tables, row, col):
    j = 0
    pivot = tables[row][col]
    for x in tables[row]:
        tables[row][j] = tables[row][j] / pivot
        j += 1
    i = 0
    for xi in tables:
        if i != row:
            ratio = xi[col]
            j = 0
            for xij in xi:
                xij -= ratio * tables[row][j]
                tables[i][j] = xij
                j += 1
        i += 1
    return tables






def Phase1(tables):
    THETA_INFINITE = -1
    opt = False
    unbounded = False
    n = len(tables[0])
    m = len(tables) - 2

    while ((not opt) and (not unbounded)):
        min = 0.0
        pivotCol = j = 1
        while (j < (n - m)):
            cj = tables[1][j]
            if (cj < min):
                min = cj
                pivotCol = j
            j += 1
        if min == 0.0:
            opt = True
            continue
        pivotRow = i = 0
        minTheta = THETA_INFINITE
        for xi in tables:
            if (i > 1):
                xij = xi[pivotCol]
                if xij > 0:
                    theta = (xi[0] / xij)
                    if (theta < minTheta) or (minTheta == THETA_INFINITE):
                        minTheta = theta
                        pivotRow = i
            i += 1
        if minTheta == THETA_INFINITE:
            unbounded = True
            continue
        tables = PivotDivider(tables, pivotRow, pivotCol)
    return tables






def RemoveRs(tables):
    n = len(tables[0])
    j = n - 1
    isbasis = True
    while (j > 0):
        found = False
        i = -1
        row = 0
        for xi in tables:
            i += 1
            if (xi[j] == 1):
                if (found):
                    isbasis = False
                    continue
                elif (i > 1):
                    row = i
                    found = True
            elif (xi[0] != 0):
                isbasis = False
                continue
        if (isbasis and found):
            if (j >= n):
                tables = PivotDivider(tables, row, j)
            else:
                return tables
        j -= 1
    return tables







def Phase2(tables):
    THETA_INFINITE = -1
    opt = False
    unbounded = False
    n = len(tables[0])
    m = len(tables) - 1

    while ((not opt) and (not unbounded)):
        min = 0.0
        pivotCol = j = 0
        while (j < (n - m)):
            cj = tables[0][j]
            if (cj < min) and (j > 0):
                min = cj
                pivotCol = j
            j += 1
        if min == 0.0:
            opt = True
            continue
        pivotRow = i = 0
        minTheta = THETA_INFINITE
        for xi in tables:
            if (i > 0):
                xij = xi[pivotCol]
                if xij > 0:
                    theta = (xi[0] / xij)
                    if (theta < minTheta) or (minTheta == THETA_INFINITE):
                        minTheta = theta
                        pivotRow = i
            i += 1
        if minTheta == THETA_INFINITE:
            unbounded = True
            continue
        tableu = PivotDivider(tables, pivotRow, pivotCol)
    return tables







def TwoPhasedSimplex(tables):
    infeasible = False
    tables = Phase1(tables)
    sigma = tables[1][0]
    if (sigma > 0):
        infeasible = True
        print('infeasible')
    else:
        # sigma is equals to zero
        tables = RemoveRs(tables)
        m = len(tables) - 2
        n = len(tables[0])
        n -= m
        tables.pop(1)
        i = 0
        while (i < len(tables)):
            tables[i] = tables[i][:n]
            i += 1
        tables = Phase2(tables)
    return tables






def PrintTables(tables):
    print('--------------------------------------------------')
    for row in tables:
        print(row)
    print('--------------------------------------------------')
    return






print("\n________________________________________________________________________\n")
print("Press 1 to see a pre defined problem which is as follow :\n\n\t Max(Z) = x1 + x2 + x3 + x4 + x5 \n\t\t  3*x1 + 2*x2 + x3 >= 1 \n\t\t  5*x1 + x2 + x3 + x4 >= 3 \n\t\t  2*x1 + 5*x2 + x3 + x5 >= 4 ")
print("\nPress 2 to define your own problem")
choice = int(input(" >> "))
print("\n________________________________________________________________________\n")



if(choice == 2) :
    print("Please Enter the coefficients of the objective function Z (with spaces, such as 1.0 2.9 ...):") 
    c = list(map(int, input().split(" ")))
    print("\n________________________________________________________________________\n")
    print("Please enter the number of your constraints:")
    constraints = int(input(" >> "))
    print("________________________________________________________________________")
    print("Please enter the coefficients of your constraints with spaces (each in a new line):")
    eqs = []
    for i in range(constraints):
        eqs.append(list(map(int, input(" >> ").split(" "))))
    print("Please enter the right hand side of your constraints:")
    print("________________________________________________________________________")
    b = list(map(int, input(" >> ").split(" ")))
    print("________________________________________________________________________")
    

else : 
    c = [1.0, 1.0, 1.0, 1.0, 1.0]
    eq1 = [3.0, 2.0, 1.0, 0.0, 0.0]
    eq2 = [5.0, 1.0, 1.0, 1.0, 0.0]
    eq3 = [2.0, 5.0, 1.0, 0.0, 1.0]
    b = [1.0, 3.0, 4.0]
    eqs = []
    eqs.append(eq1)
    eqs.append(eq2)
    eqs.append(eq3)


tables = SetUpTables(c, eqs, b)
PrintTables(tables)
tables = TwoPhasedSimplex(tables)
PrintTables(tables)
print('minimum cost is = {}'.format(-tables[0][0]))
