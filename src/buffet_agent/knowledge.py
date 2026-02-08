"""知识图谱和推理能力模块"""
import os
import json
from typing import Optional, Dict, Any, List, Set, Tuple

class InvestmentKnowledgeGraph:
    """投资知识图谱"""
    
    def __init__(self):
        """
        初始化投资知识图谱
        """
        self.industry_knowledge: Dict[str, Dict[str, Any]] = {}
        self.company_relationships: Dict[str, List[Dict[str, str]]] = {}
        self.investment_logics: List[Dict[str, Any]] = []
        self.knowledge_base: Dict[str, Any] = {}
        
        # 初始化默认知识
        self._initialize_default_knowledge()
    
    def _initialize_default_knowledge(self):
        """
        初始化默认知识
        """
        # 行业知识
        self.industry_knowledge = {
            "白酒": {
                "characteristics": ["高毛利率", "强品牌效应", "抗周期性", "社交属性"],
                "key_metrics": ["毛利率", "净利率", "ROE", "品牌价值"],
                "risks": ["政策风险", "消费升级风险", "竞争加剧"],
                "leaders": ["贵州茅台", "五粮液", "泸州老窖"],
                "growth_prospects": "稳定",
                "valuation_band": "PE 15-30"
            },
            "银行": {
                "characteristics": ["高杠杆", "强监管", "周期性", "资产规模效应"],
                "key_metrics": ["ROE", "不良贷款率", "拨备覆盖率", "净息差"],
                "risks": ["信用风险", "利率风险", "监管风险"],
                "leaders": ["工商银行", "建设银行", "招商银行"],
                "growth_prospects": "缓慢",
                "valuation_band": "PB 0.5-1.5"
            },
            "医药": {
                "characteristics": ["研发驱动", "高壁垒", "长周期", "刚需属性"],
                "key_metrics": ["研发投入", "毛利率", "新药管线", "市场份额"],
                "risks": ["研发失败风险", "政策风险", "专利到期风险"],
                "leaders": ["恒瑞医药", "药明康德", "长春高新"],
                "growth_prospects": "良好",
                "valuation_band": "PE 20-40"
            },
            "科技": {
                "characteristics": ["技术迭代快", "高增长", "高风险", "规模效应"],
                "key_metrics": ["研发投入", "营收增长率", "毛利率", "用户增长"],
                "risks": ["技术迭代风险", "竞争风险", "估值风险"],
                "leaders": ["腾讯控股", "阿里巴巴", "华为"],
                "growth_prospects": "高速",
                "valuation_band": "PE 25-50"
            }
        }
        
        # 投资逻辑模板
        self.investment_logics = [
            {
                "id": "value_investing_basic",
                "name": "价值投资基础逻辑",
                "premises": [
                    "公司具有持续盈利能力",
                    "当前估值具有安全边际",
                    "公司具有护城河",
                    "管理层诚信且有能力"
                ],
                "conclusion": "该公司是一个潜在的价值投资标的",
                "confidence": 0.85,
                "applicable_industries": ["白酒", "银行", "医药", "科技"]
            },
            {
                "id": "growth_investing",
                "name": "成长投资逻辑",
                "premises": [
                    "公司营收高速增长",
                    "公司处于成长期行业",
                    "公司具有技术或商业模式优势",
                    "公司管理团队优秀"
                ],
                "conclusion": "该公司是一个潜在的成长投资标的",
                "confidence": 0.75,
                "applicable_industries": ["科技", "医药"]
            },
            {
                "id": "contrarian_investing",
                "name": "逆向投资逻辑",
                "premises": [
                    "公司当前估值处于历史低位",
                    "公司基本面并未恶化",
                    "市场对公司过度悲观",
                    "公司具有自我修复能力"
                ],
                "conclusion": "该公司可能存在逆向投资机会",
                "confidence": 0.7,
                "applicable_industries": ["银行", "周期股"]
            }
        ]
    
    def add_company_relationship(self, company: str, relationship: Dict[str, str]):
        """
        添加公司关系
        
        Args:
            company: 公司名称
            relationship: 关系信息，包含type和target
        """
        if company not in self.company_relationships:
            self.company_relationships[company] = []
        self.company_relationships[company].append(relationship)
    
    def get_company_relationships(self, company: str) -> List[Dict[str, str]]:
        """
        获取公司关系网络
        
        Args:
            company: 公司名称
            
        Returns:
            公司关系列表
        """
        return self.company_relationships.get(company, [])
    
    def get_industry_knowledge(self, industry: str) -> Optional[Dict[str, Any]]:
        """
        获取行业知识
        
        Args:
            industry: 行业名称
            
        Returns:
            行业知识
        """
        return self.industry_knowledge.get(industry)
    
    def infer_industry(self, company_name: str) -> Optional[str]:
        """
        根据公司名称推断行业
        
        Args:
            company_name: 公司名称
            
        Returns:
            推断的行业
        """
        industry_mappings = {
            "茅台": "白酒",
            "五粮液": "白酒",
            "泸州老窖": "白酒",
            "工商": "银行",
            "建设": "银行",
            "招商": "银行",
            "恒瑞": "医药",
            "药明": "医药",
            "长春": "医药",
            "腾讯": "科技",
            "阿里": "科技",
            "华为": "科技"
        }
        
        for keyword, industry in industry_mappings.items():
            if keyword in company_name:
                return industry
        
        return None
    
    def build_investment_reasoning_chain(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        构建投资推理链
        
        Args:
            company_data: 公司数据
            
        Returns:
            推理链
        """
        company_name = company_data.get("name", "未知公司")
        industry = self.infer_industry(company_name)
        
        # 收集证据
        evidence = self._collect_evidence(company_data, industry)
        
        # 应用投资逻辑
        applicable_logics = self._find_applicable_logics(industry)
        
        # 构建推理链
        reasoning_chain = {
            "company": company_name,
            "industry": industry,
            "evidence": evidence,
            "applicable_logics": applicable_logics,
            "reasoning_steps": self._generate_reasoning_steps(evidence, applicable_logics),
            "conclusion": self._draw_conclusion(evidence, applicable_logics),
            "confidence": self._calculate_confidence(evidence, applicable_logics)
        }
        
        return reasoning_chain
    
    def _collect_evidence(self, company_data: Dict[str, Any], industry: Optional[str]) -> List[Dict[str, Any]]:
        """
        收集证据
        
        Args:
            company_data: 公司数据
            industry: 行业
            
        Returns:
            证据列表
        """
        evidence = []
        
        # 财务指标证据
        roe = company_data.get("roe_ttm", 0)
        if roe > 15:
            evidence.append({
                "type": "financial",
                "metric": "ROE",
                "value": roe,
                "assessment": "优秀",
                "weight": 0.2
            })
        
        pe = company_data.get("pe", 0)
        if pe < 20:
            evidence.append({
                "type": "valuation",
                "metric": "PE",
                "value": pe,
                "assessment": "低估",
                "weight": 0.15
            })
        
        debt_to_asset = company_data.get("debt_to_asset", 100)
        if debt_to_asset < 50:
            evidence.append({
                "type": "financial",
                "metric": "资产负债率",
                "value": debt_to_asset,
                "assessment": "健康",
                "weight": 0.15
            })
        
        revenue_growth = company_data.get("revenue_growth", 0)
        if revenue_growth > 8:
            evidence.append({
                "type": "growth",
                "metric": "营收增长率",
                "value": revenue_growth,
                "assessment": "良好",
                "weight": 0.15
            })
        
        gross_margin = company_data.get("gross_margin", 0)
        if gross_margin > 30:
            evidence.append({
                "type": "profitability",
                "metric": "毛利率",
                "value": gross_margin,
                "assessment": "优秀",
                "weight": 0.15
            })
        
        # 行业证据
        if industry and industry in self.industry_knowledge:
            industry_info = self.industry_knowledge[industry]
            evidence.append({
                "type": "industry",
                "metric": "行业前景",
                "value": industry_info.get("growth_prospects", "一般"),
                "assessment": "正面" if industry_info.get("growth_prospects") in ["良好", "高速"] else "中性",
                "weight": 0.1
            })
        
        # 安全边际证据
        pe_hist_percent = company_data.get("pe_hist_percent", 100)
        if pe_hist_percent < 30:
            evidence.append({
                "type": "valuation",
                "metric": "PE历史分位",
                "value": pe_hist_percent,
                "assessment": "低估",
                "weight": 0.1
            })
        
        return evidence
    
    def _find_applicable_logics(self, industry: Optional[str]) -> List[Dict[str, Any]]:
        """
        找到适用的投资逻辑
        
        Args:
            industry: 行业
            
        Returns:
            适用的投资逻辑列表
        """
        applicable_logics = []
        
        for logic in self.investment_logics:
            if not industry:
                applicable_logics.append(logic)
            elif industry in logic.get("applicable_industries", []):
                applicable_logics.append(logic)
        
        return applicable_logics
    
    def _generate_reasoning_steps(self, evidence: List[Dict[str, Any]], applicable_logics: List[Dict[str, Any]]) -> List[str]:
        """
        生成推理步骤
        
        Args:
            evidence: 证据
            applicable_logics: 适用的投资逻辑
            
        Returns:
            推理步骤列表
        """
        steps = []
        
        # 第一步：分析财务健康度
        financial_evidence = [e for e in evidence if e["type"] == "financial"]
        if financial_evidence:
            positive_financial = [e for e in financial_evidence if e["assessment"] in ["优秀", "良好", "健康"]]
            if len(positive_financial) > 0:
                steps.append(f"财务分析：{len(positive_financial)}/{len(financial_evidence)}个财务指标表现良好")
            else:
                steps.append("财务分析：财务指标表现一般")
        
        # 第二步：分析估值水平
        valuation_evidence = [e for e in evidence if e["type"] == "valuation"]
        if valuation_evidence:
            positive_valuation = [e for e in valuation_evidence if e["assessment"] == "低估"]
            if len(positive_valuation) > 0:
                steps.append(f"估值分析：{len(positive_valuation)}/{len(valuation_evidence)}个估值指标显示低估")
            else:
                steps.append("估值分析：估值水平一般")
        
        # 第三步：分析增长潜力
        growth_evidence = [e for e in evidence if e["type"] == "growth"]
        industry_evidence = [e for e in evidence if e["type"] == "industry"]
        all_growth_evidence = growth_evidence + industry_evidence
        
        if all_growth_evidence:
            positive_growth = [e for e in all_growth_evidence if e["assessment"] in ["优秀", "良好", "正面"]]
            if len(positive_growth) > 0:
                steps.append(f"增长分析：{len(positive_growth)}/{len(all_growth_evidence)}个增长指标表现良好")
            else:
                steps.append("增长分析：增长潜力一般")
        
        # 第四步：应用投资逻辑
        if applicable_logics:
            steps.append(f"应用投资逻辑：{len(applicable_logics)}个投资逻辑适用于该公司")
        
        return steps
    
    def _draw_conclusion(self, evidence: List[Dict[str, Any]], applicable_logics: List[Dict[str, Any]]) -> str:
        """
        得出结论
        
        Args:
            evidence: 证据
            applicable_logics: 适用的投资逻辑
            
        Returns:
            结论
        """
        # 计算正面证据比例
        positive_evidence = [e for e in evidence if e["assessment"] in ["优秀", "良好", "健康", "低估", "正面"]]
        positive_ratio = len(positive_evidence) / len(evidence) if evidence else 0
        
        # 计算逻辑支持度
        logic_support = sum([logic.get("confidence", 0) for logic in applicable_logics]) / len(applicable_logics) if applicable_logics else 0
        
        # 综合评估
        score = positive_ratio * 0.7 + logic_support * 0.3
        
        if score >= 0.7:
            return "强烈推荐：该公司符合价值投资标准，具有良好的投资价值"
        elif score >= 0.5:
            return "谨慎推荐：该公司具有一定投资价值，但存在一些风险因素"
        else:
            return "不推荐：该公司不符合价值投资标准，存在较多风险"
    
    def _calculate_confidence(self, evidence: List[Dict[str, Any]], applicable_logics: List[Dict[str, Any]]) -> float:
        """
        计算置信度
        
        Args:
            evidence: 证据
            applicable_logics: 适用的投资逻辑
            
        Returns:
            置信度
        """
        if not evidence and not applicable_logics:
            return 0.3
        
        # 证据置信度
        evidence_confidence = sum([e.get("weight", 0) for e in evidence]) / len(evidence) if evidence else 0
        
        # 逻辑置信度
        logic_confidence = sum([logic.get("confidence", 0) for logic in applicable_logics]) / len(applicable_logics) if applicable_logics else 0
        
        # 综合置信度
        confidence = evidence_confidence * 0.6 + logic_confidence * 0.4
        
        return max(0.3, min(0.95, confidence))
    
    def cross_validate_information(self, company_data: Dict[str, Any], external_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        多源信息交叉验证
        
        Args:
            company_data: 公司数据
            external_data: 外部数据
            
        Returns:
            验证结果
        """
        validation_results = {
            "matches": [],
            "mismatches": [],
            "conflicts": [],
            "overall_assessment": ""
        }
        
        # 验证关键指标
        key_metrics = ["pe", "pb", "roe_ttm", "revenue_growth", "profit_growth"]
        
        for metric in key_metrics:
            internal_value = company_data.get(metric)
            external_value = external_data.get(metric)
            
            if internal_value and external_value:
                # 计算差异百分比
                if internal_value != 0:
                    diff_percent = abs((float(external_value) - float(internal_value)) / float(internal_value)) * 100
                    
                    if diff_percent < 10:
                        validation_results["matches"].append({
                            "metric": metric,
                            "internal_value": internal_value,
                            "external_value": external_value,
                            "diff_percent": diff_percent,
                            "assessment": "一致"
                        })
                    elif diff_percent < 30:
                        validation_results["mismatches"].append({
                            "metric": metric,
                            "internal_value": internal_value,
                            "external_value": external_value,
                            "diff_percent": diff_percent,
                            "assessment": "轻微差异"
                        })
                    else:
                        validation_results["conflicts"].append({
                            "metric": metric,
                            "internal_value": internal_value,
                            "external_value": external_value,
                            "diff_percent": diff_percent,
                            "assessment": "显著差异"
                        })
        
        # 总体评估
        total_metrics = len(key_metrics)
        match_count = len(validation_results["matches"])
        mismatch_count = len(validation_results["mismatches"])
        conflict_count = len(validation_results["conflicts"])
        
        if match_count / total_metrics >= 0.7:
            validation_results["overall_assessment"] = "数据一致性良好"
        elif conflict_count / total_metrics >= 0.3:
            validation_results["overall_assessment"] = "数据存在显著冲突"
        else:
            validation_results["overall_assessment"] = "数据存在轻微差异"
        
        return validation_results
    
    def enhance_analysis_with_knowledge(self, analysis: Dict[str, Any], company_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        使用知识图谱增强分析
        
        Args:
            analysis: 原始分析
            company_data: 公司数据
            
        Returns:
            增强后的分析
        """
        # 构建投资推理链
        reasoning_chain = self.build_investment_reasoning_chain(company_data)
        
        # 添加行业洞察
        company_name = company_data.get("name", "未知公司")
        industry = self.infer_industry(company_name)
        industry_insights = self.get_industry_knowledge(industry) if industry else None
        
        # 增强分析结果
        enhanced_analysis = analysis.copy()
        enhanced_analysis["knowledge_enhanced"] = {
            "reasoning_chain": reasoning_chain,
            "industry_insights": industry_insights,
            "company_relationships": self.get_company_relationships(company_name),
            "confidence_enhancement": reasoning_chain.get("confidence", 0.5),
            "knowledge_based_recommendation": reasoning_chain.get("conclusion", "无法得出结论")
        }
        
        # 调整综合推荐
        if "integrated_recommendation" in enhanced_analysis:
            knowledge_confidence = reasoning_chain.get("confidence", 0.5)
            if knowledge_confidence > 0.7:
                # 知识图谱高度支持，增强推荐强度
                current_rec = enhanced_analysis["integrated_recommendation"]
                if "规避" in current_rec:
                    enhanced_analysis["integrated_recommendation"] = "⚠️  中性观察"
                elif "中性" in current_rec:
                    enhanced_analysis["integrated_recommendation"] = "✅ 建议买入"
                elif "买入" in current_rec:
                    enhanced_analysis["integrated_recommendation"] = "🌟 强烈推荐"
        
        return enhanced_analysis

# 导出函数
def build_investment_reasoning(company_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    构建投资推理
    
    Args:
        company_data: 公司数据
        
    Returns:
        推理结果
    """
    knowledge_graph = InvestmentKnowledgeGraph()
    return knowledge_graph.build_investment_reasoning_chain(company_data)

def enhance_analysis(analysis: Dict[str, Any], company_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    增强分析
    
    Args:
        analysis: 原始分析
        company_data: 公司数据
        
    Returns:
        增强后的分析
    """
    knowledge_graph = InvestmentKnowledgeGraph()
    return knowledge_graph.enhance_analysis_with_knowledge(analysis, company_data)

def cross_validate_data(company_data: Dict[str, Any], external_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    交叉验证数据
    
    Args:
        company_data: 公司数据
        external_data: 外部数据
        
    Returns:
        验证结果
    """
    knowledge_graph = InvestmentKnowledgeGraph()
    return knowledge_graph.cross_validate_information(company_data, external_data)
