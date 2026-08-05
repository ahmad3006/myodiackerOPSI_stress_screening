#pragma once

enum class DecisionState {
  NORMAL = 0,
  WARNING = 1,
  HIGH_STRESS = 2
};

struct BiosignalSample {
  int emgRaw;
  int hrvRaw;
  int gsrRaw;
};

struct ProcessedFeatures {
  float emgRMS;
  float hrvSdnn;
  float gsrTonic;
};
