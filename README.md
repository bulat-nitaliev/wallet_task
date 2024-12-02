#  DEPOSIT or WITHDRAW

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

 приложение, которое по REST принимает запрос вида
POST api/v1/wallets/<WALLET_UUID>/operation
{
operationType: DEPOSIT or WITHDRAW,
amount: 1000
}
после выполнять логику по изменению счета в базе данных
также есть возможность получить баланс кошелька
GET api/v1/wallets/{WALLET_UUID}

## Getting Started <a name = "getting_started"></a>



### Installing



```
git clone https://github.com/bulat-nitaliev/wallet_task.git
```

And repeat

```
cd task
```

```
    sudo docker compose build
```

```
    sudo docker compose up
```
    ![Описание изображения](/Снимок экрана от 2024-11-16 10-16-12.png)

<image src="wallet_api.png" alt="Описание изображения">

<image src="deposit.png" alt="Описание изображения">

<image src="withdraw.png" alt="Описание изображения">
