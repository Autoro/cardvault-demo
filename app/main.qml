import QtQuick 6.8
import QtQuick.Layouts 6.8
import QtQuick.Controls 6.8
import QtQuick.Window 6.8
import QtQuick.Controls.Material 6.8

import cardvault 1.0

ApplicationWindow {
    id: page
    title: "Card Vault Demo"
    width: 1280
    height: 720
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.Red

    CardVault {
        id: cardvault
    }

    GridLayout {
        anchors.fill: parent
        anchors.margins: 8
        columns: 2

        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredWidth: 300

            Text {
                Layout.alignment: Qt.AlignHCenter
                color: "white"
                text: "Settings"
            }

            GridLayout {
                columns: 2
                rows: 5

                Layout.fillWidth: true

                Label { text: "Source" }
                ComboBox {
                    textRole: "text"
                    valueRole: "value"
                    Component.onCompleted: currentIndex = indexOfValue(cardvault.selected_image)
                    model: cardvault.image_files
                    onActivated: cardvault.selected_image = currentValue
                }

                Label { text: "Display Mode" }
                ComboBox {
                    textRole: "text"
                    valueRole: "value"
                    Component.onCompleted: currentIndex = indexOfValue(cardvault.display_mode)
                    model: cardvault.display_modes
                    onActivated: cardvault.display_mode = currentValue
                }

                Label { text: "Contour" }
                Switch {
                    checked: cardvault.contoured
                    onClicked: cardvault.contoured = checked
                }

                Label { text: "Auto Threshold" }
                Switch {
                    id: autoThreshold
                    checked: cardvault.auto_threshold
                    onClicked: cardvault.auto_threshold = checked
                }

                Label { text: "Threshold"; visible: !autoThreshold.checked }
                Slider {
                    id: thresholdSlider
                    visible: !autoThreshold.checked
                    from: 0
                    value: cardvault.threshold
                    to: 255
                    stepSize: 1
                    snapMode: Slider.SnapAlways
                    onPressedChanged: if (!pressed) cardvault.threshold = value

                    Label {
                        anchors.left: parent.right;
                        anchors.verticalCenter: parent.verticalCenter
                        text: thresholdSlider.value}
                }

                Label { text: "Epsilon Factor" }
                ComboBox {
                    textRole: "text"
                    valueRole: "value"
                    Component.onCompleted: currentIndex = indexOfValue(cardvault.epsilon_factor)
                    model: cardvault.epsilon_factors
                    onActivated: cardvault.epsilon_factor = currentValue
                }

                Label { text: "Sides" }
                RangeSlider {
                    id: sidesSlider
                    from: 0
                    first.value: cardvault.min_sides
                    second.value: cardvault.max_sides
                    to: 10
                    stepSize: 1
                    snapMode: RangeSlider.SnapAlways
                    first.onPressedChanged: if(!first.pressed) cardvault.min_sides = first.value
                    second.onPressedChanged: if(!second.pressed) cardvault.max_sides = second.value

                    Label {
                        anchors.left: parent.right;
                        anchors.verticalCenter: parent.verticalCenter
                        text: parseInt(sidesSlider.first.value) + " - " + parseInt(sidesSlider.second.value)}
                }

                Label { text: "Min Area" }
                Slider {
                    id: areaSlider
                    from: 0
                    value: cardvault.min_area
                    to: 1000
                    stepSize: 100
                    snapMode: Slider.SnapAlways
                    onPressedChanged: if (!pressed) cardvault.min_area = value

                    Label {
                        anchors.left: parent.right;
                        anchors.verticalCenter: parent.verticalCenter
                        text: areaSlider.value}
                }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredWidth: 600

            Image {
                id: displayImage
                fillMode: Image.PreserveAspectFit
                source: cardvault.image
                width: 400
                height: 400
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.alignment: Qt.AlignCenter
            }
        }
    }
}