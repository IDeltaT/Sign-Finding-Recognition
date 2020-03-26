#------------------------------------------
# Program by Krasnokutskiy.I.
#
#
# Version   ---Date---    -----Info-----
#   1.0     00.00.2020    Initial version
#
# SignFinder (Нахождение подписи)
#------------------------------------------



from tkinter import *
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import os


def calculation_of_new_sizes(width_img, height_img, lable_width, lable_height):
    """
    Расчет новых размеров изображения, в соответствии с размерами рамки

    :param width_img: Исходная ширина изображения
    :type width_img:  int

    :param height_img: Исходная высота изображения
    :type height_img:  int

    :param lable_width: Ширина окна
    :type lable_width:  int

    :param lable_height: Высота окна
    :type lable_height:  int 
    
    :return: Возврощает список: [новая ширина, новая высота]
    :rtype: list
    """

    if (width_img > height_img):
        width_new = lable_width
        k_resize = round(lable_width * 100 / width_img)
        height_new = round(height_img * k_resize / 100)

    elif (width_img < height_img):
        height_new = lable_height
        k_resize = round(lable_height * 100 / height_img)
        width_new = round(width_img * k_resize / 100)

    else:
        # если width_img = height_img
        if (lable_width > lable_height):
            width_new = lable_height
            height_new = lable_height

        elif(lable_width <= lable_height):
            width_new = lable_width
            height_new = lable_width

    return [width_new, height_new]


def open_file(arg):
    """
    Считывание указанного (в проводнике) изображения, перерасчет его размеров и
    присваивание этого изображения объекту Label

    :param arg: Список: [ссылка на объект рамки (Label), ширина рамки, высота рамки]
    :type arg:  list

    """

    l_panel = arg[0]
    lable_width = arg[1]
    lable_height = arg[2]

    global PIL_img
    global TK_img

    file_name = fd.askopenfilename()

    PIL_img = Image.open(file_name)

    width_img = PIL_img.width
    height_img = PIL_img.height

    new_size = calculation_of_new_sizes(width_img, height_img, lable_width, lable_height)
    width_new = new_size[0]
    height_new = new_size[1]

    PIL_img = PIL_img.resize((width_new, height_new), Image.ANTIALIAS)#
    TK_img = ImageTk.PhotoImage(PIL_img) 
    l_panel['image'] = TK_img


def main():
    ''' Главная функция '''

    root = Tk()
    root.geometry('1000x600') #'200x200'

    WLABEL = 400
    HLABEL = 520

    f_left = Frame(root)

    f_source_img = LabelFrame(root, text = "Исходное изображение", width = 420, height = 520,)
    f_processed_img = LabelFrame(root, text = "Обработанное изображение", width = 420, height = 520)

    l_panel_source = Label(root) 

    label_test = Label(text = "123")
    
    b_arg_list = [l_panel_source, WLABEL, HLABEL]
    b_open_file = Button(f_left, text = 'Открыть', width = 10, command = lambda arg = b_arg_list: open_file(arg))

    b_process = Button(f_left, text = 'Обработать', width = 10)
    #b_open_file = Button(text = 'Открыть', command = lambda panel = l_panel: open_file(panel))
    #b_open_file.bind('<Button-1>', lambda event, panel = l_panel: open_file(event, panel))

    f_source_img.grid(row = 0, column = 1, columnspan = 10, rowspan = 13, ipady=16, )
    f_processed_img.grid(row = 0, column = 15, columnspan = 10, rowspan = 13, ipady=16,)
    l_panel_source.grid(row = 1, column = 1, columnspan = 10, rowspan = 13,)

    #b_open_file.grid(row = 0, column = 0, padx = 5, ipady = 5)
    #b_process.grid(row = 1, column = 0, padx = 5, ipady = 5,)

    f_left.grid(row = 0, column = 0, rowspan = 2, ipady=6, padx = 5)
    b_open_file.pack(pady = 1)
    b_process.pack(pady = 1)
    

    label_test.grid(row = 14, column = 0, padx = 5,)
    print(root.grid_size()) 

    root.mainloop()
    



if __name__ == '__main__':
    main()






#------TEMP------#
'''
file_name = fd.askopenfilename()
print(file_name)
img1 = Image.open(file_name)
#img = ImageTk.PhotoImage(Image.open(file_name))
img1 = img1.resize((400, 400), Image.ANTIALIAS)#
img = ImageTk.PhotoImage(img1)    
l_panel['image'] = img
'''

#img = Image.open(file_name)
#img.show()

#canvas = Canvas(root,width=150,height=150) 

#pilImage = Image.open(file_name)
#image = ImageTk.PhotoImage(pilImage)
#imagesprite = canvas.create_image(400,400,image=image)

#canvas.pack()
