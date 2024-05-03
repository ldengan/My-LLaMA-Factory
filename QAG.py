import json
from lmqg import TransformersQG

qa_model = TransformersQG(language="en")

with open('data/all_faculties.json', 'r') as f:
    json_data = json.load(f)

all_qa_pairs = []

# 迭代每个faculty生成QA对
for faculty in json_data:
    try:
        # 构建上下文字符串
        context = ""
        if 'name' in faculty:
            context += f"Name: {faculty['name']['en']} "
        if 'edu' in faculty:
            context += f"Education: {faculty['edu'][0]} "
        if 'post' in faculty:
            context += f"Posts: {', '.join(faculty['post'])} "
        if 'contact' in faculty:
            contact_info = ", ".join(f"{k}: {v}" for k, v in faculty['contact'].items())
            context += f"Contact: {contact_info} "
        if 'profile' in faculty and 'interests' in faculty['profile']:
            context += f"Interests: {', '.join(faculty['profile']['interests'])} "

        # 生成QA对
        qa_pairs = qa_model.generate_qa(context, num_questions=10)  # 可以生成多个问题
        for qa in qa_pairs:
            all_qa_pairs.append(qa)

    except Exception as e:
        print(f"Error generating QA for faculty: {faculty}, Error: {e}")

final_qa_pairs = [{"question": item[0], "answer": item[1]} for item in all_qa_pairs]

with open('data/qa_pairs.json', 'w', encoding='utf-8') as json_file:
    json.dump(final_qa_pairs, json_file, ensure_ascii=False, indent=4)