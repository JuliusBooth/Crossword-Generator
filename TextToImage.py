import csv

from PIL import Image, ImageDraw, ImageFont

def save_image(input_file, output_file):
    puzzle = []

    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            puzzle.append(line)

    #set image parameters
    fontsize = 18
    x_offset = 4
    y_offset = -1.5

    width = len(puzzle[0])*fontsize
    height = len(puzzle)*fontsize
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
        d.line([(xGrid, 0),(xGrid, height)], fill = (0,0,0))

    for j in range(len(puzzle)):
        yGrid = j*fontsize
        d.line([(0, yGrid),(width, yGrid)], fill = (0,0,0))

    d.line([(width-1, 0),(width-1, height)], fill = (0,0,0))
    d.line([(0, height-1),(width, height-1)], fill = (0,0,0))

    img.save(output_file)

#choose .txt file to read in
input_file = "Valid_Boards/4x4/Board#1012"

output_file = "Puzzle_Images/4x4_generated1012.png"
save_image(input_file,output_file)

