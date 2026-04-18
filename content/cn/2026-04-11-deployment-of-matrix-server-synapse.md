---
title: 部署 Matrix 服务器 Synapse
enTitle: Deployment of Matrix Server Synapse
author: 范叶亮
date: 2026-04-11
slug: deployment-of-matrix-server-synapse
categories:
  - Tech101
  - 教程
tags:
  - Matrix
  - Synapse
---

# 环境信息

[Matrix](https://matrix.org/) 是一种用于实时通讯的开放、去中心化协议，专注于安全、加密的文字、语音和视频聊天。它允许不同服务器上的用户互通，类似于邮件系统，并支持端到端加密，使用户能完全控制数据，不受单一实体限制。

{{< figure src="/images/cn/2026-04-11-deployment-of-matrix-server-synapse/federation-matrix-ids.svg" title="Matrix 联邦服务器之间连接的客户端" >}}

[Synapse](https://github.com/element-hq/synapse) 是一个使用 Python/Twisted 和 Rust 编写的开源 Matrix 服务器实现。本教程将介绍使用 Docker 容器部署 Matrix 服务器 Synapse。本教程涉及到的软件信息如下：

| 软件       | Docker 镜像                  | 版本    |
| :--------- | :--------------------------- | ------- |
| PostgreSQL | mixdeve/postgres-zhparser:18 | 18      |
| Redis      | redis:8                      | 8       |
| Synapse    | matrixdotorg/synapse:latest  | 1.151.0 |

{{% admonition type="warning" title="注意" %}}
将后续命令中的 `example.com` 替换为实际域名。
{{% /admonition %}}

# 准备工作

## 数据库

为了支持中文搜索，在此选择内置 zhparser 分词功能的 PostgreSQL 镜像。在适当位置创建 PostgreSQL 的存储目录，例如 `postgresql`。运行如下命令生成配置：

```sh
docker run -d \
  --name postgresql \
  --restart always \
  -v $(pwd)/postgresql:/var/lib/postgresql \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=<密码> \
  -e ALLOW_IP_RANGE=0.0.0.0/0 \
  -p 5432:5432 \
  mixdeve/postgres-zhparser:18
```

相关参数说明如下：

| 参数              | 说明                                 |
|:------------------|:-------------------------------------|
| POSTGRES_USER     | 数据库用户名，默认 `postgres`        |
| POSTGRES_PASSWORD | 数据库密码                           |
| POSTGRES_DB       | 默认数据库名，默认 `postgres`        |
| ALLOW_IP_RANGE    | 允许访问的 IP 范围                   |

进入数据库执行如下 SQL 进行配置：

```sql
-- 创建用户
CREATE USER synapse WITH PASSWORD '<密码>';

-- 创建数据库
CREATE DATABASE synapse WITH OWNER = synapse ENCODING = 'UTF8' LC_COLLATE = 'C' LC_CTYPE = 'C' TEMPLATE = template0;

-- 授权
GRANT ALL PRIVILEGES ON DATABASE synapse TO synapse;
```

## 缓存

为了提升服务性能，在此开启 Redis 缓存。在适当位置创建 Redis 的存储目录，例如 `redis`。运行如下命令启动 Redis 容器：

```sh
docker run -d \
  --name redis \
  --restart always \
  -v $(pwd)/redis:/data \
  -p 6379:6379 \
  redis:8 \
  redis-server --save 60 1 --appendonly yes
```

# 配置文件

进入服务器在适当位置创建 Synapse 的存储目录，例如 `synapse`。运行如下命令生成配置：

```sh
docker run -it --rm \
  -v $(pwd)/synapse:/data \
  -e SYNAPSE_SERVER_NAME=example.com \
  -e SYNAPSE_REPORT_STATS=no \
  -e SYNAPSE_HTTP_PORT=8008 \
  -e UID=1000 \
  -e GID=1000 \
  matrixdotorg/synapse:latest generate
```

相关参数说明如下：

| 参数                 | 说明                                                      |
|:---------------------|:----------------------------------------------------------|
| SYNAPSE_SERVER_NAME  | 服务器域名                                                |
| SYNAPSE_REPORT_STATS | 是否上报统计信息，默认 `yes`                              |
| SYNAPSE_HTTP_PORT    | HTTP 端口，默认 `8008`                                    |
| SYNAPSE_CONFIG_DIR   | 配置目录，默认 `/data`                                    |
| SYNAPSE_CONFIG_PATH  | 配置文件路径，默认 `<SYNAPSE_CONFIG_DIR>/homeserver.yaml` |
| SYNAPSE_DATA_DIR     | 数据目录，默认 `/data`                                    |
| UID                  | 用户 ID，默认 `991`                                       |
| GID                  | 组 ID，默认 `991`                                         |

修改配置文件服务部分如下：

```yaml
public_baseurl: https://matrix-homeserver.example.com
serve_server_wellknown: true
```

修改配置文件数据库部分如下：

```yaml
database:
  name: psycopg2
  txn_limit: 10000
  args:
    user: synapse
    password: <密码>
    dbname: synapse
    host: <数据库地址>
    port: 5432
    cp_min: 5
    cp_max: 10
```

修改配置文件缓存部分如下：

```yaml
redis:
  enabled: true
  host: <数据库地址>
  port: 6379
  dbid: 0
```

# 启动服务

运行如下命令启动服务：

```sh
docker run -d \
  --name synapse \
  --restart always \
  -v $(pwd)/synapse:/data \
  -u 1000:1000 \
  -p 8008:8008 \
  matrixdotorg/synapse:latest
```

在服务商中配置 DNS 将 `matrix-homeserver.example.com` 解析至 Docker 服务器的 IP 地址。通过浏览器访问 <http://matrix-homeserver.example.com:8008>  即可查看 Synapse 服务是否启动成功。

# 中文搜索

{{% admonition type="tip" title="提示" %}}
如果不需要中文搜索服务，可跳过本节。
{{% /admonition %}}

在 PostgreSQL 数据中运行如下 SQL 安装 zhparser 扩展并配置中文搜索：

```sql
-- 创建 zhparser 扩展
CREATE EXTENSION IF NOT EXISTS zhparser;

-- 创建中文搜索配置
CREATE TEXT SEARCH CONFIGURATION chinese (PARSER = zhparser);
ALTER TEXT SEARCH CONFIGURATION chinese ADD MAPPING FOR n,v,a,i,e,l WITH simple;

-- 添加中文向量列
ALTER TABLE event_search ADD COLUMN IF NOT EXISTS chinese_vector tsvector;

-- 对已有数据进行中文分词处理
UPDATE event_search
SET chinese_vector =
  CASE
    WHEN event_search.key = 'content.body' AND TRIM(event_json.json::jsonb->'content'->>'body') != ''
      THEN to_tsvector('chinese', event_json.json::jsonb->'content'->>'body')
    WHEN event_search.key = 'content.name' AND TRIM(event_json.json::jsonb->'content'->>'name') != ''
      THEN to_tsvector('chinese', event_json.json::jsonb->'content'->>'name')
    WHEN event_search.key = 'content.topic' AND TRIM(event_json.json::jsonb->'content'->>'topic') != ''
      THEN to_tsvector('chinese', event_json.json::jsonb->'content'->>'topic')
    ELSE NULL
  END
FROM
  event_json
WHERE
  event_search.event_id = event_json.event_id
  AND (
    event_search.chinese_vector IS NULL
    OR event_search.chinese_vector::text = ''
  );

-- 创建中文索引
CREATE INDEX CONCURRENTLY event_search_chinese_vector_idx ON event_search USING GIN (chinese_vector);
```

将修改后的 [`search.py`](/codes/cn/2026-04-11-deployment-of-matrix-server-synapse/search.py) 文件映射至 Synapse 容器，删除之前的容器，运行如下命令重新创建容器：

```sh
docker run -d \
  --name synapse \
  --restart always \
  -v $(pwd)/synapse:/data \
  -v $(pwd)/synapse/search.py:/usr/local/lib/python3.13/site-packages/synapse/storage/databases/main/search.py \
  -u 1000:1000 \
  -p 8008:8008 \
  matrixdotorg/synapse:latest
```

{{% admonition type="warning" title="注意" %}}
更新 Synapse 版本后，请注意原始 [`search.py`](https://github.com/element-hq/synapse/blob/develop/synapse/storage/databases/main/search.py) 是否发生变化，如有则需要重新修改支持中文的 `search.py`。同时请注意 [`Dockerfile`](https://github.com/element-hq/synapse/blob/develop/docker/Dockerfile) 中镜像基于的系统环境和 Python 版本是否发生变化，如有则需要对应调整将修改后 `search.py` 文件的映射路径。
{{% /admonition %}}

# 发现服务

{{% admonition type="tip" title="提示" %}}
如果希望使用主域名 `example.com` 成为 Matrix 服务域名（例如：`@user:example.com`），则需要配置发现服务。如果希望使用子域名 `matrix-homeserver.example.com` 成为 Matrix 服务域名（例如：`@user:matrix-homeserver.example.com`），则可以跳过本节。
{{% /admonition %}}

发现服务是 Matrix 网络发现服务器位置的一种方式。因为实际服务运行在子域名 `matrix-homeserver.example.com` 上，需要让其他服务器和客户端知道我们使用主域名，因此需要提供 `/.well-known/matrix` 信息。因此需要将 `https://example.com/.well-known/matrix` 映射到 `https://matrix-homeserver.example.com/.well-known/matrix`，相关细节请参考[官方文档](https://element-hq.github.io/synapse/latest/delegate.html)。

# 注册用户

Synapse 服务默认是禁止自助注册用户的，运行如下命令进入 Synapse 容器：

```sh
docker exec -it synapse /bin/bash
```

运行如下命令创建用户：

```sh
register_new_matrix_user http://localhost:8008 \
  -c /data/homeserver.yaml -a \
  -u "<用户名>" \
  -p "<密码>"
```

# 开始使用

在浏览器上打开 <https://app.element.io>，单击 {{< button >}}Sign in{{</ button >}} 切换 Homeserver 到 `example.com`，输入用户名和密码即可登录。
