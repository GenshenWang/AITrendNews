# coding=utf-8
"""
消息分批处理模块

提供消息内容分批拆分功能，确保消息大小不超过各平台限制
核心格式：加粗日期主标题 + 全局连续序号. 标题（链接）
"""

from datetime import datetime
from typing import Dict, List, Optional, Callable

from trendradar.report.formatter import format_title_for_platform

# 默认批次大小配置（保留核心平台限制）
DEFAULT_BATCH_SIZES = {
    "dingtalk": 20000,
    "feishu": 29000,
    "ntfy": 3800,
    "default": 4000,
}


def split_content_into_batches(
    report_data: Dict,
    format_type: str,
    update_info: Optional[Dict] = None,
    max_bytes: Optional[int] = None,
    mode: str = "daily",
    batch_sizes: Optional[Dict[str, int]] = None,
    feishu_separator: str = "---",
    region_order: Optional[List[str]] = None,
    get_time_func: Optional[Callable[[], datetime]] = None,
    rss_items: Optional[list] = None,
    rss_new_items: Optional[list] = None,
    timezone: str = "Asia/Shanghai",
    display_mode: str = "keyword",
    ai_content: Optional[str] = None,
    standalone_data: Optional[Dict] = None,
    rank_threshold: int = 10,
    ai_stats: Optional[Dict] = None,
    report_type: str = "AI热门资讯",
    show_new_section: bool = True,
) -> List[str]:
    """
    分批处理消息内容（仅保留新增新闻）
    核心格式：**YYYY-MM-DD AI热门资讯** + 全局连续序号. 标题（链接）
    """
    # 合并批次大小配置
    sizes = {**DEFAULT_BATCH_SIZES, **(batch_sizes or {})}
    if max_bytes is None:
        max_bytes = sizes.get(format_type, sizes["default"])

    batches = []
    now = get_time_func() if get_time_func else datetime.now()
    # 核心修改1：重构主标题（仅保留日期+AI热门资讯，加粗）
    main_title = f"**{now.strftime('%Y-%m-%d')} {report_type}**"
    
    # 核心修改2：扁平化提取所有新增新闻，生成全局序号列表
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
                    format_type, title_data_copy, show_source=False
                )
                # 移除标题后的[数字]后缀（如[19]）
                formatted_title = formatted_title.rsplit("[", 1)[0].rstrip()
                # 移除末尾的 **
                formatted_title = formatted_title.rstrip("*").rstrip()
                all_new_titles.append(f"{global_index}. {formatted_title}")
                global_index += 1
            if global_index > max_titles:
                break

    # 核心修改3：分批处理（仅处理新增新闻，忽略所有其他区块）
    if not all_new_titles:
        # 无内容时返回主标题+提示
        return [f"{main_title}\n\n📭 暂无本次新增热点新闻"]

    # 初始化当前批次
    current_batch = main_title + "\n\n"
    current_batch_size = len(current_batch.encode("utf-8"))

    for line in all_new_titles:
        line_bytes = len(line.encode("utf-8")) + 1  # +1 是换行符
        
        # 检查是否超出批次大小限制
        if current_batch_size + line_bytes > max_bytes:
            # 超出限制，完成当前批次
            batches.append(current_batch.rstrip("\n"))
            # 开启新批次，重置状态
            current_batch = main_title + "\n\n" + line + "\n"
            current_batch_size = len(current_batch.encode("utf-8"))
        else:
            # 未超出限制，添加到当前批次
            current_batch += line + "\n"
            current_batch_size += line_bytes

    # 完成最后一个批次
    if current_batch.strip() != main_title:
        batches.append(current_batch.rstrip("\n"))

    return batches


# 以下辅助函数全部删除，因为我们不再处理其他区块
# 如需保留，可单独提取，但当前核心逻辑已完全重构
