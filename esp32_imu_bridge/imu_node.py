#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import serial

class ESP32ImuNode(Node):
    def __init__(self):
        super().__init__('imu_node')
        self.publisher_ = self.create_publisher(Imu, '/imu/data_raw', 10)
        
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        
        port = self.get_parameter('port').get_parameter_value().string_value
        baudrate = self.get_parameter('baudrate').get_parameter_value().integer_value
        
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            self.get_logger().info(f"Successfully connected to ESP32 on {port}")
        except Exception as e:
            self.get_logger().error(f"Failed to connect to serial port: {e}")
            raise e

        # Timer running at 50 Hz (0.02s)
        self.timer = self.create_timer(0.02, self.timer_callback)

    def timer_callback(self):
        try:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                val = [float(x) for x in line.split(',')]
                
                if len(val) >= 6:
                    imu_msg = Imu()
                    imu_msg.header.stamp = self.get_clock().now().to_msg()
                    imu_msg.header.frame_id = "imu_link"
                    
                    # Linear acceleration
                    imu_msg.linear_acceleration.x = val[0]
                    imu_msg.linear_acceleration.y = val[1]
                    imu_msg.linear_acceleration.z = val[2]
                    
                    # Angular velocity
                    imu_msg.angular_velocity.x = val[3]
                    imu_msg.angular_velocity.y = val[4]
                    imu_msg.angular_velocity.z = val[5]
                    
                    self.publisher_.publish(imu_msg)
        except Exception:
            pass

def main(args=None):
    rclpy.init(args=args)
    node = ESP32ImuNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()