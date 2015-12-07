import atexit
import subprocess

from colorama import Style, Fore

def compile(src_path, dest_path):
    subprocess.check_call(' '.join([
        'sass',
        '%s:%s' % (src_path, dest_path)
    ]), shell=True)

def start_watch(src_path, dest_path):
    print Style.BRIGHT + "Starting SASS." + Style.RESET_ALL

    try:
        process = subprocess.Popen(' '.join([
            'sass',
            '--watch',
            '%s:%s' % (src_path, dest_path)
        ]), shell=True)
        atexit.register(process.kill)
    except OSError, e:
        print Style.BRIGHT + Fore.RED
        print "SASS failure: %s" % e
        print "SASS files will not be built."
        print Style.RESET_ALL
