# Zashboard 界面设置

个人使用的 Zashboard 外观与界面偏好，供多设备导入。公开文件只保存可分享的设置。

[导入说明](#使用方法) · [下载设置](https://raw.githubusercontent.com/zzpice/zashboard-config/main/zashboard-settings.json) · [ZZP · 所有项目](https://zzp.moe/)

[![检查](https://github.com/zzpice/zashboard-config/actions/workflows/validate.yml/badge.svg)](https://github.com/zzpice/zashboard-config/actions/workflows/validate.yml)

个人使用的 [Zashboard](https://github.com/Zephyruso/zashboard) 面板配置备份与多设备同步仓库。

## 使用方法

在 Zashboard 的“从 URL 导入”中填入：

```text
https://raw.githubusercontent.com/zzpice/zashboard-config/main/zashboard-settings.json
```

然后点击“从 URL 导入设置”，确认覆盖本地设置，再开启“自动从 URL 导入”。

自动导入会在打开面板时检查远端配置；配置变化时，默认仍会要求确认。若希望免确认应用更新，可在确认对话框中选择“不再询问、始终应用”。这个偏好保存在当前浏览器中，不随设置文件导出，需要在各浏览器 / 设备分别选择。

首次导入后，其他设备也可以使用同一个地址加载这套配置。

## 更新配置

当 Zashboard 中的设置有变化时：

1. 在 Zashboard 中导出最新设置；
2. 用新文件替换本仓库中的 `zashboard-settings.json`；
3. 提交更改；
4. GitHub Actions 自动校验配置；
5. 其他设备在打开 Zashboard 时读取最新配置。

## 自动校验

每次修改 `zashboard-settings.json`，GitHub Actions 会检查：

- JSON 能否正常解析；
- 顶层结构是否为对象；
- 自动导入 URL 是否使用 HTTPS；
- 是否出现明显的密码、Token、Secret、私钥字段；
- 是否误放入 `ss://`、`vmess://`、`vless://`、`trojan://`、`hysteria2://`、`tuic://` 等节点链接；
- 是否出现带用户名密码的 HTTP Basic Auth URL。

这些检查是防呆措施，不能代替提交前的人工检查。

## 当前配置

目前主要包含：

- 字体：MiSans；
- Emoji：noto-color-emoji；
- 基础字号：17.5px；
- 自动切换浅色 / 深色主题；
- 自定义策略组图标；
- 代理页、连接页和测速相关设置。

## 公开边界

本仓库只用于保存 Zashboard 的界面与面板设置。

请勿上传：

- sing-box 服务端配置；
- 节点或订阅链接；
- Reality 私钥；
- UUID 等连接凭据；
- API Secret / Token；
- SSH 凭据。

公开文件不保留来源 IP 与设备标签映射，`config/source-ip-label-list` 固定为空列表。局域网地址、设备名称和其他个人网络信息放在自己的私有覆盖文件中；应用这类覆盖时关闭自动从公开 URL 导入，避免下次启动时覆盖本地设置。

此前版本曾包含设备映射，本轮已从当前公开文件移除。Git 历史仍能访问旧内容；若其中的信息需要撤回，应另行评估历史清理与受影响环境的调整。

## 配置文件

`zashboard-settings.json` 是 Zashboard 导出的设置文件，也是各设备自动导入时使用的配置源。

## 项目体系

属于 [ZZP 工具与资源](https://zzp.moe/)。共同的[设计与仓库规范](https://github.com/zzpice/zzp-home/blob/main/docs/design.md)由入口仓库维护；使用步骤、生成产物和验证方式仍以本仓库为准。

## 本地验证

```sh
python3 scripts/validate.py
python3 -m unittest discover -s scripts -p 'test_*.py'
```

校验器检查 JSON、固定导入地址、凭据、节点链接、嵌套 JSON 以及私人地址与设备映射，只输出规则编号，不回显设置内容。
