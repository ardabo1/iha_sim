import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration

def generate_launch_description():
    pkg_name = 'iha_sim'
    pkg_share = get_package_share_directory(pkg_name)

    # 1. Gazebo'nun modelleri bulabilmesi için yol tanımları
    # Bu ayar sayesinde Gazebo, 'models' klasörünü görebilecek.
    gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[
            os.path.join(pkg_share, 'models'),
            ':',
            os.path.join(pkg_share, 'worlds'),
        ]
    )

    # 2. Dünya dosyasının yolu
    world_file = PathJoinSubstitution([pkg_share, 'worlds', 'main.world'])

    # 3. Gazebo Harmonic Başlatma (ros_gz_sim)
    # -r: simülasyonu çalışır durumda başlatır (paused değil)
    # -v4: detaylı log gösterir
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': ['-r -v4 ', world_file]}.items()
    )

    # 4. (Opsiyonel) ROS-GZ Bridge
    # Eğer ROS üzerinden topic dinleyecekseniz (kamera, lidar vb.) buraya bridge eklenebilir.
    # Şimdilik boş bırakıyorum, ArduPilot zaten MAVLink üzerinden haberleşecek.
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # ÖRNEK: Gazebo'daki /camera topiğini ROS2'ye aktar
            '/camera@sensor_msgs/msg/Image@gz.msgs.Image',
            # ÖRNEK: Gazebo'daki /scan (Lidar) topiğini ROS2'ye aktar
            '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan'
        ],
        output='screen'
    )
    return LaunchDescription([
        gz_resource_path,
        gazebo,
        bridge
    ])
