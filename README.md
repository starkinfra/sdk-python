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
    - [PixRequests](#create-pix-requests): PIX receivables
    - [PixReversals](#create-pix-reversals): Reverse PIX transactions
    - [PixBalance](#get-pix-balance): Account balance
    - [PixStatement](#create-pix-statement): Account statement entry
    - [WebhookEvents](#process-webhook-events): Manage webhook events
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
(for example: `help(starkinfra.boleto.create)`)

## Create pix requests
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

**Note**: Instead of using Pix Request objects, you can also pass each transaction element in dictionary format

## Query pix requests

You can query multiple pix requests according to filters.

```python
import starkinfra
from datetime import datetime

requests = starkinfra.pixrequest.query(
    fields=["amount", "id"],
    limit=10,
    after=datetime(2020, 1, 1),
    before=datetime(2020, 4, 1),
    status="success",
    tags=["iron", "suit"],
    end_to_end_id="E79457883202101262140HHX553UPqeq",
)

for request in requests:
    print(request)
```

## Get a pix request

After its creation, information on a pix request may be retrieved by its id. Its status indicates whether it has been paid.

```python
import starkinfra

request = starkinfra.pixrequest.get("5155165527080960")

print(request)
```

## Process pix request authorization requests

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
  
## Query pix request logs

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

## Get a pix request log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.pixrequest.log.get("5155165527080960")

print(log)
```

## Create pix reversals

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

## Query pix reversals 

You can query multiple pix reversals according to filters. 

```python
import starkinfra

reversals = starkinfra.pixreversal.query(
    fields=["amount", "id"],
    limit=10,
    after=datetime(2020, 1, 1),
    before=datetime(2020, 4, 1),
    status="success",
    tags=["iron", "suit"],
    return_id="D20018183202202030109X3OoBHG74wo",
)

for reversal in reversals:
    print(reversal)
```

## Get a pix reversal

After its creation, information on a pix reversal may be retrieved by its id. Its status indicates whether it has been paid.

```python
import starkinfra

reversal = starkinfra.pixreversal.get("5155165527080960")

print(reversal)
```

## Process pix reversal authorization requests

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

## Query pix reversal logs

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

## Get a pix reversal log

You can also get a specific log by its id.

```python
import starkinfra

log = starkinfra.pixreversal.log.get("5155165527080960")

print(log)
```

## Get pix balance 

To know how much money you have in your workspace, run:

```python
import starkinfra

balance = starkinfra.pixbalance.get()

print(balance)
```

## Create pix statement

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

## Query pix statements

You can query multiple pix statements according to filters. 

```python
import starkinfra

statements = starkinfra.pixstatement.query(
    limit=50, 
    after="2022-01-01", # Note that this after and before parameters are different from the ones used in the creation of the statement. 
    before="2022-01-20",
)

for statement in statements:
    print(statement)
```

## Get a pix statement

Statements are only available for direct participants. To get a pix statement by its id:

```python
import starkinfra

statement = starkinfra.pixstatement.get("5155165527080960")

print(statement)
```

## Get a pix statement .csv file

To get a .csv file of a pix statement using its id, run:

```python
import starkinfra

csv = starkinfra.pixstatement.csv("5155165527080960")

with open("test.zip", "wb") as file:
    file.write(csv)
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

Email: developers@starkbank.com
