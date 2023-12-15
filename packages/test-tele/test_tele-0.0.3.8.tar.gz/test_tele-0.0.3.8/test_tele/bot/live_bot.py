"""A bot to controll settings for tgcf live mode."""

import logging
import re
import yaml

from telethon import events, Button
from telethon.tl import types

from test_tele import config
from test_tele import config_bot
from test_tele.bot.bot_header import get_entity, send_grouped_messages, forward_group_messages, start_sending
from test_tele.bot.utils import (
    admin_protect,
    display_forwards,
    get_args,
    get_command_prefix,
    get_command_suffix,
    remove_source
)
from test_tele.config import CONFIG, write_config
from test_tele.config_bot import BOT_CONFIG, write_bot_config
from test_tele.plugin_models import Style
from test_tele.plugins import TgcfMessage


@admin_protect
async def forward_command_handler(event):
    """Handle the `/forward` command."""
    notes = """The `/forward` command allows you to add a new forward.
    Example: suppose you want to forward from a to (b and c)

    ```
    /forward source: a
    dest: [b,c]
    ```

    a,b,c are chat ids

    """.replace(
        "    ", ""
    )

    try:
        args = get_args(event.message.text)
        if not args:
            raise ValueError(f"{notes}\n{display_forwards(config.CONFIG.forwards)}")

        parsed_args = yaml.safe_load(args)
        forward = config.Forward(**parsed_args)
        try:
            remove_source(forward.source, config.CONFIG.forwards)
        except:
            pass
        CONFIG.forwards.append(forward)
        config.from_to, config.reply_to = await config.load_from_to(event.client, config.CONFIG.forwards)

        await event.respond("Success")
        write_config(config.CONFIG)
    except ValueError as err:
        logging.error(err)
        await event.respond(str(err))

    finally:
        raise events.StopPropagation


@admin_protect
async def remove_command_handler(event):
    """Handle the /remove command."""
    notes = """The `/remove` command allows you to remove a source from forwarding.
    Example: Suppose you want to remove the channel with id -100, then run

    `/remove source: -100`

    """.replace(
        "    ", ""
    )

    try:
        args = get_args(event.message.text)
        if not args:
            raise ValueError(f"{notes}\n{display_forwards(config.CONFIG.forwards)}")

        parsed_args = yaml.safe_load(args)
        source_to_remove = parsed_args.get("source")
        CONFIG.forwards = remove_source(source_to_remove, config.CONFIG.forwards)
        config.from_to, config.reply_to = await config.load_from_to(event.client, config.CONFIG.forwards)

        await event.respond("Success")
        write_config(config.CONFIG)
    except ValueError as err:
        logging.error(err)
        await event.respond(str(err))

    finally:
        raise events.StopPropagation


@admin_protect
async def style_command_handler(event):
    """Handle the /style command"""
    notes = """This command is used to set the style of the messages to be forwarded.

    Example: `/style bold`

    Options are preserve,normal,bold,italics,code, strike

    """.replace(
        "    ", ""
    )

    try:
        args = get_args(event.message.text)
        if not args:
            raise ValueError(f"{notes}\n")
        _valid = [item.value for item in Style]
        if args not in _valid:
            raise ValueError(f"Invalid style. Choose from {_valid}")
        CONFIG.plugins.fmt.style = args
        await event.respond("Success")
        write_config(CONFIG)
    except ValueError as err:
        logging.error(err)
        await event.respond(str(err))

    finally:
        raise events.StopPropagation


async def start_command_handler(event):
    """Handle the /start command"""

    if not event.message.chat_id in [item.user_id for item in BOT_CONFIG.user_cfg]:
        user_cfg = config_bot.UserBot(user_id=event.message.chat_id)
        BOT_CONFIG.user_cfg.append(user_cfg)
        write_bot_config(config_bot.BOT_CONFIG)

    await event.respond(BOT_CONFIG.bot_messages.start)


async def help_command_handler(event):
    """Handle the /help command."""
    await event.respond(BOT_CONFIG.bot_messages.bot_help)


async def get_message_command_handler(event):
    """Handle the command /get"""
    notes = """This command is used to get the messages from public channel or group.

    Command: `/get`
    Usage: LINK..
    Note: copy the message link from the public channel or group, and paste it here as argument
    
    **Example** 
    `/get https://t.me/username/post_id`
    """.replace("    ", "")

    try:
        args = get_args(event.message.text)

        if not args:
            raise ValueError(f"{notes}\n")

        # pattern = r'(t.me/c/?)?(\-?\w+)?/(\d+)'
        pattern = r'(t.me/(c/)?|)(-?\w+)/(\d+)'
        match = re.search(pattern, args)

        tm = TgcfMessage(event.message)

        if match:
            entity = str(match.group(3))
            ids = int(match.group(4))
            chat = await get_entity(event, entity)

            if chat is None:
                raise ValueError("Unable to get post")

            message = await event.client.get_messages(chat, ids=ids)
            
            tm.text = message.message + f'\n\nForwarded by {BOT_CONFIG.bot_name}'
            tm.new_file = message.media
            tm.reply_to = event.message.id

            if message.grouped_id is not None and message.media:
                try:
                    await send_grouped_messages(chat, tm, message, ids)
                except:
                    await forward_group_messages(chat, tm, message, ids)
            else:
                await start_sending(tm.message.chat_id, tm)

    except ValueError as err:
        logging.error(err)
        await event.respond(str(err))

    finally:
        raise events.StopPropagation


