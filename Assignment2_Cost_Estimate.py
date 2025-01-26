# EAE 130A - Aircraft Performance and Design
# Assignment 2 - Cost Estimate
# Group 9
# 31 January 2025

import math

# Using the cost escalation factor (CEF) to convert the costs between different years

base_year = 1989 # Roskam uses 1989 as the base year for calculations and we have chosen to stick with Roskam - using euqations cited in Metabook
then_year = 2035 # Year representing the technology level of the aircraft 

# For 2025 - equation from Metabook
base_CEF = 5.17053 + 0.104981 * (base_year - 2025)
then_CEF = 5.17053 + 0.104981 * (then_year - 2025)

CEF = then_CEF / base_CEF

# Total aircraft and engine price for a turboprop commuter aircraft
MTOW = float(input("Enter the Mean Takeoff Weight (lbs): "))  # Resulting value from Weight Estimate code
SHP_TO = float(input("Enter the Takeoff Shaft Horsepower (hp): "))

cost_aircraft = (10 ** (1.1846 + 1.2625 * math.log10(MTOW))) * CEF  # Aircraft cost
cost_engine = (10 ** (2.5262 + 0.9465 * math.log10(SHP_TO))) * CEF  # Turboprop engine

print("Total cost of aircraft + engine: $" + str(round(cost_aircraft + cost_engine, 2)))

cost_airframe = cost_aircraft - cost_engine
print("Total cost of airframe: $" + str(round(cost_airframe, 2)))

# Cash Operating Cost (COC) - costs directly related to flights

block_time = float(input("Enter the block time (hrs): "))
cost_crew = 0.34 * (2.75 * (MTOW ** 0.40) * block_time) * CEF

# Cost of fuel
fuel_weight = float(input("Enter the weight of the fuel (lbs): "))
P_f = float(input("Enter the price per gallon of fuel (USD/gal): "))
rho_f = float(input("Enter the fuel density (lbs/gal): "))
cost_fuel = 1.02 * fuel_weight * (P_f / rho_f)

print("Cost of fuel: $" + str(round(cost_fuel, 2)))

# Cost of oil
weight_oil = 0.0125 * fuel_weight * (block_time / 100)
P_oil = float(input("Enter the price per gallon of oil (USD/gal): "))
rho_oil = float(input("Enter the oil density (lbs/gal): "))
cost_oil = 1.02 * weight_oil * (P_oil / rho_oil)

print("Cost of oil: $" + str(round(cost_oil, 2)))

# Landing Fees
cost_airport = 1.5 * (MTOW / 1000) * CEF
print("Cost of landing fees: $" + str(round(cost_airport, 2)))

# Airframe Maintenance Fees
empty_weight = float(input("Enter the empty weight (lbs): "))
engine_weight = float(input("Enter the engine weight (lbs): "))
airframe_weight = empty_weight - engine_weight
R_L = float(input("Enter the labor rate (USD/hr): "))

C_ML = 1.03 * (3 + (0.067 * airframe_weight / 1000)) * R_L
C_MM = (1.03 * 30 * CEF) + ((0.79 * 10 ** -5) * cost_airframe)
cost_airframe_maintenance = (C_ML + C_MM) * block_time

print("Cost of airframe maintenance fees: $" + str(round(cost_airframe_maintenance, 2)))

# Engine Maintenance Fees
num_engines = float(input("Enter the number of engines: "))
H_em = float(input("Enter the number of hours between engine overhauls (hrs): "))
C_ML_engine = 1.03 * 1.3 * (0.4956 + 0.0532 * ((SHP_TO / num_engines) / 1000) * (1100 / H_em) + 0.1) * R_L
T_0 = float(input("Enter the engine maximum thrust (lbs): "))
C_MM_engine = (25 + (18 * T_0 / 10 ** 4)) * (0.62 + 0.38 / block_time) * CEF
cost_engine_maintenance = num_engines * block_time * (C_ML_engine + C_MM_engine)

print("Cost of engine maintenance fees: $" + str(round(cost_engine_maintenance, 2)))

# Direct Operating Cost (DOC)
DOC = (cost_crew + cost_fuel + cost_oil + cost_airport +
       cost_airframe_maintenance + cost_engine_maintenance)

# Fixed Operating Cost
# Insurance
U_annual = (1.5 * 10 ** 3) * (3.4546 * block_time + 2.994 - (
    (12.289 * block_time ** 2) - (5.6626 * block_time) + 8.964) ** 0.5)
C_insurance = ((0.02 * cost_aircraft) / U_annual) * block_time
print("Cost of insurance fees: $" + str(round(C_insurance, 2)))

# Financing
C_financing = 0.07 * DOC
print("Cost of financing (loan) fees: $" + str(round(C_financing, 2)))

# Registration tax fees
C_registration = (0.001 + (10 ** -8) * MTOW) * DOC
print("Cost of registration fees: $" + str(round(C_registration, 2)))

# Update total DOC to include fixed operating costs
DOC += (C_insurance + C_financing + C_registration)

print("The Direct Operating Cost (DOC) is estimated to be: $" + str(round(DOC, 2)))


