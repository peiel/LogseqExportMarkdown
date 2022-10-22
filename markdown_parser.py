def format_line(line):
    """
    Format Logseq markdown line to standard markdown line
    :param line:
    :return:
    """
    if line.lstrip().startswith('- '):
        idx = line.index('-')
        line = line[:idx] + '  ' + line[idx + 2:]
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
    r_idx = line.rindex('[')
    l_idx = line.index(']')
    return line[r_idx + 1:l_idx]


def get_create_time_by_line(line):
    """
    获取 Markdown 的创建时间
    :param line:
    :return:
    """
    start = line.index('#')
    end = line[start:].index(' ') + start
    return line[start + 1:end]


def get_tags_by_line(line):
    """
    获取 Markdown 的标签
    :param line:
    :return: 标签列表
    """
    tags = list()
    tag = ''
    for ch in line:
        if '#' == ch:
            tag = ch
            continue
        if '#' in tag and ch != ' ':
            tag = tag + ch
            continue
        if ch == ' ' and tag != '':
            tags.append(tag.strip())
            tag = ''
    if tag != '':
        tags.append(tag.strip())
    return tags[1:]


def generate_blog_markdown(md_content_lines, md_title, create_time, tags):
    """
    通过原始信息生成新的 Markdown 文本
    :param md_content_lines: 获取的原始的内容的列表
    :param md_title: Markdown 的标题
    :param create_time: Markdown 的创建时间
    :param tags: 标签列表
    :return: 转换后的 Markdown 文本
    """
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
    for line in md_content_lines:
        line = format_line(line)
        if line.strip() == '-':  # 忽略的情况
            idx = idx + 1
            continue
        if line.strip().startswith('```'):
            loop_code = not loop_code
        if not loop_code:
            line = '\t' + line.lstrip() if need_add_tab(md_content_lines, idx) else line.lstrip()
            content = content + line
            content = content + '\n'
        else:
            content = content + line[2:]
        idx = idx + 1
    return content
