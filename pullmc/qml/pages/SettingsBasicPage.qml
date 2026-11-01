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

    Component.onCompleted: {
        syncNameMode()
        syncDisplayName()
        syncLanguage()
    }

    Connections {
        target: settings
        function onUseSystemDisplayNameChanged() { page.syncNameMode() }
        function onDisplayNameChanged() { page.syncDisplayName() }
        function onLanguageChanged() { page.syncLanguage() }
    }

    Connections {
        target: I18n
        function onRevisionChanged() {
            page.syncNameMode()
            page.syncLanguage()
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
    }
}
