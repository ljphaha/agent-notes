from concurrent.futures import ThreadPoolExecutor
from cs329z_hw1.pipelines.priority import classify_priority

#给状态按紧急情况排序,unknown和normal同级
Rank = {"urgent": 0, "normal": 1, "unknown": 1, "ignore": 2}

#并发调用classify_priority,返回一个list,每个元素是一个dict,包含category和reason
def label_emails(emails: list, lm) -> list:
    with ThreadPoolExecutor(max_workers=16) as executor:
        results = list(executor.map(lambda email: classify_priority(email, lm), emails))
    return results

#去掉ignore的邮件,并且同一thread_id的邮件只保留一个,保留紧急程度最高的那封,如果有多封紧急程度相同的,就保留最早的那封
def filter_emails(emails: list, labels: list) -> list:
    filtered_emails = []
    seen_thread_ids = set()
    for email, label in sorted(zip(emails, labels), key=lambda x: (Rank[x[1]["category"]], x[0].get("date", ""))):
        if label["category"] == "ignore":
            continue
        thread_id = email.get("thread_id")
        if thread_id not in seen_thread_ids:
            filtered_emails.append((email, label))
            seen_thread_ids.add(thread_id)
    return filtered_emails

#拼接材料
def build_material(items: list) -> str:
    material=""
    #保留名字、状态、日期、主题（ignore忽略）、正文（只保留前500个字符）
    for item in items:
        material += f"Name: {item[0].get('from', 'N/A')}\n"
        material += f"Status: {item[1].get('category', 'N/A')}\n"
        material += f"Date: {item[0].get('date', 'N/A')}\n"
        material += f"Subject: {item[0].get('subject', 'N/A')}\n"
        material += f"Body: {item[0].get('body', 'N/A')[:500]}\n\n"
    return material

DIGEST_PROMPT = """
The task is to read a list of emails and summarize them into a digest.
The digest should be a concise summary of the emails, highlighting the most urgent and important information. The summary should be clear, informative, and easy to read.
The digest should include the following information for urgent email:
- Name of the sender
- Details of the email, including the name of the company or person, the specific address, and the specific request or issue mentioned in the email.
Each urgent email should be summarized in one sentence, focusing on the most important information.
Other emails should be summarized in a more general way, no more than three sentences totally, focusing on the titles.
The forbidden things in the digest are:
- Do not include any personal opinions or biases in the summary.
- Do not include any irrelevant information or details that are not directly related to the emails.
The digest should be written in a professional and neutral tone, avoiding any personal opinions or biases. The maximum length of the digest should be 250 words. If there are no emails to summarize, the digest should state that there are no emails to summarize.
"""

#调用以上函数,返回一个dict,包含material和labels
def digest_emails(emails: list, lm) -> str:
    # ① 空的一天 → 直接 return 一句话，不调用模型
    # ② labels = label_emails(...)；items = filter_emails(...)
    # ③ 全被过滤掉了（items 是空的）→ 也直接 return 一句话
    # ④ material = build_material(items)
    # ⑤ messages = [system: DIGEST_PROMPT, user: material]；reply = lm(messages)
    # ⑥ return reply
    if not emails:
        return "No emails to digest."
    labels = label_emails(emails, lm)
    items = filter_emails(emails, labels)           
    if not items:
        return "No relevant emails to digest."
    material = build_material(items)
    messages = [{"role": "system", "content": DIGEST_PROMPT}, {"role": "user", "content": material}]
    reply = lm(messages)
    return reply    



