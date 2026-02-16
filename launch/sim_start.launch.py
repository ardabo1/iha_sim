import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'iha_sim'
    pkg_share = get_package_share_directory(pkg_name)

    # 1. Gazebo Harmonic için Kaynak Yolları
    # Modelleri ve dünyaları bulması için bu şart
    gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[
            os.path.join(pkg_share, 'models'),
            ':',
            os.path.join(pkg_share, 'worlds'),
        ]
    )

    # 2. Dünya Dosyası
    world_file = PathJoinSubstitution([pkg_share, 'worlds', 'sim.sdf'])

    # 3. Gazebo Harmonic'i DOĞRUDAN Başlatma (ExecuteProcess)
    # ros_gz_sim paketini çağırmak yerine direkt terminal komutu gibi 'gz sim' çalıştırıyoruz.
    # Bu sayede 'ign' (eski sürüm) açılma ihtimalini %100 ortadan kaldırıyoruz.
    gazebo_process = ExecuteProcess(
        cmd=['gz', 'sim', '-r', '-v4', world_file],
        output='screen'
    )

    # 4. Bridge (Köprü)
    # Gazebo <-> ROS 2 haberleşmesi
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # İhtiyaç duyarsan topicleri buraya açarsın
            # '/camera@sensor_msgs/msg/Image@gz.msgs.Image',
        ],
        output='screen'
    )

    return LaunchDescription([
        gz_resource_path,
        gazebo_process,
        bridge,
    ])