import json

# 原始JSON数据
with open('data/qa_pairs.json', 'r') as f:
    original_data = json.load(f)

# 将原始数据转换成所需的格式
def convert_json(original_data):
    converted_data = []
    for item in original_data:
        converted_item = {
            "instruction": item["question"],
            "input": "",  # 假设没有用户输入
            "output": item["answer"],
            "system": "",  # 假设没有系统提示
            "history": []  # 假设没有历史记录
        }
        converted_data.append(converted_item)
    return converted_data

# 执行转换
converted_data = convert_json(original_data)

# 将转换后的数据写入新的JSON文件
with open('data/standard_data.json', 'w', encoding='utf-8') as f:
    json.dump(converted_data, f, ensure_ascii=False, indent=2)
