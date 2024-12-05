class CNCProcessor:
    def __init__(self):
        self.last_f = 0.0
        self.last_s = 0.0
        self.remaining_x = 0.0
        self.remaining_y = 0.0
        self.pulse = 0.005
        self.max_f = 1000
        self.m_commands = {
            "2": "Ignoring end of gcode",
            "02": "Ignoring end of gcode",
            "4": "Ignoring laser turn-on",
            "04": "Ignoring laser turn-on",
            "5": "Ignoring laser turn-off",
            "05": "Ignoring laser turn-off",
            "3": "Ignoring laser turn-on",
            "03": "Ignoring laser turn-on",
            "9": "Ignoring cooler turn-off",
            "09": "Ignoring cooler turn-off",
            "8": "Ignoring cooler turn-on",
            "08": "Ignoring cooler turn-on",
        }
        self.g_commands = {
            "90": "Error: Absolute positioning detected",
            "91": "Relative positioning detected",
            "17": "Ignoring coordinate plane selection",
            "18": "Ignoring coordinate plane selection",
            "19": "Ignoring coordinate plane selection",
            "20": "Warning: Inch units detected",
            "21": "Ignoring metric unit setting",
            "40": "Ignoring tool compensation off",
            "41": "Error: Tool compensation detected",
            "42": "Error: Tool compensation detected",
            "54": "Ignoring coordinate zeroing",
            "55": "Ignoring coordinate zeroing",
            "56": "Ignoring coordinate zeroing",
            "57": "Ignoring coordinate zeroing",
            "58": "Ignoring coordinate zeroing",
            "59": "Ignoring coordinate zeroing",
        }

    def _extract_parameters(self, line: str):
        x, y, f, s = 0.0, 0.0, self.last_f, self.last_s
        params = {"x": 0.0, "y": 0.0, "f": f, "s": s}
        index = 0
        length = len(line)

        while index < length:
            char = line[index].lower()
            index += 1
            if char in params and index < length:
                start_index = index
                while index < length and (
                    line[index].isdigit() or line[index] in ".+-"
                ):
                    index += 1
                value_str = line[start_index:index]
                if value_str:
                    params[char] = float(value_str)
            else:
                continue

        return params

    def _adjust_coordinates(self, x, y):
        x = x + self.remaining_x
        y = y + self.remaining_y
        round_x = round(x / self.pulse)
        round_y = round(y / self.pulse)
        self.remaining_x = x - (round_x * self.pulse)
        self.remaining_y = y - (round_y * self.pulse)
        return round_x, round_y

    def extract_g0_parameters(self, line: str, output_file):
        params = self._extract_parameters(line)
        if self.last_s != 0:
            output_file.write(f"CNC.laser_power(0)\n")
            self.last_s = 0
        round_x, round_y = self._adjust_coordinates(params["x"], params["y"])
        output_file.write(f"CNC.linear_move({round_x}, {round_y}, {self.max_f})\n")

    def extract_g1_parameters(self, line: str, output_file):
        params = self._extract_parameters(line)
        if self.last_s != params["s"]:
            output_file.write(f"CNC.laser_power({params['s']})\n")
            self.last_s = params["s"]
        if self.last_f != params["f"]:
            self.last_f = params["f"]
        round_x, round_y = self._adjust_coordinates(params["x"], params["y"])
        output_file.write(f"CNC.linear_move({round_x}, {round_y}, {params['f']})\n")

    def process_line(self, line: str, output_file):
        line = line.strip()
        while line:
            command_type = line[0].lower()
            code = line[1:3] if len(line) > 2 and line[2].isdigit() else line[1]
            if command_type == "m":
                message = self.m_commands.get(code, f"Unknown M code: {code}")
                print(message)
                line = line[len(code) + 1 :]
            elif command_type == "g":
                if code in ["0", "00"]:
                    print("Writing G00 command to output file")
                    index = len(code) + 1
                    length = len(line)
                    while index < length:
                        char = line[index]
                        if char not in ["g", "G", "m", "M", ";"]:
                            index += 1
                        else:
                            break
                    self.extract_g0_parameters(line[len(code) + 1 : index], output_file)
                    line = line[index:]
                elif code in ["1", "01"]:
                    print("Writing G01 command to output file")
                    index = len(code) + 1
                    length = len(line)
                    while index < length:
                        char = line[index]
                        if char not in ["g", "G", "m", "M", ";"]:
                            index += 1
                        else:
                            break
                    self.extract_g1_parameters(line[len(code) + 1 : index], output_file)
                    line = line[index:]
                else:
                    message = self.g_commands.get(code, f"Unknown G code: {code}")
                    print(message)
                    line = line[len(code) + 1 :]
            elif command_type == ";":
                output_file.write(f"#{line[1:]}\n")
                line = ""
            else:
                print(f"ERROR - unknown line:{line}")
                line = ""
