import QtQuick
import QtQuick.Layouts
import RinUI
import PullMC 1.0
import "../dialogs"

FluentPage {
    id: page

    objectName: "settingsPage"
    title: I18n.t("settings.page.title", "设置")

    readonly property string copyrightBody: [
        I18n.t("about.copyright.notice", "Copyright © 2026 MCsmallbee. 保留所有权利。"),
        I18n.t("about.copyright.license", "PullMC 以 MIT License 发布；源代码、文档及原创视觉资源的版权归 MCsmallbee 所有，另有说明的除外。"),
        I18n.t("about.copyright.body", "PullMC 是独立的开源项目。界面使用的部分图标来自 Microsoft Fluent UI System Icons，遵循其 MIT License；Minecraft 是 Mojang Studios 的商标。")
    ].join("\n\n")

    readonly property string disclaimerBody: [
        I18n.t("about.disclaimer.lead", "使用 PullMC 前，请了解以下声明。"),
        I18n.t("legal.disclaimer.body", "PullMC 是一个开源、非官方的 Minecraft Java 版下载与部署工具，仅提供版本元数据获取、文件下载与本地校验功能。"),
        "1. " + I18n.t("legal.disclaimer.item1", "本项目不托管、不运营游戏资源站，也不镜像游戏文件；下载请求由你的设备直接发往所选源（Mojang 官方、BMCLAPI 等公开镜像或加载器官方源），不经过本项目服务器。"),
        "2. " + I18n.t("legal.disclaimer.item2", "本项目与 Microsoft、Mojang Studios 及其关联公司、代理商无隶属、合作、授权或背书关系。"),
        "3. " + I18n.t("legal.disclaimer.item3", "Minecraft 是 Mojang Studios 的商标；本项目名称仅用于说明兼容目标，不代表 Mojang Studios 的认可。"),
        "4. " + I18n.t("legal.disclaimer.item4", "使用前，请确认你已通过官方渠道合法取得 Minecraft: Java Edition 的使用授权，并遵守其最终用户许可协议。"),
        "5. " + I18n.t("legal.disclaimer.item5", "本项目按“现状”提供，不对第三方下载源的可用性、稳定性或安全性作担保；使用风险由你自行承担。")
    ].join("\n\n")

    ColumnLayout {
        Layout.fillWidth: true
        spacing: 12

        Column {
            Layout.fillWidth: true
            spacing: 3

            Text {
                text: I18n.t("settings.category.heading", "设置")
                typography: Typography.BodyStrong
            }

            SettingCard {
                objectName: "settingsBasicCard"
                width: parent.width
                icon.name: "ic_fluent_options_20_regular"
                title: I18n.t("settings.category.basic.title", "常规设置")
                description: I18n.t("settings.category.basic.description", "显示名称、界面语言与版本获取。")
                clickable: true
                onClicked: page.Window.window.navigationView.push(Qt.resolvedUrl("SettingsBasicPage.qml"))
            }

            SettingCard {
                objectName: "settingsAppearanceCard"
                width: parent.width
                icon.name: "ic_fluent_color_20_regular"
                title: I18n.t("settings.category.appearance.title", "外观设置")
                description: I18n.t("settings.category.appearance.description", "颜色模式、主题色与窗口背景效果。")
                clickable: true
                onClicked: page.Window.window.navigationView.push(Qt.resolvedUrl("SettingsAppearancePage.qml"))
            }

            SettingCard {
                objectName: "settingsAdvancedCard"
                width: parent.width
                icon.name: "ic_fluent_code_20_regular"
                title: I18n.t("settings.category.advanced.title", "高级设置")
                description: I18n.t("settings.category.advanced.description", "调试控制台与日志。")
                clickable: true
                onClicked: page.Window.window.navigationView.push(Qt.resolvedUrl("SettingsAdvancedPage.qml"))
            }
        }

        Column {
            Layout.fillWidth: true
            spacing: 3

            Text {
                text: I18n.t("settings.category.about.heading", "关于")
                typography: Typography.BodyStrong
            }

            SettingExpander {
                objectName: "aboutExpander"
                width: parent.width
                title: appInfo.name
                description: I18n.t("about.summary", "PullMC 是一个开源的 Minecraft Java 版下载与部署工具。")
                icon.source: Qt.resolvedUrl("../../res/logo.svg")
                icon.size: 26
                contentFrame.color: Theme.currentTheme.colors.cardSecondaryColor

                content: Text {
                    color: Theme.currentTheme.colors.textSecondaryColor
                    text: I18n.t("about.version", "版本") + " " + appInfo.version
                }

                SettingItem {
                    title: I18n.t("about.repository", "GitHub 仓库")
                    description: I18n.t("about.repository.description", "查看源代码、提交问题或参与贡献。")
                    actionIcon.name: "ic_fluent_open_20_regular"
                    clickable: true
                    onClicked: Qt.openUrlExternally("https://github.com/MCsmallbee/PullMC")
                }

                SettingItem {
                    title: I18n.t("about.license", "MIT License")
                    description: I18n.t("about.license.description", "本项目使用 MIT License 开源。")

                    Hyperlink {
                        text: I18n.t("about.license", "MIT License")
                        openUrl: "https://github.com/MCsmallbee/PullMC/blob/main/LICENSE"
                    }
                }

                SettingItem {
                    objectName: "copyrightSetting"
                    title: I18n.t("about.copyright.title", "版权信息")
                    description: I18n.t("about.copyright.description", "查看版权、许可与第三方资源说明。")
                    actionIcon.name: "ic_fluent_info_20_regular"
                    clickable: true
                    onClicked: copyrightDialog.open()
                }

                SettingItem {
                    objectName: "disclaimerSetting"
                    title: I18n.t("about.disclaimer.title", "免责声明")
                    description: I18n.t("about.disclaimer.description", "查看使用 PullMC 前需要了解的声明。")
                    actionIcon.name: "ic_fluent_shield_20_regular"
                    clickable: true
                    onClicked: disclaimerDialog.open()
                }

                SettingItem {
                    Column {
                        objectName: "dependenciesSetting"
                        Layout.fillWidth: true
                        Layout.topMargin: 8
                        Layout.bottomMargin: 8
                        spacing: 2

                        Text {
                            text: I18n.t("about.dependencies", "依赖与参考")
                            typography: Typography.Body
                        }
                        Hyperlink {
                            text: I18n.t("about.dependency.qt", "Qt & Qt Quick")
                            openUrl: "https://www.qt.io/"
                        }
                        Hyperlink {
                            text: I18n.t("about.dependency.fluent", "Fluent Design System")
                            openUrl: "https://fluent2.microsoft.design/"
                        }
                        Hyperlink {
                            text: I18n.t("about.dependency.icons", "Fluent UI System Icons")
                            openUrl: "https://github.com/microsoft/fluentui-system-icons/"
                        }
                        Hyperlink {
                            text: I18n.t("about.dependency.rinui", "RinUI")
                            openUrl: "https://github.com/RinLit-233-shiroko/Rin-UI"
                        }
                    }
                }
            }
        }
    }

    AboutTextDialog {
        id: copyrightDialog
        objectName: "copyrightAboutDialog"
        heading: I18n.t("about.copyright.title", "版权信息")
        bodyText: page.copyrightBody
        okObjectName: "copyrightDialogOk"
    }

    AboutTextDialog {
        id: disclaimerDialog
        objectName: "disclaimerAboutDialog"
        heading: I18n.t("about.disclaimer.title", "免责声明")
        bodyText: page.disclaimerBody
        okObjectName: "disclaimerDialogOk"
    }
}
