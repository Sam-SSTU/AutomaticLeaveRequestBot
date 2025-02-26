#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import argparse

def request_verify_code(phone, session_key=None):
    """
    请求验证码到指定手机号
    
    Args:
        phone: 手机号码
        session_key: 会话密钥（third-session值）
    """
    # 默认会话密钥
    if not session_key:
        session_key = "efe1e329-1292-4006-ba43-ed6866fcfa7c"
    
    # API 端点
    base_url = "http://fk.ghcollege.cn"
    verify_code_endpoint = "/visitor/api/iep/weixin/api/ams/wx0b5c194a8eb873fc/verifyCode"
    url = base_url + verify_code_endpoint
    
    # 请求头
    headers = {
        "Host": "fk.ghcollege.cn",
        "Accept": "application/json",
        "third-session": session_key,
        "WOKU-TOKEN": "Basic YXBwOmFwcA==",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Origin": "http://fk.ghcollege.cn",
        "Referer": "http://fk.ghcollege.cn/visitor/pages/ask/ask",
        "Connection": "keep-alive"
    }
    
    # 请求体
    payload = {"phone": phone}
    
    print(f"正在为手机号 {phone} 请求验证码...")
    
    try:
        # 发送请求
        response = requests.post(
            url, 
            headers=headers, 
            json=payload,
            timeout=10
        )
        
        # 打印响应状态和内容
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 解析响应
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get("code") == 200:
                    print("\n✅ 验证码已成功发送到手机号: " + phone)
                    print("请检查您的短信，验证码有效期约5分钟")
                    return True
                else:
                    print(f"\n❌ 请求失败: {result.get('msg', '未知错误')}")
            except json.JSONDecodeError:
                print("\n❌ 响应格式错误，无法解析JSON")
        else:
            print(f"\n❌ 请求失败，状态码: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求异常: {e}")
        
    return False

def main():
    parser = argparse.ArgumentParser(description="请求验证码到指定手机号")
    parser.add_argument("phone", help="接收验证码的手机号码")
    parser.add_argument("--session", help="可选: 会话密钥 (third-session值)")
    args = parser.parse_args()
    
    # 请求验证码
    request_verify_code(args.phone, args.session)

if __name__ == "__main__":
    main() 