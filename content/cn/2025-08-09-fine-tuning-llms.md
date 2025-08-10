---
title: '大语言模型微调 (Fine-tuning Large Language Models)'
author: 范叶亮
date: '2025-08-09'
slug: fine-tuning-llms
categories:
  - 深度学习
tags:
  - 微调
  - Fine-tuning
  - 大语言模型
  - LLMs
  - Large Language Models
  - 预训练
  - Pre-training
  - 后训练
  - Post-training
  - 全参数微调
  - Full Fine-tuning
  - 部分参数微调
  - Repurposing
  - 监督微调
  - Supervised Fine-tuning
  - 无监督微调
  - Unsupervised Fine-tuning
  - 指令微调
  - Instruction Fine-tuning
  - 对齐微调
  - Alignment Fine-tuning
  - 参数高效微调
  - Parameter-efficient Fine-tuning
  - Prefix Tuning
  - Prompt Tuning
  - P-Tuning
  - P-Tuning v2
  - LoRA
  - IA3
images:
  - /images/cn/2025-08-09-fine-tuning-llm/parameter-efficient-fine-tuning-methods-taxonomy.avif
---

# 什么是微调

微调（Fine-tuning）是深度学习中迁移学习的一种方法，其将现有模型已经学到的知识作为学习新任务的起点。虽然微调表面上是模型训练中使用的一种技术，但它与传统意义上的“训练”截然不同。为了消除歧义，在这种情况下通常将传统意义上的“训练”称为预训练（Pre-training）。[^ibm-fine-tuning]

与微调类似的另一个概念称之为后训练（Post-training），两者均发生在预训练之后，其目的也都是为了进一步提升模型的效果，通常两者可以理解为相同的概念。从优化的发起人角度出发：当终端用户希望模型可以更好的适配自己的领域知识，则需要进行的操作称之为微调；当模型开发者希望可以更好的将模型与人类的价值、道德和预期保持一致，则需要进行的操作称之为后训练。[^huyen2024ai]

# 为什么微调

从本质上讲，磨练一个预训练基础模型的能力要比从头开始训练一个新模型更容易，也更省钱，因为预训练已经获得了与当前任务相关的广泛知识。对于具有数百万甚至数十亿个参数的深度学习模型尤其如此，例如在自然语言处理（NLP）领域的大语言模型（LLM）或卷积神经网络（CNN）和视觉转换器（ViT）（用于计算机视觉任务，例如图像分类、对象检测或图像分割等）。

通过迁移学习利用先前的模型训练，微调可以减少获得适合特定用例和业务需求的大模型所需的昂贵算力和标记数据量。例如，微调可用于调整预训练大语言模型的对话语气或预训练图像生成模型的图片样式，还可用于使用专有数据或领域特定的专业知识来补充模型的原始训练数据集。

# 如何去微调

微调是需要进一步训练模型的技术，模型的权重已经通过先前的预训练得到了更新。使用基础模型的先前知识作为起点，通过在任务特定的较小数据集上进行训练来对模型进行微调。

虽然从理论上讲，任务特定的数据集都可以用于初始训练，但在小数据集上从头开始训练一个大模型可能会存在过拟合的风险：模型可能会在训练示例中学习得到良好的表现，但对新数据的泛化能力却很差。这会导致模型不适合给定的任务，也违背了模型训练的初衷。 因此，微调可以兼具两者的优势：利用对大量数据进行预训练所获得的广泛知识和稳定性，并训练模型对更详细、更具体概念的理解。

## 微调方法分类

### 参数角度

从参数角度，我们可以将微调分为全参数微调（Full Fine-tuning）和部分参数微调（Repurposing）：

- **全参数微调**：即对模型的所有参数进行微调。这种微调方法通常适用于任务与预训练模型之间存在较大差异的情况。全参数微调需要耗费较大的计算资源和时间，通常可以获得更好的性能，但在数据不足时容易出现过拟合问题。
- **部分参数微调**：即仅对模型的部分参数或额外的模型参数进行微调。相比于全参数微调，部分参数微调可以在较少的计算资源和时间的情况下，在一些特定任务上提高模型的性能。

### 数据角度

从数据角度，我们可以将微调分为监督微调（Supervised Fine-tuning）和无监督微调（Unsupervised Fine-tuning）：

