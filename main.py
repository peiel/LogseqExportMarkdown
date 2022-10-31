import os

from markdown_parser import *
from util import *

logseq_page_dir_path = '/Users/peiel/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/logseq/pages/'
blog_out_dir_path = '/Users/peiel/blog/content/posts/'

if __name__ == '__main__':
    # 清空博客目录
    os.system("rm -rf %s*" % blog_out_dir_path)
    # 读取page页面
    page_list = os.listdir(logseq_page_dir_path)
    cnt = 0
    for page in page_list:
        if 'md' not in page:
            continue
        md_content_lines = read_file_to_string(logseq_page_dir_path + page)
        if not need_publish_markdown(md_content_lines):
            continue
        md_name = page.replace('.md', '')
        # 生成 Markdown
        new_md_content = generate_blog_markdown(md_content_lines, md_name)
        # 写入到 blog 目录中
        write_to_blog_path(blog_out_dir_path, new_md_content, md_name)
        cnt = cnt + 1
    print("Export Blog Article Finish , Blog Cnt Is %s" % cnt)
