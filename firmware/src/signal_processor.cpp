#include "signal_processor.h"
#include "data_types.h"

bool SignalProcessor::begin() {
  return true;
}

ProcessedFeatures SignalProcessor::process(const BiosignalSample &sample) {
  ProcessedFeatures features;
  computeEMG(sample, features);
  computeHRV(sample, features);
  computeGSR(sample, features);
  return features;
}

DecisionState SignalProcessor::classify(const ProcessedFeatures &features) {
  float score = randomForestScore(features);

  if (score > 0.75f) {
    return DecisionState::HIGH_STRESS;
  }
  if (score > 0.45f) {
    return DecisionState::WARNING;
  }
  return DecisionState::NORMAL;
}

void SignalProcessor::computeEMG(const BiosignalSample &sample, ProcessedFeatures &features) {
  features.emgRMS = abs(sample.emgRaw) / 1023.0f;
}

void SignalProcessor::computeHRV(const BiosignalSample &sample, ProcessedFeatures &features) {
  features.hrvSdnn = sample.hrvRaw;
}

void SignalProcessor::computeGSR(const BiosignalSample &sample, ProcessedFeatures &features) {
  features.gsrTonic = sample.gsrRaw / 1023.0f;
}

float SignalProcessor::randomForestScore(const ProcessedFeatures &features) {
  return (features.emgRMS * 0.4f) + (features.hrvSdnn * 0.3f) + (features.gsrTonic * 0.3f);
}
