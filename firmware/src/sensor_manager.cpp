#include "sensor_manager.h"
#include "data_types.h"
#include <Arduino.h>

bool SensorManager::begin() {
  initEMG();
  initHRV();
  initGSR();
  randomSeed(analogRead(0));
  return true;
}

BiosignalSample SensorManager::readSensors() {
  // Dummy sensor output for development without hardware.
  BiosignalSample sample;
  sample.emgRaw = random(150, 900);
  sample.hrvRaw = random(20, 120);
  sample.gsrRaw = random(100, 900);
  return sample;
}

void SensorManager::initEMG() {
  pinMode(34, INPUT);
}

void SensorManager::initHRV() {
  // HRV sensor initialization stub for dummy mode.
}

void SensorManager::initGSR() {
  pinMode(35, INPUT);
}
