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
    titleEnabled: false
    title: I18n.t("app.name", "PullMC")
    defaultPage: Qt.resolvedUrl("pages/HomePage.qml")
    navigationItems: window.buildNavigation()
    navigationView.objectName: "mainNavigation"
    navigationView.navigationBar.windowIcon: Qt.resolvedUrl("../res/logo-title.svg")

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

    Connections {
        target: I18n
        function onRevisionChanged() {
            window.refreshNavigation()
        }
    }

    function syncBackButtonOpacity() {
        var host = window.titleBarLeadingHost
        if (!host || host.children.length === 0)
            return
        var row = host.children[0]
        for (var i = 0; i < row.children.length; i++) {
            var item = row.children[i]
            if (item.icon && item.icon.name === "ic_fluent_arrow_left_20_regular") {
                item.opacity = item.enabled ? 1.0 : 0.4
                return
            }
        }
    }

    Connections {
        target: navigationView
        function onLastPagesChanged() {
            window.syncBackButtonOpacity()
        }
        function onCurrentPageChanged() {
            if (navigationView.currentPage === window.defaultPage)
                navigationView.lastPages = []
            Qt.callLater(window.syncBackButtonOpacity)
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
        if (navigationView.currentPage === "")
            navigationView.safePush(defaultPage, false, true)
        window.applyAccent()
        window.applyBackdrop()
        bridge.applyAppearance()
        if (!onboarding.visible && settings.disclaimerAcceptedVersion < appInfo.disclaimerVersion)
            Qt.callLater(function() { disclaimer.open() })
        Qt.callLater(window.syncBackButtonOpacity)
        bridge.ping()
    }
}
