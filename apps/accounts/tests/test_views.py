'''
from django.test import TestCase
from django.urls import reverse
from ..models import Test
# Create your tests here.


class TestSetUP(TestCase):
    view = None

    def setUp(self):
        # create Test objects
        for i in range(20):
            test = Test.objects.create(desc='desc ' + str(i))
            test.save()


class TestListTest(TestSetUP):
    view = 'test_list'

    def test_get_tests(self):
        url = reverse(self.view)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_post_test(self):
        url = reverse(self.view)

        res = self.client.post(
            url,
            data={
                'desc': 'test description'
            },
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)


class TestDetailTest(TestSetUP):
    view = 'test_detail'

    def test_get_test(self):
        url = reverse(self.view, kwargs={'pk': 1})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_get_nonexistent_test(self):
        url = reverse(self.view, kwargs={'pk': 8888899})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)

    def test_put_test(self):
        url = reverse(self.view, kwargs={'pk': 1})
        res = self.client.put(
            url,
            data={
                'desc': 'new description'
            },
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)

    def test_delete_test(self):
        url = reverse(self.view, kwargs={'pk': 1})
        res = self.client.delete(
            url
        )
        self.assertEqual(res.status_code, 204)
'''
