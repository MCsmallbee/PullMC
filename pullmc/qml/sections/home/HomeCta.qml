import QtQuick
import RinUI

Button {
    id: root

    property string label: ""
    signal activated()

    text: label
    highlighted: true
    implicitWidth: Math.max(150, labelText.implicitWidth + 32)
    implicitHeight: 46
    onClicked: activated()

    contentItem: Text {
        id: labelText
        text: root.label
        font: root.font
        color: root.highlighted ? "#FFFFFF" : Theme.currentTheme.colors.textColor
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
}
