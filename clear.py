import os, shutil

def remove(path, excludes=[]):
    try:
        for f in os.listdir(path):
            if f not in excludes:
                try:
                    os.remove(os.path.join(path, f))
                except PermissionError:
                    shutil.rmtree(os.path.join(path, f))
    except FileNotFoundError:
        pass


encoding_dir = r"build\exe.win32-3.4\tcl\encoding"
encoding_excludes = ['ascii.enc', 'cp1254.enc', 'iso8859-9.enc', 'macTurkish.enc']

msg_dir = r"build\exe.win32-3.4\tcl\msgs"
msg_excludes = ['tr.msg']

tzdata_dir = r"build\exe.win32-3.4\tcl\tzdata"
tzdata_excludes = ['Turkey', r'Europe'] 

europe_dir = os.path.join(tzdata_dir, 'Europe')
europe_dir_excludes = ['Istanbul']

demos_dir = r"build\exe.win32-3.4\tk\demos"
images_dir = r"build\exe.win32-3.4\tk\images"
msgs_dir = r"build\exe.win32-3.4\tk\msgs"

remove(encoding_dir, encoding_excludes)
remove(msg_dir, msg_excludes)
remove(tzdata_dir, tzdata_excludes)
remove(europe_dir, europe_dir_excludes)
remove(demos_dir)
remove(images_dir)
remove(msgs_dir)

try:
    os.rename('build', 'siparis')
    os.rename(r'siparis\exe.win32-3.4', r'siparis\data')
except FileNotFoundError:
    pass