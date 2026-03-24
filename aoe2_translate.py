from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.objects.support.trigger_select import TS
import os
from googletrans import Translator
import asyncio
import json

input_dir = "input"

async def translate_scenario(src='zh-cn', dest='en', replace=False):
    '''
    src: 原始语言代码，例如中文为'zh-cn'，英文为'en'/ source language code, e.g. 'zh-cn' for Chinese, 'en' for English
    dest: 目标语言代码，例如中文为'zh-cn'，英文为'en'/ destination language code, e.g. 'zh-cn' for Chinese, 'en' for English
    replace: 是否替换已存在的翻译文件/ whether to replace existing translated files
    ''' 

    scenario_files = [
        f for f in os.listdir(input_dir)
        if f.endswith(".aoe2scenario") and os.path.isfile(os.path.join(input_dir, f))
    ]

    async with Translator() as translator:

        for scenario_file in scenario_files:
            scenario_file_fullpath = os.path.join(input_dir, scenario_file)
            scenario_file_translated = 'output/' + scenario_file.split('.')[0] + f'_{dest}.' + scenario_file.split('.')[-1]
            
            if not replace and os.path.exists(scenario_file_translated):
                print(f"{scenario_file_translated} already exists, skipping translation for {scenario_file}")
                continue

            raw_text = []

            scenario = AoE2DEScenario.from_file(scenario_file_fullpath)
            
            player_manager = scenario.player_manager
            player_one = player_manager.players[PlayerId.ONE]
            if player_one.tribe_name:
                p1_name = player_one.tribe_name
                raw_text.append(p1_name)
            player_two = player_manager.players[PlayerId.TWO]
            if player_two.tribe_name:
                p2_name = player_two.tribe_name
                raw_text.append(p2_name)
            player_three = player_manager.players[PlayerId.THREE]
            if player_three.tribe_name:
                p3_name = player_three.tribe_name
                raw_text.append(p3_name)
            player_four = player_manager.players[PlayerId.FOUR]
            if player_four.tribe_name:
                p4_name = player_four.tribe_name
                raw_text.append(p4_name)
            player_five = player_manager.players[PlayerId.FIVE]
            if player_five.tribe_name:
                p5_name = player_five.tribe_name
                raw_text.append(p5_name)
            player_six = player_manager.players[PlayerId.SIX]
            if player_six.tribe_name:
                p6_name = player_six.tribe_name
                raw_text.append(p6_name)
            player_seven = player_manager.players[PlayerId.SEVEN]
            if player_seven.tribe_name:
                p7_name = player_seven.tribe_name
                raw_text.append(p7_name)
            player_eight = player_manager.players[PlayerId.EIGHT]
            if player_eight.tribe_name:
                p8_name = player_eight.tribe_name
                raw_text.append(p8_name)



            message_manager = scenario.message_manager
            if message_manager.instructions:
                raw_text.append(message_manager.instructions)
            if message_manager.hints:
                raw_text.append(message_manager.hints)
            if message_manager.history:
                raw_text.append(message_manager.history)
            if message_manager.loss:
                raw_text.append(message_manager.loss)
            if message_manager.scouts:
                raw_text.append(message_manager.scouts)
            if message_manager.victory:
                raw_text.append(message_manager.victory)

            trigger = scenario.trigger_manager.get_trigger(TS.display(0))

            for trigger in scenario.trigger_manager.triggers:
                if trigger.description:
                    raw_text.append(trigger.description)

                if trigger.short_description:
                    raw_text.append(trigger.short_description)

                for effect in trigger.effects:
                    if effect.message:
                            raw_text.append(effect.message)

            translated = await translator.translate(raw_text, src=src, dest=dest)

            i = 0

            if player_one.tribe_name:
                player_one.tribe_name = translated[i].text
                i += 1
            if player_two.tribe_name:
                player_two.tribe_name = translated[i].text
                i += 1
            if player_three.tribe_name:
                player_three.tribe_name = translated[i].text
                i += 1
            if player_four.tribe_name:
                player_four.tribe_name = translated[i].text
                i += 1
            if player_five.tribe_name:
                player_five.tribe_name = translated[i].text
                i += 1
            if player_six.tribe_name:
                player_six.tribe_name = translated[i].text
                i += 1
            if player_seven.tribe_name:
                player_seven.tribe_name = translated[i].text
                i += 1
            if player_eight.tribe_name:
                player_eight.tribe_name = translated[i].text
                i += 1



            if message_manager.instructions:
                message_manager.instructions = translated[i].text
                i += 1
            if message_manager.hints:
                message_manager.hints = translated[i].text
                i += 1
            if message_manager.history:
                message_manager.history = translated[i].text
                i += 1
            if message_manager.loss:
                message_manager.loss = translated[i].text
                i += 1
            if message_manager.scouts:
                message_manager.scouts = translated[i].text
                i += 1
            if message_manager.victory:
                message_manager.victory = translated[i].text
                i += 1



            for trigger in scenario.trigger_manager.triggers:
                if trigger.description:
                    trigger.description = translated[i].text
                    i += 1

                if trigger.short_description:
                    trigger.short_description = translated[i].text
                    i += 1

                for effect in trigger.effects:
                    if effect.message:
                        effect.message = translated[i].text
                        i += 1

            scenario.write_to_file(scenario_file_translated)



