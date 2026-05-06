# map_loader.launch.py — Humble compatible

import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    bringup_share = get_package_share_directory('testbed_bringup')
    default_map = os.path.join(bringup_share, 'maps', 'testbed_world.yaml')

    # Fallback for workspaces where testbed_bringup installs YAML but not image assets.
    installed_map_image = Path(bringup_share) / 'maps' / 'testbed_world.pgm'
    if not installed_map_image.exists():
        workspace_root = None
        for parent in Path(bringup_share).resolve().parents:
            if (parent / 'src').exists():
                workspace_root = parent
                break
        if workspace_root is not None:
            for candidate in (workspace_root / 'src').rglob('testbed_bringup/maps/testbed_world.yaml'):
                if candidate.with_suffix('.pgm').exists():
                    default_map = str(candidate)
                    break

    map_file = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time')

    declare_map = DeclareLaunchArgument(
        'map',
        default_value=default_map,
        description='Absolute path to map yaml file',
    )
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation clock',
    )

    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[
            {
                'yaml_filename': map_file,
                'use_sim_time': use_sim_time,
            },
        ],
    )

    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_map',
        output='screen',
        parameters=[
            {
                'autostart': True,
                'node_names': ['map_server'],
                'use_sim_time': use_sim_time,
            }
        ],
    )

    return LaunchDescription([
        declare_map,
        declare_use_sim_time,
        map_server,
        lifecycle_manager,
    ])