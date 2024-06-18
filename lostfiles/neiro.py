import atexit
import time

from ultralytics import YOLO
import cv2
import supervision as sv
from datetime import date, datetime
import json
import configparser

dir_path = "../diplom_project/lostfiles"


def main():
    model = YOLO("yolov8m.pt")  # Импортируем модель
    model.classes = [0, 24, 25, 26, 28, 67]  # Присваиваем нейронке только нужные классы 0 -person
    # 24 - backpack 25 - umbrella 26 - handbag 28 - suitcase, 67 - cell phone

    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("Config.ini", encoding='utf-8-sig')  # Читаем наш файл конфигурации
    kor_aud = config["auditory"]["kor_aud"]  # Присваиваем значение хранящееся в корпус_аудитории
    atexit.register(the_time_has_come, model, kor_aud)  # Создаем действие при завершении работы
    break_times = ["10:00", "11:40", "13:20", "15:30", "17:10", "18:50", "20:30"]  # Список времени окончаний пар
    while True:  # Цикл для проверки совпадения текущего времени с временем из списка break_times
        now = datetime.now()  # Берем текущее время
        current_time = now.strftime("%H:%M")  # Приводим его к нужному шаблону

        #if (current_time in break_times):  # Это нужно впринципе, но на показе лучше не использовать
        the_time_has_come(model, kor_aud)  # вызываем метод для начала работы нейросети
        break
        #else:
            #time.sleep(30)  # Делаем паузу на 30 секунд

def the_time_has_come(model,  kor_aud):
    data = []  # Список для помещение туда информации о предметах
    now = datetime.now()  # Берем текущее время
    current_time = now.strftime("%H:%M")  # Приводим его к нужному шаблону
    img_name, item_names = neiro_work(model)  # Вызываем метод для работы нейросети передавая туда нашу модель
    if item_names.__len__() > 0:  # Проверяем нашла ли наша нейросеть что-нибудь
        for i in item_names:  # перебираем содержимое имен найденных предметов
            data.append({"img_path": img_name,  # Путь до картинки
                         "item_name": i,  # Имя предмета
                         "date": str(date.today()) + "-" + current_time,  # Дата нахождение
                         "aud": kor_aud,  # Аудитория и корпус
                         })
            with open(f"{dir_path}/{kor_aud}.json", "w") as file:  # Открываем json файл в следующем пути
                json.dump(data, file)  # Записываем нашу дату

def neiro_work(model):  # Метод работы нейросети
    cap = cv2.VideoCapture(0)  # Берем нашу вебкамеру
    now = datetime.now()  # Берем дату
    modelnames = []  # Создаем список имен который вернем в конце программы
    current_time = now.strftime("%H-%M-%S")  # Приводим время к нужному формату
    img_name = "./" + str(
        date.today()) + "-" + current_time + ".png"  # Создаем название имени файла которое состоит из даты и времени
    BoundingBoxAnnotator = sv.BoundingBoxAnnotator(  # Создаем рамку
        thickness=2,
    )
    LabelAnnotator = sv.LabelAnnotator(  # Создаем подпись для рамки
        text_thickness=2,
        text_scale=1
    )
    time.sleep(10)
    ret, frame = cap.read()  # Возращаем кадр
    result = model(frame)[0]  # Обрабатывакм кадр
    for r in result:  # Перебираем содержимое result
        boxes = r.boxes  # Берем наши рамки
        for box in boxes:  # Перебираем рамки
            c = box.cls  # присваиваем имя первой рамки
            # if (model.names[int(c)] == "person"):
            #     modelnames.clear()
            #     break
            print(model.names[int(c)])
            modelnames.append(model.names[int(c)])  # Записываем имя нашей первой рамки
    detections = sv.Detections.from_ultralytics(result)  # Собираем наши обнаружения
    frame = BoundingBoxAnnotator.annotate(scene=frame, detections=detections)  # Рисуем на кадре наши рамки
    frame = LabelAnnotator.annotate(scene=frame, detections=detections)  # Подписываем на рисунке наши рамки
    cv2.imwrite(f"{dir_path}/{img_name}", frame)  # Записываем нашу картинку по следующему пути
    return img_name, modelnames  # Возвращаем название картинки и название обнаружений


if __name__ == "__main__":
    main()
