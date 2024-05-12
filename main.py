# 导入必要库
import json
from datetime import datetime
from random import choice
from time import sleep
from webbrowser import open as openwp

# 逐字输出
old_print = print
def print(*args):
    for i in args:
        for j in i:
            old_print(j, flush=True, end="")
            sleep(0.05)
    old_print()

# 输出错误信息
def print_error(string):
    old_print(f"\033[1;30;41m[error] {string}\033[0m")

# 输出日志信息
def print_log(string):
    old_print(f"\033[1;30;46m[log] {string}\033[0m")

# 导入 openai 库
try:
    import openai
    print_log("导入 openai 库成功！")
except ImportError:
    print_error("导入 openai 库失败，请先安装 openai 库！")
    sleep(0.5)
    exit()

# 设置部分变量
knowledge_file = __file__ + r"\..\knowledge.json"
api_config_file = __file__ + r"\..\api_config.json"

# 读取配置文件
try:
    with open(api_config_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        chatgpt_first_time = data["chatgpt_first_time"]
        openai.api_key = data["api"]
        openai.api_base = data["proxy"]
        chatgpt_model = data["model"]
    print_log("导入配置文件成功！")
except Exception:
    print_error("导入配置文件失败！")

# 调用知识库函数
def find_answer(file_path, question):
    with open(file_path, encoding="utf-8") as f:
        ls = json.load(f)
        for data in ls:
            if data["question"].lower() in question:
                return data["answer"]
    return "我暂时还不知道呢，你可以在 GitHub 上为我贡献代码哦！"

# 响应函数
def answer(text):
    old_print("wbot：", end="")
    if "你好" in text:
        print(choice(["你好啊，主人！", "嗨，主人！"]))
    elif "你是谁" in text or "名字" in text:
        print("我是wbot，你的小助手")
    elif "你会" in text or "你可以" in text or "做" in text:
        print("我可以帮你查询时间、查询日期、搜索内容等等，具体可以查看我的源代码")
    elif "你知道" in text or "什么是" in text or "是什么" in text:
        print(find_answer(knowledge_file, text))
    elif "日期" in text or "几月几日" in text or "几月几号" in text:
        date = datetime.now().strftime(r"%Y年%m月%d日")
        weekday = datetime.now().weekday()
        ls = ["一", "二", "三", "四", "五", "六", "日"]
        print(f"今天是{date}，星期{ls[weekday]}")
    elif "时间" in text or "几点" in text:
        time = datetime.now().strftime(r"%H时%M分%S秒")
        print(f"现在是{time}")
    elif "github" in text and "搜索" in text:
        w = input("请输入你要在 GitHub 上搜索的内容：")
        openwp(f"https://github.com/search?q={w}")
    elif "搜索" in text:
        try:
            c = input("""1. 百度
      2. 必应
      请输入你要使用的搜索引擎：""")
            w = input("      请输入你要查询的内容：")
        except KeyboardInterrupt:
            print()
            old_print("[error] 检测到 KeyboardInterrupt，即将退出")
            s = choice(["下次再见！", "期待下次见面！"])
            print(f"wbot：{s}")
            sleep(0.5)
            exit()
        if c == "1":
            openwp(f"https://www.baidu.com/s?wd={w}")
        elif c == "2":
            openwp(f"https://cn.bing.com/search?q={w}")
        else:
            print("输入错误！")
            sleep(0.5)
    elif "谢谢" in text or "感谢" in text:
        print("不用谢，主人！")
    elif "音乐" in text:
        m = input("请输入你要搜索的音乐：")
        openwp(f"http://tool.liumingye.cn/music/#/search/B/song/{m}")
    elif "天气" in text:
        c = input("请输入你要查询的城市：")
        openwp(f"https://www.baidu.com/s?wd={c}天气")
    elif "翻译" in text:
        w = input("请输入你要翻译的英文：")
        openwp(f"https://fanyi.baidu.com/translate#en/zh/{w}")
    elif "chatgpt" in text:
        global chatgpt_first_time, chatgpt_model
        if chatgpt_first_time:
            cw = input("请输入您的 OpenAI 服务器地址（官方接口请留空）：")
            if (cw != ""):
                openai.api_base = cw
            openai.api_key = input("      请输入您的 ChatGPT API Key：")
            cm = input("      请输入您要使用的模型（默认为 gpt-3.5-turbo）：")
            if (cm != ""):
                chatgpt_model = cm
            else:
                chatgpt_model = "gpt-3.5-turbo"
            with open(api_config_file, "r+", encoding="utf-8") as f:
                data = json.load(f)
                data["api"] = openai.api_key
                data["proxy"] = openai.api_base
                data["chatgpt_first_time"] = False
                data["model"] = chatgpt_model
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=4)
                f.truncate()
            cq = input("      请输入您要和 ChatGPT 聊天的内容：")
        else:
            cq = input("请输入您要和 ChatGPT 聊天的内容：")
        print("      等待回答中……")
        try:
            completion = openai.ChatCompletion.create(
                model=chatgpt_model,
                messages=[
                    {"role": "user", "content": cq}
                ]
            )
            print(f"      ChatGPT：{completion["choices"][0]["message"]["content"]}") # type: ignore
        except Exception:
            old_print("      ")
            print_error("发送请求时发生错误！")
            sleep(0.5)
    elif "再见" in text or "拜拜" in text or "退出" in text:
        print(choice(["下次再见！", "期待下次见面！"]))
        sleep(0.5)
        exit()
    else:
        print("我暂时还不会呢，你可以在 GitHub 上为我贡献代码哦！")

# 主程序
print_log("进入主程序成功！")
old_print("   |=====欢迎使用 wbot 智能聊天机器人！=====|   ")
while True:
    try:
        text = input("你：").lower()
    except KeyboardInterrupt:
        print()
        print_error("检测到 KeyboardInterrupt，即将退出")
        s = choice(["下次再见！", "期待下次见面！"])
        print(f"wbot：{s}")
        sleep(0.5)
        exit()
    answer(text)
