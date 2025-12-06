# nlp/ner_extract.py
from underthesea import ner
import re

BAD_LOCATIONS = [
    "nhóm", "nhom",
    "tuần",
    "lớp", "lop",
    "đội", "doi",
    "ban",
    "tổ", "to",
    "họp", "hop",
    "làm", "lam",
    "gặp", "gap",
    "lúc", "luc",
    "09", "9", "10", "11",
]


def extract_ner(text: str):
    entities = ner(text)
    locations = []

    # -------------------------------------------------
    # 1. LOCATION từ Underthesea nhưng phải lọc blacklist
    # -------------------------------------------------
    for token, pos, chunk, entity in entities:
        if entity == "B-LOC":
            t = token.lower().strip()

            # loại bỏ nhầm lẫn
            if t in BAD_LOCATIONS:
                continue

            # bỏ token 1 kí tự hoặc toàn số
            if t.isdigit():
                continue

            locations.append(token)

    # -------------------------------------------------
    # 2. RULE-BASED
    # -------------------------------------------------
    # Cho phép phòng có tên bằng chữ hoặc số (phòng 101, phòng A)
    # \w+ sẽ khớp với chữ, số và dấu gạch dưới
    room = re.search(r"phòng\s+\w+", text.lower())
    if room:
        locations.append(room.group())

    # -------------------------------------------------
    # 3. RULE-BASED
    # -------------------------------------------------
    # Cải tiến: Dừng lại khi gặp các từ khóa thời gian (lúc, vào, ngày, thứ,...)
    at_match = re.search(r"(tại|ở)\s+([^,]+?)(?=\s+(?:lúc|vào|ngày|thứ)|$)", text.lower())
    if at_match:
        raw = at_match.group(2).strip()

        # Không cần split(",") nữa vì regex đã xử lý
        if raw not in BAD_LOCATIONS:
            locations.append(raw)

    # -------------------------------------------------
    # 4. ƯU TIÊN RULE → loại trùng → giữ cái đúng
    # -------------------------------------------------
    unique_locations = list(dict.fromkeys(locations))

    return {"locations": unique_locations}
