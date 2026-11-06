import QtQuick
import QtQuick as Q
import QtQuick.Controls as Controls
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

        RowLayout {
            Layout.fillWidth: true
            spacing: 8

            Segmented {
                id: categories

                Layout.alignment: Qt.AlignVCenter
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
            }

            ToolButton {
                objectName: "libraryRefreshButton"
                Layout.alignment: Qt.AlignVCenter
                icon.name: "ic_fluent_arrow_clockwise_20_regular"
                enabled: library.state !== "loading"
                onClicked: library.refresh()
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
                spacing: 4
                clip: true

                Controls.ScrollBar.vertical: Controls.ScrollBar {
                    id: listScrollBar

                    policy: Controls.ScrollBar.AsNeeded
                    width: 8
                    background: Item {}

                    contentItem: Rectangle {
                        implicitWidth: 6
                        radius: 3
                        color: Theme.currentTheme.colors.textSecondaryColor
                        opacity: listScrollBar.pressed ? 0.85 : 0.45
                    }
                }

                delegate: SettingCard {
                    width: versionList.width
                    topPadding: 10
                    bottomPadding: 10
                    title: model.versionId
                    description: model.releaseText
                    icon.name: model.iconName
                    clickable: false
                }
            }
        }
    }

    Component.onCompleted: {
        if (library.state === "idle")
            library.refresh()
    }
}
