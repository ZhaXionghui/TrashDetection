## This project includes explanation videos, with experimental reports and code also open-sourced on the Gitee platform. Below are the related links, with all videos hosted on the bilibili video platform:

### Gitee: [https://gitee.com/ZhaXionghui/TrashDetection](https://gitee.com/ZhaXionghui/TrashDetection)

### 1. Video: [【基于轻量型模型的垃圾桶满溢识别检测——论文讲解与代码的讲解和运行】](https://www.bilibili.com/video/BV16u4y1h76eAI)
**Paper Explanation**: 《基于轻量型卷积神经网络的垃圾桶满溢识别及应用》

The first half of the video provides a detailed explanation of the paper, covering:
- Research background
- Overview of related techniques
- Dataset establishment
- Hybrid attention mechanism
- Integration with traditional object detection
- Deployment efforts

The second half focuses on the code explanation:
- Detailed walkthrough of network module implementation.
- Debugging and successful execution of the author's code.
- Local deployment verification to ensure feasibility.

---

### 2. Video: [【基于轻量型模型的垃圾桶满溢识别检测——轻量型模型对比实验】](https://www.bilibili.com/video/BV12b4y1N7bZ)  
**AI Studio Experimental Report**: [https://aistudio.baidu.com/projectdetail/7184259](https://aistudio.baidu.com/projectdetail/7184259)

This video compares dozens of object detection models available in Baidu Paddle, as well as newer models like YOLOv8 and lightweight models outside the Paddle series. Key highlights include:
- **Performance**: Picodet outperformed the metrics provided in the paper across various indicators.
- **Deployments**: Explained deployments on multiple platforms, including AI Studio BML code, PaddleX, local environments, Docker, and Sugon.

**Selected Models**:
- NanoDet, Picodet-s, Picodet-xs
- PP-YOLOv2, PP-YOLO_MobileNetV3_small, PP-YOLO-Tiny
- PP-YOLOE, PP-YOLOE_crn_s, PP-YOLOE_plus_crn_s, PP-YOLOE_plus_crn_l
- YOLOv8n, YOLOX-tiny, YOLOX-cdn-tiny
- PP-ShiTuv2-det, RT-DETR_HGNetV2_I

---

### 3. Video: [【基于轻量型模型的垃圾桶满溢识别检测——基于生成模型的数据增强】](https://www.bilibili.com/video/BV1nK4y1q7hB)  
**Gitee**: [https://gitee.com/ZhaXionghui/TrashDetection](https://gitee.com/ZhaXionghui/TrashDetection)

Data augmentation was performed using Stable Diffusion to generate datasets with various weather conditions, including:
- Snow, rain, sandstorms, smog, and nighttime scenarios under different lighting conditions.
- Rain streak models for realistic rainy-day data.

A total of tens of thousands of new images were generated. The video explains:
- Relevant knowledge
- Data annotation principles
- Demonstration of the entire workflow

---

### 4. Video: [【基于轻量型模型的垃圾桶满溢识别检测——服务器模型部署及应用】](https://www.bilibili.com/video/BV1TA4m1G745)  
**Gitee**: [https://gitee.com/ZhaXionghui/TrashDetection/blob/master/docs/task3/README.md](https://gitee.com/ZhaXionghui/TrashDetection/blob/master/docs/task3/README.md)

The server uses Alibaba Cloud’s lightweight application server with CentOS 7.6 OS. Deployment details:
- **Frontend**: Built with vite+vue3 toolchain, locally validated, and deployed using nginx for reverse proxy.
- **Backend**: Flask framework for server-side deployment.

**Key Features**:
1. **Model Selection**: Users can choose inference models.
2. **Image Inference**:
   - Upload custom images or select default ones.
   - Images are uploaded to the server, inferred, and results are returned.
3. **Video Inference**:
   - Upload custom videos or select default ones.
   - Videos are processed and results are returned for download.
   - Note: Video inference is CPU-intensive. Videos longer than 5 seconds may take considerable time. For example, using Picodet, a 5-second video inference takes about 1 minute.
4. **Webpage Features**: Users can adjust styles and modes.

---

### Summary of LLM Survey
Our team collaboratively reviewed numerous papers on large language models (LLMs), culminating in a comprehensive survey. It covers detailed analyses of:
- **LLM design and architecture**
- **Datasets, training, and fine-tuning**
- **Applications, capability evaluation, and challenges**

Additionally, an optimization experiment with the LLaMA2 70B pre-trained model explored:
- Model parallelism
- Cache optimization
- Flash Attention's role in training
