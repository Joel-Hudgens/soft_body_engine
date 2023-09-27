# Soft Body Physics Engine

Welcome to the Soft Body Physics Engine repository! This program is a simple implementation of a soft body physics simulation using Python and the Pygame library. In this README, we'll explain the basics of the "pressure model" soft body and how it works, as well as provide an overview of how we use vectors for each point along with connected springs to create the soft body circle. Let's dive into the fun world of soft body physics!

## What is a Soft Body?

A soft body is a 2D or 3D object that deforms and reacts realistically to external forces, just like real-world materials such as rubber or cloth. This simulation mimics the behavior of soft bodies by modeling the interactions between individual points (particles) connected by springs.

## How the Pressure Model Soft Body Works

### Particle System
- The soft body is represented by a collection of interconnected particles, each behaving like a point mass.
- These particles are arranged in a circular shape, which forms our soft body circle.

### Springs
- Springs are virtual connections between particles.
- When the distance between two connected particles deviates from a rest length, a spring force is applied.
- The stiffness of the springs and their rest lengths are adjustable parameters, influencing the softness or rigidity of the body.

### Gravity
- The simulation incorporates gravity, causing each particle to experience a downward force.
- The strength of gravity is customizable to control how quickly the soft body reacts to it.

### Pressure Model
- This soft body simulation introduces a pressure model.
- When particles get closer to each other than their natural spacing, a repulsive force is generated to simulate internal pressure.
- This pressure helps the soft body maintain its shape and prevents it from collapsing entirely.

### Integration and Collision
- The positions and velocities of particles are updated based on the forces acting on them over time using numerical integration.
- The simulation handles collisions with the ground and walls to ensure particles stay within the screen boundaries.

### Calculations
- 1. Positions of particles are updated based on their current velocities and the elapsed time.
- 2. Velocities of particles are updated considering spring forces and gravity.
- 3. Collisions with the ground and screen boundaries are detected and handled, resetting positions and velocities as needed.


## How to Interact with the Simulation

- Use the **Arrow Keys** to move the soft body circle around the screen.
- Press the **Spacebar** to pause and unpause the simulation.
- Click and drag the mouse to draw lines on the screen that interact with the soft body.

## Requirements
- Python3 or any higher version
- pip install pygame
