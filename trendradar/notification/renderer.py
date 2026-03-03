# coding=utf-8
"""
通知内容渲染模块

提供多平台通知内容渲染功能，生成格式化的推送消息
"""

from datetime import datetime
from typing import Dict, List, Optional, Callable

from trendradar.report.formatter import format_title_for_platform


def render_feishu_content(
    report_data: Dict,
    update_info: Optional[Dict] = None,
    mode: str = "daily",
    separator: str = "---",
    region_order: Optional[List[str]] = None,
    get_time_func: Optional[Callable[[], datetime]] = None,
    rss_items: Optional[list] = None,
    show_new_section: bool = True,
) -> str:
    """渲染飞书通知内容，仅保留【全局序号. 标题（链接）】核心格式"""
    new_titles_content = ""
    if show_new_section and report_data["new_titles"]:
        global_index = 1
        for source_data in report_data["new_titles"]:
            for title_data in source_data["titles"]:
                title_data_copy = title_data.copy()
                title_data_copy["is_new"] = False
                formatted_title = format_title_for_platform(
                    "feishu", title_data_copy, show_source=False
                )
                new_titles_content += f"{global_index}. {formatted_title}\n"
                global_index += 1
    return new_titles_content.rstrip("\n") if new_titles_content else "📭 暂无本次新增热点新闻"


def render_dingtalk_content(
    report_data: Dict,
    update_info: Optional[Dict] = None,
    mode: str = "daily",
    region_order: Optional[List[str]] = None,
    get_time_func: Optional[Callable[[], datetime]] = None,
    rss_items: Optional[list] = None,
    show_new_section: bool = True,
) -> str:
    """渲染钉钉通知内容，格式：【加粗主标题（日期AI热门资讯） + 全局序号. 标题（链接）】"""
    # 1. 获取当前日期，格式化为 YYYY-MM-DD
    now = get_time_func() if get_time_func else datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    # 2. 构造加粗主标题：XXX 日期AI热门资讯（这里XXX可根据需求替换，默认用「每日」）
    main_title = f"**每日 {date_str} AI热门资讯**"
    
    # 3. 生成全局序号的新闻条目
    new_titles_content = ""
    if show_new_section and report_data["new_titles"]:
        global_index = 1
        for source_data in report_data["new_titles"]:
            for title_data in source_data["titles"]:
                title_data_copy = title_data.copy()
                title_data_copy["is_new"] = False
                formatted_title = format_title_for_platform(
                    "dingtalk", title_data_copy, show_source=False
                )
                new_titles_content += f"{global_index}. {formatted_title}\n"
                global_index += 1
    
    # 4. 拼接最终内容（主标题 + 条目，无内容时仅显示主标题+提示）
    if new_titles_content:
        final_content = f"{main_title}\n\n{new_titles_content}".rstrip("\n")
    else:
        final_content = f"{main_title}\n\n📭 暂无本次新增热点新闻"
    
    return final_content


def render_rss_feishu_content(
    rss_items: list,
    feeds_info: Optional[Dict] = None,
    separator: str = "---",
    get_time_func: Optional[Callable[[], datetime]] = None,
) -> str:
    """渲染 RSS 飞书通知内容，仅保留【大标题 + 全局序号. 标题（链接）】格式"""
    if not rss_items:
        return "📭 暂无新的 RSS 订阅内容"

    text_content = "📰 **RSS 订阅更新**\n\n"
    global_index = 1
    for item in rss_items:
        title = item.get("title", "")
        url = item.get("url", "")
        if url:
            text_content += f"{global_index}. [{title}]({url})\n"
        else:
            text_content += f"{global_index}. {title}\n"
        global_index += 1
    return text_content.rstrip("\n")


def render_rss_dingtalk_content(
    rss_items: list,
    feeds_info: Optional[Dict] = None,
    get_time_func: Optional[Callable[[], datetime]] = None,
) -> str:
    """渲染 RSS 钉钉通知内容，仅保留【大标题 + 全局序号. 标题（链接）】格式"""
    if not rss_items:
        return "📭 暂无新的 RSS 订阅内容"

    text_content = "📰 **RSS 订阅更新**\n\n"
    global_index = 1
    for item in rss_items:
        title = item.get("title", "")
        url = item.get("url", "")
        if url:
            text_content += f"{global_index}. [{title}]({url})\n"
        else:
            text_content += f"{global_index}. {title}\n"
        global_index += 1
    return text_content.rstrip("\n")


def render_rss_markdown_content(
    rss_items: list,
    feeds_info: Optional[Dict] = None,
    get_time_func: Optional[Callable[[], datetime]] = None,
) -> str:
    """渲染 RSS 通用 Markdown 格式内容，仅保留【大标题 + 全局序号. 标题（链接）】格式"""
    if not rss_items:
        return "📭 暂无新的 RSS 订阅内容"

    text_content = "📰 **RSS 订阅更新**\n\n"
    global_index = 1
    for item in rss_items:
        title = item.get("title", "")
        url = item.get("url", "")
        if url:
            text_content += f"{global_index}. [{title}]({url})\n"
        else:
            text_content += f"{global_index}. {title}\n"
        global_index += 1
    return text_content.rstrip("\n")


def _render_rss_section_feishu(rss_items: list, separator: str = "---") -> str:
    """渲染 RSS 内容区块（飞书格式），仅保留【大标题 + 全局序号. 标题（链接）】格式"""
    if not rss_items:
        return ""

    text_content = "📰 **RSS 订阅更新**\n\n"
    global_index = 1
    for item in rss_items:
        title = item.get("title", "")
        url = item.get("url", "")
        if url:
            text_content += f"{global_index}. [{title}]({url})\n"
        else:
            text_content += f"{global_index}. {title}\n"
        global_index += 1
    return text_content.rstrip("\n")


def _render_rss_section_markdown(rss_items: list) -> str:
    """渲染 RSS 内容区块（通用 Markdown 格式），仅保留【大标题 + 全局序号. 标题（链接）】格式"""
    if not rss_items:
        return ""

    text_content = "📰 **RSS 订阅更新**\n\n"
    global_index = 1
    for item in rss_items:
        title = item.get("title", "")
        url = item.get("url", "")
        if url:
            text_content += f"{global_index}. [{title}]({url})\n"
        else:
            text_content += f"{global_index}. {title}\n"
        global_index += 1
    return text_content.rstrip("\n")
