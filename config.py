import os
import json
from languages import default_language

class Config:
    def __init__(self):
        # 配置文件路径
        self.config_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(self.config_dir, "config.json")
        
        # 默认配置
        self.defaults = {
            "language": default_language,  # 默认语言
            "project_root": self.config_dir,  # 项目根目录
            "chrome_path": "",  # Chrome路径
            "chromedriver_path": ""  # ChromeDriver路径
        }
        
        # 加载配置文件
        self.settings = self.load()
    
    def load(self):
        """从配置文件加载设置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                # 确保所有键都存在，如果缺少则使用默认值
                for key, value in self.defaults.items():
                    if key not in settings:
                        settings[key] = value
                return settings
        except Exception as e:
            print(f"加载配置文件时出错: {e}")
        
        # 如果加载失败或文件不存在，返回默认配置
        return self.defaults.copy()
    
    def save(self):
        """保存设置到配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"保存配置文件时出错: {e}")
            return False
    
    def get(self, key, default=None):
        """获取设置值"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """设置值并保存"""
        self.settings[key] = value
        return self.save()
    
    def update(self, settings_dict):
        """批量更新设置并保存"""
        self.settings.update(settings_dict)
        return self.save()

# 全局配置实例
config = Config() 