# 实验报告2- 基于生成模型的数据增强

> 本次的数据生成主要采用Stable Diffusion，基于Stable Diffusion我们利用其文生图，图生图的能力生成了下雪，下雨，沙尘暴，雾霾等多种不同天气的数据，于此同时我们也在夜晚条件下，通过Controlnet获得不同光照情况下生成的数据，生成超万张新的数据。我们给出了相应的生成参数同时也对与Stable Diffusion相关的GAN，VAE，潜在扩散模型（Latent Diffusion Models，LDMs）一些基础内容做了讲解。
>
> 我们还对数据标注的原理与方法进行了较为详细的讲解，并进行了完整操作流程的演示。

<!-- TOC -->

- [实验报告2- 基于生成模型的数据增强](#实验报告2--基于生成模型的数据增强)
  - [生成式深度学习模型](#生成式深度学习模型)
    - [（Generative Adversarial Network	，GAN）](#generative-adversarial-networkgan)
    - [（Variational autoencoder，VAE）](#variational-autoencodervae)
    - [潜在扩散模型（Latent Diffusion Models，LDMs）](#潜在扩散模型latent-diffusion-modelsldms)
      - [方法](#方法)
      - [图片感知压缩（Perceptual Image Compression）](#图片感知压缩perceptual-image-compression)
      - [潜在扩散模型（Latent Diffusion Models）](#潜在扩散模型latent-diffusion-models)
      - [条件机制（Conditioning Mechanisms）](#条件机制conditioning-mechanisms)
  - [数据增强](#数据增强)
    - [天气状态](#天气状态)
      - [下雨（不同程度的）](#下雨不同程度的)
      - [下雪（不同程度的）](#下雪不同程度的)
    - [光线状态](#光线状态)
      - [较暗、傍晚、路灯（或其它灯光）等](#较暗傍晚路灯或其它灯光等)
  - [数据标注——原理与方法](#数据标注原理与方法)
    - [什么是数据标注？](#什么是数据标注)
    - [数据标记的工作原理](#数据标记的工作原理)
    - [有标签数据与无标签数据](#有标签数据与无标签数据)
    - [标注细节（本例+百度EasyData）](#标注细节本例百度easydata)
    - [数据标注优化方法](#数据标注优化方法)
    - [使用场景](#使用场景)
    - [参考链接](#参考链接)

<!-- /TOC -->
## 生成式深度学习模型



### （Generative Adversarial Network	，GAN）



### （Variational autoencoder，VAE）



### 潜在扩散模型（Latent Diffusion Models，LDMs）

[High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752)

- Latent Diffusion Models规避了Diffusion Models的高昂的计算成本，使文图生成能够在消费级GPU上快速生成图片。
- 相比于其它空间压缩方法，论文提出的方法可以生成更细致的图像，并且在高分辨率图片生成任务（如风景图生成，百万像素图像）上表现得也很好。
- 论文还提出了cross-attention的方法来实现多模态训练，使得条件图片生成任务也可以实现。论文中提到的条件图片生成任务包括类别条件图片生成（class-condition）, 文图生成（text-to-image）, 布局条件图片生成（layout-to-image）。这也为日后Stable Diffusion的开发奠定了基础。

#### 方法

> 我们主要来看一下论文High-Resolution Image Synthesis with Latent Diffusion Models的方法部分。

![frame](../../images/article-Figure3-1-1024x508.png)


Latent Diffusion Models整体框架如上图所示，首先需要训练好一个自编码模型（AutoEncoder，包括一个**编码器**$\varepsilon$和一个**解码器** $D$）,这个编码模型将压缩学习阶段与生成学习阶段明确分开以降低计算复杂度。这样一来，我们就可以利用编码模型对图片进行压缩，然后在潜在表示空间上做**扩散操作（Diffusion Process）**，最后我们再用解码器恢复到原始像素空间，论文将这种将高维特征压缩到低维，然后在低维空间上进行操作的方法称之为**感知压缩（Perceptual Compression）**。

在潜在表示空间上做**扩散操作（Diffusion Process）**其主要过程和标准的扩散模型没有太大的区别，所用到的扩散模型的具体实现为 time-conditional UNet。但是有一个重要的地方是论文为diffusion操作引入了**条件机制（Conditioning Mechanisms）**，通过cross-attention的方式来实现多模态训练，使得条件图片生成任务也可以实现。

#### 图片感知压缩（Perceptual Image Compression）

感知压缩通过对所学的空间 $z$ 进行任意的一维排序来对其分布进行自回归建模，从而忽略掉 $z$ 的许多固有结构。引入感知压缩就是说通过VAE这类自编码模型对原图片进行处理，忽略掉图片中的高频信息，只保留重要、基础的一些特征。这种方法，能够大幅降低训练和采样阶段的计算复杂度，让文图生成等任务能够在消费级GPU上快速生成图片。

感知压缩主要利用一个预训练的自编码模型，该模型能够学习到一个在感知上等同于图像空间的潜在表示空间。这种方法的一个优势是只需要训练一个通用的自编码模型，就可以用于不同的扩散模型的训练，在不同的任务上使用。

由此，基于感知压缩的扩散模型的训练本质上是一个**两阶段训练的过程**，第一阶段需要训练一个自编码器，第二阶段才需要训练扩散模型本身。在第一阶段训练自编码器时，为了避免潜在表示空间出现高度的异化，作者尝试了两种正则化方法，一种是KL-reg，另一种是VQ-reg，因此在官方发布的一阶段预训练模型中，会看到KL和VQ两种实现。在Stable Diffusion中主要采用AutoencoderKL这种实现。

具体来说，给定图像$x \in \mathbb{R}^{H \times W \times 3}$ ，我们可以先利用一个编码器 $\varepsilon$ 来将图像编码到潜在表示空间$z=\varepsilon(x)$ ，其中 $z \in \mathbb{R}^{h \times w \times c}$，然后再用解码器从潜在表示空间重建图片$\tilde{x} = D(z) = D(\varepsilon(x))$ 。在感知压缩压缩的过程中，下采样系数的大小为 $f = \frac{H}{h}=\frac{W}{w}$， $f=2^{m},m \in N$ 。

#### 潜在扩散模型（Latent Diffusion Models）

首先看一下普通的**扩散模型（Diffusion Models，DMs）**，它是一种概率模型。可以解释为一个时序去噪自编码器（equally weighted sequence of denoising autoencoders） $\epsilon_{\theta}(x_{t},t);t=1, \cdots ,T$，其目标是根据输入$x_{t}$去预测一个对应去噪后的变体，或者说预测噪音，其中$x_{t}$是输入 $x$ 的噪音版本。相应的目标函数可以写成如下形式：

$$
L_{DM}=\mathbb{E}_{x,t \sim \mathcal{N}(0,1),t}[\parallel \epsilon-\epsilon_{\theta}(z_{t},t) \parallel_{2}^{2}]
$$
其中 $t$从 $\{1,\cdots,T\}$ 中均匀采样获得。

在**潜在扩散模型**中，引入了预训练的感知压缩模型，它包括一个编码器 $\varepsilon$ 和一个解码器 $D$。这样就可以利用在训练时就可以利用编码器得到 $z_{t}$，从而让模型在潜在表示空间中学习，相应的目标函数可以写成如下形式：

$$
L_{LDM} \coloneqq \mathbb{E}_{x,t \sim \mathcal{N}(0,1),t}[\parallel \epsilon-\epsilon_{\theta}(z_{t},t) \parallel_{2}^{2}]
$$

#### 条件机制（Conditioning Mechanisms）

除了无条件图片生成外，我们也可以进行条件图片生成，这主要是通过拓展得到一个条件时序去噪自编码器（conditional denoising autoencoder）$\epsilon_{\theta}(z_{t},t,y)$ 来实现的，这样一来我们就可通过 $y$ 来控制图片合成的过程。具体来说，论文通过在UNet主干网络上增加cross-attention机制来实现$\epsilon_{\theta}(z_{t},t,y)$。为了能够从多个不同的模态预处理 $y$ ，论文引入了一个领域专用编码器（domain specific encoder）$\tau_{\theta}$ ，它用来将 $y$ 映射为一个中间表示 $\tau_{\theta}(y) \in \mathbb{R}^{M \times d_{\tau}}$ ，这样我们就可以很方便的引入各种形态的条件（文本、类别、layout等等）。最终模型就可以通过一个cross-attention层映射将控制信息融入到UNet的中间层，cross-attention层的实现如下：
$$
Attention(Q,K,V) = softmax(\frac{QK^T}{\sqrt{d}} \cdot V), with \\
Q  = W_{Q}^{(i)} \cdot \varphi_{i}(z_{t}),K=W_{K}^{(i)} \cdot \tau_{\theta}(y)
$$


其中 $\varphi_{i}(z_{t}) \in \mathbb{R}^{N \times d_{\epsilon}^{i}}$ 是UNet的一个中间表征。相应的目标函数可以写成如下形式：

$$
L_{LDM} \coloneqq \mathbb{E}_{\varepsilon(x),t \sim \mathcal{N}(0,1),t}[\parallel \epsilon-\epsilon_{\theta}(z_{t},t) \parallel_{2}^{2}]
$$


参考：

https://arxiv.org/abs/2112.10752

https://ommer-lab.com/research/latent-diffusion-models/

https://zhuanlan.zhihu.com/p/582693939

## 数据增强

### 天气状态

#### 下雨（不同程度的）


#### 下雪（不同程度的）

[Heavy snowfall - v1.0 | Stable Diffusion LoRA | Civitai](https://civitai.com/models/219932/heavy-snowfall)

```yaml
snowy,winter,(snowfall in background:1.2),(heavyfall:1.15),snow,very snowy,photorealistic,<lora:snowfall:0.8>,
Negative prompt: Unrealistic,
Steps: 20, Sampler: DPM++ 2M Karras, CFG scale: 7, Seed: 712934690, Size: 500x375, Model hash: fe7578cb5e, Model: realisticVisionV60B1_v60B1VAE, VAE hash: 735e4c3a44, VAE: vae-ft-mse-840000-ema-pruned.safetensors, Denoising strength: 0.34, Clip skip: 2, Lora hashes: "snowfall: f8324b7af7d9", Version: v1.6.0-2-g4afaaf8a
```

重绘幅度:0.34,0.35

![image-20240113201648520](../../images/image-20240113201648520.png)





### 光线状态

#### 较暗、傍晚、路灯（或其它灯光）等





## 数据标注——原理与方法

### 什么是数据标注？

数据标注（或称数据注释）是开发[机器学习](https://www.ibm.com/cn-zh/topics/machine-learning) (ML) 模型时预处理阶段的一部分。 它负责识别原始数据（如图像、文本文件、视频），然后向原始数据添加一个或多个标签，以指定模型的上下文，帮助机器学习模型做出准确的预测。例如，标签可指示相片是否包含鸟或汽车、录音中有哪些词发音，或者 X 影像是否包含肿瘤。各种使用案例都需要用到数据标记，包括计算机视觉、自然语言处理和语音识别。

![](../../images/How%20it%20Works.bc19de267c29570783c4add8bb2286ee584fcfbc.png)

### 数据标记的工作原理

如今最实用的机器学习模型利用的是监督学习，它应用算法以将一个输入映射到一个输出。为了使监督学习发挥作用，我们需要一组带标签的数据，使模型能够从中学习以做出正确的决定。数据标记的起点通常是要求人类就指定的无标签数据做出判断。例如，标记者可能需要为数据集中“相片是否包含鸟”的答案为“是”的所有图片添加标签。添加标签可能像简单的是/否一样粗疏，也可能像识别图片中与鸟相关的像素一样精细。机器学习模型在模型训练的流程中，使用人类提供的标签学习背后的模式。 这样训练过的模型，可用于对新数据进行预测。

在机器学习中，用作客观标准来训练和评估指定模型的正确标记的数据集通常称为“标准答案”。 训练过的模型的准确度将取决于标准答案的准确度，因此付出一些时间和资源来确保高准确度的数据标记至关重要。

### 有标签数据与无标签数据  

- 有标签数据用于[监督式学习](https://www.ibm.com/cn-zh/topics/supervised-learning)， 而无标签数据用于[无监督学习](https://www.ibm.com/cn-zh/topics/unsupervised-learning)。 
- 有标签数据更难以收集和存储（既耗时又费力），而无标签数据更易于收集和存储。
- 有标签数据可用于确定切实可行的洞察（例如预测任务），而无标签数据的用途则比较有限。 无监督学习方法可以帮助发现新的数据聚类，从而能够在添加标签时新建类别。

计算机还可以结合使用这两种数据进行半监督学习，这样可以减少对手动添加数据标签的需求，同时提供添加了注释的大型数据集。

### 标注细节（本例+百度EasyData）

采用矩形框标记，标注的类别主要分三类：**分别是未满溢的垃圾桶、满溢的垃圾桶和垃圾**

- 每个矩形框中指包含一个物体，不可以将两个物体合并标注
- 矩形框的大小不应过大或过小，应刚好框住物体
- 矩形框直接可以重叠
- 如物体漏出面积小于本体30%则可以不标

### 数据标注优化方法

以下方法有助于优化数据标注的准确性和效率：

- **直观、简化的任务界面：**可以最大程度地减轻标签添加人员的认知负荷和背景切换工作。 

- **Consensus：**用于衡量多个标签添加者（人或机器）之间的一致性。 共识分数的计算方法是将相同标签的总数除以每个资产的标签总数。

- **Label auditing：**验证标签的准确性并根据需要进行更新。 

- **Transfer learning：**从一个数据集中获取一个或多个预先训练的模型，并将其应用于另一个数据集。 这包括同时进行的多任务学习。

- **Active learning**：

  一类 ML 算法，属于半监督学习，可帮助人类确定最合适的数据集。 主动学习方法包括：

  - *Membership query synthesis* — 生成综合实例并为其请求标签。 
  - *Pool-based sampling* — 根据信息含量指标对所有无标签的实例进行排名，并选择要注释的最佳查询。
  - *Stream-based selective sampling* — 逐个选择无标签的实例，并根据其信息含量或不确定性添加标签或将其忽略。

*可以利用机器学习模型自动标记数据，以使标记更加高效。在此流程中，先在由人类标记的原始数据子集上训练用于标记数据的机器学习模型。如果标记模型基于其迄今所学的内容认为其结果的置信度较高，则它将自动将标签应用于原始数据。如果标记模型认为其结果置信度较低，它会将数据传递给人工标识器进行标记。然后，将人类生成的标签反馈给标记模型供其从中学习，并提高其自动标记下一组原始数据的能力。随着时间的推移，该模型可以自动标记越来越多的数据，并大大加快创建培训数据集的速度。*

### 使用场景

数据标注有助于在各行各业的多种背景下增强准确性、质量和易用性，比较突出的用例包括：

- **计算机视觉：**在这个人工智能领域，训练数据用于构建计算机视觉模型，以实现图像分割和类别自动化，确定图像中的关键点以及检测对象的位置。 
- **自然语言处理 (NLP)：** AI 的一个分支，将计算语言学与统计、机器学习和深度学习模型相结合，用于识别和标记文本的重要部分，然后生成训练数据，用于情绪分析、实体名称识别和光学字符识别。 NLP 越来越多地用于企业解决方案，如垃圾邮件检测、机器翻译、[语音识别](https://www.ibm.com/cn-zh/topics/speech-recognition)、文本摘要、虚拟助手和聊天机器人以及语音操作的 GPS 系统。 这使得 NLP 成为任务关键型业务流程发展的关键组成部分。
- **音频处理：**音频处理可以将所有类型的声音，例如语音、野生动物噪音（吠声、嚎叫或鸟鸣）和建筑声音（打碎玻璃、扫描或警报），转换成结构化格式，以便用于机器学习。音频处理通常要求首先手动将其转录为书面文本。然后，可以通过添加标签并对音频进行分类，找出关于该音频的更深层的信息。这种经过分类的音频就可以作为训练数据集。

### 参考链接

https://aws.amazon.com/what-is/data-labeling/?nc1=h_ls

https://www.ibm.com/topics/data-labeling

