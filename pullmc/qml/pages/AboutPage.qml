import QtQuick
import QtQuick.Layouts
import RinUI
import PullMC 1.0

FluentPage {
    id: page

    title: I18n.t("nav.about", "关于")

    ColumnLayout {
        Layout.fillWidth: true
        spacing: 12

        Text {
            text: appInfo.name
            typography: Typography.Title
        }

        Text {
            text: I18n.t("about.version", "版本") + " " + appInfo.version
            typography: Typography.Body
            color: Theme.currentTheme.colors.textSecondaryColor
        }

        Text {
            text: I18n.t("about.license", "MIT License")
            typography: Typography.Body
            color: Theme.currentTheme.colors.textSecondaryColor
        }

        Text {
            Layout.fillWidth: true
            text: I18n.t("page.about.placeholder", "PullMC 是一个开源的 Minecraft Java 版下载与部署工具。")
            typography: Typography.Body
            color: Theme.currentTheme.colors.textSecondaryColor
            wrapMode: Text.WordWrap
        }
    }
}
