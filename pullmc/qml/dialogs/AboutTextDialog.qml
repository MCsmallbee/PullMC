import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI
import PullMC 1.0

Dialog {
    id: root
    objectName: "aboutTextDialog"

    property string heading: ""
    property string bodyText: ""
    property string okObjectName: "aboutDialogOk"

    title: root.heading
    modal: true
    closePolicy: Popup.CloseOnEscape
    width: 620
    height: 460
    padding: 24
    bottomPadding: 0
    background.layer.enabled: false

    contentItem: ColumnLayout {
        spacing: 12

        Text {
            Layout.fillWidth: true
            typography: Typography.Title
            text: root.heading
            wrapMode: Text.WordWrap
        }

        Flickable {
            id: bodyScroller
            objectName: "aboutDialogScroller"
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumHeight: 180
            contentWidth: width
            contentHeight: body.implicitHeight
            clip: true
            boundsBehavior: Flickable.StopAtBounds
            ScrollBar.vertical: ScrollBar {}

            Text {
                id: body
                objectName: "aboutDialogBody"
                width: bodyScroller.width
                text: root.bodyText
                textFormat: Text.PlainText
                wrapMode: Text.Wrap
                typography: Typography.Body
                lineHeightMode: Text.ProportionalHeight
                lineHeight: 1.35
                color: Theme.currentTheme.colors.textSecondaryColor
            }
        }
    }

    footer: DialogButtonBox {
        standardButtons: DialogButtonBox.NoButton
        padding: 16
        implicitHeight: 64

        contentItem: RowLayout {
            spacing: 8

            Item {
                Layout.fillWidth: true
            }

            Button {
                objectName: root.okObjectName
                text: I18n.t("common.ok", "确定")
                highlighted: true
                onClicked: root.close()
            }
        }
    }

    onOpened: {
        bodyScroller.contentY = 0
        Qt.callLater(function() { bodyScroller.contentY = 0 })
    }
    onVisibleChanged: {
        if (visible) {
            bodyScroller.contentY = 0
            Qt.callLater(function() { bodyScroller.contentY = 0 })
        }
    }
}
