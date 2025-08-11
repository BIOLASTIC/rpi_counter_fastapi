# Operator Manual

This guide explains how to operate the Box Counter System from the web interface.

---

### 1. Dashboard Page

The Dashboard is the main control center for the application.

![Dashboard](https://i.imgur.com/example.png)  <!-- You can add screenshots here later -->

#### Production Control
-   **Object Profile (Recipe):** This is the most important setting. You must select a "recipe" that matches the product you are running on the conveyor. This tells the system how to configure the camera and other settings.
-   **Target Count:** Enter the number of items you want to count in a single batch. If you set this to `0`, the system will run continuously until you press "Stop".
-   **Post-Run Pause (s):** The number of seconds the system will pause *after* a batch is completed before automatically starting the next one.
-   **Load & Start Run:** After selecting a profile and setting a target, click this button. You will be asked to enter your **Operator Name** and a **Batch Code**. After confirming, the conveyor will start.
-   **Stop Run:** This stops the conveyor and ends the current production run immediately. The current batch is marked as "Aborted by User".
-   **Full Reset:** This is a soft reset that stops all hardware and clears the application's current state.

#### Live Process View
-   **ON BELT:** Shows the number of items currently detected between the entry and exit sensors.
-   **PROCESSED:** Shows the count for the *current* batch. This resets to zero for each new loop.
-   **MODE:** Shows the current system state (e.g., `Running`, `Paused`, `Stopped`).

#### Run Status
This circular progress bar shows how close the current batch is to reaching its target count. It also displays the name of the currently active recipe.

#### System Control Panel
These are manual override toggles. **Use with caution during a live run.** They allow you to manually turn hardware components on or off for testing or clearing jams.

---

### 2. Management Pages

The "Management" dropdown contains pages for configuring the system's "recipes".

-   **Object Profiles (Recipes):** This is where you create the master recipes. A recipe links a **Product** (what you're making) to a **Camera Profile** (how the camera should be set up).
-   **Product Master:** This is the master list of all products your facility produces. Here you can define product names, versions, and validation rules (like the minimum/maximum time a sensor should be blocked).
-   **Operator Master:** A simple list of all approved operators. You must add operators here before they can be selected when starting a run.

---

### 3. Run History Page

This page provides a complete log of all past production runs.

-   You can filter the list by date, product, or operator.
-   Clicking the **"View Images"** button for any run will open a pop-up showing all the photos that were taken during that specific run.
-   From the pop-up, you can download all images for that run as a single `.zip` file.