- **监督微调**：在进行微调时使用**有标签**的训练数据集。通过使用这些标签来指导模型的微调，可以使模型更好地适应特定任务。
- **无监督微调**：在进行微调时使用**无标签**的训练数据集。通过学习数据的内在结构或生成数据来进行微调，以提取有用的特征或改进模型的表示能力。

### 方式角度

从方式角度，我们可以将微调划分为指令微调（Instruction Fine-tuning）和对齐微调（Alignment Fine-tuning）：

- **指令微调**：利用格式化的实例以有监督的方式微调大语言模型。通过指令微调不仅可以改善模型的性能，同时也可以增强模型的泛化能力。
- **对齐微调**：为了避免大语言模型的幻觉问题，以及同人类的价值观和偏好对齐，提高伦理表现，将人类整合到模型的训练过程中。例如基于人类对结果的反馈，模型通过强化学习从而与人类对齐。

## 显存消耗

在进行模型微调时我们需要关注显存的消耗，以确保在当前的硬件环境中可以正常进行微调。在进行模型微调时，显存消耗主要同如下因素有关：

- **参数精度**：决定了每个参数占用的实际显存大小，例如 FP32（单精度）占用 4 字节，FP16（半精度）占用 2 字节，INT8 占用 1 字节等。
- **模型参数**：微调所需显存的基础决定因素，例如微调一个 1B 模型，其参数总量则为 10 亿。
- **梯度**：在微调过程中需要存储反向传播计算得到的梯度信息，这部分大小同模型参数相同，精度同训练精度一致。
- **优化器状态**：优化器所需的额外信息，例如动量、方差等，不同的优化器占用的显存大小也不尽相同，保守估计为模型参数所需显存的 4 倍。
- **激活值**：用于储存前向传播过程中的中间结果，所需显存大小主要受到批大小和序列长度的影响，量级相比前面可以忽略不计。

以全参数微调一个 1B 模型为例，所需的显存大致为 12GB（模型参数：2GB，梯度：2GB，优化器状态：8GB）。在使用部分参数微调时，模型参数本身不变，需要微调的参数会大幅度减少，因此梯度和优化器状态所需的显存也会大幅度减少。在应用一些量化技术后，例如使用 INT8 精度进行微调，则所有部分的显存占用均会相应的减少。

## 参数高效微调

