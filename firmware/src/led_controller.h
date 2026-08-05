#pragma once

#include "data_types.h"

class LedController {
public:
  bool begin();
  void setState(const DecisionState &state);

private:
  void setRed();
  void setYellow();
  void setGreen();
};
