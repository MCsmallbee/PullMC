<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/img/logo_dark.svg">
    <img alt="PullMC Logo" src="docs/img/logo.svg" width="100">
  </picture>
<h1>PullMC</h1>

**简体中文** &nbsp;|&nbsp; [English](docs/README_EN.md) &nbsp;|&nbsp; [日本語](docs/README_JP.md)

<p>轻量、纯净的 Minecraft Java版 版本下载工具</p>

[![主要语言](https://img.shields.io/github/languages/top/MCsmallbee/PullMC)](https://github.com/MCsmallbee/PullMC)
[![星标数量](https://img.shields.io/github/stars/MCsmallbee/PullMC?label=%E6%98%9F%E6%A0%87%E6%95%B0%E9%87%8F)](https://github.com/MCsmallbee/PullMC/stargazers)
[![开源协议](https://img.shields.io/github/license/MCsmallbee/PullMC?label=%E5%BC%80%E6%BA%90%E5%8D%8F%E8%AE%AE)](https://github.com/MCsmallbee/PullMC/blob/main/LICENSE)
[![最新发行版日期](https://img.shields.io/github/release-date-pre/MCsmallbee/PullMC?label=%E6%9C%80%E6%96%B0%E5%8F%91%E8%A1%8C%E7%89%88%E6%97%A5%E6%9C%9F)](https://github.com/MCsmallbee/PullMC/releases)
[![语言数量](https://img.shields.io/github/languages/count/MCsmallbee/PullMC?label=%E8%AF%AD%E8%A8%80%E6%95%B0%E9%87%8F)](https://github.com/MCsmallbee/PullMC)
[![仓库大小](https://img.shields.io/github/repo-size/MCsmallbee/PullMC?label=%E4%BB%93%E5%BA%93%E5%A4%A7%E5%B0%8F)](https://github.com/MCsmallbee/PullMC)

</div>

> [!IMPORTANT]
> 🎉 **PullMC 首个发行版已公布！** 当前版本 `0.0.0.20261102_base(Scaffold)`。
>
> 查看 [首个发行版庆祝公告](docs/ANNOUNCEMENT.md)，了解版本亮点、下载方式与后续路线。
>
> 此项目主要功能还处于**开发中**阶段，目前仅完成基础UI框架
>
> **敬请期待~**

> [!IMPORTANT]
> **重要**：本项目内大量代码采用**氛围编程 (Vibe Coding)** 方式编写；本项目内文档采用**AI辅助生成**，并经过**人工二次审核**，能保证内容的**真实性和准确性**。
> 
> 如果您排斥此类项目，请无视本项目，谢谢。


## 📖 项目概述

PullMC 是一个开源、非官方的 Minecraft Java 版下载与部署工具，面向希望以更轻量、更透明的方式管理游戏版本与文件的玩家。

它专注于三件事：

- 获取版本元数据
- 下载并校验游戏文件
- 将文件部署到你指定的目录

PullMC 不提供游戏账号、启动器或联机服务，也不会托管或镜像游戏资源。桌面端基于 Python、PySide6、QML 与 RinUI 构建，支持简体中文、繁体中文、English 和日本語，并跟随 Windows 主题。

当前处于 `base` 阶段：桌面 UI、首次启动向导和设置已完成；版本库、下载、校验与部署仍在开发中。

## 🗺️ 待办事项

- [x] 基础窗口UI布局实现
- [x] 设置页、关于页、多语言与版本命名
- [ ] Minecraft 版本清单获取与版本库
- [ ] 游戏文件下载、校验与部署
- [ ] 下载任务队列与进度
- [ ] 下载源、镜像与代理设置
- [ ] 模组加载器与模组下载
- [ ] 整合包安装支持

## ⚠️ 免责声明

PullMC 是一个开源的 Minecraft Java 版下载与部署工具，仅用于获取版本元数据、下载游戏文件并校验本地文件；不提供游戏账号、服务器或联机服务。

- 本项目不托管、不运营任何游戏资源下载站，也不镜像游戏文件。所有下载请求均由你的设备直接发往你选择的源（Mojang 官方、BMCLAPI 等公开镜像或加载器官方源），并写入你指定的本地目录。
- 本项目与 Microsoft、Mojang Studios 及其关联公司、代理商无隶属、合作、授权或背书关系。
- Minecraft 是 Mojang Studios 的商标；本项目名称仅用于说明兼容目标，不代表 Mojang Studios 的认可。
- 使用本项目前，你应已通过官方渠道合法取得 Minecraft: Java Edition 的使用授权，并遵守相关最终用户许可协议。
- 本项目按“现状”提供，不对第三方下载源的可用性、稳定性或安全性作任何担保；使用风险由你自行承担。

## ⚖️ 开源协议

版权所有 (c) 2026 MCsmallbee

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

简而言之：你可以自由使用、复制、修改、分发本项目的代码，但需保留版权声明，且作者不承担任何责任。

## 🏷️ 版本命名

当前版本：`0.0.0.20261102_base(Scaffold)`

版本号规则与阶段说明见 [docs/VERSIONING.md](docs/VERSIONING.md)。

## ⭐ 星标历史

<a href="https://www.star-history.com/?repos=mcsmallbee%2Fpullmc&type=date&legend=bottom-right">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=mcsmallbee/pullmc&type=date&theme=dark&legend=bottom-right" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=mcsmallbee/pullmc&type=date&legend=bottom-right" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=mcsmallbee/pullmc&type=date&legend=bottom-right" />
 </picture>
</a>