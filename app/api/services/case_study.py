from app import db
from app.api.helpers import Service
from app.models import CaseStudy, Domain

from sqlalchemy import and_, func, or_


class CaseStudyService(Service):
    __model__ = CaseStudy

    def __init__(self, *args, **kwargs):
        super(CaseStudyService, self).__init__(*args, **kwargs)

    def get_approved_case_studies_by_supplier_code(self, supplier_code, domain_id):
        domain_name = (
            db
            .session
            .query(Domain.name)
            .filter(Domain.id == domain_id)
            .subquery()
        )

        case_study = (
            db.session.query(CaseStudy.id.label('cs_id'), CaseStudy.data)
            .filter(CaseStudy.supplier_code == supplier_code,
                    CaseStudy.status == 'approved',
                    CaseStudy.data['service'].astext == domain_name.c.name
                    )
        )

        cs_values = case_study.all()
        t = {}
        for value in case_study.all():
            t = value

        # print('t')
        # print(t)
        # test = {}
        # for k, v in cs_values:
        #     for k1, v1 in v.items():
        #         if k1 == 'service':
        #             test['category_name'] = v1

        return [value._asdict() for value in case_study.all()]
