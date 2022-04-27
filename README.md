# Stark Infra Python SDK - Beta

Welcome to the Stark Infra Python SDK! This tool is made for Python 
developers who want to easily integrate with our API.
This SDK version is compatible with the Stark Infra API v2.

# Introduction

## Index

- [Introduction](#introduction)
    - [Supported Python versions](#supported-python-versions)
    - [API documentation](#stark-infra-api-documentation)
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
        - [Authorizations](#process-authorizations): Respond card purchase authorization requests
        - [Balance](#get-your-issuingbalance): View your issuing balance
        - [Transactions](#query-issuingtransactions): View the transactions that have affected your issuing balance
        - [Holders](#create-issuingholders): Manage card holders
        - [BINs](#query-issuingbins): View available sub-issuer BINs (a.k.a. card number ranges)
        - [Invoices](#create-issuinginvoices): Add money to your issuing balance
        - [Withdrawals](#create-issuingwithdrawals): Send money back to your Workspace from your issuing balance
        - [Cards](#create-issuingcards): Create virtual and/or physical cards
        - [Purchases](#query-issuingpurchases): View your past purchases
    - [Pix](#pix)
        - [PixRequests](#create-pixrequests): Create Pix transactions
        - [PixReversals](#create-pixreversals): Reverse Pix transactions
        - [PixBalance](#get-pixbalance): View your account balance
        - [PixStatement](#create-pixstatement): Request your account statement
        - [PixKey](#create-a-pix-key): Create a Pix Key
        - [PixClaim](#create-a-pix-claim): Claim a Pix Key
    - [Credit Note](#credit-note)
        - [CreditNote](#create-creditnotes): Create credit notes
    - [WebhookEvents](#process-webhook-events): Manage Webhook events
- [Handling errors](#handling-errors)
- [Help and Feedback](#help-and-feedback)

## Supported Python Versions

This library supports the following Python versions:

* Python 2.7
* Python 3.4+

## Stark Infra API documentation

Feel free to take a look at our [API docs](https://www.starkinfra.com/docs/api).

## Versioning

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

## 2. Create your Private and Public Keys

We use ECDSA. That means you need to generate a secp256k1 private
key to sign your requests to our API, and register your public key
with us, so we can validate those requests.

You can use one of the following methods:

2.1. Check out the options in our [tutorial](https://starkbank.com/faq/how-to-create-ecdsa-keys). 

2.2. Use our SDK:

```python
import starkinfra

privateKey, publicKey = starkinfra.key.create()

# or, to also save .pem files in a specific path
privateKey, publicKey = starkinfra.key.create("file/keys/")
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

3.1.1. Log into [StarkInfra Sandbox](https://web.sandbox.starkinfra.com)

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

3.2.1. Log into [Starkinfra Sandbox](https://web.sandbox.starkinfra.com)

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

```

NOTE 1: Never hard-code your private key. Get it from an environment variable or an encrypted database.

NOTE 2: We support `'sandbox'` and `'production'` as environments.

NOTE 3: The credentials you registered in `sandbox` do not exist in `production` and vice versa.


## 4. Setting up the user

There are three kinds of users that can access our API: **Organization**, **Project**, and **Member**.

- `Project` and `Organization` are designed for integrations and are the ones meant for our SDKs.
- `Member` is the one you use when you log into our webpage with your e-mail.

There are two ways to inform the user to the SDK:

4.1 Passing the user as an argument in all functions:

```python
import starkinfra

balance = starkinfra.pixbalance.get(user=project)  # or organization
```

4.2 Set it as a default user in the SDK:

```python
import starkinfra

starkinfra.user = project  # or organization

balance = starkinfra.pixbalance.get()
```

Just select the way of passing the user that is more convenient to you.
On all following examples, we will assume a default user has been set.

## 5. Setting up the error language

The error language can also be set in the same way as the default user:

```python
import starkinfra

starkinfra.language = "en-US"
```

Language options are "en-US" for English and "pt-BR" for Brazilian Portuguese. English is the default.

# Resource listing and manual pagination

Almost all SDK resources provide a `query` and a `page` function.

- The `query` function provides a straightforward way to efficiently iterate through all results that match the filters you inform,
seamlessly retrieving the next batch of elements from the API only when you reach the end of the current batch.
If you are not worried about data volume or processing time, this is the way to go.

```python
import starkinfra

for request in starkinfra.pixrequest.query(limit=200):
    print(request)
```

- The `page` function gives you full control over the API pagination. With each function call, you receive up to
100 results and the cursor to retrieve the next batch of elements. This allows you to stop your queries and
pick up from where you left off whenever it is convenient. When there are no more elements to be retrieved, the returned cursor will be `None`.

```python
import starkinfra

cursor = None
while True:
    requests, cursor = starkinfra.pixrequest.page(limit=50, cursor=cursor)
    for request in requests:
        print(request)
    if cursor is None:
        break
```

To simplify the following SDK examples, we will only use the `query` function, but feel free to use `page` instead.

# Testing in Sandbox

Your initial balance is zero. For many operations in Stark Infra, you'll need funds
in your account, which can be added to your balance by creating a Pix Request. 

In the Sandbox environment, most of the created Pix Requests will be automatically paid,
so there's nothing else you need to do to add funds to your account. Just create
a few Pix Request and wait around a bit.

In Production, you (or one of your clients) will need to actually pay this Pix Request
for the value to be credited to your account.


# Usage

Here are a few examples on how to use the SDK. If you have any doubts, use the built-in
`help()` function to get more info on the desired functionality
(for example: `help(starkinfra.issuinginvoice.create)`)

## Issuing

### Process Authorizations

It's easy to process Authorizations delivered to your Webhook endpoint. 

If you do not approve or decline the authorization within 2 seconds, the authorization will be denied.

```python
import starkinfra

request = listen()  # this is the method you made to get the events posted to your webhook endpoint

authorization = starkinfra.issuingauthorization.parse(
    content=request.data.decode("utf-8"),
    signature=request.headers["Digital-Signature"],
)

sendResponse(  # you should also implement this method
    starkinfra.issuingauthorization.response(  # this optional method just helps you build the response JSON
        status="accepted",
        amount=authorization.amount,
        tags=["my-purchase-id/123"],
    )
)

# or 

sendResponse(
    starkinfra.issuingauthorization.response(
        status="denied",
        reason="other",
        tags=["other-id/456"],
    )
)
```

### Get your IssuingBalance

To know how much money you have in your workspace, run:

```python
import starkinfra

balance = starkinfra.issuingbalance.get()

print(balance)
```

### Query IssuingTransactions

To understand your balance changes (issuing statement), you can query
transactions. Note that our system creates transactions for you when
you make purchases, withdrawals, receive issuing invoice payments, for example.

```python
import starkinfra

transactions = starkinfra.issuingtransaction.query(
    after="2020-01-01",
    before="2020-03-01"
)
for transaction in transactions:
    print(transaction)
```

### Get an IssuingTransaction

You can get a specific transaction by its id:

```python
import starkinfra

transaction = starkinfra.issuingtransaction.get("5155165527080960")

print(transaction)
```

### Create IssuingHolders

You can create card holders to your Workspace.

```python
import starkinfra

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

**Note**: Instead of using IssuingHolder objects, you can also pass each element in dictionary format

### Query IssuingHolders

You can query multiple holders according to filters.

```python
import starkinfra

holders = starkinfra.issuingholder.query()

for holder in holders:
    print(holder)
```

### Delete an IssuingHolder

To cancel a single Issuing Holder by its id, run:

```python
import starkinfra

holder = starkinfra.issuingholder.delete("5155165527080960")

print(holder)
```

### Get an IssuingHolder

To get a single Issuing Holder by its id, run:

```python
import starkinfra

holder = starkinfra.issuingholder.get("5155165527080960")

print(holder)
```

### Query IssuingHolder logs

You can query holder logs to better understand holder life cycles.

```python
import starkinfra

logs = starkinfra.issuingholder.log.query(limit=50)

for log in logs:
    print(log.id)
```

### Get an IssuingHolder log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.issuingholder.log.get("5155165527080960")

print(log)
```

### Query IssuingBins

To take a look at the sub-issuer BINs linked to your workspace, just run the following:

```python
import starkinfra

bins = starkinfra.issuingbin.query()
for bin in bins:
    print(bin)
```

### Create IssuingInvoices

You can create dynamic QR Code invoices to receive money from accounts you have in other banks to your Issuing account.

Since the banking system only understands value modifiers (discounts, fines and interest) when dealing with **dates** (instead of **datetimes**), these values will only show up in the end user banking interface if you use **dates** in the "due" and "discounts" fields. 

If you use **datetimes** instead, our system will apply the value modifiers in the same manner, but the end user will only see the final value to be paid on his interface.

Also, other banks will most likely only allow payment scheduling on invoices defined with **dates** instead of **datetimes**.

```python
import starkinfra

invoice = starkinfra.issuinginvoice.create(
    amount=1000
)

print(invoice)
```

**Note**: Instead of using Invoice objects, you can also pass each element in dictionary format

### Get an IssuingInvoice

After its creation, information on an invoice may be retrieved by its id. 
Its status indicates whether it's been paid.

```python
import starkinfra

invoice = starkinfra.issuinginvoice.get("5155165527080960")

print(invoice)
```

### Query IssuingInvoices

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

### Query IssuingInvoice logs

Logs are pretty important to understand the life cycle of an invoice.

```python
import starkinfra

logs = starkinfra.issuinginvoice.log.query(limit=150)

for log in logs:
    print(log)
```

### Create IssuingWithdrawals

You can create withdrawals to send back cash to your Banking account by using the Withdrawal resource

```python
import starkinfra

withdrawal = starkinfra.issuingwithdrawal.create(
    amount=10000,
    external_id="123",
    description="Sending back"
)

print(withdrawal)
```

**Note**: Instead of using Withdrawal objects, you can also pass each element in dictionary format

### Get an IssuingWithdrawal

After its creation, information on a withdrawal may be retrieved by its id.

```python
import starkinfra

invoice = starkinfra.issuingwithdrawal.get("5155165527080960")

print(invoice)
```

### Query IssuingWithdrawals

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

### Create IssuingCards

You can issue cards with specific spending rules to make purchases.

```python
import starkinfra

cards = starkinfra.issuingcard.create([
    starkinfra.IssuingCard(
        holder_name="Developers",
        holder_tax_id="012.345.678-90",
        holder_external_id="1234",
        rules=starkinfra.IssuingRule(
            name="general",
            interval="week",
            amount=50000,
            currency_code="USD"
        )
    )
])

for card in cards:
    print(card)
```

### Query IssuingCards

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

### Get an IssuingCard

After its creation, information on a card may be retrieved by its id.

```python
import starkinfra

card = starkinfra.issuingcard.get("5155165527080960")

print(card)
```

### Update an IssuingCard

You can update a specific Issuing Card by its id.

```python
import starkinfra

card = starkinfra.issuingcard.update("5155165527080960", status="blocked")

print(card)
```

### Delete an IssuingCard

You can also cancel a card by its id.
Note that this is not possible if it has been processed already.

```python
import starkinfra

card = starkinfra.issuingcard.delete("5155165527080960")

print(card)
```

### Query IssuingCard logs

Logs are pretty important to understand the life cycle of a card.

```python
import starkinfra

logs = starkinfra.issuingcard.log.query(limit=150)

for log in logs:
    print(log)
```

### Get an IssuingCard log

You can get a single log by its id.

```python
import starkinfra

log = starkinfra.issuingcard.log.get("5155165527080960")

print(log)
```


### Query IssuingPurchases

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

### Get an IssuingPurchase

After its creation, information on a purchase may be retrieved by its id. 

```python
import starkinfra

purchase = starkinfra.issuingpurchase.get("5155165527080960")

print(purchase)
```

### Query IssuingPurchase logs

Logs are pretty important to understand the life cycle of a purchase.

```python
import starkinfra

logs = starkinfra.issuingpurchase.log.query(limit=150)

for log in logs:
    print(log)
```

### Get an IssuingPurchase log

You can get a single log by its id.

```python
import starkinfra

log = starkinfra.issuingpurchase.log.get("5155165527080960")

print(log)
```

**Note**: the Organization user can only update a workspace with the Workspace ID set.

## Pix

### Create PixRequests
You can create a Pix request to charge a user:

```python
import starkinfra

requests = starkinfra.pixrequest.create([
    starkinfra.PixRequest(
        amount=100,  # (R$ 1.00)
        external_id="141234121",  # so we can block anything you send twice by mistake
        sender_branch_code="0000",
        sender_account_number="00000-0",
        sender_account_type="checking",
        sender_name="Tyrion Lannister",
        sender_tax_id="012.345.678-90",
        receiver_bank_code="00000001",
        receiver_branch_code="0001",
        receiver_account_number="00000-1",
        receiver_account_type="checking",
        receiver_name="Jamie Lannister",
        receiver_tax_id="45.987.245/0001-92",
        end_to_end_id="E20018183202201201450u34sDGd19lz",
        description="For saving my life",
    ),
    starkinfra.PixRequest(
        amount=200,  # (R$ 2.00)
        external_id="2135613462",  # so we can block anything you send twice by mistake
        sender_account_number="00000-0",
        sender_branch_code="0000",
        sender_account_type="checking",
        sender_name="Arya Stark",
        sender_tax_id="012.345.678-90",
        receiver_bank_code="00000001",
        receiver_account_number="00000-1",
        receiver_branch_code="0001",
        receiver_account_type="checking",
        receiver_name="John Snow",
        receiver_tax_id="012.345.678-90",
        end_to_end_id="E20018183202201201450u34sDGd19lz",
        tags=["Needle", "sword"],
    )
])

for request in requests:
    print(request)
```

**Note**: Instead of using PixRequest objects, you can also pass each element in dictionary format

### Query PixRequests

You can query multiple pix requests according to filters.

```python
import starkinfra
from datetime import datetime

requests = starkinfra.pixrequest.query(
    limit=10,
    after=datetime(2020, 1, 1),
    before=datetime(2020, 4, 1),
    status="success",
    tags=["iron", "suit"],
    end_to_end_ids=["E79457883202101262140HHX553UPqeq"],
)

for request in requests:
    print(request)
```

### Get a PixRequest

After its creation, information on a pix request may be retrieved by its id. Its status indicates whether it has been paid.

```python
import starkinfra

request = starkinfra.pixrequest.get("5155165527080960")

print(request)
```

### Process PixRequests authorization requests

It's easy to process authorization requests that arrived in your handler. Remember to pass the
signature header so the SDK can make sure it's StarkInfra that sent you
the event.

```python
import starkinfra

request = listen_requests()  # this is your handler to listen for authorization requests

pix_request = starkinfra.pixrequest.parse(
    content=request.data.decode("utf-8"),
    signature=request.headers["Digital-Signature"],
)

print(pix_request)
```
  
### Query PixRequest logs

You can query pix request logs to better understand pix request life cycles. 

```python
import starkinfra

logs = starkinfra.pixrequest.log.query(
    limit=50, 
    after="2022-01-01",
    before="2022-01-20",
)

for log in logs:
    print(log)
```

### Get a pix request log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.pixrequest.log.get("5155165527080960")

print(log)
```

### Create PixReversals

You can reverse a pix request by whole or by a fraction of its amount using a pix reversal.

```python
import starkinfra

reversal = starkinfra.pixreversal.create([
    starkinfra.PixReversal(
        amount=100,
        end_to_end_id="E00000000202201060100rzsJzG9PzMg",
        external_id="17238435823958934",
        reason="bankError",
    )
])

print(reversal)
```

### Query PixReversals 

You can query multiple pix reversals according to filters. 

```python
import starkinfra
from datetime import datetime

reversals = starkinfra.pixreversal.query(
    limit=10,
    after=datetime(2020, 1, 1),
    before=datetime(2020, 4, 1),
    status="success",
    tags=["iron", "suit"],
    return_ids=["D20018183202202030109X3OoBHG74wo"],
)

for reversal in reversals:
    print(reversal)
```

### Get a PixReversal

After its creation, information on a pix reversal may be retrieved by its id. Its status indicates whether it has been paid.

```python
import starkinfra

reversal = starkinfra.pixreversal.get("5155165527080960")

print(reversal)
```

### Process PixReversal authorization requests

It's easy to process authorization requests that arrived in your handler. Remember to pass the
signature header so the SDK can make sure it's StarkInfra that sent you
the event.

```python
import starkinfra

request = listen()  # this is your handler to listen for authorization requests

reversal = starkinfra.pixreversal.parse(
    content=request.data.decode("utf-8"),
    signature=request.headers["Digital-Signature"],
)

print(reversal)
```

### Query PixReversal logs

You can query pix reversal logs to better understand pix reversal life cycles. 

```python
import starkinfra

logs = starkinfra.pixreversal.log.query(
    limit=50, 
    after="2022-01-01",
    before="2022-01-20",
)

for log in logs:
    print(log)
```

### Get a PixReversal log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.pixreversal.log.get("5155165527080960")

print(log)
```

### Get PixBalance 

To know how much money you have in your workspace, run:

```python
import starkinfra

balance = starkinfra.pixbalance.get()

print(balance)
```

### Create PixStatement

Statements are only available for direct participants. To create a statement of all the transactions that happened on your workspace during a specific day, run:

```python
import starkinfra

statement = starkinfra.pixstatement.create(
    starkinfra.PixStatement(
        after="2022-01-01", # This is the date that you want to create a statement.
        before="2022-01-01", # After and before must be the same date.
        type="transaction" # Options are "interchange", "interchangeTotal", "transaction".
    )
)

print(statement)
```

### Query PixStatements

You can query multiple pix statements according to filters. 

```python
import starkinfra

statements = starkinfra.pixstatement.query(
    limit=50, 
)

for statement in statements:
    print(statement)
```

### Get a PixStatement

Statements are only available for direct participants. To get a pix statement by its id:

```python
import starkinfra

statement = starkinfra.pixstatement.get("5155165527080960")

print(statement)
```

### Get a PixStatement .csv file

To get a .csv file of a pix statement using its id, run:

```python
import starkinfra

csv = starkinfra.pixstatement.csv("5155165527080960")

with open("test.zip", "wb") as file:
    file.write(csv)
```

## Create a pix key
You can create a Pix Key to link bank account information to a key id:

```python
import starkinfra

key = starkinfra.pixkey.create(
    starkinfra.PixKey(
        account_created="2022-02-01T00:00:00.00",
        account_number="00000",
        account_type="savings",
        branch_code="0000",
        name="Jamie Lannister",
        tax_id="012.345.678-90",
        id =  "+5511989898989",
    )
)

print(key)
```

## Query pix keys

You can query multiple pix keys according to filters.

```python
import starkinfra
from datetime import datetime

keys = starkinfra.pixkey.query(
    limit=1,
    after="2022-01-01",
    before="2022-01-12",
    status="registered",
    tags=["iron", "bank"],
    ids=["+5511989898989"],
    type="phone"
)

for key in keys:
    print(key)
```

## Get a pix key

After its creation, information on a Pix key may be retrieved by its id and the tax id of the consulting agent.

```python
import starkinfra

key = starkinfra.pixkey.get("5155165527080960", payer_id="012.345.678-90", end_to_end_id=starkinfra.new_end_to_end_id("20018183"))

print(key)
```

## Patch a pix key

Update the account information or the holder's name linked to a Pix Key.

```python
import starkinfra

key = starkinfra.pixkey.update(
    id="+5511989898989",
    reason="branchTransfer",
    name="Jamie Lannister"
)

print(key)
```

## Delete a pix key

Cancel a specific Pix Key using its id.

```python
import starkinfra

key = starkinfra.pixkey.delete("5155165527080960")

print(key)
```

## Query pix key logs

You can query pix key logs to better understand pix key life cycles. 

```python
import starkinfra

logs = starkinfra.pixkey.log.query(
    limit=50, 
    ids=["5729405850615808"],
    after="2022-01-01",
    before="2022-01-20",
    types=["created"],
    key_ids=["+5511989898989"]
)

for log in logs:
    print(log)
```

## Get a pix key log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.pixkey.log.get("5155165527080960")

print(log)
```

## Create a pix claim
You can create a Pix claim to request a transfer of a Pix key to another account:

```python
import starkinfra

claim = starkinfra.pixclaim.create(
    starkinfra.PixClaim(
        account_created="2022-02-01T00:00:00.00",
        account_number="5692908409716736",
        account_type="checking",
        branch_code="0000",
        name="testKey",
        tax_id="012.345.678-90",
        type="ownership",
        key_id="+5511989898989"
    )
)

print(claim)
```

## Query pix claims

You can query multiple pix claims according to filters.

```python
import starkinfra

claims = starkinfra.pixclaim.query(
    limit=1,
    after="2022-01-01",
    before="2022-01-12",
    status="registered",
    ids=["5729405850615808"],
    type="ownership",
    agent="claimed",
    key_type="phone",
    key_id="+5511989898989"
)

for claim in claims:
    print(claim)
```

## Get a pix claim

After its creation, information on a pix claim may be retrieved by its id. Its status indicates whether it has been paid.

```python
import starkinfra

claim = starkinfra.pixclaim.get("5155165527080960")

print(claim)
```

## Patch a pix claim

A Pix Claim can be patched for two distinct reasons. A received Pix Claim can be confirmed or canceled by patching 
its status. A received Pix Claim must be confirmed by the donor to be completed. Ownership Pix Claims can only be 
canceled by the donor if the reason is fraud. A sent Pix Claim can also be canceled by patching its status.

```python
import starkinfra

claim = starkinfra.pixclaim.update(
    id="+5511989898989",
    status="confirmed"
)

print(claim)
```

## Query pix claim logs

You can query pix claim logs to better understand pix claim life cycles. 

```python
import starkinfra

logs = starkinfra.pixclaim.log.query(
    limit=50, 
    ids=["5729405850615808"],
    after="2022-01-01",
    before="2022-01-20",
    types=["registered"],
    claim_ids=["5719405850615809"]
)

for log in logs:
    print(log)
```

## Get a pix claim log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.pixclaim.log.get("5155165527080960")

print(log)
```

## Create an infraction report
Infraction reports are used to report transactions that are suspected of fraud, to request a refund or to 
reverse a refund. Infraction reports can be created by either participant of a transaction.
```python
import starkinfra

report = starkinfra.infractionreport.create(
    starkinfra.InfractionReport(
        reference_id="E20018183202201201450u34sDGd19lz",
        type="fraud",
    )
)

print(report)
```

## Query infraction reports

You can query multiple infraction reports according to filters.

```python
import starkinfra

reports = starkinfra.infractionreport.query(
    limit=1,
    after="2022-01-01",
    before="2022-01-12",
    status="registered",
    ids=["5155165527080960"],
    type="phone"
)

for report in reports:
    print(report)
```

## Get an infraction report

After its creation, information on an Infraction Report may be retrieved by its.

```python
import starkinfra

report = starkinfra.infractionreport.get("5155165527080960")

print(report)
```

## Patch an infraction report

A received Infraction Report can be confirmed or declined by patching its status. After an Infraction Report 
is Patched, its status changes to closed.

```python
import starkinfra

report = starkinfra.infractionreport.update(
    id="5155165527080960",
    result="agreed",
)

print(report)
```

## Delete an infraction report

Cancel a specific Infraction Report using its id.

```python
import starkinfra

report = starkinfra.infractionreport.delete("5155165527080960")

print(report)
```

## Query infraction report logs

You can query infraction report logs to better understand infraction report life cycles. 

```python
import starkinfra

logs = starkinfra.infractionreport.log.query(
    limit=50, 
    ids=["5729405850615808"],
    after="2022-01-01",
    before="2022-01-20",
    types=["created"],
    report_ids=["5155165527080960"]
)

for log in logs:
    print(log)
```

## Get an infraction report log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.infractionreport.log.get("5155165527080960")

print(log)
```

## Create an reversal request
A reversal request can be created when fraud is detected on a transaction or a system malfunction 
results in an erroneous transaction. The reversal request can be made by the user or by the payer's 
participant directly.
```python
import starkinfra

request = starkinfra.reversalrequest.create(
    starkinfra.ReversalRequest(
        amount=100,
        reference_id="E20018183202201201450u34sDGd19lz",
        reason="fraud",
    )
)

print(request)
```

## Query reversal requests

You can query multiple reversal requests according to filters.

```python
import starkinfra

requests = starkinfra.reversalrequest.query(
    limit=1,
    after="2022-01-01",
    before="2022-01-12",
    status="registered",
    ids=["5155165527080960"]
)

for request in requests:
    print(request)
```

## Get an reversal request

After its creation, information on a Reversal Request may be retrieved by its.

```python
import starkinfra

request = starkinfra.reversalrequest.get("5155165527080960")

print(request)
```

## Patch an reversal request

A received Reversal Request can be accepted or rejected by patching its status. After a Reversal Request 
is Patched, its status changes to closed.

```python
import starkinfra

request = starkinfra.reversalrequest.update(
    id="5155165527080960",
    result="accepted",
    reversal_reference_id="D20018183202201201450u34sDGd19lz"
)

print(request)
```

## Delete an reversal request

Cancel a specific Reversal Request using its id.

```python
import starkinfra

request = starkinfra.reversalrequest.delete("5155165527080960")

print(request)
```

## Query reversal request logs

You can query reversal request logs to better understand reversal request life cycles. 

```python
import starkinfra

logs = starkinfra.reversalrequest.log.query(
    limit=50, 
    ids=["5729405850615808"],
    after="2022-01-01",
    before="2022-01-20",
    types=["created"],
    request_ids=["5155165527080960"]
)

for log in logs:
    print(log)
```

## Get an reversal request log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.reversalrequest.log.get("5155165527080960")

print(log)
```

## Process webhook events

It's easy to process events delivered to your Webhook endpoint. Remember to pass the
signature header so the SDK can make sure it was StarkInfra that sent you
the event.

```python
import starkinfra

request = listen()  # this is the method you made to get the events posted to your webhook endpoint

event = starkinfra.event.parse(
    content=request.data.decode("utf-8"),
    signature=request.headers["Digital-Signature"],
)

if "pix-request" in event.subscription:
    print(event.log.request)

elif "pix-reversal" in event.subscription:
    print(event.log.reversal)
```

## Credit Note

### Create CreditNotes
You can create a Credit Note to generate a CCB contract:

```python
import starkinfra

notes = starkinfra.creditnote.create([
    starkinfra.CreditNote(
        template_id="0123456789101112",
        name="Jamie Lannister",
        tax_id="012.345.678-90",
        nominal_amount=100000,
        scheduled="2022-04-28",
        invoices=[
            {
                "due": "2023-06-25",
                "amount": 120000,
                "fine": 10,
                "interest": 2
            }
        ],
        transfer={
            "bank_code": "00000000",
            "branch_code": "1234",
            "account_number": "129340-1",
            "name": "Jamie Lannister",
            "taxId": "012.345.678-90"
        },
        signers=[
            {
                "name": "Jamie Lannister",
                "contact": "jamie.lannister@gmail.com",
                "method": "link"
            }
        ],
    ),
    starkinfra.CreditNote(
        template_id="5656565656565656",
        name="Jamie Lannister",
        tax_id="012.345.678-90",
        nominal_amount=240000,
        scheduled="2022-04-28",
        invoices=[
            {
                "due": "2023-06-25",
                "amount": 100000,
                "fine": 10,
                "interest": 2
            },
            {
                "due": "2023-07-25",
                "amount": 100000,
                "fine": 11,
                "interest": 2.1
            },
            {
                "due": "2023-08-25",
                "amount": 100000,
                "fine": 12.5,
                "interest": 2.2
            }
        ],
        tags=["test", "testing"],
        transfer={
            "bank_code": "00000000",
            "branch_code": "1234",
            "account_number": "129340-1",
            "name": "Jamie Lannister",
            "taxId": "012.345.678-90"
        },
        signers=[
            {
                "name": "Jamie Lannister",
                "contact": "jamie.lannister@gmail.com",
                "method": "link"
            }
        ],
    )
])

for note in notes:
    print(note)
```

**Note**: Instead of using CreditNote objects, you can also pass each element in dictionary format

### Query CreditNotes

You can query multiple credit notes according to filters.

```python
import starkinfra
from datetime import datetime

notes = starkinfra.creditnote.query(
    limit=10,
    after=datetime(2020, 1, 1),
    before=datetime(2020, 4, 1),
    status="success",
    tags=["iron", "suit"],
)

for note in notes:
    print(note)
```

### Get a CreditNote

After its creation, information on a credit note may be retrieved by its id.

```python
import starkinfra

note = starkinfra.creditnote.get("5155165527080960")

print(note)
```

### Cancel a CreditNote

You can cancel a credit note if it has not been signed yet.

```python
import starkinfra

note = starkinfra.creditnote.delete("5155165527080960")

print(note)
```
  
### Query CreditNote logs

You can query credit note logs to better understand credit note life cycles. 

```python
import starkinfra

logs = starkinfra.creditnote.log.query(
    limit=50, 
    after="2022-01-01",
    before="2022-01-20",
)

for log in logs:
    print(log)
```

### Get a CreditNote log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.creditnote.log.get("5155165527080960")

print(log)
```

### Process webhook events

It's easy to process events delivered to your Webhook endpoint. Remember to pass the
signature header so the SDK can make sure it was StarkInfra that sent you
the event.

```python
import starkinfra

request = listen()  # this is the method you made to get the events posted to your webhook endpoint

event = starkinfra.event.parse(
    content=request.data.decode("utf-8"),
    signature=request.headers["Digital-Signature"],
)

if "pix-request" in event.subscription:
    print(event.log.request)

elif "pix-reversal" in event.subscription:
    print(event.log.reversal)
    
elif "pix-key" in event.subscription:
    print(event.log.key)
    
elif "pix-claim" in event.subscription:
    print(event.log.claim)

elif "issuing-card" in event.subscription:
    print(event.log.card)

elif "issuing-invoice" in event.subscription:
    print(event.log.invoice)

elif "issuing-purchase" in event.subscription:
    print(event.log.purchase)

elif "credit-note" in event.subscription:
    print(event.log.note)
```

# Handling errors

The SDK may raise one of four types of errors: __InputErrors__, __InternalServerError__, __UnknownError__, __InvalidSignatureError__

__InputErrors__ will be raised whenever the API detects an error in your request (status code 400).
If you catch such an error, you can get its elements to verify each of the
individual errors that were detected in your request by the API.
For example:

```python
import starkinfra

try:
    reversal = starkinfra.pixreversal.create([
        starkinfra.PixReversal(
            amount=100,
            end_to_end_id="E00000000202201060100rzsJzG9PzMg",
            external_id="17238435823958934",
            reason="bankError",
        )
    ])
except starkinfra.error.InputErrors as exception:
    for error in exception.errors:
        print(error.code)
        print(error.message)
```

__InternalServerError__ will be raised if the API runs into an internal error.
If you ever stumble upon this one, rest assured that the development team
is already rushing in to fix the mistake and get you back up to speed.

__UnknownError__ will be raised if a request encounters an error that is
neither __InputErrors__ nor an __InternalServerError__, such as connectivity problems.

__InvalidSignatureError__ will be raised specifically by starkinfra.event.parse()
when the provided content and signature do not check out with the Stark Infra public
key.

# Help and Feedback

If you have any questions about our SDK, just send us an email.
We will respond you quickly, pinky promise. We are here to help you integrate with us ASAP.
We also love feedback, so don't be shy about sharing your thoughts with us.

Email: help@starkbank.com