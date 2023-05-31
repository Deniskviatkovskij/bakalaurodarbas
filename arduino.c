#include <DHT.h>

int Humidity;
int Temperature;
float Voltage;
float Voltage1;
float Voltage2;

int analogInput = A1; // Define Analog pin A1 f to read potential
float vout = 0.0;
float vin = 0.0;
float R1 = 30000.0; //
float R2 = 7500.0; //
int value = 0;

#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
   dht.begin();
  pinMode(analogInput, INPUT);
}

void loop() {
   float Temperature = dht.readTemperature();

  // read the value at analog input
  value = analogRead(analogInput);
  vout = (value * 5.0) / 1024.0; // see text
  vin = vout / (R2 / (R1 + R2)); // Calculate Input voltage
  Voltage = vin;

  unsigned int x=0;
  float AcsValue=0.0,Samples=0.0,AvgAcs=0.0,Current=0.0, Power=0.0;

  for (int x = 0; x < 150; x++){ //Get 150 samples
    AcsValue = analogRead(A0);     //Read current sensor values   
    Samples = Samples + AcsValue;  //Add samples together
    delay (3); // let ADC settle before next sample 3ms
  }
  AvgAcs=Samples/150.0;//Taking Average of Samples

  //((AvgAcs * (5.0 / 1024.0)) is converitng the read voltage in 0-5 volts
  //2.5 is offset(I assumed that arduino is working on 5v so the viout at no current comes
  //out to be 2.5 which is out offset. If your arduino is working on different voltage than 
  //you must change the offset according to the input voltage)
  //0.100v(100mV) is rise in output voltage when 1A current flows at input
  Current = (2.5 - (AvgAcs * (5.0 / 1024.0)) )/0.100;
  Power = Current * Voltage;

  Serial.print("{\"Temperature\":");
  Serial.print(Temperature);
  Serial.print(",\"Voltage\":");
  Serial.print(Voltage);
  Serial.print(",\"Current\":");
  Serial.print(Current);
  Serial.print(",\"Power\":");
  Serial.print(Power);
 
  Serial.println ("}");
  
  delay(2000);
}