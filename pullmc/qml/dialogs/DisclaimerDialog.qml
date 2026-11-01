import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI
import PullMC 1.0

Dialog {
    id: root
    objectName: "disclaimerDialog"

    title: root.tr("legal.disclaimer.title", "PullMC 开源声明")
    modal: true
    closePolicy: Popup.NoAutoClose
    width: 620
    height: Math.min(460, (Overlay.overlay ? Overlay.overlay.height : 800) - 48)
    bottomPadding: 0
    background.layer.enabled: false

    property bool accepted: false
    property string errorText: ""
    signal exitRequested()

    readonly property bool contentScrollable: scroller.contentHeight > scroller.height + 1
    readonly property bool contentAtBottom: !contentScrollable
        || scroller.contentY >= scroller.contentHeight - scroller.height - 1

    function tr(key, fallback) {
        // Touching revision keeps every label in sync with a live language switch.
        I18n.revision
        return I18n.t(key, fallback)
    }

    function accept() {
        root.errorText = ""
        if (!acceptBox.checked || !root.contentAtBottom)
            return
        if (bridge.acceptDisclaimer(appInfo.disclaimerVersion)) {
            root.accepted = true
            root.close()
        } else {
            root.errorText = root.tr(
                "legal.disclaimer.save_error",
                "无法保存确认状态，请检查磁盘权限后重试。"
            )
        }
    }

    contentItem: ColumnLayout {
        spacing: 12

        Text {
            Layout.fillWidth: true
            typography: Typography.Title
            text: root.tr("legal.disclaimer.title", "PullMC 开源声明")
            wrapMode: Text.WordWrap
        }

        Text {
            Layout.fillWidth: true
            typography: Typography.BodyStrong
            text: root.tr("legal.disclaimer.lead", "首次使用前，请阅读并确认以下内容。")
            wrapMode: Text.WordWrap
        }

        Text {
            Layout.fillWidth: true
            typography: Typography.Body
            text: root.tr(
                "legal.disclaimer.body",
                "PullMC 是一个开源、非官方的 Minecraft Java 版下载与部署工具，仅提供版本元数据获取、文件下载与本地校验功能。"
            )
            wrapMode: Text.WordWrap
            color: Theme.currentTheme.colors.textSecondaryColor
        }

        Flickable {
            id: scroller
            objectName: "disclaimerScroller"
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumHeight: 140
            Layout.preferredHeight: 240
            contentWidth: width
            contentHeight: items.implicitHeight
            clip: true
            boundsBehavior: Flickable.StopAtBounds
            ScrollBar.vertical: ScrollBar {}

            ColumnLayout {
                id: items
                width: scroller.width
                spacing: 10

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 8
                    Text {
                        text: "1."
                        typography: Typography.Body
                        Layout.alignment: Qt.AlignTop
                    }
                    Text {
                        Layout.fillWidth: true
                        typography: Typography.Body
                        text: root.tr(
                            "legal.disclaimer.item1",
                            "本项目不托管、不运营游戏资源站，也不镜像游戏文件；下载请求由你的设备直接发往所选源（Mojang 官方、BMCLAPI 等公开镜像或加载器官方源），不经过本项目服务器。"
                        )
                        wrapMode: Text.WordWrap
                        color: Theme.currentTheme.colors.textSecondaryColor
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 8
                    Text {
                        text: "2."
                        typography: Typography.Body
                        Layout.alignment: Qt.AlignTop
                    }
                    Text {
                        Layout.fillWidth: true
                        typography: Typography.Body
                        text: root.tr(
                            "legal.disclaimer.item2",
                            "本项目与 Microsoft、Mojang Studios 及其关联公司、代理商无隶属、合作、授权或背书关系。"
                        )
                        wrapMode: Text.WordWrap
                        color: Theme.currentTheme.colors.textSecondaryColor
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 8
                    Text {
                        text: "3."
                        typography: Typography.Body
                        Layout.alignment: Qt.AlignTop
                    }
                    Text {
                        Layout.fillWidth: true
                        typography: Typography.Body
                        text: root.tr(
                            "legal.disclaimer.item3",
                            "Minecraft 是 Mojang Studios 的商标；本项目名称仅用于说明兼容目标，不代表 Mojang Studios 的认可。"
                        )
                        wrapMode: Text.WordWrap
                        color: Theme.currentTheme.colors.textSecondaryColor
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 8
                    Text {
                        text: "4."
                        typography: Typography.Body
                        Layout.alignment: Qt.AlignTop
                    }
                    Text {
                        Layout.fillWidth: true
                        typography: Typography.Body
                        text: root.tr(
                            "legal.disclaimer.item4",
                            "使用前，请确认你已通过官方渠道合法取得 Minecraft: Java Edition 的使用授权，并遵守其最终用户许可协议。"
                        )
                        wrapMode: Text.WordWrap
                        color: Theme.currentTheme.colors.textSecondaryColor
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 8
                    Text {
                        text: "5."
                        typography: Typography.Body
                        Layout.alignment: Qt.AlignTop
                    }
                    Text {
                        Layout.fillWidth: true
                        typography: Typography.Body
                        text: root.tr(
                            "legal.disclaimer.item5",
                            "本项目按“现状”提供，不对第三方下载源的可用性、稳定性或安全性作担保；使用风险由你自行承担。"
                        )
                        wrapMode: Text.WordWrap
                        color: Theme.currentTheme.colors.textSecondaryColor
                    }
                }
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.preferredHeight: 18

            Text {
                anchors.fill: parent
                visible: root.contentScrollable && !root.contentAtBottom
                text: root.tr(
                    "legal.disclaimer.scroll_hint",
                    "请滚动阅读到底部后勾选"
                )
                typography: Typography.Caption
                color: Theme.currentTheme.colors.textSecondaryColor
                wrapMode: Text.WordWrap
            }
        }

        CheckBox {
            id: acceptBox
            objectName: "disclaimerAccept"
            Layout.fillWidth: true
            enabled: root.contentAtBottom
            text: root.tr("legal.disclaimer.accept", "我已阅读并理解上述声明")
            onCheckedChanged: if (checked) root.errorText = ""
        }

        Text {
            Layout.fillWidth: true
            visible: root.errorText !== ""
            text: root.errorText
            typography: Typography.Caption
            color: Theme.currentTheme.colors.systemCriticalColor
            wrapMode: Text.WordWrap
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
                text: root.tr("legal.disclaimer.exit", "退出")
                onClicked: root.exitRequested()
            }

            Button {
                text: root.tr("legal.disclaimer.continue", "同意并继续")
                highlighted: true
                enabled: acceptBox.checked && root.contentAtBottom
                onClicked: root.accept()
            }
        }
    }

    Shortcut {
        sequence: "Escape"
        onActivated: root.exitRequested()
    }

    onClosed: {
        if (!root.accepted)
            root.exitRequested()
    }
    onOpened: {
        scroller.contentY = 0
        acceptBox.forceActiveFocus()
    }
}
