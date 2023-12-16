"""

Recommendations are classes that provide guidance
toward the next course of action.

** Example: **
```python
def compute_results(self) -> ProtocolResult:
    result = ProtocolResult()

    if self.has_suspect_eye_condition:
        title = ('Consider updating the Diabetes without complications (E11.9) '
                 'to Diabetes with secondary eye disease as clinically appropriate.')
        result.add_narrative(comment)
        result.add_diagnose_recommendation(
            key='HCC003v1_RECOMMEND_DIAGNOSE_EYE',
            rank=1,
            button='Diagnose',
            title=title,
            narrative=f'{self.patient.first_name} has Diabetes without complications,
            command={'key': 'diagnose'})

"""

from typing import List, Optional, Type, Dict

from .constants import (
    COMMAND_TYPE_ALLERGY,
    COMMAND_TYPE_ASSESS,
    COMMAND_TYPE_DIAGNOSE,
    COMMAND_TYPE_FOLLOWUP,
    COMMAND_TYPE_IMAGING,
    COMMAND_TYPE_IMMUNIZATION,
    COMMAND_TYPE_INSTRUCTION,
    COMMAND_TYPE_INTERVIEW,
    COMMAND_TYPE_LAB_ORDER,
    COMMAND_TYPE_PERFORM,
    COMMAND_TYPE_PLAN,
    COMMAND_TYPE_PRESCRIBE,
    COMMAND_TYPE_REFERRAL,
    COMMAND_TYPE_STRUCTURED_ASSESSMENT,
    COMMAND_TYPE_TASK,
    COMMAND_TYPE_VITALSIGN
)
from .patient import Patient
from .value_set.value_set import ValueSet
from .intervention import Intervention

# Lower numbers displayed first
RANK_MAX = 1000


class Recommendation(Intervention):
    """
    A standard recommendation.
    """

    # HACK: title and narrative have defaults here so I didn't have to reorder the arguments when
    # adding a default for rank (to make it optional)
    def __init__(self,
                 key,
                 rank=RANK_MAX,
                 button='',
                 title=None,
                 narrative=None,
                 command=None,
                 context=None,
                 href=None):
        if not title:
            raise ValueError

        self.button = button
        self.command = command or {}
        self.context = context or {}
        self.key = key
        self.narrative = narrative
        self.rank = rank
        self.title = title
        self.href = href

    @staticmethod
    def command_filter(command_type: str, value_sets: List[Type[ValueSet]]):
        """
        Build up a command that contains a search filter by value set
        system codes, like a search for a particular vaccine or lab or
        medicine to prescribe.
        """

        # sets to lists for json encode - can't directly encode sets
        codes = {}
        for value_set in value_sets:
            for system in value_set.values:
                if system not in codes:
                    codes[system] = {'system': system, 'code': list()}

                codes[system]['code'].extend(list(value_set.values[system]))

        return {
            'type': command_type,
            'filter': {
                'coding': [val for key, val in codes.items()],
            },
        }


class AllergyRecommendation(Recommendation):
    """
    A recommendation specifying an allergy to add to the patient's allergy list.
    """

    def __init__(
            self, key, allergy: Type[ValueSet], rank=RANK_MAX, button='Allergy',
            title=None, narrative=None, context=None):
        if not title:
            title = allergy.name
        if not narrative:
            narrative = ''

        command = self.command_filter(COMMAND_TYPE_ALLERGY, [allergy])

        super().__init__(
            key, rank, button, title=title, narrative=narrative, command=command, context=context
        )

class AssessRecommendation(Recommendation):
    """
    A recommendation specifying an assessment of the patient's condition.
    """

    def __init__(self, key, patient: Patient, rank=RANK_MAX, button='Assess', title=None, context=None):
        command = {'type': COMMAND_TYPE_ASSESS}

        if not title:
            title = 'Assess condition'

        super().__init__(key, rank, button, title, command=command, context=context)


class DiagnoseRecommendation(Recommendation):
    """
    A recommendation specifying a condition to diagnose the patient.
    """

    def __init__(
            self, key, patient: Patient, condition: Type[ValueSet],
            rank=RANK_MAX, button='Diagnose', title=None, narrative=None, context=None):
        if not title:
            title = condition.name
        if not narrative:
            narrative = f'Consider diagnosing {patient.first_name} with {condition.name}'

        command = self.command_filter(COMMAND_TYPE_DIAGNOSE, [condition])

        super().__init__(
            key, rank, button, title=title, narrative=narrative, command=command, context=context)


