#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import datetime
import pandas as pd
import subprocess
import tempfile
from pathlib import Path
import shutil

def get_messages_db_path():
    """获取 Messages 数据库路径"""
    home = Path.home()
    db_path = home / "Library" / "Messages" / "chat.db"
    return db_path

def copy_messages_db():
    """创建 Messages 数据库的副本"""
    original_db = get_messages_db_path()
    
    if not original_db.exists():
        print(f"原始数据库不存在: {original_db}")
        return None
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    temp_db = Path(temp_dir) / "messages_copy.db"
    
    try:
        # 复制数据库文件
        print(f"尝试复制数据库到: {temp_db}")
        subprocess.run(['cp', str(original_db), str(temp_db)], check=True)
        print("数据库复制成功！")
        return temp_db
    except subprocess.CalledProcessError as e:
        print(f"复制数据库失败: {e}")
        return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None

def read_messages_from_copy(limit=100):
    """从数据库副本读取消息"""
    db_path = copy_messages_db()
    
    if db_path is None:
        print("无法创建数据库副本")
        return None
    
    try:
        # 连接到数据库
        print(f"尝试打开数据库副本: {db_path}")
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
        
        # 清理临时文件
        if db_path.exists():
            os.remove(db_path)
        temp_dir = db_path.parent
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            
        return df
    
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")
    
    # 清理临时文件
    try:
        if db_path and db_path.exists():
            os.remove(db_path)
        temp_dir = db_path.parent
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
    except:
        pass
        
    return None

def main():
    print("尝试通过复制数据库来读取 Mac Messages 应用中的消息...")
    
    # 检查原始数据库路径
    db_path = get_messages_db_path()
    print(f"原始 Messages 数据库路径: {db_path}")
    print(f"数据库文件是否存在: {db_path.exists()}")
    
    # 读取消息
    messages = read_messages_from_copy(20)  # 获取最近20条消息
    
    if messages is not None and not messages.empty:
        print(f"\n成功读取 {len(messages)} 条消息:")
        print(messages)
    else:
        print("\n无法读取消息。可能的原因:")
        print("1. 权限不足: 即使使用复制方法也需要相应权限")
        print("2. 数据库结构变化: Apple可能已更改数据库结构")
        print("3. 文件访问受限: Messages数据库可能被加密或受到SIP保护")
        
        print("\n解决方法:")
        print("- 在系统设置 > 隐私与安全性 > 隐私 > 完全磁盘访问权限中添加终端或Python应用")
        print("- 确保 Terminal 应用有足够的权限执行复制操作")
        print("- 可以尝试手动复制数据库文件:")
        print(f"  cp {db_path} ~/Desktop/messages_copy.db")
        print("  然后修改脚本读取这个手动复制的文件")

if __name__ == "__main__":
    main() 