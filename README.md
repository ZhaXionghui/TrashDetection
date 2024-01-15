# 实验报告1- 轻量型检测模型的对比实验

> 本次轻量型检测模型的对比实验中，我们小组先从百度飞桨PaddleDetection库中，选取了符合项目未来需求的所有轻量型检测模型进行调参训练，并论文中的模型进行对比。同时，由于百度飞桨平台提供的轻量模型有限，我们还尝试了PaddleDetection库中一些较为轻量的模型，并对比了参数、性能等指标。在PaddleDetection库之外，我们尝试了一些最新的目标检测模型，包括YOLOv8系列模型。
>
> 在训练模型并对比模型后，我们发现Picodet模型在各项指标上均优于论文中的模型；NanoDet、PP-YOLO-Tiny等其他模型在参数量小幅增加的情况下，其性能（mAP）高于论文中所给指标。

具体部署及技术细节请参照

`传送门`：[实验报告1- 轻量型检测模型的对比实验](docs/task1/README.md)



## 模型性能对比

| 模型(论文)            | 参数量（MB）    | $mAP_{0.5:0.95}(\%)$ | $mAP_{0.5}(\%)$ | 轮次 |
| --------------------- | --------------- | -------------------- | --------------- | ---- |
| yolox-nano            | 0.8971          | 75.77                | 96.7            | 300  |
| yolox-nano(+CSA)      | 0.8983(+0.0012) | 76.4(+0.63)          | 97.0(+0.3)      | 300  |
| yolov4-tiny           | 5.8787          | 68.12                | 96.71           | 300  |
| yolov4-tiny（DP）     | 5.5409(-0.3378) | 65.23(-2.89)         | 94.35(-2.36)    | 300  |
| yolov4-tiny（DP+CSA） | 5.5413(-0.3374) | 65.42(-2.70)         | 94.67(-2.04)    | 300  |

| 模型                      | 参数量（MB） | $mAP_{0.5:0.95}(\%)$ | $mAP_{0.5}(\%)$ | 轮次 | FPS     | 硬件               |
| ------------------------- | ------------ | -------------------- | --------------- | ---- | ------- | ------------------ |
| Picodet-xs                | 0.674        | 82.1                 | 97.3            | 450  | 86.260  | GPU:RTX3060 laptop |
| NanoDet                   | 0.950        | 78.4                 | 97.7            | 130  | 97.752  | CPU:Intel-i9-32核  |
| PP-YOLO-Tiny              | 0.997        | 59.7                 | 91.0            | 90   | 119.670 | GPU:RTX3060 laptop |
| Picodet-s                 | 1.157        | 80.4                 | 97.3            | 200  | 137.482 | GPU:Tesla V100     |
| PP-YOLO_MobileNetV3_small | 2.542        | 58                   | 89.8            | 300  | 129.639 | GPU:Tesla V100     |
| YOLOv8n                   | 3.200        | 98.8                 | 99.0            | 150  | 344.828 | GPU:RTX4060 laptop |
| YOLOX-cdn-tiny            | 5.010        | 56.4                 | 90.9            | 100  | 78.860  | GPU:Tesla V100     |
| YOLOX-tiny                | 5.033        | 54.8                 | 89.0            | 100  | 58.857  | GPU:Tesla V100     |
| PP-ShiTuv2-det            | 7.045        | 76.3                 | 90.4            | 100  | 43.256  | GPU:Tesla V100     |
| PP-YOLOE_plus_crn_s       | 7.619        | 88                   | 98.8            | 100  | 21.950  | GPU:RTX3060 laptop |
| PP-YOLOE_crn_s            | 7.619        | 73.3                 | 92.2            | 100  | 52.122  | GPU:Tesla V100     |
| RT-DETR_HGNetV2_I         | 32.812       | 78.7                 | 91.3            | 100  | 45.228  | GPU:Tesla V100     |
| PP-YOLOE_plus_crn_l       | 53.147       | 85.8                 | 97.1            | 10   | 31.770  | GPU:RTX3060 laptop |
| PP-YOLOE                  | 53.147       | 55.4                 | 91.6            | 100  | 37.349  | GPU:Tesla V100     |
| PP-YOLOv2                 | 54.165       | 72.3                 | 94.4            | 100  | 37.288  | GPU:Tesla V100     |



#### 🖥️服务器端模型性能对比

各模型结构和骨干网络的代表模型在COCO数据集上精度mAP和单卡Tesla V100上预测速度(FPS)对比图。

