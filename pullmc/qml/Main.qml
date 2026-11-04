import QtQuick
import QtQuick.Layouts
import RinUI
import PullMC 1.0
import "dialogs"

FluentWindow {
    id: window

    visible: true
    width: 900
    height: 620
    minimumWidth: 900
    minimumHeight: 620
    readonly property bool showSettingsBack: navigationView.currentPage.indexOf("SettingsBasicPage") >= 0
        || navigationView.currentPage.indexOf("SettingsAppearancePage") >= 0
    readonly property bool isHomePage: navigationView.currentPage.indexOf("HomePage") >= 0
    readonly property bool backVisible: onboarding.visible ? onboarding.step > 0 : !isHomePage
    titleEnabled: false
    title: I18n.t("app.name", "PullMC")
    defaultPage: Qt.resolvedUrl("pages/HomePage.qml")
    navigationItems: window.buildNavigation()
    navigationView.objectName: "mainNavigation"

    function buildNavigation() {
        return [
            {
                title: I18n.t("nav.home", "主页"),
                page: Qt.resolvedUrl("pages/HomePage.qml"),
                icon: "ic_fluent_home_20_regular"
            },
            {
                title: I18n.t("nav.library", "版本库"),
                page: Qt.resolvedUrl("pages/LibraryPage.qml"),
                icon: "ic_fluent_box_multiple_20_regular"
            },
            {
                title: I18n.t("nav.tasks", "任务"),
                page: Qt.resolvedUrl("pages/TasksPage.qml"),
                icon: "ic_fluent_arrow_download_20_regular"
            },
            {
                title: I18n.t("nav.settings", "设置"),
                page: Qt.resolvedUrl("pages/SettingsPage.qml"),
                icon: "ic_fluent_settings_20_regular",
                position: Position.Bottom
            }
        ]
    }

    function refreshNavigation() {
        var page = navigationView.currentPage
        navigationItems = buildNavigation()
        if (page !== "" && navigationView.currentPage !== page)
            navigationView.safePush(page, true, true)
    }

    function navigateBack() {
        if (onboarding.visible) {
            onboarding.goBack()
            return
        }
        if (window.showSettingsBack) {
            navigationView.safePush(Qt.resolvedUrl("pages/SettingsPage.qml"), false, true)
            return
        }
        if (navigationView.lastPages.length > 0) {
            navigationView.safePop()
            return
        }
        if (!window.isHomePage)
            navigationView.safePush(Qt.resolvedUrl("pages/HomePage.qml"), false, true)
    }

    Connections {
        target: I18n
        function onRevisionChanged() {
            window.refreshNavigation()
        }
    }

    function applyAccent() {
        var color = bridge.currentAccent()
        Utils.primaryColor = color
        Theme.setThemeColor(color)
        Theme.setTheme(settings.themeMode)
    }

    function applyBackdrop() {
        if (typeof ThemeManager !== "undefined" && ThemeManager.apply_backdrop_effect)
            ThemeManager.apply_backdrop_effect(settings.backdropEffect)
    }

    Connections {
        target: bridge
        function onOpenLibraryRequested() {
            navigationView.safePush(Qt.resolvedUrl("pages/LibraryPage.qml"))
        }
        function onAppearanceChanged() {
            window.applyAccent()
        }
    }

    Connections {
        target: settings
        function onBackdropEffectChanged() {
            window.applyBackdrop()
        }
    }

    RowLayout {
        parent: window.titleBarLeadingHost
        height: parent.height
        spacing: 12

        Button {
            objectName: "backButton"
            width: 36
            height: 32
            flat: true
            icon.name: "ic_fluent_arrow_left_20_regular"
            visible: window.backVisible
            enabled: window.backVisible
            onClicked: window.navigateBack()
        }

        IconWidget {
            source: Qt.resolvedUrl("../res/logo.svg")
            size: 16
            enableColorOverlay: true
            color: Utils.primaryColor
        }

        Text {
            text: I18n.t("app.name", "PullMC")
            typography: Typography.Caption
            verticalAlignment: Text.AlignVCenter
        }
    }

    DisclaimerDialog {
        id: disclaimer
        onExitRequested: Qt.quit()
    }

    OnboardingWizard {
        id: onboarding
        anchors.fill: parent
        visible: settings.onboardingCompletedVersion < appInfo.onboardingVersion
        onFinished: visible = false
        onExitRequested: Qt.quit()
    }

    navigationView.visible: !onboarding.visible

    Component.onCompleted: {
        navigationItems = buildNavigation()
        navigationView.navigationBar.titleBarEnabled = false
        if (navigationView.currentPage === "")
            navigationView.safePush(defaultPage, false, true)
        window.applyAccent()
        window.applyBackdrop()
        bridge.applyAppearance()
        if (!onboarding.visible && settings.disclaimerAcceptedVersion < appInfo.disclaimerVersion)
            Qt.callLater(function() { disclaimer.open() })
        bridge.ping()
    }
}
