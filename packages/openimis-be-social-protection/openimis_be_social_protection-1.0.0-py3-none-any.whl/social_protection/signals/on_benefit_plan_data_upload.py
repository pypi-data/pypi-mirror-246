import logging

from individual.models import IndividualDataSourceUpload
from social_protection.models import BenefitPlan, BenefitPlanDataUploadRecords

logger = logging.getLogger(__name__)


def on_benefit_plan_data_upload(**kwargs):
    result = kwargs.get('result', None)
    if result:
        try:
            benefit_plan = kwargs['data'][0][1]
            workflow = kwargs['data'][0][2].name
            if not isinstance(benefit_plan, BenefitPlan):
                raise ValueError("Unexpected argument in input data.")
            upload = IndividualDataSourceUpload.objects \
                .get(id=result['data']['upload_uuid'])
            record = BenefitPlanDataUploadRecords(
                data_upload=upload,
                benefit_plan=benefit_plan,
                workflow=workflow
            )
            record.save(username=kwargs['cls_'].user.username)
        except (KeyError, ValueError) as e:
            logger.error(
                "Failed to create benefit plan data upload registry."
                F"Expected input to provide `data[0][1]` of type `benefit_plan` (input: {kwargs['data']}). "
                F"and result to provide `data.upload_uuid` (input: {result})"
            )
