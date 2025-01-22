# EAE 130A - Aircraft Performance and Design
# Assignment 2
# Group 9
# 31 January 2025

import math

# Function to calculate cruise weight fraction
def cruise_weight_fraction(R, c, eta, CL_CD):
    return math.exp(-R * c / (eta * CL_CD))

# Function to calculate loiter weight fraction
def loiter_weight_fraction(E, V, c, eta, CL_CD):
    return math.exp(-E * V * c / (eta * CL_CD))

# Inputs for cruise - propeller (used to calculate the weight fractions for the fuel weight fraction)
R = float(input("Enter range during cruise (R) in miles: ")) * 5280  # Converting miles to feet

# Inputs for loiter - propeller (used to calculate the weight fractions for the fuel weight fraction)
E = float(input("Enter endurance during loiter (E) in hours: ")) * 3600  # Converting hours to seconds
V = float(input("Enter cruise velocity (V_∞) in ft/s: "))

efficiency_propeller = float(input("Enter propeller efficiency (η): "))
CL_CD = float(input("Enter lift-to-drag ratio (C_L/C_D): "))
c = float(input("Enter specific fuel consumption (c) in lb/(hp-hr): "))

# Calculate weight fractions
Wi_plus1_Wi_cruise = cruise_weight_fraction(R, c, efficiency_propeller, CL_CD)
Wi_plus1_Wi_loiter = loiter_weight_fraction(E, V, c, efficiency_propeller, CL_CD)

# Output results
print(f"\nWeight fraction for cruise (W_(i+1)/W_i): {Wi_plus1_Wi_cruise:.4f}")
print(f"Weight fraction for loiter (W_(i+1)/W_i): {Wi_plus1_Wi_loiter:.4f}")

# Input crew weight and payload weight (given constants)
weight_crew = float(input("Enter crew weight (lbs): "))
weight_payload = float(input("Enter payload weight (lbs): "))

# Empty weight fraction calculation - using historical data
print("\nTo calculate the empty weight fraction, we will use regression constants A and B such that:")
print("log(W0) = A + B * log(We)")

A = float(input("Enter the value of A: "))
B = float(input("Enter the value of B: "))

# Initial guess for takeoff weight (W0)
W0_initial = float(input("\nEnter an initial guess for the takeoff weight (lbs): "))

# Calculating W0 iteratively
tolerance = 1e-6  # Convergence tolerance
max_iterations = 100  # Maximum number of iterations
i = 0  # Iteration number (starting at 0)
W0 = W0_initial

while i < max_iterations:
    # Calculate We/W0 based on the initial guess for W0 and the regression constants
    empty_weight_fraction = 10 ** (A + B * math.log10(W0))
    
    # Check if the fraction is valid
    if empty_weight_fraction >= 1:
        print("\nError: Invalid empty weight fraction.")
        break

    # Calculate Wf/W0 based on a typical value or user input
    fuel_weight_fraction = float(input("\nEnter the fuel weight fraction (Wf/W0): "))
    
    # Update W0 using the formula
    W0_new = (weight_crew + weight_payload) / (1 - empty_weight_fraction - fuel_weight_fraction)
    
    # Check for convergence
    if abs(W0_new - W0) < tolerance:
        W0 = W0_new
        print(f"\nTakeoff weight (W0) has converged to: {W0:.2f} lbs")
        break
    
    W0 = W0_new
    i += 1

if i == max_iterations:
    print("\nThe calculation did not converge within the maximum number of iterations.")