[![img](./images/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A1-%20%E8%BD%BB%E9%87%8F%E5%9E%8B%E6%A3%80%E6%B5%8B%E6%A8%A1%E5%9E%8B%E7%9A%84%E5%AF%B9%E6%AF%94%E5%AE%9E%E9%AA%8C/206434766-caaa781b-b922-481f-af09-15faac9ed33b.png)](https://user-images.githubusercontent.com/61035602/206434766-caaa781b-b922-481f-af09-15faac9ed33b.png)

#### ⌚️移动端模型性能对比

各移动端模型在COCO数据集上精度mAP和高通骁龙865处理器上预测速度(FPS)对比图。

[![img](./images/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A1-%20%E8%BD%BB%E9%87%8F%E5%9E%8B%E6%A3%80%E6%B5%8B%E6%A8%A1%E5%9E%8B%E7%9A%84%E5%AF%B9%E6%AF%94%E5%AE%9E%E9%AA%8C/206434741-10460690-8fc3-4084-a11a-16fe4ce2fc85.png)](https://user-images.githubusercontent.com/61035602/206434741-10460690-8fc3-4084-a11a-16fe4ce2fc85.png)



# 实验报告2- 基于生成模型的数据增强

> 本次的数据增强主要采用Stable Diffusion，基于Stable Diffusion我们利用其文生图，图生图的能力生成了不同程度的下雪，下雨，沙尘暴，雾霾等多种不同天气的数据。于此同时，我们也在夜晚条件下，通过ControlNet获得不同光照情况下生成的数据。为了获得更加逼真的正在下雨效果我们也尝试了一些其他的方法，这里我们采用了基于雨线模型的数据增强以获得更为逼真的正在下雨时的图片数据。总共生成数万张新的数据。
> 
> 我们在给出了相应的生成参数的同时也对与Stable Diffusion相关的生成对抗网络（Generative Adversarial Network ，GAN），变分自编码器（Variational autoencoder，VAE），潜在扩散模型（Latent Diffusion Models，LDMs）的一些基础内容以及基于雨线模型的数据增强做了讲解。
>
> 我们还对数据标注的原理与方法进行了较为详细的讲解，并进行了完整操作流程的演示。

具体参数及技术细节请参照

`传送门`：[实验报告2- 基于生成模型的数据增强](docs/task2/README.md)

以下是部分生成的图片展示

### 天气状态

#### 下雨（不同程度的）

<center class="half">
<img src="./images/QQ图片20240114173328.jpg" width=300/>
<img src="./images/QQ图片20240114173341.jpg" width=300/>
<img src="./images/QQ图片20240114173345.jpg" width=300/>
<img src="./images/QQ图片20240114173349.jpg" width=300/>
<img src="./images/QQ图片20240114173353.jpg" width=300/>
</center>

<div>
<center class="one">
<img src="./images/3.png" alt="3" width=300 />
<img src="./images/4.png" alt="4" width=300 />
</center>
</div>
#### 下雪（不同程度的）

<center class="half">
<img src="./images/QQ图片20240114173357.jpg" width=300/>
<img src="./images/QQ图片20240114173401.jpg" width=300/>
<img src="./images/QQ图片20240114173404.jpg" width=300/>
<img src="./images/QQ图片20240114173408.jpg" width=300/>
<img src="./images/QQ图片20240114173411.jpg" width=300/>
</center>


![image-20240113201648520](./images/image-20240113201648520.png)


#### 沙尘暴

<center class="half">
<img src="./images/QQ图片20240114173414.jpg" width=300/>
<img src="./images/QQ图片20240114173417.jpg" width=300/>
<img src="./images/QQ图片20240114173421.jpg" width=300/>
<img src="./images/QQ图片20240114173424.jpg" width=300/>
<img src="./images/01388-4109244131-outdoors,_lora_garbage city_v1_0.6_,ruanyi042,no humans,(masterpiece_1.2),best quality,highres,extremely detailed CG,perfect lig.png" width=300/>
</center>

#### 雾/雾霾

<center class="half">
<img src="./images/QQ图片20240114173427.jpg" width=300/>
<img src="./images/QQ图片20240114173431.jpg" width=300/>
<img src="./images/QQ图片20240114173435.jpg" width=300/>
<img src="./images/QQ图片20240114173438.jpg" width=300/>
<img src="./images/QQ图片20240114173441.jpg" width=300/>
</center>


### 光线状态

#### 较暗、傍晚、路灯（或其它灯光）等


![image4](./images/image4.png)