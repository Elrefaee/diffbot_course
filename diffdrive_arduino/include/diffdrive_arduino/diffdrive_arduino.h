#ifndef DIFFDRIVE_ARDUINO_REAL_ROBOT_H
#define DIFFDRIVE_ARDUINO_REAL_ROBOT_H

#include "rclcpp/rclcpp.hpp"
#include "hardware_interface/system_interface.hpp"
#include "hardware_interface/handle.hpp"
#include "hardware_interface/hardware_info.hpp"
#include "hardware_interface/types/hardware_interface_return_values.hpp"

#include "config.h"
#include "wheel.h"
#include "arduino_comms.h"

using hardware_interface::return_type;

namespace diffdrive_arduino  // ✅ أضف السطر ده
{

class DiffDriveArduino : public hardware_interface::SystemInterface
{
public:
  DiffDriveArduino() = default;

  return_type configure(const hardware_interface::HardwareInfo & info);
  std::vector<hardware_interface::StateInterface> export_state_interfaces() override;
  std::vector<hardware_interface::CommandInterface> export_command_interfaces() override;
  return_type start();
  return_type stop();
  return_type read(const rclcpp::Time & time, const rclcpp::Duration & period) override;
  return_type write(const rclcpp::Time & time, const rclcpp::Duration & period) override;

private:
  Config cfg_;
  ArduinoComms arduino_;
  Wheel l_wheel_, r_wheel_;
  rclcpp::Logger logger_{rclcpp::get_logger("DiffDriveArduinoHardware")};
  std::chrono::time_point<std::chrono::system_clock> time_;
};

}  // namespace diffdrive_arduino ✅ اقفل الـ namespace هنا

#endif

