#!/usr/bin/env python3
"""plagiarism_checker —— 基于 n-gram 重叠的轻量查重。

做法：
  - 把待查文档切成字符 n-gram（默认 5 元）；
  - 与内置参考库（多篇样例）的 n-gram 集合比对；
  - 命中的 n-gram 即重叠片段，重复率 = 命中数 / 总 n-gram 数；
  - 输出最相似的参考文档、重复率与重叠片段。
零第三方依赖。

用法：
    from plagiarism_checker import PlagiarismChecker
    pc = PlagiarismChecker()
    print(pc.check("待查文本……"))
"""
from __future__ import annotations

import argparse
import re
import sys

# 内置参考库样例
REFERENCE = {
    "人工智能简介": (
        "人工智能是研究如何让计算机模拟人类智能的一门学科。它涵盖机器学习、"
        "自然语言处理、计算机视觉等方向。近年来，深度学习极大推动了该领域发展。"
    ),
    "健康生活": (
        "保持健康的生活方式需要均衡饮食、规律运动和充足睡眠。多喝水，少熬夜，"
        "每天坚持三十分钟有氧运动，有助于提升免疫力与精神状态。"
    ),
    "旅游指南": (
        "出门旅行前应提前预订住宿、查看目的地天气并规划路线。带上身份证件与常用药品，"
        "注意保管随身财物，旅途安全始终是第一位的。"
    ),
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text)


def ngrams(text: str, n: int = 5) -> list[str]:
    t = normalize(text)
    if len(t) < n:
        return [t] if t else []
    return [t[i:i + n] for i in range(len(t) - n + 1)]


class PlagiarismChecker:
    def __init__(self, references: dict[str, str] | None = None, n: int = 5):
        self.n = n
        self.references = references or REFERENCE
        self.ref_ngrams = {
            name: set(ngrams(text, n)) for name, text in self.references.items()
        }

    def check(self, text: str) -> dict:
        q = ngrams(text, self.n)
        q_set = set(q)
        if not q_set:
            return {"repetition_rate": 0.0, "best_match": None, "overlaps": []}

        best_name = None
        best_rate = 0.0
        best_hits: set[str] = set()
        for name, ref_set in self.ref_ngrams.items():
            hits = q_set & ref_set
            rate = len(hits) / len(q_set)
            if rate > best_rate:
                best_rate = rate
                best_name = name
                best_hits = hits

        return {
            "repetition_rate": round(best_rate, 4),
            "best_match": best_name,
            "overlaps": sorted(best_hits),
        }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="n-gram 重叠查重")
    p.add_argument("text", nargs="?", help="待查文本；不传则读标准输入")
    p.add_argument("--n", type=int, default=5)
    args = p.parse_args(argv)
    text = args.text or sys.stdin.read()

    pc = PlagiarismChecker(n=args.n)
    r = pc.check(text)
    print(f"重复率：{r['repetition_rate']:.2%}")
    print(f"最相似参考：{r['best_match']}")
    if r["overlaps"]:
        print("重叠片段（前 10）：")
        for frag in r["overlaps"][:10]:
            print(f"  - {frag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
