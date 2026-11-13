import json   
import re

LABELS = ("urgent", "normal", "ignore")

SYSTEM_PROMPT = """This is a task to classify the priority of an email. You will be given an email in the following format:
From: {from}To: {to}
Date: {date}Subject: {subject}{body}
You should classify the email into one of the following categories: {"urgent", "normal", "ignore"}.
Please provide your answer in the following JSON format:
{
    "category": "<one of the labels>",
    "reason": "<your reasoning for the classification>"
}
Make sure to only return valid JSON, and nothing else.
"""


def format_email(email: dict) -> str:
    # TODO: 把邮件拼成一段给模型看的文本，返回一个 str。
    # 可用的键：email["from"], email["to"]（是个 list）, email["date"], email["subject"], email["body"]
    # 提示：f-string 和 ", ".join(某个list) 就够用了
    str=""
    str+=f"From: {email['from']}\n"
    str+=f"To:{', '.join(email['to'])}\n"
    str+=f"Date: {email['date']}\n"
    str+=f"Subject: {email['subject']}\n"
    str+=f"{email['body']}\n"
    return str

def make_resson(reply:str,data=None)->str:
    #data不是None,并且data里reason去掉空格后不为空,就返回data里的reason,否则返回reply
    #reply去掉空格后不为空,就返回reply.strip()
    #返回“model returned an empty reply”
    if data is not None and data.get("reason", "").strip():
        return data.get("reason", reply)
    if reply.strip():
        return reply.strip()
    return "model returned an empty reply"

def parse_reply(reply: str) -> dict:
    #第一步：读 JSON 的 "category"     ← 正路：模型听话时，99% 在这里就结束了
    #第二步：整段找标签词               ← 兜底 1：模型没按格式写，但答案还在字里行间
    #第三步：返回 unknown              ← 兜底 2：真的读不出来，老实说不知道，不瞎猜
    start = reply.find("{")
    end = reply.rfind("}")
    if start != -1 and end != -1:
        try:
            data = json.loads(reply[start : end + 1])
            category = str(data.get("category", "")).lower()
            if category in LABELS:
                reply=make_resson(reply,data)
                return {"category": category, "reason": reply}
        except Exception:
            pass
    found = re.findall(r"\b(urgent|normal|ignore)\b", reply.lower())
    if len(set(found)) == 1:
        reply=make_resson(reply,None)
        return {"category": found[0], "reason": reply}
    reply=make_resson(reply,None)
    return {"category": "unknown", "reason": reply}




def classify_priority(email: dict, lm) -> dict:
    # TODO 1: 组装 messages：一个 list，里面放两个 dict
    #         {"role": "system", "content": ...} 和 {"role": "user", "content": ...}
    # TODO 2: reply = lm(messages)
    # TODO 3: 先不解析，直接 return {"category": "unknown", "reason": reply}
    messages=[]
    messages.append({"role": "system", "content": SYSTEM_PROMPT})
    messages.append({"role": "user", "content": format_email(email)})
    reply=lm(messages)
    return parse_reply(reply)
