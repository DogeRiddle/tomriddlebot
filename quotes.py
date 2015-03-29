__module_name__ = "Quotes"
__module_version__ = "0.1"
__module_description__ = "Quotescript for HexChat by cr5315"

import os
import random
import hexchat

TRIGGER  = "!"
FILE_NAME = "quotes-%s.txt"

CAN_EDIT_QUOTES = ["uid45119@gateway/web/irccloud.com/x-pkcomdjihcrstrvk", "dbrown@104.236.218.170"
]

# Channels in this list are exempt from the quote script
DO_NOT_QUOTE = ["#dogecoin", "#TomRiddle"]

def chan_trig(word, woerd_eol, userdata):
    # Strip input word

    word = [hexchat.strip(x, -1, 3) for x in word]
    
    user = word[0]
    trigger = word[1][0]
    
    command = (word[1][1:].strip()).split()
    
    if trigger == TRIGGER:
        channel = hexchat.get_info("channel")
        file_path = os.path.join(hexchat.get_info("configdir"), "addons", FILE_NAME % channel)
        
        # add quote
        if command[0] == "addquote" and channel not in DO_NOT_QUOTE:
            users = hexchat.get_list("users")
            for u in users:
                if u.nick == user:
                    if u.host in CAN_EDIT_QUOTES:
                        with open(file_path, "a") as f:
                            f.write(" ".join(command[1:]) + "\n")
                
                        hexchat.command("msg %s %s" % (channel, "Quote added."))
            
            return hexchat.EAT_NONE
        
        elif command[0] == "delquote" and channel not in DO_NOT_QUOTE:
            users = hexchat.get_list("users")
            for u in users:
                if u.nick == user:
                    if u.host in CAN_EDIT_QUOTES:
            
                        try:
                            fn = open(file_path, "r")
                        except:
                            hexchat.command("msg %s %s" % (channel, "Please add a quote first."))
                            return hexchat.EAT_NONE
            
                        lines = fn.readlines()
                        MAX = len(lines)
                        fn.close()
            
                        try:
                            number = int(command[1])
                        except:
                            hexchat.command("msg %s %s" % (channel, "I'm not sure which quote you would like to delete."))
                            return hexchat.EAT_NONE
                
                        old = lines.pop(number - 1)
            
                        try:
                            fout = open(file_path, "w")
                            for line in lines:
                                fout.write(line)
            
                            fout.close()
                            hexchat.command("msg %s %s" % (channel, "Quote %d deleted." % number))
                            return hexchat.EAT_NONE
                        except:
                            hexchat.command("msg %s %s" % (channel, "Unable to open quote file."))
                            return hexchat.EAT_NONE
        
        elif command[0] == "quote" and channel not in DO_NOT_QUOTE:
            try:
                fn = open(file_path, "r")
            except:
                hexchat.command("msg %s %s" % (channel, "Please add a quote first."))
                return hexchat.EAT_NONE
            
            lines = fn.readlines()
            MAX = len(lines)
            fn.close()
            random.seed()
            try:
                number = int(command[1])
                if number < 0:
                    number = MAX - abs(number) + 1
            except:
                try:
                    number = random.randint(1, MAX)
                except:
                    hexchat.command("msg %s %s" % (channel, "Please add a quote first."))
                    return hexchat.EAT_NONE
            if not (0 <= number <= MAX):
                hexchat.command("msg %s %s" % (channel, "I'm not sure which quote you would like to see."))
            else:
                line = lines[number - 1]
                hexchat.command("msg %s Quote %s of %s: %s" % (channel, str(number), str(MAX), line))
                return hexchat.EAT_NONE
                
hexchat.hook_print("Channel Message", chan_trig)
