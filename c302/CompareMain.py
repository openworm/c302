__author__ = 'Ari'

from operator import itemgetter
import xlrd
import os

def comparitor(fName1, fName2):

    path1 = "../../../" + fName1
    path2 = "../../../" + fName2
    dir = os.path.dirname(__file__)
    file1 = os.path.join(dir, path1)
    file2 = os.path.join(dir, path2)

    # read .xls files, place data in dictionary.
    cols1, indexName1 = getColumnsXls(file1)
    cols2, indexName2 = getColumnsXls(file2)

    # Format dictionaries to match, and arrange alphabetically.
    formatNames(cols1, indexName1)
    formatNames(cols2, indexName2)
    sortTwoColumns(cols1)
    sortTwoColumns(cols2)

    # Create column with matching values, while removing those values from original lists.
    matches, col1, col2 = matchLists(cols1, cols2, indexName1, indexName2)

    # Print results. Give number of pairs that are matched, remained from unmatched files, and associated pairs.
    print "Number of matching pairs: " + str(len(matches[indexName2[0]]))
    for p in range(len(matches[indexName2[0]])):
        print str(matches[indexName2[0]][p])+" -> "+str(matches[indexName2[1]][p])+" ("+str(matches[indexName2[2]][p])+", "+str(matches[indexName2[3]][p])+")"
    print "\nNumber of pairs unmatched in " + fName1 + " is: " + str(len(col1[indexName2[0]]))
    for p in range(len(col1[indexName2[0]])):
        print str(col1[indexName2[0]][p])+" -> "+str(col1[indexName2[1]][p])+" ("+str(col1[indexName2[2]][p])+", "+str(col1[indexName2[3]][p])+")"
    print "\nNumber of pairs unmatched in " + fName2 + " is: " + str(len(col2[indexName1[0]]))
    for p in range(len(col2[indexName1[0]])):
        print str(col2[indexName1[0]][p])+" -> "+str(col2[indexName1[1]][p])+" ("+str(col2[indexName1[2]][p])+", "+str(col2[indexName1[3]][p])+")"


# Get columns from .txt files
def getColumns(fileIn, delim = "\t", header = True):
    cols = {}
    indexName = {}
    for lineNum, line in enumerate(fileIn):
        if lineNum == 0:
            headings = line.split(delim)
            i = 0
            for heading in headings:
                heading = heading.strip()
                if header:
                    cols[heading] = []
                    indexName[i] = heading
                else:
                    cols[i] = [heading]
                    indexName[i] = i
                i += 1
        else:
            cells = line.split(delim)
            i = 0
            for cell in cells:
                cell = cell.strip()
                cols[indexName[i]] += [cell]
                i += 1
    return cols, indexName

# Get columns from .xls files
def getColumnsXls(fileIn):
    cols = {}
    indexName = {}
    workbook = xlrd.open_workbook(fileIn)
    # worksheet = workbook.sheet_by_name('Sheet1')
    worksheet = workbook.sheet_by_index(0)
    num_rows = worksheet.nrows - 1
    # num_cells = worksheet.ncols
    num_cells = 3
    curr_row = 0
    for c in range(4):
        indexName[c] = str(worksheet.cell_value(curr_row, c))
        cols[indexName[c]] = []
        # print indexName[c]
    while curr_row < num_rows:
        curr_row += 1
        row = worksheet.row(curr_row)
        # print 'Row:', curr_row
        curr_cell = -1
        while curr_cell < num_cells:
            curr_cell += 1
            # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
            cell_type = worksheet.cell_type(curr_row, curr_cell)
            cell_value = str(worksheet.cell_value(curr_row, curr_cell))
            # print '	', cell_type, ':', cell_value
            cols[indexName[curr_cell]] += [cell_value]
    return cols, indexName

# Sort dictionaries by first two column (From/To Neurons), first by one, then the other.
def sortTwoColumns(cols):
    cols = sorted(cols, key = itemgetter(0,1))

# Formatting involved removing any filler zeros from the middle of strings.
def formatNames(cols, indexName):
    for i in range(2):
        for char in cols[indexName[i]]:
            if char[-1] != '0':
                char = "".join(char.split("0",1))

