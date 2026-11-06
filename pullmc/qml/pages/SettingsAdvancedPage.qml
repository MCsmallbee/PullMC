import QtQuick
import QtQuick.Layouts
import RinUI
import PullMC 1.0

FluentPage {
    id: page

    objectName: "settingsAdvancedPage"
    title: I18n.t("settings.category.advanced.title", "高级设置")

    Component.onCompleted: {
        consoleSwitch.checked = settings.consoleEnabled
    }

    Connections {
        target: settings
        function onConsoleEnabledChanged() {
            consoleSwitch.checked = settings.consoleEnabled
        }
    }

    ColumnLayout {
        Layout.fillWidth: true
        spacing: 2

        Text {
            Layout.topMargin: 4
            text: I18n.t("settings.advanced.heading", "调试")
            typography: Typography.BodyStrong
        }

        SettingCard {
            Layout.fillWidth: true
            icon.name: "ic_fluent_code_20_regular"
            title: I18n.t("settings.console.label", "调试控制台")
            description: I18n.t("settings.console.description", "打开独立的控制台窗口，实时显示本次运行的日志。")

            Switch {
                id: consoleSwitch
                objectName: "consoleSwitch"
                text: ""
                checkedText: ""
                uncheckedText: ""
                onToggled: {
                    if (!bridge.setConsoleEnabled(checked))
                        checked = settings.consoleEnabled
                }
            }
        }
    }
}
