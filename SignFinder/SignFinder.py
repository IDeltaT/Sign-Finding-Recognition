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




def open_file(panel):

    l_panel = panel
    global img1
    global img
    file_name = fd.askopenfilename()
    img1 = Image.open(file_name)
    img1 = img1.resize((400, 400), Image.ANTIALIAS)#
    img = ImageTk.PhotoImage(img1) 
    l_panel['image'] = img



def main():
    ''' Главная функция '''

    root = Tk()
    root.geometry('400x400') #'200x200'

    l_panel = Label(root, width = 40, height = 10) 
    
    b_open_file = Button(text = 'Открыть', command = lambda panel = l_panel: open_file(panel))
    #b_open_file.bind('<Button-1>', lambda event, panel = l_panel: open_file(event, panel))


    l_panel.pack(side = "bottom", fill = "both", expand = "yes")
    b_open_file.pack()

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