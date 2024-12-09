from functools import wraps

from src.users.models import User


def restricted(func):
    # only those confirmed by the administrator can use the bot
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        user = User.objects.filter(id=user_id).first()
        if user and not user.is_bot_available:
            print('WARNING: Unauthorized access denied for {}.'.format(user_id))
            update.message.reply_text('User disallowed.')
            return
        return func(bot, update, *args, **kwargs)
    return wrapped
