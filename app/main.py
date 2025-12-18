# import sys
# import shutil
# import subprocess
# import os
# import shlex
# import readline

# # ------------------------------
# # Builtins
# # ------------------------------

# def builtin_exit(args):
#     sys.exit(0)

# def builtin_cd(args):
#     path = os.path.expanduser(args[0]) if args else os.path.expanduser("~")
#     try:
#         os.chdir(path)
#     except FileNotFoundError:
#         print(f"cd: {args[0]}: No such file or directory")
#     except NotADirectoryError:
#         print(f"cd: {args[0]}: Not a directory")
#     except PermissionError:
#         print(f"cd: {args[0]}: Permission denied")

# def builtin_pwd(args):
#     print(os.getcwd())

# def builtin_echo(args):
#     print(" ".join(args))

# def builtin_type(args):
#     if not args:
#         print("")
#         return

#     target = args[0]
#     if target in BUILTINs:
#         print(f"{target} is a shell builtin")
#         return

#     path = shutil.which(target)
#     if path:
#         print(f"{target} is {path}")
#         return

#     print(f"{target}: not found")

# BUILTINs = {
#     "exit": builtin_exit,
#     "echo": builtin_echo,
#     "type": builtin_type,
#     "pwd": builtin_pwd,
#     "cd": builtin_cd,
# }
# BUILTINS_LITS = ["echo","exit","type","pwd","cd"]

# last_perfix = ""
# tab_press_count = 0
# cached_matches = []

# # ------------------------------
# # Redirection parser
# # ------------------------------

# # COMMAND = ["echo", "exit"]
# COMMAND = list(BUILTINs.keys())

# # def completer(text, state):
    
# #     global last_perfix, tab_press_count, cached_matches

# #     if text != last_perfix:
# #         tab_press_count = 0
# #         cached_matches = []
# #         last_perfix = text

# #     if not cached_matches:
# #         list_execs = list_executables_in_path()
# #         list_execs.update(BUILTINS_LITS)
# #         cached_matches = sorted(cmd for cmd in list_execs if cmd.startswith(text))

# #     if not cached_matches:
# #         return None
    
# #     if len(cached_matches) == 1:
# #         return cached_matches[0] + " "
    
# #     # if state < len(cached_matches):
# #     #     return cached_matches[state] + " "
    
# #     if  tab_press_count == 0:
# #         sys.stdout.write("\x07")
# #         sys.stdout.flush()
# #         tab_press_count = 1
# #         return None
    

    
# #     if tab_press_count == 1:
# #         sys.stdout.write("\n")
# #         sys.stdout.write("  ".join((cached_matches)))
# #         sys.stdout.write("\n$ " + text)
# #         sys.stdout.flush()
# #         tab_press_count = 0
# #         return None


# #     return None
    

# # def completer(text, state):
# #     global last_perfix, cached_matches

# #     # Reset cache if prefix changes
# #     if text != last_perfix:
# #         last_perfix = text
# #         cached_matches = []

# #     # Compute matches once
# #     if not cached_matches:
# #         execs = set(list_executables_in_path())
# #         execs.update(BUILTINS_LITS)
# #         cached_matches = sorted(cmd for cmd in execs if cmd.startswith(text))

# #     if not cached_matches:
# #         return None

# #     # Multiple matches → ring bell on first TAB
# #     if len(cached_matches) > 1 and state == 0:
# #         return "\x07"

# #     # Let readline handle cycling / second TAB
# #     if state < len(cached_matches):
# #         return cached_matches[state] + " "

# #     return None


# def completer(text, state):
#     global last_perfix, tab_press_count, cached_matches

#     if text != last_perfix:
#         tab_press_count = 0
#         cached_matches = []
#         last_perfix = text

#     if not cached_matches:
#         list_execs = set(list_executables_in_path())
#         list_execs.update(BUILTINS_LITS)
#         cached_matches = sorted(cmd for cmd in list_execs if cmd.startswith(text))

#     if not cached_matches:
#         return None

#     # ✅ Single match → complete immediately
#     if len(cached_matches) == 1:
#         if state == 0:
#             return cached_matches[0] + " "
#         return None
#     # 🔔 First TAB with multiple matches → bell only
#     if tab_press_count == 0:
#         sys.stdout.write("\x07")
#         sys.stdout.flush()
#         tab_press_count = 1
#         return None

#     # ✅ Multiple matches → return RAW candidates (NO SPACE)
#     if state < len(cached_matches):
#         return cached_matches[state]

