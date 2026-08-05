#pragma once

#include "data_types.h"

class CommManager {
public:
  bool begin();
  void sendState(const DecisionState &state, const ProcessedFeatures &features);
};
