from datetime import timedelta

from django.conf import settings
from django.db.models import OuterRef, Func, F, Subquery, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.utils.translation import gettext as _

from telegram_django_bot.routing import telegram_reverse
from telegram_django_bot.td_viewset import TelegramViewSet
from telegram_django_bot.telegram_lib_redefinition import InlineKeyboardButtonDJ
from telegram_django_bot.utils import handler_decor
from telegram_django_bot.tg_dj_bot import TG_DJ_Bot

from telegram import Update

from src.software.decorator import restricted
from src.software.forms import SoftwareForm, LicenseForm, OrderForm
from src.software.models import Software, License, Order
from src.users.models import User


@handler_decor()
@restricted
def start(bot: TG_DJ_Bot, update: Update, user: User):
    User.objects.get_or_create(id=user.id)
    message = f'Привет, {user.first_name or user.telegram_username}! ' \
              f'Я бот 🤖, который помогает управлять лицензиями для софта.'
    buttons = [
        [InlineKeyboardButtonDJ(
            text=_('💻 Софт'),
            callback_data=SoftwareViewSet(telegram_reverse('software:SoftwareViewSet')).gm_callback_data('show_list'),
        )],
        [InlineKeyboardButtonDJ(
            text=_('📈 Статистика'),
            callback_data=f'show_statistics/',
        )],
    ]
    return bot.edit_or_send(update, message, buttons)


@handler_decor()
def show_statistics(bot: TG_DJ_Bot, update: Update, user: User):
    buttons = [
        [InlineKeyboardButtonDJ(
            text=_('ТОП 10 самых продаваемых soft за 1 год'),
            callback_data=TopForYearViewSet(telegram_reverse('software:TopForYearViewSet')).gm_callback_data(
                'show_list',
            ),
        )],
        [InlineKeyboardButtonDJ(
            text=_('ТОП 10 самых продаваемых soft за 1 месяц'),
            callback_data=TopForMonthViewSet(telegram_reverse('software:TopForMonthViewSet')).gm_callback_data(
                'show_list',
            ),
        )],
        [InlineKeyboardButtonDJ(
            text=_('ТОП 10 самых продаваемых soft за 1 неделю'),
            callback_data=TopForWeekViewSet(telegram_reverse('software:TopForWeekViewSet')).gm_callback_data(
                'show_list',
            ),
        )],
        [InlineKeyboardButtonDJ(
            text=_('Сумма продаж по месяцам за год'),
            callback_data=OrderSumViewSet(telegram_reverse('software:OrderSumViewSet')).gm_callback_data(
                'show_list',
            ),
        )],
        [InlineKeyboardButtonDJ(
            text=_('🔙 Back'),
            callback_data=f'show_statistics/',
        )],
    ]
    message = '💻 Здесь Вы можете посмотреть статистику продаж: '
    return bot.edit_or_send(update, message, buttons)


class SoftwareViewSet(TelegramViewSet):
    viewset_name = 'Software'
    model_form = SoftwareForm
    queryset = Software.objects.all()
    actions = ['create', 'change', 'delete', 'show_elem', 'show_list']

    def show_elem(self, model_or_pk, mess=''):
        # generate content
        model = self.get_orm_model(model_or_pk)

        # generate view of content
        if model:
            if self.use_name_and_id_in_elem_showing:
                mess += f'{self.viewset_name} #{model.pk} \n'
            mess += self.gm_show_elem_or_list_fields(model, is_elem=True)

            buttons = self.gm_show_elem_create_buttons(model)
            buttons += [
                [InlineKeyboardButtonDJ(
                    text=_('📄 Список лицензией'),
                    callback_data=LicenseViewSet(telegram_reverse('software:LicenseViewSet')).gm_callback_data(
                        'show_list', model.pk)
                )],
            ]
            return self.CHAT_ACTION_MESSAGE, (mess, buttons)
        else:
            return self.gm_no_elem(model_or_pk)

    def show_list(self, page=0, per_page=10, columns=1, *args, **kwargs):
        __, (mess, buttons) = super().show_list(page, per_page, columns)
        buttons += [
            [InlineKeyboardButtonDJ(
                text=_('➕ Add'),
                callback_data=self.gm_callback_data('create')
            )],
            [InlineKeyboardButtonDJ(
                text=_('🔙 Back'),
                callback_data=settings.TELEGRAM_BOT_MAIN_MENU_CALLBACK
            )],
        ]
        return self.CHAT_ACTION_MESSAGE, (mess, buttons)


