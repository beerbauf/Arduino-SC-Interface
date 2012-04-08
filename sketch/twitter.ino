const int R_LED = 9;
const int G_LED = 10;
const int B_LED = 11;

char buffer[6] = {0,0,0,0,0,0};
int rgb[3] = {0,0,0};
int idx = 0;

int hex2dec(char c);

void setup(){
  Serial.begin(115200);
}

void loop(){
  if(Serial.available()){
    char ch = toupper((char)Serial.read());
    if(idx<6)
      buffer[idx++]=ch;
  } else {
    idx=0;
    for(int i=0; i<6; i+=2)
      rgb[i/2] = hex2dec(buffer[i+1])+hex2dec(buffer[i])*16;
    analogWrite(R_LED, rgb[0]);
    analogWrite(G_LED, rgb[1]);
    analogWrite(B_LED, rgb[2]);
    delay(100);
  }
}

int hex2dec(char c){
  if(c>='A' && c<='F')
    return (int)(c - 'A')+10;
  else if (c >= '0' && c<='9')
    return (int)(c - '0');
}
