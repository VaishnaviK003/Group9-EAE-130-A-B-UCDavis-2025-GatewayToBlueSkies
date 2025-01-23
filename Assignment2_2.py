# EAE 130A - Aircraft Performance and Design
# Assignment 2
# Group 9
# 31 January 2025

import math

# Stating the weight of the payload and crew member
weight_crew = 180  # lbs - from lecture slides
weight_payload = 2000  # lbs - from RFP

lift2drag_ratio_max = float(input("Enter the MAX L/D ratio: "))

lift2drag_ratio = 0.94 * lift2drag_ratio_max

Range = 600  # nmi - from RFP "range is the distance flown - use for cruise" lec03
Endurance = 30 / 60  # 30 min -> 0.5 hr from RFP "endurance is the time flown - use for loiter" lec03
c = float(input("Enter the specific fuel consumption value 'c' [1/s]: "))  # Updated units for clarity
velocity = 250 * 1.69  # knots to ft/s - maximum operational speed - from RFP

# Cruising
W5_W4 = math.exp((-Range * c) / (velocity * lift2drag_ratio))  # weight fraction during cruising
print("Weight fraction during cruising: " + str(round(W5_W4, 3)))

# Loitering
W7_W6 = math.exp((-Endurance * c) / (lift2drag_ratio))  # weight fraction during loitering
print("Weight fraction during loitering: " + str(round(W7_W6, 3)))

# For final weight fraction calculations, we are using the typical weight fractions
# Warmup (0.996), Taxi (0.995), Takeoff (0.996), Climb (0.998), Descent (0.999), and Landing (0.998)

W1_W0 = 0.996  # weight fraction for warm-up
W2_W1 = 0.995  # weight fraction for taxi
W3_W2 = 0.996  # weight fraction for takeoff
W4_W3 = 0.998  # weight fraction for climb
               # calculated weight fraction for cruising
W6_W5 = 0.999  # weight fraction for descent
               # calculated weight fraction for loitering
W8_W7 = 0.999  # weight fraction for descent (2)
W9_W8 = 0.998  # weight fraction for landing

W9_W0 = W9_W8 * W8_W7 * W7_W6 * W6_W5 * W5_W4 * W4_W3 * W3_W2 * W2_W1 * W1_W0

print("Weight fraction W9/W0: " + str(round(W9_W0, 3)))

# Now calculating the fuel fraction and accounting for the trapped fuel through multiplying by a factor of 1.06
Wf_W0 = (1 - W9_W0) * 1.06

print("Total fuel fraction Wf/W0: " + str(round(Wf_W0, 3)))

# Now we shall compute the takeoff gross weight through an iterative method
W0 = 19000  # lbs - initial guess for the empty weight
list_W0 = []  # creating an empty list to store W0 guesses to plot convergence
tol = 1e-6  # setting the convergence tolerance
i = 1  # setting a value greater than the tolerance for iteration purposes

A = 0.74  # Regression constants from Martin's Metabook which cites it from Raymer (2006, Table 3.1)
C = -0.03

while i > tol:
    list_W0.append(W0)  # adding the current value of W0 to the list
    We_W0 = A * (W0 ** C)  # formula for empty weight ratio - based on the current W0
    W0_new = (weight_crew + weight_payload) / (1 - Wf_W0 - We_W0)  # calculating the new takeoff gross weight
    i = abs(W0_new - W0) / abs(W0_new)  # finding the difference between the last and current iteration of W0
    W0 = W0_new  # updating the takeoff gross weight

We = We_W0 * W0

print("Empty weight: " + str(round(We, 3)) + " lbs")  # outputting the numerical value for the empty weight
print("Regression's empty weight fraction (We/W0): " + str(round(We_W0, 3)))  # if needed for further analysis

print("Takeoff Gross Weight (TOGW): " + str(round(W0)) + " lbs")  # outputting the takeoff gross weight as calculated from our model
