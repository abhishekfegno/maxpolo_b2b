from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, APITestCase

from apps.executivetracking.models import CheckInDay
from apps.user.models import Executive


class ExecutiveCheckInFlow(APITestCase):
    fixtures = ['test_executive_inflow.json', ]
    databases = 'testdb'
    def test_create_checkin(self):
        url = reverse('executive-tracking-api:check-in-day-create-api')
        data = {
            'location': {"type": "Point", "coordinates": [8492242.807019850239158, 1120189.920763866277412]},
            'location_text': '1st floor, Confident Antlia Gold Commercial, Elamakkara, Kaloor, Ernakulam, Elamakkara, Kochi, Kerala 682026, India',
            'device_name': 'Redmi Note 9 Pro',
            'device_id': '6c96191c0ae9bbf7',
            'battery_percentage': 98,
            'executive': 2,
            'check_in_at': '2021-03-25T10:52:49+05:30'
        }
        initial_count = CheckInDay.objects.all().count()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CheckInDay.objects.all().count(), initial_count + 1)
        self.assertEqual(response.data['device_id'], '6c96191c0ae9bbf7')






