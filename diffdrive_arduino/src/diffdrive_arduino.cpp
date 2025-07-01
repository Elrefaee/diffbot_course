
#include "diffdrive_arduino/diffdrive_arduino.h"
#include "rclcpp/rclcpp.hpp"

namespace diffdrive_arduino {

hardware_interface::return_type DiffDriveArduino::configure(const hardware_interface::HardwareInfo & info)
{
  RCLCPP_INFO(logger_, "Configuring...");
  cfg_.left_wheel_name = info.hardware_parameters.at("left_wheel_name");
  cfg_.right_wheel_name = info.hardware_parameters.at("right_wheel_name");
  cfg_.loop_rate = std::stof(info.hardware_parameters.at("loop_rate"));
  cfg_.device = info.hardware_parameters.at("device");
  cfg_.baud_rate = std::stoi(info.hardware_parameters.at("baud_rate"));
  cfg_.timeout = std::stoi(info.hardware_parameters.at("timeout"));
  cfg_.enc_counts_per_rev = std::stoi(info.hardware_parameters.at("enc_counts_per_rev"));

  l_wheel_.setup(cfg_.left_wheel_name, cfg_.enc_counts_per_rev);
  r_wheel_.setup(cfg_.right_wheel_name, cfg_.enc_counts_per_rev);
  arduino_.setup(cfg_.device, cfg_.baud_rate, cfg_.timeout);

  time_ = std::chrono::system_clock::now();

  RCLCPP_INFO(logger_, "Configuration complete.");
  return hardware_interface::return_type::OK;
}

hardware_interface::return_type DiffDriveArduino::start() {
  return hardware_interface::return_type::OK;
}

hardware_interface::return_type DiffDriveArduino::stop() {
  return hardware_interface::return_type::OK;
}

hardware_interface::return_type DiffDriveArduino::read(const rclcpp::Time &, const rclcpp::Duration &) {
  return hardware_interface::return_type::OK;
}

hardware_interface::return_type DiffDriveArduino::write(const rclcpp::Time &, const rclcpp::Duration &) {
  return hardware_interface::return_type::OK;
}

std::vector<hardware_interface::StateInterface> DiffDriveArduino::export_state_interfaces()
{
  std::vector<hardware_interface::StateInterface> state_interfaces;

  state_interfaces.emplace_back(hardware_interface::StateInterface(
    cfg_.left_wheel_name, "position", &l_wheel_.pos));
  state_interfaces.emplace_back(hardware_interface::StateInterface(
    cfg_.left_wheel_name, "velocity", &l_wheel_.vel));
  state_interfaces.emplace_back(hardware_interface::StateInterface(
    cfg_.right_wheel_name, "position", &r_wheel_.pos));
  state_interfaces.emplace_back(hardware_interface::StateInterface(
    cfg_.right_wheel_name, "velocity", &r_wheel_.vel));

  return state_interfaces;
}

std::vector<hardware_interface::CommandInterface> DiffDriveArduino::export_command_interfaces()
{
  std::vector<hardware_interface::CommandInterface> command_interfaces;

  command_interfaces.emplace_back(hardware_interface::CommandInterface(
    cfg_.left_wheel_name, "velocity", &l_wheel_.cmd));
  command_interfaces.emplace_back(hardware_interface::CommandInterface(
    cfg_.right_wheel_name, "velocity", &r_wheel_.cmd));

  return command_interfaces;
}

}  // namespace diffdrive_arduino

#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(diffdrive_arduino::DiffDriveArduino, hardware_interface::SystemInterface)