#     return None

   
# def display_matches_hook(substitution, matches, longest_match_length):
#     sys.stdout.write("\n")
#     sys.stdout.write("  ".join(sorted(matches)))
#     sys.stdout.write("\n$ " + readline.get_line_buffer())
#     sys.stdout.flush()



# # def display_matches_hook(substitution, matches, longest_match_length):
# #     # Called automatically by readline on second TAB
# #     sys.stdout.write("\n")
# #     sys.stdout.write("  ".join(sorted(matches)))
# #     sys.stdout.write("\n$ " + readline.get_line_buffer())
# #     sys.stdout.flush()


# def list_executables_in_path():
#     executables = set()
#     for dir_path in os.environ.get("PATH", "").split(os.pathsep):
#         if not os.path.isdir(dir_path):
#             continue
#         try:
#             for file in os.listdir(dir_path):
#                 full_path = os.path.join(dir_path, file)
#                 if os.access(full_path, os.X_OK) and os.path.isfile(full_path):
#                     executables.add(file)
#         except PermissionError:
#             continue
#     return list(executables)    

# def get_executables():
#     executables = set()
#     for dir_path in os.environ.get("PATH", "").split(os.pathsep):
#         if not os.path.isdir(dir_path):
#             continue
#         for file in os.listdir(dir_path):
#             full_path = os.path.join(dir_path, file)
#             if os.access(full_path, os.X_OK) and not os.path.isdir(full_path):
#                 executables.add(file)

#     return list(executables)


# def parse_redirection(parts):
#     """
#     Detects:
#         cmd args > file, 1> file, >> file, 1>> file, 2> file
#     Returns:
#         clean_parts, stdout_file, stderr_file, stdout_append
#     """
#     stdout_file = None
#     stderr_file = None
#     stdout_append = False
#     stderr_append = False
#     clean_parts = []

#     i = 0
#     while i < len(parts):
#         tok = parts[i]

#         # stdout overwrite
#         if tok in [">", "1>"] and i + 1 < len(parts):
#             stdout_file = parts[i + 1]
#             stdout_append = False
#             i += 2
#             continue

#         # stdout append
#         if tok in [">>", "1>>"] and i + 1 < len(parts):
#             stdout_file = parts[i + 1]
#             stdout_append = True
#             i += 2
#             continue

#         # stderr overwrite
#         if tok == "2>" and i + 1 < len(parts):
#             stderr_file = parts[i + 1]
#             stderr_append = False
#             i += 2
#             continue

#         if tok == "2>>" and i + 1 < len(parts):
#             stderr_file = parts[i + 1]
#             stderr_append = True
#             i += 2
#             continue

#         # normal token
#         clean_parts.append(tok)
#         i += 1

#     return clean_parts, stdout_file, stderr_file, stdout_append, stderr_append

# # ------------------------------
# # Main shell loop
# # ------------------------------

# def main():
    
#     readline.set_completer(completer)
#     readline.set_completion_display_matches_hook(display_matches_hook)
#     readline.parse_and_bind("tab: complete")
#     while True:
#         sys.stdout.write("$ ")
#         sys.stdout.flush()
#         try:
#             command = input().strip()
#         except EOFError:
#             print()
#             break

#         if not command:
#             continue

#         parts = shlex.split(command)
#         parts, stdout_file, stderr_file, stdout_append, stderr_append = parse_redirection(parts)

#         if not parts:
#             continue

#         cmd = parts[0]
#         args = parts[1:]



#         # Builtins
#         if cmd in BUILTINs:
#             save_stdout = sys.stdout
#             save_stderr = sys.stderr
#             try:
#                 if stdout_file:
#                     sys.stdout = open(stdout_file, "a" if stdout_append else "w")
#                 if stderr_file:
#                     sys.stderr = open(stderr_file, "a" if stderr_append else "w")
#                 BUILTINs[cmd](args)
#             finally:
#                 if stdout_file:
#                     sys.stdout.close()
#                 if stderr_file:
#                     sys.stderr.close()
#                 sys.stdout = save_stdout
#                 sys.stderr = save_stderr
#             continue

#         # External commands
#         path = shutil.which(cmd)
#         if path:
#             stdout_target = open(stdout_file, "a" if stdout_append else "w") if stdout_file else None
#             stderr_target = open(stderr_file, "a" if stderr_append else "w") if stderr_file else None

#             subprocess.run([cmd] + args, stdout=stdout_target, stderr=stderr_target)

