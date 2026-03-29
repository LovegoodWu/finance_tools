#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AmazingData ETF 数据测试脚本
用于测试获取 EXTRA_ETF（上交所 A 股、深交所的 ETF 列表）数据

作者：Kilo Code
日期：2026-03-29

注意：调用任何数据接口之前，必须先调用登录接口。
"""

import sys
import os
import traceback
from datetime import datetime

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ==================== 配置区域 ====================
# 请修改为您的实际配置
USERNAME = "111"      # 替换为您的账号
PASSWORD = "11@11"      # 替换为您的密码
HOST = "1"              # 替换为服务器 IP
PORT = 1                    # 替换为服务器端口号
# ================================================


def test_login():
    """
    测试 AmazingData 登录功能
    调用任何数据接口之前，必须先调用登录接口
    """
    print("\n" + "=" * 60)
    print("步骤 1: AmazingData 登录")
    print("=" * 60)
    print(f"    服务器：{HOST}:{PORT}")
    print(f"    账号：{USERNAME}")
    
    # 检查配置是否为默认值
    if USERNAME == "your_username" or HOST == "your_host":
        print("\n[!] 检测到使用默认配置，请先修改配置")
        print("\n请编辑此脚本，修改以下配置：")
        print(f"    USERNAME = 'your_username'    # 替换为您的账号")
        print(f"    HOST = 'your_host'            # 替换为服务器 IP")
        print(f"    PORT = 12345                  # 替换为服务器端口号")
        return False
    
    try:
        import AmazingData as ad
        result = ad.login(username=USERNAME, password=PASSWORD, host=HOST, port=PORT)
        print(f"[✓] 登录成功")
        return True
    except KeyboardInterrupt:
        print(f"\n[!] 登录被用户中断")
        return False
    except Exception as e:
        print(f"[✗] 登录失败：{e}")
        traceback.print_exc()
        return False


def test_get_calendar():
    """测试获取交易日历"""
    print("\n" + "=" * 60)
    print("步骤 2: 测试获取交易日历 (get_calendar)")
    print("=" * 60)
    
    try:
        import AmazingData as ad
        base_data_object = ad.BaseData()
        calendar = base_data_object.get_calendar()
        
        print(f"[✓] 获取交易日历成功")
        print(f"    返回类型：{type(calendar)}")
        print(f"    数据长度：{len(calendar) if calendar else 0}")
        
        if calendar and len(calendar) > 0:
            print(f"    最近 5 个交易日：{calendar[-5:]}")
        
        return True
    except Exception as e:
        print(f"[✗] 获取交易日历失败：{e}")
        traceback.print_exc()
        return False


def test_get_code_list_extra_etf():
    """测试获取 EXTRA_ETF 代码列表"""
    print("\n" + "=" * 60)
    print("步骤 3: 测试获取 ETF 列表 (get_code_list with EXTRA_ETF)")
    print("=" * 60)
    
    try:
        import AmazingData as ad
        base_data_object = ad.BaseData()
        
        # 获取 ETF 列表
        code_list = base_data_object.get_code_list(security_type='EXTRA_ETF')
        
        print(f"[✓] 获取 ETF 列表成功")
        print(f"    返回类型：{type(code_list)}")
        print(f"    ETF 数量：{len(code_list) if code_list else 0}")
        
        if code_list and len(code_list) > 0:
            print(f"\n    前 10 个 ETF 代码：")
            for i, code in enumerate(code_list[:10], 1):
                print(f"      {i}. {code}")
            
            if len(code_list) > 10:
                print(f"      ... 还有 {len(code_list) - 10} 个 ETF")
        
        return code_list
    except Exception as e:
        print(f"[✗] 获取 ETF 列表失败：{e}")
        traceback.print_exc()
        return None


def test_get_code_list_other_types():
    """测试获取其他类型的代码列表"""
    print("\n" + "=" * 60)
    print("步骤 4: 测试获取其他类型代码列表")
    print("=" * 60)
    
    try:
        import AmazingData as ad
        base_data_object = ad.BaseData()
        
        # 测试获取 A 股列表
        print("\n    测试获取 A 股列表 (EXTRA_STOCK_A)...")
        stock_list = base_data_object.get_code_list(security_type='EXTRA_STOCK_A')
        print(f"    [✓] A 股数量：{len(stock_list) if stock_list else 0}")
        
        # 测试获取指数列表
        print("\n    测试获取指数列表 (EXTRA_INDEX_A)...")
        index_list = base_data_object.get_code_list(security_type='EXTRA_INDEX_A')
        print(f"    [✓] 指数数量：{len(index_list) if index_list else 0}")
        
        return True
    except Exception as e:
        print(f"[✗] 获取其他类型代码列表失败：{e}")
        traceback.print_exc()
        return False


def save_etf_list(etf_list, filename='etf_list.txt'):
    """保存 ETF 列表到文件"""
    print("\n" + "=" * 60)
    print("步骤 5: 保存 ETF 列表到文件")
    print("=" * 60)
    
    if not etf_list:
        print("[!] ETF 列表为空，跳过保存")
        return
    
    try:
        # 保存到 tests 目录
        output_path = os.path.join(os.path.dirname(__file__), filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# ETF 列表\n")
            f.write(f"# 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 总数：{len(etf_list)}\n")
            f.write("#\n")
            for code in etf_list:
                f.write(f"{code}\n")
        
        print(f"[✓] ETF 列表已保存到 {output_path}")
    except Exception as e:
        print(f"[✗] 保存文件失败：{e}")


def main():
    """主函数"""
    print("\n" + "#" * 60)
    print("#" + " " * 18 + "AmazingData ETF 数据测试" + " " * 18 + "#")
    print("#" * 60 + "\n")
    
    # 1. 登录（必须先登录）
    login_result = test_login()
    if not login_result:
        print("\n[!] 登录失败，无法继续测试")
        sys.exit(1)
    
    # 2. 测试获取交易日历
    test_get_calendar()
    
    # 3. 测试获取 ETF 列表
    etf_list = test_get_code_list_extra_etf()
    
    # 4. 测试获取其他类型代码列表
    test_get_code_list_other_types()
    
    # 5. 保存 ETF 列表到文件
    if etf_list:
        save_etf_list(etf_list)
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
