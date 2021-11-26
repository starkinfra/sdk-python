# Stark Infra Python SDK

Welcome to the Stark Infra Python SDK! This tool is made for Python 
developers who want to easily integrate with our API.
This SDK version is compatible with the Stark Bank API v2.

If you have no idea what Stark Bank is, check out our [website](https://www.starkbank.com/) 
and discover a world where receiving or making payments 
is as easy as sending a text message to your client!

# Introduction

## Index

- [Introduction](#introduction)
    - [Supported Python versions](#supported-python-versions)
    - [API documentation](#stark-bank-api-documentation)
    - [Versioning](#versioning)
- [Setup](#setup)
    - [Install our SDK](#1-install-our-sdk)
    - [Create your Private and Public Keys](#2-create-your-private-and-public-keys)
    - [Register your user credentials](#3-register-your-user-credentials)
    - [Setting up the user](#4-setting-up-the-user)
    - [Setting up the error language](#5-setting-up-the-error-language)
- [Resource listing and manual pagination](#resource-listing-and-manual-pagination)
- [Testing in Sandbox](#testing-in-sandbox) 
- [Usage](#usage)
    - [Issuing](#issuing)
        - [Transactions](#query-issuing-transactions): Account statement entries
        - [Balance](#get-issuing-balance): Account balance
        - [Holders](#create-issuing-holders): Wallet Card holders
        - [BINs](#query-issuing-bins): Account sub-issue BINs
        - [Issuing Invoices](#create-issuing-invoices): Instutitions recognized by the Central Bank
        - [Withdrawals](#create-issuing-withdrawals): send money back to your Stark Bank account
        - [Cards](#create-issuing-cards): Create virtual Cards
        - [Purchases](#query-issuing-purchases): View your past purchases
- [Handling errors](#handling-errors)
- [Help and Feedback](#help-and-feedback)

### Supported Python Versions

This library supports the following Python versions:

* Python 2.7
* Python 3.4+

### Stark Infra API documentation

Feel free to take a look at our [API docs](https://www.starkinfra.com/docs/api).

### Versioning

This project adheres to the following versioning pattern:

Given a version number MAJOR.MINOR.PATCH, increment:

- MAJOR version when the **API** version is incremented. This may include backwards incompatible changes;
- MINOR version when **breaking changes** are introduced OR **new functionalities** are added in a backwards compatible manner;
- PATCH version when backwards compatible bug **fixes** are implemented.

# Setup

## 1. Install our SDK

1.1 To install the package with pip, run:

```sh
pip install starkinfra
```

1.2 To install from source, clone the repo and run:

```sh
python setup.py install
```

**Note**: This SDKs uses the starkbank SDK as its core dependency, so watch out for version and user conflicts if you are using both SDKs.
Also, the rest of this setup is pretty much the same as the starkbank SDK,so if you already use it, feel free to skip the rest of the section.

## 2. Create your Private and Public Keys

We use ECDSA. That means you need to generate a secp256k1 private
key to sign your requests to our API, and register your public key
with us so we can validate those requests.

You can use one of following methods:

2.1. Check out the options in our [tutorial](https://starkbank.com/faq/how-to-create-ecdsa-keys).

2.2. Use our SDK:

```python
import starkbank

privateKey, publicKey = starkbank.key.create()

# or, to also save .pem files in a specific path
privateKey, publicKey = starkbank.key.create("file/keys/")
```

**NOTE**: When you are creating new credentials, it is recommended that you create the
keys inside the infrastructure that will use it, in order to avoid risky internet
transmissions of your **private-key**. Then you can export the **public-key** alone to the
computer where it will be used in the new Project creation.

## 3. Register your user credentials

You can interact directly with our API using two types of users: Projects and Organizations.

- **Projects** are workspace-specific users, that is, they are bound to the workspaces they are created in.
One workspace can have multiple Projects.
- **Organizations** are general users that control your entire organization.
They can control all your Workspaces and even create new ones. The Organization is bound to your company's tax ID only.
Since this user is unique in your entire organization, only one credential can be linked to it.

3.1. To create a Project in Sandbox:

3.1.1. Log into [Starkbank Sandbox](https://web.sandbox.starkbank.com)

3.1.2. Go to Menu > Integrations

3.1.3. Click on the "New Project" button

3.1.4. Create a Project: Give it a name and upload the public key you created in section 2

3.1.5. After creating the Project, get its Project ID

3.1.6. Use the Project ID and private key to create the object below:

```python
import starkinfra

# Get your private key from an environment variable or an encrypted database.
# This is only an example of a private key content. You should use your own key.
private_key_content = """
-----BEGIN EC PARAMETERS-----
BgUrgQQACg==
-----END EC PARAMETERS-----
-----BEGIN EC PRIVATE KEY-----
MHQCAQEEIMCwW74H6egQkTiz87WDvLNm7fK/cA+ctA2vg/bbHx3woAcGBSuBBAAK
oUQDQgAE0iaeEHEgr3oTbCfh8U2L+r7zoaeOX964xaAnND5jATGpD/tHec6Oe9U1
IF16ZoTVt1FzZ8WkYQ3XomRD4HS13A==
-----END EC PRIVATE KEY-----
"""

project = starkinfra.Project(
    environment="sandbox",
    id="5656565656565656",
    private_key=private_key_content
)
```

3.2. To create Organization credentials in Sandbox:

3.2.1. Log into [Starkbank Sandbox](https://web.sandbox.starkbank.com)

3.2.2. Go to Menu > Integrations

3.2.3. Click on the "Organization public key" button

3.2.4. Upload the public key you created in section 2 (only a legal representative of the organization can upload the public key)

3.2.5. Click on your profile picture and then on the "Organization" menu to get the Organization ID

3.2.6. Use the Organization ID and private key to create the object below:

```python
import starkinfra

# Get your private key from an environment variable or an encrypted database.
# This is only an example of a private key content. You should use your own key.
private_key_content = """
-----BEGIN EC PARAMETERS-----
BgUrgQQACg==
-----END EC PARAMETERS-----
-----BEGIN EC PRIVATE KEY-----
MHQCAQEEIMCwW74H6egQkTiz87WDvLNm7fK/cA+ctA2vg/bbHx3woAcGBSuBBAAK
oUQDQgAE0iaeEHEgr3oTbCfh8U2L+r7zoaeOX964xaAnND5jATGpD/tHec6Oe9U1
IF16ZoTVt1FzZ8WkYQ3XomRD4HS13A==
-----END EC PRIVATE KEY-----
"""

organization = starkinfra.Organization(
    environment="sandbox",
    id="5656565656565656",
    private_key=private_key_content,
    workspace_id=None,  # You only need to set the workspace_id when you are operating a specific workspace_id
)

# To dynamically use your organization credentials in a specific workspace_id,
# you can use the Organization.replace() function:
balance = starkinfra.issuingbalance.get(user=starkinfra.Organization.replace(organization, "4848484848484848")
```

NOTE 1: Never hard-code your private key. Get it from an environment variable or an encrypted database.

NOTE 2: We support `'sandbox'` and `'production'` as environments.

NOTE 3: The credentials you registered in `sandbox` do not exist in `production` and vice versa.


## 4. Setting up the user

There are three kinds of users that can access our API: **Organization**, **Project** and **Member**.

- `Project` and `Organization` are designed for integrations and are the ones meant for our SDKs.
- `Member` is the one you use when you log into our webpage with your e-mail.

There are two ways to inform the user to the SDK:

4.1 Passing the user as argument in all functions:

```python
import starkinfra

balance = starkinfra.issuingbalance.get(user=project)  # or organization
```

4.2 Set it as a default user in the SDK:

```python
import starkinfra

starkinfra.user = project  # or organization

balance = starkinfra.issuingbalance.get()
```

Just select the way of passing the user that is more convenient to you.
On all following examples we will assume a default user has been set.

## 5. Setting up the error language

The error language can also be set in the same way as the default user:

```python
import starkbank

starkbank.language = "en-US"
```

Language options are "en-US" for english and "pt-BR" for brazilian portuguese. English is default.

## Resource listing and manual pagination

Almost all SDK resources provide a `query` and a `page` function.

- The `query` function provides a straight forward way to efficiently iterate through all results that match the filters you inform,
seamlessly retrieving the next batch of elements from the API only when you reach the end of the current batch.
If you are not worried about data volume or processing time, this is the way to go.

```python
import starkinfra

for transaction in starkinfra.issuingtransaction.query(limit=200):
    print(transaction)
```

- The `page` function gives you full control over the API pagination. With each function call, you receive up to
100 results and the cursor to retrieve the next batch of elements. This allows you to stop your queries and
pick up from where you left off whenever it is convenient. When there are no more elements to be retrieved, the returned cursor will be `None`.

```python
import starkinfra

cursor = None
while True:
    transactions, cursor = starkinfra.issuingtransaction.page(limit=50, cursor=cursor)
    for transaction in transactions:
        print(transaction)
    if cursor is None:
        break
```

To simplify the following SDK examples, we will only use the `query` function, but feel free to use `page` instead.

# Testing in Sandbox

Your initial balance is zero. For many operations in Stark Infra, you'll need funds
in your account, which can be added to your balance by creating an Invoice or a Boleto. 

In the Sandbox environment, most of the created Invoices and Boletos will be automatically paid,
so there's nothing else you need to do to add funds to your account. Just create
a few Invoices and wait around a bit.

In Production, you (or one of your clients) will need to actually pay this Invoice or Boleto
for the value to be credited to your account.


# Usage

Here are a few examples on how to use the SDK. If you have any doubts, use the built-in
`help()` function to get more info on the desired functionality
(for example: `help(starkinfra.issuingtransaction.create)`)

## Issuing

### Query issuing transactions

To understand your balance changes (issuing statement), you can query
transactions. Note that our system creates transactions for you when
you receive boleto payments, pay a bill or make transfers, for example.

```python
import starkinfra

transactions = starkinfra.issuingtransaction.query(
    after="2020-01-01",
    before="2020-03-01"
)
for transaction in transactions:
    print(transaction)
```

### Get an issuing transaction

You can get a specific transaction by its id:

```python
import starkinfra

transaction = starkinfra.issuingtransaction.get("5155165527080960")

print(transaction)
```

### Get issuing balance

To know how much money you have in your workspace, run:

```python
import starkinfra

balance = starkinfra.issuingbalance.get()

print(balance)
```

### Create issuing holders

You can create card holders to your Workspace.

```python
import starkinfra
from datetime import datetime, timedelta

holders = starkinfra.issuingholder.create([
    starkinfra.IssuingHolder(
        name="Iron Bank S.A.",
        external_id="1234",
        tax_id="012.345.678-90",
        tags=[
            "Traveler Employee"
        ],
        rules=[
            {
                "name": "General USD",
                "interval": "day",
                "amount": 100000,
                "currencyCode": "USD"
            }
        ]
    )
])

for holder in holders:
    print(holder)
```

**Note**: Instead of using IssuingHolder objects, you can also pass each transfer element in dictionary format

### Query issuing holders

You can query multiple transfers according to filters.

```python
import starkinfra

holders = starkinfra.issuingholder.query()

for holder in holders:
    print(holder)
```

### Delete an issuing holder

To cancel a single issuing holder by its id, run:

```python
import starkinfra

holder = starkinfra.issuingholder.delete("5155165527080960")

print(holder)
```

### Get an issuing holder

To get a single issuing holder by its id, run:

```python
import starkinfra

holder = starkinfra.issuingholder.get("5155165527080960")

print(holder)
```

### Query issuing holder logs

You can query transfer logs to better understand transfer life cycles.

```python
import starkinfra

logs = starkinfra.issuingholder.log.query(limit=50)

for log in logs:
    print(log.id)
```

### Get an issuing holder log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.issuingholder.log.get("5155165527080960")

print(log)
```

### Query issuing BINs

To take a look at the sub-issuer BINs linked to your workspace, just run the following:

```python
import starkinfra

bins = starkinfra.issuingbin.query()
for bin in bins:
    print(bin)
```

### Create issuing invoices

You can create dynamic QR Code invoices to receive money from accounts you have in other banks to your Issuing account.

Since the banking system only understands value modifiers (discounts, fines and interest) when dealing with **dates** (instead of **datetimes**), these values will only show up in the end user banking interface if you use **dates** in the "due" and "discounts" fields. 

If you use **datetimes** instead, our system will apply the value modifiers in the same manner, but the end user will only see the final value to be paid on his interface.

Also, other banks will most likely only allow payment scheduling on invoices defined with **dates** instead of **datetimes**.

```python
# coding: utf-8
import starkinfra

invoices = starkinfra.issuinginvoice.create([
    IssuingInvoice(
        amount=1000,
    )
])

for invoice in invoices:
    print(invoice)
```

**Note**: Instead of using Invoice objects, you can also pass each invoice element in dictionary format

### Get an issuing invoice

After its creation, information on an invoice may be retrieved by its id. 
Its status indicates whether it's been paid.

```python
import starkinfra

invoice = starkinfra.issuinginvoice.get("5155165527080960")

print(invoice)
```

### Query issuing invoices

You can get a list of created invoices given some filters.

```python
import starkinfra
from datetime import datetime

invoices = starkinfra.issuinginvoice.query(
    after=datetime(2020, 1, 1),
    before=datetime(2020, 3, 1)
)

for invoice in invoices:
    print(invoice)
```

### Query issuing invoice logs

Logs are pretty important to understand the life cycle of an invoice.

```python
import starkinfra

logs = starkinfra.issuinginvoice.log.query(limit=150)

for log in logs:
    print(log)
```

### Get an issuing invoice log

You can get a single log by its id.

```python
import starkinfra

log = starkinfra.issuinginvoice.log.get("5155165527080960")

print(log)
```

### Create issuing withdrawals

You can create withdrawals to send back cash to your Banking account by using the Withdrawal resource

```python
# coding: utf-8
import starkinfra

withdrawals = starkinfra.issuingwithdrawal.create([
    starkinfra.IssuingWithdrawal(
        amount=10000,
        external_id="123",
        description="Sending back"
    )
])

for withdrawal in withdrawals:
    print(withdrawal)
```

**Note**: Instead of using Withdrawal objects, you can also pass each withdrawal element in dictionary format

### Get an issuing withdrawal

After its creation, information on an withdrawal may be retrieved by its id.

```python
import starkinfra

invoice = starkinfra.issuingwithdrawal.get("5155165527080960")

print(invoice)
```

### Query issuing withdrawals

You can get a list of created invoices given some filters.

```python
import starkinfra
from datetime import datetime

withdrawals = starkinfra.issuingwithdrawal.query(
    after=datetime(2020, 1, 1),
    before=datetime(2020, 3, 1)
)

for withdrawal in withdrawals:
    print(withdrawal)
```

### Create issuing cards

You can create boletos to charge customers or to receive money from accounts
you have in other banks.

```python
# coding: utf-8
import starkinfra
from datetime import datetime


cards = starkinfra.issuingcard.create([
    {
        "holderName": "Developers",
        "holderTaxId": "012.345.678-90",
        "holderExternalId": "1234"
    }
])

for card in cards:
    print(card)
```

### Query issuing cards

You can get a list of created cards given some filters.

```python
import starkinfra
from datetime import datetime

cards = starkinfra.issuingcard.query(
    after=datetime(2020, 1, 1),
    before=datetime(2020, 3, 1)
)

for card in cards:
    print(card)
```

### Get an issuing card

After its creation, information on a card may be retrieved by its id.

```python
import starkinfra

card = starkinfra.issuingcard.get("5155165527080960")

print(card)
```

### Delete an issuing card

You can also cancel a card by its id.
Note that this is not possible if it has been processed already.

```python
import starkinfra

card = starkinfra.issuingcard.delete("5155165527080960")

print(card)
```

### Query issuing card logs

Logs are pretty important to understand the life cycle of a card.

```python
import starkinfra

logs = starkinfra.issuingcard.log.query(limit=150)

for log in logs:
    print(log)
```

### Get an issuing card log

You can get a single log by its id.

```python
import starkinfra

log = starkinfra.issuingcard.log.get("5155165527080960")

print(log)
```


### Query issuing purchases

You can get a list of created purchases given some filters.

```python
import starkinfra
from datetime import datetime

purchases = starkinfra.issuingpurchase.query(
    after=datetime(2020, 1, 1),
    before=datetime(2020, 3, 1)
)

for purchase in purchases:
    print(purchase)
```

### Get an issuing purchase

After its creation, information on a purchase may be retrieved by its id. 

```python
import starkinfra

purchase = starkinfra.issuingpurchase.get("5155165527080960")

print(purchase)
```

### Query issuing purchase logs

Logs are pretty important to understand the life cycle of a purchase.

```python
import starkinfra

logs = starkinfra.issuingpurchase.log.query(limit=150)

for log in logs:
    print(log)
```

### Get an issuing purchase log

You can get a single log by its id.

```python
import starkinfra

log = starkinfra.issuingpurchase.log.get("5155165527080960")

print(log)
```

**Note**: the Organization user can only update a workspace with the Workspace ID set.

# Handling errors

The SDK may raise one of four types of errors: __InputErrors__, __InternalServerError__, __UnknownError__, __InvalidSignatureError__

__InputErrors__ will be raised whenever the API detects an error in your request (status code 400).
If you catch such an error, you can get its elements to verify each of the
individual errors that were detected in your request by the API.
For example:

```python
import starkbank
import starkinfra

try:
    withdrawals = starkinfra.issuingwithdrawal.create([
        starkinfra.IssuingWithdrawal(
            amount=99999999999999,  # (R$ 999,999,999,999.99)
            external_id="123",  # so we can block anything you send twice by mistake
            description="Sending back"
        ),
    ])
except starkbank.error.InputErrors as exception:
    for error in exception.errors:
        print(error.code)
        print(error.message)
```

__InternalServerError__ will be raised if the API runs into an internal error.
If you ever stumble upon this one, rest assured that the development team
is already rushing in to fix the mistake and get you back up to speed.

__UnknownError__ will be raised if a request encounters an error that is
neither __InputErrors__ nor an __InternalServerError__, such as connectivity problems.

__InvalidSignatureError__ will be raised specifically by starkbank.event.parse()
when the provided content and signature do not check out with the Stark Bank public
key.

# Help and Feedback

If you have any questions about our SDK, just send us an email.
We will respond you quickly, pinky promise. We are here to help you integrate with us ASAP.
We also love feedback, so don't be shy about sharing your thoughts with us.

Email: developers@starkbank.com
