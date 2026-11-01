import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI
import PullMC 1.0

FluentPage {
    id: page

    objectName: "settingsAppearancePage"
    title: I18n.t("settings.category.appearance.title", "外观设置")

    readonly property var themeCodes: ["Auto", "Light", "Dark"]
    readonly property var accentCodes: ["system", "custom"]
    readonly property var backdropCodes: ["mica", "tabbed", "acrylic", "none"]

    function colorHex(value) {
        return "#" + value.toString().slice(-6).toUpperCase()
    }

    function syncThemeMode() {
        themeBox.currentIndex = Math.max(0, page.themeCodes.indexOf(settings.themeMode))
    }

    function syncAccentMode() {
        accentBox.currentIndex = Math.max(0, page.accentCodes.indexOf(settings.accentMode))
    }

    function syncBackdrop() {
        backdropBox.currentIndex = Math.max(0, page.backdropCodes.indexOf(settings.backdropEffect))
    }

    Component.onCompleted: {
        syncThemeMode()
        syncAccentMode()
        syncBackdrop()
    }

    Connections {
        target: settings
        function onThemeModeChanged() { page.syncThemeMode() }
        function onAccentModeChanged() { page.syncAccentMode() }
        function onBackdropEffectChanged() { page.syncBackdrop() }
    }

    Connections {
        target: I18n
        function onRevisionChanged() {
            page.syncThemeMode()
            page.syncAccentMode()
            page.syncBackdrop()
        }
    }

    ColumnLayout {
        Layout.fillWidth: true
        spacing: 2

        SettingCard {
            Layout.fillWidth: true
            icon.name: "ic_fluent_dark_theme_20_regular"
            title: I18n.t("settings.themeMode.label", "颜色模式")
            description: I18n.t("settings.themeMode.description", "选择浅色、深色，或跟随 Windows。")

            ComboBox {
                id: themeBox
                Layout.preferredWidth: 220
                model: [
                    I18n.t("settings.themeMode.auto", "跟随系统"),
                    I18n.t("settings.themeMode.light", "浅色"),
                    I18n.t("settings.themeMode.dark", "深色")
                ]
                onActivated: bridge.setThemeMode(page.themeCodes[currentIndex])
            }
        }

        SettingCard {
            Layout.fillWidth: true
            icon.name: "ic_fluent_color_20_regular"
            title: I18n.t("settings.accentMode.label", "主题色")
            description: I18n.t("settings.accentMode.description", "默认跟随 Windows 强调色，也可以手动选择。")

            RowLayout {
                spacing: 8

                ComboBox {
                    id: accentBox
                    Layout.preferredWidth: 120
                    model: [
                        I18n.t("settings.accentMode.system", "跟随系统"),
                        I18n.t("settings.accentMode.custom", "自定义")
                    ]
                    onActivated: bridge.setAccentMode(page.accentCodes[currentIndex])
                }

                DropDownColorPicker {
                    Layout.preferredWidth: 120
                    visible: settings.accentMode === "custom"
                    color: settings.effectiveAccentColor
                    textVisible: true
                    hexText: true
                    onColorChanged: {
                        if (settings.accentMode !== "custom")
                            return
                        var hex = page.colorHex(color)
                        if (hex !== settings.accentColor)
                            bridge.setAccentColor(hex)
                    }
                }
            }
        }

        SettingCard {
            Layout.fillWidth: true
            icon.name: "ic_fluent_window_20_regular"
            title: I18n.t("settings.backdrop.label", "背景效果")
            description: I18n.t("settings.backdrop.description", "选择窗口背景材质；需要系统支持。")

            ComboBox {
                id: backdropBox
                Layout.preferredWidth: 220
                model: [
                    I18n.t("settings.backdrop.mica", "云母"),
                    I18n.t("settings.backdrop.tabbed", "云母（增强）"),
                    I18n.t("settings.backdrop.acrylic", "亚克力"),
                    I18n.t("settings.backdrop.none", "无")
                ]
                onActivated: bridge.setBackdropEffect(page.backdropCodes[currentIndex])
            }
        }
    }
}
