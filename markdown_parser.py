import datetime as dt


def need_publish_markdown(lines):
    for line in lines:
        if line.startswith('publish:: '):
            return True
    return False


def format_line(line):
    """
    Format Logseq markdown line to standard markdown line
    :param line:
    :return:
    """
    if line.lstrip().startswith('- '):
        idx = line.index('-')
        line = line[:idx] + '  ' + line[idx + 2:]
    if line.lstrip().startswith("!["):
        start_idx = line.index('(')
        end_idx = line.index(')')
        line = line[:start_idx] + (line[start_idx:end_idx].replace(' ', '%20')) + line[end_idx:]
    return line


def need_add_tab(lines, idx):
    """
    判断 - 号格式的 markdown 文本是否需要添加 \t
    :param lines:
    :param idx:
    :return:
    """
    if idx == 0:  # 第一行不需要判断
        return False
    current_line = format_line(lines[idx])
    pre_line = format_line(lines[idx - 1])
    if '-' not in current_line or '-' not in pre_line:
        return False
    return current_line.index('-') - pre_line.index('-') == 1


def get_markdown_title_by_line(line):
    """
    通过行来获取 Markdown 的标题
    :param line:
    :return:
    """
    left_idx = line.index('[')
    right_idx = line.index(']')
    return line[left_idx + 2:right_idx]


def get_create_time_by_line(lines):
    """
    获取 Markdown 的创建时间
    :param lines:
    :return:
    """
    for line in lines:
        if line.startswith("publish:: "):
            idx = line.index('#2') + 1
            return line[idx:idx + 10]
    return dt.datetime.now().strftime('%Y-%m-%d')


def find_tags_line(lines):
    for line in lines:
        if 'tags::' in line:
            return line
    return []


def get_tags_by_line(lines):
    """
    获取 Markdown 的标签
    :param lines:
    :return: 标签列表
    """
    tags_prop_line = find_tags_line(lines)
    tags = list()
    tag = ''
    for ch in tags_prop_line:
        if '#' == ch:
            tag = ch
            continue
        if '#' in tag and ch != ' ':
            tag = tag + ch
            continue
        if ch == ' ' and tag != '':
            tags.append(tag.replace('[', '').strip())
            tag = ''
    if tag != '':
        tags.append(tag.replace('[', '').strip())
    return tags


def generate_blog_markdown(md_content_lines, md_title):
    """
    通过原始信息生成新的 Markdown 文本
    :param md_content_lines: 获取的原始的内容的列表
    :param md_title: Markdown 的标题
    :return: 转换后的 Markdown 文本
    """
    # 解析 tags
    tags = get_tags_by_line(md_content_lines)
    create_time = get_create_time_by_line(md_content_lines)
    # 头部内容开始拼接
    content = ''
    content = content + '---\n'
    content = content + 'title: ' + md_title + '\n'
    content = content + 'date: ' + create_time + '\n'
    if tags:
        content = content + 'tags:\n'
    for tag in tags:
        content = content + '  - ' + tag[1:] + '\n'
    content = content + '---\n\n'
    # 头部内容结束拼接
    idx = 0
    loop_code = False
    code_left_charset_length = 0
    for line in md_content_lines:
        line = format_line(line)
        if line.strip() == '-' \
                or 'collapsed::' in line \
                or 'title::' in line \
                or 'publish::' in line \
                or 'tags::' in line:  # 忽略的情况
            idx = idx + 1
            continue
        if line.strip().startswith('```'):
            loop_code = not loop_code
            if loop_code:
                code_left_charset_length = line.index("`")
            else:
                code_left_charset_length = 0
        if not loop_code:
            line = '\t' + line.lstrip() if need_add_tab(md_content_lines, idx) else line.lstrip()
            content = content + line
            content = content + '\n'
        else:
            content = content + line[code_left_charset_length:]
        idx = idx + 1
    return content
