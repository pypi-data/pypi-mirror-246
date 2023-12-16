from typing import List, Tuple

import arrow

from canvas_workflow_kit import settings

from canvas_workflow_kit.builtin_cqms.cms138v6p1 import ClinicalQualityMeasure138v6p1
from canvas_workflow_kit.patient_recordset import (
    BillingLineItemRecordSet,
    InterviewRecordSet,
    ProtocolOverrideRecordSet
)
from canvas_workflow_kit.tests.base import SDKBaseTest
from canvas_workflow_kit.timeframe import Timeframe


class TestClinicalQualityMeasure138v6p1(SDKBaseTest):

    def setUp(self):
        self.mocks_path = f'{settings.BASE_DIR}/builtin_cqms/tests/mock_data'

    def test_enabled(self):
        self.assertTrue(ClinicalQualityMeasure138v6p1.enabled())

    def test_description(self):
        expected = ('Patients aged 18 years and older who have not been '
                    'screened for tobacco use in the last year.')
        self.assertEqual(expected, ClinicalQualityMeasure138v6p1._meta.description)

    def test_information(self):
        expected = 'https://ecqi.healthit.gov/sites/default/files/ecqm/measures/CMS138v6.html'
        self.assertEqual(expected, ClinicalQualityMeasure138v6p1._meta.information)

    def test_change_types(self):
        result = ClinicalQualityMeasure138v6p1._meta.compute_on_change_types
        expected = [
            'protocol_override',
            'billing_line_item',
            'interview',
            'patient',
        ]
        self.assertEqual(len(expected), len(result))
        for change in expected:
            self.assertIn(change, result)

    def test_in_initial_population(self):
        start = arrow.get('2018-04-01 13:24:56')
        end = arrow.get('2019-04-01 13:24:56')
        timeframe = Timeframe(start=start, end=end)

        # patient over 18 + patient had a preventive visit
        tests = {
            '2018-03-30': False,
            '2018-04-02': True,
            '2019-02-06': True,
            '2019-03-30': True,
            '2019-04-02': False,
        }
        for on_day, expected in tests.items():
            # context guidance --> always true regardless of any visit
            patient = self.load_patient('cms138v6')
            tested = ClinicalQualityMeasure138v6p1(patient=patient, timeframe=timeframe)
            self.assertTrue(tested.in_initial_population(), f'{on_day}')

            # context report
            patient = self.load_patient('cms138v6')
            patient.billing_line_items = self.helper_visits([(on_day, '99396')])
            tested = ClinicalQualityMeasure138v6p1(patient=patient, timeframe=timeframe)
            if expected:
                self.assertTrue(tested.in_initial_population(), f'{on_day}')
            else:
                self.assertFalse(tested.in_initial_population(), f'{on_day}')

        # patient over 18 + patient had two visits
        tests = {
            '2018-03-30': False,
            '2018-04-02': True,
            '2019-02-06': True,
            '2019-03-30': True,
            '2019-04-02': False,
        }
        for on_day, expected in tests.items():
            patient = self.load_patient('cms138v6')
            patient.billing_line_items = self.helper_visits([
                (on_day, '96151'),
                (on_day, '99201'),
            ])
            tested = ClinicalQualityMeasure138v6p1(patient=patient, timeframe=timeframe)
            if expected:
                self.assertTrue(tested.in_initial_population(), f'{on_day}')
            else:
                self.assertFalse(tested.in_initial_population(), f'{on_day}')

        # patient over 18 + patient had one visit --> false
        patient = self.load_patient('cms138v6')
        patient.billing_line_items = self.helper_visits([('2019-02-06', '96151')])
        tested = ClinicalQualityMeasure138v6p1(patient=patient, timeframe=timeframe)
        self.assertFalse(tested.in_initial_population())

        # patient is not 18 + patient had a preventive visit --> false
        patient = self.load_patient('cms138v6')
        patient.patient['birthDate'] = '2002-04-01'
        patient.billing_line_items = self.helper_visits([('2019-02-06', '99396')])
        tested = ClinicalQualityMeasure138v6p1(patient=patient, timeframe=timeframe)
        self.assertFalse(tested.in_initial_population())

        # patient is not 18 + patient had two visits --> false
        patient = self.load_patient('cms138v6')
        patient.patient['birthDate'] = '2002-04-01'
        patient.billing_line_items = self.helper_visits([
            ('2019-02-06', '99396'),
            ('2019-02-06', '99201'),
        ])
        tested = ClinicalQualityMeasure138v6p1(patient=patient, timeframe=timeframe)
        self.assertFalse(tested.in_initial_population())

    def test_in_initial_population_with_override(self):
        override = ProtocolOverrideRecordSet([{
            'protocolKey': 'ClinicalQualityMeasure138v6p1',
            'adjustment': {
                'reference': '2018-10-01T00:00:00Z',
                'cycleDays': 60
            },
            'snooze': None,
            'modified': '2018-03-15T12:32:54Z',
        }])  # yapf: disable

        # patient over 18 + patient had a preventive visit
        tests = {
            '2019-01-14': False,
            '2019-01-16': True,
            '2019-03-14': True,
            '2019-04-17': False,
        }
        for on_day, expected in tests.items():
            patient = self.load_patient('cms138v6')
            patient.protocol_overrides = override
            patient.billing_line_items = self.helper_visits([('2019-01-15', '99396')])
            tested = ClinicalQualityMeasure138v6p1(
                patient=patient, now=arrow.get(f'{on_day} 13:24:56'))
            if expected:
                self.assertTrue(tested.in_initial_population(), f'{on_day}')
            else:
                self.assertFalse(tested.in_initial_population(), f'{on_day}')

        # patient over 18 + patient had two visits
        tests = {
            '2019-01-14': False,
            '2019-01-16': True,
            '2019-03-14': True,
            '2019-03-16': False,
        }
        for on_day, expected in tests.items():
            patient = self.load_patient('cms138v6')
            patient.protocol_overrides = override
            patient.billing_line_items = self.helper_visits([
                ('2019-01-15', '96151'),
                ('2019-01-15', '99201'),
            ])
            tested = ClinicalQualityMeasure138v6p1(
                patient=patient, now=arrow.get(f'{on_day} 13:24:56'))
            if expected:
                self.assertTrue(tested.in_initial_population(), f'{on_day}')
            else:
                self.assertFalse(tested.in_initial_population(), f'{on_day}')

        # patient over 18 + patient had one visit --> false
        patient = self.load_patient('cms138v6')
        patient.protocol_overrides = override
        patient.billing_line_items = self.helper_visits([('2019-02-06', '96151')])
        tested = ClinicalQualityMeasure138v6p1(
            patient=patient, now=arrow.get('2019-02-26 13:24:56'))
        self.assertFalse(tested.in_initial_population())

        # patient is not 18 + patient had a preventive visit --> false
        patient = self.load_patient('cms138v6')
        patient.protocol_overrides = override
        patient.patient['birthDate'] = '2002-04-01'
        patient.billing_line_items = self.helper_visits([('2019-02-06', '99396')])
        tested = ClinicalQualityMeasure138v6p1(
            patient=patient, now=arrow.get('2019-02-26 13:24:56'))
        self.assertFalse(tested.in_initial_population())

        # patient is not 18 + patient had two visits --> false
        patient = self.load_patient('cms138v6')
        patient.protocol_overrides = override
        patient.patient['birthDate'] = '2002-04-01'
        patient.billing_line_items = self.helper_visits([
            ('2019-02-06', '99396'),
            ('2019-02-06', '99201'),
        ])
        tested = ClinicalQualityMeasure138v6p1(
            patient=patient, now=arrow.get('2019-02-26 13:24:56'))
        self.assertFalse(tested.in_initial_population())

    def test_in_denominator(self):
        start = arrow.get('2018-04-01 13:24:56')
        end = arrow.get('2019-04-01 13:24:56')
        timeframe = Timeframe(start=start, end=end)

        # patient over 18 + patient had a preventive visit + is a user
        patient = self.load_patient('cms138v6')
        patient.billing_line_items = self.helper_visits([('2018-10-09', '99396')])
        patient.interviews = self.helper_tobacco_screening('2019-02-05', '2018-11-23')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, timeframe=timeframe)
        self.assertTrue(tested.in_denominator())

        # patient over 18 + patient had a preventive visit + is NOT a user
        patient = self.load_patient('cms138v6')
        patient.billing_line_items = self.helper_visits([('2018-10-09', '99396')])
        patient.interviews = self.helper_tobacco_screening('2018-11-05', '2018-11-23')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, timeframe=timeframe)
        self.assertTrue(tested.in_denominator())

        # patient over 18 + patient had two visits + is a user
        patient = self.load_patient('cms138v6')
        patient.billing_line_items = self.helper_visits([
            ('2018-08-29', '96151'),
            ('2018-10-09', '99201'),
        ])
        patient.interviews = self.helper_tobacco_screening('2019-02-05', '2018-11-23')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, timeframe=timeframe)
        self.assertTrue(tested.in_denominator())

        # patient over 18 + patient had two visits + is NOT a user
        patient = self.load_patient('cms138v6')
        patient.billing_line_items = self.helper_visits([
            ('2018-08-29', '96151'),
            ('2018-10-09', '99201'),
        ])
        patient.interviews = self.helper_tobacco_screening('2018-11-05', '2018-11-23')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, timeframe=timeframe)
        self.assertTrue(tested.in_denominator())

        # patient is not 18 + patient had a preventive visit + is a user --> false
        patient = self.load_patient('cms138v6')
        patient.patient['birthDate'] = '2002-04-01'
        patient.billing_line_items = self.helper_visits([('2018-10-09', '99396')])
        patient.interviews = self.helper_tobacco_screening('2019-02-05', '2018-11-23')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, timeframe=timeframe)
        self.assertFalse(tested.in_denominator())

        # patient is not 18 + patient had two visits --> false
        patient = self.load_patient('cms138v6')
        patient.patient['birthDate'] = '2002-04-01'
        patient.billing_line_items = self.helper_visits([
            ('2018-08-29', '96151'),
            ('2018-10-09', '99201'),
        ])
        patient.interviews = self.helper_tobacco_screening('2019-02-05', '2018-11-23')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, timeframe=timeframe)
        self.assertFalse(tested.in_denominator())

    def test_in_denominator_with_override(self):
        override = ProtocolOverrideRecordSet([{
            'protocolKey': 'CMS138v6p1',
            'adjustment': {
                'reference': '2018-10-01T00:00:00Z',
                'cycleDays': 60
            },
            'snooze': None,
            'modified': '2018-03-15T12:32:54Z',
        }])  # yapf: disable

        # patient over 18 + patient had a preventive visit + is a user
        patient = self.load_patient('cms138v6')
        patient.protocol_overrides = override
        patient.billing_line_items = self.helper_visits([('2019-01-29', '99396')])
        patient.interviews = self.helper_tobacco_screening('2019-02-05', '2018-11-23')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, now=arrow.get('2019-03-17'))
        self.assertTrue(tested.in_denominator())

        # patient over 18 + patient had a preventive visit + is NOT a user
        patient = self.load_patient('cms138v6')
        patient.protocol_overrides = override
        patient.billing_line_items = self.helper_visits([('2019-01-29', '99396')])
        patient.interviews = self.helper_tobacco_screening('2018-11-23', '2019-02-05')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, now=arrow.get('2019-03-17'))
        self.assertTrue(tested.in_denominator())

        # patient over 18 + patient had two visits + is a user
        patient = self.load_patient('cms138v6')
        patient.protocol_overrides = override
        patient.billing_line_items = self.helper_visits([
            ('2019-01-29', '96151'),
            ('2019-02-09', '99201'),
        ])
        patient.interviews = self.helper_tobacco_screening('2019-02-05', '2018-11-23')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, now=arrow.get('2019-03-17'))
        self.assertTrue(tested.in_denominator())

        # patient over 18 + patient had two visits + is NOT a user
        patient = self.load_patient('cms138v6')
        patient.protocol_overrides = override
        patient.billing_line_items = self.helper_visits([
            ('2019-01-29', '96151'),
            ('2019-02-09', '99201'),
        ])
        patient.interviews = self.helper_tobacco_screening('2018-11-23', '2019-02-05')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, now=arrow.get('2019-03-17'))
        self.assertTrue(tested.in_denominator())

        # patient is not 18 + patient had a preventive visit + is a user --> false
        patient = self.load_patient('cms138v6')
        patient.protocol_overrides = override
        patient.patient['birthDate'] = '2002-04-01'
        patient.billing_line_items = self.helper_visits([('2019-01-29', '99396')])
        patient.interviews = self.helper_tobacco_screening('2019-02-05', '2018-11-23')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, now=arrow.get('2019-03-17'))
        self.assertFalse(tested.in_denominator())

        # patient is not 18 + patient had two visits --> false
        patient = self.load_patient('cms138v6')
        patient.protocol_overrides = override
        patient.patient['birthDate'] = '2002-04-01'
        patient.billing_line_items = self.helper_visits([
            ('2019-01-29', '96151'),
            ('2019-02-09', '99201'),
        ])
        patient.interviews = self.helper_tobacco_screening('2019-02-05', '2018-11-23')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, now=arrow.get('2019-03-17'))
        self.assertFalse(tested.in_denominator())

    def test_in_numerator(self):
        start = arrow.get('2018-04-01 13:24:56')
        end = arrow.get('2019-04-01 13:24:56')
        timeframe = Timeframe(start=start, end=end)

        # population #1
        # - patient over 18 + patient had a preventive visit + is a user
        patient = self.load_patient('cms138v6')
        patient.billing_line_items = self.helper_visits([('2018-10-09', '99396')])
        patient.interviews = self.helper_tobacco_screening('2019-02-05', '2018-11-23')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, timeframe=timeframe)
        tested.in_initial_population()
        self.assertTrue(tested.in_numerator())
        # - patient over 18 + patient had preventive visit + is NOT a user
        patient = self.load_patient('cms138v6')
        patient.billing_line_items = self.helper_visits([('2018-10-09', '99396')])
        patient.interviews = self.helper_tobacco_screening('2018-11-23', '2019-02-05')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, timeframe=timeframe)
        tested.in_initial_population()
        self.assertTrue(tested.in_numerator())
        # - patient over 18 + patient had NO preventive visit
        patient = self.load_patient('cms138v6')
        patient.billing_line_items = self.helper_visits([('2018-10-09', '99396')])
        tested = ClinicalQualityMeasure138v6p1(patient=patient, timeframe=timeframe)
        tested.in_initial_population()
        self.assertFalse(tested.in_numerator())

    def test_compute_results(self):
        # patient is under 18
        patient = self.load_patient('cms138v6')
        patient.patient['birthDate'] = '2002-04-01'
        patient.billing_line_items = self.helper_visits([
            ('2019-01-29', '96151'),
            ('2019-02-09', '99201'),
        ])
        patient.interviews = self.helper_tobacco_screening('2019-02-05', '2018-11-23')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, now=arrow.get('2019-03-17'))
        result = tested.compute_results()
        self.assertEqual('not_applicable', result.status)
        self.assertEqual(381, result.due_in)

        #  patient over 18 + patient had NO visit
        patient = self.load_patient('cms138v6')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, now=arrow.get('2019-03-17'))
        result = tested.compute_results()
        self.assertEqual('not_applicable', result.status)
        self.assertIsNone(result.due_in)

        #  patient over 18 + patient had preventive visit + is NOT a user
        patient = self.load_patient('cms138v6')
        patient.billing_line_items = self.helper_visits([('2018-10-09', '99396')])
        patient.interviews = self.helper_tobacco_screening('2018-11-23', '2019-02-05')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, now=arrow.get('2019-03-17'))
        result = tested.compute_results()
        self.assertEqual('satisfied', result.status)
        expected = 'Jenny had a Tobacco screening a month ago on 2/5/19 and is not a smoker.'
        self.assertEqual(expected, ''.join(result.narrative))
        self.assertEqual(325, result.due_in)

        #  patient over 18 + patient had preventive visit + is a user
        patient = self.load_patient('cms138v6')
        patient.billing_line_items = self.helper_visits([('2018-10-09', '99396')])
        patient.interviews = self.helper_tobacco_screening('2019-02-04', '2018-02-06')
        tested = ClinicalQualityMeasure138v6p1(patient=patient, now=arrow.get('2019-03-17'))
        result = tested.compute_results()
        self.assertEqual('satisfied', result.status)
        expected = 'Jenny had a Tobacco screening a month ago on 2/4/19 and is a smoker.'
        self.assertEqual(expected, ''.join(result.narrative))
        self.assertEqual(324, result.due_in)

        #  patient over 18 + patient had NO tobacco screening
        patient = self.load_patient('cms138v6')
        patient.billing_line_items = self.helper_visits([('2018-10-09', '99396')])
        tested = ClinicalQualityMeasure138v6p1(patient=patient, now=arrow.get('2019-03-30'))
        result = tested.compute_results()
        self.assertEqual('due', result.status)
        expected = 'Jenny should be screened for tobacco use.'
        self.assertEqual(expected, ''.join(result.narrative))
        self.assertEqual(-1, result.due_in)
        expected = [{
            'title': 'Complete tobacco use questionnaire',
            'command': {
                'type': 'interview',
            },
            'rank': 1,
            'key': 'CMS138v6p1_RECOMMEND_TOBACCO_USE_SCREENING',
            'button': 'Plan',
        }]
        self.helper_compare_recommendations(expected, result.recommendations)

    # helpers
    def helper_compare_recommendations(self, expected, result):
        self.assertEqual(len(expected), len(result))
        for exp, recommendation in zip(expected, result):
            self.assertEqual(exp['key'], recommendation.key)
            self.assertEqual(exp['rank'], recommendation.rank)
            self.assertEqual(exp['button'], recommendation.button)
            self.assertEqual(exp['title'], recommendation.title)
            self.assertEqual(exp['command']['type'], recommendation.command['type'])

    def helper_tobacco_screening(self, user_date, non_user_date) -> InterviewRecordSet:
        return InterviewRecordSet(
            [{
                'noteTimestamp': f'{user_date} 11:54:00+00:00',
                'results': [{
                    'codeSystem': 'http://loinc.org',
                    'code': '68535-4'
                }],
                'questionnaires': [{
                    'id': 30,
                    'code': '62541-8',
                    'codeSystem': 'http://loinc.org'
                }],
                'questions': [{
                    'questionResponseId': 5,
                    'code': '711013002',
                    'codeSystem': 'http://snomed.info/sct',
                    'questionnaireId': 30
                }],
                'responses': [{
                    'questionResponseId': 5,
                    'value': 'Current every day smoker',
                    'code': '449868002',
                    'codeSystem': 'http://snomed.info/sct'
                }]
            }, {
                'noteTimestamp': f'{non_user_date} 11:54:00+00:00',
                'results': [{
                    'codeSystem': 'http://loinc.org',
                    'code': '68535-4'
                }],
                'questionnaires': [{
                    'id': 30,
                    'code': '62541-8',
                    'codeSystem': 'http://loinc.org'
                }],
                'questions': [{
                    'questionResponseId': 5,
                    'code': '711013002',
                    'codeSystem': 'http://snomed.info/sct',
                    'questionnaireId': 30
                }],
                'responses': [{
                    'questionResponseId': 5,
                    'value': 'Current every day smoker',
                    'code': '105539002',
                    'codeSystem': 'http://snomed.info/sct'
                }]
            }]
        )  # yapf: disable

    def helper_visits(self, visits: List[Tuple[str, str]]) -> BillingLineItemRecordSet:
        return BillingLineItemRecordSet([{
            'created': f'{on_date} 11:54:00+00:00',
            'datetimeOfService': f'{on_date} 11:54:00+00:00',
            'cpt': code,
        } for on_date, code in visits])
