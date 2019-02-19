import QtQuick 2.4
import QtGraphicalEffects 1.0

Canvas {
    id: canvas

    property int value : 0

    onValueChanged: {

        var rotate = -150 +  Math.min(canvas.value,80)* 120/80//Math.min(Math.max(-250, canvas.value*3.5 - 149), -30);
        if(canvas.value>80)
            rotate += Math.min((canvas.value - 80),20)* 15/20
        if(canvas.value>100)
            rotate +=  Math.min((canvas.value - 100),20)* 15/20

        zeiger.rotation = rotate;

        canvas.currentValue = zeiger.rotation - 210} //130 minrotation, -30 maxrotation
    width: parent.width; height: parent.height

    Rectangle {
        id: zeiger
        rotation: -150 //siehe minrotation
        width: 4
        height: parent.width / 4
        transformOrigin: Item.Bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.verticalCenter

        smooth: true
        antialiasing: true
        color: "#81FFFE"
        onRotationChanged: {canvas.currentValue = zeiger.rotation - 210; canvas.requestPaint()}//texti.text = zeiger.rotation

            Behavior on rotation {
                NumberAnimation{
                    duration: 500
                    easing.type: Easing.Linear
                }
            }
    }


      antialiasing: true

      property color secondaryColor: zeiger.color

      property real centerWidth: width / 2
      property real centerHeight: height / 2
      property real radius: Math.min(canvas.width, canvas.height) / 2

      property real minimumValue: -360
      property real maximumValue: 0
      property real currentValue: -360

      // this is the angle that splits the circle in two arcs
      // first arc is drawn from 0 radians to angle radians
      // second arc is angle radians to 2*PI radians
      property real angle: (currentValue - minimumValue) / (maximumValue - minimumValue) * 2 * Math.PI
      property real angleOffset: 2.1 //to start at 0mph //-Math.PI / 2


      onPaint: {
          var ctx = getContext("2d");
          ctx.save();

          var gradient2 = ctx.createRadialGradient((parent.width / 2),(parent.height / 2), 0, (parent.width / 2),(parent.height / 2),parent.height);
           gradient2.addColorStop(0.5, "#81FFFE");   //oben
          gradient2.addColorStop(0.46, "#81FFFE");   //oben
          gradient2.addColorStop(0.45, "#112478");   //mitte
          gradient2.addColorStop(0.33, "transparent");   //unten

          ctx.clearRect(0, 0, canvas.width, canvas.height);

          ctx.beginPath();
          ctx.lineWidth = 150;
          ctx.strokeStyle = gradient2



          ctx.arc(canvas.centerWidth, canvas.centerHeight, canvas.radius - (ctx.lineWidth / 2), canvas.angleOffset, canvas.angleOffset + canvas.angle);
          ctx.stroke();

          ctx.restore();
      }
}

