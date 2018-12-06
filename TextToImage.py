import csv

from PIL import Image, ImageDraw, ImageFont

text = "Valid_Boards/15x15_v1.txt"
#text = "Valid_Boards/4x8_v1.txt"
#text = "Valid_Boards/4x4_v1.txt"

puzzle = []

with open(text) as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        puzzle.append(line)

fontsize = 20
width = len(puzzle[0])*fontsize
height = len(puzzle)*fontsize
x_offset = 3
y_offset = 2
img = Image.new('RGB', (width,height), color = 'white')
font = ImageFont.truetype('calibri.ttf', fontsize)
d = ImageDraw.Draw(img)

yTop = 0

for line in puzzle:
    for i in range(len(line)):
        d.text((x_offset + i*fontsize, y_offset + yTop), line[i], fill = (0,0,0), font = font)

    yTop += fontsize

#draw grid
for j in range(len(puzzle[0])):
    xGrid = j*fontsize
    d.line([(xGrid, 0),(xGrid, height)], fill = (0,0,0))

for j in range(len(puzzle)):
    yGrid = j*fontsize
    d.line([(0, yGrid),(width, yGrid)], fill = (0,0,0))

d.line([(width-1, 0),(width-1, height)], fill = (0,0,0))
d.line([(0, height-1),(width, height-1)], fill = (0,0,0))

img.save('CrosswordTest3.png')
