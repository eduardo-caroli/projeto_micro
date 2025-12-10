#include <AccelStepper.h>
#include <Arduino.h>

// ===================== CONFIGURAÇÃO CNC ======================
#define PIN_STEP_X 2
#define PIN_DIR_X 5
#define PIN_STEP_Y 3
#define PIN_DIR_Y 6
#define PIN_STEP_Z 4
#define PIN_DIR_Z 7

#define OFFSET_X 50

#define PIN_LIMIT_X 24
#define PIN_LIMIT_Y 22

#define VELOCIDADE_MAX 1000
#define VELOCIDADE 800
#define ESPACAMENTO_PONTOS 11 //real eh 11   //250
#define ESPACAMENTO_LINHAS 31 //real eh 31   //700

#define PIN_SOLENOIDE_A 30
#define PIN_SOLENOIDE_B 42
#define PINOS_ESPACAMENTO_SOLENOIDE 12

#define X_MAX 1750
#define Y_MAX 2000

AccelStepper stepper_x(AccelStepper::DRIVER, PIN_STEP_X, PIN_DIR_X);
AccelStepper stepper_y(AccelStepper::DRIVER, PIN_STEP_Y, PIN_DIR_Y);
AccelStepper stepper_z(AccelStepper::DRIVER, PIN_STEP_Z, PIN_DIR_Z);

int pos_x = 0;
int pos_y = 0;

int inner_space = 20;
int v_outer_space=40;
int v_inner_space = 20;
int h_outer_space = 20;

// ================== VARIÁVEIS DO PARSER SERIAL =================
#define MAX_LETRAS 20
#define MAX_BITS 6
#define MAX_VETORES 3
#define MAX_DUPLAS 40

int linha[MAX_LETRAS][MAX_BITS];
int bitsCount[MAX_LETRAS];
int separados[MAX_VETORES][MAX_LETRAS * 2];
int duplas[MAX_VETORES][MAX_DUPLAS][2];
int totalLinhas = 0;
int totalDuplasGeradas[MAX_VETORES];

// ===================== FUNÇÕES CNC =============================

int calculaEspacamentoPontos(float espacamento){

  int espacamento_pontos = (espacamento*2000)/425;
  return espacamento_pontos;
  
}

void go_home() {
  stepper_x.setSpeed(VELOCIDADE);
  stepper_y.setSpeed(VELOCIDADE);
  stepper_z.setSpeed(-VELOCIDADE);

  bool x_homed = false;
  bool y_homed = false;

  while ((!x_homed) || (!y_homed)) {
    if (!x_homed) {
      if (digitalRead(PIN_LIMIT_X) == LOW) {
        x_homed = true;
        stepper_x.stop();
        stepper_x.setCurrentPosition(0);
        stepper_x.moveTo(0);
      } else stepper_x.runSpeed();
    }

    if (!y_homed) {
      if (digitalRead(PIN_LIMIT_Y) == LOW) {
        y_homed = true;
        stepper_y.stop();
        stepper_z.stop();
        stepper_y.setCurrentPosition(0);
        stepper_z.setCurrentPosition(0);
        stepper_y.moveTo(0);
        stepper_z.moveTo(0);
      } else {
        stepper_y.runSpeed();
        stepper_z.runSpeed();
      }
    }
  }

  pos_x = 0;
  pos_y = 0;
}

void moverPara(int destino_x, int destino_y) {
  stepper_x.move(destino_x - pos_x);
  stepper_y.move(destino_y - pos_y);
  stepper_z.move((destino_y - pos_y) * (-1));

  stepper_x.setSpeed(VELOCIDADE * (destino_x >= pos_x ? 1 : -1));
  stepper_y.setSpeed(VELOCIDADE * (destino_y >= pos_y ? 1 : -1));
  stepper_z.setSpeed(VELOCIDADE * (destino_y >= pos_y ? 1 : -1));

  while (stepper_x.distanceToGo() != 0 || stepper_y.distanceToGo() != 0) {
    stepper_x.runSpeedToPosition();
    stepper_y.runSpeedToPosition();
    stepper_z.runSpeedToPosition();
  }

  pos_x = destino_x;
  pos_y = destino_y;
}

// ===================== FUNÇÕES SERIAL ==========================
void resetLinha() {
  for (int i = 0; i < MAX_LETRAS; i++){
    bitsCount[i] = 0;
  }
}