#             if stdout_target:
#                 stdout_target.close()
#             if stderr_target:
#                 stderr_target.close()
#             continue

#         # Unknown command
#         print(f"{command}: command not found", file=sys.stderr)


# if __name__ == "__main__":
#     main()














# import sys
# import shutil
# import subprocess
# import os
# import shlex
# import readline

# # ------------------------------
# # Builtins
# # ------------------------------

# def builtin_exit(args):
#     sys.exit(0)

# def builtin_cd(args):
#     path = os.path.expanduser(args[0]) if args else os.path.expanduser("~")
#     try:
#         os.chdir(path)
#     except FileNotFoundError:
#         print(f"cd: {args[0]}: No such file or directory")
#     except NotADirectoryError:
#         print(f"cd: {args[0]}: Not a directory")
#     except PermissionError:
#         print(f"cd: {args[0]}: Permission denied")

# def builtin_pwd(args):
#     print(os.getcwd())

# def builtin_echo(args):
#     print(" ".join(args))

# def builtin_type(args):
#     if not args:
#         print("")
#         return

#     target = args[0]
#     if target in BUILTINs:
#         print(f"{target} is a shell builtin")
#         return

#     path = shutil.which(target)
#     if path:
#         print(f"{target} is {path}")
#         return

#     print(f"{target}: not found")

# BUILTINs = {
#     "exit": builtin_exit,
#     "echo": builtin_echo,
#     "type": builtin_type,
#     "pwd": builtin_pwd,
#     "cd": builtin_cd,
# }

# BUILTINS_LITS = ["echo", "exit", "type", "pwd", "cd"]

# # ------------------------------
# # Completion state
# # ------------------------------

# last_prefix = ""
# cached_matches = []

# # ------------------------------
# # ✅ NEW: Longest Common Prefix
# # ------------------------------

# def longest_common_prefix(strings):
#     """Return longest common prefix of a list of strings."""
#     if not strings:
#         return ""

#     prefix = strings[0]
#     for s in strings[1:]:
#         while not s.startswith(prefix):
#             prefix = prefix[:-1]
#             if not prefix:
#                 return ""
#     return prefix

# # ------------------------------
# # ✅ UPDATED: Completer with LCP
# # ------------------------------

# def completer(text, state):
#     global last_prefix, cached_matches

#     # Reset cache if prefix changes
#     if text != last_prefix:
#         last_prefix = text
#         cached_matches = []

#     # Compute matches once
#     if not cached_matches:
#         execs = set(list_executables_in_path())
#         execs.update(BUILTINS_LITS)
#         cached_matches = sorted(cmd for cmd in execs if cmd.startswith(text))

#     if not cached_matches:
#         return None

#     # ✅ Single match → complete fully + space
#     if len(cached_matches) == 1:
#         if state == 0:
#             return cached_matches[0] + " "
#         return None

#     # ✅ Multiple matches → complete to LCP if possible
#     lcp = longest_common_prefix(cached_matches)

#     if len(lcp) > len(text):
#         if state == 0:
#             return lcp
#         return None

#     # 🔔 No progress possible → ring bell (once)
#     if state == 0:
#         sys.stdout.write("\x07")
#         sys.stdout.flush()

#     return None




# # ------------------------------
# # Display matches hook
# # ------------------------------

# def display_matches_hook(substitution, matches, longest_match_length):
#     sys.stdout.write("\n")
#     sys.stdout.write("  ".join(sorted(matches)))
#     sys.stdout.write("\n$ " + readline.get_line_buffer())
#     sys.stdout.flush()

# # ------------------------------
# # Executable discovery
# # ------------------------------

# def list_executables_in_path():
#     executables = set()
#     for dir_path in os.environ.get("PATH", "").split(os.pathsep):
#         if not os.path.isdir(dir_path):
#             continue
#         try:
#             for file in os.listdir(dir_path):
#                 full_path = os.path.join(dir_path, file)
#                 if os.access(full_path, os.X_OK) and os.path.isfile(full_path):
#                     executables.add(file)
#         except PermissionError:
#             continue
#     return list(executables)

# # ------------------------------
# # Redirection parser
# # ------------------------------

# def parse_redirection(parts):
#     stdout_file = None
#     stderr_file = None
#     stdout_append = False
#     stderr_append = False
#     clean_parts = []

#     i = 0
#     while i < len(parts):
#         tok = parts[i]

#         if tok in [">", "1>"] and i + 1 < len(parts):
#             stdout_file = parts[i + 1]
#             stdout_append = False
#             i += 2
#             continue

