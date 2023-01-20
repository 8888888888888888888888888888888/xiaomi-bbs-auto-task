import time, json, requests, json, hashlib, time, random
from requests_toolbelt.multipart.encoder import MultipartEncoder
import login


class Apply:

    def __init__(self) -> None:
        pass

    projectTypes = {
        10001: 1,  # 10001 开发版公测
        10002: 0,  # 10002 开发版内测
        10003: 2  # 10003 稳定版内测
    }
    planId: str or int
    WebCookie: dict
    device: str

    def Sign(self):
        url = "https://api-alpha.vip.miui.com/api/alpha/miui/sign"
        params = {
            "projectType":
            self.projectTypes[int(self.planId)],  # 开发版内测 0 , 开发版公测 1 , 稳定版内测 2
            "pathname": "/mio/systemTestApply",
            "version": "dev.20001",
            "miui_version": "undefined",
            "android_version": "undefined",
            "oaid": "false",
            "device": self.device,
            "restrict_imei": "",
            "miui_big_version": "",
            "model": "黄金版 Iphone 13 Pro Max",  # 假装B格拉满
            "androidVersion": "undefined",
            "miuiBigVersion": ""
        }
        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        }
        res = requests.get(url=url,
                           params=params,
                           headers=headers,
                           cookies=self.WebCookie)
        self.applyInfo = json.loads(res.text)["entity"]
        self.userId = self.applyInfo["userId"]

    def Signature(self):
        self.ts = int(time.time())
        msg = f"{self.userId}-{self.planId}-{self.ts}-f0e666e08a3c786a87f617fe0f37cfd0"
        md5 = hashlib.md5()
        md5.update(msg.encode())
        self.signature = md5.hexdigest()

    def RandomPhoneNum(self):
        return random.randint(10000000000, 20000000000)

    def get_matched(self):
        conditions = self.applyInfo["conditions"]
        matchedList = []
        matched = ""
        for condition in conditions:
            matchedList.append(condition["content"])

        for condition in conditions:
            index = int(condition["index"]) - 1
            content = condition["content"]
            matchedList[index] = content
        for msg in matchedList:
            matched += f"{msg}|"
        self.matched = matched[:-1]

    def getdata(self):
        fields = {
            "contact": (None, str(self.RandomPhoneNum())),
            "supplement": (None, ""),
            "isAcceptProtocol": (None, "true"),
            "device": (None, self.device),
            "planId": (None, str(self.applyInfo["devices"][0]["planId"])),
            "matched": (None, self.matched),
            "projectType": (None, str(self.projectTypes[int(self.planId)])),
            "ts": (None, str(self.ts)),
            "signature": (None, self.signature),
            "miui_vip_a_ph": (None, self.WebCookie["miui_vip_a_ph"]),
            "miui_vip_a_slh": (None, self.WebCookie["miui_vip_a_slh"]),
            "miui_vip_a_serviceToken":
            (None, self.WebCookie["miui_vip_a_serviceToken"])
        }
        data = MultipartEncoder(
            fields=fields, boundary="----WebKitFormBoundaryZkkMlfDoYxkRFhlC")
        return data

    def signup(self):
        url = "https://api-alpha.vip.miui.com/api/alpha/miui/signup"
        params = {
            "ref": "vipAccountShortcut",
            "pathname": "/mio/systemTestApply",
            "version": "dev.220326",
            "miui_version": "V13.0.3.0.SJSCNXM",
            "android_version": "12",
            "oaid": "",
            "device": self.device,
            "restrict_imei": "",
            "miui_big_version": "V130",
            "model": "黄金版 Iphone 13 Pro Max",
            "androidVersion": "12",
            "miuiBigVersion": "V130",
            "cUserId": self.WebCookie["cUserId"],
            "miui_vip_a_ph": self.WebCookie["miui_vip_a_ph"],
            "miui_vip_a_slh": self.WebCookie["miui_vip_a_slh"],
            "miui_vip_a_serviceToken":
            self.WebCookie["miui_vip_a_serviceToken"]
        }
        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
            "Cache-Control":
            "no-cache",
            "Accept":
            "application/json",
            "Content-Type":
            "multipart/form-data; boundary=----WebKitFormBoundaryZkkMlfDoYxkRFhlC"
        }
        data = self.getdata()
        res = requests.post(url=url,
                            params=params,
                            headers=headers,
                            data=data,
                            cookies=self.WebCookie)
        message = json.loads(res.text)["message"]
        taskname = {"10001": "开发版公测", "10002": "开发版内测", "10003": "稳定版内测"}
        print(
            f'申请 {taskname[str(self.planId)]} {self.applyInfo["devices"][0]["name"]}: {message}'
        )

    def run(self):
        self.Sign()
        self.Signature()
        self.get_matched()
        self.signup()


