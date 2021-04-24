
from __future__ import print_function
from PIL import Image
import os,sys,glob,math,time
#change prieview to after 
#update read me 
def main():
    #variables 
    small_pic = str
    dice_data = []
    raw_pixel_data = []
    error = False
    #Input
    file_path = get_file_path()
    new_size  = (20,20) #get_dice_resolution()
    parser    = "d"#get_parsing_method()

    if (file_path == 'QUIT' or new_size == 'QUIT'):
        pass
    else:
        #process
        big_pic = Image.open(file_path)
        print('Resizing and reshaping')
        small_pic = resize(big_pic, new_size,file_path) # usesd pil thumnnail function 
        pic = Image.open(small_pic).convert("L") #puts image in grayscale 
        print('processing pixel data')
        raw_pixel_data = get_raw_pixel_data(pic)
        pixel_metrics = get_pixel_metrics(new_size,raw_pixel_data)
        print(pixel_metrics)
        dice_data = get_dice_data(pic,pixel_metrics,parser)
        #output
        print('printing instructions')  
        print_instructions(dice_data,pic.size,file_path[15:])
        print('making preview')
        try:
            make_preview(dice_data,pic.size,file_path[15:],parser)
        except (PermissionError):
            print('Sorry!')
            print('experincing techinical difficulties, wait a few minutes before trying again')
            time.sleep(20)
            error = True

        delete_thumbnail(file_path[15:])
        if error != True:
            print('finished')
            time.sleep(5)


""" Input Functions """  
def get_file_path(): # asks the user to input a file name 
    os.chdir('regular images')
    print('enter q or Q anytime to quit')
    print('Enter the entire filename of the jpeg you want diced')
    print('For exampe: myFace.jpg \n')
    file_name = input()
    while (os.path.isfile(file_name) == False):
        if (file_name.upper() == 'Q'): 
            return 'QUIT'
        print('I could not find that file please try again\n')
        file_name = input()
    os.chdir("..")
    return "regular images/" + file_name 


def get_dice_resolution():
    print('how many dice wide by how many dice high')
    print('i.e 100,75  keep in mind that the max is 128,128')
    user_input = ''
    while(user_input.upper != 'Q'):
        user_input = input()
        if user_input.upper() == 'Q':
            return 'QUIT'
        try:
            my_string = user_input
            values = my_string.split(',')
            w = values[0]
            h = values[1]
            w = int(w)
            h = int(h)
            if w <= 0 or h <= 0 or w >128 or h > 128: 
                print('it has to be tho postive whole numbers below 128')
                continue 
            return (w,h)
        except:
            print('it has have no spaces and be two positive whole numbers')
            continue
    return 'QUIT'


def get_parsing_method():
    print("Which transformation method should we use?")
    print('Direct Translation    "d"')
    print('Mid Tone Translation  "m"')
    print('More information      "i"')
    user_input = ' '
    while(user_input != "q"):
        user_input = input().lower()
        if (user_input == "d") or (user_input == "direct") or (user_input == "direct translation"):
            return "d"
        if (user_input == "m") or (user_input == "mid" )or (user_input == "mid tone"):
            return "m"
        if (user_input == "i") or (user_input == "more" )or (user_input == "more information"):
            print("Direct Translation is a 1 to 1 copy of the image into dice ")
            print("Mid Tone Translation smooths the contrast of the image and can be useful")
        print('Direct Translation    "d"')
        print('Mid Tone Translation  "m"')
        print('More information      "i"')


'''Processing Functions'''
def resize(image, size,fileName):#takes an image and a tuple, makes thumbnail sized images, returns the name of the file
    file = fileName.split('.')[0]
    image.thumbnail(size)
    checkFile = os.listdir()
    if (str(file) +" thumbnail" + ".JPG" not in checkFile):
        image.save(file +" thumbnail" + ".jpg", "JPEG")
    return str(file) +" thumbnail" + ".JPG"


