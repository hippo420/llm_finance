from utils.stock_registry import stock_registry

def resolve_stock_code(token: str) -> str | None:
    #종목 코드 직접 입력
    if token.isdigit():
        return token

    #In-Memory alias lookup
    return stock_registry.resolve(token)