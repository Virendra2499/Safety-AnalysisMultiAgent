safety_requirements = [
"The system shall initiate an emergency stop if an obstacle is detected within 0.5 meters.",
"The robot must shut down if its core temperature exceeds 85°C.",
"All motor drives must cease operation if a fault signal is received from the safety PLC.",
"If the pressure sensor reads above 120 PSI, the valve must be closed within 2 seconds.",
"The system shall log all safety-critical events within 100 ms of occurrence.",
]

system_descriptions = [
"The obstacle detection system uses ultrasonic sensors but only raises a warning. No emergency stop is implemented.",
"Core temperature is monitored every 10 seconds. If it exceeds 85°C, the robot sends an alert to the dashboard.",
"Motor drivers are connected to a safety PLC. When a fault is received, the system issues a stop command immediately.",
"Pressure sensors can detect values above 120 PSI, but the valve closing logic is handled manually by an operator.",
"The system logs safety events, but due to storage limitations, entries are written with a 5-second delay.",
]