#         if tok in [">>", "1>>"] and i + 1 < len(parts):
#             stdout_file = parts[i + 1]
#             stdout_append = True
#             i += 2
#             continue

#         if tok == "2>" and i + 1 < len(parts):
#             stderr_file = parts[i + 1]
#             stderr_append = False
#             i += 2
#             continue

#         if tok == "2>>" and i + 1 < len(parts):
#             stderr_file = parts[i + 1]
#             stderr_append = True
#             i += 2
#             continue

#         clean_parts.append(tok)
#         i += 1

#     return clean_parts, stdout_file, stderr_file, stdout_append, stderr_append

# # ------------------------------
# # Main shell loop
# # ------------------------------

# def main():
#     readline.set_completer(completer)
#     readline.set_completion_display_matches_hook(display_matches_hook)
#     readline.parse_and_bind("tab: complete")

#     while True:
#         sys.stdout.write("$ ")
#         sys.stdout.flush()
#         try:
#             command = input().strip()
#         except EOFError:
#             print()
#             break

#         if not command:
#             continue

#         parts = shlex.split(command)
#         parts, stdout_file, stderr_file, stdout_append, stderr_append = parse_redirection(parts)

#         if not parts:
#             continue

#         cmd = parts[0]
#         args = parts[1:]

#         # Builtins
#         if cmd in BUILTINs:
#             save_stdout = sys.stdout
#             save_stderr = sys.stderr
#             try:
#                 if stdout_file:
#                     sys.stdout = open(stdout_file, "a" if stdout_append else "w")
#                 if stderr_file:
#                     sys.stderr = open(stderr_file, "a" if stderr_append else "w")
#                 BUILTINs[cmd](args)
#             finally:
#                 if stdout_file:
#                     sys.stdout.close()
#                 if stderr_file:
#                     sys.stderr.close()
#                 sys.stdout = save_stdout
#                 sys.stderr = save_stderr
#             continue

#         # External commands
#         path = shutil.which(cmd)
#         if path:
#             stdout_target = open(stdout_file, "a" if stdout_append else "w") if stdout_file else None
#             stderr_target = open(stderr_file, "a" if stderr_append else "w") if stderr_file else None

#             subprocess.run([cmd] + args, stdout=stdout_target, stderr=stderr_target)

#             if stdout_target:
#                 stdout_target.close()
#             if stderr_target:
#                 stderr_target.close()
#             continue

#         print(f"{command}: command not found", file=sys.stderr)

# if __name__ == "__main__":
#     main()










import sys
import shutil
import subprocess
import os
import shlex
import readline

# ------------------------------
# Builtins
# ------------------------------

def builtin_exit(args):
    sys.exit(0)

def builtin_cd(args):
    path = os.path.expanduser(args[0]) if args else os.path.expanduser("~")
    try:
        os.chdir(path)
    except FileNotFoundError:
        print(f"cd: {args[0]}: No such file or directory")
    except NotADirectoryError:
        print(f"cd: {args[0]}: Not a directory")
    except PermissionError:
        print(f"cd: {args[0]}: Permission denied")

def builtin_pwd(args):
    print(os.getcwd())

def builtin_echo(args):
    print(" ".join(args))

def builtin_type(args):
    if not args:
        print("")
        return

    target = args[0]
    if target in BUILTINs:
        print(f"{target} is a shell builtin")
        return

    path = shutil.which(target)
    if path:
        print(f"{target} is {path}")
        return

    print(f"{target}: not found")

BUILTINs = {
    "exit": builtin_exit,
    "echo": builtin_echo,
    "type": builtin_type,
    "pwd": builtin_pwd,
    "cd": builtin_cd,
}

BUILTINS_LITS = ["echo", "exit", "type", "pwd", "cd"]

# ------------------------------
# Completion state
# ------------------------------

last_prefix = ""
cached_matches = []

# ------------------------------
# ✅ NEW: Longest Common Prefix
# ------------------------------

