# Zashboard Config

个人使用的 [Zashboard](https://github.com/Zephyruso/zashboard) 面板配置备份与多设备同步仓库。

## 使用方法

在 Zashboard 的“从 URL 导入”中填入：

```text
https://raw.githubusercontent.com/zzpice/zashboard-config/main/zashboard-settings.json
```

然后开启：

- 从 URL 导入设置
- 自动从 URL 导入

首次导入后，其他设备也可以使用同一个地址加载这套配置。

## 更新配置

当 Zashboard 中的设置有变化时：

1. 在 Zashboard 中导出最新设置。
2. 用新的文件替换本仓库中的 `zashboard-settings.json`。
3. 提交更改。
4. 其他设备会在打开 Zashboard 时自动读取最新配置。

## 当前配置

目前主要包含：

- 字体：MiSans
- Emoji：noto-color-emoji
- 基础字号：17.5px
- 自动切换浅色 / 深色主题
- 自定义策略组图标
- 来源 IP 设备标签
- 代理页、连接页和测速相关设置

## 注意事项

本仓库仅用于保存 Zashboard 的界面与面板设置。

请勿上传以下内容：

- sing-box 服务端配置
- Reality 私钥
- UUID
- API Secret
- SSH 凭据
- 含 Token 的订阅链接

## 配置文件

`zashboard-settings.json` 是 Zashboard 导出的设置文件，也是各设备自动导入时使用的配置源。