async def get_id_command_handler(event):
    """Handle the /id command"""

    try:
        args = get_args(event.message.text)

        if not args and CONFIG.login.user_type == 1:
            tm = TgcfMessage(event.message)
            tm.text = ""
            i = 0

            async for dialog in event.client.iter_dialogs():
                if dialog.is_channel:
                    i += 1
                    if i <= 80:
                        ch_id = f"`{str(dialog.id)}`"
                        ch_name = str(dialog.name).replace("`", "'")
                        tm.text += ch_id + " 👉 " + ch_name + "\n"
                    else:
                        await start_sending(tm.message.chat_id, tm)
                        tm.text = ""
                        i = 0
            
            await start_sending(tm.message.chat_id, tm)

        message = await event.message.get_reply_message()
        await event.respond(f"```{message.stringify()}```")

    except Exception as err:
        logging.warning(err)
        message = await event.message.get_reply_message()
        await event.respond(f"```{message.stringify()}```")

    finally:
        raise events.StopPropagation


async def report_command_handler(event):
    """Handle the /report command"""
    notes = """The `/report` command allows you to send a message to the bot Admin.

    Command: `/report`
    Usage: MESSAGE..

    **Example**
    `/report Bot is not responding. Not sure if you received this or not.. lol`
    """.replace(
        "    ", ""
    )

    try:
        args = get_args(event.message.text)
        if not args:
            raise ValueError(f"{notes}\n")
        
        tm = TgcfMessage(event.message)
        tm.text = args
        tm.text += f"\n from: `{tm.message.chat_id}`\n#report"

        await start_sending(CONFIG.admins[0], tm)
        await event.respond("We have received your message. Please wait while the Admin attempts to fix it")
        
    except ValueError as err:
        await event.respond(str(err))
    finally:
        raise events.StopPropagation


@admin_protect
async def respond_command_handler(event):
    """Handle the /respond_to command handler"""
    
    try:
        args = get_args(event.message.text)
        if not args:
            return

        tm = TgcfMessage(event.message)
        id_user, isi_pesan = re.match(r'(\d+)\s(.+)', args).groups()

        tm.text = f'Admin says: "{isi_pesan}"'
        await start_sending(int(id_user), tm)

    except Exception as err:
        logging.warning(err)
    finally:
        raise events.StopPropagation


@admin_protect
async def pixiv_downloader(event):
    """Handle the pixiv command"""
    import shlex
    import asyncio
    import json

    try:
        await event.respond("bisa")
        
        tm = TgcfMessage(event.message)
        tm.text = ""

        command = shlex.split(f"gallery-dl {event.message.text} --config-ignore -c config/config.json -j --range 1-5")
        # print(*command)

        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await process.communicate()

        if stderr:
            print(stderr.decode())
        else:
            links = []
            result = json.loads(stdout.decode())

            for elemen in result:
                if elemen[0] == 3:
                    links.append(elemen[1])
                    # tm.text += elemen[1] + "\n"
            
            tm.new_file = links
            await start_sending(tm.message.chat_id, tm)


    except Exception as err:
        logging.warning(err)
        message = await event.message.get_reply_message()
        await event.respond(f"```{message.stringify()}```")

    finally:
        raise events.StopPropagation

   

# async def download_deez_command_handler(event):
#     """Handle the /dd command"""
#     notes = """
#     **Usage**

#     Command: `/dd`
#     Usage: URL.. [OPTION].. 

#     **Option**
#     `-o INT` : Offset, will start from n+1 of images
#     `-r INT` : Range, number of images

#     **Example**
#     `/dd https://example.com/test -r 3`
#     `/dd https://example.com/test -o 3`
#     `/dd https://example.com/test -o 3 -r 3`

#     """.replace(
#         "    ", ""
#     )

#     try:
#         args = get_args(event.message.text)
#         if not args:
#             raise ValueError(f"{notes}\n")

#         url, opsi = await get_link_text(args)

#         if url:
#             opt = []
#             if opsi['args']:
#                 for item in opsi['args']:
#                     opt.append(item)
            
#             if 'r' in opsi:
#                 opt.append(f"r({opsi['r']})") 
#             if 'o' in opsi:
#                 opt.append(f"o({opsi['o']})") 

#             auto_respond = await event.respond(
#                 f'URL: {url}\nOption: {(", ").join(opt) if opt else "none"}\nProcessing...')
            
#             tm = TgcfMessage(event.message)
#             tm.reply_to = tm.message.id
#             await start_download(
#                 event.message.chat_id, tm, url=url, opt=opsi, msg_res=auto_respond
#             )

#     except ValueError as err:
#         logging.error(err)
#         await event.respond(str(err))

#     finally:
#         raise events.StopPropagation
    


def get_events(val): # tambah argumen
    logging.info(f"Command prefix is . for userbot and / for bot")
    _ = get_command_prefix(val)
    u = get_command_suffix(val)
    command_events = {
        "start": (start_command_handler, events.NewMessage(pattern=f"{_}start{u}")),
        "forward": (forward_command_handler, events.NewMessage(pattern=f"{_}forward")),
        "remove": (remove_command_handler, events.NewMessage(pattern=f"{_}remove")),
        "style": (style_command_handler, events.NewMessage(pattern=f"{_}style")),
        "help": (help_command_handler, events.NewMessage(pattern=f"{_}help{u}")),
        "get_post": (get_message_command_handler, events.NewMessage(pattern=f"{_}get")),
        "get_id": (get_id_command_handler, events.NewMessage(pattern=f"{_}id{u}")),
    }
    if val == 0: # bot
        khusus_bot= {
            "report": (report_command_handler, events.NewMessage(pattern=f"{_}report")),
            "respond": (respond_command_handler, events.NewMessage(pattern=f"{_}respond")),
            "test": (pixiv_downloader, events.NewMessage(pattern=r'((.+\.pixiv\.\w{3}).+)')),
    #         "get_test": (get_test_command_handler, events.NewMessage(outgoing=True)),
        }
        command_events.update(khusus_bot)

    return command_events
