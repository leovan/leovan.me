---
title: '在 OpenWrt 和群晖中自动申请和部署证书'
author: 范叶亮
date: '2025-05-25'
slug: auto-apply-and-deploy-certificate-on-openwrt-and-synology
categories:
  - 编程
tags:
  - OpenWrt
  - 群晖
  - Synology
  - 证书
  - Certificate
  - acme.sh
  - Let's Encrypt
  - Cloudflare
images:
  - /images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/openwrt-ip-domain.png
  - /images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/synology-ip-domain.png
---

为了在本地局域网环境中摆脱 IP 用上域名（纯属闲来无事瞎鼓捣），购入了 `leovan.dev` 域名。想着把各种服务都映射到不同的二级域名上，这样就可以不用 IP 和端口了，岂不完美。然，问题这就来了。

# acme.sh

域名是在 Cloudflare 上申请的，在 Cloudflare 上使用 [Page 服务](https://pages.cloudflare.com/)部署网站就可以白嫖他家的证书，还能自动帮你续期，比如当前的站点就是使用 Page 进行部署的。但你要是想生成证书下载下来使用，就会很麻烦，因为证书的有效期只有三个月，手动续期再加上各种替换操作就不太方便了。

这时候就要请出我们的 [acme.sh](https://github.com/acmesh-official/acme.sh) 了，除了支持各种桌面和服务器操作系统外，还支持 OpenWrt 路由器系统。

# Cloudflare

使用 acme.sh 申请免费证书需要使用 DNS 验证对域名的所有权，本文以 Cloudflare 为例，其它 DNS 请参考[官方文档](https://github.com/acmesh-official/acme.sh/wiki/dnsapi)。Cloudflare 支持两种方式，一种是使用 API Token，另一种是使用全局 API Key，这里我们以 API Token 为例。

进入 [API Token 页面](https://dash.cloudflare.com/profile/api-tokens)，单击 <button>创建令牌</button> 按钮，在 API 令牌模板中选择 `编辑区域 DNS`，单击 <button>使用模板</button> 按钮。在 `权限` 中添加 `区域 - DNS - 编辑` 和 `区域 - 区域 - 读取` 的权限，在 `区域资源` 中根据你的需求选择对应的 `特定区域`，例如 `leovan.dev`，或为了省事选择 `所有区域` 也可以，如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/cloudflare-create-api-token.png" title="创建 API Token" large-max-width="60%" >}}

创建完毕后会生成 Token，将 Token 保存为 `CF_Token="xxxxxxxxx"`，注意该 Token 在 Cloudflare 中不会再展示。

之后从 Cloudflare 账户主页进入对应的域名详情页面，在右下角可以找到 API 的区域 ID 和账户 ID 两个代码，如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/cloudflare-region-id-account-id.png" title="区域 ID 和账户 ID" large-max-width="40%" middle-max-width="60%" >}}

将区域 ID 保存为 `CF_Zone_ID="xxxxxxxxx"`，将账户 ID 保存为 `CF_Account_ID="xxxxxxxxx"`。

# OpenWrt

Opwnert 使用 [uHTTPd](https://openwrt.org/docs/guide-user/services/webserver/http.uhttpd) 作为默认的 Web 服务器。正如官网上说的，这是一个轻量极了的 Web 服务器，以至于不支持反向代理。

{{% admonition type="warning" title="" %}}
那就安装一个 Nginx 吧，不是说不行，只是 Nginx 和 uHTTPd 存在冲突，你需要把路由器的 LuCI 也切换到 Nginx 上，麻烦不说，后续如果有更新还有可能又会变回 uHTTPd。自己搞了下，差点登录不进去 Web 页面，遂放弃。
{{% /admonition %}}

但这不影响我们先把路由器的域名 `router.leovan.dev` 映射到 `192.168.100.1` 上先用起来。

## acme.sh

通过 `系统 - 软件包` 或命令行安装 acme.sh 相关软件包：

```sh
opkg install acme acme-acmesh-dnsapi luci-app-acme luci-i18n-acme-zh-cn luci-ssl-openssl
```

安装完毕后可以在 `服务` 菜单下找到 `ACME 证书` 子菜单，进入后在 `ACME 全局配置` 中输入 `电子邮件帐户`，勾选 `启用调试日志记录`，如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/openwrt-acme-global-conf.png" title="ACME 证书 - ACME 全局配置" large-max-width="80%" >}}

在 `证书配置` 中删除默认的配置，在下方输入框中输入配置名称，例如 `leovan_dev`，如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/openwrt-acme-certificate-conf.png" title="ACME 证书 - 证书配置" large-max-width="80%" >}}

单击 <button>添加</button> 按钮打开配置对话框。在 `常规设置` 中勾选 `已启用`，输入所需的域名，选择验证方式为 `DNS`，其它保持默认，如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/openwrt-acme-add-certificate-1.png" title="ACME 证书 - 证书配置 - 常规设置" large-max-width="80%" >}}

在 `DNS 质询验证` 中选择对应的 DNS API（本文使用 `CloudFlare.com`），并将上文中的 `CF_Token="xxxxxxxxx"`、`CF_Zone_ID="xxxxxxxxx"` 和 `CF_Account_ID="xxxxxxxxx"` 填写到对应的位置，其它保持默认，如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/openwrt-acme-add-certificate-2.png" title="ACME 证书 - 证书配置 - DNS 质询验证" large-max-width="80%" >}}

在 `高级设置` 中根据自己的需求选择 `密钥长度`（本文使用 `ECC 256 位`），其它保持默认，如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/openwrt-acme-add-certificate-3.png" title="ACME 证书 - 证书配置 - 高级设置" large-max-width="80%" >}}

单击 <button>保存</button> 按钮，并在 `ACME 证书` 页面单击 <button>保存并应用</button> 按钮。

稍等片刻后，如果运行正常则可以在 `证书` 中看到对应域名的证书，如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/openwrt-acme-certificate.png" title="ACME 证书 - 证书" large-max-width="80%" >}}

同时，系统会启动自动续签，在 `系统 - 计划任务` 中可以看到添加了如下一条记录：

```
0 0 * * * /etc/init.d/acme renew
```

## uHTTPd

通过 `系统 - 软件包` 或命令行安装 uHTTPd 的管理界面：

```sh
opkg install luci-app-uhttpd luci-i18n-uhttpd-zh-cn
```

安装完毕后可以在 `服务` 菜单下找到 `uHTTPd` 子菜单，进入后在 `MAIN - 常规设置` 中添加 HTTPS 监听，如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/openwrt-uhttpd-https-listen.png" title="uHTTPd - HTTPS 监听" large-max-width="50%" middle-max-width="70%" >}}

在 `HTTPS 证书` 中选择上文中生成的证书（本文为 `/etc/ssl/acme/leovan.dev.fullchain.crt`），如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/openwrt-uhttpd-https-cer.png" title="uHTTPd - HTTPS 证书" large-max-width="60%" >}}

在 `HTTPS 私钥` 中选择上文中生成的私钥（本文为 `/etc/ssl/acme/leovan.dev.key`），如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/openwrt-uhttpd-https-key.png" title="uHTTPd - HTTPS 证书" large-max-width="60%" >}}

在 `uHTTPd` 页面单击 <button>保存并应用</button> 按钮。

在 Cloudflare 中将 `router.leovan.dev` 解析到 `192.168.100.1` 上后，分别通过 `http://192.168.100.1`、`https://192.168.100.1` 和 `https://router.leovan.dev` 访问路由器，如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/openwrt-ip-domain.png" title="路由器 - IP 和 域名访问" large-max-width="40%" middle-max-width="60%" >}}

可以看出通过 `router.leovan.dev` 域名进行访问已经实现了 HTTPS 安全访问。

# 群晖

由于在 OpenWrt 上搞 Nginx 有些麻烦，此时此刻，恰巧手里还有一台群晖的 NAS，恰巧群晖默认支持反向代理服务器，这一切的一切不就又双叒叕完美了。

## acme.sh

稍显遗憾的是在群晖中没有像 OpenWrt 那样的工具可以直接使用，这里就只能用脚本的方式手搓部署了。首先通过命令行 SSH 登录群晖，并切换到 root 用户：

```sh
sudo su
cd /root
```

由于群晖没有 crontab，因此需要使用如下命令强制安装，根据实际情况修改命令中的电子邮箱：

```sh
curl https://get.acme.sh | sh -s email=my@example.com --force
```

当控制台显示 `Install success!` 后表示安装成功。进入 `/root/.acme.sh` 目录，修改 `account.conf` 文件：

```sh
cd /root/.acme.sh
vi account.conf
```

`account.conf` 文件示例如下，请根据上文中的内容修改 `CF_Token`、`CF_Zone_ID` 和 `CF_Account_ID` 配置项：

```txt
export CF_Token="xxxxxxxxx"
export CF_Zone_ID="xxxxxxxxx"
export CF_Account_ID="xxxxxxxxx"

LOG_FILE="/root/.acme.sh/acme.sh.log"
LOG_LEVEL=1

AUTO_UPGRADE="1"

ACCOUNT_EMAIL="my@example.com"
UPGRADE_HASH="xxxxxxxxx"
```

运行如下命令申请证书：

```sh
./acme.sh --set-default-ca --server letsencrypt
./acme.sh --issue --dns dns_cf --keylength ec-256 -d leovan.dev -d *.leovan.dev
```

正常情况下，申请的证书将保存在 `/root/.acme.sh/leovan.dev_ecc` 目录下。

运行如下命令将证书部署到群晖系统中：

```sh
export SYNO_USE_TEMP_ADMIN=1
./acme.sh --deploy --deploy-hook synology_dsm -d leovan.dev -d *.leovan.dev
```

此时进入群晖的 `控制面板 - 安全性 - 证书` 中，可以看到 `leovan.dev` 证书已经部署到系统中并作为默认证书，如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/synology-cer.png" title="控制面板 - 安全性 - 证书" large-max-width="80%" >}}

在群晖中创建计划任务来实现自动更新并部署证书，在 `控制面板 - 计划任务` 中选择 `新建 - 计划的任务 - 用户自定的脚本`。在 `常规` 中设置 `任务名称`，选择 `用户账号` 为 `root`，如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/synology-cron-1.png" title="计划任务 - 常规" large-max-width="60%" >}}

在 `计划` 中设置执行的周期，由于 acme.sh 在证书到期前一个月会发起重新申请，因此可以将计划任务周期设置为每周，如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/synology-cron-2.png" title="计划任务 - 计划" large-max-width="60%" >}}

在 `任务设置` 中设置 `用户自定义的脚本`：

```sh
/root/.acme.sh/acme.sh --cron --home /root/.acme.sh
```

根据个人需要可以勾选 `通过电子邮件发送运行详情`，如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/synology-cron-3.png" title="计划任务 - 任务设置" large-max-width="60%" >}}

## 反向代理

在 Cloudflare 中将 `nas.leovan.dev` 解析到 `192.168.100.10` 上后，在群晖的 `登录门户 - 高级` 单击 <button>反向代理服务器</button> 按钮打开对话框，单击 <button>新增</button> 按钮，根据下图添加配置：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/synology-reverse-proxy.png" title="反向代理" large-max-width="60%" >}}

分别通过 http://192.168.100.10:500 和 https://nas.leovan.dev 访问群晖，如下图所示：

{{< figure src="/images/cn/2025-05-25-auto-apply-and-deploy-certificate-on-openwrt-and-synology/synology-ip-domain.png" title="群晖 - IP 和 域名访问" large-max-width="40%" middle-max-width="60%" >}}

可以看出通过 `nas.leovan.dev` 域名进行访问已经实现了 HTTPS 安全访问。

{{% admonition type="tip" title="" %}}
针对局域网其它机器上的 Web 服务，可以先将域名解析到群晖的 IP 上，再利用群晖的反向代理转发到对应机器的 Web 服务上。对于非 Web 服务，将域名直接解析到对应的机器上即可。
{{% /admonition %}}
