int En0 = 7;  //  Low enabled
int En1 = 6;  //  Low enabled
 
 
int S0  = 5;
int S1  = 4;
int S2  = 3;
int S3  = 2;

int All_Sensor = 0;
int Left_Sensor = 0;
int Right_Sensor = 0;
int back_Sensor = 0;
int front_Sensor = 0;


int x = 0; 
int SIG_pin = A3;
 
 
void setup() {
  Serial.begin(115200);
  pinMode(En0, OUTPUT);
  pinMode(En1, OUTPUT);
 
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
 
}
 
void loop() {

    for(int i = 0; i < 31; i++){
    All_Sensor += readMux(i);
  } 
  for(int i = 5; i < 10; i++){
    Left_Sensor += readMux(i);
  }
  Left_Sensor += readMux(11);
  Left_Sensor += readMux(13);
  
  for(int i = 21; i < 26; i++){
    Right_Sensor += readMux(i);
  }
  Right_Sensor += readMux(15);
  Right_Sensor += readMux(17);
  Right_Sensor += readMux(19);

  
  for(int i = 0; i < 5; i++){
    back_Sensor += readMux(i);
  }
  for(int i = 26; i < 31; i++){
    back_Sensor += readMux(i);
  }
  
  front_Sensor += readMux(10);
  front_Sensor += readMux(12);
  front_Sensor += readMux(14);
  front_Sensor += readMux(16);
  front_Sensor += readMux(18);
  front_Sensor += readMux(20);

  double left =   (double)Left_Sensor / All_Sensor * 100;
  double right =  (double)Right_Sensor / All_Sensor * 100;
  double front =  (double)front_Sensor / All_Sensor * 100;
  double back =   (double)back_Sensor / All_Sensor * 100;

  int final_left = round(left);
  int final_right = round(right);
  int final_front = round(front);
  int final_back = round(back);
  
  int percent = final_left + final_right + final_front + final_back;
  
  //Serial.print("Left : ");
  Serial.print(String(final_left));
  //Serial.print("%");
  //Serial.print(" ");
  Serial.print("/");
  //Serial.print(" ");
  //Serial.print("right : ");
  Serial.print(String(final_right));
  //Serial.print("%");
  //Serial.print(" ");
  Serial.print("/");
  //Serial.print(" ");
  //Serial.print("front : ");
  Serial.print(String(final_front));
  //Serial.print("%");
  //Serial.print(" ");
  Serial.print("/");
  //Serial.print(" ");
  //Serial.print("back : ");
  Serial.println(String(final_back));
  //Serial.print("%");
  //Serial.print(" ");
  //Serial.print("/");
  //Serial.print(" ");
  //Serial.println(percent);
  

  All_Sensor = 0;
  Right_Sensor = 0;
  Left_Sensor = 0;
  front_Sensor = 0;
  back_Sensor = 0;
 delay(1000);

}
 
 
int readMux(int channel){
  int controlPin[] = {S0,S1,S2,S3,En0,En1};
 
  int muxChannel[31][6]={
    {0,0,0,0,0,1}, //channel 0
    {0,0,0,1,0,1}, //channel 1
    {0,0,1,0,0,1}, //channel 2
    {0,0,1,1,0,1}, //channel 3
    {0,1,0,0,0,1}, //channel 4
    {0,1,0,1,0,1}, //channel 5
    {0,1,1,0,0,1}, //channel 6
    {0,1,1,1,0,1}, //channel 7
    {1,0,0,0,0,1}, //channel 8
    {1,0,0,1,0,1}, //channel 9
    {1,0,1,0,0,1}, //channel 10
    {1,0,1,1,0,1}, //channel 11
    {1,1,0,0,0,1}, //channel 12
    {1,1,0,1,0,1}, //channel 13
    {1,1,1,0,0,1}, //channel 14
    {1,1,1,1,0,1}, //channel 15
    {0,0,0,0,1,0}, //channel 16
    {0,0,0,1,1,0}, //channel 17
    {0,0,1,0,1,0}, //channel 18
    {0,0,1,1,1,0}, //channel 19
    {0,1,0,0,1,0}, //channel 20
    {0,1,0,1,1,0}, //channel 21
    {0,1,1,0,1,0}, //channel 22
    {0,1,1,1,1,0}, //channel 23
    {1,0,0,0,1,0}, //channel 24
    {1,0,0,1,1,0}, //channel 25
    {1,0,1,0,1,0}, //channel 26
    {1,0,1,1,1,0}, //channel 27
    {1,1,0,0,1,0}, //channel 28
    {1,1,0,1,1,0}, //channel 29
    {1,1,1,0,1,0}, //channel 30
  };
  
  //loop through the 6 sig
  for(int i = 0; i < 6; i ++){
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }
 
  //read the value at the SIG pin
  int val = analogRead(SIG_pin);
 
  //return the value
  return val;
}
