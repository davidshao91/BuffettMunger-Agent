import requests
import json

def load_sample_data():
    """
    加载示例离线数据，与前端 data.js 保持一致
    """
    return {
        "600519.SH": {
            "code": "600519.SH",
            "name": "优质价值公司",
            "pe": 15.2,
            "pb": 3.1,
            "peg": 0.8,
            "pe_hist_percent": 22,
            "pb_hist_percent": 18,
            "roe_ttm": 22.5,
            "debt_to_asset": 35,
            "revenue_growth": 12,
            "profit_growth": 10,
            "gross_margin": 40,
            "cash_flow_healthy": True
        },
        "000858.SZ": {
            "code": "000858.SZ",
            "name": "五粮液",
            "pe": 18.1,
            "pb": 3.8,
            "peg": 0.9,
            "pe_hist_percent": 25,
            "pb_hist_percent": 22,
            "roe_ttm": 25.2,
            "debt_to_asset": 28,
            "revenue_growth": 10,
            "profit_growth": 9,
            "gross_margin": 74,
            "cash_flow_healthy": True
        },
        "600000.SH": {
            "code": "600000.SH",
            "name": "高风险高估公司",
            "pe": 48,
            "pb": 5.5,
            "peg": 1.9,
            "pe_hist_percent": 80,
            "pb_hist_percent": 85,
            "roe_ttm": 12.0,
            "debt_to_asset": 65,
            "revenue_growth": 2,
            "profit_growth": -3,
            "gross_margin": 20,
            "cash_flow_healthy": False
        }
    }

def get_sina_finance_data(stock_code):
    """
    从新浪财经获取实时股票数据
    """
    try:
        # 转换股票代码格式，新浪财经使用的格式
        if stock_code.endswith('.SH'):
            api_code = 'sh' + stock_code[:6]
        elif stock_code.endswith('.SZ'):
            api_code = 'sz' + stock_code[:6]
        else:
            return None
        
        # 新浪财经API接口
        url = f"http://hq.sinajs.cn/list={api_code}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            # 解析返回的数据
            data = response.text
            if '=' in data:
                data_part = data.split('=')[1].strip().strip('"')
                stock_info = data_part.split(',')
                
                if len(stock_info) > 3:
                    # 构建基本数据结构
                    return {
                        "code": stock_code,
                        "name": stock_info[0],
                        "pe": 15.0,  # 模拟数据
                        "pb": 3.0,   # 模拟数据
                        "peg": 1.0,  # 模拟数据
                        "pe_hist_percent": 50,  # 模拟数据
                        "pb_hist_percent": 50,  # 模拟数据
                        "roe_ttm": 15.0,  # 模拟数据
                        "debt_to_asset": 40,  # 模拟数据
                        "revenue_growth": 8,  # 模拟数据
                        "profit_growth": 5,  # 模拟数据
                        "gross_margin": 30,  # 模拟数据
                        "cash_flow_healthy": True  # 模拟数据
                    }
        return None
    except Exception as e:
        print(f"新浪财经API获取数据失败: {e}")
        return None

def get_xueqiu_data(stock_code):
    """
    从雪球网获取股票数据
    """
    try:
        # 转换股票代码格式，雪球网使用的格式
        if stock_code.endswith('.SH'):
            xueqiu_code = 'SH' + stock_code[:6]
        elif stock_code.endswith('.SZ'):
            xueqiu_code = 'SZ' + stock_code[:6]
        else:
            return None
        
        # 雪球网API接口（示例）
        url = f"https://stock.xueqiu.com/v5/stock/detail/{xueqiu_code}/profile.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": f"https://xueqiu.com/S/{xueqiu_code}"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            try:
                data = response.json()
                # 解析雪球网返回的数据
                if "data" in data:
                    stock_data = data["data"]
                    # 构建数据结构
                    return {
                        "code": stock_code,
                        "name": stock_data.get("name", "未知"),
                        "pe": 18.0,  # 模拟数据，实际需要从API返回中提取
                        "pb": 4.0,   # 模拟数据
                        "peg": 1.2,  # 模拟数据
                        "pe_hist_percent": 60,  # 模拟数据
                        "pb_hist_percent": 55,  # 模拟数据
                        "roe_ttm": 18.0,  # 模拟数据
                        "debt_to_asset": 35,  # 模拟数据
                        "revenue_growth": 10,  # 模拟数据
                        "profit_growth": 8,  # 模拟数据
                        "gross_margin": 35,  # 模拟数据
                        "cash_flow_healthy": True,  # 模拟数据
                        "source": "xueqiu"  # 标记数据源
                    }
            except json.JSONDecodeError:
                print("雪球网API返回数据格式错误")
        return None
    except Exception as e:
        print(f"雪球网API获取数据失败: {e}")
        return None

def get_xiaohongshu_data(stock_code):
    """
    从小红书获取相关投资信息和市场情绪
    """
    try:
        # 验证股票代码格式
        if not (stock_code.endswith('.SH') or stock_code.endswith('.SZ')):
            return None
        
        # 从小红书搜索相关股票信息
        # 注意：小红书API可能需要特殊处理，这里使用模拟数据作为示例
        # 实际项目中可能需要使用网页爬虫或官方API
        
        # 构建模拟数据，包含市场情绪和相关信息
        return {
            "code": stock_code,
            "name": "小红书数据",
            "pe": 20.0,  # 模拟数据
            "pb": 3.5,   # 模拟数据
            "peg": 1.1,  # 模拟数据
            "pe_hist_percent": 55,  # 模拟数据
            "pb_hist_percent": 50,  # 模拟数据
            "roe_ttm": 16.0,  # 模拟数据
            "debt_to_asset": 38,  # 模拟数据
            "revenue_growth": 9,  # 模拟数据
            "profit_growth": 7,  # 模拟数据
            "gross_margin": 32,  # 模拟数据
            "cash_flow_healthy": True,  # 模拟数据
            "source": "xiaohongshu",  # 标记数据源
            "market_sentiment": "positive",  # 市场情绪
            "related_topics": ["价值投资", "长期持有", "稳健增长"]  # 相关话题
        }
    except Exception as e:
        print(f"小红书数据获取失败: {e}")
        return None

def get_real_time_data(stock_code):
    """
    获取实时股票数据
    尝试从多个数据源获取数据
    """
    # 首先尝试从雪球网获取数据
    xueqiu_data = get_xueqiu_data(stock_code)
    if xueqiu_data:
        return xueqiu_data
    
    # 如果雪球网获取失败，尝试从新浪财经获取
    sina_data = get_sina_finance_data(stock_code)
    if sina_data:
        return sina_data
    
    # 如果新浪财经获取失败，尝试从小红书获取
    xiaohongshu_data = get_xiaohongshu_data(stock_code)
    if xiaohongshu_data:
        return xiaohongshu_data
    
    # 所有数据源都失败
    return None

def load_data(stock_code=None, use_real_time=False):
    """
    加载股票数据
    :param stock_code: 股票代码
    :param use_real_time: 是否使用实时数据
    :return: 股票数据字典
    """
    if use_real_time and stock_code:
        # 尝试获取实时数据
        real_time_data = get_real_time_data(stock_code)
        if real_time_data:
            return real_time_data
    
    # 如果无法获取实时数据或未指定股票代码，返回示例数据
    sample_data = load_sample_data()
    if stock_code and stock_code in sample_data:
        return sample_data[stock_code]
    return sample_data