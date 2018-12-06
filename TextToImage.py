import csv

from PIL import Image, ImageDraw

text = "Valid_Boards/4x4_v1.txt"
width = 55
height = 60
yTop = 10
i = 0
puzzle = []
img = Image.new('RGB', (width,height), color = 'white')
d = ImageDraw.Draw(img)

with open(text) as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        puzzle.append(line)

for line in puzzle:
    d.text((10,yTop), line[0], fill = (0,0,0))
    d.text((20,yTop), line[1], fill = (0,0,0))
    d.text((30,yTop), line[2], fill = (0,0,0))
    d.text((40,yTop), line[3], fill = (0,0,0))
    yTop += 10

img.save('Crossword.png')
