# plagiarism-checker-lite

基于 **n-gram 重叠**的轻量查重器：把待查文档切成字符 n-gram，与内置参考库比对，
输出最相似参考、重复率与重叠片段。零第三方依赖。

## 功能简介

- 字符 n-gram（默认 5 元，空白先折叠）；
- 内置 3 篇中文参考样例（人工智能 / 健康生活 / 旅游指南），开箱即用；
- `check(text)` 返回 `{repetition_rate, best_match, overlaps}`；
- 重复率 = 命中参考库的 n-gram 数 / 待查文档总 n-gram 数。

## 快速开始

环境：Python 3.10+，零依赖。

```bash
python3 plagiarism_checker.py "人工智能是研究如何让计算机模拟人类智能的一门学科。"
```

作为库：

```python
from plagiarism_checker import PlagiarismChecker
pc = PlagiarismChecker()
print(pc.check("待查文本……"))
```

## 使用示例（真实命令）

```bash
$ python3 plagiarism_checker.py "人工智能是研究如何让计算机模拟人类智能的一门学科"
重复率：85.xx%
最相似参考：人工智能简介
重叠片段（前 10）：
  - 人工智能是
  - 工智能是研
  ...
```

## 无 API key 如何运行

纯本地 n-gram 集合比对，**不需要任何 API key**，不联网。

## 目录结构

```
plagiarism-checker-lite/
├── plagiarism_checker.py            # n-gram 查重 + 内置参考库 + CLI
├── tests/
│   └── test_plagiarism.py           # unittest
├── README.md
├── LICENSE
└── .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests -v
```

## 许可证

[MIT](./LICENSE) © 2026 ljiang9
