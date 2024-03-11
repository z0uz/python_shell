import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import print_formatted_text, HTML

# Custom completer for dynamic tab completion
class PathCompleter(Completer):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        current_path = os.path.abspath(os.path.expanduser(word_before_cursor))

        # If the path ends with a separator, or if it's an empty string, list contents of the directory
        if word_before_cursor.endswith(os.sep) or not word_before_cursor:
            dirname, rest = os.path.split(current_path)

            if not os.path.exists(dirname):
                return

            for filename in os.listdir(dirname):
                full_path = os.path.join(dirname, filename)
                if os.path.isdir(full_path) and filename.startswith(rest):
                    yield Completion(filename + os.sep, -len(rest))
                elif filename.startswith(rest):
                    yield Completion(filename, -len(rest))
        else:
            dirname, rest = os.path.split(current_path)

            if not os.path.exists(dirname):
                return

            for filename in os.listdir(dirname):
                full_path = os.path.join(dirname, filename)
                if os.path.isdir(full_path) and filename.startswith(rest):
                    yield Completion(filename + os.sep, -len(rest))
                elif filename.startswith(rest):
                    yield Completion(filename, -len(rest))


# Define functions for your basic shell implementation

def parse_input(input_str):
    # Function to parse user input
    return input_str.strip().split()


def execute_command(command):
    # Function to execute commands
    if command[0] == 'exit':
        print("Exiting shell.")
        exit()
    elif command[0] == 'cd':
        if len(command) > 1:
            try:
                os.chdir(command[1])
            except FileNotFoundError:
                print("Directory not found.")
        else:
            print("Usage: cd <directory>")
    else:
        try:
            os.system(" ".join(command))
        except Exception as e:
            print("Error executing command:", e)


def main():
    print("Welcome to the Simple Shell!")
    while True:
        user_input = prompt('$ ',
                            completer=PathCompleter(),
                            complete_while_typing=True)
        if user_input:
            command = parse_input(user_input)
            execute_command(command)


if __name__ == "__main__":
    main()
