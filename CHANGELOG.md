# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to the following versioning pattern:

Given a version number MAJOR.MINOR.PATCH, increment:

- MAJOR version when the **API** version is incremented. This may include backwards incompatible changes;
- MINOR version when **breaking changes** are introduced OR **new functionalities** are added in a backwards compatible manner;
- PATCH version when backwards compatible bug **fixes** are implemented.


## [Unreleased]

## [0.3.1] - 2022-10-08
### Fixed
- Fixed query() cursor and limit iteration

## [0.3.0] - 2022-08-26
### Changed
- CreditNotePreview sub-resource to CreditPreview.CreditNotePreview sub-resource
- amount to nominal_amount, fine_amount to fine, interest_amount to interest, and discount_amount to discounts in response_due method of DynamicBrcode resource
- settlement parameter to funding_type in IssuingProduct resource
- client parameter to holder_type in IssuingProduct resource
- agent parameter to flow in PixInfraction and PixChargeback resources
- agent parameter to flow in query and page methods of PixInfraction and PixChargeback resources
- bank_code parameter to claimer_bank_code in PixClaim resource
### Fixed
- JSON body returned from response method of PixRequest resource
- JSON body returned from response method of PixReversal resource
### Added
- BrcodePreview resource
- CreditPreview sub-resource
- key_id, cash_amount, cashier_bank_code and cashier_type attributes to BrcodePreview resource 
- code attribute to IssuingProduct resource
- expand parameter to create method of IssuingHolder resource
- default to fee, external_id and tags in parse method of PixRequest and PixReversal resources
- tags parameter to PixClaim, PixInfraction, Pix Chargeback, DynamicBrcode and StaticBrcode resources
- tags parameter to query and page methods in PixChargeback, PixClaim and PixInfraction resources
- flow parameter to PixClaim resource
- flow parameter to query and page methods of PixClaim
- zip_code, purchase, is_partial_allowed, card_tags and holder_tags attributes to IssuingPurchase resource
- brcode, link and due attributes to IssuingInvoice resource
### Removed
- category parameter from IssuingProduct resource
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
- fine and interest attributes to return only in CreditNote.Invoice sub-resource
- expiration from returned-only to optional parameter in the CreditNote resource 
- Creditnote.Signer sub-resource to CreditSigner resource

## [0.1.1] - 2022-06-09
### Fixed
- validation for masked dates and datetimes

## [0.1.0] - 2022-06-03
### Added
- credit receiver's billing address in CreditNote
### Fixed
- after and before parameter types in query and page methods

## [0.0.7] - 2022-05-23
### Added
- CreditNote.Signer sub-resource
- CreditNote.Invoice sub-resource
- CreditNote.Transfer sub-resource
- get method to issuinginvoice.Log resource
- Webhook resource
- merchant_fee attribute to IssuingPurchase
### Changed
- rules parameter from a list of dictionaries to a list of IssuingRule objects 
  in IssuingCard and IssuingHolder resources
- transfer parameter to payment and payment_type in CreditNote resource
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
- expand parameter to get method in IssuingHolder resource
- PixClaim resource for Indirect and Direct Participants
- PixKey resource for Indirect and Direct Participants
- InfractionReport resource for Indirect and Direct Participants
- ReversalRequest resource for Indirect and Direct Participants
- get, query, page, delete and update methods to Event resource
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
