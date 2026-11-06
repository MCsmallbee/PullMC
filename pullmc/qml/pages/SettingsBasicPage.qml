import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI
import PullMC 1.0

FluentPage {
    id: page

    objectName: "settingsBasicPage"
    title: I18n.t("settings.category.basic.title", "基础设置")

    readonly property var languageCodes: ["system", "zh_CN", "zh_TW", "en", "ja"]
    readonly property var mirrorCodes: ["auto", "mojang", "bmclapi"]

    function syncNameMode() {
        nameMode.currentIndex = settings.useSystemDisplayName ? 0 : 1
    }

    function syncDisplayName() {
        if (!nameField.activeFocus)
            nameField.text = settings.displayName
    }

    function syncLanguage() {
        languageBox.currentIndex = Math.max(0, page.languageCodes.indexOf(settings.language))
    }

    function syncMirror() {
        mirrorBox.currentIndex = Math.max(0, page.mirrorCodes.indexOf(settings.mirrorMode))
    }

    function syncTimeout() {
        timeoutBox.value = settings.requestTimeout
    }

    Component.onCompleted: {
        syncNameMode()
        syncDisplayName()
        syncLanguage()
        syncMirror()
        syncTimeout()
    }

    Connections {
        target: settings
        function onUseSystemDisplayNameChanged() { page.syncNameMode() }
        function onDisplayNameChanged() { page.syncDisplayName() }
        function onLanguageChanged() { page.syncLanguage() }
        function onMirrorModeChanged() { page.syncMirror() }
        function onRequestTimeoutChanged() { page.syncTimeout() }
    }

    Connections {
        target: I18n
        function onRevisionChanged() {
            page.syncNameMode()
            page.syncLanguage()
            page.syncMirror()
        }
    }

    ColumnLayout {
        Layout.fillWidth: true
        spacing: 2

        SettingCard {
            Layout.fillWidth: true
            icon.name: "ic_fluent_person_20_regular"
            title: I18n.t("settings.displayName.label", "显示名称")
            description: I18n.t("settings.displayName.description", "选择使用系统用户名，或输入自定义称呼。")

            RowLayout {
                spacing: 8

                ComboBox {
                    id: nameMode
                    Layout.preferredWidth: 180
                    model: [
                        I18n.t("settings.displayName.system", "使用系统用户名"),
                        I18n.t("settings.displayName.custom", "自定义")
                    ]
                    onActivated: {
                        if (currentIndex === 0) {
                            bridge.setUseSystemDisplayName(true)
                        } else {
                            bridge.setUseSystemDisplayName(false)
                            nameField.forceActiveFocus()
                        }
                    }
                }

                TextField {
                    id: nameField
                    Layout.preferredWidth: 170
                    enabled: !settings.useSystemDisplayName
                    placeholderText: settings.systemDisplayName
                    onEditingFinished: bridge.setDisplayName(text)
                }
            }
        }

        SettingCard {
            Layout.fillWidth: true
            icon.name: "ic_fluent_local_language_20_regular"
            title: I18n.t("settings.language.label", "界面语言")
            description: I18n.t("settings.language.description", "选择界面语言。跟随系统时使用 Windows 语言。")

            ComboBox {
                id: languageBox
                objectName: "languageBox"
                Layout.preferredWidth: 220
                model: [
                    I18n.t("settings.language.system", "跟随系统"),
                    "简体中文",
                    "繁體中文",
                    "English",
                    "日本語"
                ]
                onActivated: bridge.setLanguage(page.languageCodes[currentIndex])
            }
        }

        Text {
            Layout.topMargin: 12
            text: I18n.t("settings.versionFetch.heading", "获取 Minecraft 版本")
            typography: Typography.BodyStrong
        }

        SettingCard {
            Layout.fillWidth: true
            icon.name: "ic_fluent_cloud_20_regular"
            title: I18n.t("settings.mirror.label", "镜像源")
            description: I18n.t("settings.mirror.description", "选择获取版本清单的源；自动会先测速再选择。")

            ComboBox {
                id: mirrorBox
                objectName: "mirrorBox"
                Layout.preferredWidth: 220
                model: [
                    I18n.t("settings.mirror.auto", "自动"),
                    I18n.t("settings.mirror.mojang", "Mojang 官方"),
                    I18n.t("settings.mirror.bmclapi", "BMCLAPI 镜像")
                ]
                onActivated: bridge.setMirrorMode(page.mirrorCodes[currentIndex])
            }
        }

        SettingCard {
            Layout.fillWidth: true
            icon.name: "ic_fluent_timer_20_regular"
            title: I18n.t("settings.requestTimeout.label", "请求超时")
            description: I18n.t("settings.requestTimeout.description", "单次网络请求的超时时间，单位秒（5–60）。")

            SpinBox {
                id: timeoutBox
                objectName: "requestTimeoutBox"
                Layout.preferredWidth: 140
                from: 5
                to: 60
                stepSize: 5
                editable: true
                onValueModified: bridge.setRequestTimeout(value)
            }
        }
    }
}
