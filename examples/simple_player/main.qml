import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import mpvplayer 1.0

Window {
    width: 1280
    height: 720
    visible: true

    MpvPlayer {
        id: renderer
        anchors.fill: parent

        MouseArea {
            anchors.fill: parent
            onClicked: renderer.play("../videos/test.mkv")
        }
    }
}