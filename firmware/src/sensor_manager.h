#pragma once

#include <Arduino.h>
#include "data_types.h"

class SensorManager {
public:
  bool begin();
  BiosignalSample readSensors();

private:
  void initEMG();
  void initHRV();
  void initGSR();
};
