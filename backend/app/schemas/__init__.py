from .user import User, UserCreate, UserUpdate, UserInDB
from .token import Token, TokenData
from .news import News, NewsCreate, NewsBase
from .prompt import Prompt, PromptCreate, PromptUpdate

# This makes imports cleaner - now you can do:
# from app.schemas import User, Token, etc.
# instead of:
# from app.schemas.user import User
# from app.schemas.token import Token
# etc.