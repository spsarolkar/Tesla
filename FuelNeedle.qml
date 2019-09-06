import QtQuick 2.4
import QtGraphicalEffects 1.0

Canvas {
    id: canvas

    property int value : 100

    onValueChanged: {
        zeiger.rotation = 90 + 45 * canvas.value/100 + 0.01//Math.max(canvas.value*2.25 - 90,90)//Math.min(Math.max(10, canvas.value*3.5 - 90), 90);
        canvas.currentValue = zeiger.rotation - 90
    }
        //90 minrotation, 10 maxrotation
    width: parent.width; height: parent.height


    Rectangle {
        id: zeiger
        rotation: 90 //siehe minrotation
        width: 2
        height: parent.width / 4
        transformOrigin: Item.Bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.verticalCenter

        antialiasing: true
        smooth: true
        color: "#6cf213"
        onRotationChanged: {

            canvas.currentValue = zeiger.rotation - 90;


            canvas.requestPaint()}

            Behavior on rotation {
                NumberAnimation{
                    duration: 1000
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
    property real angle: (currentValue - minimumValue) / (maximumValue - minimumValue) * 2 * Math.PI + 0.0001
    property real angleOffset: 0 //Math.PI//21.288 //to start at 0mph //-Math.PI / 2
    onPaint: {
    //Magic
        var ctx = getContext("2d");
        ctx.save();

        var gradient2 = ctx.createRadialGradient((parent.width / 2),(parent.height / 2), 200, (parent.width / 2),(parent.height / 2),2);
         gradient2.addColorStop(0.7, "#6cf213");   //oben
        gradient2.addColorStop(0.6, "#6cf213");   //oben
        gradient2.addColorStop(0.6, "#a5e27c");   //mitte
        gradient2.addColorStop(0.5, "transparent");   //unten

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.beginPath();
        ctx.lineWidth = 150;
        ctx.strokeStyle = gradient2
        ctx.arc(canvas.centerWidth, canvas.centerHeight, (canvas.radius - (ctx.lineWidth / 2))/3-4, canvas.angleOffset, canvas.angleOffset + canvas.angle, true);
        ctx.stroke();

        ctx.restore();

    }
}

