import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription 
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

import xacro


def generate_launch_description():

    # Check if we're told to use sim time
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('armsim'))
    xacro_file = os.path.join(pkg_path,'description','robot.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file).toxml()
    
    #Path to controller configuration
    controller_config = os.path.join(pkg_path,"config","my_controllers.yaml")
    # Create a robot_state_publisher node
    params = {'robot_description': robot_description_config, 'use_sim_time': use_sim_time}
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    # node_controller_manager_launcher = LaunchDescription([
    #     Node(
    #         package="controller_manager",
    #         executable="ros2_control_node",
    #         parameters=[
    #             {"robot_description":robot_description_config,"update_rate":30,"use_sim_time":use_sim_time},
    #             "/home/rushhaank/arm_sim/Arm_Sim/src/config/my_controllers.yaml"
    #         ],
    #         output="screen"
    #     )
    # ])

    rviz = LaunchDescription([
        Node(
            package="rviz2",
            executable="rviz2",
            parameters=[{"use_sim_time":use_sim_time}],
            output="screen"
        )
    ])

    #Launch Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory("gazebo_ros"),"launch","gazebo.launch.py"
        )]),
        launch_arguments={"verbose":"true"}.items()
    )

    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-entity","3dof_arm","-topic","robot_description"],
        output="screen",
        parameters=[{"use_sim_time":use_sim_time}])
    
    #Spawn the controllers
    spawn_joint_state_publisher = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        parameters=[{"use_sim_time":use_sim_time}],
        output="screen"
    )

    spawn_arm_position_controller = Node(
        package="controller_manager",
        executable="spawner",
        #Pass in config yaml so the controller manager knows gains
        arguments=["arm_position_controller","--param-file",controller_config],
        parameters=[{"use_sim_time":use_sim_time}],
        output="screen"
    )


    # Launch!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use sim time if true'),
            gazebo,
            node_robot_state_publisher,
            spawn_entity,
            #node_controller_manager_launcher,
            spawn_joint_state_publisher,
            spawn_arm_position_controller,
            rviz
    ])
