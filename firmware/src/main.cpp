#include <Arduino.h>
#include "sensor_manager.h"
#include "signal_processor.h"
#include "led_controller.h"
#include "comm_manager.h"

SensorManager sensorManager;
SignalProcessor signalProcessor;
LedController ledController;
CommManager commManager;

void setup() {
  Serial.begin(115200);
  sensorManager.begin();
  signalProcessor.begin();
  ledController.begin();
  commManager.begin();
}

void loop() {
  BiosignalSample sample = sensorManager.readSensors();
  ProcessedFeatures features = signalProcessor.process(sample);
  DecisionState decision = signalProcessor.classify(features);
  ledController.setState(decision);
  commManager.sendState(decision, features);
  delay(200);
}
