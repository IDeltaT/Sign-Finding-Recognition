#------------------------------------------
# Program by Krasnokutskiy.I.
#
#
# Version   ---Date---    -----Info-----
#   1.0     00.00.2020    Initial version
#
# SignFinder (Нахождение подписи)
#------------------------------------------


import cv2
from imageai.Detection.Custom import CustomObjectDetection
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

    :param arg: Список: [ссылка на объект рамки (Label), ширина рамки, высота рамки,
    ссылка на объект детектора (Detector)]
    :type arg:  list

    """

    l_panel = arg[0]
    lable_width = arg[1]
    lable_height = arg[2]
    detector = arg[3]

    global PIL_img
    global TK_img

    file_name = fd.askopenfilename(filetypes = (("PNG", "*.png"),
                                                ("JPG", "*.jpg")))

    #Передача ссылки на файл детектору
    detector.image_path = file_name

    PIL_img = Image.open(file_name)

    width_img = PIL_img.width
    height_img = PIL_img.height

    new_size = calculation_of_new_sizes(width_img, height_img, lable_width, lable_height)
    width_new = new_size[0]
    height_new = new_size[1]

    PIL_img = PIL_img.resize((width_new, height_new), Image.ANTIALIAS)
    TK_img = ImageTk.PhotoImage(PIL_img) 
    l_panel['image'] = TK_img


def open_model_file(e_model_path):
    """
    Считывание указанного (в проводнике) файла модели и
    присваивание этого изображения объекту Entry

    :param arg: Объект типа Entry
    :type arg:  Entry

    """

    file_name = fd.askopenfilename(filetypes = (("h5", "*.h5"), ("All files", "*.*")))

    e_model_path.delete(0, END)
    e_model_path.insert(0, file_name)


def open_json_file(e_json_path): 
    """
    Считывание указанного (в проводнике) файла Json и
    присваивание этого изображения объекту Entry

    :param arg: Объект типа Entry
    :type arg:  Entry

    """

    file_name = fd.askopenfilename(filetypes = (("JSON File", "*.json"), ("All files", "*.*")))

    e_json_path.delete(0, END)
    e_json_path.insert(0, file_name)


def load_model(arg): 
    """
    Загрузка готовой модели.
    Пути к файлам беруться из полей e_model_path и e_json_path

    :param arg: Список: [ссылка на объект поля (model) (Entry), 
    ссылка на объект поля (json) (Entry), ссылка на объект консоли (Text),
    ссылка на объект detector (class Detector)]
    :type arg:  list
    """

    e_model_path = arg[0]
    e_json_path = arg[1]
    t_console = arg[2]
    detector = arg[3]

    #Тег ошибки (красный цвет текста)
    t_console.tag_config('warning', foreground="red")
    #Тег успеха (зеленый цвет текста)
    t_console.tag_config('success', foreground="green")

    model_path = e_model_path.get()
    json_path = e_json_path.get()

    if ((len(model_path) == 0) or (len(json_path) == 0)):
        t_console.insert(1.0, "\nНеверно указан путь к файлу Модели или к Json!", 'warning')
        t_console.see("end")
    else:
        t_console.insert("end", "\nЗагрузка модели...", )
        t_console.see("end")

        try:      
            detector.detector.setModelTypeAsYOLOv3()
            detector.detector.setModelPath(model_path) #"detection_model-ex-008--loss-0003.909.h5"
            detector.detector.setJsonPath(json_path)   #"detection_config.json"
            detector.detector.loadModel()

            t_console.insert("end", "\nМодель загружена!", 'success')
            t_console.insert("end", "\nНазвание модели: " + model_path.split("/")[-1])
            t_console.see("end")

            detector.is_model_load = True
        except Exception:
            t_console.insert("end", "\nНе удалось загрузить модель!", 'warning')
            t_console.see("end")
    pass


class Detector:
    def __init__(self):
        self.detector = CustomObjectDetection()
        self.is_model_load = False
        self.image_path = ""


def process_file(arg):
    """
    Обработка изображения.

    :param arg: Список: [ссылка на объект поля (model) (Entry), 
    ссылка на объект поля (json) (Entry), ссылка на объект консоли (Text),
    ссылка на объект detector (class Detector),
    ссылка на объект t_console (Text)]
    :type arg:  list
    """

    detector = arg[0]
    l_panel_processed = arg[1]
    WLABEL = arg[2]
    HLABEL = arg[3]
    t_console = arg[4]

    #Тег ошибки (красный цвет текста)
    t_console.tag_config('warning', foreground="red")
    #Тег успеха (зеленый цвет текста)
    t_console.tag_config('success', foreground="green")
    
    if (detector.is_model_load):
        if (len(detector.image_path) != 0):

            t_console.insert("end", "\nОбработка...", )
            t_console.see("end")

            global PIL_img_n
            global TK_img_n

            detections = detector.detector.detectObjectsFromImage(input_image = detector.image_path,
                                                                  output_image_path = "image000.jpg",
                                                                  minimum_percentage_probability = 15,
                                                                  display_percentage_probability = False,
                                                                  display_object_name = False,
                                                                  thread_safe = True,
                                                                  )
            print(detections)
    
            # Вывод кординат и процентов совпадения подписей в консоль
            for detection in detections:
                t_console.insert("end", "\n" + str(detection["name"]) + ":" + str(detection["percentage_probability"]) + ":" + str(detection["box_points"]))
            t_console.see("end")

            PIL_img_n = Image.open("image000.jpg")

            width_img = PIL_img_n.width
            height_img = PIL_img_n.height

            new_size = calculation_of_new_sizes(width_img, height_img, WLABEL, HLABEL)
            width_new = new_size[0]
            height_new = new_size[1]

            PIL_img_n = PIL_img_n.resize((width_new, height_new), Image.ANTIALIAS)
            TK_img_n = ImageTk.PhotoImage(PIL_img_n) 
            l_panel_processed['image'] = TK_img_n

            t_console.insert("end", "\nИзображение обработано!", 'success')
            t_console.see("end")
        else:
            t_console.insert("end", "\nНе верно указан путь к изображению!", 'warning')
            t_console.see("end")
    else:
        t_console.insert("end", "\nМодель не загружена!", 'warning')
        t_console.see("end")



def main():
    ''' Главная функция '''

    #Инициализация обработчика
    detector = Detector()

    #Главное окно
    root = Tk()
    root.geometry('1000x680')
    root.configure(bg = '#dddddd')
    root.resizable(False, False) # Запрет на изменение размеров окна
    root.title("Finder")

    #Создание меню в шапке
    main_menu = Menu(root) 
    root.config(menu = main_menu)

    #Размер центральных окон
    WLABEL = 400
    HLABEL = 520


    #Окна отображения изображений
    f_left = Frame(root)
    f_left.configure(bg = '#dddddd')

    #Окно отображающее не обработанное изображение
    f_source_img = LabelFrame(root, text = "Исходное изображение", width = 420, height = 520,) 
    l_panel_source = Label(root) 
    
    #Окно отображающее обработанное изображение
    f_processed_img = LabelFrame(root, text = "Обработанное изображение", width = 420, height = 520)
    l_panel_processed = Label(root)


    #Нижнее меню
    #region down mwnu

    #Консоль
    t_console = Text(width = 50, height = 6)
    scroll_console = Scrollbar(command = t_console.yview, orient="vertical")
    t_console.config(yscrollcommand=scroll_console.set)

    #Тег ошибки (красный цвет текста)
    t_console.tag_config('warning', foreground="red")

    t_console.insert("end", "Загрзите модель и json файл!", 'warning')
    t_console.see("end")

    #Выбор пути к модели и json
    l_model_path = Label(text = "Директория модели:")
    l_json_path  = Label(text = "Директория json:")
    e_model_path = Entry(width = 60)
    e_json_path  = Entry(width = 60)
    b_model_path = Button(root, text = '...', command = lambda arg = e_model_path: open_model_file(arg))
    b_json_path  = Button(root, text = '...', command = lambda arg = e_json_path: open_json_file(arg))
    b_load_model = Button(root, text = 'Загрузить модель', command = lambda arg = [e_model_path, e_json_path, t_console, detector]: load_model(arg))
    l_model_path.configure(bg = '#dddddd')
    l_json_path.configure(bg = '#dddddd')
    #endregion


    #Боковое меню
    b_arg_list = [l_panel_source, WLABEL, HLABEL, detector]
    b_open_file = Button(f_left, text = 'Открыть', width = 10, command = lambda arg = b_arg_list: open_file(arg))

    b_process = Button(f_left, text = 'Обработать', width = 10, command = lambda arg = [detector, l_panel_processed, WLABEL, HLABEL, t_console]: process_file(arg))
    b_compare = Button(f_left, text = 'Сравнить', width = 10, )


    #Упаковка центральных окон
    f_source_img.grid(row = 0, column = 1, columnspan = 10, rowspan = 13, ipady = 16,)
    f_processed_img.grid(row = 0, column = 15, columnspan = 10, rowspan = 13, ipady = 16,)
    l_panel_source.grid(row = 1, column = 1, columnspan = 10, rowspan = 13, pady = 16)
    l_panel_processed.grid(row = 0, column = 15, columnspan = 10, rowspan = 13,)


    #Упаковка бокового меню
    f_left.grid(row = 0, column = 0, rowspan = 3, ipady=6, padx = 5)
    b_open_file.pack(pady = 1)
    b_process.pack(pady = 1)
    b_compare.pack(pady = 1)
   
    
    #Меню в шапке
    #region Menu
    file_menu = Menu(main_menu, tearoff = 0)
    file_menu.add_command(label = "Открыть...", command = lambda arg = b_arg_list: open_file(arg))
    file_menu.add_command(label = "Новый")
    file_menu.add_command(label = "Сохранить...")
    file_menu.add_command(label = "Выход")
 
    help_menu = Menu(main_menu, tearoff = 0)
    help_menu.add_command(label = "Помощь")
    help_menu.add_command(label = "О программе")
 
    main_menu.add_cascade(label = "Файл", menu = file_menu)
    main_menu.add_cascade(label = "Справка", menu = help_menu)
    #endregion
    

    #Упаковка нижнего меню
    #region down_menu_gird
    l_model_path.grid(row = 15, column = 1, columnspan = 9, sticky=W) 
    e_model_path.grid(row = 16, column = 1, columnspan = 9, sticky=W)
    b_model_path.grid(row = 16, column = 10, sticky=W+N)
    l_json_path.grid(row = 17, column = 1, columnspan = 9, sticky=W ) #padx = 5
    e_json_path.grid(row = 18, column = 1, columnspan = 9, sticky=W ) 
    b_json_path.grid(row = 18, column = 10, sticky=W+N)
    b_load_model.grid(row = 19, column = 1, columnspan = 9)
    t_console.grid(row = 15, column = 12, columnspan = 5, rowspan = 5) 
    scroll_console.grid(row = 15, column = 20, rowspan = 5, sticky=N+S) 
    #endregion



    root.mainloop()



if __name__ == '__main__':
    main()






#------TEMP------#

#---------TRANING------------#
'''
from imageai.Detection.Custom import DetectionModelTrainer
trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="sign")
trainer.setTrainConfig(object_names_array=["sign"], batch_size=2, num_experiments=8, train_from_pretrained_model="pretrained-yolov3.h5")
trainer.trainModel()
'''

#---------MARK-----------#
'''
trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="sign")
metrics = trainer.evaluateModel(model_path="sign/models", json_path="sign/json/detection_config.json", iou_threshold=0.5, object_threshold=0.3, nms_threshold=0.5)
print(metrics)
'''
#------------DETECTED-----------#
'''
from imageai.Detection.Custom import CustomObjectDetection

detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("detection_model-ex-008--loss-0003.909.h5")
detector.setJsonPath("detection_config.json")
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image="image (68).jpg", output_image_path="image (68)-detected.jpg", minimum_percentage_probability=10)
for detection in detections:
    print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])
'''

#------------TEMP-----------#
'''
file_name3 = fd.askopenfilename()
detections = detector.detectObjectsFromImage(input_image=file_name3, output_image_path="image000.jpg", minimum_percentage_probability=10)
print(detections)
    
#for detection in detections:
    #print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])

PIL_img = Image.open("image000.jpg")

width_img = PIL_img.width
height_img = PIL_img.height

new_size = calculation_of_new_sizes(width_img, height_img, WLABEL, HLABEL)
width_new = new_size[0]
height_new = new_size[1]

PIL_img = PIL_img.resize((width_new, height_new), Image.ANTIALIAS)
TK_img = ImageTk.PhotoImage(PIL_img) 
l_panel_processed['image'] = TK_img
'''