# coding=utf-8
"""
平台标题格式化模块

提供多平台标题格式化功能
"""

from typing import Dict

from trendradar.report.helpers import clean_title, html_escape, format_rank_display


def format_title_for_platform(
    platform: str, title_data: Dict, show_source: bool = True, show_keyword: bool = False, plain_text: bool = False
) -> str:
    """统一的标题格式化方法

    为不同平台生成对应格式的标题字符串。

    Args:
        platform: 目标平台，支持:
            - "feishu": 飞书
            - "dingtalk": 钉钉
            - "wework": 企业微信
            - "bark": Bark
            - "telegram": Telegram
            - "ntfy": ntfy
            - "slack": Slack
            - "html": HTML 报告
        title_data: 标题数据字典，包含以下字段:
            - title: 标题文本
            - source_name: 来源名称
            - time_display: 时间显示
            - count: 出现次数
            - ranks: 排名列表
            - rank_threshold: 高亮阈值
            - url: PC端链接
            - mobile_url: 移动端链接（优先使用）
            - is_new: 是否为新增标题（可选）
            - matched_keyword: 匹配的关键词（可选，platform 模式使用）
        show_source: 是否显示来源名称（keyword 模式使用）
        show_keyword: 是否显示关键词标签（platform 模式使用）

    Returns:
        格式化后的标题字符串
    """
    rank_display = format_rank_display(
        title_data["ranks"], title_data["rank_threshold"], platform,
        use_html=not (platform == "feishu" and not show_source and not show_keyword)
    )

    link_url = title_data["mobile_url"] or title_data["url"]
    cleaned_title = clean_title(title_data["title"])

    # 获取关键词标签（platform 模式使用）
    keyword = title_data.get("matched_keyword", "") if show_keyword else ""

    if platform == "feishu":
        # 纯文本模式：标题 + 空格 +URL
        # Markdown 模式：[标题](URL) - 平台会渲染成蓝色可点击文本
        if plain_text:
            if link_url:
                formatted_title = f"{cleaned_title} {link_url}"
            else:
                formatted_title = cleaned_title
        else:
            if link_url:
                formatted_title = f"[{cleaned_title}]({link_url})"
            else:
                formatted_title = cleaned_title

        title_prefix = "🆕 " if title_data.get("is_new") else ""

        if show_source:
            result = f"<font color='grey'>[{title_data['source_name']}]</font> {title_prefix}{formatted_title}"
        elif show_keyword and keyword:
            result = f"<font color='blue'>[{keyword}]</font> {title_prefix}{formatted_title}"
        else:
            # 不显示来源和关键词时，使用纯文本前缀（与钉钉一致）
            result = f"{title_prefix}{formatted_title}"

        # 不显示来源时，也不显示排名、时间、次数（保持简洁）
        # if rank_display:
        #     result += f" {rank_display}"
        # if title_data["time_display"]:
        #     result += f" - {title_data['time_display']}"
        # if title_data["count"] > 1:
        #     result += f" ({title_data['count']}次)"

        return result

    elif platform == "dingtalk":
        # 纯文本模式：标题 + 空格 +URL
        # Markdown 模式：[标题](URL) - 平台会渲染成蓝色可点击文本
        if plain_text:
            if link_url:
                formatted_title = f"{cleaned_title} {link_url}"
            else:
                formatted_title = cleaned_title
        else:
            if link_url:
                formatted_title = f"[{cleaned_title}]({link_url})"
            else:
                formatted_title = cleaned_title

        title_prefix = "🆕 " if title_data.get("is_new") else ""

        if show_source:
            result = f"[{title_data['source_name']}] {title_prefix}{formatted_title}"
        elif show_keyword and keyword:
            result = f"[{keyword}] {title_prefix}{formatted_title}"
        else:
            result = f"{title_prefix}{formatted_title}"

        # 不显示来源时，也不显示排名、时间、次数（保持简洁）
        # if rank_display:
        #     result += f" {rank_display}"
        # if title_data["time_display"]:
        #     result += f" - {title_data['time_display']}"
        # if title_data["count"] > 1:
        #     result += f" ({title_data['count']}次)"

        return result

    elif platform in ("wework", "bark"):
        # WeWork 和 Bark 使用 markdown 格式
        if link_url:
            formatted_title = f"[{cleaned_title}]({link_url})"
        else:
            formatted_title = cleaned_title

        title_prefix = "🆕 " if title_data.get("is_new") else ""

        if show_source:
            result = f"[{title_data['source_name']}] {title_prefix}{formatted_title}"
        elif show_keyword and keyword:
            result = f"[{keyword}] {title_prefix}{formatted_title}"
        else:
            result = f"{title_prefix}{formatted_title}"

        if rank_display:
            result += f" {rank_display}"
        if title_data["time_display"]:
            result += f" - {title_data['time_display']}"
        if title_data["count"] > 1:
            result += f" ({title_data['count']}次)"

        return result

    elif platform == "telegram":
        if link_url:
            formatted_title = f'<a href="{link_url}">{html_escape(cleaned_title)}</a>'
        else:
            formatted_title = cleaned_title

        title_prefix = "🆕 " if title_data.get("is_new") else ""

        if show_source:
            result = f"[{title_data['source_name']}] {title_prefix}{formatted_title}"
        elif show_keyword and keyword:
            result = f"<b>[{html_escape(keyword)}]</b> {title_prefix}{formatted_title}"
        else:
            result = f"{title_prefix}{formatted_title}"

        if rank_display:
            result += f" {rank_display}"
        if title_data["time_display"]:
            result += f" <code>- {title_data['time_display']}</code>"
        if title_data["count"] > 1:
            result += f" <code>({title_data['count']}次)</code>"

        return result

    elif platform == "ntfy":
        if link_url:
            formatted_title = f"[{cleaned_title}]({link_url})"
        else:
            formatted_title = cleaned_title

        title_prefix = "🆕 " if title_data.get("is_new") else ""

        if show_source:
            result = f"[{title_data['source_name']}] {title_prefix}{formatted_title}"
        elif show_keyword and keyword:
            result = f"[{keyword}] {title_prefix}{formatted_title}"
        else:
            result = f"{title_prefix}{formatted_title}"

        if rank_display:
            result += f" {rank_display}"
        if title_data["time_display"]:
            result += f" `- {title_data['time_display']}`"
        if title_data["count"] > 1:
            result += f" `({title_data['count']}次)`"

        return result

    elif platform == "slack":
        # Slack 使用 mrkdwn 格式
        if link_url:
            # Slack 链接格式: <url|text>
            formatted_title = f"<{link_url}|{cleaned_title}>"
        else:
            formatted_title = cleaned_title

        title_prefix = "🆕 " if title_data.get("is_new") else ""

        if show_source:
            result = f"[{title_data['source_name']}] {title_prefix}{formatted_title}"
        elif show_keyword and keyword:
            result = f"*[{keyword}]* {title_prefix}{formatted_title}"
        else:
            result = f"{title_prefix}{formatted_title}"

        # 排名（使用 * 加粗）
        rank_display = format_rank_display(
            title_data["ranks"], title_data["rank_threshold"], "slack"
        )
        if rank_display:
            result += f" {rank_display}"
        if title_data["time_display"]:
            result += f" `- {title_data['time_display']}`"
        if title_data["count"] > 1:
            result += f" `({title_data['count']}次)`"

        return result

    elif platform == "html":
        rank_display = format_rank_display(
            title_data["ranks"], title_data["rank_threshold"], "html"
        )

        link_url = title_data["mobile_url"] or title_data["url"]

        escaped_title = html_escape(cleaned_title)
        escaped_source_name = html_escape(title_data["source_name"])

        # 构建前缀（来源或关键词）
        if show_source:
            prefix = f'<span class="source-tag">[{escaped_source_name}]</span> '
        elif show_keyword and keyword:
            escaped_keyword = html_escape(keyword)
            prefix = f'<span class="keyword-tag">[{escaped_keyword}]</span> '
        else:
            prefix = ""

        if link_url:
            escaped_url = html_escape(link_url)
            formatted_title = f'{prefix}<a href="{escaped_url}" target="_blank" class="news-link">{escaped_title}</a>'
        else:
            formatted_title = f'{prefix}<span class="no-link">{escaped_title}</span>'

        if rank_display:
            formatted_title += f" {rank_display}"
        if title_data["time_display"]:
            escaped_time = html_escape(title_data["time_display"])
            formatted_title += f" <font color='grey'>- {escaped_time}</font>"
        if title_data["count"] > 1:
            formatted_title += f" <font color='green'>({title_data['count']}次)</font>"

        if title_data.get("is_new"):
            formatted_title = f"<div class='new-title'>🆕 {formatted_title}</div>"

        return formatted_title

    else:
        return cleaned_title
