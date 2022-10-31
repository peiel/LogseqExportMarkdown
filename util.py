import re
import pinyin


def read_file_to_string(path):
    """
    通过文件的路径获取内容
    :param path:
    :return: 行的列表
    """
    # path = path.replace('#', '%23')
    with open(path) as f:
        return f.readlines()


def write_to_blog_path(target_path, new_md_content, md_name):
    """
    把 Markdown 内容写到文件中
    :param target_path:
    :param new_md_content:
    :param md_name:
    :return:
    """
    english_name = convert_chinese_string_to_pinyin(md_name) + '.md'
    write_content_to_path(target_path + english_name, new_md_content)


def write_content_to_path(target_path, content):
    """
    把内容写到目标文件中
    :param target_path:
    :param content:
    :return:
    """
    with open(target_path, 'wt', encoding='utf-8') as f:
        f.write(content)


def convert_chinese_string_to_pinyin(chinese_str):
    chinese_str = chinese_str.replace(" ", "-")
    chinese_str = chinese_str.replace("(", "-")
    chinese_str = chinese_str.replace(")", "-")
    chinese_str = chinese_str.replace("（", "-")
    chinese_str = chinese_str.replace("）", "-")
    chinese_str = chinese_str.replace(",", "-")
    chinese_str = chinese_str.replace("'", "-")
    chinese_str = chinese_str.replace("~", "-")
    chinese_str = chinese_str.replace("?", "-")
    chinese_str = chinese_str.replace("？", "-")
    m = {}
    for n in re.findall(r'[\u4e00-\u9fff]+', chinese_str):
        m[n] = pinyin.get(n, format="strip", delimiter=" ")
    for key in m:
        chinese_str = chinese_str.replace(key, m[key])
    py = chinese_str.replace(' ', '-').lower()
    pys = py.split('-')
    result = ''
    for item in pys:
        if item:
            result = result + item + '-'
    return result[:-1]
