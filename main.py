from aoe2_translate import *

if __name__ == "__main__":
    # 翻译.aoe2scenario文件/ translate .aoe2scenario file
    asyncio.run(translate_scenario(src='en', dest='zh-cn', replace=False))

    '''
    #翻译 info.json/layout.json .../ translate info.json/layout.json ...
    campaign_name = "your_campaign" # 需要翻译的战役文件夹名称/ name of the campaign folder to be translated
    asyncio.run(translate_other(campaign_name))
    '''

