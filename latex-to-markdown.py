import re
import sys

def convert_latex_to_markdown(latex_content):
    """Convert LaTeX content to Markdown for Obsidian, replacing '&=' with '=' in align environments."""
    # Extract title, author, and date from preamble if present
    title = re.search(r'\\title{(.+?)}', latex_content)
    author = re.search(r'\\author{(.+?)}', latex_content)
    date = re.search(r'\\date{(.+?)}', latex_content)

    # Find document content between \begin{document} and \end{document}
    start = latex_content.find(r'\begin{document}')
    end = latex_content.find(r'\end{document}', start)
    if start != -1 and end != -1:
        content = latex_content[start + len(r'\begin{document}'):end].strip()
    else:
        content = latex_content

    lines = content.split('\n')
    markdown_lines = []
    in_math = False
    in_align = False
    in_equation_star = False
    in_list = False
    math_content = ""
    list_depth = 0

    # Add title, author, date at the top if they exist
    if title:
        markdown_lines.append(f'# {title.group(1)}')
    if author:
        markdown_lines.append(f'**Author:** {author.group(1)}')
    if date and date.group(1):
        markdown_lines.append(f'**Date:** {date.group(1)}')
    if title or author or date:
        markdown_lines.append('')

    # Handle table of contents
    if r'\tableofcontents' in content:
        markdown_lines.append('## Table of Contents')
        markdown_lines.append('*(Generated automatically in LaTeX, list sections manually in Markdown if needed)*')
        markdown_lines.append('')

    for line in lines:
        line = line.strip()
        if in_equation_star:
            if line.startswith(r'\end{equation*}'):
                in_equation_star = False
                if math_content:
                    markdown_lines.append(f'$${math_content.strip()}$$')
                math_content = ""
            else:
                math_content += " " + line.strip()
        elif in_align:
            if line.startswith(r'\end{align*}'):
                in_align = False
                if math_content:
                    # Split align content into separate equations and replace '&=' with '='
                    equations = math_content.split('\\\\')
                    for eq in equations:
                        eq = eq.strip().replace('&=', '=').replace('&', '')
                        if eq:
                            markdown_lines.append(f'$${eq}$$')
                math_content = ""
            else:
                math_content += " " + line.strip()
        elif in_math:
            if line.startswith(r'\]'):
                in_math = False
                if math_content:
                    markdown_lines.append(f'$${math_content.strip()}$$')
                math_content = ""
            else:
                math_content += " " + line.strip()
        elif in_list:
            if line.startswith(r'\end{itemize}'):
                in_list = False
                list_depth -= 1
            elif line.startswith(r'\item'):
                item_text = re.sub(r'\\item\s+', '', line).strip()
                markdown_lines.append(f'{"  " * list_depth}- {item_text}')
            else:
                markdown_lines.append(line)
        else:
            if line.startswith(r'\begin{equation*}'):
                in_equation_star = True
                math_content = line[len(r'\begin{equation*}'):].strip()
            elif line.startswith(r'\begin{align*}'):
                in_align = True
                math_content = line[len(r'\begin{align*}'):].strip()
            elif line.startswith(r'\['):
                in_math = True
                math_content = line[2:].strip()  # Remove '\['
            elif line.startswith(r'\begin{itemize}'):
                in_list = True
                list_depth += 1
            elif line.startswith(r'\section{'):
                section_title = re.search(r'\\section{(.+?)}', line).group(1)
                markdown_lines.append(f'# {section_title}')
            elif line.startswith(r'\subsection{'):
                subsection_title = re.search(r'\\subsection{(.+?)}', line).group(1)
                markdown_lines.append(f'## {subsection_title}')
            elif line.startswith(r'\subsubsection{'):
                subsubsection_title = re.search(r'\\subsubsection{(.+?)}', line).group(1)
                markdown_lines.append(f'### {subsubsection_title}')
            elif line.startswith(r'\newpage') or line.strip() == r'\maketitle' or line.strip() == r'\tableofcontents':
                continue  # Ignore these commands
            else:
                markdown_lines.append(line)

    return '\n'.join(markdown_lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the input file name.")
        sys.exit(1)

    input_file = sys.argv[1]
    with open(input_file, 'r') as file:
        latex_content = file.read()

    markdown_content = convert_latex_to_markdown(latex_content)

    output_file = input_file.replace('.txt', '.md')
    with open(output_file, 'w') as file:
        file.write(markdown_content)

    print(f"Conversion complete. Output written to {output_file}")
