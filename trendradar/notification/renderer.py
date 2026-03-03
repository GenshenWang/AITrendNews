# coding=utf-8
"""
通知内容渲染模块

提供多平台通知内容渲染功能，生成格式化的推送消息
核心格式：加粗日期主标题 + 全局连续序号. 标题（链接）
"""

from datetime import datetime
from typing import Dict, List, Optional, Callable

from trendradar.report.formatter import format_title_for_platform


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
        max_titles = 15  # 固定推送 15 条
        for source_data in report_data["new_titles"]:
            for title_data in source_data["titles"]:
                if global_index > max_titles:
                    break
                title_data_copy = title_data.copy()
                title_data_copy["is_new"] = False
                # 生成纯标题+链接，不显示来源
                formatted_title = format_title_for_platform(
                    "dingtalk", title_data_copy, show_source=False
                )
                # 移除标题后的[数字]后缀（如[19]）
                formatted_title = formatted_title.rsplit("[", 1)[0].rstrip()
                # 新增：移除末尾的 **
                formatted_title = formatted_title.rstrip("*").rstrip()
                all_new_titles.append(f"{global_index}. {formatted_title}")
                global_index += 1
            if global_index > max_titles:
                break

    # 3. 拼接最终内容（无任何冗余信息）
    if not all_new_titles:
        return f"{main_title}\n\n📭 暂无本次新增热点新闻"

    final_content = f"{main_title}\n\n" + "\n".join(all_new_titles)
    return final_content


def render_feishu_content(
    report_data: Dict,
    update_info: Optional[Dict] = None,
    mode: str = "daily",
    separator: str = "---",
    region_order: Optional[List[str]] = None,
    get_time_func: Optional[Callable[[], datetime]] = None,
    rss_items: Optional[list] = None,
    show_new_section: bool = True,
    report_type: str = "AI热门资讯"
) -> str:
    """
    渲染飞书通知内容（与分批模块格式完全一致）
    核心格式：**YYYY-MM-DD AI热门资讯** + 全局连续序号. 标题（链接）
    """
    # 1. 生成加粗日期主标题（和分批模块、钉钉渲染函数对齐）
    now = get_time_func() if get_time_func else datetime.now()
    main_title = f"**{now.strftime('%Y-%m-%d')} {report_type}**"

    # 2. 扁平化提取所有新增新闻，生成全局序号列表
    all_new_titles = []
    if show_new_section and report_data.get("new_titles", []):
        global_index = 1
        max_titles = 15  # 固定推送 15 条
        for source_data in report_data["new_titles"]:
            for title_data in source_data["titles"]:
                if global_index > max_titles:
                    break
                title_data_copy = title_data.copy()
                title_data_copy["is_new"] = False
                # 生成纯标题+链接，不显示来源
                formatted_title = format_title_for_platform(
                    "feishu", title_data_copy, show_source=False
                )
                # 移除标题后的[数字]后缀（如[19]）
                formatted_title = formatted_title.rsplit("[", 1)[0].rstrip()
                # 新增：移除末尾的 **
                formatted_title = formatted_title.rstrip("*").rstrip()
                all_new_titles.append(f"{global_index}. {formatted_title}")
                global_index += 1
            if global_index > max_titles:
                break

    # 3. 拼接最终内容（无任何冗余信息）
    if not all_new_titles:
        return f"{main_title}\n\n📭 暂无本次新增热点新闻"

    final_content = f"{main_title}\n\n" + "\n".join(all_new_titles)
    return final_content


# 保留RSS相关渲染函数，同步格式对齐（可选）
def render_rss_dingtalk_content(
    rss_items: list,
    feeds_info: Optional[Dict] = None,
    get_time_func: Optional[Callable[[], datetime]] = None,
    report_type: str = "RSS订阅更新"
) -> str:
    """渲染RSS钉钉通知内容（格式对齐）"""
    now = get_time_func() if get_time_func else datetime.now()
    main_title = f"**{now.strftime('%Y-%m-%d')} {report_type}**"
    
    all_rss_titles = []
    if rss_items:
        global_index = 1
        for item in rss_items:
            title = item.get("title", "")
            url = item.get("url", "")
            # 移除标题后缀
            title = title.rsplit("[", 1)[0].rstrip()
            # 新增：移除末尾的 **
            title = title.rstrip("*").rstrip()
            if url:
                all_rss_titles.append(f"{global_index}. [{title}]({url})")
            else:
                all_rss_titles.append(f"{global_index}. {title}")
            global_index += 1

    if not all_rss_titles:
        return f"{main_title}\n\n📭 暂无新的RSS订阅内容"
    
    return f"{main_title}\n\n" + "\n".join(all_rss_titles)


def render_rss_feishu_content(
    rss_items: list,
    feeds_info: Optional[Dict] = None,
    separator: str = "---",
    get_time_func: Optional[Callable[[], datetime]] = None,
    report_type: str = "RSS订阅更新"
) -> str:
    """渲染RSS飞书通知内容（格式对齐）"""
    now = get_time_func() if get_time_func else datetime.now()
    main_title = f"**{now.strftime('%Y-%m-%d')} {report_type}**"
    
    all_rss_titles = []
    if rss_items:
        global_index = 1
        for item in rss_items:
            title = item.get("title", "")
            url = item.get("url", "")
            # 移除标题后缀
            title = title.rsplit("[", 1)[0].rstrip()
            # 新增：移除末尾的 **
            title = title.rstrip("*").rstrip()
            if url:
                all_rss_titles.append(f"{global_index}. [{title}]({url})")
            else:
                all_rss_titles.append(f"{global_index}. {title}")
            global_index += 1

    if not all_rss_titles:
        return f"{main_title}\n\n📭 暂无新的RSS订阅内容"
    
    return f"{main_title}\n\n" + "\n".join(all_rss_titles)


def render_rss_markdown_content(
    rss_items: list,
    feeds_info: Optional[Dict] = None,
    get_time_func: Optional[Callable[[], datetime]] = None,
    report_type: str = "RSS订阅更新"
) -> str:
    """渲染RSS通用Markdown内容（格式对齐）"""
    now = get_time_func() if get_time_func else datetime.now()
    main_title = f"**{now.strftime('%Y-%m-%d')} {report_type}**"
    
    all_rss_titles = []
    if rss_items:
        global_index = 1
        for item in rss_items:
            title = item.get("title", "")
            url = item.get("url", "")
            # 移除标题后缀
            title = title.rsplit("[", 1)[0].rstrip()
            # 新增：移除末尾的 **
            title = title.rstrip("*").rstrip()
            if url:
                all_rss_titles.append(f"{global_index}. [{title}]({url})")
            else:
                all_rss_titles.append(f"{global_index}. {title}")
            global_index += 1

    if not all_rss_titles:
        return f"{main_title}\n\n📭 暂无新的RSS订阅内容"
    
    return f"{main_title}\n\n" + "\n".join(all_rss_titles)
