#include "led_controller.h"
#include <Arduino.h>

static const int LED_RED_PIN = 2;
static const int LED_GREEN_PIN = 4;
static const int LED_BLUE_PIN = 5;

bool LedController::begin() {
  pinMode(LED_RED_PIN, OUTPUT);
  pinMode(LED_GREEN_PIN, OUTPUT);
  pinMode(LED_BLUE_PIN, OUTPUT);
  setGreen();
  return true;
}

void LedController::setState(const DecisionState &state) {
  switch (state) {
    case DecisionState::HIGH_STRESS:
      setRed();
      break;
    case DecisionState::WARNING:
      setYellow();
      break;
    case DecisionState::NORMAL:
    default:
      setGreen();
      break;
  }
}

void LedController::setRed() {
  digitalWrite(LED_RED_PIN, HIGH);
  digitalWrite(LED_GREEN_PIN, LOW);
  digitalWrite(LED_BLUE_PIN, LOW);
}

void LedController::setYellow() {
  digitalWrite(LED_RED_PIN, HIGH);
  digitalWrite(LED_GREEN_PIN, HIGH);
  digitalWrite(LED_BLUE_PIN, LOW);
}

void LedController::setGreen() {
  digitalWrite(LED_RED_PIN, LOW);
  digitalWrite(LED_GREEN_PIN, HIGH);
  digitalWrite(LED_BLUE_PIN, LOW);
}