async def translate_cascade_dict(obj, target_key, translator):
    '''
    翻译嵌套字典或列表中目标键的值/ translate the value of the target key in a nested dictionary or list
    '''
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == target_key and isinstance(value, str):
                translated = await translator.translate(value, src='zh-cn', dest='en')
                obj[key] = translated.text
            else:
                await translate_cascade_dict(obj[key], target_key, translator)

    elif isinstance(obj, list):
        for i in range(len(obj)):
            await translate_cascade_dict(obj[i], target_key, translator)



async def translate_other(campaign_name, src='zh-cn', dest='en'):
    '''
    campaign_name: 需要翻译的战役文件夹名称/ name of the campaign folder to be translated

    确保文件结构至少包含以下文件/ make sure the file structure contains at least the following files:
    确保所有文件前缀都和文件夹同名，此处都为'my_campaign'/ make sure all files have the same name as the folder, here it's all 'my_campaign'

    my_campaign\
    │
    ├── info.json
    └── resources\
        └── _common\
            └── campaign\
                ├── my_campaign.aoe2campaign
                |── my_campaign_layout.json
                |── my_campaign.json
    '''
    campaign_json_file = f"{input_dir}/{campaign_name}/resources/_common/campaign/{campaign_name}.json"
    with open(campaign_json_file, 'r', encoding='utf-8') as f:
        campaign_data = json.load(f)
        await translate_cascade_dict(campaign_data, "String", Translator())

    with open(campaign_json_file, 'w', encoding='utf-8') as f_out:
        json.dump(campaign_data, f_out, ensure_ascii=False, indent=4)



    campaign_layout_json = f"{input_dir}/{campaign_name}/resources/_common/campaign/{campaign_name}_layout.json"
    with open(campaign_layout_json, 'r', encoding='utf-8') as f:
        campaign_layout_data = json.load(f)
        await translate_cascade_dict(campaign_layout_data, "Text", Translator())

    with open(campaign_layout_json, 'w', encoding='utf-8') as f_out:
        json.dump(campaign_layout_data, f_out, ensure_ascii=False, indent=4)



    info_json_file = f"{input_dir}/{campaign_name}/info.json"
    with open(info_json_file, 'r', encoding='utf-8') as f:
        info_data = json.load(f)

        description = info_data["Description"]
        translated = await Translator().translate(description, src=src, dest=dest)
        info_data["Description"] = translated.text

        title = info_data["Title"]
        translated = await Translator().translate(title, src=src, dest=dest)
        info_data["Title"] = translated.text
        
    with open(info_json_file, 'w', encoding='utf-8') as f_out:
        json.dump(info_data, f_out, ensure_ascii=False, indent=4)
