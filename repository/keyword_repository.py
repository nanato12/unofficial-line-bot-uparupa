from random import choices
from typing import Optional

from constants.enums.authority import Authority
from database.models.keyword import Keyword
from database.models.user import User


def find_keywords_from_receive_text(s: str) -> list[Keyword]:
    return Keyword.query.filter(Keyword.receive_text == s).all()  # type: ignore[no-any-return]


def extract_admin_keyword(keywords: list[Keyword]) -> Optional[Keyword]:
    admin_keywords = [
        k for k in keywords if k.registrant.authority == Authority.ADMIN
    ]
    if admin_keywords:
        return admin_keywords[0]
    return None


def choice_keyword(keywords: list[Keyword]) -> Optional[Keyword]:
    """複数のキーワード候補から一つ絞り込む関数
    ---
    権限によって返信確率が定義されているため、確率が当たらなかった場合はNoneが返る

    Args:
        keywords (list[Keyword]): キーワード候補リスト

    Returns:
        Optional[Keyword]: キーワード
    """
    admin_keyword = extract_admin_keyword(keywords)
    if admin_keyword:
        return admin_keyword

    # 返信比率の重みづけを算出する（権限レベルxユーザーレベル）
    users: list[User] = [k.registrant for k in keywords]
    weights = [u.authority * u.level for u in users]

    # Noneの重み
    keywords.append(None)  # type: ignore[arg-type]
    weights.append(int(sum(weights) / 2))

    return choices(keywords, weights=weights)[0]


def find_keyword_from_user_and_text(u: User, text: str) -> Optional[Keyword]:
    keywords: list[Keyword] = u.keywords
    if filtered_keywords := list(
        filter(lambda x: x.receive_text == text, keywords)
    ):
        return filtered_keywords[0]
    return None


def check_registration_keyword(u: User, text: str) -> bool:
    return bool(find_keyword_from_user_and_text(u, text))
