import QtQuick
import QtQuick.Controls

ApplicationWindow {
    id: window
    width: 1500
    height: 1000
    visible: true

    TableView {
        id: penaltytable
        anchors.fill: parent
        alternatingRows: true
    }
}