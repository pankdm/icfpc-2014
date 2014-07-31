import sys

input_filename = sys.argv[1]
output_filename = sys.argv[2]

labels = {}

def get_number_of_commands(command):
    if command.startswith("call_"):
        return 2
    else:
        return 1

def process_command(command):
    parts = command.split(' ')
    final_command = ""
    if command.startswith("call_"):
        final_command = "ldf " + labels[parts[0][5:]] + "\nap " + parts[1]
    else:
        for part in parts:
            if part.startswith("goto_"):
                part = labels[part[5:]]

            if final_command:
                final_command = final_command + " "
            final_command = final_command + part
    return final_command.upper()

commands = []
line_id = 0
for line in open(input_filename, "r").readlines():
    no_comment_line = line.split(";")[0].lower()
    if no_comment_line.find(":") == -1:
        command = no_comment_line
    else:
        # Contain label
        label, command = no_comment_line.split(":")
        if label in labels:
            raise "Label redeclaration + " + label
        labels[label] = str(line_id)
    command = command.strip()
    if command:
        commands.append(command)
        line_id = line_id + get_number_of_commands(command)

output = open(output_filename, "w")
for command in commands:
    print >> output, process_command(command)
