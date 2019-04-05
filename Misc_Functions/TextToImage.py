import csv
import os
from PIL import Image, ImageDraw, ImageFont

def save_image(input_file, output_file):
    puzzle = []

    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            puzzle.append(line)

    #set image parameters

    x_offset = 4
    y_offset = -1.5
    size= len(puzzle)
    fontsize = int(18 * 500 / (size*size))
    width = len(puzzle[0])*fontsize
    height = len(puzzle)*fontsize
    linewidth=int(15/size)
    img = Image.new('RGB', (width,height), color = 'white')
    font = ImageFont.truetype('FRAMDCN.ttf', fontsize)
    d = ImageDraw.Draw(img)

    #fill the image with the contents of the .txt file
    yTop = 0
    for line in puzzle:
        for i in range(len(line)):
            if line[i] == 'I':
                I_offset = 2
                d.text((I_offset + x_offset + i*fontsize, y_offset + yTop), line[i], fill = (0,0,0), font = font)
            elif line[i] == 'T':
                T_offset = 1
                d.text((T_offset + x_offset + i*fontsize, y_offset + yTop), line[i], fill = (0,0,0), font = font)
            elif line[i] == '-':
                x0 = i*fontsize
                x1 = (i+1)*fontsize
                y0 = yTop
                y1 = yTop + fontsize
                d.rectangle([x0, y0, x1, y1], fill = (0,0,0))
            else:
                d.text((x_offset + i*fontsize, y_offset + yTop), line[i], fill = (0,0,0), font = font)

        yTop += fontsize

    #draw grid
    for j in range(len(puzzle[0])):
        xGrid = j*fontsize
        d.line([(xGrid, 0),(xGrid, height)], fill = (0,0,0), width=linewidth)

    for j in range(len(puzzle)):
        yGrid = j*fontsize
        d.line([(0, yGrid),(width, yGrid)], fill = (0,0,0), width=linewidth)

    d.line([(width-1, 0),(width-1, height)], fill = (0,0,0), width=linewidth)
    d.line([(0, height-1),(width, height-1)], fill = (0,0,0), width=linewidth)

    img.save(output_file)

#choose .txt file to read in
input_name_prefix = "../Valid_Boards/testing/"
for filename in os.listdir(input_name_prefix):
    output_name_prefix = "../Puzzle_Images/Solved/"
    input_file = input_name_prefix + filename
    output_file = output_name_prefix + filename + ".png"
    if output_name_prefix not in os.listdir(output_name_prefix):
        save_image(input_file, output_file)

raise
input_file = "../Valid_Boards/testing/15x15_Depth2_Iterations7500000_#6_650"
input_file = "../Valid_Boards/15x15_v3.txt"
output_file = "../Puzzle_Images/15x15_v3.png"

save_image(input_file,output_file)

