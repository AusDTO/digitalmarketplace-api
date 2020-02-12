import collections

import pendulum

from app.api.business.agreement_business import (get_current_agreement,
                                                 get_new_agreement,
                                                 has_signed_current_agreement)
from app.api.business.validators import SupplierValidator
from app.api.services import application_service, key_values_service, suppliers
import requests as req
import os, ssl


def abn_is_used(abn):
    abn = "".join(abn.split())
    supplier = suppliers.get_supplier_by_abn(abn)
    if supplier:
        return True
    application = application_service.get_applications_by_abn(abn)
    if application:
        return True
    return False

def validate_abn(abn):
        # GUID
    authenticationGuid = '7ef41140-8406-40b4-8bf2-12582b5404ce'
    includeHistoricalDetails = 'N'
    abn = abn
    # if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    #     getattr(ssl, '_create_unverified_context', None)):
    #     ssl._create_default_https_context = ssl._create_unverified_contexta

    includeHistoricalDetails = 'N'


    # need to import os, ssl since i get this error URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:727)>
    conn = req.get('https://abr.business.gov.au/abrxmlsearch/AbrXmlSearch.asmx/SearchByABNv201205?searchString=' + abn + '&includeHistoricalDetails='+ includeHistoricalDetails +'&authenticationGuid='+ authenticationGuid)
    # conn.status_code == requests.codes.ok will print True or if you do conn.status_code will print out 200
    print('HELLOOOOOOOOO')
    print(conn.text)
    # returnedXML = conn.get_data()
    # f = open('output.xml', 'wb')
    # f.write(returnedXML)
    # f.close
    # print(returnedXML)

def get_supplier_messages(code, skip_application_check):
    applications = application_service.find(
        supplier_code=code,
        type='edit'
    ).all()

    supplier = suppliers.get_supplier_by_code(code)
    validation_result = SupplierValidator(supplier).validate_all()

    if any([a for a in applications if a.status == 'saved']):
        validation_result.warnings.append({
            'message': 'You have saved updates on your profile. '
                       'You must submit these changes to the Marketplace for review. '
                       'If you did not make any changes, select \'Discard all updates\'.',
            'severity': 'warning',
            'step': 'update',
            'id': 'SB001'
        })

    if not skip_application_check:
        if any([a for a in applications if a.status == 'submitted']):
            del validation_result.warnings[:]
            del validation_result.errors[:]

    if not has_signed_current_agreement(supplier):
        if get_current_agreement():
            message = (
                'Your authorised representative {must accept the new Master Agreement} '
                'before you can apply for opportunities.'
            )
            validation_result.errors.append({
                'message': message,
                'severity': 'error',
                'step': 'representative',
                'id': 'SB002',
                'links': {
                    'must accept the new Master Agreement': '/2/seller-edit/{}/representative'.format(code)
                }
            })
    else:
        new_master_agreement = get_new_agreement()
        if new_master_agreement:
            start_date = new_master_agreement.start_date.in_tz('Australia/Canberra').date()
            message = (
                'From {}, your authorised representative must '
                'accept the new Master Agreement '
                'before you can apply for opportunities.'
            ).format(start_date.strftime('%-d %B %Y'))

            validation_result.warnings.append({
                'message': message,
                'severity': 'warning',
                'step': 'representative',
                'id': 'SB002'
            })

    return validation_result
