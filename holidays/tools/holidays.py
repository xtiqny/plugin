from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class HolidaysTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        date = tool_parameters.get("date", "")
        
        if not date:
            yield self.create_json_message({
                "error": "Date parameter is required"
            })
            return
        
        # 调用 timor.tech API 查询节假日信息
        url = f"https://timor.tech/api/holiday/info/{date}"
        
        # 简化 headers，避免压缩导致的问题
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # 检查响应内容是否为空
            if not response.text or not response.text.strip():
                yield self.create_json_message({
                    "error": "Empty response from API",
                    "date": date
                })
                return
            
            # 尝试解析 JSON
            try:
                data = response.json()
            except ValueError as json_err:
                yield self.create_json_message({
                    "error": f"Invalid JSON response: {str(json_err)}",
                    "raw_response": response.text[:200],
                    "date": date
                })
                return
            
            # 解析 API 返回的数据
            holiday_data = data.get("holiday") or {}
            type_data = data.get("type") or {}
            
            result = {
                "date": date,
                "is_holiday": holiday_data.get("holiday", False) if isinstance(holiday_data, dict) else False,
                "holiday_name": holiday_data.get("name", "") if isinstance(holiday_data, dict) else "",
                "wage": holiday_data.get("wage", 0) if isinstance(holiday_data, dict) else 0,
                "rest_days": holiday_data.get("rest", 0) if isinstance(holiday_data, dict) else 0,
                "week_type": type_data.get("name", "") if isinstance(type_data, dict) else "",
                "week_number": type_data.get("week", 0) if isinstance(type_data, dict) else 0,
                "type": self._get_holiday_type(data),
                "raw_response": data
            }
            
            yield self.create_json_message(result)
            
        except requests.exceptions.Timeout:
            yield self.create_json_message({
                "error": "Request timeout",
                "date": date
            })
        except requests.exceptions.ConnectionError as e:
            yield self.create_json_message({
                "error": f"Connection error: {str(e)}",
                "date": date
            })
        except requests.exceptions.RequestException as e:
            yield self.create_json_message({
                "error": f"Failed to fetch holiday info: {str(e)}",
                "date": date
            })
        except Exception as e:
            yield self.create_json_message({
                "error": f"Unexpected error: {str(e)}",
                "date": date
            })
    
    def _get_holiday_type(self, data: dict) -> str:
        """
        根据 API 返回的数据判断日期类型
        """
        holiday = data.get("holiday")
        if isinstance(holiday, dict) and holiday.get("holiday"):
            return "holiday"
        
        type_data = data.get("type", {})
        if isinstance(type_data, dict):
            type_code = type_data.get("type", 0)
            if type_code == 2:
                return "holiday"
            elif type_code == 1:
                return "workday"
            elif type_code == 0:
                return "normal"
        
        return "unknown"
