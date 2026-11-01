import QtQuick
import QtQuick.Layouts
import RinUI
import PullMC 1.0

FluentPage {
    id: page

    objectName: "settingsPage"
    title: I18n.t("settings.page.title", "设置")

    ColumnLayout {
        Layout.fillWidth: true
        spacing: 2

        SettingCard {
            Layout.fillWidth: true
            icon.name: "ic_fluent_person_20_regular"
            title: I18n.t("settings.category.basic.title", "基础设置")
            description: I18n.t("settings.category.basic.description", "显示名称与界面语言。")
            clickable: true
            onClicked: page.Window.window.navigationView.pushStack(Qt.resolvedUrl("SettingsBasicPage.qml"))
        }

        SettingCard {
            Layout.fillWidth: true
            icon.name: "ic_fluent_color_20_regular"
            title: I18n.t("settings.category.appearance.title", "外观设置")
            description: I18n.t("settings.category.appearance.description", "颜色模式、主题色与背景效果。")
            clickable: true
            onClicked: page.Window.window.navigationView.pushStack(Qt.resolvedUrl("SettingsAppearancePage.qml"))
        }
    }
}
