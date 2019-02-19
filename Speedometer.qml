import QtQuick 2.4
import QtGraphicalEffects 1.0

Rectangle {
    color: "transparent"

              SpeedNeedle {
                  id: speedoNeedle

                       anchors.verticalCenterOffset: 0
                       anchors.centerIn: parent

                       focus: true
                       Keys.onPressed: {
                                if (event.key == Qt.Key_Space && !event.isAutoRepeat) {
                                    speedoNeedle.value = 20
                                    rpmNeedle.value = 3000
                                    fuelNeedle.value = 75
                                    //innerring.info = "All good"
                                    drive()
                                }
                       }
                       Keys.onReleased: {
                               if (event.key == Qt.Key_Space && !event.isAutoRepeat) {
                                   speedoNeedle.value = 0
                                   rpmNeedle.value = 0
                                   fuelNeedle.value = 0.01
                               }}}

              RPMNeedle {
                  id: rpmNeedle
                  anchors.verticalCenterOffset: 0
                  anchors.centerIn: parent
                  value: 0
              }

              FuelNeedle {
                  id: fuelNeedle
                  anchors.verticalCenterOffset: 0
                  anchors.centerIn: parent
                  value: 0
              }

              InnerRing    {
                id: innerring
                speed: (Math.round(speedoNeedle.currentValue, 0) + 360) * 0.68
              }

              //Letter: P R N D
              Grid {
                  anchors.horizontalCenter: parent.horizontalCenter
                  y: parent.height - 65
                  columns: 4
                   Rectangle { color: "transparent"; width: 25; height: 25
                      Text {
                          id: letterP
                          text: " P "
                           font.family: "Eurostile"; font.pixelSize: 36
                          color: "white"
                          anchors.centerIn: parent
                      } }
                    Rectangle { color: "transparent"; width: 25; height: 25
                      Text {
                          text: " R "
                           font.family: "Eurostile"; font.pixelSize: 18
                          color: "darkgray"
                          anchors.centerIn: parent
                      }}
                    Rectangle { color: "transparent"; width: 25; height: 25
                          Text {
                              text: " N "
                               font.family: "Eurostile"; font.pixelSize: 18
                              color: "darkgray"
                              anchors.centerIn: parent
                          }}
                    Rectangle { color: "transparent"; width: 25; height: 25
                      Text {
                          id: letterD
                          text: " D "
                          font.family: "Eurostile"; font.pixelSize: 18
                          color: "darkgray"
                          anchors.centerIn: parent
                      }}
              }

              function drive() {
                  letterD.font.bold = true
                  letterD.color = "white"
                  letterD.font.pixelSize = 36
                  letterP.font.bold = false
                  letterP.color = "darkgray"
                  letterP.font.pixelSize = 18
              }


 }