class FollowUpRecommendation(Recommendation):
    """
    A recommendation specifying a follow-up appointment for the patient.
    """

    def __init__(
            self, key, patient: Patient, rank=RANK_MAX, button='Follow up', title=None,
            narrative=None, context=None):
        if not title:
            title = 'Request follow-up appointment'
        if not narrative:
            narrative = f'{patient.first_name} needs a follow-up appointment'

        command = {'type': COMMAND_TYPE_FOLLOWUP}

        super().__init__(key, rank, button, title, narrative=narrative, command=command, context=context)


class ImagingRecommendation(Recommendation):
    """
    A recommendation specifying an imaging to order. Title and narrative are
    auto-generated but may be overridden.
    """

    def __init__(self,
                 key,
                 patient: Patient,
                 imaging,
                 rank=RANK_MAX,
                 button='Order',
                 title=None,
                 narrative=None,
                 context=None):
        if not title:
            title = f'Order {imaging.name}'
            narrative = f'{patient.first_name} should be ordered {imaging.name}.'

        command = self.command_filter(COMMAND_TYPE_IMAGING, [imaging])

        super().__init__(
            key, rank, button, title=title, narrative=narrative, command=command, context=context)


class ImmunizationRecommendation(Recommendation):
    """
    A recommendation specifying an immunization to order. Use this to guide the user to the
    [immunization command](https://canvas-medical.zendesk.com/hc/en-us/articles/360057140293-Documenting-an-Immunization)
    """

    def __init__(self,
                 key,
                 patient: Patient,
                 immunization: Type[ValueSet],
                 rank=RANK_MAX,
                 button='Order',
                 title=None,
                 narrative=None,
                 context=None):
        # use patient, condition and lab to generate text and commands
        if not title:
            title = f'Order {immunization.name}'
            narrative = f'{patient.first_name} should get an {immunization.name}.'

        command = self.command_filter(COMMAND_TYPE_IMMUNIZATION, [immunization])

        super().__init__(key, rank, button, title=title, narrative=narrative, command=command, context=context)


class InstructionRecommendation(Recommendation):
    """
    A recommendation specifying an instruction for the patient.
    """

    def __init__(self,
                 key,
                 patient: Patient,
                 instruction: Type[ValueSet],
                 rank=RANK_MAX,
                 button='Instruct',
                 title=None,
                 narrative=None,
                 context=None):
        # use patient, condition and lab to generate text and commands
        if not title:
            title = f'Instruct {instruction.name}'
            narrative = f'{patient.first_name} should get an {instruction.name}.'

        command = self.command_filter(COMMAND_TYPE_INSTRUCTION, [instruction])

        super().__init__(key, rank, button, title=title, narrative=narrative, command=command, context=context)


class InterviewRecommendation(Recommendation):
    """
    A recommendation specifying an interview for the patient.
    """

    # questionnaire should be a set of ValueSet
    def __init__(self,
                 key,
                 patient: Patient,
                 questionnaires: List[Type[ValueSet]],
                 rank=RANK_MAX,
                 button='Plan',
                 title=None,
                 narrative=None,
                 context=None):
        # use patient, condition and lab to generate text and commands
        if not title:
            labels = ', '.join([item.name for item in questionnaires])
            title = 'Interview %s' % labels
            narrative = '%s should be given a %s.' % (patient.first_name, labels)

        command = self.command_filter(COMMAND_TYPE_INTERVIEW, questionnaires)

        super().__init__(key, rank, button, title=title, narrative=narrative, command=command, context=context)


class LabRecommendation(Recommendation):
    """
    A recommendation specifying a lab to order. Title and narrative are auto-generated but
    may be overridden.
    """

    def __init__(self,
                 key: str,
                 patient: Patient,
                 condition: Type[ValueSet],
                 lab: Type[ValueSet],
                 rank: int = RANK_MAX,
                 button: str = 'Order',
                 title=None,
                 narrative=None,
                 context=None):
        # use patient, condition and lab to generate text and commands
        if not title:
            title = f'Order {lab.name}'
            narrative = (
                f'{patient.first_name} has {condition.name} and a {lab.name} is recommended.')

        command = self.command_filter(COMMAND_TYPE_LAB_ORDER, [lab])

        super().__init__(
            key, rank, button, title=title, narrative=narrative, command=command, context=context)


