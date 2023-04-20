#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char *ssid = "xxx";        // The name of the Wi-Fi network that will be created
const char *password = "xxxxxx"; // The password required to connect to it, leave blank for an open network

ESP8266WebServer server(80);

// motor A pins
const byte Motor_A_Speed = D1;    // GPI05
const byte Motor_A_Direcion = D3; // GPI04

// preset motor B pins
const byte Motor_B_Direcion = D4; // GPI02
const byte Motor_B_Speed = D2;    // GPI12

// preset motor A and B speeds
int a1 = 100;
int a2 = 133;
int a3 = 166;
int a4 = 200;
int a5 = 233;
int b1 = 100;
int b2 = 133;
int b3 = 166;
int b4 = 200;
int b5 = 233;

int Set_Motor_A_Speed = 100;
int Set_Motor_B_Speed = 100;

void motorSpeed(int prmA, byte prmA1, int prmB, byte prmB1)
{
    analogWrite(Motor_A_Speed, prmA);
    analogWrite(Motor_B_Speed, prmB);

    digitalWrite(Motor_A_Direcion, prmA1);
    digitalWrite(Motor_B_Direcion, prmB1);
}

void handleRoot()
{
    String message = "";
    message += "<html><head><title>Dual Motor Boat Controller</title><head>";
    message += "<body><h1>Dual Motor Boat Controller</h1>";
    message += "<table> ";
    message += "<tr>";
    message += "<h3>Motor A Speed = ";
    message += Set_Motor_A_Speed;
    message += "<p>Motor B Speed = ";
    message += Set_Motor_B_Speed;
    message += "</p></h3>";
    message += "<tr>";
    message += "</table> ";
    message += "</body></html>";
    server.send(200, "text/html", message);
}

void handleBoat()
{
    String message = "";
    int BtnValue = 0;
    for (uint8_t i = 0; i < server.args(); i++)
    {
        if (server.argName(i) == "a")
        {
            String s = server.arg(i);
            BtnValue = s.toInt();
        }
        Serial.println(server.argName(i) + ": " + server.arg(i) + "\n");
    }

    switch (BtnValue)
    {
        case 2: // forward
            motorSpeed(Set_Motor_A_Speed, HIGH, Set_Motor_B_Speed, HIGH);
            break;
        case 4: // turn left
            motorSpeed(Set_Motor_A_Speed, LOW, Set_Motor_B_Speed, HIGH);
            break;
        case 5: // stop
            motorSpeed(Set_Motor_A_Speed - Set_Motor_A_Speed, LOW, Set_Motor_B_Speed - Set_Motor_B_Speed, LOW);
            break;
        case 6: //   turn right
            motorSpeed(Set_Motor_A_Speed, HIGH, Set_Motor_B_Speed, LOW);
            break;
        case 8: // reverse
            motorSpeed(Set_Motor_A_Speed, LOW, Set_Motor_B_Speed, LOW);
            break;
        case 10: // Set_Motor_A_Speed = 1
            Set_Motor_A_Speed = a1;
            break;
        case 11: // Set_Motor_A_Speed = 2
            Set_Motor_A_Speed = a2;
            break;
        case 12: // Set_Motor_A_Speed = 3
            Set_Motor_A_Speed = a3;
            break;
        case 13: // Set_Motor_A_Speed = 4
            Set_Motor_A_Speed = a4;
            break;
        case 14: // Set_Motor_A_Speed = 5
            Set_Motor_A_Speed = a5;
            break;
        case 15: // comment
            Set_Motor_B_Speed = b1;
            break;
        case 16: // comment
            Set_Motor_B_Speed = b2;
            break;
        case 17: // comment
            Set_Motor_B_Speed = b3;
            break;
        case 18: // comment
            Set_Motor_B_Speed = b4;
            break;
        case 19: // comment
            Set_Motor_B_Speed = b5;
            break;
        case 20: // comment
            Set_Motor_A_Speed = a1;
            Set_Motor_B_Speed = b1;
            break;
        case 21: // comment
            Set_Motor_A_Speed = a2;
            Set_Motor_B_Speed = b2;
            break;
        case 22: // comment
            Set_Motor_A_Speed = a3;
            Set_Motor_B_Speed = b3;
            break;
        case 23: // comment
            Set_Motor_A_Speed = a4;
            Set_Motor_B_Speed = b4;
            break;
        case 24: // comment
            Set_Motor_A_Speed = a5;
            Set_Motor_B_Speed = b5;
            break;

        default:
            break;
    }

    // ??
    message += "<html><head><title>Dual Motor Boat Controller</title><head>";
    message += "<body><h1>Dual Motor Boat Controller</h1>";
    message += "<table> ";
    message += "<tr>";
    message += "<h3>Motor A Speed = ";
    message += Set_Motor_A_Speed;
    message += "<p>Motor B Speed = ";
    message += Set_Motor_B_Speed;
    message += "</p></h3>";
    message += "<tr>";
    message += "</table> ";
    message += "</body></html>";
    server.send(200, "text/html", message);
}

// void tempSinyal()
// {
// }

void handleNotFound()
{
    String message = "File Not Found\n\n";
    message += "URI: ";
    message += server.uri();
    message += "\nMethod: ";
    message += (server.method() == HTTP_GET) ? "GET" : "POST";
    message += "\nArguments: ";
    message += server.args();
    message += "\n";
    for (uint8_t i = 0; i < server.args(); i++)
    {
        message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
    }
    server.send(404, "text/plain", message);
}

void getInfo()
{
    DynamicJsonDocument doc(1024);
    doc["motor_1_speed"] = Set_Motor_A_Speed;
    doc["motor_2_speed"] = Set_Motor_B_Speed;
    doc["gps_lat"] = "0.00000";
    doc["gps_lon"] = "0.00000";
    doc["gps_course"] = "0.00N";
    // doc["gps_speed"] = "0.0 knots";
    // doc["gps_sat_no"] = "1";
    // doc["cur_date"] = "2023 April 14";
    // doc["cur_time"] = "12:34";

    serializeJson(doc, serial);
    server.send(200, "text/json", serial)
}

void setup()
{
    pinMode(Motor_A_Direcion, OUTPUT);
    pinMode(Motor_B_Direcion, OUTPUT);

    digitalWrite(Motor_A_Direcion, LOW);
    digitalWrite(Motor_B_Direcion, LOW);

    Serial.begin(115200);

    delay(10);
    Serial.println('\n');

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    Serial.println("");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());


    // routes
    server.on("/", handleRoot);
    server.on("/command", handleBoat);

    server.on("/status", []() {
        server.send(200, "text/plain", "Server is online");
    });

    server.on('/info', HTTP_GET, getInfo);

    server.onNotFound(handleNotFound);

    server.begin();
    Serial.println("HTTP server started");
}

void loop()
{
    server.handleClient();
}