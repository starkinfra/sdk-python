# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to the following versioning pattern:

Given a version number MAJOR.MINOR.PATCH, increment:

- MAJOR version when the **API** version is incremented. This may include backwards incompatible changes;
- MINOR version when **breaking changes** are introduced OR **new functionalities** are added in a backwards compatible manner;
- PATCH version when backwards compatible bug **fixes** are implemented.


## [Unreleased]
### Added
- expand as query parameter to pix key resource
- reason parameter on pix key cancellation resource

## [0.18.0] - 2025-04-23
### Added
- priority to pix request resource
### Fixed
- BrCodePreview status param documentation

## [0.17.0] - 2025-04-04
### Added
- CCB disbursement pdf file (`starkinfra.creditnote.pdf`)
### Fixed
- CreditNote datetime properties

## [0.16.0] - 2025-03-31
### Added
- IssuingBillingTransaction resource
- IssuingBillingInvoice resource

## [0.15.0] - 2025-03-19
### Added
- operator_email and operator_phone to PixInfraction resource

## [0.14.0] - 2024-12-04
### Added
- description to BR Code preview
- data to Dynamic BR Code
### Fixed
- readme

## [0.13.0] - 2024-09-25
### Added
- installment data to IssuingPurchase resource
- pixReversal description

## [0.12.0] - 2024-07-01
### Added
- request methods
### Changed
- starkcore to v0.5.0
### Fixed
- request prefix param

## [0.11.0] - 2024-03-19
### Added
- Update IssuingPurchase

## [0.10.1] - 2023-11-13
### Fixed
- fraud_type parameter to PixInfraction resource

## [0.10.0] - 2023-11-13
### Added
- PixUser resource
- PixFraud resource
- IssuingToken resource
- IssuingTokenLog resource
- IssuingTokenDesign resource
- IssuingTokenRequest sub-resource
- IssuingTokenActivation sub-resource
- method, fraud_type and fraud_id parameters to PixInfraction resource
- bacen_id attribute to PixClaim, PixChargeback, PixInfraction resources
- merchant_category_type, description and holder_id attributes to IssuingPurchase resource
### Changed
- type parameter to PixInfraction resource
- sender_tax_id and receiver_tax_id parameters to DynamicBrcode resource

## [0.9.0] - 2023-06-21
### Added
- metadata attribute to IssuingPurchase resource
### Changed
- starkcore to v0.1.1

## [0.8.0] - 2023-05-11
### Added
- payer_id and end_to_end_id parameter to BrcodePreview resource
- description parameter to StaticBrcode resource
### Changed
- nominal_amount and amount parameter to conditionally required to CreditNote resource

## [0.7.0] - 2023-04-27
### Added
- CreditHolmes resource
- IssuingEmbossingKit resource
- cashier_bank_code attribute to StaticBrcode resource

## [0.6.0] - 2022-12-02
### Added
- product_id attribute to IssuingPurchase resource
- type attribute to IssuingDesign resource

## [0.5.0] - 2022-11-23
### Changed
- IssuingPurchase.Log errors field from JSON to StarkInfra.Error Object
### Added
- IssuingDesign resource
- IssuingStock resource
- IssuingRestock resource
- IssuingEmbossingRequest resource
### Fixed
- identity ids parameter on IndividualIdentityLog

## [0.4.0] - 2022-11-11
### Added
- IndividualIdentity resource
- IndividualDocument resource

## [0.3.1] - 2022-10-08
### Fixed
- Fixed query() cursor and limit iteration

