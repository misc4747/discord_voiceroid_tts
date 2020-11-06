import discord
import text2wav
import ffmpeg
import time
import re

TOKEN = "TOKEN" #Replace TOKEN with your discord bot token
client = discord.Client()
queue = []

def play_voice(path):
    print(queue)
    if not voice.is_playing():
        voice.play(discord.FFmpegPCMAudio(path),after=after_playing)
        
def after_playing(err):
    if len(queue) > 1:
        queue.pop(0)
        time.sleep(1)
        play_voice(queue[0])
    else:
        queue.pop(0)
        print('end')

def make_input_text(text):
    userid_pattern = r"<@!(?P<user_id>\d+)>"
    emoji_pattern = r"<:.+:(?P<emoji_id>\d+)>"
    replace_username = re.match(userid_pattern, text)
    replace_emojiname = re.match(emoji_pattern, text)

    if replace_username:
        user_name = client.get_user(int(replace_username.group("user_id"))).name
        text = re.sub(userid_pattern, user_name, text)
        
    if replace_emojiname:
        emoji_name = client.get_emoji(int(replace_emojiname.group("emoji_id"))).name
        text = re.sub(emoji_pattern, emoji_name, text)

    return text

@client.event
async def on_ready():
    print('{0.user}'.format(client)+'としてログインしました。')

@client.event
async def on_message(message):
    global voice
    if message.author == client.user:
        return

    if message.content == "!summon":
        command_ary = message.content.split()
        if len(command_ary) == 1:
            try:
                voice_channel = message.author.voice.channel
                voice = await voice_channel.connect()
            except:
                attention = await message.channel.send('ボイスチャットに入ってから!summonコマンドをつかってください。')
                time.sleep(5)
                await attention.delete()
        else:
            print("hoge")

    if message.content == "!leave":
        try:
            if voice.is_connected():
                await voice.disconnect()
            else:
                attention = await message.channel.send('botはボイスチャンネルに参加していません。')
                time.sleep(5)
                await attention.delete()
        except NameError:
            attention = await message.channel.send('botはボイスチャンネルに参加していません。')
            time.sleep(5)
            await attention.delete()

    if message.content.startswith('!tts'):
        command_ary = message.content.split(' ', maxsplit=1)
        if len(command_ary) > 1 and voice.is_connected():          
            print(command_ary[1])
            text = make_input_text(command_ary[1])
            mp3_path = text2wav.generate_wav(text)
            queue.append(mp3_path)
            play_voice(mp3_path)

        else:
            attention = await message.channel.send('『!tts hogehoge』と入力してください。')
            time.sleep(5)
            await attention.delete()

client.run(TOKEN)