class LicenseViewSet(TelegramViewSet):
    viewset_name = 'Лицензия'
    model_form = LicenseForm
    queryset = License.objects.all()
    foreign_filter_amount = 1
    updating_fields = ['period_activity', 'status', 'price']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.foreign_filters[0]:
            queryset = queryset.filter(software=self.foreign_filters[0])
        return queryset

    def create(self, field=None, value=None, initial_data=None):
        initial_data = {
            'software': self.foreign_filters[0],
        }
        return super().create(field, value, initial_data)

    def show_list(self, page=0, per_page=10, columns=1, *args, **kwargs):
        __, (mess, buttons) = super().show_list(page, per_page, columns)
        buttons += [
            [InlineKeyboardButtonDJ(
                text=_('➕ Add'),
                callback_data=self.gm_callback_data('create')
            )],
            [InlineKeyboardButtonDJ(
                text=_('🔙 Back'),
                callback_data=SoftwareViewSet(
                    telegram_reverse('software:SoftwareViewSet'),
                ).gm_callback_data('show_list'),
            )],
        ]
        return self.CHAT_ACTION_MESSAGE, (mess, buttons)

    def show_elem(self, model_or_pk, mess=''):
        # generate content
        model = self.get_orm_model(model_or_pk)

        # generate view of content
        if model:
            if self.use_name_and_id_in_elem_showing:
                mess += f'{self.viewset_name} #{model.pk} \n'
            mess += self.gm_show_elem_or_list_fields(model, is_elem=True)

            buttons = self.gm_show_elem_create_buttons(model)
            buttons += [
                [InlineKeyboardButtonDJ(
                    text=_('🛒 Купить лицензию'),
                    callback_data=OrderViewSet(telegram_reverse('software:OrderViewSet')).gm_callback_data(
                        'create', model.pk)
                )],
            ]
            return self.CHAT_ACTION_MESSAGE, (mess, buttons)
        else:
            return self.gm_no_elem(model_or_pk)


class OrderViewSet(TelegramViewSet):
    viewset_name = 'Покупка'
    actions = ['create']
    model_form = OrderForm
    queryset = Order.objects.all()
    foreign_filter_amount = 1

    def create(self, field=None, value=None, initial_data=None):
        price = License.objects.get(id=self.foreign_filters[0]).price
        initial_data = {
            'license': self.foreign_filters[0],
            'user': self.user,
            'price': price,
        }
        return super().create(field, value, initial_data)


class TopForBaseViewSet(TelegramViewSet):
    queryset = Software.objects.all()
    actions = ['show_list']
    model_form = SoftwareForm

    def show_list(self, page=0, per_page=10, columns=1, *args, **kwargs):
        __, (mess, buttons) = super().show_list(page, per_page, columns)
        buttons = [
            [InlineKeyboardButtonDJ(
                text=_('🔙 Back'),
                callback_data=f'show_statistics/',
            )],
        ]
        return self.CHAT_ACTION_MESSAGE, (mess, buttons)


class TopForYearViewSet(TopForBaseViewSet):
    viewset_name = 'ТОП за год'

    def get_queryset(self):
        orders = Order.objects.filter(
            license__software_id=OuterRef('pk'),
            created_at__year=timezone.now().year,
        ).annotate(count=Func(F('id'), function='Count')).values('count')
        return Software.objects.annotate(num_orders=Subquery(orders)).order_by('-num_orders')[:10]


class TopForMonthViewSet(TopForBaseViewSet):
    viewset_name = 'ТОП за месяц'

    def get_queryset(self):
        orders = Order.objects.filter(
            license__software_id=OuterRef('pk'),
            created_at__month=timezone.now().month,
        ).annotate(count=Func(F('id'), function='Count')).values('count')
        return Software.objects.annotate(num_orders=Subquery(orders)).order_by('-num_orders')[:10]


class TopForWeekViewSet(TopForBaseViewSet):
    viewset_name = 'ТОП за неделю'

    def get_queryset(self):
        week_ago = timezone.now() - timedelta(days=7)
        orders = Order.objects.filter(
            license__software_id=OuterRef('pk'),
            created_at__gte=week_ago,
        ).annotate(count=Func(F('id'), function='Count')).values('count')
        return Software.objects.annotate(num_orders=Subquery(orders)).order_by('-num_orders')[:10]


class OrderSumViewSet(TelegramViewSet):
    viewset_name = 'Сумма продаж по месяцам за год'
    queryset = Order.objects.all()
    actions = ['show_list']
    model_form = OrderForm

    def get_queryset(self):
        return Order.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(summa=Sum('price'))

    def gm_show_list_button_names(self, it_m, model):
        return f'{it_m}'

    def gm_show_elem_or_list_fields(self, **kwargs):
        mess = ''
        for data in self.get_queryset():
            for key in data:
                value = data[key]
                try:
                    value = value.month
                except AttributeError:
                    pass
                mess += f'<b>{key}</b>: {value}\n'
        return mess

    def gm_show_list_elem_info(self, **kwargs) -> str:
        mess = self.gm_show_elem_or_list_fields()
        return mess

    def show_list(self, page=0, per_page=10, columns=1, *args, **kwargs):
        mess = self.gm_show_list_elem_info()

        buttons = [
            [InlineKeyboardButtonDJ(
                text=_('🔙 Back'),
                callback_data=f'show_statistics/',
            )],
        ]
        return self.CHAT_ACTION_MESSAGE, (mess, buttons)
