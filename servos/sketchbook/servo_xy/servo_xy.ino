#define USB_USBCON
#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

#include <Servo.h> 
#include <ros.h>
#include <servos/XYPose.h>

ros::NodeHandle nh;

Servo servo_x, servo_y;

void servo_cb( const servos::XYPose& cmd_msg){
  servo_x.write(cmd_msg.x);
  servo_y.write(cmd_msg.y);
}

ros::Subscriber<servos::XYPose> sub("/servos_pose", servo_cb);

void setup(){
  //nh.getHardware()->setBaud(9600);
  nh.initNode();
  nh.subscribe(sub);

  servo_x.attach(9);
  servo_y.attach(10);
  servo_x.write(45);
  servo_y.write(10);
}

void loop(){
  nh.spinOnce();
  delay(1);
}