def longest_common_prefix(strings):
    """Return longest common prefix of a list of strings."""
    if not strings:
        return ""

    prefix = strings[0]
    for s in strings[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix

# ------------------------------
# ✅ UPDATED: Completer with LCP
# ------------------------------

# def completer(text, state):
#     global last_prefix, cached_matches

#     # Reset cache if prefix changes
#     if text != last_prefix:
#         last_prefix = text
#         cached_matches = []

#     # Compute matches once
#     if not cached_matches:
#         execs = set(list_executables_in_path())
#         execs.update(BUILTINS_LITS)
#         cached_matches = sorted(cmd for cmd in execs if cmd.startswith(text))

#     if not cached_matches:
#         return None

#     # ✅ Single match → complete fully + space
#     if len(cached_matches) == 1:
#         if state == 0:
#             return cached_matches[0] + " "
#         return None

#     # ✅ Multiple matches → complete to LCP if possible
#     lcp = longest_common_prefix(cached_matches)

#     if len(lcp) > len(text):
#         if state == 0:
#             return lcp
#         return None

#     # 🔔 No progress possible → ring bell (once)
#     if state == 0:
#         sys.stdout.write("\x07")
#         sys.stdout.flush()

#     return None



# def completer(text, state):
#     global last_prefix, cached_matches

#     # Reset cache when text changes
#     if text != last_prefix:
#         last_prefix = text
#         cached_matches = []

#     # Compute matches once
#     if not cached_matches:
#         execs = set(list_executables_in_path())
#         execs.update(BUILTINS_LITS)
#         cached_matches = sorted(cmd for cmd in execs if cmd.startswith(text))

#     if not cached_matches:
#         return None

#     # ✅ Single match → complete fully
#     if len(cached_matches) == 1:
#         return cached_matches[0] + " " if state == 0 else None

#     # ✅ Multiple matches → attempt LCP
#     lcp = longest_common_prefix(cached_matches)

#     if len(lcp) > len(text):
#         return lcp if state == 0 else None

#     # 🔔 No LCP progress:
#     # First TAB → ring bell
#     if state == 0:
#         sys.stdout.write("\x07")
#         sys.stdout.flush()
#         return None
    
#     index = state - 1
#     if index < len(cached_matches):
#         return cached_matches[index]

#     # Second TAB → allow readline to call display_matches_hook
#     return None




# def completer(text, state):
#     global last_prefix, cached_matches

#     # Reset cache if prefix changed
#     if text != last_prefix:
#         last_prefix = text
#         cached_matches = []

#     # Build matches once
#     if not cached_matches:
#         execs = set(list_executables_in_path())
#         execs.update(BUILTINS_LITS)
#         cached_matches = sorted(cmd for cmd in execs if cmd.startswith(text))

#     if not cached_matches:
#         return None

#     # ✅ Single match → complete + space
#     if len(cached_matches) == 1:
#         return cached_matches[0] + " " if state == 0 else None

#     # ✅ Longest Common Prefix
#     lcp = longest_common_prefix(cached_matches)
#     if len(lcp) > len(text):
#         return lcp if state == 0 else None

#     # 🔔 No progress possible
#     if state == 0:
#         sys.stdout.write("\x07")
#         sys.stdout.flush()
#         return None

#     # ✅ SECOND TAB → enumerate matches
#     index = state - 1
#     if index < len(cached_matches):
#         return cached_matches[index]

#     return None


# def completer(text, state):
#     global last_prefix, cached_matches, tab_press_count

#     # Reset TAB state if text changes
#     if text != last_prefix:
#         last_prefix = text
#         tab_press_count = 0
#         cached_matches = []

#     # Build matches ONCE
#     if not cached_matches:
#         execs = set(list_executables_in_path())
#         execs.update(BUILTINS_LITS)
#         cached_matches = sorted(cmd for cmd in execs if cmd.startswith(text))

#     if not cached_matches:
#         return None

#     # -----------------------------
#     # SINGLE MATCH → complete fully
#     # -----------------------------
#     if len(cached_matches) == 1:
#         if state == 0:
#             return cached_matches[0] + " "
#         return None

#     # -----------------------------
#     # MULTIPLE MATCHES
#     # -----------------------------
#     if state == 0:
#         # FIRST TAB → bell only
#         if tab_press_count == 0:
#             sys.stdout.write("\a")
#             sys.stdout.flush()
#             tab_press_count = 1
#             return None

#         # SECOND TAB → print matches manually
#         sys.stdout.write("\n" + "  ".join(cached_matches))
#         sys.stdout.write("\n$ " + text)
#         sys.stdout.flush()
#         return text

#     # readline must get None after manual printing
#     return None


def completer(text, state):
    global last_prefix, cached_matches, tab_press_count

    # Reset TAB state if text changes
    if text != last_prefix:
        last_prefix = text
        tab_press_count = 0
        cached_matches = []

    # Build matches ONCE
    if not cached_matches:
        execs = set(list_executables_in_path())
        execs.update(BUILTINS_LITS)
        cached_matches = sorted(cmd for cmd in execs if cmd.startswith(text))

    if not cached_matches:
        return None

    # -----------------------------
    # SINGLE MATCH
    # -----------------------------
    if len(cached_matches) == 1:
        if state == 0:
            return cached_matches[0] + " "
        return None

    # -----------------------------
    # MULTIPLE MATCHES
    # -----------------------------
    if state == 0:
        # Compute Longest Common Prefix (LCP)
        lcp = os.path.commonprefix(cached_matches)

        # CASE 1: LCP extends current text → complete
        if len(lcp) > len(text):
            tab_press_count = 0
            return lcp

        # CASE 2: LCP == text → bell on first TAB
        if tab_press_count == 0:
            sys.stdout.write("\a")
            sys.stdout.flush()
            tab_press_count = 1
            return None

        # CASE 3: second TAB → show all matches
        sys.stdout.write("\n" + "  ".join(cached_matches))
        sys.stdout.write("\n$ " + text)
        sys.stdout.flush()
        return text

    return None



# ------------------------------
# Display matches hook
# ------------------------------

def display_matches_hook(substitution, matches, longest_match_length):
    sys.stdout.write("\n")
    sys.stdout.write("  ".join(sorted(matches)))
    sys.stdout.write("\n$ " + readline.get_line_buffer())
    sys.stdout.flush()

# ------------------------------
# Executable discovery
# ------------------------------

def list_executables_in_path():
    executables = set()
    for dir_path in os.environ.get("PATH", "").split(os.pathsep):
        if not os.path.isdir(dir_path):
            continue
        try:
            for file in os.listdir(dir_path):
                full_path = os.path.join(dir_path, file)
                if os.access(full_path, os.X_OK) and os.path.isfile(full_path):
                    executables.add(file)
        except PermissionError:
            continue
    return list(executables)

# ------------------------------
# Redirection parser
# ------------------------------

def parse_redirection(parts):
    stdout_file = None
    stderr_file = None
    stdout_append = False
    stderr_append = False
    clean_parts = []

    i = 0
    while i < len(parts):
        tok = parts[i]

        if tok in [">", "1>"] and i + 1 < len(parts):
            stdout_file = parts[i + 1]
            stdout_append = False
            i += 2
            continue

        if tok in [">>", "1>>"] and i + 1 < len(parts):
            stdout_file = parts[i + 1]
            stdout_append = True
            i += 2
            continue

        if tok == "2>" and i + 1 < len(parts):
            stderr_file = parts[i + 1]
            stderr_append = False
            i += 2
            continue

        if tok == "2>>" and i + 1 < len(parts):
            stderr_file = parts[i + 1]
            stderr_append = True
            i += 2
            continue

        clean_parts.append(tok)
        i += 1

    return clean_parts, stdout_file, stderr_file, stdout_append, stderr_append

# ------------------------------
# Main shell loop
# ------------------------------

def main():
    readline.set_completer(completer)
    readline.set_completion_display_matches_hook(display_matches_hook)
    readline.parse_and_bind("tab: complete")

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        try:
            command = input().strip()
        except EOFError:
            print()
            break

        if not command:
            continue

        parts = shlex.split(command)
        parts, stdout_file, stderr_file, stdout_append, stderr_append = parse_redirection(parts)

        if not parts:
            continue

        cmd = parts[0]
        args = parts[1:]

        # Builtins
        if cmd in BUILTINs:
            save_stdout = sys.stdout
            save_stderr = sys.stderr
            try:
                if stdout_file:
                    sys.stdout = open(stdout_file, "a" if stdout_append else "w")
                if stderr_file:
                    sys.stderr = open(stderr_file, "a" if stderr_append else "w")
                BUILTINs[cmd](args)
            finally:
                if stdout_file:
                    sys.stdout.close()
                if stderr_file:
                    sys.stderr.close()
                sys.stdout = save_stdout
                sys.stderr = save_stderr
            continue

        # External commands
        path = shutil.which(cmd)
        if path:
            stdout_target = open(stdout_file, "a" if stdout_append else "w") if stdout_file else None
            stderr_target = open(stderr_file, "a" if stderr_append else "w") if stderr_file else None

            subprocess.run([cmd] + args, stdout=stdout_target, stderr=stderr_target)

            if stdout_target:
                stdout_target.close()
            if stderr_target:
                stderr_target.close()
            continue

        print(f"{command}: command not found", file=sys.stderr)

if __name__ == "__main__":
    main()
