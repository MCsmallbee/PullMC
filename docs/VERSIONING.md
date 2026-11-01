# PullMC 版本命名规则

PullMC 的公开版本号格式如下：

```text
主版本号.副版本号.修订号.日期版本号_阶段(Codename)
```

示例：

```text
0.0.0.20261102_base(Scaffold)
```

## 各段含义

| 段 | 示例 | 含义 |
| --- | --- | --- |
| 主版本号 | `0` | 功能模块或整体架构发生较大变化时递增。 |
| 副版本号 | `0` | 增加权限控制、自定义视图等功能时递增。 |
| 修订号 | `0` | Bug 修复或小型变更时递增；严重问题修复后可发布修订版。 |
| 日期版本号 | `20261102` | 当前修改日期，格式为 `YYYYMMDD`。每天修改项目都应更新。 |
| 阶段 | `base` | `base`、`alpha`、`beta`、`RC`、`release` 之一。 |
| Codename | `Scaffold` | 大版本或特殊版本代号，由开发者决定，通常使用英文。 |

## 阶段说明

- `base`：假页面链接阶段，页面和整体架构已建立，但功能尚未完整实现。
- `alpha`：初级版本，以功能实现为主，通常仅在开发者内部交流，Bug 较多。
- `beta`：消除了严重错误，主要进行 UI 与稳定性测试，可对外发布测试版。
- `RC`：候选发布版本，基本不存在阻断性 Bug，与正式版接近。
- `release`：最终交付版本。

## 当前版本

```text
0.0.0.20261102_base(Scaffold)
```

## 代码中的位置

- `pullmc/__init__.py`：
  - `__version__`：PEP 440 可用的纯数字版本，供打包元数据使用。
  - `__version_stage__`：阶段，例如 `base`。
  - `__version_codename__`：版本代号，例如 `Scaffold`。
  - `__version_label__`：界面展示的完整版本，例如 `0.0.0.20261102_base(Scaffold)`。
- `pullmc/app_info.py` 通过 `appInfo.version` 向 QML 暴露完整版本号。

发布新版本时，至少更新 `__version__`、`__version_stage__`、`__version_codename__` 中的对应部分，并同步本文件中的“当前版本”。
