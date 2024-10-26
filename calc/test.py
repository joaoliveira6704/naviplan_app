import math

# Constants
R = 287.05  # J/(kg·K)

# Input for aircraft type
acType = int(input("Select Aircraft type (A320/B737/A321/A330 (ENTER LAST THREE DIGITS ONLY)): "))
flapSetting = int(input("Enter Flap Setting (1-2-3-4): "))

# Input for airport elevation
airportElevation_F = int(input("Enter airport elevation (ft): "))  # Elevation above sea level
airportElevation = airportElevation_F / 3.280

# Input for wind conditions
windSpeed = int(input("Enter wind speed (knots): "))  # Wind speed in knots
windDirection = input("Enter wind direction (headwind/tailwind): ")  # Wind direction

# Input for outside air temperature
oAT = int(input("Enter Outside Temperature (ºC): "))  # Outside air temperature in Celsius

isa = 15 - ((airportElevation_F/1000 * (1.98 * (-1))))

flex = oAT + isa + 20

# Calculate air pressure at the elevation
sea_level_pressure = 1013.25  # Standard sea-level pressure in hPa
# Approximate pressure drop with elevation (in hPa)
airPressure = sea_level_pressure * math.exp(-airportElevation / 8400)

# Calculate air density
airDensity = airPressure / (R * (oAT + 273.15))

# Debug: Check air density
print(f"Calculated Air Density: {airDensity:.3f} kg/m³")

# Lift coefficients based on flap settings
match flapSetting:
    case 1:
        liftCoefficient_min = 0.5
        liftCoefficient_max = 0.6
    case 2:
        liftCoefficient_min = 0.7
        liftCoefficient_max = 0.9
    case 3:
        liftCoefficient_min = 1.0
        liftCoefficient_max = 1.2
    case 4:
        liftCoefficient_min = 1.4
        liftCoefficient_max = 1.6
    case _:
        print("Invalid flap setting!")
        exit(1)

# Wing area for different aircraft types
match acType:
    case 320 | 321:
        wingarea = 35.80  # Correct wing area in m²
    case 737:
        wingarea = 34.31  # Correct wing area in m²
    case 330:
        wingarea = 60.30  # Correct wing area in m²
    case _:
        print("Invalid type or not supported yet!")
        exit(1)

# Input for gross weight
grossWeight = int(input("Enter aircraft gross weight (kg): "))  # Ensure this is realistic

# Calculate V1, V2, and VR
# Use the given formula for V1
divisionV1 = math.sqrt(grossWeight / 60000)
v1 = 1.2 * divisionV1 * 113  # V1 calculation with a factor of 113

# Calculate stall speeds
# Check for realistic stall speeds based on air density and wing area
divisionvStallmin = airDensity * wingarea * liftCoefficient_min * 28.5
divisionvStallmax = airDensity * wingarea * liftCoefficient_max * 28.5

# Calculate stall speeds
vStallmin = math.sqrt((2 * grossWeight) / divisionvStallmin)
vStallmax = math.sqrt((2 * grossWeight) / divisionvStallmax)

# Calculate V2 and VR based on stall speeds
v2_min = 1.2 * vStallmax  # 1.2 times the minimum stall speed
v2_max = 1.2 * vStallmin  # 1.2 times the maximum stall speed
vR_min = 1.07 * vStallmax # 1.05 times the minimum stall speed
vR_max = 1.07 * vStallmin  # 1.05 times the maximum stall speed

# Adjust for wind
if windDirection.lower() == "headwind":
    v1 -= windSpeed * 0.5  # Adjust V1 for headwind
    vR_min -= windSpeed * 0.5
    vR_max -= windSpeed * 0.5
    v2_min -= windSpeed * 0.5
    v2_max -= windSpeed * 0.5
elif windDirection.lower() == "tailwind":
    v1 += windSpeed * 0.5  # Adjust V1 for tailwind
    vR_min += windSpeed * 0.5
    vR_max += windSpeed * 0.5
    v2_min += windSpeed * 0.5
    v2_max += windSpeed * 0.5

# Output results
print(f"Performance Calculations for A320-{acType}:\n")
print(f"V1: {int(v1)} knots")
print(f"VR: {int(vR_min)} - {int(vR_max)} knots")
print(f"V2: {int(v2_min)} - {int(v2_max)} knots")
print(f"FLEX: {int(flex)}ºC")