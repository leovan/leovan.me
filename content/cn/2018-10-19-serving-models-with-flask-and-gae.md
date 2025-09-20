---
title: 利用 Flask 和 Google App Engine 部署模型服务
author: 范叶亮
date: '2018-10-19'
slug: serving-models-with-flask-and-gae
categories:
  - 编程
  - 机器学习
  - 深度学习
tags:
  - Flask
  - Google App Engine
  - GAE
  - RESTful
  - 模型部署
  - 模型服务
images:
  - /images/cn/2018-10-19-serving-models-with-flask-and-gae/model-serving.png
---

{{% admonition %}}
本文的配套代码请参见 [这里](https://github.com/leovan/model-serving-demo)，建议配合代码阅读本文。
{{% /admonition %}}

# 模型部署和服务调用

对于做算法的同学，大家或多或少的更关心模型的性能指标多些，对于一些工程性问题考虑的较少。模型的部署是这些工程性问题中重要的一个，它直接关系到模型在生产系统的使用。一些成熟的机器学习框架会提供自己的解决方案，例如 [Tensorflow](https://www.tensorflow.org) 提供的 [Serving](https://www.tensorflow.org/serving/) 服务等。但很多情况下我们构建的工程可能不只使用了一种框架，因此一个框架自身的部署工具可能就很难满足我们的需求了。

针对此类情况，本文介绍一个 **简单** 的 **准生产** 模型部署方案。简单是指除了模型相关代码之外的工程性代码量不大，这得益于将要使用的 [Flask](http://flask.pocoo.org/) 框架。准生产是指这种部署方案应对一般的生产环境问题不大，对于高并发的场景可以通过横向扩容并进行负载均衡解决，但对于单次调用时效性要求较高的场景则需要另寻其他解决方案。

本文方案的模型部署和服务调用框架如下图所示：

![Model-Serving](/images/cn/2018-10-19-serving-models-with-flask-and-gae/model-serving.png)

其主要特性如下：

1. 服务端采用 Python 的 Flask 框架构建，无需使用其他外部服务。Flask 框架的 [微服务](https://zh.wikipedia.org/zh/微服务) (Microframework) 特性使得服务端代码简洁高效。
2. 利用 [Gunicorn](https://gunicorn.org/) 提供的高性能 Python WSGI HTTP UNIX Server，方便在服务端运行 Flask 应用。
3. 客户端和服务端之间采用 [RESTful API](https://zh.wikipedia.org/zh/表现层状态转换) 调用方式，尽管在性能上可能不及其他一些方案 (例如：基于 RPC 的解决方案等)，但其较好地解决了跨语言交互的问题，不同语言之间交互仅需使用 HTTP 协议和 JSON 数据格式即可。

# Flask 服务和 AJAX 调用

## Flask 服务封装

为了将模型代码和 Flask 服务进行整合，首先假设你已经对模型部分代码做了完美的封装 😎，整个工程先叫做 `model-serving-demo` 吧。整理一下代码的目录结构，给一个我中意的 Python 目录结构风格：

```
model-serving-demo/                # 工程根目录
├── bin/                           # 可执行命令目录
|   ├─ start.sh                    # 启动脚本
|   ├─ stop.sh                     # 停止脚本
|   └─ ...
├── conf/                          # 配置文件目录
|   ├─ logging.conf                # 日志配置文件
|   ├─ xxx_model.conf              # XXX Model 配置文件
|   └─ ...
├── data/                          # 数据文件目录
├── docs/                          # 文档目录
├── model_serving/                 # 模块根目录
|   ├─ models/                     # 模型代码目录
|   |   ├─ __init__.py
|   |   ├─ xxx_model.py            # XXX Model 代码
|   |   └─ ...
|   ├─ resources/                  # Flask RESTful Resources 代码目录
|   |   ├─ __init__.py
|   |   ├─ xxx_model_resource.py   # XXX Model Flask RESTful Resources 代码
|   |   └─ ...
|   ├─ tests/                      # 测试代码根目录
|   |   ├─ models                  # 模型测试代码目录
|   |   |   ├─ __init__.py
|   |   |   ├─ test_xxx_model.py   # XXX Model 测试代码
|   |   |   └─ ...
|   |   ├─ __init__.py
|   |   └─ ...
|   ├─ tmp/                        # 临时目录
|   └─ ...
├── .gitignore                     # Git Ignore 文件
├── app.yaml                       # Google App Engine 配置文件
├── LICENSE                        # 授权协议
├── main.py                        # 主程序代码
├── README.md                      # 说明文件
└── requirements.txt               # 依赖包列表
```

我们利用一个极简的示例介绍整个模型部署，相关的库依赖 `requirements.txt` 如下：

```
Flask==1.0.2
Flask-RESTful==0.3.6
Flask-Cors==3.0.6
jsonschema==2.6.0
docopt==0.6.2

# 本地部署时需保留，GAE 部署时请删除
# gunicorn==19.9.0
```

其中：

1. [Flask](http://flask.pocoo.org/) 用于构建 Flask 服务。
2. [Flask-RESTful](https://flask-restful.readthedocs.io/) 用于构建 Flask RESTful API。
3. [Flask-Cors](https://flask-cors.readthedocs.io/) 用于解决 AJAX 调用时的 [跨域问题](https://zh.wikipedia.org/zh/跨來源資源共享)。
4. [jsonschema](https://python-jsonschema.readthedocs.io/) 用于对请求数据的 JSON 格式进行校验。
5. [docopt](http://docopt.org/) 用于从代码文档自动生成命令行参数解析器。
6. [gunicorn](https://gunicorn.org/) 用于提供的高性能 Python WSGI HTTP UNIX Server。

XXX Model 的代码 `xxx_model.py` 如下：

```python
from ..utils.log_utils import XXXModel_LOGGER


LOGGER = XXXModel_LOGGER


class XXXModel():
    def __init__(self):
        LOGGER.info('Initializing XXX Model ...')

        LOGGER.info('XXX Model Initialized.')

    def hello(self, name:str) -> str:
        return 'Hello, {name}!'.format(name=name)
```

其中 `hello()` 为服务使用的方法，其接受一个类型为 `str` 的参数 `name`，并返回一个类型为 `str` 的结果。

XXX Model 的 Flask RESTful Resource 代码 `xxx_model_resource.py` 如下：

```python
from flask_restful import Resource, request

from ..models.xxx_model import XXXModel
from ..utils.validation_utils import validate_json


xxx_model_instance = XXXModel()
xxx_model_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'}
    },
    'required': ['name']
}


class XXXModelResource(Resource):
    @validate_json(xxx_model_schema)
    def post(self):
        json = request.json

        return {'result': xxx_model_instance.hello(json['name'])}
```

我们需要从 Flask RESTful 的 `Resource` 类继承一个新的类 `XXXModelResource` 用于处理 XXX Model 的服务请求。如上文介绍，我们在整个模型服务调用中使用 POST 请求方式和 JSON 数据格式，因此我们需要在类 `XXXModelResource` 中实现 `post()` 方法，同时对于传入数据的 JSON 格式进行校验。

`post()` 方法用于处理整个模型的服务请求，`xxx_model_instance` 模型实例在类 `XXXModelResource` 外部进行实例化，避免每次处理请求时都进行初始化。`post()` 的返回结果无需处理成 JSON 格式的字符串，仅需返回词典数据即可，Flask RESTful 会自动对其进行转换。

为了方便对请求数据的 JSON 格式进行校验，我们将对 JSON 格式的校验封装成一个修饰器。使用时如上文代码中所示，在 `post()` 方法上方添加 `@validate_json(xxx_model_schema)` 即可，其中 `xxx_model_schema` 为一个符合 [jsonschema](https://python-jsonschema.readthedocs.io/) 要求的 JSON Schema。示例代码中要求传入的 JSON 数据 **必须** 包含一个名为 `name` 类型为 `string` 的字段。

`validate_json` 修饰器的代码 `validation_utils.py` 如下：

```python
from functools import wraps
from jsonschema import validate, ValidationError
from flask_restful import request


def validate_json(schema, force=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            json_body = request.get_json(force=force)

            if json_body is None:
                return {'message': 'No JSON object'}, 400

            try:
                validate(json_body, schema)
            except ValidationError as e:
                return {'message': e.message}, 400

            return f(*args, **kwargs)
        return wrapper
    return decorator
```

首先我们需要验证请求包含一个 JSON 请求体，同时 JSON 请求体的内容需满足 `schema` 的要求。如果不满足这些条件，我们需要返回对应的错误信息 `message`，同时返回合理的 [HTTP 状态码](https://zh.wikipedia.org/zh/HTTP状态码) (例如：`400`) 用于表示无法处理错误的请求。对于正常的请求响应 (即 HTTP 状态码为 200 的情况)，状态码可以省略不写。

构建完 XXX Model 的 Flask RESTful Resource 后，我们就可以构建 Flask 的主服务了，主程序代码 `main.py` 如下：

```python
"""
Model Serving Demo

Usage:
    main.py [--host <host>] [--port <port>] [--debug]
    main.py (-h | --help)
    main.py --version

Options:
    --host <host>                     绑定的 Host [default: 0.0.0.0]
    --port <port>                     绑定的 Port [default: 9999]
    --debug                           是否开启 Debug [default: False]
    -h --help                         显示帮助
    -v --version                      显示版本

"""

from docopt import docopt

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from model_serving.resources.xxx_model_resource import XXXModelResource


app = Flask(__name__)
CORS(app)

api = Api(app)
api.add_resource(XXXModelResource, '/v1/XXXModel')


if __name__ == '__main__':
    args = docopt(__doc__, version='Model Serving Demo v1.0.0')
    app.run(host=args['--host'], port=args['--port'], debug=args['--debug'])
```

`docopt` 库用于从代码文档自动生成命令行参数解析器，具体使用方法请参见 [官方文档](http://docopt.org/)。整个 Flask 主服务的构建比较简单，流程如下：

1. 构建 Flask 主程序，`app = Flask(__name__)`。
2. 解决 AJAX 调用的跨域问题， `CORS(app)`。为了方便起见，我们不加任何参数，允许任意来源的请求，详细的使用方式请参见 [官方文档](https://flask-cors.readthedocs.io/)。
3. 构建 Flask RESTful API，`api = Api(app)`。
4. 将构建好的 XXX Model 的 Flask RESTful Resource 添加到 API 中，`api.add_resource(XXXModelResource, '/v1/XXXModel')`。
其中第二个参数为请求的 URL，对于这个 URL 的建议将在后续小节中详细说明。

Flask 主程序配置完毕后，我们通过 `app.run()` 在本地启动 Flask 服务，同时可以指定绑定的主机名，端口，以及是否开启调试模式等。通过 `python main.py` 启动 Flask 服务后，可以在命令行看到如下类似的日志：

```
[2018/10/21 00:00:00] - [INFO] - [XXXModel] - Initializing XXX Model ...
[2018/10/21 00:00:00] - [INFO] - [XXXModel] - XXX Model Initialized.
 * Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
[2018/10/21 00:00:00] - [INFO] - [werkzeug] -  * Running on http://0.0.0.0:9999/ (Press CTRL+C to quit)
```

现在就可以测试调用服务了，我们用 `curl` 命令进行简单的测试，相关代码 `request-demo.sh` 如下：

```bash
host=0.0.0.0
port=9999
url=/v1/XXXModel
curl_url=http://${host}:${port}${url}

invalid_json='{}'
valid_json='{"name": "Leo"}'

# No JSON object
curl --request POST --url ${curl_url} --verbose

# Invalid JSON object
curl --header 'Content-Type: application/json; charset=UTF-8' \
    --request POST --data ${invalid_json} --url ${curl_url} --verbose

# Valid JSON object
curl --header 'Content-Type: application/json; charset=UTF-8' \
    --request POST --data ${valid_json} --url ${curl_url} --verbose
```

三种不同的请求返回的 HTTP 状态码和结果如下：

```
HTTP/1.0 400 BAD REQUEST
{"message": "No JSON object"}

HTTP/1.0 400 BAD REQUEST
{"message": "'name' is a required property"}

HTTP/1.0 200 OK
{"result": "Hello, Leo!"}
```

上文中，我们通过 `python main.py` 利用内置的 Server 启动了 Flask 服务，启动后日志中打印出来一条警告信息，告诉使用者不要在生产环境中使用内置的 Server。在生产环境中我们可以利用高性能 Python WSGI HTTP UNIX Server [gunicorn](https://gunicorn.org/) 来启动 Flask 服务。

服务启动 (`start.sh`) 脚本代码如下：

```bash
cd `dirname $0`
cd ..

base_dir=`pwd`
tmp_dir=${base_dir}/tmp
pid_file_path=${tmp_dir}/model-serving-demo.pid
log_file_path=${tmp_dir}/model-serving-demo.log

bind_host=0.0.0.0
bind_port=9999
workers=2

nohup gunicorn -b ${bind_host}:${bind_port} \
  -w ${workers} -p ${pid_file_path} \
  main:app > ${log_file_path} 2>&1 &
```

服务停止 (`stop.sh`) 脚本代码如下：

```bash
cd `dirname $0`
cd ..

base_dir=`pwd`
tmp_dir=${base_dir}/tmp
pid_file_path=${tmp_dir}/model-serving-demo.pid

kill -TERM `echo ${pid_file_path}`
```

gunicorn 的详细参数配置和使用教程请参见 [官方文档](https://docs.gunicorn.org/en/stable/)。

## RESTful API 设计

RESTful API 是一种符合 REST(Representational State Transfer，表现层状态转换) 原则的框架，该框架是由 Fielding 在其博士论文 [^fielding2000architectural] 中提出。相关的核心概念如下：

1. **资源 (Resources)**，即网络中的一个实体 (文本，图片，服务等)，使用一个 URL 进行表示。
2. **表现层 (Representation)**，资源具体的呈现形式即为表现层，例如图片可以表示为 PNG 文件，音乐可以表示为 MP3 文件，还有本文使用的数据格式 JSON 等。HTTP 请求的头信息中用 Accept 和 Content-Type 字段对表现层进行描述。
3. **状态转换 (State Transfer)**，互联网通信协议 HTTP 协议是一个无状态协议，所有的状态都保存在服务端。因此如果客户端想要操作服务器，必须通过某种手段让服务器端发生 **状态转换**。客户端利用 HTTP 协议中的动作对服务器进行操作，例如：GET，POST，PUT，DELETE 等。

利用 RESTful API 构建模型服务时，需要注意如下几点：

1. 为模型服务设置专用域名，例如：`https://api.example.com`，并配以负载均衡。
2. 将 API 的版本号写入 URL 中，例如：`https://api.example.com/v1`。
3. RESTful 框架中每个 URL 表示一种资源，因此可以将模型的名称作为 URL 的终点 (Endpoint)，例如：`https://api.example.com/v1/XXXModel`。
4. 对于操作资源的 HTTP 方式有多种，综合考虑建议选用 POST 方式，同时建议使用 JSON 数据格式。
5. 为请求响应设置合理的状态码，例如：200 OK 表示正常返回，400 INVALID REQUEST 表示无法处理客户端的错误请求等。
6. 对于错误码为 4xx 的情况，建议在返回中添加键名为 `message` 的错误信息。

## AJAX 调用

对于动态网页，我们可以很容易的在后端服务中发起 POST 请求调用模型服务，然后将结果在前端进行渲染。对于静态网页，我们可以利用 AJAX 进行相关操作，实现细节请参见 [示例代码](https://github.com/leovan/model-serving-demo/tree/master/client/xxx-model-ajax-client.html)。

AJAX 服务请求代码的核心部分如下：

```javascript
$(document).ready(function() {
    $("#submit").click(function() {
        $.ajax({
            url: "http://0.0.0.0:9999/v1/XXXModel",
            method: "POST",
            contentType: "application/json; charset=UTF-8",
            data: JSON.stringify({"name": $("#name").val()}),
            timeout: 3000,

            success: function (data, textStatus, jqXHR) {
                $("#result").html(data.result);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                $("#result").html(errorThrown);
            }
        });
    });
});
```

代码使用了 [jQuery](https://jquery.com/) 的相关函数。`JSON.stringify({"name": $("#name").val()})` 获取 ID 为 `name` 的元素的值，并将其转换成符合服务端要求的 JSON 格式。通过 AJAX 向远程发出请求后，如果请求成功则将返回数据 `data` 中对应的结果 `result` 填充到 ID 为 `result` 的元素中，否则填入返回的错误信息。

# Google App Engine 部署

上文中已经介绍了如何在本地利用 Flask 部署模型服务和相关调用方法，但如果希望在自己的网站中调用时，则利用 SaaS 来部署符合会是一个不二之选。国内外多个厂商均提供了相应的 SaaS 产品，例如 [Google](https://cloud.google.com/appengine/)，[Amazon](https://aws.amazon.com/partners/saas-on-aws/)，[Microsoft](https://azure.microsoft.com/en-us/solutions/saas/) 等。Google App Engine (GAE) 提供了一个 [始终免费](https://cloud.google.com/free/docs/always-free-usage-limits) 方案，虽然部署阶段会受到 GFW 的影响，但调用阶段测试影响并不是很大 (不同地区和服务提供商会有差异)。综合考虑，本文选择 GAE 作为 SaaS 平台部署服务，各位看官请自备梯子。

## 环境准备

首先，在 [Google Cloud Platform Console](https://console.cloud.google.com/projectcreate) 中建立一个新的 Project，假设项目名为 `YOUR_PROJECT_ID`。

其次，根据 [Google Cloud SDK 文档](https://cloud.google.com/sdk/docs/) 在本地安装相应版本的 Google Cloud SDK。MacOS 下建议通过 `brew cask install google-cloud-sdk` 方式安装，安装完毕后确认在命令行中可以运行 `gcloud` 命令。

```bash
$ gcloud version
Google Cloud SDK 221.0.0
bq 2.0.35
core 2018.10.12
gsutil 4.34
```

## 构建 GAE 工程

模型服务仅作为后端应用，因此本节不介绍前端页面开发的相关部分，有兴趣的同学请参见 [官方文档](https://cloud.google.com/appengine/docs/standard/python3/quickstart)。GAE 部署 Python Web 应用采用了 [WSGI 标准](https://wsgi.readthedocs.io/en/latest/)，我们构建的本地部署版本完全满足这个要求，因此仅需为项目在根目录添加一个 GAE 配置文件 `app.yaml` 即可，内容如下：

```yaml
runtime: python37

handlers:
  - url: /.*
    script: main.app

skip_files:
  - .idea/
  - .vscode/
  - __pycache__/
  - .hypothesis/
  - .pytest_cache/
  - bin/
  - ^(.*/)?.*\.py[cod]$
  - ^(.*/)?.*\$py\.class$
  - ^(.*/)?.*\.log$
```

其中，`runtime` 指定了服务运行的环境，`handlers` 指定了不同的 URL 对应的处理程序，在此所有的 URL 均由 `main.py` 中的 `app` 进行处理，`skip_files` 用于过滤不需要上传的文件。更多关于 `app.yaml` 的设置信息，请参见 [官方文档](https://cloud.google.com/appengine/docs/standard/python3/config/appref)。

## 部署 GAE 工程

在部署 GAE 工程之前我们可以利用本地的开发环境对其进行测试，测试无误后，即可运行如下命令将其部署到 GAE 上：

```bash
gcloud app deploy --project [YOUR_PROJECT_ID]
```

然后根据命令行提示完成整个部署流程，部署完成的远程服务 URL 为 `https://YOUR_PROJECT_ID.appspot.com`，更多的测试和部署细节请参见 [官方文档](https://cloud.google.com/appengine/docs/standard/python3/testing-and-deploying-your-app)。

部署后的 GAE 服务使用了其自带的域名 `appspot.com`。如果你拥有自己的域名，可以根据官方文档 [设置自己的域名](https://cloud.google.com/appengine/docs/standard/python3/mapping-custom-domains) 并 [开启 SSL](https://cloud.google.com/appengine/docs/standard/python3/secURLng-custom-domains-with-ssl)。

{{% admonition %}}
本文部分内容参考了 Genthial 的博客 [Serving a model with Flask](https://guillaumegenthial.github.io/serving.html) 和阮一峰的博客 [理解RESTful架构](https://www.ruanyifeng.com/blog/2011/09/restful.html) 和 [RESTful API 设计指南](https://www.ruanyifeng.com/blog/2014/05/restful_api.html)。
{{% /admonition %}}

[^fielding2000architectural]: Fielding, Roy T., and Richard N. Taylor. _Architectural styles and the design of network-based software architectures._ Vol. 7. Doctoral dissertation: University of California, Irvine, 2000.
