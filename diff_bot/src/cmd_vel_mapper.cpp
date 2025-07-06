#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"

class Mapper : public rclcpp::Node
{
public:
    Mapper() : Node("converter")
    {
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>(
            "/diff_cont/cmd_vel_unstamped", 10);

        subscriber_ = this->create_subscription<geometry_msgs::msg::Twist>(
            "/cmd_vel", 10, std::bind(&Mapper::callback, this, std::placeholders::_1));
    }

private:
    void callback(const geometry_msgs::msg::Twist::SharedPtr msg)
    {
        geometry_msgs::msg::Twist new_msg;
        new_msg.linear = msg->linear;
        new_msg.angular = msg->angular;
        publisher_->publish(new_msg);
    }

    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr subscriber_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Mapper>());
    rclcpp::shutdown();
    return 0;
}
