#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import datetime
import pandas as pd
from pathlib import Path

def get_copied_db_path():
    """获取手动复制的 Messages 数据库路径"""
    home = Path.home()
    # 默认检查桌面上的复制文件
    db_path = home / "Desktop" / "messages_copy.db"
    
    # 也可以检查其他可能的位置
    alternative_paths = [
        home / "Downloads" / "messages_copy.db",
        home / "Documents" / "messages_copy.db",
        Path("/tmp/messages_copy.db")
    ]
    
    if db_path.exists():
        return db_path
    
    # 如果默认位置不存在，检查其他位置
    for path in alternative_paths:
        if path.exists():
            return path
    
    return None

def read_messages(db_path, limit=100):
    """从复制的数据库读取消息"""
    if not db_path.exists():
        print(f"复制的数据库不存在: {db_path}")
        return None
    
    try:
        # 连接到数据库
        print(f"尝试打开复制的数据库: {db_path}")
        conn = sqlite3.connect(db_path)
        
        # 尝试查看数据库结构
        tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql_query(tables_query, conn)
        print("数据库表:")
        print(tables)
        
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
    print("尝试读取手动复制的 Mac Messages 数据库...")
    
    # 找到复制的数据库路径
    db_path = get_copied_db_path()
    
    if db_path is None:
        print("\n未找到复制的数据库文件！请先手动复制数据库:")
        print("1. 打开终端并确保已授予完全磁盘访问权限")
        print("2. 执行命令: cp ~/Library/Messages/chat.db ~/Desktop/messages_copy.db")
        print("3. 或者使用 Finder 手动复制文件 (可能需要管理员权限)")
        print("4. 再次运行此脚本")
        return
    
    print(f"找到复制的数据库: {db_path}")
    
    # 读取消息
    messages = read_messages(db_path, 20)  # 获取最近20条消息
    
    if messages is not None and not messages.empty:
        print(f"\n成功读取 {len(messages)} 条消息:")
        print(messages)
        
        # 导出到 CSV (可选)
        csv_path = db_path.parent / "messages_export.csv"
        messages.to_csv(csv_path, index=False)
        print(f"\n消息已导出到: {csv_path}")
    else:
        print("\n无法读取消息。可能的原因:")
        print("1. 复制的数据库可能已损坏")
        print("2. 数据库结构与预期不符")
        print("3. 数据库可能是加密的")

if __name__ == "__main__":
    main() 