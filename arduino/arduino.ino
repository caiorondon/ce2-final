/*
 * Autor: Caio Rondon Botelho de Carvalho - 140058842
 * Trabalho final de Circuitos Eletricos 2
 * Projeto: Controle remoto controlado por receptor ADS-B
 * Parte do projeto: Controle remoto
 */
#include <IRremote.h>

/*
 * !!!!!!! Esses codigos precisam ser previamente medidos e variam de televisao para televisao
 */

#define INCREASE_VOLUME 0x4582ABFC // Codigo para aumentar o volume da televisao
#define DECREASE_VOLUME 0xF36FA75C // Codigo para diminuir o volume da televisao
#define STEP_DISTANCE 100

IRsend irsend; // !!!!!! conecte o IR no pino 3
int received_data = 0; // Guarda valor recebido em metros recebido na serial
int last_received = 0; // Guarda ultimo valor utilizado

void setup()
{
  Serial.begin(9600);
  pinMode(8, OUTPUT); // Debug
  pinMode(9, OUTPUT); // Debug
}

void loop() {
  if (Serial.available() > 0) { // Verifica se ha informacao na porta serial
    // Se há, lê dado
    received_data = Serial.readString().toInt();
    Serial.println(received_data);
    
    if (received_data >= 6000){
      Serial.println("Skipped");
      return;
    }
    
    if ((last_received - received_data) > STEP_DISTANCE){ // se aproximando
      irsend.sendSony(INCREASE_VOLUME, 32);
      Serial.println("Increase");
      digitalWrite(8, HIGH);
      delay(1000);
      digitalWrite(8, LOW);
      last_received = received_data;
    } else if ((last_received - received_data) < STEP_DISTANCE*(-1)){ // se distanciando
      irsend.sendSony(DECREASE_VOLUME, 32);
      Serial.println("Decrease");
      digitalWrite(9, HIGH);
      delay(1000);
      digitalWrite(9, LOW);
      last_received = received_data;
    }
  }
}
