# EAE 130A - Aircraft Performance and Design
# Assignment 2 - Cost Estimate
# Group 9
# 31 January 2025

import math

### PART C ###

# Using the cost escalation factor (CEF) to convert the costs between different years

base_year = 1989 # Roskam uses 1989 as the base year for calculations
                 # and we have chosen to stick with Roskam -
                 # using euqations cited in Metabook (2025 works better with numbers and is our reference year)
then_year = 2024 # Year representing the technology level of the aircraft 

# For 2024 - equation from Metabook
base_CEF = 5.17053 + 0.104981 * (base_year - 2006)
then_CEF = 5.17053 + 0.104981 * (then_year - 2006)

CEF = then_CEF / base_CEF

# Total aircraft and engine price for a turboprop commuter aircraft
MTOW = float(input("Enter the Mean Takeoff Weight (lbs): "))  # Resulting value from Weight Estimate code
SHP_TO = float(input("Enter the Takeoff Shaft Horsepower (shp): "))

cost_aircraft = (10 ** (1.1846 + (1.2625 * math.log10(MTOW)))) * CEF  # Aircraft cost
cost_engine = (10 ** (2.5262 + (0.9465 * math.log10(SHP_TO)))) * CEF  # Turboprop engine

print("Total cost of aircraft + engine: $" + str(round(cost_aircraft + cost_engine, 2)))

cost_airframe = cost_aircraft - cost_engine
print("Total cost of airframe: $" + str(round(cost_airframe, 2)))

# Cash Operating Cost (COC) - costs directly related to flights

block_time = float(input("Enter the block time (hrs): ")) # the overall time for which the aircraft is in use for a given mission, measured
                                                          # from the time the wheel blocks are removed before departure, to the time they
                                                          # are placed after arrival at the destination.
cost_crew = 0.34 * (2.75 * (MTOW ** 0.40) * block_time) * CEF
print("Cost of crew: $" + str(round(cost_crew, 2)))

# Cost of fuel
fuel_weight = float(input("Enter the weight of the fuel (lbs): "))
P_f = 1.83 # price per gallon of fuel (for ethanol) (USD/gal)
rho_f = 6.59 # fuel density (lbs/gal)
cost_fuel = 1.02 * fuel_weight * (P_f / rho_f)

print("Cost of fuel: $" + str(round(cost_fuel, 2)))

# Cost of oil
weight_oil = 0.0125 * fuel_weight * (block_time / 100)
P_oil = 95 # price per gallon of oil (USD/gal)
rho_oil = 7.29 # oil density (lbs/gal)
cost_oil = 1.02 * weight_oil * (P_oil / rho_oil)

print("Cost of oil: $" + str(round(cost_oil, 2)))

# Landing Fees
cost_airport = 1.5 * (MTOW / 1000) * CEF
print("Cost of landing fees: $" + str(round(cost_airport, 2)))

# Airframe Maintenance Fees
empty_weight = float(input("Enter the empty weight (lbs): "))
engine_weight = 331 # engine weight (lbs)
airframe_weight = empty_weight - engine_weight
R_L = 36.25 # labor rate (USD/hr)

C_ML = 1.03 * (3 + (0.067 * airframe_weight / 1000)) * R_L
C_MM = (1.03 * 30 * CEF) + ((0.79 * 10 ** -5) * cost_airframe)
cost_airframe_maintenance = (C_ML + C_MM) * block_time

print("Cost of airframe maintenance fees: $" + str(round(cost_airframe_maintenance, 2)))

# Engine Maintenance Fees
num_engines = 1 # number of engines
H_em = 4000 # number of hours between engine overhauls (hrs)
C_ML_engine = 1.03 * 1.3 * (0.4956 + 0.0532 * ((SHP_TO / num_engines) / 1000) * (1100 / H_em) + 0.1) * R_L
T_0 = 976 * 0.85 # engine maximum thrust (lbs) - calcuated from maximum speed and takeoff shaft horsepower
C_MM_engine = (25 + (18 * T_0 / 10 ** 4)) * (0.62 + 0.38 / block_time) * CEF
cost_engine_maintenance = num_engines * block_time * (C_ML_engine + C_MM_engine)

print("Cost of engine maintenance fees: $" + str(round(cost_engine_maintenance, 2)))

# FOC
# Insurance
U_annual = (1.5 * 10 ** 3) * (3.4546 * block_time + 2.994 - (
    (12.289 * block_time ** 2) - (5.6626 * block_time) + 8.964) ** 0.5)
C_insurance = ((0.02 * cost_aircraft) / U_annual) * block_time
print("Cost of insurance fees: $" + str(round(C_insurance, 2)))