bool parseLine(String raw) {
  raw.trim();
  if (!raw.startsWith("p:")) return false;

  raw = raw.substring(2);
  raw.trim();
  resetLinha();

  int start = 0;
  int letra = 0;

  while (true) {
    int end = raw.indexOf("],[", start);

    String bloco;
    if (end == -1) bloco = raw.substring(start);
    else bloco = raw.substring(start, end);

    bloco.replace("[", "");
    bloco.replace("]", "");
    bloco.trim();

    int pos = 0;
    bitsCount[letra] = 0;

    while (true) {
      int comma = bloco.indexOf(",", pos);
      String bit;

      if (comma == -1) bit = bloco.substring(pos);
      else bit = bloco.substring(pos, comma);

      bit.trim();
      if (bit.length() > 0) {
        linha[letra][bitsCount[letra]] = bit.toInt();
        bitsCount[letra]++;
      }

      if (comma == -1) break;
      pos = comma + 1;
    }

    letra++;
    if (end == -1) break;
    start = end + 3;
  }

  totalLinhas = letra;
  return true;
}

void criaSeparados() {
  for (int v = 0; v < MAX_VETORES; v++) {
    int idx = 0;
    for (int l = 0; l < totalLinhas; l++) {
      separados[v][idx++] = linha[l][v * 2];
      separados[v][idx++] = linha[l][v * 2 + 1];
    }
  }
}

void criaDuplasLinhas(int n) {
  for (int v = 0; v < MAX_VETORES; v++) {
    int totalElems = totalLinhas * 2;
    bool usado[MAX_DUPLAS] = {false}; 
    int duplaIdx = 0;

    for (int i = 0; i < totalElems; i++) {
      if (usado[i]) continue;

      int j = i + n;
      duplas[v][duplaIdx][0] = separados[v][i];

      if (j < totalElems && !usado[j]) {
        duplas[v][duplaIdx][1] = separados[v][j];
        usado[j] = true;
      } else {
        duplas[v][duplaIdx][1] = 0;
      }

      usado[i] = true;
      duplaIdx++;

      if (duplaIdx >= MAX_DUPLAS) break;
    }

    totalDuplasGeradas[v] = duplaIdx;
  }
}

void marcaPontos(int a, int b){

  if(a == 1){
    digitalWrite(PIN_SOLENOIDE_A,LOW);
    delay(1000);
  }
  digitalWrite(PIN_SOLENOIDE_A,HIGH);

  if(b == 1){
    digitalWrite(PIN_SOLENOIDE_B,LOW);
    delay(1000);
  }
  digitalWrite(PIN_SOLENOIDE_B,HIGH);

  delay(100);
}

// ============================ LOOP ==============================
void setup() {
  Serial.begin(9600);

  stepper_x.enableOutputs();
  stepper_x.setMaxSpeed(VELOCIDADE_MAX);

  stepper_y.enableOutputs();
  stepper_y.setMaxSpeed(VELOCIDADE_MAX);

  stepper_z.enableOutputs();
  stepper_z.setMaxSpeed(VELOCIDADE_MAX);

  pinMode(PIN_LIMIT_X, INPUT_PULLUP);
  pinMode(PIN_LIMIT_Y, INPUT_PULLUP);

  pinMode(PIN_SOLENOIDE_A, OUTPUT);
  pinMode(PIN_SOLENOIDE_B, OUTPUT);

  digitalWrite(PIN_SOLENOIDE_A,HIGH);
  digitalWrite(PIN_SOLENOIDE_B,HIGH);

  go_home();
}

int param_count = 0;

void loop() {
  if (Serial.available() > 0) {
    String raw = Serial.readStringUntil('\n');
    // if (param_count < 4) {
    //   if (param_count == 0) {
    //     inner_space = raw.toInt();
    //     Serial.println("p");
    //     param_count++;
    //   }
    //   if (param_count == 1) {
    //     v_outer_space = raw.toInt();
    //     Serial.println("p");
    //     param_count++;
    //   }
    //   if (param_count == 2) {
    //     v_inner_space = raw.toInt();
    //     Serial.println("p");
    //     param_count++;
    //   }
    //   if (param_count == 3) {
    //     h_outer_space = raw.toInt();
    //     Serial.println("p");
    //     param_count++;
    //   }
    // }
    if (raw == "0") {
      moverPara(pos_x - inner_space, pos_y);
      Serial.println("p");
    }
    if (raw == "1") {
      marcaPontos(1,0);
      moverPara(pos_x - inner_space, pos_y);
      Serial.println("p");
    }
    if (raw == "n") {
      moverPara(OFFSET_X, pos_y - v_outer_space);
      Serial.println("p");
    }
    if (raw == "j") {
      moverPara(OFFSET_X, pos_y - v_inner_space);
      Serial.println("p");
    }
    if (raw == "s") {
      moverPara(pos_x - h_outer_space, pos_y);
      Serial.println("p");
    }
  }
}