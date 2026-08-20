import re
from pathlib import Path
from src.drw_parser import parse_drw_file
from src.svg_renderer import render_svg

def convert_mss(mss_content: str, filename: str, smi_dir: str | Path) -> str:
    smi_dir = Path(smi_dir)
    svg_out_dir = Path("/Users/dmoisa/Documents/sun/smi/suds-tools/data/svg")
    svg_out_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Strip SAIL-era comment block
    sail_comment_pattern = re.compile(r'^COMMENT\s+⊗.*?C⊗;', re.DOTALL | re.MULTILINE)
    mss_content = sail_comment_pattern.sub('', mss_content)
    
    # 2. Form feeds to page breaks
    mss_content = mss_content.replace('\f', '\n---\n')

    structural = {
        'chapter': '# ',
        'section': '## ',
        'subsection': '### ',
        'subheading': '#### ',
        'heading': '# ',
        'majorheading': '# '
    }
    
    inline_format = {
        'b': '**', 'i': '*', 'I': '*', 'c': '`', 'C': '`', 't': '`',
        'x': '[', 'X': '[', 'ss': '**'
    }
    
    strip_cmds = {
        'make', 'device', 'style', 'modify', 'Modify', 'define', 'Define',
        'Form', 'font', 'FONT', 'set', 'textform', 'pageheading', 'pagefooting',
        'copyrightnotice', 'Enter', 'Leave',
        'tabset', 'tabclear', 'skip', 'avb',
    }
    
    def parse_nested(text, start_idx):
        open_char = text[start_idx]
        if open_char == '(': close_char = ')'
        elif open_char == '[': close_char = ']'
        elif open_char == '{': close_char = '}'
        elif open_char == '<': close_char = '>'
        elif open_char == '"': close_char = '"'
        elif open_char == "'": close_char = "'"
        else: return -1, ''
        
        count = 1
        i = start_idx + 1
        while i < len(text):
            if text[i] == open_char and open_char not in ('"', "'"):
                count += 1
            elif text[i] == close_char:
                count -= 1
                if count == 0:
                    return i, text[start_idx+1:i]
            i += 1
        return -1, text[start_idx+1:]

    at_count = mss_content.count('@')

    def process_content(text):
        env_stack = []
        res = []
        i = 0
        
        while i < len(text):
            if text[i] == '@':
                if text[i:i+8].lower() == '@newpage':
                    res.append('\n---\n')
                    i += 8
                    continue
                
                cmd_match = re.match(r'^@([a-zA-Z0-9]+)', text[i:])
                if cmd_match:
                    cmd = cmd_match.group(1)
                    cmd_len = len(cmd)
                    after_cmd_idx = i + 1 + cmd_len
                    
                    if after_cmd_idx < len(text) and text[after_cmd_idx] in '([{<"\'':
                        end_idx, arg = parse_nested(text, after_cmd_idx)
                        if end_idx != -1:
                            if cmd in strip_cmds:
                                pass # do not evaluate arg
                            elif cmd in structural:
                                res.append(f"\n{structural[cmd]}{process_content(arg)}\n")
                            elif cmd in inline_format:
                                if cmd in ('x', 'X'):
                                    res.append(f"[{process_content(arg)}]")
                                else:
                                    f = inline_format[cmd]
                                    res.append(f"{f}{process_content(arg)}{f}")
                            elif cmd.lower() == 'blankspace':
                                res.append("\n\n")
                            elif cmd.lower() == 'flushleft':
                                res.append(process_content(arg))
                            elif cmd.lower() == 'center':
                                res.append(f"\n<center>{process_content(arg)}</center>\n")
                            elif cmd == 'value':
                                if arg == 'date': res.append('[date]')
                            elif cmd.lower() == 'caption':
                                res.append(f"\n*Figure: {process_content(arg)}*\n")
                            elif cmd == 'tag' or cmd == 'label':
                                res.append(f'<a id="{arg}"></a>')
                            elif cmd == 'ref':
                                res.append(f'[Figure](#{arg})')
                            elif cmd == 'include':
                                inc_path = smi_dir / arg
                                if inc_path.exists():
                                    res.append(convert_mss(inc_path.read_text(errors='ignore'), arg, smi_dir))
                            elif cmd == 'getfile':
                                inc_path = smi_dir / arg
                                content = inc_path.read_text(errors='ignore') if inc_path.exists() else "File not found."
                                res.append(f"\n> 📄 **Source:** `{arg}`\n```\n{content}\n```\n")
                            elif cmd == 'presspicture':
                                file_match = re.search(r'file\s*=\s*"?([^\s",]+)"?', arg, re.IGNORECASE)
                                if file_match:
                                    press_file = file_match.group(1)
                                    base = press_file.replace('.press', '').replace('.PRESS', '').lower()
                                    import glob
                                    drw_matches = glob.glob(str(smi_dir / f"octal/{base}*.drw.O"))
                                    if drw_matches:
                                        drw_file = drw_matches[0]
                                        drw_base = Path(drw_file).name
                                        svg_name = drw_base + ".svg"
                                        svg_path = svg_out_dir / svg_name
                                        if not svg_path.exists():
                                            try:
                                                drw = parse_drw_file(drw_file)
                                                svg_str = render_svg(drw)
                                                svg_path.write_text(svg_str)
                                            except Exception as e:
                                                print(f"Error rendering {drw_file}: {e}")
                                        res.append(f"\n![{press_file}](../svg/{svg_name})\n")
                                    else:
                                        res.append(f"\n![Placeholder: {press_file}]()\n")
                            elif cmd == 'begin':
                                env = arg.lower()
                                env_stack.append(env)
                                if env in ('itemize', 'enumerate'):
                                    res.append("\n")
                                elif env == 'example' or env == 'format':
                                    res.append("\n```\n")
                                elif env == 'titlepage':
                                    res.append("\n---\n")
                                elif env in ('abstract', 'researchcredit', 'quotation', 'description'):
                                    res.append("\n> ")
                            elif cmd == 'end':
                                env = arg.lower()
                                if env_stack and env_stack[-1] == env:
                                    env_stack.pop()
                                    if env in ('example', 'format'):
                                        res.append("\n```\n")
                                    elif env == 'titlepage':
                                        res.append("\n---\n")
                            elif cmd == 'foot':
                                res.append(f' *({process_content(arg)})*')
                            else:
                                res.append(process_content(arg))
                                
                            i = end_idx + 1
                            continue
                    elif cmd == 'xsym' and after_cmd_idx < len(text) and text[after_cmd_idx] == '[':
                        end_idx, arg = parse_nested(text, after_cmd_idx)
                        if end_idx != -1 and arg == '}':
                            res.append('©')
                            i = end_idx + 1
                            continue
                    
                    if cmd in strip_cmds:
                        i = after_cmd_idx
                        continue
                    else:
                        res.append(f"@{cmd}")
                        i = after_cmd_idx
                        continue
            
            char = text[i]
            
            # handle list formatting
            if char == '\n' and env_stack and env_stack[-1] in ('itemize', 'enumerate'):
                res.append(char)
                if i + 1 < len(text) and text[i+1] == '\t':
                    if env_stack[-1] == 'itemize':
                        res.append("- ")
                    else:
                        res.append("1. ")
                    i += 2
                    continue
                i += 1
                continue

            res.append(char)
            i += 1

        return "".join(res)
    
    out = process_content(mss_content)

    # ── Post-processing cleanup ───────────────────────────────────────
    # Collapse 3+ consecutive blank lines to 2
    out = re.sub(r'\n{4,}', '\n\n\n', out)
    # Collapse multiple --- separators
    out = re.sub(r'(\n---\n){2,}', '\n---\n', out)
    # Remove trailing whitespace on lines
    out = re.sub(r'[ \t]+$', '', out, flags=re.MULTILINE)
    # Remove leading blank lines
    out = out.lstrip('\n')
    # Remove trailing blank lines
    out = out.rstrip('\n') + '\n'

    # Plain text files — add title if no heading found
    if at_count < 6 and not re.search(r'^#\s+', out, re.MULTILINE):
        out = f"# {filename}\n\n" + out

    return out