def get_raw_pixel_data(image): #takes in an image object, returns an grid of dice values in arrays
    x,y = image.size
    i_x = 0 #horizontal iterator
    i_y = 0 #vertical iterator
    flag = False
    grid_values = []
    grid_values_2 = []
    px = image.load()
    raw_value = None
    while i_x < x - 1:
        if flag == True:
            i_x = i_x + 1
            grid_values.append(grid_values_2)
            i_y = 0
            grid_values_2 = []
        flag = False                                           
        while i_y < y:                                          
            raw_value = image.getpixel((i_x,i_y))
            grid_values_2.append(raw_value)                         
            i_y = i_y + 1                                       
            flag = True
    return grid_values


def get_pixel_metrics(image_size,pixel_values): 
    #takes tuple and 2D list of pixel data returns mean, range, standard deviaion
    (x,y) = image_size
    number_of_pixels = x*y
    sum_of_values = 0
    residual_total = 0 
    biggest = 0
    smallest = 0 
    for x_values in pixel_values:
        if biggest <  max(x_values):
            biggest = max(x_values)
        if smallest > min(x_values):
            smallest = min(x_values)
        for y_values in x_values:
            sum_of_values = sum_of_values + y_values
    mean = sum_of_values/number_of_pixels 
    
    for x_values in pixel_values:
        for y_values in x_values:
            residual = ( (y_values - mean)**2)
            residual_total = residual_total + residual
    residual_mean = residual_total/number_of_pixels
    standard_deviation = math.sqrt(residual_mean)
    return (mean,standard_deviation,biggest,smallest)
            
                       
def get_dice_data(image,mean_data,parser): #takes in an image object, returns a grid of dice values in arrays
    x,y = image.size
    i_x = 0 #horizontal iterator
    i_y = 0 #vertical iterator
    flag = False
    grid_values = [] #stores the y values for a collum in the x value
    grid_values_2 = [] #stores the y values 
    px = image.load()
    raw_value = None
    while i_x < x - 1:
        if flag == True:
            i_x = i_x + 1
            grid_values.append(grid_values_2)
            i_y = 0
            grid_values_2 = []
        flag = False                                           
        while i_y < y:                                          
            raw_value = image.getpixel((i_x,i_y))
            value = dice_values(raw_value,mean_data,parser)
            grid_values_2.append(value)                         
            i_y = i_y + 1                                       
            flag = True
    return grid_values


def dice_values(pixel,mean_data,parser): #takes in an int of pixel data and returns a value of 1-6
    mean, stand_dev,biggest,smallest = mean_data
    if (parser == "d"):
        distance =  biggest - smallest
        one_sixth = distance/6
        if pixel >= smallest and pixel <= (smallest + one_sixth):
            return 6
        elif pixel > (smallest + one_sixth) and pixel <= (smallest + (2*one_sixth) ):
            return 5
        elif pixel > (smallest + (2*one_sixth)) and pixel <= (smallest + (3*one_sixth)):
            return 4
        elif pixel > (smallest + (3*one_sixth) )and pixel <= (smallest + (4*one_sixth)):
            return 3
        elif pixel > (smallest + (4*one_sixth)) and pixel <= (smallest + (5*one_sixth)):
            return 2
        elif pixel > (smallest + (5*one_sixth)) and pixel <= (smallest + (6*one_sixth)+1):
            return 1
    elif(parser == "m"):
        if pixel >= 0 and pixel <= (mean - stand_dev):
            return 6
        elif pixel > (mean - stand_dev) and pixel <= (mean - (0.5)*stand_dev):
            return 5
        elif pixel > (mean - (0.5)*stand_dev) and pixel <= mean:
            return 4
        elif pixel > mean and  pixel<= (mean + (0.5)*stand_dev):
            return 3
        elif pixel > (mean + (0.5)*stand_dev) and pixel <= (mean + stand_dev):
            return 2
        elif pixel > (mean + stand_dev) and pixel <= 255:
            return 1


