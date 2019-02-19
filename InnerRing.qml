import QtQuick 2.0
import QtGraphicalEffects 1.0
Item {

    property int speed: 0


    height: 250 //TODO: Groesse skalierbar machen
    width: height
    x: (parent.width / 2) - (width / 2)
    y: (parent.height / 2) - (height / 2)


    Image {
         id: innerRingRect
         height: parent.height
         width: parent.width
         source: "/pics/Tacho_Mitte.png"


         Text {
             id: speeddigit
             text: speed
             font.pixelSize: 64
             font.bold: true
             font.family: "Eurostile"
             y: 50
             color: "white"
             anchors.horizontalCenter: parent.horizontalCenter
         }

         DropShadow {
                 anchors.fill: speeddigit
                 horizontalOffset: 0
                 verticalOffset: 8
                 radius: 4.0
                 samples: 16
                 color: "black"
                 source: speeddigit
             }

         Text {
             text: "km/h"
             font.pixelSize: 12
             font.bold: true
             font.family: "Eurostile"
             y: 130
             color: "white"
             anchors.horizontalCenter: parent.horizontalCenter
         }


         Text {
             text: "209"
             font.pixelSize: 25
             font.bold: true
             font.family: "Eurostile"
             y: 170
             color: "white"
             anchors.horizontalCenter: parent.horizontalCenter
         }

         Text {
             text: "Total covered"
             font.pixelSize: 13
             font.bold: true
             font.family: "Eurostile"
             y: 200
             color: "#666666"
             anchors.horizontalCenter: parent.horizontalCenter
         }

    }
}
