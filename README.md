# Shadowrocket 自动订阅聚合

本仓库每小时同步一次经过上游可用性测试的公开节点列表，去重后生成 Shadowrocket 可导入的 Base64 订阅文件 `subscribe.txt`。

## 首次使用

1. 在仓库 **Settings → Actions → General → Workflow permissions** 中选择 **Read and write permissions** 并保存。
2. 打开 **Actions → 更新 Shadowrocket 订阅 → Run workflow** 手动运行一次。之后工作流每小时在北京时间约 **:17** 自动刷新。

## Shadowrocket 订阅地址

```text
https://raw.githubusercontent.com/kfk0535/sr-auto-subscription/main/subscribe.txt
```

在 Shadowrocket 中点首页右上角 **＋**，类型选 **Subscribe（订阅）**，粘贴 URL，填写备注后点 **完成**。

## 可用性测试说明

当前来源是 `Au1rxx/free-vpn-subscriptions` 发布的 V2Ray/Shadowrocket 格式订阅。该上游说明会从多个公开来源收集节点，并通过 sing-box 实际发出 HTTP/HTTPS 代理请求、分两轮筛选后发布。**本仓库同步上游筛选结果，没有在 GitHub Actions 中再逐个发起连接测试。**测试发生在上游的网络环境，节点在你的网络中可能被拦截或已失效；节点也可能在测试后失效。

## 隐私提醒

免费公共节点由第三方运营。不要用它登录重要账号、处理敏感信息或传输隐私数据。