def main():

    input("是否已在accounts.json填入账号和申请机型, 回车确认...")
    planIds = ["10001", "10002", "10003"]
    with open("data/accounts.json", "r", encoding="utf-8") as r:
        accounts = json.load(r)
    for Account in accounts:
        account = Account["account"]
        password = Account["password"]
        try:
            WebCookie = login.Web(account=account, password=password)
            print(f"\n{account}登录成功!")
        except:
            print(f"\n{account}登录失败...")
            continue
        Devices = Account["devices"]
        for planId in planIds:
            devices = Devices[planId]
            if devices == []: continue
            a = Apply()
            a.WebCookie = WebCookie
            a.planId = planId
            for device in devices:
                a.device = device
                try:
                    a.run()
                except:
                    print(f"未知原因导致{device}申请失败...")


def available():
    with open("data/accounts.json", "r", encoding="utf-8") as r:
        accounts = json.load(r)
    Account = accounts[0]
    account = Account["account"]
    password = Account["password"]
    taskname = {"10001": "开发版公测", "10002": "开发版内测", "10003": "稳定版内测"}
    planIds = ["10001", "10002", "10003"]
    try:
        with open("data/available.json", "r", encoding="utf-8") as r:
            Devices = json.load(r)
        Devices["10001"]
    except:
        Devices = {"10001": [], "10002": [], "10003": []}

    try:
        WebCookie = login.Web(account=account, password=password)
    except:
        print("登录失败,无法检测可用设备,有以下解决方法...")
        print("1.在data/accounts.json的第一栏填入账号密码")
        print("2.在浏览器登录小米社区,通过验证码校验")
        exit()
    with open("data/devices.json", "r", encoding="utf-8") as r:
        devices = json.load(r)
    for planId in planIds:
        tt = 0
        try:
            startcode = Devices[planId][-1]
        except:
            startcode = "代号名称"
        print()
        for device in devices:
            if startcode == device["code"]: tt += 1
            if tt == 0: continue
            a = Apply()
            a.WebCookie = WebCookie
            a.device = device["code"]
            if device["code"] in Devices[planId]: continue
            a.planId = planId
            a.Sign()
            applyInfo = a.applyInfo
            time.sleep(1)
            if applyInfo["devices"] != []:
                Devices[planId].append(device["code"])
                print(f'{taskname[planId]} {device["name"]} 可用!')
                with open("data/available.json", "w", encoding="utf-8") as w:
                    json.dump(Devices, fp=w, ensure_ascii=False, indent=2)
                continue
            print(f'{taskname[planId]} {device["name"]} 不可用!')


