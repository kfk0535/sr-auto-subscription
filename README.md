# Shadowrocket 自动订阅聚合

GitHub Actions 每 6 小时拉取 `sources.txt` 中的公开订阅源，合并、去重节点，并生成 Shadowrocket 可导入的 Base64 订阅文件 `subscribe.txt`。

## 启用

1. 在仓库根目录保留 `sources.txt`，并把公开订阅源 URL 每行写一个。
2. 将 `scripts/aggregate.py` 和 `.github/workflows/update.yml` 添加到仓库对应路径。
3. 在 GitHub 仓库打开 **Settings → Actions → General → Workflow permissions**，选择 **Read and write permissions** 并保存。
4. 打开 **Actions → 更新 Shadowrocket 订阅 → Run workflow** 手动运行一次。此后每 6 小时自动更新。

## Shadowrocket 订阅地址

```text
https://raw.githubusercontent.com/kfk0535/sr-auto-subscription/main/subscribe.txt
```

在 Shadowrocket 中打开 **配置/订阅 → 添加订阅**，粘贴此地址并保存，然后更新订阅。

## 添加或修改来源

编辑 `sources.txt`，每行放一个能直接访问的节点列表 URL。脚本支持常见 Base64 订阅以及包含 `vmess://`、`vless://`、`ss://`、`trojan://` 等链接的纯文本。改动并推送后也会触发一次更新。

## 注意

这是公开网络上的免费节点集合，在线状态、速度和隐私保护无法保证。节点运营者可能看到连接元数据或流量内容；不要用于登录重要账号、处理敏感信息或传输隐私数据。公共节点也可能随时失效。
