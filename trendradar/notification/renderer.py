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
    """渲染飞书通知内容：仅【加粗日期主标题 + 全局序号. 标题（链接）】"""
    # 1. 构造加粗主标题（和钉钉统一格式）
    now = get_time_func() if get_time_func else datetime.now()
    main_title = f"**{now.strftime('%Y-%m-%d')} AI热门资讯**"
    
    # 2. 扁平化遍历所有新闻，生成全局序号条目（完全删除来源分组）
    items = []
    global_index = 1
    if show_new_section and report_data.get("new_titles", []):
        # 直接扁平化，跳过来源分组的打印
        for source_data in report_data["new_titles"]:
            for title_data in source_data["titles"]:
                # 移除is_new标记，避免格式干扰
                title_data_copy = title_data.copy()
                title_data_copy["is_new"] = False
                # 生成纯标题+链接，不包含来源/后缀数字
                formatted_title = format_title_for_platform(
                    "feishu", title_data_copy, show_source=False
                )
                items.append(f"{global_index}. {formatted_title}")
                global_index += 1

    # 3. 拼接最终内容
    if items:
        return f"{main_title}\n\n" + "\n".join(items)
    else:
        return f"{main_title}\n\n📭 暂无本次新增热点新闻"


def render_dingtalk_content(
    report_data: Dict,
    update_info: Optional[Dict] = None,
    mode: str = "daily",
    region_order: Optional[List[str]] = None,
    get_time_func: Optional[Callable[[], datetime]] = None,
    rss_items: Optional[list] = None,
    show_new_section: bool = True,
    report_type: str = "AI热门资讯"
) -> str:
    """
    渲染钉钉通知内容（与分批模块格式完全一致）
    核心格式：**YYYY-MM-DD AI热门资讯** + 全局连续序号. 标题（链接）
    """
    # 1. 生成加粗日期主标题（和分批模块对齐）
    now = get_time_func() if get_time_func else datetime.now()
    main_title = f"**{now.strftime('%Y-%m-%d')} {report_type}**"
    
    # 2. 扁平化提取所有新增新闻，生成全局序号列表
    all_new_titles = []
    if show_new_section and report_data.get("new_titles", []):
        global_index = 1
        for source_data in report_data["new_titles"]:
            for title_data in source_data["titles"]:
                title_data_copy = title_data.copy()
                title_data_copy["is_new"] = False
                # 生成纯标题+链接，不显示来源
                formatted_title = format_title_for_platform(
                    "dingtalk", title_data_copy, show_source=False
                )
                # 移除标题后的[数字]后缀（如[19]）
                formatted_title = formatted_title.rsplit("[", 1)[0].rstrip()
                all_new_titles.append(f"{global_index}. {formatted_title}")
                global_index += 1

    # 3. 拼接最终内容（无任何冗余信息）
    if not all_new_titles:
        return f"{main_title}\n\n📭 暂无本次新增热点新闻"
    
    final_content = f"{main_title}\n\n" + "\n".join(all_new_titles)
    return final_content


def render_rss_feishu_content(
    rss_items: list,
    feeds_info: Optional[Dict] = None,
    separator: str = "---",
    get_time_func: Optional[Callable[[], datetime]] = None,
) -> str:
    """渲染RSS飞书内容：仅【加粗主标题 + 全局序号. 标题（链接）】"""
    now = get_time_func() if get_time_func else datetime.now()
    main_title = f"**{now.strftime('%Y-%m-%d')} RSS订阅更新**"
    items = []
    global_index = 1
    if rss_items:
        for item in rss_items:
            title = item.get("title", "")
            url = item.get("url", "")
            items.append(f"{global_index}. [{title}]({url})" if url else f"{global_index}. {title}")
            global_index += 1
    return f"{main_title}\n\n" + "\n".join(items) if items else f"{main_title}\n\n📭 暂无新的RSS订阅内容"


def render_rss_dingtalk_content(
    rss_items: list,
    feeds_info: Optional[Dict] = None,
    get_time_func: Optional[Callable[[], datetime]] = None,
) -> str:
    """渲染RSS钉钉内容：仅【加粗主标题 + 全局序号. 标题（链接）】"""
    now = get_time_func() if get_time_func else datetime.now()
    main_title = f"**{now.strftime('%Y-%m-%d')} RSS订阅更新**"
    items = []
    global_index = 1
    if rss_items:
        for item in rss_items:
            title = item.get("title", "")
            url = item.get("url", "")
            items.append(f"{global_index}. [{title}]({url})" if url else f"{global_index}. {title}")
            global_index += 1
    return f"{main_title}\n\n" + "\n".join(items) if items else f"{main_title}\n\n📭 暂无新的RSS订阅内容"


def render_rss_markdown_content(
    rss_items: list,
    feeds_info: Optional[Dict] = None,
    get_time_func: Optional[Callable[[], datetime]] = None,
) -> str:
    """渲染RSS通用Markdown内容：仅【加粗主标题 + 全局序号. 标题（链接）】"""
    now = get_time_func() if get_time_func else datetime.now()
    main_title = f"**{now.strftime('%Y-%m-%d')} RSS订阅更新**"
    items = []
    global_index = 1
    if rss_items:
        for item in rss_items:
            title = item.get("title", "")
            url = item.get("url", "")
            items.append(f"{global_index}. [{title}]({url})" if url else f"{global_index}. {title}")
            global_index += 1
    return f"{main_title}\n\n" + "\n".join(items) if items else f"{main_title}\n\n📭 暂无新的RSS订阅内容"


# 以下辅助函数若无需合并推送，可直接删除；若需保留，同步扁平化修改
def _render_rss_section_feishu(rss_items: list, separator: str = "---") -> str:
    if not rss_items:
        return ""
    items = []
    global_index = 1
    for item in rss_items:
        title = item.get("title", "")
        url = item.get("url", "")
        items.append(f"{global_index}. [{title}]({url})" if url else f"{global_index}. {title}")
        global_index += 1
    return "📰 **RSS订阅更新**\n\n" + "\n".join(items)


def _render_rss_section_markdown(rss_items: list) -> str:
    if not rss_items:
        return ""
    items = []
    global_index = 1
    for item in rss_items:
        title = item.get("title", "")
        url = item.get("url", "")
        items.append(f"{global_index}. [{title}]({url})" if url else f"{global_index}. {title}")
        global_index += 1
    return "📰 **RSS订阅更新**\n\n" + "\n".join(items)
