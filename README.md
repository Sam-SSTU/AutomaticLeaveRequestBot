# Mac Messages 数据读取工具

这个 Python 工具用于读取 macOS Messages 应用程序中的消息数据。Messages 应用中的所有消息都存储在一个 SQLite 数据库中，该脚本通过访问这个数据库来获取消息内容。

## 前提条件

- macOS 操作系统
- Python 3.6+
- pandas 库（用于数据处理）

## 安装依赖

```bash
pip install pandas
```

## 不同的读取方法

本项目提供了三种不同的方法来尝试读取 Messages 数据：

1. **直接读取** (`read_messages.py`): 尝试直接读取原始数据库，需要完全磁盘访问权限。
2. **自动复制** (`read_messages_copy.py`): 尝试自动创建数据库副本再读取，同样需要完全磁盘访问权限。
3. **手动复制** (`read_manual_copy.py`): 读取用户手动复制到桌面（或其他位置）的数据库副本。

## 处理 macOS 安全限制的详细步骤

### 方法 1: 使用完全磁盘访问权限

1. 打开"系统设置"（System Settings）
2. 导航至"隐私与安全性" > "隐私" > "完全磁盘访问权限"
3. 单击锁图标并输入您的密码以进行更改
4. 点击"+"按钮，添加以下应用：
   - Terminal（终端）
   - iTerm（如果您使用）
   - Python 应用程序（通常在 `/Applications/Python 3.x/` 或 `/usr/local/bin/python3`）
   - 您的代码编辑器（如 VS Code、PyCharm 等）
5. 确保所有添加的应用程序旁边的复选框都已选中
6. 重启所有相关应用程序
7. 运行 `python read_messages.py`

### 方法 2: 手动复制数据库（推荐）

这是绕过权限问题最可靠的方法：

1. 确保已为 Terminal 授予完全磁盘访问权限
2. 打开 Terminal 并运行：
   ```bash
   cp ~/Library/Messages/chat.db ~/Desktop/messages_copy.db
   ```
3. 如果上述命令返回权限错误，尝试使用 `sudo`：
   ```bash
   sudo cp ~/Library/Messages/chat.db ~/Desktop/messages_copy.db
   ```
   (需要输入您的管理员密码)
4. 运行脚本读取复制的数据库：
   ```bash
   python read_manual_copy.py
   ```

### 方法 3: 使用 Time Machine 备份

如果您有 Time Machine 备份，可以通过备份访问消息数据：

1. 进入 Time Machine 备份
2. 导航到 `~/Library/Messages/`
3. 复制 `chat.db` 到一个您可以访问的位置
4. 修改 `read_manual_copy.py` 中的路径以指向备份复制的位置

## 故障排除

### 权限被拒绝

如果您遇到 "Operation not permitted" 错误：

```
ls: /Users/username/Library/Messages/: Operation not permitted
```

这是因为 macOS 的隐私保护机制（System Integrity Protection, SIP）阻止了对某些系统文件的访问。即使是 sudo 或管理员用户也可能无法访问。请使用上述完全磁盘访问权限方法解决。

### 数据库结构问题

如果脚本可以访问数据库但查询失败，可能是因为 Apple 更改了数据库结构。尝试以下方法：

1. 使用 SQLite 浏览器检查数据库结构：
   ```bash
   sqlite3 ~/Desktop/messages_copy.db .schema
   ```

2. 根据实际结构修改脚本中的 SQL 查询

### 其他常见问题

- **空结果**: 可能是因为您的 Messages 数据很少或存储在 iCloud 中
- **SQL 错误**: 检查是否使用了正确的表名和列名
- **时间戳不正确**: macOS 使用特殊的时间戳格式（从2001年1月1日开始计数），确保正确转换

## 数据导出

成功读取消息后，脚本可以将结果导出为 CSV 文件，便于使用 Excel 或其他工具分析：

```python
# 导出到CSV
df.to_csv("messages_export.csv", index=False)
```

## 注意事项

- 该工具仅供学习和个人使用
- 请尊重他人隐私，不要未经许可读取他人的消息数据
- Apple 可能会在未来版本中进一步限制对 Messages 数据的访问

## 数据库备份

建议在使用此脚本前备份您的 Messages 数据库:

```bash
cp -r ~/Library/Messages ~/Desktop/Messages_Backup
``` 