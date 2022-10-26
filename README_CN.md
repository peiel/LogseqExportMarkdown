# LogseqExportMarkdown

从 logseq 页面中导出 Markdown。

## 准备工作

logseq 页面中必须包含如下属性。

```
publish:: $category $DATE(%Y-%m-%d)
```

其他属性的支持

```
tags:: #xxx #xxx
```

## 如何使用

1. 拉取本仓库到本地
2. 配置 logseq 的页面路径和 Markdown 输出的路径
3. 执行命令 `python main.py`
