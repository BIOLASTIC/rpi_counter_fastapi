# Safety Instructions

**WARNING:** This system controls physical, high-power equipment. Failure to follow safety procedures can result in equipment damage or serious injury.

---

### 1. Electrical Safety

-   **ALWAYS** completely power down the Raspberry Pi, the Modbus IO modules, and the main power supply (e.g., 12V/24V) before connecting, disconnecting, or modifying any wiring.
-   Ensure all high-voltage connections to relays are properly insulated and secured.
-   Keep the control box and wiring dry and free of debris.
-   Do not operate the system if any wires appear frayed or damaged.

### 2. Mechanical Safety

-   **Pinch Points:** The conveyor belt, gears, and gate/diverter mechanisms are pinch points. Keep hands, clothing, and hair clear of all moving parts while the system is in operation.
-   **Conveyor Operation:** Be aware that the conveyor can be started remotely via the web interface. Do not place tools or foreign objects on the belt.
-   **Jam Clearing:** If the conveyor jams, press the **Stop Run** button in the web UI *before* attempting to clear the obstruction.

### 3. Emergency Procedures

-   The **"Stop Run"** button on the Dashboard is the primary software method for stopping the system under normal conditions.
-   An **Emergency Stop** API endpoint exists for immediate hardware shutdown. This requires a secret API key and should be integrated into a physical emergency stop button by your system integrator.
-   In case of a software failure, be prepared to physically disconnect power to the main conveyor motor.

### 4. General System Operation

-   Do not block the proximity sensors during a run, as this will cause incorrect counts or trigger size mismatch alarms.
-   Ensure the camera lens is clean and the area is well-lit for reliable operation.
-   Report any unusual noises, alarms, or system behavior to a supervisor immediately.