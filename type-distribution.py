#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MBTI类型分布统计分析工具
分析不同人群中MBTI类型的分布特征
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import json

class MBTIDistributionAnalyzer:
    """MBTI类型分布分析器"""

    def __init__(self):
        self.types = [
            'ISTJ', 'ISFJ', 'INFJ', 'INTJ',
            'ISTP', 'ISFP', 'INFP', 'INTP',
            'ESTP', 'ESFP', 'ENFP', 'ENTP',
            'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'
        ]

        # 全球人口分布数据 (百分比)
        self.global_distribution = {
            'ISTJ': 11.6, 'ISFJ': 13.8, 'INFJ': 1.5, 'INTJ': 2.1,
            'ISTP': 5.4, 'ISFP': 8.8, 'INFP': 4.4, 'INTP': 3.3,
            'ESTP': 4.3, 'ESFP': 7.3, 'ENFP': 8.1, 'ENTP': 2.5,
            'ESTJ': 8.7, 'ESFJ': 12.3, 'ENFJ': 2.5, 'ENTJ': 2.7
        }

        # 中国人口分布估计 (基于研究数据)
        self.china_distribution = {
            'ISTJ': 13.2, 'ISFJ': 15.1, 'INFJ': 2.1, 'INTJ': 2.8,
            'ISTP': 6.1, 'ISFP': 9.2, 'INFP': 5.1, 'INTP': 3.9,
            'ESTP': 4.8, 'ESFP': 7.9, 'ENFP': 8.8, 'ENTP': 2.9,
            'ESTJ': 9.5, 'ESFJ': 13.6, 'ENFJ': 2.8, 'ENTJ': 3.1
        }

    def load_survey_data(self, file_path: str) -> pd.DataFrame:
        """加载调查数据"""
        try:
            df = pd.read_csv(file_path)
            return df
        except FileNotFoundError:
            print(f"数据文件 {file_path} 不存在")
            return None

    def calculate_distribution(self, data: pd.DataFrame, type_column: str = 'mbti_type') -> Dict[str, float]:
        """计算类型分布"""
        if type_column not in data.columns:
            raise ValueError(f"列 '{type_column}' 不存在")

        type_counts = data[type_column].value_counts()
        total_count = len(data)

        distribution = {}
        for mbti_type in self.types:
            count = type_counts.get(mbti_type, 0)
            distribution[mbti_type] = (count / total_count) * 100

        return distribution

    def compare_distributions(self, dist1: Dict[str, float], dist2: Dict[str, float],
                            label1: str = "分布1", label2: str = "分布2") -> Dict:
        """比较两个分布的差异"""
        differences = {}
        for mbti_type in self.types:
            diff = dist1.get(mbti_type, 0) - dist2.get(mbti_type, 0)
            differences[mbti_type] = diff

        return {
            'differences': differences,
            'max_diff_type': max(differences.items(), key=lambda x: abs(x[1])),
            'correlation': self._calculate_correlation(dist1, dist2)
        }

    def _calculate_correlation(self, dist1: Dict[str, float], dist2: Dict[str, float]) -> float:
        """计算两个分布的相关系数"""
        values1 = [dist1.get(t, 0) for t in self.types]
        values2 = [dist2.get(t, 0) for t in self.types]
        return np.corrcoef(values1, values2)[0, 1]

    def analyze_by_demographics(self, data: pd.DataFrame,
                              group_column: str, type_column: str = 'mbti_type') -> Dict:
        """按人口统计学特征分析分布"""
        groups = data[group_column].unique()
        group_distributions = {}

        for group in groups:
            group_data = data[data[group_column] == group]
            distribution = self.calculate_distribution(group_data, type_column)
            group_distributions[group] = distribution

        return group_distributions

    def plot_distribution_comparison(self, dist1: Dict[str, float], dist2: Dict[str, float],
                                   title: str = "MBTI类型分布对比",
                                   label1: str = "分布1", label2: str = "分布2"):
        """绘制分布对比图"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # 第一个子图：柱状图对比
        x = np.arange(len(self.types))
        width = 0.35

        values1 = [dist1.get(t, 0) for t in self.types]
        values2 = [dist2.get(t, 0) for t in self.types]

        ax1.bar(x - width/2, values1, width, label=label1, alpha=0.8)
        ax1.bar(x + width/2, values2, width, label=label2, alpha=0.8)

        ax1.set_xlabel('MBTI类型')
        ax1.set_ylabel('百分比 (%)')
        ax1.set_title('类型分布对比')
        ax1.set_xticks(x)
        ax1.set_xticklabels(self.types, rotation=45)
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 第二个子图：散点图
        ax2.scatter(values1, values2, alpha=0.7, s=60)
        ax2.plot([0, max(max(values1), max(values2))],
                [0, max(max(values1), max(values2))], 'r--', alpha=0.5)

        # 添加类型标签
        for i, mbti_type in enumerate(self.types):
            ax2.annotate(mbti_type, (values1[i], values2[i]),
                        xytext=(5, 5), textcoords='offset points', fontsize=8)

        ax2.set_xlabel(f'{label1} (%)')
        ax2.set_ylabel(f'{label2} (%)')
        ax2.set_title('分布相关性')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    def generate_report(self, survey_data: pd.DataFrame = None) -> str:
        """生成分析报告"""
        report = []
        report.append("# MBTI类型分布分析报告\n")

        # 全球分布
        report.append("## 全球人口分布\n")
        global_sorted = sorted(self.global_distribution.items(), key=lambda x: x[1], reverse=True)
        for mbti_type, percentage in global_sorted:
            report.append(f"- **{mbti_type}**: {percentage:.1f}%")

        # 中国分布对比
        report.append("\n## 中国人口分布对比\n")
        comparison = self.compare_distributions(self.china_distribution, self.global_distribution,
                                             "中国", "全球")
        report.append(f"- 最大差异类型: {comparison['max_diff_type'][0]} "
                     f"(差异: {comparison['max_diff_type'][1]:+.1f}%)")
        report.append(f"- 相关系数: {comparison['correlation']:.3f}")

        # 如果有调查数据，添加分析
        if survey_data is not None:
            report.append("\n## 调查数据分析\n")
            survey_dist = self.calculate_distribution(survey_data)
            survey_comparison = self.compare_distributions(survey_dist, self.global_distribution,
                                                        "调查", "全球")
            report.append(f"- 调查样本数: {len(survey_data)}")
            report.append(f"- 与全球分布相关系数: {survey_comparison['correlation']:.3f}")

        return "\n".join(report)

    def export_data(self, filename: str, distributions: Dict[str, Dict[str, float]]):
        """导出分析数据"""
        export_data = {
            'metadata': {
                'types': self.types,
                'description': 'MBTI类型分布数据'
            },
            'distributions': distributions
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

def main():
    """主函数示例"""
    analyzer = MBTIDistributionAnalyzer()

    # 生成基础分析报告
    print("生成MBTI分布分析报告...")
    report = analyzer.generate_report()
    print(report)

    # 导出数据
    distributions = {
        'global': analyzer.global_distribution,
        'china': analyzer.china_distribution
    }
    analyzer.export_data('mbti_distributions.json', distributions)
    print("数据已导出到 mbti_distributions.json")

if __name__ == "__main__":
    main()