## [0.3.0] - 2022-08-26
### Changed
- amount to nominal_amount, fine_amount to fine, interest_amount to interest, and discount_amount to discounts on response_due method of DynamicBrcode resource
- settlement parameter to funding_type of Issuing Product resource
- client parameter to holder_type of Issuing Product resource
- CreditNotePreview sub-resource to CreditPreview.CreditNotePreview sub-resource
- agent parameter to flow in PixInfraction and PixChargeback resources
- bank_code parameter to claimer_bank_code in PixClaim resource
- agent parameter to flow on query and page methods in PixInfraction and PixChargeback resources
### Fixed
- JSON body returned from response method of PixRequest resource
- JSON body returned from response method of PixReversal resource
### Added
- key_id, cash_amount, cashier_bank_code and cashier_type attributes to BrcodePreview resource 
- code attribute to IssuingProduct resource
- expand parameter to create method of IssuingHolder resource
- CreditPreview sub-resource
- default to fee, external_id and tags on PixRequest and PixReversal parse method
- BrcodePreview resource
- tags parameter to PixClaim, PixInfraction, Pix Chargeback, DynamicBrcode and StaticBrcode resources
- flow parameter to PixClaim resource
- flow parameter to query and page methods to PixClaim
- tags parameter to query and page methods to PixChargeback, PixClaim and PixInfraction resources
- zip_code, purchase, is_partial_allowed, card_tags and holder_tags attributes to IssuingPurchase resource
- brcode, link and due attributes to IssuingInvoice resource
### Removed
- category parameter to IssuingProduct resource
- bacen_id parameter from PixChargeback and PixInfraction resources
- agent parameter from PixClaim.Log resource

## [0.2.0] - 2022-07-07
### Added
- StaticBrcode resource
- DynamicBrcode resource
- CreditNotePreview sub-resource
- IssuingRule.Method sub-resources
- IssuingRule.Country sub-resources
- IssuingRule.Category sub-resources
- parse method to IssuingPurchase resource
- response method to PixRequest, PixReversal and IssuingPurchase resources
- nominal_interest attribute to CreditNote resource
### Removed
- IssuingAuthorization resource
- bank_code attribute from PixReversal resource
### Changed
- IssuingBin resource to IssuingProduct
- fine and interest attributes to return only on CreditNote.Invoice sub-resource
- expiration in the CreditNote resource from returned-only to optional parameter
- Creditnote.Signer sub-resource to CreditSigner resource

## [0.1.1] - 2022-06-09
### Fixed
- validation for masked dates and datetimes

## [0.1.0] - 2022-06-03
### Added
- credit receiver's billing address on CreditNote
### Fixed
- after and before parameter types on query and page methods

## [0.0.7] - 2022-05-23
### Added
- CreditNote.Signer sub-resource
- CreditNote.Invoice sub-resource
- CreditNote.Transfer sub-resource
- issuinginvoice.log.get() function
- Webhook resource to receive Events
- merchant_fee atribute to IssuingPurchase
### Changed
- rules parameter from IssuingCard and IssuingHolder objects returned from the 
  API changed from a list of dictionaries to a list of IssuingHolder objects
- CreditNote.transfer parameter to payment and payment_type
- BrcodeCertificate resource name to PixDomain
- InfractionReport resource name to PixInfraction
- ReversalRequest resource name to PixChargeback
- PixInfraction and PixChargeback to post in batches
- delete methods name to cancel

## [0.0.6] - 2022-05-04
### Added
- BrcodeCertificate resource for Indirect and Direct Participants

## [0.0.5] - 2022-05-02
### Added
- PixDirector resource for Indirect and Direct Participants

## [0.0.4] - 2022-05-01
### Added
- expand parameter to issuingholder.get()
- PixClaim resource for Indirect and Direct Participants
- PixKey resource for Indirect and Direct Participants
- InfractionReport resource for Indirect and Direct Participants
- ReversalRequest resource for Indirect and Direct Participants
- event.get(), event.query(), event.page(), event.delete() and event.update() functions
- Event.Attempt sub-resource to allow retrieval of information on failed webhook event delivery attempts

## [0.0.3] - 2022-04-22
### Added
- CreditNote resource for money lending with Stark Infra's endorsement
- IssuingAuthorization resource for Sub Issuers
- IssuingBalance resource for Sub Issuers
- IssuingBin resource for Sub Issuers
- IssuingCard resource for Sub Issuers
- IssuingHolder resource for Sub Issuers
- IssuingInvoice resource for Sub Issuers
- IssuingPurchase resource for Sub Issuers
- IssuingTransaction resource for Sub Issuers
- IssuingWithdrawal resource for Sub Issuers

## [0.0.2] - 2022-03-15
### Added
- PixRequest resource for Indirect and Direct Participants
- PixReversal resource for Indirect and Direct Participants
- PixDirector resource for Indirect and Direct Participants
- PixBalance resource for Indirect and Direct Participants
- PixStatement resource for Direct Participants
- Event resource for webhook receptions
