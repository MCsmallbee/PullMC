import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI
import PullMC 1.0

Item {
    id: wizard
    objectName: "onboardingWizard"

    property int step: 0
    property bool termsAccepted: false
    property bool contentAtBottom: false
    property bool contentScrollable: false
    property string errorText: ""

    readonly property var languageCodes: ["system", "zh_CN", "zh_TW", "en", "ja"]
    readonly property var backdropCodes: ["mica", "tabbed", "acrylic", "none"]

    signal finished()
    signal exitRequested()

    function colorHex(value) {
        return "#" + value.toString().slice(-6).toUpperCase()
    }

    function syncLanguage() {
        languageBox.currentIndex = Math.max(0, languageCodes.indexOf(settings.language))
    }

    function syncBackdrop() {
        backdropBox.currentIndex = Math.max(0, backdropCodes.indexOf(settings.backdropEffect))
    }

    Component.onCompleted: {
        wizard.syncLanguage()
        wizard.syncBackdrop()
    }

    Connections {
        target: settings
        function onLanguageChanged() { wizard.syncLanguage() }
        function onBackdropEffectChanged() { wizard.syncBackdrop() }
    }

    Connections {
        target: I18n
        function onRevisionChanged() {
            wizard.syncLanguage()
            wizard.syncBackdrop()
        }
    }

    function canAdvance() {
        if (step === 1)
            return termsAccepted && (!contentScrollable || contentAtBottom)
        return true
    }

    function advance() {
        errorText = ""
        if (step === 0) {
            step = 1
            return
        }
        if (step === 1) {
            if (!termsAccepted || (contentScrollable && !contentAtBottom)) {
                errorText = I18n.t("legal.disclaimer.scroll_hint", "请滚动阅读到底部后勾选")
                return
            }
            if (!bridge.acceptDisclaimer(appInfo.disclaimerVersion)) {
                errorText = I18n.t("legal.disclaimer.save_error", "无法保存确认状态，请检查磁盘权限后重试。")
                return
            }
        }
        if (step === 2) {
            if (!settings.useSystemDisplayName && !bridge.setDisplayName(nameField.text)) {
                errorText = I18n.t("legal.disclaimer.save_error", "无法保存确认状态，请检查磁盘权限后重试。")
                return
            }
        }
        if (step < 4) {
            step += 1
            return
        }
        if (!bridge.completeOnboarding()) {
            errorText = I18n.t("legal.disclaimer.save_error", "无法保存确认状态，请检查磁盘权限后重试。")
            return
        }
        finished()
    }

    function goBack() {
        errorText = ""
        if (step > 0)
            step -= 1
    }

    visible: false
    z: 1000

    ColumnLayout {
        width: Math.min(parent.width - 64, 760)
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 24
        anchors.bottomMargin: 24
        spacing: 6

                Item {
                    Layout.fillWidth: true
                    Layout.preferredHeight: steps.implicitHeight
                    visible: wizard.step > 0

                    Segmented {
                        id: steps
                        anchors.centerIn: parent
                        currentIndex: Math.max(0, wizard.step - 1)

                        SegmentedItem { text: I18n.t("onboarding.tab.terms", "协议") }
                        SegmentedItem { text: I18n.t("onboarding.tab.basic", "基础") }
                        SegmentedItem { text: I18n.t("onboarding.tab.appearance", "外观") }
                        SegmentedItem { text: I18n.t("onboarding.tab.done", "完成") }
                    }

                    MouseArea {
                        anchors.fill: parent
                        acceptedButtons: Qt.AllButtons
                        hoverEnabled: false
                        onPressed: mouse.accepted = true
                    }
                }

                StackLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    currentIndex: wizard.step

                    // ------------------------------------------------- welcome
                    Item {
                        ColumnLayout {
                            anchors.centerIn: parent
                            width: Math.min(520, parent.width)
                            spacing: 16

                            Text {
                                Layout.fillWidth: true
                                text: I18n.t("onboarding.welcome.title", "欢迎使用 PullMC")
                                typography: Typography.TitleLarge
                                horizontalAlignment: Text.AlignHCenter
                            }

                            Text {
                                Layout.fillWidth: true
                                text: I18n.t("onboarding.welcome.body", "一个开源、非官方的 Minecraft Java 版下载与部署工具。")
                                typography: Typography.BodyLarge
                                color: Theme.currentTheme.colors.textSecondaryColor
                                horizontalAlignment: Text.AlignHCenter
                                wrapMode: Text.WordWrap
                            }

                            Button {
                                Layout.alignment: Qt.AlignHCenter
                                text: I18n.t("onboarding.welcome.start", "开始设置")
                                highlighted: true
                                onClicked: wizard.advance()
                            }
                        }
                    }

                    // --------------------------------------------------- terms
                    Item {
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: 10

                            Text {
                                text: I18n.t("onboarding.terms.title", "开源声明")
                                typography: Typography.Title
                            }

                            Flickable {
                                id: termsFlick
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                Layout.minimumHeight: 170
                                clip: true
                                contentWidth: width
                                contentHeight: termsColumn.implicitHeight
                                boundsBehavior: Flickable.StopAtBounds

                                property bool scrollable: contentHeight > height + 1
                                property bool atBottom: !scrollable || contentY >= contentHeight - height - 2

                                onScrollableChanged: {
                                    wizard.contentScrollable = scrollable
                                    if (!scrollable) wizard.contentAtBottom = true
                                }
                                onAtBottomChanged: {
                                    wizard.contentAtBottom = atBottom
                                }
                                Component.onCompleted: {
                                    wizard.contentScrollable = scrollable
                                    wizard.contentAtBottom = atBottom
                                }

                                ColumnLayout {
                                    id: termsColumn
                                    width: termsFlick.width
                                    spacing: 12

                                    Text {
                                        Layout.fillWidth: true
                                        text: I18n.t("legal.disclaimer.lead", "首次使用前，请阅读并确认以下内容。")
                                        typography: Typography.BodyStrong
                                        wrapMode: Text.WordWrap
                                    }

                                    Text {
                                        Layout.fillWidth: true
                                        text: I18n.t("legal.disclaimer.body", "")
                                        typography: Typography.Body
                                        color: Theme.currentTheme.colors.textSecondaryColor
                                        wrapMode: Text.WordWrap
                                    }

                                    Repeater {
                                        model: 5
                                        Text {
                                            Layout.fillWidth: true
                                            text: I18n.t("legal.disclaimer.item" + (index + 1), "")
                                            typography: Typography.Body
                                            wrapMode: Text.WordWrap
                                        }
                                    }
                                }

                                ScrollBar.vertical: ScrollBar {
                                    policy: termsFlick.scrollable ? ScrollBar.AsNeeded : ScrollBar.AlwaysOff
                                }
                            }

                            Item {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 18

                                Text {
                                    anchors.fill: parent
                                    text: I18n.t("legal.disclaimer.scroll_hint", "请滚动阅读到底部后勾选")
                                    typography: Typography.Caption
                                    color: Theme.currentTheme.colors.textSecondaryColor
                                    visible: termsFlick.scrollable && !termsFlick.atBottom
                                }
                            }

                            CheckBox {
                                id: termsCheck
                                text: I18n.t("legal.disclaimer.accept", "我已阅读并理解上述声明")
                                enabled: !termsFlick.scrollable || termsFlick.atBottom
                                checked: wizard.termsAccepted
                                onToggled: wizard.termsAccepted = checked
                            }
                        }
                    }

                    // --------------------------------------------------- basic
                    Item {
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: 6

                            Text {
                                text: I18n.t("onboarding.basic.title", "基础设置")
                                typography: Typography.Title
                            }

                            Text {
                                Layout.fillWidth: true
                                text: I18n.t("onboarding.basic.description", "先设置称呼和界面语言，之后随时可以修改。")
                                typography: Typography.Body
                                color: Theme.currentTheme.colors.textSecondaryColor
                                wrapMode: Text.WordWrap
                            }

                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: 2

                                SettingCard {
                                    Layout.fillWidth: true
                                    icon.name: "ic_fluent_person_20_regular"
                                    title: I18n.t("settings.displayName.label", "显示名称")
                                    description: I18n.t("settings.displayName.description", "留空时自动使用系统用户名。")

                                    RowLayout {
                                        spacing: 10

                                        ComboBox {
                                            id: accountModeBox
                                            Layout.preferredWidth: 180
                                            model: [
                                                I18n.t("settings.displayName.system", "使用系统用户名"),
                                                I18n.t("settings.displayName.custom", "自定义")
                                            ]
                                            currentIndex: settings.useSystemDisplayName ? 0 : 1
                                            onActivated: bridge.setUseSystemDisplayName(currentIndex === 0)
                                        }

                                        TextField {
                                            id: nameField
                                            Layout.preferredWidth: 190
                                            text: settings.displayName
                                            placeholderText: settings.systemDisplayName
                                            enabled: !settings.useSystemDisplayName
                                        }
                                    }
                                }

                                SettingCard {
                                    Layout.fillWidth: true
                                    icon.name: "ic_fluent_local_language_20_regular"
                                    title: I18n.t("settings.language.label", "界面语言")
                                    description: I18n.t("settings.language.description", "选择界面语言。跟随系统时使用 Windows 语言。")

                                    ComboBox {
                                        id: languageBox
                                        objectName: "wizardLanguageBox"
                                        Layout.preferredWidth: 220
                                        model: [
                                            I18n.t("settings.language.system", "跟随系统"),
                                            "简体中文",
                                            "繁體中文",
                                            "English",
                                            "日本語"
                                        ]
                                        onActivated: bridge.setLanguage(wizard.languageCodes[currentIndex])
                                    }
                                }
                            }

                            Item { Layout.fillHeight: true }
                        }
                    }

                    // ----------------------------------------------- appearance
                    Item {
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: 6

                            Text {
                                text: I18n.t("onboarding.appearance.title", "外观")
                                typography: Typography.Title
                            }

                            Text {
                                Layout.fillWidth: true
                                text: I18n.t("onboarding.appearance.description", "选择颜色模式和主题色。默认跟随 Windows。")
                                typography: Typography.Body
                                color: Theme.currentTheme.colors.textSecondaryColor
                                wrapMode: Text.WordWrap
                            }

                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: 2

                                SettingCard {
                                    Layout.fillWidth: true
                                    icon.name: "ic_fluent_dark_theme_20_regular"
                                    title: I18n.t("settings.themeMode.label", "颜色模式")
                                    description: I18n.t("settings.themeMode.description", "选择浅色、深色，或跟随 Windows。")

                                    ComboBox {
                                        Layout.preferredWidth: 220
                                        model: [
                                            I18n.t("settings.themeMode.auto", "跟随系统"),
                                            I18n.t("settings.themeMode.light", "浅色"),
                                            I18n.t("settings.themeMode.dark", "深色")
                                        ]
                                        currentIndex: Math.max(0, ["Auto", "Light", "Dark"].indexOf(settings.themeMode))
                                        onActivated: bridge.setThemeMode(["Auto", "Light", "Dark"][currentIndex])
                                    }
                                }

                                SettingCard {
                                    Layout.fillWidth: true
                                    icon.name: "ic_fluent_color_20_regular"
                                    title: I18n.t("settings.accentMode.label", "主题色")
                                    description: I18n.t("settings.accentMode.description", "默认跟随 Windows 强调色，也可以手动选择。")

                                    RowLayout {
                                        spacing: 12

                                        ComboBox {
                                            Layout.preferredWidth: 180
                                            model: [
                                                I18n.t("settings.accentMode.system", "跟随系统"),
                                                I18n.t("settings.accentMode.custom", "自定义")
                                            ]
                                            currentIndex: Math.max(0, ["system", "custom"].indexOf(settings.accentMode))
                                            onActivated: bridge.setAccentMode(["system", "custom"][currentIndex])
                                        }

                                        DropDownColorPicker {
                                            visible: settings.accentMode === "custom"
                                            color: settings.effectiveAccentColor
                                            textVisible: true
                                            hexText: true
                                            onColorChanged: {
                                                if (settings.accentMode !== "custom")
                                                    return
                                                var hex = wizard.colorHex(color)
                                                if (hex !== settings.accentColor)
                                                    bridge.setAccentColor(hex)
                                            }
                                        }
                                    }
                                }

                                Text {
                                    Layout.fillWidth: true
                                    text: I18n.t("settings.accentColor.description", "选择后立即应用到界面。")
                                    typography: Typography.Caption
                                    color: Theme.currentTheme.colors.textSecondaryColor
                                    visible: settings.accentMode === "custom"
                                }

                                SettingCard {
                                    Layout.fillWidth: true
                                    icon.name: "ic_fluent_square_hint_sparkles_20_regular"
                                    title: I18n.t("settings.backdrop.label", "窗口背景效果")
                                    description: I18n.t("settings.backdrop.description", "选择窗口背景材质，需要系统支持。")

                                    ComboBox {
                                        id: backdropBox
                                        Layout.preferredWidth: 220
                                        model: [
                                            I18n.t("settings.backdrop.mica", "云母"),
                                            I18n.t("settings.backdrop.tabbed", "云母（增强）"),
                                            I18n.t("settings.backdrop.acrylic", "亚克力"),
                                            I18n.t("settings.backdrop.none", "无")
                                        ]
                                        onActivated: bridge.setBackdropEffect(wizard.backdropCodes[currentIndex])
                                    }
                                }
                            }

                            Item { Layout.fillHeight: true }
                        }
                    }

                    // ---------------------------------------------------- done
                    Item {
                        ColumnLayout {
                            anchors.centerIn: parent
                            width: Math.min(520, parent.width)
                            spacing: 16

                            Text {
                                Layout.fillWidth: true
                                text: I18n.t("onboarding.done.title", "设置完成")
                                typography: Typography.TitleLarge
                                horizontalAlignment: Text.AlignHCenter
                            }

                            Text {
                                Layout.fillWidth: true
                                text: I18n.t("onboarding.done.body", "一切就绪。你可以随时在设置中修改这些选项。")
                                typography: Typography.BodyLarge
                                color: Theme.currentTheme.colors.textSecondaryColor
                                horizontalAlignment: Text.AlignHCenter
                                wrapMode: Text.WordWrap
                            }

                            Button {
                                Layout.alignment: Qt.AlignHCenter
                                text: I18n.t("onboarding.done.start", "进入 PullMC")
                                highlighted: true
                                onClicked: wizard.advance()
                            }
                        }
                    }
                }

                Text {
                    Layout.fillWidth: true
                    text: wizard.errorText
                    typography: Typography.Caption
                    color: Theme.currentTheme.colors.systemCriticalColor
                    wrapMode: Text.WordWrap
                    visible: wizard.errorText.length > 0
                }

                RowLayout {
                    Layout.fillWidth: true
                    visible: wizard.step > 0 && wizard.step < 4
                    spacing: 10

                    Button {
                        text: I18n.t("onboarding.back", "上一步")
                        visible: wizard.step > 0 && wizard.step < 4
                        onClicked: wizard.goBack()
                    }

                    Item { Layout.fillWidth: true }

                    Button {
                        text: wizard.step === 0
                            ? I18n.t("onboarding.welcome.start", "开始设置")
                            : (wizard.step === 4
                                ? I18n.t("onboarding.done.start", "进入 PullMC")
                                : I18n.t("onboarding.next", "下一步"))
                        highlighted: true
                        enabled: wizard.canAdvance()
                        onClicked: wizard.advance()
                    }
                }
    }
}
