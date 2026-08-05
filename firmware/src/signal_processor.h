#pragma once

#include "data_types.h"

class SignalProcessor {
public:
  bool begin();
  ProcessedFeatures process(const BiosignalSample &sample);
  DecisionState classify(const ProcessedFeatures &features);

private:
  void computeEMG(const BiosignalSample &sample, ProcessedFeatures &features);
  void computeHRV(const BiosignalSample &sample, ProcessedFeatures &features);
  void computeGSR(const BiosignalSample &sample, ProcessedFeatures &features);
  float randomForestScore(const ProcessedFeatures &features);
};
