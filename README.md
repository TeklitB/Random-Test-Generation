## RTG Prototype
RTG: Random-Test-Generation
This is a prototype of random test generation framework for Android apps. The prototype generates test cases for Android GUI-based testing using random fuzzing approach. The prototype uses a third party tool called [ ACVTool](https://github.com/pilgun/acvtool) to measure code coverage.
## Installation
### Environment Configration
* Python: 2.7
* Java version 1.8
* Android SDK: API 28
* Linux OS

Install Python dependencies:

    sudo pip install -r requirements.txt

Install ACVTool: To install ACVTool follow instructions given in the following link.
    [ ACVTool](https://github.com/pilgun/acvtool)

## Usage
### Settings
Before starting STGFA-SMOG the following parameters in settings.py should be set.
* FITNESS_FUNCS
* ACVTOOL\_WDIR 
* ACVTOOL\_CMDDIR

### Start STGFA-SMOG
    python main.py <apk_path>

### Limitations
This prototype performs best if:
* The Android app does not require the user to login.

## Output
Output content:

    /batt_usage - Battery usage logs of each test case.
    /cpu_usage_stats - CPU usage logs of each test case.
    /crash_logs - Crash logs and their corresponding test cases that lead to the crashes.
    /fitness_values - Fitness values of the fitness functions for the test cases.
    /mem_usage_stats - Memory usage logs of each test case.
    /net_usage - Network usage logs of each test case.
    /test-scripts - Generated test cases.

## Notes
* FITNESS_FUNCS - This is the parameter where the combination of fitness functions to be used are configured, i.e. [crash, length, cpu|memory|network|battery|line|method|class]
* ACVTOOL\_WDIR - Set the directory where the instrumented APK will be saved when any of the code coverage fitness functions are selected.
* ACVTOOL\_CMDDIR - Specify the directory where the instrumented APK is found. This parameter is used in the ACVTool commands.