# Compare two lists, create new list of matching pairs, remove pairs from respective original lists.
def matchLists(cols1, cols2, indexName1, indexName2):
    # Ensure that largest list is always "col1"
    if len(cols1[indexName1[0]]) > len(cols2[indexName2[0]]):
        col1 = cols1.copy()
        col2 = cols2.copy()
        indexNames1 = indexName1.copy()
        indexNames2 = indexName2.copy()
    else:
        col1 = cols2.copy()
        col2 = cols1.copy()
        indexNames1 = indexName2.copy()
        indexNames2 = indexName1.copy()

    # Initialize matches dictionary
    matches = {}
    for i in range(len(indexNames1)):
        matches[indexNames1[i]] = []

    # 1 - check if pair matches from long list and short list
    for pair in zip(col1[indexNames1[0]], col1[indexNames1[1]]):
        for p1, x1 in enumerate(zip(col1[indexNames1[0]], col1[indexNames1[1]])):
            if x1 == pair:
                index1 = p1
        # ind = [p for p,x in enumerate(zip(cols1[indexName1[0], cols1[indexName1[1]]])) if x == pair]
        # If first two columns of small array contain current pair from long array...
        if zip(col2[indexNames2[0]], col2[indexNames2[1]]).__contains__(pair):
            for p2, x2 in enumerate(zip(col2[indexNames2[0]], col2[indexNames2[1]])):
                if x2 == pair:
                    index2 = p2
            # If matches array does not contain current pair from long array, add it
            if not zip(matches[indexNames1[0]], matches[indexNames1[1]]).__contains__(([pair[0]],[pair[1]])):
                # print matches[indexNames1[0]], matches[indexNames1[1]]
                for i in range(len(indexNames1)):
                    if col1[indexNames1[i]][index1] == col2[indexNames2[i]][index2]:
                        # if i < 2 & len(col1[indexNames1[i]][index1]):
                        #     print "HO"
                        matches[indexNames1[i]] += [[col1[indexNames1[i]][index1]]]
                        del col2[indexNames2[i]][index2]
                        del col1[indexNames1[i]][index1]
                    else:
                        matches[indexNames1[i]] += [[col1[indexNames1[i]][index1], col2[indexNames2[i]][index2]]]
                        del col2[indexNames2[i]][index2]
                        del col1[indexNames1[i]][index1]
            # If pair is already in array, add value from last two columns to array
            else:
                for p3, x3 in enumerate(zip(matches[indexNames1[0]], matches[indexNames1[1]])):
                    if x3 == ([pair[0]], [pair[1]]):
                        index3 = p3
                for i in range(len(indexNames1)):
                    if i > 1:
                        matches[indexNames1[i]][index3] += [col1[indexNames1[i]][index1]]
                    del col1[indexNames1[i]][index1]
                    del col2[indexNames2[i]][index2]

    # 2* - check if pair matches again from long list and matching list
    for pair in zip(col1[indexNames1[0]], col1[indexNames1[1]]):
        for p1, x1 in enumerate(zip(col1[indexNames1[0]], col1[indexNames1[1]])):
            if x1 == pair:
                index1 = p1
        # If matches array does contain current pair from long array, add its conn. type and number
        if zip(matches[indexNames1[0]], matches[indexNames1[1]]).__contains__(([pair[0]],[pair[1]])):
            for p3, x3 in enumerate(zip(matches[indexNames1[0]], matches[indexNames1[1]])):
                if x3 == ([pair[0]], [pair[1]]):
                    index3 = p3
            for i in range(len(indexNames1)):
                if i > 1:
                    matches[indexNames1[i]][index3] += [col1[indexNames1[i]][index1]]
                del col1[indexNames1[i]][index1]

    # 3 - check if pair from match list has a reversable pair from the long list
    for pair in zip(col1[indexNames1[0]], col1[indexNames1[1]]):
        # reversepair = [pair[1],pair[0]]
        for p1, x1 in enumerate(zip(col1[indexNames1[0]], col1[indexNames1[1]])):
            if x1 == pair:
                index1 = p1
        # if zip(matches[indexNames1[1]],matches[indexNames1[0]]).__contains__(([pair[0]], [pair[1]])):
        for p4, x4 in enumerate(zip(matches[indexNames1[0]], matches[indexNames1[1]])):
            if x4 == ([pair[1]], [pair[0]]):
                index4 = p4
        if zip(matches[indexNames1[0]], matches[indexNames1[1]]).__contains__(([pair[1]], [pair[0]])):
            # print zip(matches[indexNames1[0]], matches[indexNames1[1]])
            # print ([pair[1]], [pair[0]])
            for i in range(len(indexNames1)):
                if i > 1:
                    # print len(matches[indexNames1[i]]), index4
                    # print len(col1[indexNames1[i]]), index1
                    matches[indexNames1[i]][index4] += [col1[indexNames1[i]][index1]]
                del col1[indexNames1[i]][index1]


    return matches, col1, col2

# Option of additional formatting to shorten lists. Not used. Not complete.
# 'EJ' maps to 'GapJunction'.
# 'R', 'Rp', 'S', 'Sp' map to 'Send'.
# 'NMJ' does not map.
def typeMapping(cols1, cols2, indexName1, indexName2):
    list1 = ['GapJunction','Send']
    list2 = ['EJ','NMJ','R','Rp','S','Sp']
    type1 = cols1[indexName1[2]]
    type2 = cols2[indexName2[2]]


if __name__ == '__main__':
    fName1 = "CElegansNeuronTables.xls"
    fName2 = "NeuronConnectFormatted.xlsx"

    # file1 = "C:\\Users\\Ari\\Documents\\Projects\\OpenWorm\\book1.txt"
    # file2 = "C:\\Users\\Ari\\Documents\\Projects\\OpenWorm\\book2.txt"
    # xfile1 = "C:\\Users\\Ari\\Documents\\Projects\\OpenWorm\\CElegansNeuroML\\CElegansNeuronTables.xls"
    # xfile2 = "C:\\Users\\Ari\\Documents\\Projects\\OpenWorm\\CElegansNeuroML\\NeuronConnectFormatted.xlsx"
    comparitor(fName1,fName2)