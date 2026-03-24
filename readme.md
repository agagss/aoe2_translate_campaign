使用googletrans翻译帝国时代2战役/ use googletrans to translate Age of Empire campaign/scenario

## 使用方法/ usage:

### 翻译.aoe2scenario/ translate .aoe2scenario：

将所有要翻译的.aoe2scenario文件放到input文件夹，在main.py中运行 
put all raw .aoe2scenario files to 'input' folder, then run in main.py:

···python
asyncio.run(translate_scenario(src='en', dest='zh-cn', replace=False))
```

input文件夹中已经有F4_Sforza_2.aoe2scenario，可以先运行下试试/ there is a F4_Sforza_2.aoe2scenario in the input folder, you can try run the code to see result


### 翻译campaign文件夹/ tanslate campaign folder:

确保campaign文件夹至少包含以下文件/ make sure the file structure contains at least the following files:
确保所有文件前缀都和文件夹同名，此处都为'my_campaign'/ make sure all files have the same name as the folder, here it's all 'my_campaign'
```
    my_campaign\
    │
    ├── info.json
    └── resources\
        └── _common\
            └── campaign\
                ├── my_campaign.aoe2campaign
                |── my_campaign_layout.json
                |── my_campaign.json
```

将campaign文件夹放入input文件夹，在main.py中运行 / put campaign folder inside 'input' folder, run in main.py

···python
asyncio.run(translate_other(campaign_name))
```

