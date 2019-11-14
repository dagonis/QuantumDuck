"""
Main functionality of QuantumDuck
author: KT (github.com/dagonis)
"""
from abc import ABC

COMMAND_KEY_TABLE = {"DELETE": "X_DELETE", "HOME": "X_HOME", "INSERT": "X_INSERT", "PAGEUP": "X_PGUP", "PAGEDOWN": "X_PGDN", "WINDOWS": "X_LGUI", "GUI": "X_LGUI", "BREAK": "X_PAUSE", "PAUSE": "X_PAUSE", 
                     "UPARROW": "X_UP", "DOWNARROW": "X_DOWN", "LEFTARROW": "X_LEFT", "RIGHTARROW": "X_RIGHT", "TAB": "X_TAB", "END": "X_END", "ESC": "X_ESCAPE", "ESCAPE": "X_ESCAPE", "SPACE": "X_SPACE"}
F_KEY_TABLE = {"F1": "X_F1", "F2": "X_F2", "F3": "X_F3", "F4": "X_F4", "F5": "X_F5", "F6": "X_F6", "F7": "X_F7", "F8": "X_F8", "F9": "X_F9", "F10": "X_F10", "F11": "X_F11", "F12": "X_F12",
               "F13": "X_F13", "F14": "X_F14", "F15": "X_F15", "F16": "X_F16", "F17": "X_F17", "F18": "X_F18", "F19": "X_F19", "F20": "X_F20", "F21": "X_F21", "F22": "X_F22", "F23": "X_F23", "F24": "X_F24"}


class BaseToken(ABC):
    def __init__(self, input_token, repeat=0):
        self.input_token = input_token
        self.repeat = repeat
        self.output_token = self.format_output()

    def format_output(self):
        output_template = '{}'
        stripped_input = ""
        return output_template.format(stripped_input)

    def __str__(self):
        return self.output_token

class Enter(BaseToken):
    def format_output(self):
        return "SEND_STRING(SS_TAP(X_ENTER));"

class ExtendedCommand(BaseToken):
    def format_output(self):
        if self.input_token.strip() in COMMAND_KEY_TABLE:
            return f"SEND_STRING(SS_TAP({COMMAND_KEY_TABLE[self.input_token.strip()]}));"

class Remark(BaseToken):
    def format_output(self):
        output_template = "/* {} */"
        stripped_input = self.input_token.lstrip("REM ")
        return output_template.format(stripped_input)


class Delay(BaseToken):
    def format_output(self):
        output_template = "wait_ms({});"
        stripped_input = self.input_token.lstrip("DELAY ")
        return output_template.format(stripped_input)


class DuckyString(BaseToken):
    def format_output(self):
        output_template = 'SEND_STRING("{}");'
        stripped_input = self.input_token.lstrip("STRING ")
        return output_template.format(stripped_input)


class SuperMod(BaseToken):
    def format_output(self):
        if self.input_token.split(" ")[1] == "SPACE":
            return 'SEND_STRING(SS_LGUI(" "));'
        output_template = 'SEND_STRING(SS_LGUI("{}"));'
        if 'GUI' in self.input_token:
            stripped_input = self.input_token.lstrip("GUI ")
        else:
            stripped_input = self.input_token.lstrip("WINDOWS ")
        return output_template.format(stripped_input)


class ShiftMod(BaseToken):
    def format_output(self):
        key_in = self.input_token.strip().split(" ")[1]
        output_template = f'SEND_STRING(SS_SFT({COMMAND_KEY_TABLE[key_in]}));'
        return output_template

class AltMod(BaseToken):
    def format_output(self):
        key_in = self.input_token.strip().split(" ")[1]
        output_template = 'SEND_STRING(SS_LALT({}));'
        if key_in in COMMAND_KEY_TABLE:
            return output_template.format(COMMAND_KEY_TABLE[key_in])
        elif key_in in F_KEY_TABLE:
            return output_template.format(F_KEY_TABLE[key_in])
        else:
            return output_template.format(f'"{key_in}"')
        return output_template

class CtrlMod(BaseToken):
    def format_output(self):
        key_in = self.input_token.strip().split(" ")[1]
        output_template = 'SEND_STRING(SS_LCTRL({}));'
        if key_in in COMMAND_KEY_TABLE:
            return output_template.format(COMMAND_KEY_TABLE[key_in])
        elif key_in in F_KEY_TABLE:
            return output_template.format(F_KEY_TABLE[key_in])
        else:
            return output_template.format(f'"{key_in}"')
        return output_template

class ArrowKey(BaseToken):
    def format_output(self):
        output_template = 'SEND_STRING({});'
        if self.input_token.startswith('DOWN'):
            return output_template.format(COMMAND_KEY_TABLE["DOWNARROW"])
        elif self.input_token.startswith('UP'):
            return output_template.format(COMMAND_KEY_TABLE["UPARROW"])
        elif self.input_token.startswith('RIGHT'):
            return output_template.format(COMMAND_KEY_TABLE["RIGHTARROW"])
        elif self.input_token.startswith('LEFT'):
            return output_template.format(COMMAND_KEY_TABLE["LEFTARROW"])
        else:
            pass

class DuckScript:
    def __init__(self, commands):
        self.commands = commands

    @classmethod 
    def create_duckscript_object(cls, ducky_script_file):
        commands = []
        duckyscript = open(ducky_script_file, "r").readlines()
        for line in duckyscript:
            line = line.strip()
            if line.startswith("ENTER"):
                commands.append(Enter(line))
            elif line.startswith("REM"):
                commands.append(Remark(line))
            elif line.startswith("DELAY"):
                commands.append(Delay(line))
            elif line.startswith("STRING"):
                commands.append(DuckyString(line))
            elif line.startswith("GUI") or line.startswith("WINDOWS"):
                commands.append(SuperMod(line))
            elif line.startswith("SHIFT"):
                commands.append(ShiftMod(line))
            elif line.startswith("ALT"):
                commands.append(AltMod(line))
            elif line.startswith("CONTROL") or line.startswith("CTRL"):
                commands.append(CtrlMod(line))
            elif line.startswith("UP") or line.startswith("DOWN") or line.startswith("LEFT") or line.startswith("RIGHT"):
                commands.append(ArrowKey(line))
            elif line.strip() in COMMAND_KEY_TABLE:
                commands.append(ExtendedCommand(line))
            else:
                pass
        return DuckScript(commands)

    def __str__(self):
        return "\n".join([_.__str__() for _ in self.commands])

    def full_output(self, name, indent=12):
        print("# This part will go into the process_record_user() function")
        send_string_template = """
        case {}:
          if (record->event.pressed) {{
{}
        }}
        return false;"""
        macro_str = ""
        for command in self.commands:
            macro_str += " " * indent
            macro_str += command.__str__()
            macro_str += "\n"
        print(send_string_template.format(name, macro_str.rstrip()))
        print("\n# This part will go towards the top of your config in your custom_keycodes section")
        keycodes_template = """
        enum custom_keycodes {{
            {}
        }};""".format(name)
        print(keycodes_template)
        print("\nDon't forget to add the key into your keymaps! Happy QuantumQuacking!!!")