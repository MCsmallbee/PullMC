import QtQuick
import QtQuick as Q
import QtQuick.Layouts
import RinUI
import PullMC 1.0

FluentPage {
    id: page

    objectName: "libraryPage"
    title: I18n.t("nav.library", "版本库")

    readonly property var categoryKeys: ["release", "snapshot", "old", "april_fools"]

    ColumnLayout {
        Layout.fillWidth: true
        spacing: 14

        Segmented {
            id: categories

            Layout.alignment: Qt.AlignLeft
            currentIndex: 0

            SegmentedItem {
                text: I18n.t("library.category.release", "正式版")
            }
            SegmentedItem {
                text: I18n.t("library.category.snapshot", "快照版")
            }
            SegmentedItem {
                text: I18n.t("library.category.old", "远古版")
            }
            SegmentedItem {
                text: I18n.t("library.category.april_fools", "愚人节版")
            }

            onCurrentIndexChanged: {
                if (library)
                    library.setCategory(page.categoryKeys[currentIndex])
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.preferredHeight: Math.max(260, page.height - 190)

            Text {
                anchors.centerIn: parent
                visible: library.state === "idle" || library.state === "loading"
                text: I18n.t("library.loading", "正在获取版本清单…")
                color: Theme.currentTheme.colors.textSecondaryColor
                typography: Typography.Body
            }

            Column {
                anchors.centerIn: parent
                width: Math.min(parent.width - 48, 420)
                spacing: 10
                visible: library.state === "error"

                Text {
                    width: parent.width
                    text: I18n.t("library.error", "无法获取版本清单")
                    color: Theme.currentTheme.colors.textColor
                    typography: Typography.BodyStrong
                    horizontalAlignment: Text.AlignHCenter
                }
                Text {
                    width: parent.width
                    text: library.error
                    color: Theme.currentTheme.colors.textSecondaryColor
                    typography: Typography.Caption
                    wrapMode: Text.Wrap
                    horizontalAlignment: Text.AlignHCenter
                }
                Button {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: I18n.t("library.retry", "重试")
                    onClicked: library.refresh()
                }
            }

            Text {
                anchors.centerIn: parent
                visible: library.state === "ready" && library.count === 0
                text: I18n.t("library.empty", "没有可显示的版本。")
                color: Theme.currentTheme.colors.textSecondaryColor
                typography: Typography.Body
            }

            Q.ListView {
                id: versionList

                anchors.fill: parent
                visible: library.state === "ready" && library.count > 0
                model: versionModel
                spacing: 8
                clip: true

                delegate: SettingCard {
                    width: versionList.width
                    title: model.versionId
                    description: model.releaseText
                    icon.name: model.iconName
                    clickable: false
                }
            }
        }
    }

    Component.onCompleted: library.refresh()
}
