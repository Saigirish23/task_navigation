# 🤖 Navigation Task — Testbed-T1.0.0

**Hey Folks!** 👋

Now that you're familiar with **mapping** and have a rough idea of **localization** too, let's take things a step higher — we're going to look at **Navigation!** 🚀

In this task, you'll wire up a complete Nav2 navigation stack for our custom differential-drive robot. Given a **pre-built map**, your job is to make the robot **localize itself** and **autonomously navigate** to any goal you click in RViz.

---

## 📁 File Structure

```
task_navigation/
├── testbed_bringup/                  # Launches Gazebo world + robot + RViz
│   ├── launch/
│   │   └── testbed_full_bringup.launch.py
│   ├── maps/
│   │   ├── testbed_world.pgm         # Pre-built occupancy grid image
│   │   └── testbed_world.yaml        # Map metadata (resolution, origin, etc.)
│   ├── CMakeLists.txt
│   └── package.xml
│
├── testbed_description/              # Robot model (URDF/Xacro) + RViz configs
│   ├── launch/
│   │   ├── robot_description.launch.py
│   │   └── testbed_rviz_barebones.launch.py
│   ├── meshes/                       # STL meshes for the robot
│   ├── rviz/                         # RViz config files
│   ├── urdf/                         # Robot URDF/Xacro files
│   ├── CMakeLists.txt
│   └── package.xml
│
├── testbed_gazebo/                   # Gazebo simulation world + models
│   ├── launch/
│   │   ├── spawn_playground.launch.py
│   │   └── spawn_testbed.launch.py
│   ├── models/                       # Custom Gazebo models (walls, rooms, etc.)
│   ├── worlds/                       # .world files for Gazebo
│   ├── CMakeLists.txt
│   └── package.xml
│
├── testbed_navigation/               # ⭐ YOUR WORKSPACE — Nav2 stack
│   ├── config/
│   │   ├── amcl_params.yaml          # AMCL localization parameters
│   │   └── nav2_params.yaml          # Full Nav2 stack parameters
│   ├── launch/
│   │   ├── map_loader.launch.py      # ✅ Already done — loads the map
│   │   ├── localization.launch.py    # 📝 YOU COMPLETE THIS
│   │   └── navigation.launch.py     # 📝 YOU COMPLETE THIS
│   ├── CMakeLists.txt
│   └── package.xml
│
├── media/
│   └── Navigation_assignment.mp4     # Demo video of the final result
│
└── README.md                         # ← You are here!
```

---

## 📦 What Each Folder Does (Quick Summary)

| Folder | What's Inside |
|---|---|
| **`testbed_bringup/`** | The main launch file that brings up the full simulation — spawns the Gazebo world, loads the robot, and opens RViz. Also contains the **pre-built map** files (`.pgm` + `.yaml`). |
| **`testbed_description/`** | Everything about the robot's physical model — URDF/Xacro files that define the robot's shape, joints, sensors, and wheels, along with STL meshes and RViz display configs. |
| **`testbed_gazebo/`** | The Gazebo simulation setup — world files that define the environment, custom 3D models (walls, fences, rooms), and launch files to spawn the world and robot into Gazebo. |
| **`testbed_navigation/`** | **⭐ Your workspace!** Contains the Nav2 config files (`amcl_params.yaml`, `nav2_params.yaml`), the already-completed `map_loader.launch.py`, and the two launch files **you need to write**. |

---

## ⚙️ Compatibility & System Requirements

| Requirement | Version |
|---|---|
| **OS** | Ubuntu 22.04 (Jammy Jellyfish) |
| **ROS 2** | Humble Hawksbill |
| **Gazebo** | Gazebo Classic 11.10.2 |
| **Build System** | colcon |

> ⚠️ **Important:** This project is built and tested on **ROS 2 Humble** with **Gazebo Classic 11**. If you're running a different distro (e.g., Jazzy, Iron) or a different Gazebo version (e.g., Ignition/Gz Sim), you **will** run into plugin and dependency mismatches. Stick with Humble!

---

## 🔧 Setup

### 1. Install ROS 2 Humble (if not already installed)

Follow the official guide: [ROS 2 Humble Installation](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)

### 2. Install Nav2 and Dependencies

```bash
sudo apt update
sudo apt install -y \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-robot-state-publisher \
  ros-humble-joint-state-publisher \
  ros-humble-xacro \
  ros-humble-rviz2
```

### 3. Clone and Build

```bash
# Create your workspace (skip if you already have one)
mkdir -p ~/nav_ws/src
cd ~/nav_ws/src

# Clone this repo
git clone https://github.com/Saigirish23/task_navigation.git .

# Go back to workspace root and build
cd ~/nav_ws
colcon build
source install/setup.bash
```

> 💡 **Tip:** Add `source ~/nav_ws/install/setup.bash` to your `~/.bashrc` so you don't have to source it every time.

---

## 🚀 Launching the Simulation

To bring up the Gazebo world with the robot and RViz:

```bash
ros2 launch testbed_bringup testbed_full_bringup.launch.py
```

This will open:
- **Gazebo** — the 3D simulation with the playground world
- **RViz** — for visualization
- The robot spawned and ready to go!

---

## 📝 Your Task

Given the **pre-built map** and the **working bringup**, your job is to complete the Nav2 navigation stack by writing two launch files:

### **1. `localization.launch.py`** (in `testbed_navigation/launch/`)

