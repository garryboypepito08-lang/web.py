import re


def escape_report_text(value):
    if value is None:
        return ""
    return re.sub(r"[<>&\"']", lambda m: {
        '<': '&lt;',
        '>': '&gt;',
        '&': '&amp;',
        '"': '&quot;',
        "'": '&#39;'
    }[m.group(0)], str(value))


def report_download_name(title):
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", str(title or "report")).strip("._")
    return safe or "report"