class PerformRecommendation(Recommendation):
    """
    A recommendation specifying a procedure to perform. Title and narrative are
    auto-generated but may be overridden.
    """

    def __init__(self,
                 key: str,
                 patient: Patient,
                 procedure: Type[ValueSet],
                 condition: Type[ValueSet],
                 rank: int = RANK_MAX,
                 button: str = 'Perform',
                 title: Optional[str] = None,
                 narrative: Optional[str] = None,
                 context: Optional[Dict] = None):
        if not title:
            title = f'Perform {procedure.name}'
            narrative = (f'{patient.first_name} has {condition.name} and a {procedure.name} is '
                         'recommended.')

        command = self.command_filter(COMMAND_TYPE_PERFORM, [procedure])

        super().__init__(key, rank, button, title=title, narrative=narrative, command=command, context=context)


class PlanRecommendation(Recommendation):
    """
    A recommendation advising the provider to make a plan for the patient.
    """

    def __init__(
            self, key, patient: Patient, rank=RANK_MAX, button='Plan', title=None, narrative=None,
            context=None):
        # use patient, condition and lab to generate text and commands
        if not title:
            title = 'Make a plan'
            narrative = f'{patient.first_name} should have a plan.'

        command = {'type': COMMAND_TYPE_PLAN}

        super().__init__(key, rank, button, title=title, narrative=narrative, command=command, context=context)


class PrescribeRecommendation(Recommendation):
    """
    A recommendation specifying an prescribe for the patient.
    """

    def __init__(self,
                 key,
                 patient: Patient,
                 prescription: Type[ValueSet],
                 rank=RANK_MAX,
                 button: str = 'Prescribe',
                 title=None,
                 narrative=None,
                 context=None):
        # use patient, condition and lab to generate text and commands
        if not title:
            title = f'Prescribe {prescription.name}'
            narrative = f'{patient.first_name} should be prescribed {prescription.name}.'

        command = self.command_filter(COMMAND_TYPE_PRESCRIBE, [prescription])

        super().__init__(key, rank, button, title=title, narrative=narrative, command=command, context=context)


class ReferRecommendation(Recommendation):
    """
    A recommendation specifying a referral to order. Title and narrative are
    auto-generated but may be overridden.
    """

    def __init__(self,
                 key: str,
                 patient: Patient,
                 referral: Type[ValueSet],
                 condition: Optional[Type[ValueSet]] = None,
                 rank: int = RANK_MAX,
                 button: str = 'Refer',
                 title=None,
                 narrative=None,
                 context=None):
        if not title:
            title = f'Refer {referral.name}'

            if condition:
                narrative = (
                    f'{patient.first_name} has {condition.name} and should be referred for '
                    f'{referral.name}.')
            else:
                narrative = f'{patient.first_name} should be referred for {referral.name}.'

        command = self.command_filter(COMMAND_TYPE_REFERRAL, [referral])

        super().__init__(
            key, rank, button, title=title, narrative=narrative, command=command, context=context)


class StructuredAssessmentRecommendation(Recommendation):
    """
    StructuredAssessmentRecommendation

    A recommendation specifying a structured assessment for the patient.
    """

    # questionnaire should be a set of ValueSet
    def __init__(self,
                 key,
                 patient: Patient,
                 questionnaires: List[Type[ValueSet]],
                 rank=RANK_MAX,
                 button: str = 'Assess',
                 title=None,
                 narrative=None,
                 context=None):
        if not title:
            labels = ', '.join([item.name for item in questionnaires])
            title = f'Interview {labels}'
            narrative = f'{patient.first_name} should be given a {labels}.'

        command = self.command_filter(COMMAND_TYPE_STRUCTURED_ASSESSMENT, questionnaires)

        super().__init__(key, rank, button, title=title, narrative=narrative, command=command, context=context)


class TaskRecommendation(Recommendation):
    """
    A recommendation advising the provider to setup a task for someone else.
    """

    def __init__(self, patient, *args, **kwargs):
        super().__init__(command={'type': COMMAND_TYPE_TASK}, *args, **kwargs)


class VitalSignRecommendation(Recommendation):
    """
    A recommendation specifying a vital sign reading should be taken.
    """

    def __init__(
            self, key, patient: Patient, rank=RANK_MAX, button='Plan', title=None, narrative=None,
            context=None):
        # use patient, condition and lab to generate text and commands
        if not title:
            title = 'Collect vitals'
            narrative = f'{patient.first_name} should vital signs collected.'

        command = {'type': COMMAND_TYPE_VITALSIGN}

        super().__init__(key, rank, button, title=title, narrative=narrative, command=command, context=context)


class HyperlinkRecommendation(Recommendation):
    """
    A recommendation specifying a button and href that opens a link in a new tab.
    """

    def __init__(self, key, href, title='', button='', rank=RANK_MAX):
        super().__init__(key, rank, button, title=title, href=href)
