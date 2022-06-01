# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to the following versioning pattern:

Given a version number MAJOR.MINOR.PATCH, increment:

- MAJOR version when the **API** version is incremented. This may include backwards incompatible changes;
- MINOR version when **breaking changes** are introduced OR **new functionalities** are added in a backwards compatible manner;
- PATCH version when backwards compatible bug **fixes** are implemented.


## [Unreleased]
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
