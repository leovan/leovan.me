---
title: 本地部署大模型服务
enTitle: Local Deployment of LLM Services
author: 范叶亮
date: 2026-04-05
slug: local-deployment-of-llm-server
categories:
  - AI
  - Tech101
  - 教程
tags:
  - 人工智能
  - AI
  - 本地部署
  - 大模型
  - ollama
  - LM Studio
  - vllm
  - oMLX
  - Gemma
  - Qwen
  - CoPaw
---

# 环境信息

本教程将介绍在 macOS 和 Windows 环境下部署本地大模型服务。如无特殊说明，macOS 系统下需在终端中执行命令，Windows 系统下需要在 PowerShell 中执行命令。本教程涉及到的软件和模型信息如下：

| 软件       | 版本                   |
|:-----------|:-----------------------|
| ollama     | 0.20.2                 |
| LM Studio  | 0.4.9+1                |
| vllm       | 0.19.0                 |
| vllm-metal | v0.1.0-20260404-164341 |
| vllm-mlx   | 0.2.7                  |
| oMLX       | 0.3.4                  |
{caption="软件信息"}

| 名称               | 架构 | 量化 | 内存 / 显存  | 能力 | 链接 |
|:-------------------|:-----|:-----|:------------ | :--- | :--- |
| gemma-4-31B-it     | 稠密 | 4bit | 32 GB 及以上 | <i class="icon-mask icon-lucide-image" style="background-color: oklch(64.6% 0.222 41.116);"></i> <i class="icon-mask icon-lucide-video" style="background-color: oklch(62.7% 0.265 303.9);"></i> <i class="icon-mask icon-lucide-audio-lines" style="background-color: oklch(79.5% 0.184 86.047);"></i> <i class="icon-mask icon-lucide-hammer" style="background-color: oklch(62.3% 0.214 259.815);"></i> <i class="icon-mask icon-lucide-brain" style="background-color: oklch(72.3% 0.219 149.579);"></i> | <i class='icon icon-huggingface'></i>：[GGUF](https://huggingface.co/lmstudio-community/gemma-4-31B-it-GGUF) / [GGUF](https://huggingface.co/unsloth/gemma-4-31B-it-GGUF) / [MLX](https://huggingface.co/mlx-community/gemma-4-31b-it-nvfp4) <br/> <i class='icon icon-modelscope'></i>：[GGUF](https://modelscope.cn/models/lmstudio-community/gemma-4-31B-it-GGUF) / [GGUF](https://modelscope.cn/models/unsloth/gemma-4-26B-A4B-it-GGUF) / [MLX](https://modelscope.cn/models/mlx-community/gemma-4-31b-it-nvfp4) |
| gemma-4-26B-A4B-it | MoE  | 4bit | 32 GB 及以上 | <i class="icon-mask icon-lucide-image" style="background-color: oklch(64.6% 0.222 41.116);"></i> <i class="icon-mask icon-lucide-video" style="background-color: oklch(62.7% 0.265 303.9);"></i> <i class="icon-mask icon-lucide-audio-lines" style="background-color: oklch(79.5% 0.184 86.047);"></i> <i class="icon-mask icon-lucide-hammer" style="background-color: oklch(62.3% 0.214 259.815);"></i> <i class="icon-mask icon-lucide-brain" style="background-color: oklch(72.3% 0.219 149.579);"></i> | <i class='icon icon-huggingface'></i>：[GGUF](hhttps://huggingface.co/lmstudio-community/gemma-4-26B-A4B-it-GGUF) / [GGUF](https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF) / [MLX](https://huggingface.co/mlx-community/gemma-4-26b-a4b-it-nvfp4) <br/> <i class='icon icon-modelscope'></i>：[GGUF](https://modelscope.cn/models/lmstudio-community/gemma-4-26B-A4B-it-GGUF) / [GGUF](https://modelscope.cn/models/unsloth/gemma-4-26B-A4B-it-GGUF) / [MLX](https://modelscope.cn/models/mlx-community/gemma-4-26b-a4b-it-nvfp4) |
| Qwen3.5-27B        | 稠密 | 4bit | 32 GB 及以上 | <i class="icon-mask icon-lucide-image" style="background-color: oklch(64.6% 0.222 41.116);"></i> <i class="icon-mask icon-lucide-hammer" style="background-color: oklch(62.3% 0.214 259.815);"></i> <i class="icon-mask icon-lucide-brain" style="background-color: oklch(72.3% 0.219 149.579);"></i> | <i class='icon icon-huggingface'></i>：[GGUF](https://huggingface.co/lmstudio-community/Qwen3.5-27B-GGUF) / [GGUF](https://huggingface.co/unsloth/Qwen3.5-27B-GGUF) / [MLX](https://huggingface.co/mlx-community/Qwen3.5-27B-4bit) <br/> <i class='icon icon-modelscope'></i>：[GGUF](https://modelscope.cn/models/lmstudio-community/Qwen3.5-27B-GGUF) / [GGUF](https://modelscope.cn/models/unsloth/Qwen3.5-27B-GGUF) / [MLX](https://modelscope.cn/models/mlx-community/Qwen3.5-27B-4bit) |
| Qwen3.5-35B-A3B    | MoE  | 4bit | 32 GB 及以上 | <i class="icon-mask icon-lucide-image" style="background-color: oklch(64.6% 0.222 41.116);"></i> <i class="icon-mask icon-lucide-hammer" style="background-color: oklch(62.3% 0.214 259.815);"></i> <i class="icon-mask icon-lucide-brain" style="background-color: oklch(72.3% 0.219 149.579);"></i> | <i class='icon icon-huggingface'></i>：[GGUF](https://huggingface.co/lmstudio-community/Qwen3.5-35B-A3B-GGUF) / [GGUF](https://huggingface.co/unsloth/Qwen3.5-35B-A3B-GGUF) / [MLX](https://huggingface.co/mlx-community/Qwen3.5-35B-A3B-4bit) <br/> <i class='icon icon-modelscope'></i>：[GGUF](https://modelscope.cn/models/lmstudio-community/Qwen3.5-35B-A3B-GGUF) / [GGUF](https://modelscope.cn/models/unsloth/Qwen3.5-35B-A3B-GGUF) / [MLX](https://modelscope.cn/models/mlx-community/Qwen3.5-35B-A3B-4bit) |
| CoPaw-Flash-9B     | 稠密 | 4bit | 16 GB 及以上 | <i class="icon-mask icon-lucide-image" style="background-color: oklch(64.6% 0.222 41.116);"></i> <i class="icon-mask icon-lucide-hammer" style="background-color: oklch(62.3% 0.214 259.815);"></i> <i class="icon-mask icon-lucide-brain" style="background-color: oklch(72.3% 0.219 149.579);"></i> | <i class='icon icon-huggingface'></i>：[GGUF](https://huggingface.co/agentscope-ai/CoPaw-Flash-9B-Q4_K_M) <br/> <i class='icon icon-modelscope'></i>：[GGUF](https://modelscope.cn/models/AgentScope/CoPaw-Flash-9B-Q4_K_M) |
{caption="模型信息" footnote="<i class='icon-mask icon-lucide-image' style='background-color: oklch(64.6% 0.222 41.116);'></i>：图片， <i class='icon-mask icon-lucide-video' style='background-color: oklch(62.7% 0.265 303.9);'></i>：视频，<i class='icon-mask icon-lucide-audio-lines' style='background-color: oklch(79.5% 0.184 86.047);'></i>：音频，<i class='icon-mask icon-lucide-hammer' style='background-color: oklch(62.3% 0.214 259.815);'></i>：工具调用，<i class='icon-mask icon-lucide-brain' style='background-color: oklch(72.3% 0.219 149.579);'></i>：思考<br/><i class='icon icon-huggingface'></i>：Hugging Face，<i class='icon icon-modelscope'></i>：ModelScope"}

为了加速从 Hugging Face 模型仓库下载模型，可以运行如下命令配置相关环境变量：

{{< tab id="env-variable" >}}
{{% tab-item label="<i class='icon icon-macos'></i> macOS" %}}
```sh
echo "HF_ENDPOINT=https://hf-mirror.com" >> ~/.bash_profile
```
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-windows'></i> Windows" %}}
```powershell
[Environment]::SetEnvironmentVariable("HF_ENDPOINT", "https://hf-mirror.com", "User")
```
{{% /tab-item %}}
{{< /tab >}}

更多使用方式可参考 [HF-Mirror](https://hf-mirror.com/) 官方网站。

# ollama

推荐在终端运行如下命令安装 ollama：

{{< tab id="ollama-install" >}}
{{% tab-item label="<i class='icon icon-macos'></i> macOS" %}}
```sh
curl -fsSL https://ollama.com/install.sh | sh
```
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-windows'></i> Windows" %}}
```powershell
irm https://ollama.com/install.ps1 | iex
```
{{% /tab-item %}}
{{< /tab >}}

运行如下命令可以显示当前安装的版本号：

```plain
ollama --version
# ollama version is 0.20.2
```

ollama 当前采用 `ollama pull MODEL` 命令下载模型，除了使用[官方模型库](https://ollama.com/library)中的模型名称外（例如：`qwen3.5:27b-nvfp4`），还可以使用 Hugging Face 的模型链接（例如：`https://huggingface.co/lmstudio-community/Qwen3.5-27B-GGUF`），运行如下命令下载模型：

```plain
ollama pull qwen3.5:27b-nvfp4
ollama pull https://huggingface.co/lmstudio-community/Qwen3.5-27B-GGUF
```

ollama 当前仅支持通过环境变量配置监听地址和端口，运行如下命令进行配置：

{{< tab id="ollama-host" >}}
{{% tab-item label="<i class='icon icon-macos'></i> macOS" %}}
```sh
echo "OLLAMA_HOST=0.0.0.0:11434" >> ~/.bash_profile
```
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-windows'></i> Windows" %}}
```powershell
[Environment]::SetEnvironmentVariable("OLLAMA_HOST", "0.0.0.0:11434", "User")
```
{{% /tab-item %}}
{{< /tab >}}

运行如下命令启动模型服务：

{{< tab id="ollama-service" >}}
{{% tab-item label="<i class='icon icon-macos'></i> macOS" %}}
```sh
ollama run <模型名称>
```
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-windows'></i> Windows" %}}
```powershell
ollama run <模型名称>
```
{{% /tab-item %}}
{{< /tab >}}

{{% admonition type="tip" title="提示" %}}
ollama 默认会选择最适合的运行库，如果需要切换可以手动指定 LLM 运行库，运行如下命令表示使用 CPU 进行推理：

```plain
OLLAMA_LLM_LIBRARY="cpu_avx2" ollama serve <模型名称>
```
{{% /admonition %}}

{{% admonition type="warning" title="注意" %}}
在 Settings 中将 Context length 设置为最大值，以确保在后续使用过程中不会因上下文长度不足而导致效果下降。
{{% /admonition %}}

{{< tab id="ollama-settings" >}}
{{% tab-item label="<i class='icon icon-macos'></i> macOS" %}}
{{< figure src="/images/cn/2026-04-05-local-deployment-of-llm-server/ollama-settings-macos.avif" large-max-height="400px" >}}
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-windows'></i> Windows" %}}
{{< figure src="/images/cn/2026-04-05-local-deployment-of-llm-server/ollama-settings-windows.avif" large-max-height="400px" >}}
{{% /tab-item %}}
{{< /tab >}}

打开 ollama 主页面，选择对应的模型，即可开始对话：

{{< tab id="ollama-chat" >}}
{{% tab-item label="<i class='icon icon-macos'></i> macOS" %}}
{{< figure src="/images/cn/2026-04-05-local-deployment-of-llm-server/ollama-chat-macos.avif" large-max-height="400px" >}}
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-windows'></i> Windows" %}}
{{< figure src="/images/cn/2026-04-05-local-deployment-of-llm-server/ollama-chat-windows.avif" large-max-height="400px" >}}
{{% /tab-item %}}
{{< /tab >}}

模型服务运行在 `http://127.0.0.1:11434`，API 文档详见：<https://docs.ollama.com/api/introduction>。运行如下命令以 OpenAI 兼容的接口测试服务：

{{< tab id="ollama-test" >}}
{{% tab-item label="<i class='icon icon-macos'></i> macOS" %}}
```sh
curl http://127.0.0.1:11434/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "<模型名称>",
        "messages": [
            {
                "role": "user",
                "content": "你好"
            }
        ]
    }'
```
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-windows'></i> Windows" %}}
```powershell
iwr -Uri http://127.0.0.1:11434/v1/chat/completions `
    -Method Post `
    -ContentType "application/json" `
    -Body '{
        "model": "<模型名称>",
        "messages": [
            {
                "role": "user",
                "content": "你好"
            }
        ]
    }'
```
{{% /tab-item %}}
{{< /tab >}}

# LM Studio

{{< admonition type="info" title="建议 Windows 系统测试使用" />}}

推荐从 [LM Studio](https://lmstudio.ai/) 官网下载安装包，并运行安装 LM Studio。如果只需要安装 LM Studio 核心，不需要 GUI 界面，则可以在终端运行如下命令：

{{< tab id="llmster-install" >}}
{{% tab-item label="<i class='icon icon-macos'></i> macOS" %}}
```sh
curl -fsSL https://lmstudio.ai/install.sh | bash
```
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-windows'></i> Windows" %}}
```powershell
irm https://lmstudio.ai/install.ps1 | iex
```
{{% /tab-item %}}
{{< /tab >}}

下载并安装所需的 Runtime，macOS 系统支持 GGUF 和 MLX 两种格式，Windows 系统仅支持 GGUF 格式。

{{< tab id="lmstudio-runtime" >}}
{{% tab-item label="<i class='icon icon-macos'></i> macOS" %}}
{{< figure src="/images/cn/2026-04-05-local-deployment-of-llm-server/lmstudio-runtime-macos.avif" large-max-height="500px" >}}
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-windows'></i> Windows" %}}
{{< figure src="/images/cn/2026-04-05-local-deployment-of-llm-server/lmstudio-runtime-windows.avif" large-max-height="500px" >}}
{{% /tab-item %}}
{{< /tab >}}

{{% admonition type="warning" title="注意" %}}
在 Settings - Model Defaults 中将 Default Context Length 设置为 Model Maximum，以确保在后续使用过程中不会因上下文长度不足而导致效果下降。
{{% /admonition %}}

打开 LM Studio 主页面，选择对应的模型，即可开始对话：

{{< tab id="lmstudio-chat" >}}
{{% tab-item label="<i class='icon icon-macos'></i> macOS" %}}
{{< figure src="/images/cn/2026-04-05-local-deployment-of-llm-server/lmstudio-chat-macos.avif" large-max-height="400px" >}}
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-windows'></i> Windows" %}}
{{< figure src="/images/cn/2026-04-05-local-deployment-of-llm-server/lmstudio-chat-windows.avif" large-max-height="400px" >}}
{{% /tab-item %}}
{{< /tab >}}

单击左侧的 <i class='icon-mask icon-lucide-square-terminal'></i> 按钮，单击 <i class='icon-mask icon-lucide-server'></i> Local Server，将 Status 滑动至 Running 状态。模型服务运行在 `http://127.0.0.1:1234`，API 文档详见：<https://lmstudio.ai/docs/developer>。运行如下命令以 OpenAI 兼容的接口测试服务：

{{< tab id="lmstudio-test" >}}
{{% tab-item label="<i class='icon icon-macos'></i> macOS" %}}
```sh
curl http://127.0.0.1:1234/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "<模型名称>",
        "messages": [
            {
                "role": "user",
                "content": "你好"
            }
        ]
    }'
```
{{% /tab-item %}}

{{% tab-item label="<i class='icon icon-windows'></i> Windows" %}}
```powershell
iwr -Uri http://127.0.0.1:1234/v1/chat/completions `
    -Method Post `
    -ContentType "application/json" `
    -Body '{
        "model": "<模型名称>",
        "messages": [
            {
                "role": "user",
                "content": "你好"
            }
        ]
    }'
```
{{% /tab-item %}}
{{< /tab >}}

# oMLX

{{< admonition type="info" title="建议 macOS 系统测试使用" />}}

推荐从 [oMLX](https://omlx.ai/) 官网下载安装包，并运行安装 oMLX。安装完毕后启动，并从 macOS 菜单栏或 Windows 系统托盘单击 oMLX 图标，选择 `Start Server` 启动服务。待服务启动后，单击 `Admin Panel` 从浏览器打开管理面板，初次登录需要设置 API Key。在 Models - Downloader 中可以直接从 Hugging Face 和 ModelScope 模型仓库下载模型。

{{% admonition type="tip" title="提示" %}}
建议国内用户切换至 ModelScope 标签，复制上文 ModelScope 模型连接的尾部（例如：`mlx-community/gemma-4-31b-it-nvfp4`）至 REPOSITORY ID 中下载模型。
{{% /admonition %}}

{{< figure src="/images/cn/2026-04-05-local-deployment-of-llm-server/omlx-admin-panel-models-downloader.avif" large-max-width="800px" >}}

在 Settings - Model Settings 中单击对应模型 STATUS 中的按钮载入模型。

{{< figure src="/images/cn/2026-04-05-local-deployment-of-llm-server/omlx-admin-panel-settings-model-settings.avif" large-max-width="800px" >}}

{{% admonition type="warning" title="注意" %}}
在 Settings - Global Settings 中将 Max Context Window 和 Max Tokens 设置为合适的值，以确保在后续使用过程中不会因上下文长度不足而导致效果下降。
{{% /admonition %}}

单击 Chat 进入对话页面，选择对应的模型，即可开始对话：

{{< figure src="/images/cn/2026-04-05-local-deployment-of-llm-server/omlx-admin-panel-chat.avif" large-max-width="800px" >}}

模型服务运行在 `http://127.0.0.1:8000`。运行如下命令以 OpenAI 兼容的接口测试服务：

```sh
curl http://127.0.0.1:8000/v1/chat/completions \
    -H "Authorization: Bearer <API_KEY>" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "<模型名称>",
        "messages": [
            {
                "role": "user",
                "content": "你好"
            }
        ]
    }'
```

# vllm

{{< admonition type="info" title="建议 macOS 系统生产使用" />}}

{{% admonition type="tip" title="提示" %}}
vllm 官方仅支持 macOS 和 Linux 系统，暂无 GUI 界面。在此以 macOS 系统为例进行安装。
{{% /admonition %}}

在 macOS 系统上，使用 vllm-metal 库安装 vllm 服务，运行如下命令：

```sh
curl -fsSL https://raw.githubusercontent.com/vllm-project/vllm-metal/main/install.sh | bash
```

这会在 `~/.venv-vllm-metal` 路径下创建一个 Python 虚拟环境，并安装 vllm 服务。运行如下命令即可删除安装：

```sh
rm -rf ~/.venv-vllm-metal
```

运行如下命令激活 Python 虚拟环境：

```sh
source ~/.venv-vllm-metal/bin/activate
```

运行如下命令启动 vllm 服务：

```sh
vllm serve <模型名称|模型路径>
```

模型服务运行在 `http://127.0.0.1:8000`，更多环境变量设置请参考：<https://github.com/vllm-project/vllm-metal>，更多命令行参数设置请参考：<https://docs.vllm.ai/en/stable/api/>。运行如下命令以 OpenAI 兼容的接口测试服务：

```sh
curl http://127.0.0.1:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "<模型名称>",
        "messages": [
            {
                "role": "user",
                "content": "你好"
            }
        ]
    }'
```
