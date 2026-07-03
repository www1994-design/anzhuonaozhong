from ctparse import ctparse
from datetime import datetime
import re


class NLPParser:
    def __init__(self):
        pass

    def parse(self, text):
        result = {
            'time': None,
            'location': None,
            'title': None,
            'description': text
        }
        try:
            now = datetime.now()
            parsed = ctparse(text, now=now)
            if parsed and parsed.resolved_datetime:
                result['time'] = parsed.resolved_datetime.strftime("%Y-%m-%d %H:%M")
        except Exception as e:
            print(f"时间解析失败: {e}")
            result['time'] = self._fallback_time_extract(text)

        location_patterns = [
            r'在([\u4e00-\u9fa5a-zA-Z0-9\s]+?)(?:开会|见面|吃饭|讨论|集合)',
            r'去([\u4e00-\u9fa5a-zA-Z0-9\s]+?)(?:开会|见面|吃饭|讨论|集合)',
            r'地点[：:]\s*([\u4e00-\u9fa5a-zA-Z0-9\s]+)',
        ]
        for pattern in location_patterns:
            match = re.search(pattern, text)
            if match:
                result['location'] = match.group(1).strip()
                break

        result['title'] = text[:20] + "..." if len(text) > 20 else text
        return result

    def _fallback_time_extract(self, text):
        if '明天' in text:
            from datetime import timedelta
            tomorrow = datetime.now() + timedelta(days=1)
            return tomorrow.strftime("%Y-%m-%d 09:00")
        from datetime import timedelta
        default_time = datetime.now() + timedelta(hours=1)
        return default_time.strftime("%Y-%m-%d %H:%M")