import QtQuick
import RinUI

Text {
    id: root

    property string heroText: ""
    property bool narrow: false

    text: heroText
    typography: narrow ? Typography.Title : Typography.TitleLarge
    color: Theme.currentTheme.colors.textColor
    width: Math.min(parent ? parent.width * 0.6 : 600, 760)
    wrapMode: Text.WordWrap
}
