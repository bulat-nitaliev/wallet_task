import factory
from factory.django import DjangoModelFactory
from wallet.models import User, Wallet



class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_staff = True

class WalletFactory(DjangoModelFactory):
    class Meta:
        model = Wallet

    uuid = factory.Faker('uuid4')
    user = factory. Faker('pyint', min_value=0, max_value=1000)
    balance = factory.Faker('pyint', min_value=0, max_value=1000)