def ChoiceDevice():
    with open("data/devices.json", "r", encoding="utf-8") as r:
        devices = json.load(r)
    with open("data/available.json", "r", encoding="utf-8") as r:
        Devices = json.load(r)
    taskname = {"10001": "开发版公测", "10002": "开发版内测", "10003": "稳定版内测"}
    planIds = ["10001", "10002", "10003"]
    print("\n选择需要申请的内测...")
    for planId in planIds:
        print(f"{planIds.index(planId)}.{taskname[planId]}")
    planIdindex = str(input("请输入选项索引:"))
    print("\n寻找可用设备...")
    uplanId = planIds[int(planIdindex)]
    usableDevices: list = Devices[uplanId]
    t = 0
    print("\n以下是可用设备:")
    for usableDevice in usableDevices:
        column = 0
        DeviceName: str
        for deviceInfo in devices:
            if usableDevice == deviceInfo["code"]:
                DeviceName = deviceInfo["name"]
                if t < column:
                    print(f"{usableDevices.index(usableDevice)}.{DeviceName}",
                          end="\t\t")
                    t += 1
                else:
                    t = 0
                    print()
                    print(f"{usableDevices.index(usableDevice)}.{DeviceName}",
                          end="\t\t")

    print("\n多选请用空格分隔...")
    choicedeviceindexes = str(input("请输入选项索引:"))
    choicedeviceindexes = choicedeviceindexes.split()
    ChoiceDevices = []
    for choicedeviceindex in choicedeviceindexes:
        choicedeviceindex = int(choicedeviceindex)
        ChoiceDevices.append(usableDevices[choicedeviceindex])
    print("将以下内容复制到data/accounts.json的devices处即可...", end="\n\n")
    print(f'"{uplanId}":{json.dumps(ChoiceDevices)}')


def single():
    while True:

        account = input("请输入账号:")
        password = input("请输入密码:")
        try:
            WebCookie = login.Web(account=account, password=password)
            print(f"\n{account}登录成功!")
            break
        except:
            print(f"\n{account}登录失败...")
            print("登录失败, 请重新登录! ")

    def p():
        with open("data/devices.json", "r", encoding="utf-8") as r:
            devices = json.load(r)
        with open("data/available.json", "r", encoding="utf-8") as r:
            Devices = json.load(r)
        taskname = {"10001": "开发版公测", "10002": "开发版内测", "10003": "稳定版内测"}
        planIds = ["10001", "10002", "10003"]

        print("\n选择需要申请的内测...")
        for planId in planIds:
            print(f"{planIds.index(planId)}.{taskname[planId]}")
        planIdindex = str(input("请输入选项索引:"))
        print("\n寻找可用设备...")
        uplanId = planIds[int(planIdindex)]
        usableDevices: list = Devices[uplanId]
        t = 0

        print("\n以下是可用设备:")
        for usableDevice in usableDevices:
            column = 0
            DeviceName: str
            for deviceInfo in devices:
                if usableDevice == deviceInfo["code"]:
                    DeviceName = deviceInfo["name"]
                    if t < column:
                        print(
                            f"{usableDevices.index(usableDevice)}.{DeviceName}",
                            end="\t\t")
                        t += 1
                    else:
                        t = 0
                        print()
                        print(
                            f"{usableDevices.index(usableDevice)}.{DeviceName}",
                            end="\t\t")

        print("\n多选请用空格分隔...")
        choicedeviceindexes = str(input("请输入选项索引:"))
        choicedeviceindexes = choicedeviceindexes.split()
        ChoiceDevices = []
        for choicedeviceindex in choicedeviceindexes:
            choicedeviceindex = int(choicedeviceindex)
            ChoiceDevices.append(usableDevices[choicedeviceindex])
        a = Apply()
        a.WebCookie = WebCookie
        a.planId = planId
        print("开始申请...")
        for device in ChoiceDevices:
            a.device = device
            try:
                a.run()
            except:
                print(f"未知原因导致{device}申请失败...")

    while True:
        p()
        input("\n返回 选择内测类型...")


def run():

    tasks = {
        "单账号申请": single,
        "批量申请": main,
        "检测可申请设备": available,
        "选择申请设备": ChoiceDevice,
        "退出": exit
    }
    print("选择你的操作...\n")
    tasklist = list(tasks.keys())
    for taskname in tasklist:
        print(f'{tasklist.index(taskname)}.{taskname}')
    index = input("\n请输入选项索引:")
    tasks[tasklist[int(index)]]()


if __name__ == '__main__': run()
