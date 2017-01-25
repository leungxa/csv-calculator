import csv

INPUT_FILE = 'Spreadsheet HW input.csv'
GIVEN_OUTPUT_FILE = 'Spreadsheet HW output.csv'
OUTPUT_FILE = 'output.csv'

def is_cell_valid_name(name):
    if len(name) > 1 and name[0].isalpha() and name[1:].isdigit():
        return True
    return False

def test_is_cell_valid_name():
    assert(is_cell_valid_name('b24') == True)
    assert(is_cell_valid_name('24') == False)
    assert(is_cell_valid_name('b') == False)
    assert(is_cell_valid_name('') == False)

def get_cell(name):
    col = None
    row = None
    if name[0].isalpha():
        col = ord(name[0]) % 32 - 1
    if name[1:].isdigit():
        row = int(name[1:]) - 1
    return col, row

def test_get_cell():
    assert(get_cell('b24') == (1,23))
    assert(get_cell('c3') == (2,2))

def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True

def test_is_number():
    assert(is_number(5) == True)
    assert(is_number(5.0) == True)
    assert(is_number('5.0') == True)
    assert(is_number('-1') == True)
    assert(is_number('x') == False)
    assert(is_number('1/2/3') == False)

def apply_op(o1, o2, op):
    return {
        '+': o1 + o2,
        '-': o1 - o2,
        '*': o1 * o2,
        '/': o1 / o2 if o2 > 0 else None,
    }.get(op, None)

def test_apply_op():
    assert(apply_op(3.0, 3.0, '+') ==  6.0)
    assert(apply_op(7.0, 2.0, '/') ==  3.5)
    assert(apply_op(7.0, 2.0, '-') ==  5.0)
    assert(apply_op(7.0, 2.0, '*') ==  14.0)
    assert(apply_op(7.0, 0, '/') ==  None)

def evaluate(cell, doc, row=None, col=None):
    numbers = []
    valid_operators = ['+', '-', '*', '/']
    error = '#ERR'
    if not len(cell) or cell[0] == ' ':
        return '0'

    equation = cell.split(' ')
    for token in equation:
        if is_cell_valid_name(token):
            ncol, nrow = get_cell(token)
            if ncol == col and nrow == row:
                return error
            value = evaluate(doc[nrow][ncol], doc, row=nrow, col=ncol)
            doc[nrow][ncol] = value
            token = value
        if is_number(token):
            numbers.append(float(token))
        elif token in valid_operators:
            if len(numbers) < 2:
                return error
            o1 = numbers.pop()
            o2 = numbers.pop()
            result = apply_op(o2, o1, token)
            if result is None:
                return error
            numbers.append(result)
    if len(numbers) != 1:
        return error
    return '{0:g}'.format(numbers[0])

def test_evaluate():
    doc = []
    assert(evaluate('1/2/2017', doc) == '#ERR')
    assert(evaluate('3', doc) == '3')
    assert(evaluate('5 1 2', doc) == '#ERR')
    assert(evaluate('7 2 /', doc) == '3.5')
    assert(evaluate('5 1 2 + 4 * + 3 -', doc) == '14')
    assert(evaluate('+', doc) == '#ERR')
    assert(evaluate('', doc) == '0')
    assert(evaluate(' ', doc) == '0')

    doc = [
            ['c1 b1 +', '0', '1'],
            ['a1', '', ''],
        ]
    assert(evaluate('a1', doc, row=1, col=0) == '1')

    doc = [
        ['c1 b1 +', '0', '#ERR'],
        ['a1', 'b2', ''],
    ]
    assert(evaluate('a1', doc, row=1, col=0) == '#ERR')
    assert(evaluate('b2', doc, row=1, col=1) == '#ERR')

    doc = [
        ['2 b2 3 * -', '0', '#ERR'],
        ['a1', '5', 'd5'],
    ]
    assert(evaluate('b2', doc, row=0, col=0) == '5')
    assert(evaluate('2 b2 3 * -', doc, row=0, col=0) == '-13')


def run_tests():
    test_get_cell()
    test_is_cell_valid_name()
    test_is_number()
    test_apply_op()
    test_evaluate()

def main():
    doc = []
    with open(INPUT_FILE, 'rb') as csvfile: 
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader: 
            doc.append(row)

    for i, row in enumerate(doc):
        for j, cell in enumerate(row):
            doc[i][j] = evaluate(cell, doc, row=i, col=j)

    with open(OUTPUT_FILE, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|')
        for row in doc:
            spamwriter.writerow(row)

def test_main():
    with open(GIVEN_OUTPUT_FILE, 'rb') as given: 
        with open(OUTPUT_FILE, 'rb') as output:
            reader_given = csv.reader(given, delimiter=',', quotechar='|')
            reader_output = csv.reader(output, delimiter=',', quotechar='|')
            for row in reader_given:
                row2 = reader_output.next()
                assert(row == row2)

run_tests()
main()
test_main()
