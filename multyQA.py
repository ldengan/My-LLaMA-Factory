import json

with open('data/all_faculties.json', 'r') as f:
    faculty_list = json.load(f)

# 示例查询条件
conditions = [
    {"post": "President"},
    {"profile.interests": "Neuroscience"},
    {"edu": "Harvard University"}
]


def get_nested_value(data, keys):
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data


def query_faculty(conditions):
    results = faculty_list
    for condition in conditions:
        keys = list(condition.keys())[0]  # 获取查询字段
        value = condition[keys]            # 获取要匹配的条件值
        key_parts = keys.split('.')      # 分割嵌套的键

        def match(item):
            # 递归地获取嵌套的值
            nested_item = item
            for part in key_parts:
                nested_item = nested_item.get(part, None)
                if nested_item is None:
                    return False
            # 检查获取的值是否是列表
            return any(v.lower() == value.lower() for v in nested_item if isinstance(v, str))

        # 筛选出符合条件的faculty
        results = [fac for fac in results if match(fac)]
    return results

# 执行查询并生成QA对
qa_pairs = []
for condition in conditions:
    # 获取查询字段和对应的值
    query_field = list(condition.keys())[0]  # 假设每个condition字典只有一个键
    query_value = condition[query_field]

    # 根据查询字段构造question
    if query_field == "post":
        question = f"Who holds the post of {query_value}?"
    elif query_field == "profile.interests":
        question = f"Which faculty are interested in {query_value}?"
    elif query_field == "edu":
        question = f"How many faculty graduated from {query_value}?"
    else:
        question = "Unknown query condition"

    # 执行查询
    answer = query_faculty([condition])

    # 获取满足条件的faculty的英文姓名
    faculty_names = ', '.join([fac["name"]["en"] for fac in answer if "name" in fac and "en" in fac["name"]])
    count = len(answer)

    # 构造answer的字符串格式
    if count > 0:
        answer_str = f"Your search returned {count} results for faculty {faculty_names}."
    else:
        answer_str = "Your search returned 0 results."

    qa_pairs.append({
        "question": question,
        "answer": answer_str
    })

try:
    with open('data/qa_pairs.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    data = []

# 合并数据
if isinstance(data, list):
    data.extend(qa_pairs)
else:
    data['qa_pairs'].extend(qa_pairs)

# 写入合并后的数据
with open('data/qa_pairs.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)