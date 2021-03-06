import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Window 2.2

import QtQuick.Layouts 1.1

ApplicationWindow {
    title: qsTr("Tesla Model S Speedometer")
    width: 1400
    height: 600
    visible: true
    color: "black"




       QtObject {
           property var locale: Qt.locale()
           property date currentDate: new Date()
           property string dateString
           property string timeString

           Component.onCompleted: {
               dateString = currentDate.toLocaleDateString();
               timeString = currentDate.toLocaleTimeString();
           }
       }


       Image {
           width: parent.width
           height: parent.height
           source: "/pics/Background.png"
       }


       //Leiste unten
    Rectangle {
    y: parent.height - 90
    height: 200
    width: parent.width
    color: "transparent"
            RowLayout {
                   y: 50
                   x: parent.width/15
                   Text {
                       objectName: "totalKms"
                       text: "--"
                       font.pixelSize: 20
                       font.bold: true
                       color: "white"
                   }
                   Text {
                       text: "km"
                       font.pixelSize: 20
                       font.bold: false
                       color: "darkgray"
                   }
               }

            RowLayout {
                   y: -370
                   x: 15
                   Text {

                       text: "Coolant Temp: "
                       font.pixelSize: 20
                       font.bold: true
                       color: "white"
                   }
                   Text {
                       objectName: "enginTemp"
                       text: "--"
                       font.pixelSize: 20
                       font.bold: true
                       color: "darkgray"
                   }
                   Text {
                       text: "ºC"
                       font.pixelSize: 20
                       font.bold: false
                       color: "darkgray"
                   }
               }


            RowLayout {
                y: 50
                x: parent.width/1.5
                Text {
                    text: new Date().toLocaleDateString(Qt.locale(),"ddd") //ddd MMM d //h:mm AP
                    font.pixelSize: 20
                    font.bold: true
                    color: "white"
                }
                Text {
                    text: new Date().toLocaleDateString(Qt.locale(),"MMM d") //ddd MMM d //h:mm AP
                    font.pixelSize: 20
                    font.bold: false
                    color: "darkgray"
                }
            }

            RowLayout {
                y: 50
                x: parent.width/1.2
                Text {
                    text: new Date().toLocaleTimeString(Qt.locale(),"h:mm") //ddd MMM d //h:mm AP
                    font.pixelSize: 20
                    font.bold: false
                    color: "darkgray"
                }
                Text {
                    text: new Date().toLocaleTimeString(Qt.locale(),"AP") //ddd MMM d //h:mm AP
                    font.pixelSize: 20
                    font.bold: true
                    color: "white"
                }
            }
        }

//Tacho
    Image {
           height: parent.height
           width: height
           x: (parent.width / 2) - (width / 2)
           scale: 1.14
           source: "/pics/TachoRPM.png"
           fillMode: Image.PreserveAspectFit
    }

    Speedometer {
       height: 525
       width: height
       x: (parent.width / 2) - (width / 2)
       y: (parent.height / 2) - (height / 2)
    }


}


