version = "0.17.0"
language = "en-US"
timeout = 15
user = None
request_methods_prefix = "Joker"

from starkcore import Project, Organization, key, error

from . import event
from .event.__event import Event

from . import brcodepreview
from .brcodepreview.__brcodepreview import BrcodePreview

from . import pixrequest
from .pixrequest.__pixrequest import PixRequest

from . import pixreversal
from .pixreversal.__pixreversal import PixReversal

from . import pixstatement
from .pixstatement.__pixstatement import PixStatement

from . import pixbalance
from .pixbalance.__pixbalance import PixBalance

from . import pixdirector
from .pixdirector.__pixdirector import PixDirector

from . import pixkey
from .pixkey.__pixkey import PixKey

from . import pixclaim
from .pixclaim.__pixclaim import PixClaim

from . import pixdomain
from .pixdomain.__pixdomain import PixDomain

from . import pixfraud
from .pixfraud.__pixfraud import PixFraud

from . import pixinfraction
from .pixinfraction.__pixinfraction import PixInfraction

from . import pixchargeback
from .pixchargeback.__pixchargeback import PixChargeback

from . import pixuser
from .pixuser.__pixuser import PixUser

from . import issuingbalance
from .issuingbalance.__issuingbalance import IssuingBalance

from . import issuingbillinginvoice
from .issuingbillinginvoice.__issuingbillinginvoice import IssuingBillingInvoice

from . import issuingbillingtransaction
from .issuingbillingtransaction.__issuingbillingtransaction import IssuingBillingTransaction

from . import creditnote
from .creditnote.__creditnote import CreditNote

from . import creditsigner
from .creditsigner.__creditsigner import CreditSigner

from . import creditpreview
from .creditpreview.__creditpreview import CreditPreview

from . import creditholmes
from .creditholmes.__creditholmes import CreditHolmes

from . import individualidentity
from .individualidentity.__individualidentity import IndividualIdentity

from . import individualdocument
from .individualdocument.__individualdocument import IndividualDocument

from . import dynamicbrcode
from .dynamicbrcode.__dynamicbrcode import DynamicBrcode

from . import staticbrcode
from .staticbrcode.__staticbrcode import StaticBrcode

from . import issuingtransaction
from .issuingtransaction.__issuingtransaction import IssuingTransaction

from . import issuingholder
from .issuingholder.__issuingholder import IssuingHolder

from . import issuingcard
from .issuingcard.__issuingcard import IssuingCard

from . import issuingpurchase
from .issuingpurchase.__issuingpurchase import IssuingPurchase

from . import issuinginvoice
from .issuinginvoice.__issuinginvoice import IssuingInvoice

from . import issuingwithdrawal
from .issuingwithdrawal.__issuingwithdrawal import IssuingWithdrawal

from . import issuingproduct
from .issuingproduct.__issuingproduct import IssuingProduct

from . import issuingrule
from .issuingrule.__issuingrule import IssuingRule

from . import issuingstock
from .issuingstock.__issuingstock import IssuingStock

from . import issuingrestock
from .issuingrestock.__issuingrestock import IssuingRestock

from . import issuingdesign
from .issuingdesign.__issuingdesign import IssuingDesign

from . import issuingembossingrequest
from .issuingembossingrequest.__issuingembossingrequest import IssuingEmbossingRequest

from . import issuingembossingkit
from .issuingembossingkit.__issuingembossingkit import IssuingEmbossingKit

from . import issuingtoken
from .issuingtoken.__issuingtoken import IssuingToken

from . import issuingtokendesign
from .issuingtokendesign.__issuingtokendesign import IssuingTokenDesign

from . import issuingtokenrequest
from .issuingtokenrequest.__issuingtokenrequest import IssuingTokenRequest

from . import issuingtokenactivation
from .issuingtokenactivation.__issuingtokenactivation import IssuingTokenActivation

from . import merchantcategory
from .merchantcategory.__merchantcategory import MerchantCategory

from . import merchantcountry
from .merchantcountry.__merchantcountry import MerchantCountry

from . import cardmethod
from .cardmethod.__cardmethod import CardMethod

from . import webhook
from .webhook.__webhook import Webhook

from .utils import endtoendid, returnid

from . import request