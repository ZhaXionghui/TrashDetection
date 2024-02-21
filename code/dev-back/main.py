from flask import Flask, request
from flask_cors import CORS
import pandas as pd

import requests
import json
import os
import sys

import time
'''
'code': 0,
'msg': '登录成功',

'code': 0,
'msg': '数据存在',

'code': 0,
'msg': '注册成功',

状态码
'code': 4000,
'msg': '用户名错误'

'code': 4001,
'msg': '密码错误'

'code': 4002,
'msg': '用户名不存在'

'code':4003,
'msg': '注册用户名已存在'

'code': 4004,
'msg': '确认密码错误'

'code': 4005,
'msg': '答案错误'

'''
# FB 为前后端交互部分
# DB 为后端与数据库交互部分


app = Flask(__name__)
# 设置可以跨域访问
CORS(app, supports_credentials=True)

# 图片部分
@app.route('/Inference', methods=['POST'])
def Inference():
    # 获取客户端数据
    method = request.json.get('method')
    print(method)
    # 读取static文件夹下的最新图片
    files = os.listdir(os.path.join(os.getcwd(), 'static'))
    files.sort(key=lambda fn: os.path.getmtime(os.path.join(os.getcwd(), 'static', fn)))
    print(files)
    imgname = files[-1]
    print(imgname)
    # save the image
    current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    imgpath = os.path.join(os.getcwd(),'static', '{}'.format(imgname))
    # print(imgpath)
    try:
        print('收到一条推理测试请求')
        output_dir = os.path.join(os.getcwd(), 'static', 'output-infer', method, current_time)
        print(output_dir)
        # 1.调用Picodet-xs
        if method == "Picodet-xs":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/picodet_xs_416_coco_lcnet --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, current_time, file)
            for file in os.listdir(output_dir):
                if file.endswith(('jpg','png','jpeg','bmp','.webp')):
                    infer_img = os.path.join('static', 'output-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            } 
        # 2.调用Picodet-s
        elif method == "Picodet-s":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/picodet_s_320_coco_lcnet --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, current_time, file)
            for file in os.listdir(output_dir):
                if file.endswith(('jpg','png','jpeg','bmp','.webp')):
                    infer_img = os.path.join('static', 'output-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
        # 3.调用PP-YOLO-Tiny
        elif method == "PP-YOLO-Tiny":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyolo_tiny_650e_coco --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, current_time, file)
            for file in os.listdir(output_dir):
                if file.endswith(('jpg','png','jpeg','bmp','.webp')):
                    infer_img = os.path.join('static', 'output-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
        # 4.调用PP-YOLO-MobileNetV3-s
        elif method == "PP-YOLO-MobileNetV3-s":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyolo_mbv3_small_coco --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, current_time, file)
            for file in os.listdir(output_dir):
                if file.endswith(('jpg','png','jpeg','bmp','.webp')):
                    infer_img = os.path.join('static', 'output-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
        # 5.调用PP-YOLOE-crn-s
        elif method == "PP-YOLOE-crn-s":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyoloe_crn_s_400e_coco --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, current_time, file)
            for file in os.listdir(output_dir):
                if file.endswith(('jpg','png','jpeg','bmp','.webp')):
                    infer_img = os.path.join('static', 'output-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
        # 6.调用PP-YOLOE-crn-l
        elif method == "PP-YOLOE-crn-l":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyoloe_crn_l_300e_coco --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, current_time, file)
            for file in os.listdir(output_dir):
                if file.endswith(('jpg','png','jpeg','bmp','.webp')):
                    infer_img = os.path.join('static', 'output-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
        # 7.调用PP-YOLOE-plus-crn-s
        elif method == "PP-YOLOE-plus-crn-s":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyoloe_plus_crn_s_80e_coco --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, current_time, file)
            for file in os.listdir(output_dir):
                if file.endswith(('jpg','png','jpeg','bmp','.webp')):
                    infer_img = os.path.join('static', 'output-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
        # 8.调用PP-YOLOv2
        elif method == "PP-YOLOv2":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyolov2_r50vd_dcn_365e_coco --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, current_time, file)
            for file in os.listdir(output_dir):
                if file.endswith(('jpg','png','jpeg','bmp','.webp')):
                    infer_img = os.path.join('static', 'output-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
        # 9.调用YOLOX-Tiny
        elif method == "YOLOX-Tiny":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/yolox_tiny_300e_coco --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, current_time, file)
            for file in os.listdir(output_dir):
                if file.endswith(('jpg','png','jpeg','bmp','.webp')):
                    infer_img = os.path.join('static', 'output-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
        # 10.调用YOLOX-cdn-Tiny
        elif method == "YOLOX-cdn-Tiny":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/yolox_cdn_tiny_300e_coco --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, current_time, file)
            for file in os.listdir(output_dir):
                if file.endswith(('jpg','png','jpeg','bmp','.webp')):
                    infer_img = os.path.join('static', 'output-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
            
    except Exception as e:
        return {
            'code': 4001,
            'data': {
                'msg': str(e)
            }
        }

@app.route('/modelinfer', methods=['POST'])
def modelinfer():
    """
    获取客户端数据并保存图片。

    :return: 返回包含数据的字典。
    :rtype: dict
    """
    # 获取客户端数据
    method = request.json.get('method')
    imgURL = request.json.get('imgURL')
    print(method)
    print(imgURL)
    # save the image
    img = requests.get(imgURL)
    imgname = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    imgpath = os.path.join(os.getcwd(),'static', '{}.jpg'.format(imgname))
    print(imgpath)
    with open(imgpath, 'wb') as f:
        response = requests.get(imgURL)
        f.write(response.content)
    try:
        print('收到一条推理测试请求')
        output_dir = os.path.join(os.getcwd(), 'static', 'output-infer', method, imgname)
        print(output_dir)
        # 1.调用Picodet-xs
        if method == "Picodet-xs":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/picodet_xs_416_coco_lcnet --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, imgname, file)
            for file in os.listdir(output_dir):
                if file.endswith('.jpg'):
                    infer_img = os.path.join('static', 'output-infer', method, imgname, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            } 
        # 2.调用Picodet-s
        elif method == "Picodet-s":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/picodet_s_320_coco_lcnet --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, imgname, file)
            for file in os.listdir(output_dir):
                if file.endswith('.jpg'):
                    infer_img = os.path.join('static', 'output-infer', method, imgname, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
        # 3.调用PP-YOLO-Tiny
        elif method == "PP-YOLO-Tiny":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyolo_tiny_650e_coco --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, imgname, file)
            for file in os.listdir(output_dir):
                if file.endswith('.jpg'):
                    infer_img = os.path.join('static', 'output-infer', method, imgname, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
        # 4.调用PP-YOLO-MobileNetV3-s
        elif method == "PP-YOLO-MobileNetV3-s":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyolo_mbv3_small_coco --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, imgname, file)
            for file in os.listdir(output_dir):
                if file.endswith('.jpg'):
                    infer_img = os.path.join('static', 'output-infer', method, imgname, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
        # 5.调用PP-YOLOE-crn-s
        elif method == "PP-YOLOE-crn-s":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyoloe_crn_s_400e_coco --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, imgname, file)
            for file in os.listdir(output_dir):
                if file.endswith('.jpg'):
                    infer_img = os.path.join('static', 'output-infer', method, imgname, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
        # 6.调用PP-YOLOE-crn-l
        elif method == "PP-YOLOE-crn-l":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyoloe_crn_l_300e_coco --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, imgname, file)
            for file in os.listdir(output_dir):
                if file.endswith('.jpg'):
                    infer_img = os.path.join('static', 'output-infer', method, imgname, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
        # 7.调用PP-YOLOE-plus-crn-s
        elif method == "PP-YOLOE-plus-crn-s":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyoloe_plus_crn_s_80e_coco --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, imgname, file)
            for file in os.listdir(output_dir):
                if file.endswith('.jpg'):
                    infer_img = os.path.join('static', 'output-infer', method, imgname, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
        # 8.调用PP-YOLOv2
        elif method == "PP-YOLOv2":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyolov2_r50vd_dcn_365e_coco --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, imgname, file)
            for file in os.listdir(output_dir):
                if file.endswith('.jpg'):
                    infer_img = os.path.join('static', 'output-infer', method, imgname, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
        # 9.调用YOLOX-Tiny
        elif method == "YOLOX-Tiny":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/yolox_tiny_300e_coco --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, imgname, file)
            for file in os.listdir(output_dir):
                if file.endswith('.jpg'):
                    infer_img = os.path.join('static', 'output-infer', method, imgname, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
        # 10.调用YOLOX-cdn-Tiny
        elif method == "YOLOX-cdn-Tiny":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/yolox_cdn_tiny_300e_coco --image_file={} --device=CPU --save_images=True --save_results --output_dir={}'.format(imgpath, output_dir))
            # 遍历output_dir下的文件，找到json文件
            for file in os.listdir(output_dir):
                if file.endswith('.json'):
                    infer_json = os.path.join('static', 'output-infer', method, imgname, file)
            for file in os.listdir(output_dir):
                if file.endswith('.jpg'):
                    infer_img = os.path.join('static', 'output-infer', method, imgname, file)
            return {
                'code': 0,
                'data': {
                    'infer_img': infer_img,
                    'infer_json': infer_json
                }
            }
            
    except Exception as e:
        return {
            'code': 4001,
            'data': {
                'msg': str(e)
            }
        }

@app.route('/Upload', methods=['POST'])
def Upload():
    # 获取前端上传form-data格式的文件
    # print('get request')
    files = request.files['demo[]']
    # print(type(files))
    # print(files)
    # 保存图片文件
    # print(files.filename)
    # print(os.path.join('./static', files.filename))
    # files.save(os.path.join('./static', files.filename))
    # save the image
    imgname = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    imgtype = files.filename.split('.')[-1]
    imgpath = os.path.join(os.getcwd(),'static', '{}.{}'.format(imgname,imgtype))
    files.save(imgpath)
    print("save image to {}".format(imgpath))

    return {
        'code': 0,
        'data': {
            'msg': '上传成功'
        }
    }

# 视频部分
@app.route('/VideoInference', methods=['POST'])
def VideoInference():
    # 获取客户端数据
    method = request.json.get('method')
    print(method)
    # 读取static文件夹下的最新视频
    files = os.listdir(os.path.join(os.getcwd(), 'static', 'video'))
    files.sort(key=lambda fn: os.path.getmtime(os.path.join(os.getcwd(), 'static', 'video', fn)))
    print(files)
    videoname = files[-1]
    print(videoname)
    
    # img = requests.get(imgURL)
    current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    video_path = os.path.join(os.getcwd(),'static','video', '{}'.format(videoname))
    # print(imgpath)
    try:
        print('收到一条推理测试请求')
        output_dir = os.path.join(os.getcwd(), 'static', 'output-video-infer', method, current_time)
        print(output_dir)
        # 1.调用Picodet-xs
        if method == "Picodet-xs":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/picodet_xs_416_coco_lcnet --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            } 
        # 2.调用Picodet-s
        elif method == "Picodet-s":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/picodet_s_320_coco_lcnet --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        # 3.调用PP-YOLO-Tiny
        elif method == "PP-YOLO-Tiny":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyolo_tiny_650e_coco --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        # 4.调用PP-YOLO-MobileNetV3-s
        elif method == "PP-YOLO-MobileNetV3-s":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyolo_mbv3_small_coco --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        # 5.调用PP-YOLOE-crn-s
        elif method == "PP-YOLOE-crn-s":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyoloe_crn_s_400e_coco --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        # 6.调用PP-YOLOE-crn-l
        elif method == "PP-YOLOE-crn-l":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyoloe_crn_l_300e_coco --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        # 7.调用PP-YOLOE-plus-crn-s
        elif method == "PP-YOLOE-plus-crn-s":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyoloe_plus_crn_s_80e_coco --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        # 8.调用PP-YOLOv2
        elif method == "PP-YOLOv2":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyolov2_r50vd_dcn_365e_coco --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        # 9.调用YOLOX-Tiny
        elif method == "YOLOX-Tiny":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/yolox_tiny_300e_coco --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        # 10.调用YOLOX-cdn-Tiny
        elif method == "YOLOX-cdn-Tiny":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/yolox_cdn_tiny_300e_coco --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
            
    except Exception as e:
        return {
            'code': 4001,
            'data': {
                'msg': str(e)
            }
        }

