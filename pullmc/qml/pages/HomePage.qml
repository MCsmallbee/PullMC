import QtQuick
import QtQuick.Layouts
import RinUI
import PullMC 1.0
import "../sections/home"

FluentPage {
    id: page

    title: I18n.tf(home.titleId, home.titleDefault, [home.displayName])
    horizontalPadding: 48

    Item {
        Layout.fillWidth: true
        Layout.preferredHeight: Math.max(300, page.height - 150)

        HomeWidgetHost {
            anchors.fill: parent
        }
    }

    pageFooter: Item {
        height: 110

        HomeCta {
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.rightMargin: 32
            anchors.bottomMargin: 32
            label: I18n.t("home.cta.download", "前往下载 Minecraft 版本")
            onActivated: bridge.requestLibrary()
        }
    }
}
