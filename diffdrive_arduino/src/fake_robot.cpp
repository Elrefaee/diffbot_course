#include "diffdrive_arduino/fake_robot.h"
#include "rclcpp/rclcpp.hpp"

hardware_interface::return_type FakeRobot::configure(const hardware_interface::HardwareInfo & info)
{
  RCLCPP_INFO(logger_, "FakeRobot configuring...");
  cfg_.left_wheel_name = info.hardware_parameters.at("left_wheel_name");
  cfg_.right_wheel_name = info.hardware_parameters.at("right_wheel_name");
  cfg_.enc_counts_per_rev = std::stoi(info.hardware_parameters.at("enc_counts_per_rev"));

  l_wheel_.setup(cfg_.left_wheel_name, cfg_.enc_counts_per_rev);
  r_wheel_.setup(cfg_.right_wheel_name, cfg_.enc_counts_per_rev);
  time_ = std::chrono::system_clock::now();

  return hardware_interface::return_type::OK;
}

hardware_interface::return_type FakeRobot::start() { return hardware_interface::return_type::OK; }
hardware_interface::return_type FakeRobot::stop() { return hardware_interface::return_type::OK; }

hardware_interface::return_type FakeRobot::read(const rclcpp::Time &, const rclcpp::Duration &) {
  return hardware_interface::return_type::OK;
}

hardware_interface::return_type FakeRobot::write(const rclcpp::Time &, const rclcpp::Duration &) {
  return hardware_interface::return_type::OK;
}

std::vector<hardware_interface::StateInterface> FakeRobot::export_state_interfaces() { return {}; }
std::vector<hardware_interface::CommandInterface> FakeRobot::export_command_interfaces() { return {}; }