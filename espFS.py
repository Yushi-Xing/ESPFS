import  time,os
import subprocess
def run_cmd_Popen_fileno(cmd_string):
    """
    执行cmd命令，并得到执行后的返回值，python调试界面输出返回值
    :param cmd_string: cmd命令，如：'adb devices'
    :return:
    """
    #import subprocess
    
    print('运行cmd指令：{}'.format(cmd_string))
    return subprocess.Popen(cmd_string, shell=True, stdout=None, stderr=None).wait()
def get_file_list(file_path):
    file_list = os.listdir(file_path) # 得到文件夹下的所有文件名称，存在字符串列表中
    file_list.sort()
    if file_path[-1]=='/'or file_path[-1]=='\\':
        pass
    else:
        file_path+='/'
    fpath=[]
    for i in file_list :
        fpath.append(file_path+i)
    return (fpath,file_list) # 得到文件夹下的所有文件路径和文件名称

##
_,fl=get_file_list('./')
for fn in fl:
    if len(fn)>4 :
        if fn[-4:-1]+fn[-1]=='.bin':
            run_cmd_Popen_fileno(f'move {fn} ./history_bin/{fn}')
##
timestamp=time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
binname='SPIFFS_'+timestamp+'.bin'

##example FS:3MB OTA:~512KB
"""
generic.menu.eesz.4M3M=4MB (FS:3MB OTA:~512KB)
generic.menu.eesz.4M3M.build.flash_size=4M
generic.menu.eesz.4M3M.build.flash_ld=eagle.flash.4m3m.ld
generic.menu.eesz.4M3M.build.spiffs_pagesize=256
generic.menu.eesz.4M3M.build.rfcal_addr=0x3FC000
generic.menu.eesz.4M3M.build.spiffs_start=0x100000
generic.menu.eesz.4M3M.build.spiffs_end=0x3FA000
generic.menu.eesz.4M3M.build.spiffs_blocksize=8192
"""
#mkspiffs

spi_size=0x3FA000-0x100000          #FS:3MB(-24K)----spiffs_end-spiffs_start=3048*1024
page=256                            #spiffs_pagesize=256
block=8192                          #spiffs_blocksize=8192

#
port='com5'
baud=460800
FS_Start_Address=0x100000           #spiffs_start=0x100000
chip='esp8266'
##
print(run_cmd_Popen_fileno(f"mkspiffs.exe -c ./data -p {page} -b {block} -s {spi_size} {binname}"))
print(run_cmd_Popen_fileno(f"mkspiffs.exe -l {binname}"))
##
print(run_cmd_Popen_fileno(f'esptool.exe --port {port} --chip {chip} --before default_reset --after hard_reset --baud {baud} write_flash -z {FS_Start_Address} {binname}'))



