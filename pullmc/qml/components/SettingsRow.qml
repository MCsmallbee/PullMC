import QtQuick
import QtQuick.Layouts
import RinUI

Frame {
    id: root

    property string icon: ""
    property string title: ""
    property string description: ""
    default property alias action: rightContent.data

    Layout.fillWidth: true
    padding: 0
    implicitHeight: content.implicitHeight + 24
    background: Rectangle {
        color: Theme.currentTheme.colors.cardColor
        radius: Theme.currentTheme.appearance.smallRadius
        border.width: 1
        border.color: Theme.currentTheme.colors.cardBorderColor
    }

    RowLayout {
        id: content
        anchors.fill: parent
        anchors.margins: 12
        spacing: 12

        Icon {
            Layout.alignment: Qt.AlignTop
            name: root.icon
            size: 20
            visible: root.icon.length > 0
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 1

            Text {
                Layout.fillWidth: true
                text: root.title
                typography: Typography.Body
                wrapMode: Text.WordWrap
            }

            Text {
                Layout.fillWidth: true
                visible: root.description.length > 0
                text: root.description
                typography: Typography.Caption
                color: Theme.currentTheme.colors.textSecondaryColor
                wrapMode: Text.WordWrap
                maximumLineCount: 2
                elide: Text.ElideRight
            }
        }

        RowLayout {
            id: rightContent
            Layout.alignment: Qt.AlignVCenter
            spacing: 8
        }
    }
}
