#include "comm_manager.h"
#include <Arduino.h>

bool CommManager::begin() {
  return true;
}

void CommManager::sendState(const DecisionState &state, const ProcessedFeatures &features) {
  Serial.print("DECISION:");
  Serial.print((int)state);
  Serial.print(",EMG_RMS:");
  Serial.print(features.emgRMS);
  Serial.print(",HRV_SDNN:");
  Serial.print(features.hrvSdnn);
  Serial.print(",GSR_TONIC:");
  Serial.println(features.gsrTonic);
}