'''Output Functions'''
def print_instructions(array,image_size,file_name): #takes an array and a tuple prints a grid of easy to read dice values
    x_1, y_1 = image_size
    x_2 = 0 #index iterators
    y_2 = 0 #index iterators
    flag = False
    os.chdir('instructions')
    instructions = open(file_name + ' ' + str(image_size) + '.txt', 'w')
    instructions.close()
    with open(file_name + ' ' + str(image_size) + '.txt', 'w') as f:
        for i in range(0,y_1 -1):
            if flag == True:
                y_2 = y_2 +1
                x_2 = 0
                f.write("\n")
            flag = False
            for j in range(0,x_1 -1 ):
                f.write(' ' + str(array[x_2][y_2]))
                x_2 = x_2 +1
                flag = True
    os.chdir('..')


def make_preview(grid, size,file_name,parser): #takes in a 2D array of dice values and constructs an image out of pictues of dice
    x,y = tuple(100*m for m in size) 
    top_x = 0 
    top_y = 0
    bottom_x = 99 
    bottom_y = 99  
    pixel_count_x = 0
    pixel_count_y = 0
    paste_box = (top_x, top_y, bottom_x, bottom_y)
    dice_number = 0
    row_done = False
    os.chdir('dice')
    one = Image.open("side 1.jpg")
    two = Image.open("side 2.jpg")
    three = Image.open("side 3.jpg")
    four = Image.open("side 4.jpg")
    five = Image.open("side 5.jpg")
    six = Image.open("side 6.jpg")
    os.chdir('..')
    os.chdir('dice images')
    preview = Image.new('L', (x,y),0)
    preview.save( ( ("Direct_" if (parser == "d") else "Mid Tone_" ) + str(size) + "_" + file_name ), 'JPEG')
    preview1 = Image.open(( ("Direct_" if (parser == "d") else "Mid Tone_" ) + str(size) + "_" + file_name ))
    
    while bottom_x < x:
        if row_done == True:
            top_x = top_x + 100 #tracks the paste box top corner
            bottom_x = bottom_x + 100 #tracks the paste box bottom corner
            pixel_count_x = pixel_count_x + 1 #tracks the pixel in the grid of dice
            top_y = 0
            bottom_y = 0
            pixel_count_y = 0
            preview1.save( ( ("Direct_" if (parser == "d") else "Mid Tone_" ) + str(size) + "_" + file_name ), 'JPEG')
        row_done = False
        while bottom_y < y:
            paste_box = (top_x, top_y)
            try:    
                dice_number = grid[pixel_count_x][pixel_count_y]
            except:
                pass
            if dice_number == 1:
                p = preview1.paste(one,paste_box)
            elif dice_number == 2:
                p = preview1.paste(two,paste_box)
            elif dice_number == 3:
                p = preview1.paste(three,paste_box)
            elif dice_number == 4:
                p = preview1.paste(four,paste_box)
            elif dice_number == 5:
                p = preview1.paste(five,paste_box)
            elif dice_number == 6:
                p = preview1.paste(six,paste_box)
                
            top_y = top_y + 100
            bottom_y = bottom_y + 100
            
            pixel_count_y = pixel_count_y + 1
            row_done = True    
    preview1.save( ( ("Direct_" if (parser == "d") else "Mid Tone_" ) + str(size) + "_" + file_name ), 'JPEG')
    os.chdir('..')


def delete_thumbnail(file_name):
    os.chdir("regular images")
    files = os.listdir()
    for name in files:
        parts = name.split(' ')
        if (parts[-1] == 'thumbnail.jpg'):
            pass
            os.remove(name)
    os.chdir('..')


def make_dice_canvas(size): #takes a tuple of size data 
    new_size = tuple(100*x for x in size)  # changed from 10py
    canvas = Image.open("canvas/canvas.jpg")
    canvas.resize(new_size)
    canvas.save("canvas/canvas " + str(new_size) + ".Jpg", "JPEG")


######
main()
######
