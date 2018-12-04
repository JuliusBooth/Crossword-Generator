import csv

def read(text):
    puzzle = []
    with open(text) as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            puzzle.append(line)
            print(line)
    return(puzzle)

puzzle = read('crossword.txt')

def write(puzzle, text):
    with open(text, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(puzzle)

write(puzzle, 'test.txt')