> 参数高效微调部分主要参考了 [llm-action](https://github.com/liguodongiot/llm-action) 项目。

参数高效微调（Parameter-Efficient Fine-Tuning）是指固定大部分预训练模型的参数，仅微调少量或额外的模型参数的微调方法，从而可以极大的降低计算成本。参数高效微调可以从方法的角度可以分为三类 [^lialin2023scaling]：引入新参数（Addition-based），微调部分参数（Selection-based）和重参数化（Reparametrization-based），其中引入新参数又可以划分为适配器方法和软提示方法两种。

{{< figure src="/images/cn/2025-08-09-fine-tuning-llm/parameter-efficient-fine-tuning-methods-taxonomy.avif" title="参数高效微调方法分类" >}}

在实战过程中我们可以使用 Huggingface 开源的 [PEFT](https://github.com/huggingface/peft) 扩展库进行参数高效微调，作为 Huggingface 开源项目其可以与 [Transformers](https://github.com/huggingface/transformers)，[Accelerate](https://github.com/huggingface/accelerate) 和 [Diffusers](https://github.com/huggingface/diffusers) 等多个开源库无缝衔接使用。在官方文档中我们可以查看支持的[微调类型](https://huggingface.co/docs/peft/main/en/package_reference/peft_types#peft.PeftType)和[任务类型](https://huggingface.co/docs/peft/main/en/package_reference/peft_types#peft.TaskType)。

### Prefix Tuning

Prefix Tuning [^li2021prefix] 是在输入的 token 前构造与任务相关的 virtual token 作为前缀，在微调的时候仅更新前缀部分的参数。

{{< figure src="/images/cn/2025-08-09-fine-tuning-llm/li2021prefix-1.avif" large-max-width="60%" >}}

针对不同的模型结构，构造的前缀也有所不同：

- **自回归结构**：添加前缀后，得到 $z = \left[\text{PREFIX}; x; y\right]$。
- **编码器-解码器结构**：在编码器和解码器前均添加前缀，得到 $z = \left[\text{PREFIX}; x; \text{PREFIX}'; y\right]$。

{{< figure src="/images/cn/2025-08-09-fine-tuning-llm/li2021prefix-2.avif" >}}

作者发现直接更新前缀的参数会导致训练不稳定，因此在前缀之前添加了 MLP 结构，在训练完成后 MLP 部分的参数无需保留，仅保留前缀的参数即可。同时作者也针对前缀使用多少个 virtual token 以及前缀放置的位置对于微调的性能影响进行了相关实验，细节请参考论文原文。

### Prompt Tuning

Prompt Tuning [^lester2021power] 可以看作是 Prefix Tuning 的简化版本，其为每个任务定义不同的 Prompt，然后拼接到数据上作为输入。

{{< figure src="/images/cn/2025-08-09-fine-tuning-llm/lester2021power-1.avif" >}}

Prompt Tuning 仅在输入层添加 token，不需要像 Prefix Tuning 那样添加 MLP 结构解决训练问题。通过实验发现，随着模型参数的增加，Prompt Tuning 的效果会逼近全参数微调的效果。

实验还发现，与随机和使用样本词汇表的初始化相比，采用类标签初始化的微调效果更好，但随着模型参数的增加，效果差异会消失。同时 Prompt 的 token 长度在 20 左右可以获得不错的效果，同样随着模型参数的增加，token 长度带来的增益会消失。

### P-Tuning

P-Tuning [^liu2021gpt] 将 Prompt 转换为可学习的 Embedding 层，再通过 MLP+LSTM 结构对 Prompt Embedding 进行处理。

{{< figure src="/images/cn/2025-08-09-fine-tuning-llm/liu2021gpt-1.avif" >}}

对比 Prefix Tuning，P-Tuning 增加了可微的 virtual token，但仅作用于输入层，没有在每一层都添加。同时，virtual token 的位置也不一定是前缀，其插入的位置是可选的，目的是将传统人工设计的 Prompt 模板中的真实 token 替换为可微的 virtual token。

实验发现随机初始化 virtual token 容易陷入局部最优，因此通过一个 Prompt Encoder（即 MLP+LSTM 结构）对其进行编码可以获得更好的效果。

### P-Tuning v2

Prompt Tuning 和 P-Tuning 存在如下问题：

- **缺乏规模通用性**：Prompt Tuning 在模型超过 100 亿时可以与全量微调媲美，但对于较小参数的模型与全量微调的效果有很大的差距。
- **缺乏任务普遍性**：Prompt Tuning 和 P-Tuning 在一些 NLU 基准测试中表现出优势，但对序列标注任务的有效性尚未得到验证。
- **缺少深度提示优化**：在 Prompt Tuning 和 P-Tuning 中，提示仅被插入到输入中，后续插入提示位置的嵌入是通过之前层计算得到。这可能导致插入提示对模型最终效果的影响有限，同时由于序列长度限制可调参数的数量也是有限的。

考虑到上述问题，P-Tuning v2 [^liu2021p] 利用深度提示优化（例如：Prefix Tuning）对 Prompt Tuning 和 P-Tuning 进行改进，类似 Prefix Tuning，其在每一层都加入了 Prompt token 作为输入。

{{< figure src="/images/cn/2025-08-09-fine-tuning-llm/liu2021p-1.avif" >}}

P-Tuning v2 还通过移除重参数化编码器、针对不同任务采用不同提示词长度、引入多任务学习、使用传统分类标签范式等方法进行模型改进。实验表明 P-Tuning v2 可以在不同规模和不同任务中实现与全量微调相媲美的效果。

### Adapter Tuning

Adapter Tuning [^houlsby2019parameter] 设计了一个 Adapter 模块，并在每个 Transformer 层中插入两个 Adapter 模块，在微调时仅更新增加的 Adapter 模块和 Layer Norm 层中的参数。

{{< flex >}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-08-09-fine-tuning-llm/houlsby2019parameter-1.avif" large-max-width="60%" middle-max-width="80%" >}}
{{% /flex-item %}}

{{% flex-item %}}
{{< figure src="/images/cn/2025-08-09-fine-tuning-llm/houlsby2019parameter-2.avif" large-max-width="60%" middle-max-width="80%" >}}
{{% /flex-item %}}

{{< /flex >}}

Adapter 模块由两个前馈层和一个非线性层组成。第一个前馈层将 Transformer 的输入从 $d$ 维（高维）映射到 $m$ 维（低维），其中 $m \ll d$。通过控制 $m$ 的大小可以限制 Adapter 模块的参数量。中间通过非线性层后，第二个前馈层再将 $m$ 维映射回 $d$ 维作为 Adapter 模块的输出。同时通过 Skip Connection 将 Adapter 的输入也添加到 Adapter 的输出中，这样可以保证即便 Adapter 最开始的参数值接近 0，通过 Skip Connection 的设置也可以保证训练的有效性。

### LoRA

神经网络包含很多全连接层，其通过矩阵乘法实现。很多全连接层的权重矩阵是满秩的，针对特定任务微调后，模型的权重矩阵其实具有很低的本征秩（intrinsic rank），因此将参数矩阵投影到更小的空间仍可以得到有效的学习。LoRA [^hu2022lora] 的核心思想就是通过低秩分解降低特征矩阵的参数量，从而以较小的参数量来实现大模型的间接训练。

在涉及到矩阵相乘的模块中，在其旁边增加一个新的通路，通过第一个矩阵 $A$ 将维度从 $d$ 降至 $r$，在通过一个矩阵 $B$ 将维度从 $r$ 升回 $d$，其中 $r \ll d$。

{{< figure src="/images/cn/2025-08-09-fine-tuning-llm/hu2022lora-1.avif" large-max-width="30%" middle-max-width="40%" >}}

在微调时，仅更新上述两个矩阵的参数，再将两条通路的结果相加作为最终的结果，即 $h = W_0 x + B A x$。训练时矩阵 $A$ 通过高斯函数初始化，矩阵 $B$ 初始化为零矩阵，这样训练开始时 $B A = 0$，从而可以确保新的通路对模型的结果没有影响。

在 Attention 模块中，权重矩阵包括用于计算 Q，K，V 的 $W_q$，$W_k$，$W_v$ 以及多头注意力的 $W_o$，实验表明保证权重矩阵的种类数量比增加秩 $r$ 的大小更为重要，通常情况下 $r$ 选择 4，8，16 即可。

### IA3

IA3 [^liu2022few] 不同于 LoRA 学习低秩权重，而是通过学习向量（$l_k$，$l_v$，$l_{ff}$）对模型的部分参数进行加权实现对一些激活层的抑制或放大，同时优化损失函数以适应少样本学习。

{{< figure src="/images/cn/2025-08-09-fine-tuning-llm/liu2022few-1.avif" >}}

[^ibm-fine-tuning]: https://www.ibm.com/cn-zh/think/topics/fine-tuning

[^huyen2024ai]: Huyen, Chip. _AI Engineering: Building Applications with Foundation Models._ O'Reilly Media, Incorporated, 2024.

[^lialin2023scaling]: Lialin, Vladislav, Vijeta Deshpande, and Anna Rumshisky. "Scaling down to scale up: A guide to parameter-efficient fine-tuning." _arXiv preprint arXiv:2303.15647_ (2023).

[^li2021prefix]: Li, Xiang Lisa, and Percy Liang. "Prefix-tuning: Optimizing continuous prompts for generation." _arXiv preprint arXiv:2101.00190_ (2021).

[^lester2021power]: Lester, Brian, Rami Al-Rfou, and Noah Constant. "The power of scale for parameter-efficient prompt tuning." _arXiv preprint arXiv:2104.08691_ (2021).

[^liu2021gpt]: Liu, Xiao, et al. "GPT Understands, Too." _arXiv preprint arXiv:2103.10385_ (2021).

[^liu2021p]: Liu, Xiao, et al. "P-tuning v2: Prompt tuning can be comparable to fine-tuning universally across scales and tasks." _arXiv preprint arXiv:2110.07602_ (2021).

[^houlsby2019parameter]: Houlsby, Neil, et al. "Parameter-efficient transfer learning for NLP." _International conference on machine learning_. PMLR, 2019.

[^hu2022lora]: Hu, Edward J., et al. "Lora: Low-rank adaptation of large language models." _ICLR_ 1.2 (2022): 3.

[^liu2022few]: Liu, Haokun, et al. "Few-shot parameter-efficient fine-tuning is better and cheaper than in-context learning." _Advances in Neural Information Processing Systems_ 35 (2022): 1950-1965.
