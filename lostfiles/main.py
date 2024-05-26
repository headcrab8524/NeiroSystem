from ultralytics import YOLO
import cv2
import supervision as sv
from datetime import date, datetime
import json


def main():

    model = YOLO("yolov8m.pt")
    data = []
    break_times = ["10:00", "11:40", "13:20", "15:30", "17:10", "18:50", "20:30"]
    file = open("КорпусИАудитория.txt")
    kor_aud = file.readline()
    file.close()
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        #if (current_time in break_times): # Это нужно впринципе, но на показе лучше не использовать
        img_name, item_names = neiro_work(model)
        if item_names.__len__()>0:
            for i in item_names:
                data.append({ "img_path": img_name,
                            "item_name": i,
                             "date":str(date.today()) + "-" + current_time,
                             "aud" : kor_aud,
                    })
                with open(f"{kor_aud}.json", "w") as file:
                    json.dump(data, file)
        break


def neiro_work(model):
    cap = cv2.VideoCapture(0)
    now = datetime.now()
    modelnames = []
    current_time = now.strftime("%H-%M-%S")
    img_name = "./" + str(date.today()) + "-" + current_time + ".png"
    BoundingBoxAnnotator = sv.BoundingBoxAnnotator(
        thickness=2,
    )
    LabelAnnotator = sv.LabelAnnotator(
        text_thickness=2,
        text_scale=1
    )

    ret, frame = cap.read()
    result = model(frame)[0]
    for r in result:
        boxes = r.boxes
        for box in boxes:
            c = box.cls
            # if (model.names[int(c)] == "person"):
            #     modelnames.clear()
            #     break
            print(model.names[int(c)])
            modelnames.append(model.names[int(c)])
    detections = sv.Detections.from_ultralytics(result)
    frame = BoundingBoxAnnotator.annotate(scene=frame, detections=detections)
    frame = LabelAnnotator.annotate(scene=frame, detections=detections)
    cv2.imwrite(img_name, frame)
    return img_name, modelnames


if __name__ == "__main__":
    main()
