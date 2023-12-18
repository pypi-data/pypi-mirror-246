import pandas as pd

df = pd.read_csv('emoji_df.csv')
emoji_meanings=dict(zip(df['emoji'], df['name']))


def emoji_converter(text,emoji_m = emoji_meanings):
        # Replace emojis in the text with their meanings
        converted_text = text
        for emoji, meaning in emoji_m.items():
            converted_text = converted_text.replace(emoji, f':{meaning}:')
        return converted_text
