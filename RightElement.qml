import QtQuick 2.0
import QtGraphicalEffects 1.0

Rectangle {
    id: container
    width: parent.width
    height: parent.height
    color: "black"

    property int seconds
    property int tenseconds
    property int minutes

    Image {
        anchors.verticalCenter: parent.verticalCenter
        x: (parent.width - 250) - width/2
        fillMode: Image.PreserveAspectFit
        scale: 0.5
        source: "/pics/AndroidAuto.png"

        MouseArea {
                anchors.fill: parent
                onClicked: {
                    py_mainapp.startJob('test')
                }
       }

        Text {
            id:callTime
            y: 165; x: parent.width/1.2
            font.family: "Eurostile"; color: "white"; font.pixelSize: 20
            text: minutes + ":" + tenseconds + seconds
        }


    }

    Timer {
        //update Calltime, calculate 60 seconds into 1 minute etc.
           interval: 1000; running: true; repeat: true
           onTriggered: {seconds++;

           if(seconds == 10){
               tenseconds += 1
               seconds = 0
           }
           if(seconds == 0 && tenseconds==6){
               minutes += 1
               seconds = 0
               tenseconds = 0
           }
           }
       }
}

