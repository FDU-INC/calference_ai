# Copyright (C) 2025 FDU-INC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from datetime import datetime
import re
import json

def strip_outer_codeblock(md):
    # 去除最外层的```markdown ...```或```...```包裹
    pattern = r'^```(?:markdown)?\s*([\s\S]*?)\s*```$'
    match = re.match(pattern, md.strip(), re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return md

def save_dialogue_html(dialogue_log, output_html, report_docx_path=None):
    """
    Multi-agent dialogue log with beautiful bubble chat UI. User on right, agents on left.
    对非report_agent内容自动去除多余前后空行，若内容不以markdown段落开头则自动加一个空行，提升分段美观性。
    自动去除内容外层的```markdown ...```或```...```包裹，保证markdown渲染美观。
    """
    agent_styles = {
        'user': {
            'name': 'User', 'avatar': '🧑', 'align': 'right', 'bubble_color': '#f7f7f7', 'text_color': '#222',
        },
        'report_agent': {
            'name': 'Report Agent', 'avatar': '📄', 'align': 'left', 'bubble_color': '#fff', 'text_color': '#222',
        },
        'parser_agent': {
            'name': 'Parser Agent', 'avatar': '🧩', 'align': 'left', 'bubble_color': '#fff', 'text_color': '#222',
        },
        'analysis_agent': {
            'name': 'Analysis Agent', 'avatar': '📊', 'align': 'left', 'bubble_color': '#fff', 'text_color': '#222',
        },
        'review_agent': {
            'name': 'Review Agent', 'avatar': '🔍', 'align': 'left', 'bubble_color': '#fff', 'text_color': '#222',
        },
    }

    def render_message(entry):
        agent = entry.get('agent', 'user')
        style = agent_styles.get(agent, agent_styles['user'])
        align = style['align']
        avatar = style['avatar']
        bubble_color = style['bubble_color']
        text_color = style['text_color']
        name = style['name']
        time_str = entry.get('time', '')
        content = entry.get('content', '')
        if isinstance(content, list):
            content = '\n'.join([str(x) for x in content])
        # report_agent: 只显示下载链接
        if agent == 'report_agent':
            if report_docx_path:
                content_html = f'<a href="{report_docx_path}" download style="font-size:18px;color:#67C23A;font-weight:bold;">Download Word Report</a>'
            else:
                content_html = '<span style="color:#aaa;">Report generating...</span>'
        else:
            # 直接传递原始markdown字符串，不做html.escape，自动去除外层代码块
            content = str(content).strip('\n')
            content = strip_outer_codeblock(content)
            if not (content.startswith('#') or content.startswith('-') or content.startswith('**') or content.startswith('1.') or content.startswith('>')):
                content = '\n' + content
            content_html = f'<div class="markdown-body">{content}</div>'
        # agent名字旁加时间，内容默认展开
        html_msg = f'''
        <div class="msg-row {align}">
            <div class="avatar">{avatar}</div>
            <div class="bubble" style="background:{bubble_color};color:{text_color}" title="{time_str}">
                <div class="agent-name">{name} <span style='font-size:13px;color:#888;margin-left:8px;'>{time_str}</span></div>
                <div class="msg-content" style="display:block;">{content_html}</div>
            </div>
        </div>
        '''
        return html_msg

    html_msgs = [render_message(entry) for entry in dialogue_log]
    html_msgs = [msg for msg in html_msgs if msg]  # 过滤掉空内容

    # 自动检测最新docx报告
    if not report_docx_path:
        report_dir = os.path.join(os.path.dirname(output_html), '../output_reports')
        if os.path.exists(report_dir):
            docx_files = [f for f in os.listdir(report_dir) if f.endswith('.docx')]
            if docx_files:
                latest_docx = max(docx_files, key=lambda f: os.path.getmtime(os.path.join(report_dir, f)))
                report_docx_path = os.path.relpath(os.path.join(report_dir, latest_docx), os.path.dirname(output_html))

    # 动态控制自动刷新
    refresh_meta = '<meta http-equiv="refresh" content="2">' if not report_docx_path else ''

    html_code = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Multi-Agent Dialogue</title>
    {refresh_meta}
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11.9.0/styles/github.min.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/highlight.js@11.9.0/lib/highlight.min.js"></script>
    <style>
        body {{ background: #f5f7fa; font-family: 'PingFang SC','Microsoft YaHei',Arial,sans-serif; margin:0; }}
        .chat-container {{ width: 100vw; margin: 0; padding: 0; background: #fff; border-radius: 0; box-shadow: none; }}
        .chat-header {{ text-align:center; color:#222; font-size:22px; font-weight:bold; margin-bottom:18px; letter-spacing:1px; }}
        .msg-row {{ display: flex; margin-bottom: 24px; align-items: flex-start; }}
        .msg-row.left {{ flex-direction: row; justify-content: flex-start; width: 100%; }}
        .msg-row.right {{ flex-direction: row-reverse; justify-content: flex-end; width: 100%; }}
        .avatar {{ width: 52px; height: 52px; border-radius: 50%; background: #e4e7ed; display: flex; align-items: center; justify-content: center; font-size: 30px; margin-bottom: auto; }}
        .msg-row.left .avatar {{ margin: 0 0 0 4px; }}
        .msg-row.right .avatar {{ margin: 0 0 0 8px; }}
        .bubble {{ min-width: 20%; padding: 18px 22px; border-radius: 22px; position: relative; word-break: break-all; box-shadow: 0 4px 24px #0001; font-size: 18px; line-height: 1.8; border: none; align-self: flex-start; }}
        .msg-row.left .bubble {{ background: #fff; color: #222; max-width: 98%; margin-left: 0; margin-right: auto; }}
        .msg-row.right .bubble {{ background: #f7f7f7; color: #222; max-width: 98%; margin-right: 0; margin-left: auto; }}
        .bubble:hover {{ box-shadow: 0 4px 16px #0002; }}
        .agent-name {{ font-size: 14px; font-weight: bold; margin-bottom: 8px; opacity: 0.7; }}
        .msg-content {{ /* max-height: 320px; overflow-y: auto; */ }}
        /* markdown美化增强 */
        .markdown-body p {{ margin: 14px 0 14px 0; font-size: 18px; }}
        .markdown-body strong, .markdown-body b {{ font-weight: bold; color: #222; }}
        .markdown-body h1, .markdown-body h2, .markdown-body h3 {{ margin: 18px 0 10px 0; font-weight: bold; color: #222; }}
        .markdown-body ul, .markdown-body ol {{ margin: 12px 0 12px 28px; }}
        .markdown-body li {{ margin: 6px 0; font-size: 17px; }}
        .markdown-body pre, .markdown-body code {{ background: #f6f8fa; border-radius: 6px; padding: 2px 6px; font-size: 15px; }}
        .markdown-body pre {{ padding: 12px; overflow-x: auto; }}
        .markdown-body table {{ border-collapse: collapse; margin: 8px 0; }}
        .markdown-body th, .markdown-body td {{ border: 1px solid #dfe2e5; padding: 6px 13px; }}
        .markdown-body blockquote {{ color: #6a737d; border-left: 4px solid #dfe2e5; padding: 0 1em; margin: 0.5em 0; }}
        @media (max-width: 600px) {{ .chat-container {{ width: 100vw; padding: 2px; }} .bubble {{ max-width: 98%; }} }}
        ::-webkit-scrollbar {{ width: 8px; background: #eee; }}
        ::-webkit-scrollbar-thumb {{ background: #ccc; border-radius: 4px; }}
        .chat-footer {{ text-align:center; color:#aaa; font-size:15px; margin-top:18px; letter-spacing:1px; }}
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">Multi-Agent Dialogue</div>
        {''.join(html_msgs)}
        <div class="chat-footer">—— All loaded ——</div>
    </div>
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
      document.querySelectorAll('.markdown-body').forEach(function(el) {{
        el.innerHTML = marked.parse(el.textContent);
        el.querySelectorAll('pre code').forEach((block) => {{ hljs.highlightElement(block); }});
      }});
      window.scrollTo(0, document.body.scrollHeight);
    }});
    </script>
</body>
</html>
'''
    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_code) 