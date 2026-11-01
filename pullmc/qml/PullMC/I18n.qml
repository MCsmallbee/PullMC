pragma Singleton

import QtQuick

QtObject {
    readonly property int revision: i18nBackend.revision

    function t(key, fallback) {
        revision // register a binding dependency for live language switches
        return i18nBackend.t(key, fallback)
    }

    function tf(key, fallback, args) {
        revision
        return i18nBackend.tf(key, fallback, args)
    }
}
