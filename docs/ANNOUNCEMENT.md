<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="img/logo_dark.svg">
    <img alt="PullMC Logo" src="img/logo.svg" width="112">
  </picture>
  <h1>🎉 PullMC 首个发行版公布</h1>
  <p><strong>0.0.0.20261102_base(Scaffold)</strong> · 2026 年 11 月 2 日</p>
</div>

> [!IMPORTANT]
> 这是 PullMC 的第一个公开预发行版，处于 `base` 阶段。
> 当前完成的是桌面 UI 框架、首次启动流程和基础设置；版本下载与部署能力仍在开发中。

---

## 从一张 LICENSE 开始

PullMC 的故事，开始于一个只有 `LICENSE` 的空仓库。

我们想要的东西并不复杂：一个**轻量、纯净、开源**的 Minecraft Java 版下载与部署工具。它不捆绑启动器，不接管账号，不替你做选择；它只负责把正确的版本元数据和游戏文件，安全、清楚地放到你指定的位置。

今天，这个想法第一次变成了可以下载、可以打开、可以点击的 Windows 应用。

## 这个版本带来了什么

- **原生桌面体验**：基于 PySide6 6.10、QML 与 RinUI 构建，跟随 Windows 的浅色/深色模式和强调色。
- **首次启动向导**：开源声明、显示名称、界面语言、外观设置，一步一步完成初始化。
- **完整的设置骨架**：基础设置、外观设置、窗口背景效果，以及可扩展的设置入口。
- **关于与版权信息**：项目信息、版本号、GitHub 仓库、MIT License、依赖与参考，以及只读的版权/免责声明弹窗。
- **四种界面语言**：简体中文、繁体中文、English、日本語，默认跟随系统。
- **清晰的版本规则**：采用 `主.副.修订.日期_阶段(Codename)`，并写入项目文档。
- **Windows x64 可移植包**：无需安装 Python，解压即可运行。

## 下载与运行

| 项目 | 内容 |
| --- | --- |
| 发行版本 | `0.0.0.20261102_base(Scaffold)` |
| 发行页 | [GitHub Releases](<https://github.com/MCsmallbee/PullMC/releases/tag/v0.0.0.20261102_base%28Scaffold%29>) |
| 发行包 | `PullMC_Windows-x64.zip`（约 164.5 MB） |
| 直接下载 | [PullMC_Windows-x64.zip](<https://github.com/MCsmallbee/PullMC/releases/download/v0.0.0.20261102_base%28Scaffold%29/PullMC_Windows-x64.zip>) |
| 系统要求 | Windows 10 / 11 x64 |

解压后运行 `PullMC.exe` 即可。当前发行包是免安装目录版，不包含安装器。

SHA256 校验值：

```text
BC38BCC1C8B041426A9077A74EBDC36CAF0DAE74BFBB6D47927869BC0AFAA406
```

> 可执行文件尚未进行代码签名。如果 Windows SmartScreen 弹出提示，请先核对下载来源和 SHA256，再决定是否运行。

## 现在可以做什么

- 打开 PullMC，完成首次启动向导
- 查看主页、版本库和任务页面（当前为占位页面）
- 切换界面语言、颜色模式和窗口背景效果
- 查看设置中的关于、版权信息与免责声明

## 现在还不能做什么

这个版本还只是**骨架**，不是完整的下载器：

- 还不能获取并展示 Minecraft 版本清单
- 还不能下载、校验或部署游戏文件
- 还不能安装加载器或整合包
- 还没有下载任务队列、断点续传、镜像源和代理设置

请暂时不要把它当作日常使用的下载工具。接下来的每一个 `alpha`，都会把这些能力逐步补齐。

## 下一站

- [ ] Minecraft 版本清单获取与版本库
- [ ] 游戏文件下载、校验与部署
- [ ] 加载器与整合包支持
- [ ] 下载任务队列与进度
- [ ] 下载源、镜像与代理设置
- [ ] 自动构建与发布流程

完整的阶段定义见 [`docs/VERSIONING.md`](VERSIONING.md)。

## 谢谢你们

感谢 Qt、PySide6 与 RinUI 提供了这次尝试的基础，感谢 Fluent UI System Icons 提供的图标资源，也感谢每一个愿意打开这个还很稚嫩的应用、提出问题和给出建议的人。

PullMC 会继续以 MIT License 开源。你可以自由使用、修改和分发它；如果它帮到了你，欢迎点一个 Star，或者来 Issues 里聊聊你希望它变成什么样。

## 写在最后

`base` 不是终点，`Scaffold` 也不只是一个代号。

它是骨架，是第一块地基，是从“想做一个工具”到“真的有人在用这个工具”之间，必须迈出的那一步。

下一个版本见。

---

**相关链接**

- [项目主页](../README.md)
- [版本命名规则](VERSIONING.md)
- [GitHub 仓库](https://github.com/MCsmallbee/PullMC)
- [首个发行版](<https://github.com/MCsmallbee/PullMC/releases/tag/v0.0.0.20261102_base%28Scaffold%29>)
