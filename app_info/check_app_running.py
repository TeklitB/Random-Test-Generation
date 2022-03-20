import subprocess as sub
import sys, time

def app_crashed(packagename):
    pro_pid = sub.Popen("adb shell pidof {0}".format(packagename), 
        stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
    out_pid, err_pid = pro_pid.communicate()
    
    # Restart app if it does not have process id (PID)
    if out_pid == "":
        # Restart app
        proc_start = sub.Popen('adb shell monkey -p '+ packagename +' -c android.intent.category.LAUNCHER 1',
        stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
        stdoutdata_start, stderrdata_start = proc_start.communicate()
        time.sleep(5)

def check_app_is_running(package_name):
    process = sub.Popen("adb shell pidof {0}".format(package_name), 
    stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
    app_run_out, app_run_err = process.communicate()

    if app_run_out.decode() == "":
        return False
    else:
        return True

if __name__ == "__main__":
    pkg_name = sys.argv[1]
    print(check_app_is_running(pkg_name))