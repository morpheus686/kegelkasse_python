import QtQuick
import QtQuick.Controls

ApplicationWindow {
    id: window
    width: 1500
    height: 1000
    visible: true

    Drawer {
        id: drawer
        width: 0.66 * window.width
        height: window.height
    }

    Label {
        id: content

        text: "Aa"
        font.pixelSize: 96
        anchors.fill: parent
        verticalAlignment: Label.AlignVCenter
        horizontalAlignment: Label.AlignHCenter

        transform: Translate {
            x: drawer.position * content.width * 0.33
        }
    }
}