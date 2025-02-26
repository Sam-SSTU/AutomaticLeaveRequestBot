#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import datetime
import pandas as pd
from pathlib import Path

def get_messages_db_path():
    """获取 Messages 数据库路径"""
    home = Path.home()
    db_path = home / "Library" / "Messages" / "chat.db"
    return db_path

def read_messages(limit=100):
    """读取 Messages 数据库中的消息"""
    db_path = get_messages_db_path()
    
    if not db_path.exists():
        print(f"数据库文件不存在: {db_path}")
        return None
    
    try:
        # 连接到数据库
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        
        # 查询最近的消息
        query = """
        SELECT 
            m.rowid as message_id,
            m.date,
            m.text,
            h.id as chat_id,
            CASE m.is_from_me WHEN 1 THEN '发送' ELSE '接收' END as direction,
            m.service
        FROM message as m
        JOIN chat_message_join as cmj ON m.rowid = cmj.message_id
        JOIN chat as h ON cmj.chat_id = h.ROWID
        WHERE m.text IS NOT NULL
        ORDER BY m.date DESC
        LIMIT ?
        """
        
        # 执行查询
        df = pd.read_sql_query(query, conn, params=(limit,))
        
        # 处理时间戳 (Mac 时间戳是从 2001-01-01 开始的，单位是纳秒)
        mac_epoch = datetime.datetime(2001, 1, 1)
        df['date'] = df['date'].apply(lambda x: mac_epoch + datetime.timedelta(seconds=x/1000000000) if x else None)
        
        conn.close()
        return df
    
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")
    
    return None

def main():
    print("尝试读取 Mac Messages 应用中的消息...")
    
    # 检查数据库路径
    db_path = get_messages_db_path()
    print(f"Messages 数据库路径: {db_path}")
    print(f"数据库文件是否存在: {db_path.exists()}")
    
    # 读取消息
    messages = read_messages(20)  # 获取最近20条消息
    
    if messages is not None:
        print(f"\n成功读取 {len(messages)} 条消息:")
        print(messages)
    else:
        print("\n无法读取消息。可能的原因:")
        print("1. 权限不足: 需要在系统偏好设置中授予终端/Python完全磁盘访问权限")
        print("2. 数据库结构变化: Apple可能已更改数据库结构")
        print("3. 文件访问受限: Messages数据库可能被加密或受到SIP保护")
        
        print("\n解决方法:")
        print("- 在系统偏好设置 > 安全性与隐私 > 隐私 > 完全磁盘访问权限中添加终端或Python应用")
        print("- 尝试创建数据库文件的副本后再读取")

if __name__ == "__main__":
    main() 