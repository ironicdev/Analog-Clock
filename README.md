# Analog Clock Application

## Overview
This Python project implements an Analog Clock GUI application using Tkinter. The application allows users to view and interact with a clock that displays current time based on selected timezones. Additionally, it includes features for setting alarms, running timers, and changing visual themes.

## Modules Used
- **Tkinter**: Python's standard GUI toolkit for creating the application interface.
- **datetime**: Provides classes for manipulating dates and times.
- **calendar**: Useful for accessing calendar-related functionalities.
- **pytz**: Python timezone library to handle timezones effectively.
- **sounddevice**: Library for playing audio.
- **soundfile**: Library for reading and writing sound files.
- **math**: Standard mathematical functions.

## Features
- **Analog Clock Display**: Shows current time with hour, minute, and second hands.
- **Theme Selection**: Offers various visual themes for customizing the clock's appearance.
- **Timezone Selection**: Allows users to choose from a list of predefined timezones.
- **Timer**: Enables users to set and start a countdown timer.
- **Alarm**: Lets users set alarms and plays a sound when the alarm time is reached.
- **Clear Button**: Clears any active timers or alarms.
- **Real-time Updates**: The clock updates every second to reflect the current time and date.

## Files Included
1. **main.py**: Python script containing the main application code.

## Usage Instructions
1. **Dependencies Installation**:
   - Ensure Python is installed on your system.
   - Install required libraries using pip:
     ```
     pip install sounddevice soundfile pytz
     ```

2. **Running the Application**:
   - Open a terminal or command prompt.
   - Navigate to the directory containing `main.py`.
   - Run the application:
     ```
     python main.py
     ```

3. **Using the Application**:
   - Upon running the application, the analog clock interface will appear.
   - Select a theme and timezone using the dropdown menus.
   - Set alarms by specifying the hour, minute, and meridian (AM/PM).
   - Start a timer by entering hours, minutes, and seconds and clicking "Start".
   - Clear any active timers or alarms using the "Clear" button.

4. **Customization**:
   - Modify the list of timezones (`options`) and themes (`themes`) directly in the code to suit your preferences.

5. **Sound Files**:
   - Ensure sound files (`timer.wav` and `alarm.mp3`) are placed in the `assets` directory relative to `main.py` for audio functionality.

## Notes
- This application is designed to provide a user-friendly interface for viewing time across different timezones, setting alarms, and running timers.
- For any inquiries or issues, please contact Dev at devverma269@gmail.com.

