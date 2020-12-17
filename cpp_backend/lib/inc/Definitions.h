#ifndef _DEFINITIONS_H_
#define _DEFINITIONS_H_

/// Gravity constant in m^3 / (kg s^2)
const double GRAVITY_CONSTANT = 6.6743e-11;

/// Mass of particles, somewhat large to compensate the force
const double PARTICLE_MASS = 5e4;

/// Dampening of velocity
const double VELOCITY_DAMPENING = 0.99;

/// Max speed to prevent explosions
const double V_MAX = 0.5;

/// Half size of the world
const double X_MAX = 1.5;

#endif