# Direct Operating Cost (DOC)
DOC = (cost_crew + cost_fuel + cost_oil + cost_airport +
       cost_airframe_maintenance + cost_engine_maintenance + C_insurance)

# Fixed Operating Cost

# Financing
C_financing = 0.07 * DOC
print("Cost of financing (loan) fees: $" + str(round(C_financing, 2)))

# Registration tax fees
C_registration = (0.001 + (10 ** -8) * MTOW) * DOC
print("Cost of registration fees: $" + str(round(C_registration, 2)))

# Update total DOC to include fixed operating costs
DOC += (C_financing + C_registration)
#print(str(DOC))

DOC_final = DOC  * (2000 / (600 * 2000)) # DOC is in USD (assumed) and so 2000 lb payload and 1 ton is 2000 lbs so unit conversions are performed and 600 nmi range is used

print("The Direct Operating Cost (DOC) is estimated to be (USD/cargo ton-nmi): " + str(round(DOC_final, 2))) 
# DOC is in USD / cargo ton-nmi


### Roskam pg. 326 (text page 301) - cost of aircraft

cost_check = CEF * (10 ** (-1.1174 + (1.8459 * (math.log10(MTOW)))))
print("Cost of airplane (flyaway cost) estimate according to Roskam: " + str(cost_check))

### PARTS A & B ###



# Production cost = Flyaway cost: production costs consists on the materials and labor costs required to manufacture the aircraft,
# and it includes tooling costs
# Production cost and RDT&E cost are given as a combo since it is difficult to differentiate both
# Using Raymer's text for these formulas pg. 732

year = 2024 # assignment asks for the then_year of 2024

max_vel = 250 # knots - from RFP - maximum operating velocity
Q = 125 # lesser of production quantity
eng_hours = 4.86 * (empty_weight**0.777) * (max_vel**0.621) * (Q**0.163)
labor_rate_eng = (2.576 * year) - 5058 # all the labor cost equations are coming from the lecture slides 04
eng_cost = labor_rate_eng * eng_hours

tooling_hrs = 5.99 * (empty_weight**0.777) * (max_vel**0.696) * (Q**0.263)
labor_rate_tooling = (2.883 * year) - 5666
tooling_cost = labor_rate_tooling * tooling_hrs

manufacturing_hrs = 7.37 * (empty_weight**0.82) * (max_vel**0.484) * (Q**0.641)
labor_rate_manufacturing = (2.316 * year) - 4552
manufacturing_cost = labor_rate_manufacturing * manufacturing_hrs

quality_control_hrs = 0.076 # since it is a cargo plane
labor_rate_qc = (2.60 * year) - 5112
qc_cost = labor_rate_qc * quality_control_hrs

development_support_cost = 91.3 * (empty_weight**0.63) * (max_vel**1.3)

FTA = 2 # number of flight-test aircraft (typically between 2 ~ 6)
flight_test_cost = 2498 * (empty_weight**0.325) * (max_vel**0.822) * (FTA**1.21)

manufacturing_materials_cost = 22.1 * (empty_weight**0.921) * (max_vel**0.621) * (Q**0.799)

engine_max_Ma = 0.378 #  engine maximum Mach number - converting from 250 knots to Mach num
turbine_inlet_temp = 2381 # inlet temperature of the turbine in Rankine
engine_production_cost = 3112 * ((0.043 * T_0) + (243.25 * engine_max_Ma) + (0.969 * turbine_inlet_temp) - 2228)
# T_0 is the max engine thrust, as defined previously. Ma = Mach number. Turbine inlet temp in Rankine.

total_num = 125 # total quantity of production

num_per_aircraft = 1 # number of engines per aircraft

cost_avionics = 48149 # cost of avionics (GPS system, etc.) in USD

production_cost = (eng_cost + tooling_cost + manufacturing_cost +
                   qc_cost + development_support_cost + flight_test_cost +
                   manufacturing_materials_cost +
                   (engine_production_cost * total_num * num_per_aircraft)
                   + (cost_avionics * total_num)) # combination of RDT&E + flyaway

print("RDT&E + Production Costs: $" + str(round(production_cost/125, 2)))



#profit_margin = ((production_cost) + (0.1 * production_cost)) / 125
#print("Flyaway cost per airline with a 10% profit margin: $" + str(round(profit_margin, 2)))

flyaway_cost = cost_airframe + cost_engine + cost_avionics # according to lec 04 slide 13, flyaway is labeled as airframe engine and avionics only
profit = flyaway_cost + (0.1 * flyaway_cost)

print("Flyaway cost per airplane with a 10% profit margin: $" + str(round((profit), 2)))