This launch file should start the **AMCL (Adaptive Monte Carlo Localization)** node and its lifecycle manager.

- **What it does:** AMCL takes the map + laser scans + odometry and figures out **where the robot is** on the map.
- **Hint:** Use the `amcl_params.yaml` config file from the `config/` folder.
- **Nodes to launch:**
  - `nav2_amcl` → the AMCL node
  - `nav2_lifecycle_manager` → manages the AMCL node's lifecycle

### **2. `navigation.launch.py`** (in `testbed_navigation/launch/`)

This launch file should bring up the **full Nav2 navigation stack** — planner, controller, behaviors, and everything in between.

- **What it does:** Once the robot knows where it is (thanks to AMCL), the Nav2 stack plans a path and drives the robot to the goal.
- **Hint:** Use the `nav2_params.yaml` config file from the `config/` folder.
- **Key nodes/servers to launch:**
  - `controller_server` — follows the planned path
  - `planner_server` — plans a global path
  - `behavior_server` — recovery behaviors (spin, backup, wait)
  - `bt_navigator` — behavior tree navigator
  - `smoother_server` — smooths the planned path
  - `velocity_smoother` — smooths velocity commands
  - `waypoint_follower` — follows a series of waypoints
  - `collision_monitor` — safety collision monitoring
  - `nav2_lifecycle_manager` — manages all the above nodes

### 📖 Reference

Refer to the official Nav2 repository for examples of how these launch files are structured:

🔗 **[https://github.com/ros-navigation/navigation2](https://github.com/ros-navigation/navigation2)**

Specifically, check out:
- `nav2_bringup/launch/` — for launch file patterns
- `nav2_bringup/params/` — to understand how params are loaded

### ✅ Already Done For You

- `map_loader.launch.py` — Loads and publishes the map via `nav2_map_server`. Take a look at this file for a reference on how to structure your launch files!

---

## 🐛 Common Errors (& How to Fix Them)

### 1. 🔌 Plugin Mismatch (Humble vs Jazzy)

```
[ERROR] Failed to load plugin: nav2_mppi_controller::MPPIController
```

**Why:** Nav2 plugin names changed between ROS 2 distros (Humble → Jazzy). The `nav2_params.yaml` uses Humble-specific plugin names.

**Fix:** Make sure you're running **ROS 2 Humble**, not Jazzy or Iron. Plugin class names differ across distros.

### 2. 📂 Wrong Path or Name (Case Sensitive!)

```
[ERROR] Package 'Testbed_Navigation' not found
```

**Why:** ROS 2 package names are **case-sensitive**. The package is `testbed_navigation`, not `Testbed_Navigation` or `TestBed_Navigation`.

**Fix:** Double-check every package name, file name, and path in your launch files. Linux file systems are case-sensitive!

### 3. 🗺️ Map Not Loading / Map Server Crash

```
[ERROR] [map_server]: yaml_filename parameter not set
```

**Why:** The map YAML path might be incorrect, or the `.pgm` image file is missing from the installed path.

**Fix:** Make sure you've done a `colcon build` **and** sourced `install/setup.bash`. The map files need to be installed to the share directory.

### 4. ⏳ Lifecycle Nodes Not Transitioning

```
[WARN] [lifecycle_manager]: Node amcl is not yet active...
```

**Why:** The lifecycle manager can't activate a node if it hasn't fully started yet. This usually happens when nodes are started in the wrong order or the `autostart` parameter is missing.

**Fix:** Make sure your lifecycle manager has `'autostart': True` and the `'node_names'` list matches the exact names of the nodes you're launching.

### 5. 🔄 Transform (TF) Errors

```
[WARN] Timed out waiting for transform from base_footprint to map
```

**Why:** AMCL hasn't published the `map → odom` transform yet, or the robot state publisher isn't running.

**Fix:** Ensure the bringup launch is running first (it starts robot_state_publisher). AMCL needs a few seconds + an initial pose estimate to start publishing transforms.

### 6. 🔨 Build Errors After Cloning

```
Could not find a package configuration file provided by "nav2_common"
```

**Why:** Missing Nav2 dependencies.

**Fix:** Run the install command from the [Setup](#-setup) section to install all required Nav2 packages.

---

## 🎬 Expected Result

Once everything is working, you should be able to:

1. Launch the bringup (Gazebo + RViz)
2. Launch the map loader, localization, and navigation
3. Set an **initial pose** in RViz (2D Pose Estimate)
4. Click a **Nav2 Goal** (2D Goal Pose) in RViz
5. Watch the robot **autonomously navigate** to the goal! 🎉

Check out the demo video in `media/Navigation_assignment.mp4` to see what the final result looks like!

---

## 🏗️ Build & Test Workflow

```bash
# 1. Build the workspace
cd ~/nav_ws
colcon build
source install/setup.bash

# 2. Terminal 1 — Launch the simulation
ros2 launch testbed_bringup testbed_full_bringup.launch.py

# 3. Terminal 2 — Launch navigation (includes map + localization + nav2 stack)
ros2 launch testbed_navigation navigation.launch.py
```

> 💡 **Pro Tip:** The `navigation.launch.py` is designed to include `map_loader.launch.py` and `localization.launch.py` internally. So once all three files are complete, you only need to run the navigation launch!

---

**Good luck, and happy navigating!** 🧭🤖