@app.route('/modelinfervideo', methods=['POST'])
def modelinfervideo():
    # 获取客户端数据
    method = request.json.get('method')
    videoURL = request.json.get('videoURL')
    print(videoURL)
    # save the video
    # img = requests.get(imgURL)
    current_time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    # imgpath = os.path.join(os.getcwd(),'static', '{}.jpg'.format(imgname))
    # print(imgpath)
    # with open(imgpath, 'wb') as f:
    #     response = requests.get(imgURL)
    #     f.write(response.content)
    video_path = os.path.join(os.getcwd(),'static', 'video', videoURL.split('/')[-1])
    # with open(video_path, 'wb') as f:
    #     response = requests.get(videoURL)
    #     f.write(response.content)
    print(video_path)
    try:
        print('收到一条推理测试请求')
        output_dir = os.path.join(os.getcwd(), 'static', 'output-video-infer', method, current_time)
        print(output_dir)
        # 1.调用Picodet-xs
        if method == "Picodet-xs":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/picodet_xs_416_coco_lcnet --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            } 
        # 2.调用Picodet-s
        elif method == "Picodet-s":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/picodet_s_320_coco_lcnet --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        # 3.调用PP-YOLO-Tiny
        elif method == "PP-YOLO-Tiny":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyolo_tiny_650e_coco --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        # 4.调用PP-YOLO-MobileNetV3-s
        elif method == "PP-YOLO-MobileNetV3-s":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyolo_mbv3_small_coco --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        # 5.调用PP-YOLOE-crn-s
        elif method == "PP-YOLOE-crn-s":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyoloe_crn_s_400e_coco --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        # 6.调用PP-YOLOE-crn-l
        elif method == "PP-YOLOE-crn-l":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyoloe_crn_l_300e_coco --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        # 7.调用PP-YOLOE-plus-crn-s
        elif method == "PP-YOLOE-plus-crn-s":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyoloe_plus_crn_s_80e_coco --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        # 8.调用PP-YOLOv2
        elif method == "PP-YOLOv2":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/ppyolov2_r50vd_dcn_365e_coco --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        # 9.调用YOLOX-Tiny
        elif method == "YOLOX-Tiny":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/yolox_tiny_300e_coco --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        # 10.调用YOLOX-cdn-Tiny
        elif method == "YOLOX-cdn-Tiny":
            os.system('python ./PaddleDetection/deploy/python/infer.py --model_dir=./PaddleDetection/output_inference/yolox_cdn_tiny_300e_coco --video_file={} --device=CPU --save_results --output_dir={}'.format(video_path, output_dir))
            # 遍历output_dir下的文件，找到mp4文件
            for file in os.listdir(output_dir):
                if file.endswith('.mp4'):
                    infer_video = os.path.join('static', 'output-video-infer', method, current_time, file)
            return {
                'code': 0,
                'data': {
                    'infer_video': infer_video
                }
            }
        
    except Exception as e:
        return {
            'code': 4001,
            'data': {
                'msg': str(e)
            }
        }

@app.route('/UploadVideo', methods=['POST'])
def UploadVideo():
    # 获取前端上传form-data格式的文件
    print('get video upload request')
    files = request.files['demo[]']
    # print(type(files))
    # print(files)
    # 保存图片文件
    # print(files.filename)
    # print(os.path.join('./static', files.filename))
    # files.save(os.path.join('./static', files.filename))
    # save the image
    videoname = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    videotype = files.filename.split('.')[-1]
    videopath = os.path.join(os.getcwd(),'static','video', '{}.{}'.format(videoname,videotype))
    files.save(videopath)
    print("save video to {}".format(videopath))

    return {
        'code': 0,
        'data': {
            'msg': '上传成功'
        }
    }


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=5000,debug=True)