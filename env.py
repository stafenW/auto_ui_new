# 图片最低对比度，低于这个值报错
LOWEST_SIMILARITY = 96
# case报错重试几次
RETRY = 3
# team的alert bot通知接口的key
ALERT_BOT_CODE = 're_01f56c58e0e9414c84c741ce29e652ca'
# case的tag
ALL_TAGS = ['execute on launch', 'execute on everyday', 'about lead', 'about transaction']
# case code包含如下行的时候会展示出来
CODE_INDEX = ['import', 'chrome_options', 'driver', '.click', 'send_keys', 'time.sleep', 'WebDriverWait']
# linux服务器上该服务的url
BASE_URL_TEST = 'http://192.168.20.34:8086'
# 键盘操作的按键
ALL_BUTTON = ['ENTER', 'TAB', 'ESCAPE', 'SPACE', 'DELETE', 'BACKSPACE']
# MACOS在如下服务器上跑
# MACOS_URL = 'http://192.168.19.93:8086' # wilbur的mac
MACOS_URL = 'http://192.168.19.11:8086' # 旁边桌子上的mac
# 通知给alert时的链接
PLATFORM_URL = 'https://autoui.w.chime.me/#/case'
# 多线程执行chrome，同时几个线程
CHROME_THREADING = 5
