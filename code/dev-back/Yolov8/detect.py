import os
import sys
sys.path.append('.')
from ultralytics import YOLO
from PIL import Image
from datetime import datetime
import json
# # 加载模型
# model = YOLO('train_best/weights/best.pt')  # 预训练的 YOLOv8n 模型



def detect_img2json(img,path='/root/dev-back/Yolov8/runs/detect'):
    model = YOLO('train_best/weights/best.pt')
    # 命名json文件
    json_file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".json"

    result = model(img)
    # print(result)
    for r in result:
        data = r.tojson()
        # print(json)
    file_path = os.path.join(path, json_file_name)
    # os.makedirs(file_path)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)
    return file_path



def img2json(img,path='/root/dev-back/static/output-infer/YOLOv8-n'):
    model = YOLO('/root/dev-back/Yolov8/train_best/weights/best.pt')
    current_time = datetime.now()
    # 命名json文件
    json_file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".json"
    
    result = model(img)
    # print(result)
    for r in result:
        data = r.tojson()
        # print(json)
    file_path = os.path.join(path, json_file_name)
    # os.makedirs(file_path)
    print("test1.....")
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)
    print("test2.....")
    return file_path

def detect_img2img(img,path='/root/dev-back/Yolov8/runs/detect'):
    model = YOLO('train_best/weights/best.pt')
    img_file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
    result = model(img)
    file_path = os.path.join(path, img_file_name)
    # print(result)
    for r in result:
        im_array = r.plot()
        im = Image.fromarray(im_array[..., ::-1])
        im.save(file_path)
    return file_path

def img2img(img,path='/root/dev-back/static/output-infer/YOLOv8-n'):
    model = YOLO('/root/dev-back/Yolov8/train_best/weights/best.pt')
    current_time = datetime.now()
    img_file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
    result = model(img)
    file_path = os.path.join(path, img_file_name)
    # print(result)
    for r in result:
        im_array = r.plot()
        im = Image.fromarray(im_array[..., ::-1])
        im.save(file_path)
    return file_path


def detect_video2video(video,path='/root/dev-back/static/output-video-infer/YOLOv8-n'):
    data_list = []
    current_time = datetime.now()
    model = YOLO('/root/dev-back/Yolov8/train_best/weights/best.pt')
    video_file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".mp4"
    file_path = os.path.join(path, video_file_name)
    results = model(video, stream=True)
    for r in results:
         im_array = r.plot()
        #  print(im_array.shape)
         data_list.append(im_array)
         im = Image.fromarray(im_array[..., ::-1])
        #  im.save(file_path)
    frame_width, frame_height = data_list[0].shape[1], data_list[0].shape[0]
    # print(frame_width,frame_height)
    video_writer = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc(*'mp4v'), 20, (frame_width, frame_height))
    for data in data_list:
    # 将数组转换为图片
         img = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
         # 写入视频帧
         video_writer.write(img)
    # 释放资源
    video_writer.release()

    return file_path



# if __name__=="__main__":
    # directory = 'D:\\engine\\python\\python_projects\\yolov8_n\\runs\\detect'
    # current_time = datetime.now()
    # img_path = "picture_test/005.jpg"
    # img_file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
    
    # r=detect_img2json(img_path,directory)
    # r = detect_img2img(img_path)
    # print(r)
