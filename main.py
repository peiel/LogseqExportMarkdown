from util import *
from markdown_parser import *

blog_page_path = '/Users/peiel/Library/Mobile Documents/com~apple~CloudDocs/PKM/logseq/pages/blog.md'
logseq_page_dir_path = '/Users/peiel/Library/Mobile Documents/com~apple~CloudDocs/PKM/logseq/pages/'
blog_out_dir_path = '/Users/peiel/blog/content/posts/'

if __name__ == '__main__':
    # 读取page页面
    with open(blog_page_path) as f:
        lines = [line for line in f]
    lines = list(map(lambda x: format_line(x), lines))
    current_category = ""

    idx = 1
    for line in lines:
        if line.lstrip().startswith("##"):
            current_category = line.replace("##", "").strip()
            continue
        if line.startswith("\t"):
            md_name = get_markdown_title_by_line(line)
            create_time = get_create_time_by_line(line)
            tags = get_tags_by_line(line)
            print("开始生成文章 - %s \n分类: %s\n标题: %s\n创建时间: %s\n标签: %s\n"
                  % (idx, current_category, md_name, create_time, tags))
            # 读取 Markdown
            md_content_lines = read_file_to_string(logseq_page_dir_path + md_name + '.md')
            # 生成 Markdown
            new_md_content = generate_blog_markdown(md_content_lines, md_name, create_time, tags)
            # 写入到 blog 目录中
            write_to_blog_path(blog_out_dir_path, new_md_content, md_name)
            idx = idx + 1
