class GcodeParser:
    """
    A class used to parse G-code files and generate corresponding CNC commands.

    Attributes
    ----------
    last_f : float
        Last known feed rate.
    last_s : float
        Last known spindle speed.
    remaining_x : float
        Remaining distance in X direction.
    remaining_y : float
        Remaining distance in Y direction.
    pulse : float
        Duration of a single pulse (in seconds).
    max_f : int
        Maximum feed rate.
    m_commands : dict
        Dictionary of M commands and their corresponding messages.
    g_commands : dict
        Dictionary of G commands and their corresponding messages.

    Methods
    -------
    _extract_parameters(line: str) -> dict
        Extract parameters from a G-code line.
    _adjust_coordinates(x: float, y: float) -> tuple
        Adjust and round the input coordinates based on the pulse duration.
    extract_g0_parameters(line: str, output_file: file)
        Extract G0 (rapid positioning) parameters from a G-code line and write corresponding CNC commands.
    extract_g1_parameters(line: str, output_file: file)
        Extract G1 (linear interpolation) parameters from a G-code line and write corresponding CNC commands.
    process_line(line: str, output_file: file)
        Process a single line of G-code and write corresponding CNC commands to the output file.
    parser(input_file: str, output_file: str)
        Parse a G-code file and write corresponding CNC commands to an output file.
    """

    def __init__(self):
        """
        Initialize the GcodeParser object.

        This method sets up the initial state of the GcodeParser, including:
        - Last known feed rate and spindle speed
        - Remaining distance in X and Y directions
        - Pulse duration and maximum feed rate
        - Dictionaries for M and G commands with their corresponding actions or messages

        Parameters:
        None

        Returns:
        None

        Attributes:
        last_f (float): Last known feed rate
        last_s (float): Last known spindle speed
        remaining_x (float): Remaining distance in X direction
        remaining_y (float): Remaining distance in Y direction
        pulse (float): Duration of a single pulse (in seconds)
        max_f (int): Maximum feed rate
        m_commands (dict): Dictionary of M commands and their corresponding messages
        g_commands (dict): Dictionary of G commands and their corresponding messages
        """
        self.last_f = 0.0
        self.last_s = 0.0
        self.remaining_x = 0.0
        self.remaining_y = 0.0
        self.pulse = 0.02
        self.max_f = 20
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
        """
        Extract parameters from a G-code line.

        This method parses a G-code line and extracts the x, y, f (feed rate),
        and s (spindle speed) parameters. If a parameter is not present in the line,
        it uses the last known value or a default of 0.0.

        Parameters:
        line (str): A single line of G-code to parse.

        Returns:
        dict: A dictionary containing the extracted parameters:
              'x': X-coordinate (float)
              'y': Y-coordinate (float)
              'f': Feed rate (float)
              's': Spindle speed (float)

        Note:
        - The method is case-insensitive.
        - It handles decimal numbers and numbers with signs (+ or -).
        - If a parameter is not found in the line, it uses the last known value
          (stored in self.last_f and self.last_s) or defaults to 0.0.
        """
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
        """
        Adjust and round the input coordinates based on the pulse duration.

        This method adjusts the input coordinates by adding any remaining distance
        from previous operations, then rounds the result based on the pulse duration.
        It also updates the remaining distance for future operations.

        Parameters:
        x (float): The input X-coordinate to be adjusted.
        y (float): The input Y-coordinate to be adjusted.

        Returns:
        tuple: A tuple containing two integers:
            - round_x (int): The adjusted and rounded X-coordinate.
            - round_y (int): The adjusted and rounded Y-coordinate.
        """
        x = x + self.remaining_x
        y = y + self.remaining_y
        round_x = round(x / self.pulse)
        round_y = round(y / self.pulse)
        self.remaining_x = x - (round_x * self.pulse)
        self.remaining_y = y - (round_y * self.pulse)
        return round_x, round_y

    def extract_g0_parameters(self, line: str, output_file):
        """
        Extract G0 (rapid positioning) parameters from a G-code line and write corresponding CNC commands.

        This method processes a G0 command line, extracts its parameters, adjusts coordinates,
        and writes the appropriate CNC commands to the output file. It also handles laser power
        adjustment if necessary.

        Parameters:
        line (str): The G-code line containing G0 command parameters.
        output_file (file): The file object to which CNC commands will be written.

        Returns:
        None

        Side effects:
        - Writes CNC commands to the output_file.
        - Updates self.last_s (last spindle speed) if changed.
        """
        params = self._extract_parameters(line)
        if self.last_s != 0:
            output_file.write(f"CNC.laser_power(0)\n")
            self.last_s = 0
        round_x, round_y = self._adjust_coordinates(params["x"], params["y"])
        output_file.write(f"CNC.linear_move({round_x}, {round_y}, {self.max_f})\n")

    def extract_g1_parameters(self, line: str, output_file):
        """
        Extract G1 (linear interpolation) parameters from a G-code line and write corresponding CNC commands.

        This method processes a G1 command line, extracts its parameters, adjusts coordinates,
        and writes the appropriate CNC commands to the output file. It also handles laser power
        and feed rate adjustments if necessary.

        Parameters:
        line (str): The G-code line containing G1 command parameters.
        output_file (file): The file object to which CNC commands will be written.

        Returns:
        None

        Side effects:
        - Writes CNC commands to the output_file.
        - Updates self.last_s (last spindle speed) and self.last_f (last feed rate) if changed.
        """
        params = self._extract_parameters(line)
        if self.last_s != params["s"]:
            output_file.write(f"CNC.laser_power({params['s']})\n")
            self.last_s = params["s"]
        if self.last_f != params["f"]:
            self.last_f = params["f"]
        round_x, round_y = self._adjust_coordinates(params["x"], params["y"])
        output_file.write(f"CNC.linear_move({round_x}, {round_y}, {params['f']})\n")

    def process_line(self, line: str, output_file):
        """
        Process a single line of G-code and write corresponding CNC commands to the output file.

        This method interprets the G-code line, identifies the command type (G or M), and processes
        it accordingly. It extracts parameters for G0 and G1 commands and writes the appropriate
        CNC commands to the output file. It also handles comments and unknown commands.

        Parameters:
        line (str): A single line of G-code to be processed.
        output_file (file): The file object to which CNC commands will be written.

        Returns:
        None

        Side effects:
        - Writes CNC commands or comments to the output_file.
        - Prints messages for known and unknown M and G codes.
        """
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


def parser(self, input_file, output_file):
    """
    Parse a G-code file and write corresponding CNC commands to an output file.

    This function reads a G-code file line by line, processes each line using
    the GcodeParser class, and writes the resulting CNC commands to the specified
    output file.

    Parameters:
    input_file (str): The path to the input G-code file to be parsed.
    output_file (str): The path to the output file where CNC commands will be written.

    Returns:
    None
    """
    gcode_parser = GcodeParser()
    with open(input_file, "r") as file:
        with open(output_file, "w") as output:
            for line in file:
                gcode_parser.process_line(line, output)
