from flask import Flask, request, jsonify
from flask_cors import CORS
from src.buffet_agent.agent import ValueInvestmentAgent
from src.buffet_agent.data import load_data, load_sample_data
import json

app = Flask(__name__)
# 添加CORS支持
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 创建全局智能体实例
agent = ValueInvestmentAgent()

# 加载示例数据
sample_data = load_sample_data()

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    运行完整价值投资分析
    
    请求参数:
    {
        "code": "股票代码",
        "user_question": "用户问题（可选）",
        "real_time": false
    }
    
    返回结果:
    {
        "success": true,
        "data": {
            "traditional_analysis": {},
            "github_deep_analysis": {},
            "integrated_recommendation": ""
        }
    }
    """
    try:
        data = request.json
        code = data.get('code')
        user_question = data.get('user_question')
        real_time = data.get('real_time', False)
        
        if not code:
            return jsonify({"success": False, "error": "缺少股票代码"}), 400
        
        # 加载股票数据
        stock_data = load_data(code, real_time)
        if not stock_data:
            # 尝试从示例数据中获取
            stock_data = sample_data.get(code)
            if not stock_data:
                return jsonify({"success": False, "error": "找不到股票数据"}), 404
        
        # 运行分析
        result = agent.run_analysis(stock_data, user_question)
        
        return jsonify({
            "success": True,
            "data": result
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/ask', methods=['POST'])
def ask():
    """
    处理用户追问
    
    请求参数:
    {
        "question": "用户问题"
    }
    
    返回结果:
    {
        "success": true,
        "data": {
            "answer": "回答内容",
            "confidence": 0.8,
            "related_topics": []
        }
    }
    """
    try:
        data = request.json
        question = data.get('question')
        
        if not question:
            return jsonify({"success": False, "error": "缺少问题内容"}), 400
        
        # 处理追问
        result = agent.ask_follow_up(question)
        
        return jsonify({
            "success": True,
            "data": result
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    """
    获取所有可用的股票列表
    
    返回结果:
    {
        "success": true,
        "data": [
            {
                "code": "股票代码",
                "name": "公司名称",
                "industry": "行业"
            }
        ]
    }
    """
    try:
        stocks = []
        for code, data in sample_data.items():
            stocks.append({
                "code": code,
                "name": data.get('name', ''),
                "industry": data.get('industry', '')
            })
        
        return jsonify({
            "success": True,
            "data": stocks
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
