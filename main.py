import subprocess, os
import time, shutil, sys
from datetime import datetime

import retrieve_package_name
from devices import emulator
import settings
from input_events import key_event, get_events
from input_events import text_event
from input_events import tap_swap_event
from input_events import action_commands
from input_events import test_seq_generator
from runtests import runtestcases, adbcommands
from resetAUT import reset_app_state


def setup_test_cases(individual, package_name, index_indv, gen, app_name):
    
    script_filename = "test-scripts/atomicevent.evo.script."+str(gen)+str(index_indv)+".txt"
    #if not os.path.exists(script_filename):
        #os.makedirs(script_filename)

    script = open(script_filename, "w+")
    for line in individual: 
        script.write("input "+line + "\n")
    script.close()

    # rund suite on device
    fitness_values = reset_app_state.setup_aut(individual, package_name, index_indv, gen, app_name)
    func_values_path = "fitness_values/fun_values_"+str(gen)+".txt"
    check_path = os.path.exists(func_values_path)
    open_fvalues = open(func_values_path, "a" if check_path else "w+")

    for indx, value in enumerate(fitness_values):
        if indx == len(fitness_values)-1:
            open_fvalues.write(str(value))
        else:
            open_fvalues.write(str(value)+"\t")
    open_fvalues.write("\n")

    return fitness_values


def main(app_path):
    
    startTime = datetime.now()
    current_time = startTime.strftime("%H:%M:%S")
    print("Start time: {0}".format(current_time))

    if not os.path.exists(app_path):
        print("The app does not exist!\n")
        sys.exit()

    # Extract app file name
    app_name = app_path.split("/")[-1].split(".")[0]

    # Get package name of the app app-debug.apk Amazon_App.apk
    byte_package_name, app_dir = retrieve_package_name.get_package_name(app_path)
    package_name = byte_package_name.decode('utf-8')
    print("Package name: ", package_name)

    # Boot the emulator first
    emulator.boot_devices()

    print("Emulator booting completed.")

    # Uninstall the AUT if it already exists
    adbcommands.uninstall_app(package_name)

    # If code coverage measure is needed, Instrument the app with ACVTool
    if "line" in settings.FITNESS_FUNCS or "method" in settings.FITNESS_FUNCS or "class" in settings.FITNESS_FUNCS:
        # Delete acvtool working directory if it exists
        if os.path.exists(settings.ACVTOOL_WDIR):
            shutil.rmtree(settings.ACVTOOL_WDIR, ignore_errors=False, onerror=None)
        
        # Instrument the app
        print("Instrumenting ...")
        inst_proc = subprocess.Popen("acv instrument {0}".format(app_path), 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        inst_apk_output, inst_apk_err = inst_proc.communicate()

        # Install the instrumented apk
        instal_proc = subprocess.Popen("acv install {0}".format(settings.ACVTOOL_CMDDIR+"instr_"+app_name+".apk"), 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        instal_apk_output, instal_apk_err = instal_proc.communicate()
        #print("Installation Error =>", instal_apk_err)   

    # Otherwise, simply install the original app
    else:
        # Install the app
        adbcommands.install_app(app_path)
        time.sleep(1)

    #open app
    #adb_shell_cmd('monkey -p '+ package_name +' -c android.intent.category.LAUNCHER 1')
    #time.sleep(30)
    for i in range(1, settings.POPULATION_SIZE+1):
        test_case = test_seq_generator.gen_test_seq()
        setup_test_cases(test_case, package_name, i, settings.NGENERATION, app_name)

    endTime = datetime.now()
    current_end_time = endTime.strftime("%H:%M:%S")
    print("End time: {0}".format(current_end_time))

if __name__=="__main__":
    apk_path = sys.argv[1]
    main(apk_path)

