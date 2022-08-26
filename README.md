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
        - [Products](#query-issuingproducts): View available sub-issuer card products (a.k.a. card number ranges or BINs)
        - [Holders](#create-issuingholders): Manage card holders
        - [Cards](#create-issuingcards): Create virtual and/or physical cards
        - [Purchases](#process-purchase-authorizations): Authorize and view your past purchases
        - [Invoices](#create-issuinginvoices): Add money to your issuing balance
        - [Withdrawals](#create-issuingwithdrawals): Send money back to your Workspace from your issuing balance
        - [Balance](#get-your-issuingbalance): View your issuing balance
        - [Transactions](#query-issuingtransactions): View the transactions that have affected your issuing balance
        - [Enums](#issuing-enums): Query enums related to the issuing purchases, such as merchant categories, countries and card purchase methods
    - [Pix](#pix)
        - [PixRequests](#create-pixrequests): Create Pix transactions
        - [PixReversals](#create-pixreversals): Reverse Pix transactions
        - [PixBalance](#get-your-pixbalance): View your account balance
        - [PixStatement](#create-a-pixstatement): Request your account statement
        - [PixKey](#create-a-pixkey): Create a Pix Key
        - [PixClaim](#create-a-pixclaim): Claim a Pix Key
        - [PixDirector](#create-a-pixdirector): Create a Pix Director
        - [PixInfraction](#create-pixinfractions): Create Pix Infraction reports
        - [PixChargeback](#create-pixchargebacks): Create Pix Chargeback requests
        - [PixDomain](#query-pixdomains): View registered SPI participants certificates
        - [StaticBrcode](#create-staticbrcodes): Create static Pix BR codes
        - [DynamicBrcode](#create-dynamicbrcodes): Create dynamic Pix BR codes
        - [BrcodePreview](#create-brcodepreviews): Read data from BR Codes before paying them
    - [Credit Note](#credit-note)
        - [CreditNote](#create-creditnotes): Create credit notes
    - [Credit Preview](#credit-preview)
        - [CreditNotePreview](#create-a-creditnotepreview): Create a credit note preview
    - [Webhook](#webhook):
        - [Webhook](#create-a-webhook-subscription): Configure your webhook endpoints and subscriptions
        - [WebhookEvents](#process-webhook-events): Manage Webhook events
        - [WebhookEventAttempts](#query-failed-webhook-event-delivery-attempts-information): Query failed webhook event deliveries
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
in your account, which can be added to your balance by creating a starkbank.Invoice. 

In the Sandbox environment, most of the created starkbank.Invoices will be automatically paid,
so there's nothing else you need to do to add funds to your account. Just create
a few starkbank.Invoice and wait around a bit.

In Production, you (or one of your clients) will need to actually pay this Pix Request
for the value to be credited to your account.


# Usage

Here are a few examples on how to use the SDK. If you have any doubts, use the built-in
`help()` function to get more info on the desired functionality
(for example: `help(starkinfra.issuinginvoice.create)`)

## Issuing

### Query IssuingProducts

To take a look at the sub-issuer card products available to you, just run the following:

```python
import starkinfra

products = starkinfra.issuingproduct.query()

for product in products:
    print(product)
```

This will tell which card products and card number prefixes you have at your disposal.

### Create IssuingHolders

You can create card holders to which your cards will be bound.
They support spending rules that will apply to all underlying cards.

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
                "currencyCode": "USD",
                "categories": [
                    {
                        "type": "services"
                    },
                    {
                        "code": "fastFoodRestaurants"
                    }
                ],
                "countries": [
                    {
                        "code": "USA"
                    }
                ],
                "methods": [
                    {
                        "code": "token"
                    }
                ]
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

### Cancel an IssuingHolder

To cancel a single Issuing Holder by its id, run:

```python
import starkinfra

holder = starkinfra.issuingholder.cancel("5155165527080960")

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

### Create IssuingCards

You can issue cards with specific spending rules.

```python
import starkinfra

cards = starkinfra.issuingcard.create([
    starkinfra.IssuingCard(
        holder_name="Developers",
        holder_tax_id="012.345.678-90",
        holder_external_id="1234",
        rules=[starkinfra.IssuingRule(
            name="general",
            interval="week",
            amount=50000,
            currency_code="USD",
            categories=[
                starkinfra.MerchantCategory(type="services"),  # Covers all service-related MCCs
                starkinfra.MerchantCategory(code="fastFoodRestaurants")  # Covers a specific MCC
            ],
            countries=[
                starkinfra.MerchantCountry(code="BRA")
            ],
            methods=[
                starkinfra.CardMethod(code="token")
            ]
        )]
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

You can update a specific card by its id.

```python
import starkinfra

card = starkinfra.issuingcard.update("5155165527080960", status="blocked")

print(card)
```

### Cancel an IssuingCard

You can also cancel a card by its id.

```python
import starkinfra

card = starkinfra.issuingcard.cancel("5155165527080960")

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

### Process Purchase authorizations

It's easy to process purchase authorizations delivered to your endpoint.
Remember to pass the signature header so the SDK can make sure it's StarkInfra that sent you the event.
If you do not approve or decline the authorization within 2 seconds, the authorization will be denied.

```python
import starkinfra

request = listen()  # this is the method you made to get the events posted to your webhook endpoint

authorization = starkinfra.issuingpurchase.parse(
    content=request.data.decode("utf-8"),
    signature=request.headers["Digital-Signature"],
)

sendResponse(  # you should also implement this method
    starkinfra.issuingpurchase.response(  # this optional method just helps you build the response JSON
        status="approved",
        amount=authorization.amount,
        tags=["my-purchase-id/123"],
    )
)

# or 

sendResponse(
    starkinfra.issuingpurchase.response(
        status="denied",
        reason="other",
        tags=["other-id/456"],
    )
)
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

### Create IssuingInvoices

You can create Pix invoices to transfer money from accounts you have in any bank to your Issuing balance,
allowing you to run your issuing operation.

```python
import starkinfra

invoice = starkinfra.issuinginvoice.create(
    invoice=starkinfra.IssuingInvoice(
        amount=1000
    )
)

print(invoice)
```

**Note**: Instead of using IssuingInvoice objects, you can also pass each element in dictionary format

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

### Get an IssuingInvoice log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.issuinginvoice.log.get("5155165527080960")

print(log)
```

### Create IssuingWithdrawals

You can create withdrawals to send cash back from your Issuing balance to your Banking balance
by using the Withdrawal resource.

```python
import starkinfra

withdrawal = starkinfra.issuingwithdrawal.create(
    withdrawal=starkinfra.IssuingWithdrawal(
        amount=10000,
        external_id="123",
        description="Sending back"
    )
)

print(withdrawal)
```

**Note**: Instead of using IssuingWithdrawal objects, you can also pass each element in dictionary format

### Get an IssuingWithdrawal

After its creation, information on a withdrawal may be retrieved by its id.

```python
import starkinfra

invoice = starkinfra.issuingwithdrawal.get("5155165527080960")

print(invoice)
```

### Query IssuingWithdrawals

You can get a list of created withdrawals given some filters.

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

### Get your IssuingBalance

To know how much money you have available to run authorizations, run:

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

### Issuing Enums

#### Query MerchantCategories

You can query any merchant categories using this resource.
You may also use MerchantCategories to define specific category filters in IssuingRules.
Either codes (which represents specific MCCs) or types (code groups) will be accepted as filters.

```python
import starkinfra

categories = starkinfra.merchantcategory.query(
    search="food",
)

for category in categories:
    print(category)
```

#### Query MerchantCountries

You can query any merchant countries using this resource.
You may also use MerchantCountries to define specific country filters in IssuingRules.

```python
import starkinfra

countries = starkinfra.merchantcountry.query(
    search="brazil",
)

for country in countries:
    print(country)
```

#### Query CardMethods

You can query available card methods using this resource.
You may also use CardMethods to define specific purchase method filters in IssuingRules.

```python
import starkinfra

methods = starkinfra.cardmethod.query(
    search="token",
)

for method in methods:
    print(method)
```

## Pix

### Create PixRequests

You can create a Pix request to transfer money from one of your users to anyone else:

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
        end_to_end_id=starkinfra.endtoendid.create("20018183"),  # Pass your bank code to create an end to end ID
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
        end_to_end_id=starkinfra.endtoendid.create("20018183"),  # Pass your bank code to create an end to end ID
        tags=["Needle", "sword"],
    )
])

for request in requests:
    print(request)
```

**Note**: Instead of using PixRequest objects, you can also pass each element in dictionary format

### Query PixRequests

You can query multiple Pix requests according to filters.

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

After its creation, information on a Pix request may be retrieved by its id. Its status indicates whether it has been paid.

```python
import starkinfra

request = starkinfra.pixrequest.get("5155165527080960")

print(request)
```

### Process inbound PixRequest authorizations

It's easy to process authorization requests that arrived at your endpoint.
Remember to pass the signature header so the SDK can make sure it's StarkInfra that sent you the event.
If you do not approve or decline the authorization within 1 second, the authorization will be denied.

```python
import starkinfra

request = listen()  # this is your handler to listen for authorization requests

pix_request = starkinfra.pixrequest.parse(
    content=request.data.decode("utf-8"),
    signature=request.headers["Digital-Signature"],
)

print(pix_request)

sendResponse(  # you should also implement this method
    starkinfra.pixrequest.response(  # this optional method just helps you build the response JSON
        status="approved",
    )
)

# or 

sendResponse(
    starkinfra.pixrequest.response(
        status="denied",
        reason="orderRejected",
    )
)
```
  
### Query PixRequest logs

You can query Pix request logs to better understand Pix request life cycles. 

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

### Get a PixRequest log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.pixrequest.log.get("5155165527080960")

print(log)
```

### Create PixReversals

You can reverse a PixRequest either partially or totally using a PixReversal.

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

You can query multiple Pix reversals according to filters. 

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

After its creation, information on a Pix reversal may be retrieved by its id.
Its status indicates whether it has been successfully processed.

```python
import starkinfra

reversal = starkinfra.pixreversal.get("5155165527080960")

print(reversal)
```

### Process inbound PixReversal authorizations

It's easy to process authorization requests that arrived at your endpoint.
Remember to pass the signature header so the SDK can make sure it's StarkInfra that sent you the event.
If you do not approve or decline the authorization within 1 second, the authorization will be denied.

```python
import starkinfra

request = listen()  # this is your handler to listen for authorization requests

reversal = starkinfra.pixreversal.parse(
    content=request.data.decode("utf-8"),
    signature=request.headers["Digital-Signature"],
)

print(reversal)

sendResponse(  # you should also implement this method
    starkinfra.pixreversal.response(  # this optional method just helps you build the response JSON
        status="approved",
    )
)

# or 

sendResponse(
    starkinfra.pixreversal.response(
        status="denied",
        reason="orderRejected",
    )
)
```

### Query PixReversal logs

You can query Pix reversal logs to better understand their life cycles. 

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

### Get your PixBalance 

To see how much money you have in your account, run:

```python
import starkinfra

balance = starkinfra.pixbalance.get()

print(balance)
```

### Create a PixStatement

Statements are generated directly by the Central Bank and are only available for direct participants.
To create a statement of all the transactions that happened on your account during a specific day, run:

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

You can query multiple Pix statements according to filters. 

```python
import starkinfra

statements = starkinfra.pixstatement.query(
    limit=50, 
)

for statement in statements:
    print(statement)
```

### Get a PixStatement

Statements are only available for direct participants. To get a Pix statement by its id:

```python
import starkinfra

statement = starkinfra.pixstatement.get("5155165527080960")

print(statement)
```

### Get a PixStatement .csv file

To get the .csv file corresponding to a Pix statement using its id, run:

```python
import starkinfra

csv = starkinfra.pixstatement.csv("5155165527080960")

with open("test.zip", "wb") as file:
    file.write(csv)
```

### Create a PixKey

You can create a Pix Key to link a bank account information to a key id:

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
        id="+5511989898989",
    )
)

print(key)
```

### Query PixKeys

You can query multiple Pix keys you own according to filters.

```python
import starkinfra

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

### Get a PixKey

Information on a Pix key may be retrieved by its id and the tax ID of the consulting agent.
An endToEndId must be informed so you can link any resulting purchases to this query,
avoiding sweep blocks by the Central Bank.

```python
import starkinfra

key = starkinfra.pixkey.get(
    "5155165527080960",
    payer_id="012.345.678-90",
    end_to_end_id=starkinfra.endtoendid.create("20018183"),
)

print(key)
```

### Update a PixKey

Update the account information linked to a Pix Key.

```python
import starkinfra

key = starkinfra.pixkey.update(
    id="+5511989898989",
    reason="branchTransfer",
    name="Jamie Lannister"
)

print(key)
```

### Cancel a PixKey

Cancel a specific Pix Key using its id.

```python
import starkinfra

key = starkinfra.pixkey.cancel("5155165527080960")

print(key)
```

### Query PixKey logs

You can query Pix key logs to better understand a Pix key life cycle. 

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

### Get a PixKey log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.pixkey.log.get("5155165527080960")

print(log)
```

### Create a PixClaim

You can create a Pix claim to request the transfer of a Pix key from another bank to one of your accounts:

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
        key_id="+5511989898989"
    )
)

print(claim)
```

### Query PixClaims

You can query multiple Pix claims according to filters.

```python
import starkinfra

claims = starkinfra.pixclaim.query(
    limit=1,
    after="2022-01-01",
    before="2022-01-12",
    status="registered",
    ids=["5729405850615808"],
    type="ownership",
    flow="out",
    key_type="phone",
    key_id="+5511989898989"
)

for claim in claims:
    print(claim)
```

### Get a PixClaim

After its creation, information on a Pix claim may be retrieved by its id.

```python
import starkinfra

claim = starkinfra.pixclaim.get("5155165527080960")

print(claim)
```

### Update a PixClaim

A Pix Claim can be confirmed or canceled by patching its status.
A received Pix Claim must be confirmed by the donor to be completed.
Ownership Pix Claims can only be canceled by the donor if the reason is "fraud".
A sent Pix Claim can also be canceled.

```python
import starkinfra

claim = starkinfra.pixclaim.update(
    id="5155165527080960",
    status="confirmed"
)

print(claim)
```

### Query PixClaim logs

You can query Pix claim logs to better understand Pix claim life cycles.

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

### Get a PixClaim log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.pixclaim.log.get("5155165527080960")

print(log)
```

### Create a PixDirector

To register the Pix director contact information at the Central Bank, run the following:

```python
import starkinfra

director = starkinfra.pixdirector.create(
    starkinfra.PixDirector(
        name="Edward Stark",
        tax_id="03.300.300/0001-00",
        phone="+5511999999999",
        email="ned.stark@company.com",
        password="12345678",
        team_email="pix.team@company.com",
        team_phones=["+5511988889999", "+5511988889998"],
    )
)

print(director)
```

### Create PixInfractions

Pix Infraction reports are used to report transactions that raise fraud suspicion, to request a refund or to 
reverse a refund. Infraction reports can be created by either participant of a transaction.

```python
import starkinfra

infractions = starkinfra.pixinfraction.create(
    infractions=[
        starkinfra.PixInfraction(
            reference_id="E20018183202201201450u34sDGd19lz",
            type="fraud",
        )
    ]
)

for infraction in infractions:
    print(infraction)
```

### Query PixInfractions

You can query multiple infraction reports according to filters.

```python
import starkinfra

infractions = starkinfra.pixinfraction.query(
    limit=1,
    after="2022-01-01",
    before="2022-01-12",
    status="delivered",
    ids=["5155165527080960"],
)

for infraction in infractions:
    print(infraction)
```

### Get a PixInfraction

After its creation, information on a Pix Infraction may be retrieved by its id.

```python
import starkinfra

infraction = starkinfra.pixinfraction.get("5155165527080960")

print(infraction)
```

### Update a PixInfraction

A received Pix Infraction can be confirmed or declined by patching its status.
After a Pix Infraction is patched, its status changes to closed.

```python
import starkinfra

infraction = starkinfra.pixinfraction.update(
    id="5155165527080960",
    result="agreed",
)

print(infraction)
```

### Cancel a PixInfraction

Cancel a specific Pix Infraction using its id.

```python
import starkinfra

infraction = starkinfra.pixinfraction.cancel("5155165527080960")

print(infraction)
```

### Query PixInfraction logs

You can query infraction report logs to better understand their life cycles. 

```python
import starkinfra

logs = starkinfra.pixinfraction.log.query(
    limit=50, 
    ids=["5729405850615808"],
    after="2022-01-01",
    before="2022-01-20",
    types=["created"],
    infraction_ids=["5155165527080960"]
)

for log in logs:
    print(log)
```

### Get a PixInfraction log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.pixinfraction.log.get("5155165527080960")

print(log)
```

### Create PixChargebacks

A Pix chargeback can be created when fraud is detected on a transaction or a system malfunction 
results in an erroneous transaction.

```python
import starkinfra

chargebacks = starkinfra.pixchargeback.create(
    chargebacks=[
        starkinfra.PixChargeback(
            amount=100,
            reference_id="E20018183202201201450u34sDGd19lz",
            reason="fraud",
        )
    ]
)

for chargeback in chargebacks:
    print(chargeback)
```

### Query PixChargebacks

You can query multiple Pix chargebacks according to filters.

```python
import starkinfra

chargebacks = starkinfra.pixchargeback.query(
    limit=1,
    after="2022-01-01",
    before="2022-01-12",
    status="registered",
    ids=["5155165527080960"]
)

for chargeback in chargebacks:
    print(chargeback)
```

### Get a PixChargeback

After its creation, information on a Pix Chargeback may be retrieved by its.

```python
import starkinfra

chargeback = starkinfra.pixchargeback.get("5155165527080960")

print(chargeback)
```

### Update a PixChargeback

A received Pix Chargeback can be accepted or rejected by patching its status.
After a Pix Chargeback is patched, its status changes to closed.

```python
import starkinfra

chargeback = starkinfra.pixchargeback.update(
    id="5155165527080960",
    result="accepted",
    reversal_reference_id=starkinfra.returnid.create("20018183"),
)

print(chargeback)
```

### Cancel a PixChargeback

Cancel a specific Pix Chargeback using its id.

```python
import starkinfra

chargeback = starkinfra.pixchargeback.cancel("5155165527080960")

print(chargeback)
```

### Query PixChargeback logs

You can query Pix chargeback logs to better understand Pix chargeback life cycles. 

```python
import starkinfra

logs = starkinfra.pixchargeback.log.query(
    limit=50, 
    ids=["5729405850615808"],
    after="2022-01-01",
    before="2022-01-20",
    types=["created"],
    chargeback_ids=["5155165527080960"]
)

for log in logs:
    print(log)
```

### Get a PixChargeback log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.pixchargeback.log.get("5155165527080960")

print(log)
```

### Query PixDomains

Here you can list all Pix Domains registered at the Brazilian Central Bank. The Pix Domain object displays the domain 
name and the QR Code domain certificates of registered Pix participants able to issue dynamic QR Codes.

```python
import starkinfra

domains = starkinfra.pixdomain.query()
for domain in domains:
    print(domain)
```

### Create StaticBrcodes

StaticBrcodes store account information via a BR code or an image (QR code)
that represents a PixKey and a few extra fixed parameters, such as an amount 
and a reconciliation ID. They can easily be used to receive Pix transactions.

```python
import starkinfra

brcodes = starkinfra.staticbrcode.create([
    starkinfra.StaticBrcode(
        name="Jamie Lannister",
        key_id="+5511988887777",
        amount=100,
        reconciliation_id="123",
        city="Rio de Janeiro"
    )
])

for brcode in brcodes:
    print(brcode)
```

### Query StaticBrcodes

You can query multiple StaticBrcodes according to filters.

```python
import starkinfra

brcodes = starkinfra.staticbrcode.query(
    limit=1,
    after="2022-06-01",
    before="2022-06-30",
    uuids=["5ddde28043a245c2848b08cf315effa2"]
)

for brcode in brcodes:
    print(brcode)
```

### Get a StaticBrcodes

After its creation, information on a StaticBrcode may be retrieved by its UUID.

```python
import starkinfra

brcode = starkinfra.staticbrcode.get("5ddde28043a245c2848b08cf315effa2")

print(brcode)
```

### Create DynamicBrcodes

BR codes store information represented by Pix QR Codes, which are used to send 
or receive Pix transactions in a convenient way.
DynamicBrcodes represent charges with information that can change at any time,
since all data needed for the payment is requested dynamically to an URL stored
in the BR Code. Stark Infra will receive the GET request and forward it to your
registered endpoint with a GET request containing the UUID of the BR code for
identification.

```python
import starkinfra

brcodes = starkinfra.dynamicbrcode.create([
    starkinfra.DynamicBrcode(
        name="Jamie Lannister",
        city="Rio de Janeiro",
        external_id="my_unique_id_01",
        type="instant"
    )
])

for brcode in brcodes:
    print(brcode)
```

### Query DynamicBrcodes

You can query multiple DynamicBrcodes according to filters.

```python
import starkinfra

brcodes = starkinfra.dynamicbrcode.query(
    limit=1,
    after="2022-06-01",
    before="2022-06-30",
    uuids=["ac7caa14e601461dbd6b12bf7e4cc48e"]
)

for brcode in brcodes:
    print(brcode)
```

### Get a DynamicBrcode

After its creation, information on a DynamicBrcode may be retrieved by its UUID.

```python
import starkinfra

brcode = starkinfra.dynamicbrcode.get("ac7caa14e601461dbd6b12bf7e4cc48e")

print(brcode)
```

### Verify a DynamicBrcode read

When a DynamicBrcode is read by your user, a GET request will be made to the your regitered URL to 
retrieve additional information needed to complete the transaction.
Use this method to verify the authenticity of a GET request received at your registered endpoint.
If the provided digital signature does not check out with the StarkInfra public key, a stark.exception.InvalidSignatureException will be raised.

```python
import starkinfra

request = listen()  # this is the method you made to get the read requests posted to your registered endpoint

uuid = starkinfra.dynamicbrcode.verify(
    uuid=request.url.get_parameter("uuid"),
    signature=request.headers["Digital-Signature"],
)
```

### Answer to a Due DynamicBrcode read

When a Due DynamicBrcode is read by your user, a GET request containing 
the BR code UUID will be made to your registered URL to retrieve additional 
information needed to complete the transaction.

The GET request must be answered in the following format within 5 seconds 
and with an HTTP status code 200.

```python
import starkinfra

request = listen()  # this is the method you made to get the read requests posted to your registered endpoint

uuid = starkinfra.dynamicbrcode.verify(
    uuid=request.url.get_parameter("uuid"),
    signature=request.headers["Digital-Signature"],
)

invoice = get_my_invoice(uuid) # you should implement this method to get the information of the BR code from its uuid

send_response(  # you should also implement this method to respond the read request
    starkinfra.dynamicbrcode.response_due(
        version=invoice.version,
        created=invoice.created,
        due=invoice.due,
        key_id=invoice.key_id,
        status=invoice.status,
        reconciliation_id=invoice.reconciliation_id,
        amount=invoice.amount,
        sender_name=invoice.sender_name,
        receiver_name=invoice.receiver_name,
        receiver_street_line=invoice.receiver_street_line,
        receiver_city=invoice.receiver_city,
        receiver_state_code=invoice.receiver_state_code,
        receiver_zip_code=invoice.receiver_zip_code
    )
)
```

### Answer to an Instant DynamicBrcode read

When an Instant DynamicBrcode is read by your user, a GET request 
containing the BR code UUID will be made to your registered URL to retrieve 
additional information needed to complete the transaction.

The get request must be answered in the following format 
within 5 seconds and with an HTTP status code 200.

```python
import starkinfra

request = listen()  # this is the method you made to get the read requests posted to your registered endpoint

uuid = starkinfra.dynamicbrcode.verify(
    uuid=request.url.get_parameter("uuid"),
    signature=request.headers["Digital-Signature"],
)

invoice = get_my_invoice(uuid) # you should implement this method to get the information of the BR code from its uuid

send_response(  # you should also implement this method to respond the read request
    starkinfra.issuingpurchase.response_instant(
        version=invoice.version,
        created=invoice.created,
        key_id=invoice.key_id,
        status=invoice.status,
        reconciliation_id=invoice.reconciliation_id,
        amount=invoice.amount,
        cashier_type=invoice.cashier_type,
        cashier_bank_code=invoice.cashier_bank_code,
        cash_amount=invoice.cash_amount
    )
)
```

## Create BrcodePreviews
You can create BrcodePreviews to preview BR Codes before paying them.

```python
import starkinfra

previews = starkinfra.brcodepreview.create([
    starkinfra.BrcodePreview(
        id="00020126420014br.gov.bcb.pix0120nedstark@hotmail.com52040000530398654075000.005802BR5909Ned Stark6014Rio de Janeiro621605126674869738606304FF71"
    ),
    starkinfra.BrcodePreview(
        id="00020126430014br.gov.bcb.pix0121aryastark@hotmail.com5204000053039865406100.005802BR5910Arya Stark6014Rio de Janeiro6216051262678188104863042BA4"
    ),
])

for preview in previews:
    print(preview)
```

## Credit Note

### Create CreditNotes
You can create a CreditNote to generate a CCB contract:

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
            starkinfra.creditnote.Invoice(
                due="2023-06-25",
                amount=120000,
                fine=10,
                interest=2,
                tax_id="012.345.678-90",
                name="Jamie Lannister"
            )
        ],
        payment=starkinfra.creditnote.Transfer(
            bank_code="00000000",
            branch_code="1234",
            account_number="129340-1",
            name="Jamie Lannister",
            tax_id="012.345.678-90",
            amount=100000,
        ),
        payment_type="transfer",
        signers=[
            starkinfra.creditsigner.CreditSigner(
                name="Jamie Lannister",
                contact="jamie.lannister@gmail.com",
                method="link"
            )
        ],
        external_id="1234",
        street_line_1="Av. Paulista, 200",
        street_line_2="10 andar",
        district="Bela Vista",
        city="Sao Paulo",
        state_code="SP",
        zip_code="01310-000",
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

note = starkinfra.creditnote.cancel("5155165527080960")

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

## Credit Preview
You can preview different types of credits before creating them (Currently we only have CreditNote previews):

### Create a CreditNotePreview
You can preview a Credit Note before the creation of the CCB contract:

```python
import starkinfra

previews = starkinfra.creditpreview.create([
    starkinfra.CreditPreview(
        type="credit-note"
        credit=starkinfra.creditpreview.CreditNotePreview(
            initial_amount=2478,
            initial_due="2022-07-22",
            nominal_amount=90583,
            nominal_interest=3.7,
            rebate_amount=23,
            scheduled="2022-06-28",
            tax_id="477.954.506-44",
            type="sac"
        )
    ),
    starkinfra.CreditPreview(
        type="credit-note"
        credit=starkinfra.creditpreview.CreditNotePreview(
            initial_amount=4449,
            initial_due="2022-07-16",
            interval="year",
            nominal_amount=96084,
            nominal_interest=3.1,
            rebate_amount=239,
            scheduled="2022-07-02",
            tax_id="81.882.684/0001-02",
            type="price"
        )
    ),
    starkinfra.CreditPreview(
        type="credit-note"
        credit=starkinfra.creditpreview.CreditNotePreview(
            count=8,
            initial_due="2022-07-18",
            nominal_amount=6161,
            nominal_interest=3.2,
            scheduled="2022-07-03",
            tax_id="59.352.830/0001-20",
            type="american"
        )
    ),
    starkinfra.CreditPreview(
        type="credit-note"
        credit=starkinfra.creditpreview.CreditNotePreview(
            initial_due="2022-07-13",
            nominal_amount=86237,
            nominal_interest=2.6,
            scheduled="2022-07-03",
            tax_id="37.293.955/0001-94",
            type="bullet"
        )
    ),
    starkinfra.CreditPreview(
        type="credit-note"
        credit=starkinfra.creditpreview.CreditNotePreview(
            invoices=[
                starkinfra.creditnote.Invoice(
                    amount=14500,
                    due="2022-08-19"
                ),
                starkinfra.creditnote.Invoice(
                    amount=14500,
                    due="2022-09-25"
                )
            ],
            nominal_amount=29000,
            rebate_amount=900,
            scheduled="2022-07-31",
            tax_id="36.084.400/0001-70",
            type="custom"
        )
    )
])

for preview in previews:
    print(preview)
```

**Note**: Instead of using CreditPreview objects, you can also pass each element in dictionary format

## Webhook

### Create a webhook subscription

To create a webhook subscription and be notified whenever an event occurs, run:

```python
import starkinfra

webhook = starkinfra.webhook.create(
    url="https://webhook.site/dd784f26-1d6a-4ca6-81cb-fda0267761ec",
    subscriptions=[
        "credit-note",
        "issuing-card", "issuing-invoice", "issuing-purchase",
        "pix-request.in", "pix-request.out", "pix-reversal.in", "pix-reversal.out", "pix-claim", "pix-key", "pix-chargeback", "pix-infraction",
    ],
)

print(webhook)
```

### Query webhooks

To search for registered webhooks, run:

```python
import starkinfra

webhooks = starkinfra.webhook.query()

for webhook in webhooks:
    print(webhook)
```

### Get a webhook

You can get a specific webhook by its id.

```python
import starkinfra

webhook = starkinfra.webhook.get("1082736198236817")

print(webhook)
```

### Delete a webhook

You can also delete a specific webhook by its id.

```python
import starkinfra

webhook = starkinfra.webhook.delete("1082736198236817")

print(webhook)
```

### Process webhook events

It's easy to process events delivered to your Webhook endpoint.
Remember to pass the signature header so the SDK can make sure it was StarkInfra that sent you the event.

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

elif "issuing-card" in event.subscription:
    print(event.log.card)

elif "issuing-invoice" in event.subscription:
    print(event.log.invoice)

elif "issuing-purchase" in event.subscription:
    print(event.log.purchase)

elif "credit-note" in event.subscription:
    print(event.log.note)
```

### Query webhook events

To search for webhooks events, run:

```python
import starkinfra

events = starkinfra.event.query(after="2020-03-20", is_delivered=False)

for event in events:
    print(event)
```

### Get a webhook event

You can get a specific webhook event by its id.

```python
import starkinfra

event = starkinfra.event.get("1082736198236817")

print(event)
```

### Delete a webhook event

You can also delete a specific webhook event by its id.

```python
import starkinfra

event = starkinfra.event.delete("10827361982368179")

print(event)
```

### Set webhook events as delivered

This can be used in case you've lost events.
With this function, you can manually set events retrieved from the API as
"delivered" to help future event queries with `is_delivered=False`.

```python
import starkinfra

event = starkinfra.event.update(id="1298371982371921", is_delivered=True)

print(event)
```

### Query failed webhook event delivery attempts information

You can also get information on failed webhook event delivery attempts.

```python
import starkinfra

attempts = starkinfra.event.attempt.query(after="2020-03-20")

for attempt in attempts:
    print(attempt.code)
    print(attempt.message)
```

### Get a failed webhook event delivery attempt information

To retrieve information on a single attempt, use the following function:

```python
import starkinfra

attempt = starkinfra.event.attempt.get("1616161616161616")

print(attempt)
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
            external_id="1723843582395893",
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
