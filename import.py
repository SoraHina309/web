from django.db import connections

# 检查数据库连接状态
connection = connections['default']
print("Connected database:", connection.settings_dict['NAME'])
print("Connected engine:", connection.settings_dict['ENGINE'])