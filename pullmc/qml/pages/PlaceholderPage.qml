import QtQuick
import QtQuick.Layouts
import RinUI

FluentPage {
    id: page

    property string bodyText: ""

    Text {
        Layout.fillWidth: true
        text: page.bodyText
        typography: Typography.Body
        color: Theme.currentTheme.colors.textSecondaryColor
        wrapMode: Text.WordWrap
    }
}
