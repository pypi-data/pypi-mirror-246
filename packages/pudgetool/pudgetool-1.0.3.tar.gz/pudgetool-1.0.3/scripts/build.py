import tomlkit  
  
# 使用 tomlkit 创建 pyproject.toml 文件  
with open('pyproject.toml', 'w') as f:  
    tomlkit.write(f, {  
        "build-system": "setuptools",  
        "requires": ["setuptools", "wheel"],  
        "options": {  
            "build-options": {  
                "install-requires": "numpy"  
            }  
        },  
    })