#include <Stepper.h>
#include <Motor.h>

#define STEPS 2048 // the number of steps in one revolution of your motor (28BYJ-48)
Stepper stepper1(STEPS, 8, 10, 9, 11);
Stepper stepper2(STEPS, 2, 4, 3, 5);


void setup(){
  Serial.begin(9600);
}
 
void loop(){
  if (Serial.available()) {
    char fromPi = Serial.read();
    int intFromPi = static_cast<int>(fromPi);
    //String myStringFromPi = String(fromPi);
    //Serial.print("Folgender char wurde empfangen: ");
    delay(1000);
    Serial.println(intFromPi);
    delay(1000);
    
    switch (intFromPi) {
      case 98:
      motorSteuerungPlus();
      motorAus();
      break;
      case 97:
      motorSteuerungMinus();
      motorAus();
      break;
      case 99:
      motorSteuerungHoch();
      motorAus();
      break;
      case 100:
      motorSteuerungRunter();
      motorAus();
      break;
    }
  }
}

void motorSteuerungHoch(){
  Serial.println("in motorSteuerungHoch");
  stepper2.setSpeed(1); // 6 rpm
  stepper2.step(96); // do 2038 steps in the other direction with faster speed -- corresponds to one revolution in 10 seconds
}

void motorSteuerungRunter(){
  Serial.println("in motorSteuerungRunter");
  stepper2.setSpeed(1); // 6 rpm
  stepper2.step(-96); // do 2038 steps in the other direction with faster speed -- corresponds to one revolution in 10 seconds
}

void motorSteuerungMinus(){
  Serial.println("in motorSteuerungMinus");
  stepper1.setSpeed(1); // 6 rpm
  stepper1.step(-96); // do 2038 steps in the other direction with faster speed -- corresponds to one revolution in 10 seconds
}

void motorSteuerungPlus(){
  Serial.println("in motorSteuerungPlus");
  stepper1.setSpeed(1); // 6 rpm
  stepper1.step(96); // do 2038 steps in the other direction with faster speed -- corresponds to one revolution in 10 seconds
}

void motorAus(){
  Serial.print("in motorAus");
  Serial.println("Motor stoppen damit kein Strom verbraucht wird!");
  digitalWrite(8, LOW);
  digitalWrite(9, LOW);
  digitalWrite(10, LOW);
  digitalWrite(11, LOW);
  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
  delay(100);
}
