import json   
import re

LABELS = ("urgent", "normal", "ignore")

SYSTEM_PROMPT = """This is a task to classify the priority of an email for its recipient.
Classify it as exactly one of: urgent, normal, ignore.

Judge every email from the point of view of the person it is addressed to
(the `to` field), at the time it was sent. The question is what that person
should do with the message, not how important the topic is to the company.

## urgent

The recipient has to act or decide soon. Two things must both be true:

1. The email asks the recipient to do something, or reports a live problem
   that the recipient is responsible for (an outage, a failed payment, a
   customer or manager escalating an issue).
2. There is time pressure: the email states or clearly implies that the
   action is needed the same day, the next working day, or by a stated
   deadline no more than two working days away.
   A working day is Monday to Friday, counted from the email's date.

Examples:

- "The bank rejected this morning's wire. I need you to approve the
  corrected one by 1:00 PM or we pay a late penalty."
- "The customer's CFO is threatening to cancel. Can you call him before
  4:00 today?"

## normal

Legitimate work or personal mail that was written for this recipient or for
a small working group, with no deadline in the next two working days. This
covers status updates and FYIs, ordinary questions, documents sent for
review without a near deadline, meeting scheduling for later dates, replies
in an ongoing discussion, and personal notes from friends or family.

Examples:

- "Attached is the draft term sheet. Let me know if you have comments
  before our meeting the week after next."
- "Thanks for lunch yesterday. Are you still coming to the lake in
  August?"

## ignore

Mail the recipient can leave unread at no cost: advertising and spam from
vendors, newsletters and news digests, announcements sent to large employee
lists (events, training offerings, facilities notices), and automated
notifications that do not require the recipient to do anything.

Examples:

- "This week only: 40% off all standing desks. Reply REMOVE to
  unsubscribe."
- "To all employees: the annual bake sale is in the lobby on Friday from
  11:00 to 1:00."

## Deciding between two labels

- The wording does not decide the label. An email with "URGENT" in the
  subject that asks nothing of the recipient is not `urgent`. A calm email
  that says "I need your signature by 3:00 PM today" is `urgent`.
- A request with a deadline more than two working days away, or with no
  deadline, is `normal`.
- Mass mailings and advertising are `ignore` even when they use words such
  as "act now" or "important", because nothing is asked of this recipient in
  particular.
- An automated notice that asks this specific recipient to act (for
  example, an expense report waiting for their approval) is `normal`, or
  `urgent` if it states a deadline within two working days.
- A short personal or social message from someone the recipient knows is
  `normal`, not `ignore`.
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
    text=""
    text+=f"From: {email['from']}\n"
    text+=f"To:{', '.join(email['to'])}\n"
    text+=f"Date: {email['date']}\n"
    text+=f"Subject: {email['subject']}\n"
    text+=f"{email['body']}\n"
    return text

def make_reason(reply:str,data=None)->str:
    #data不是None,并且data里reason去掉空格后不为空,就返回data里的reason,否则返回reply
    #reply去掉空格后不为空,就返回reply.strip()
    #返回“model returned an empty reply”
    if data is not None:
        reason = data.get("reason")
        if isinstance(reason, str) and reason.strip():
            return reason.strip()
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
                reason=make_reason(reply,data)
                return {"category": category, "reason": reason}
        except Exception:
            pass
    found = re.findall(r"\b(urgent|normal|ignore)\b", reply.lower())
    if len(set(found)) == 1:
        reason=make_reason(reply,None)
        return {"category": found[0], "reason": reason}
    reason=make_reason(reply,None)
    return {"category": "unknown", "reason": reason}




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
