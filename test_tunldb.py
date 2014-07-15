import unittest
import tunldb
import time
import itertools
import threading
import os

PERSIST_PATH = 'test.db'

class TestTunlDB(unittest.TestCase):
    def setUp(self):
        self.db = tunldb.TunlDB()

    def test_set(self):
        self.db.set('key', 'val')
        self.assertEqual(self.db.get('key'), 'val')
        self.db.remove('key')

    def test_get(self):
        self.db.set('key', 'val')
        self.assertEqual(self.db.get('key'), 'val')
        self.db.remove('key')

    def test_remove(self):
        self.db.set('key', 'val')
        self.assertEqual(self.db.get('key'), 'val')
        self.db.remove('key')
        self.assertIsNone(self.db.get('key'))

    def test_exists(self):
        self.assertFalse(self.db.exists('key'))
        self.db.set('key', 'val')
        self.assertTrue(self.db.exists('key'))
        self.db.remove('key')

    def test_rename(self):
        self.db.set('key', 'val')
        self.assertEqual(self.db.get('key'), 'val')
        self.db.rename('key', 'key2')
        self.assertIsNone(self.db.get('key'))
        self.assertEqual(self.db.get('key2'), 'val')

    def test_expire(self):
        self.db.expire('key', 1)
        self.db.set('key', 'val')
        self.assertEqual(self.db.get('key'), 'val')
        time.sleep(1.0001)
        self.assertIsNone(self.db.get('key'))

    def test_increment(self):
        self.db.increment('key')
        self.assertEqual(self.db.get('key'), '1')
        self.db.increment('key')
        self.assertEqual(self.db.get('key'), '2')
        self.db.remove('key')

    def test_decrement(self):
        self.db.decrement('key')
        self.assertEqual(self.db.get('key'), '-1')
        self.db.decrement('key')
        self.assertEqual(self.db.get('key'), '-2')
        self.db.remove('key')

    def test_keys(self):
        self.db.set('key1', 'val1')
        self.db.set('key2', 'val2')
        self.assertEqual(self.db.keys(), {'key1', 'key2'})
        self.db.remove('key1')
        self.db.remove('key2')

    def test_set_add(self):
        self.db.set_add('key', 'val')
        self.assertEqual(self.db.set_elements('key'), {'val'})
        self.db.remove('key')

    def test_set_remove(self):
        self.db.set_add('key', 'val')
        self.assertEqual(self.db.set_elements('key'), {'val'})
        self.db.set_remove('key', 'val')
        self.assertEqual(self.db.set_elements('key'), set())
        self.db.remove('key')

    def test_set_exists(self):
        self.db.set_add('key', 'val')
        self.assertTrue(self.db.set_exists('key', 'val'))
        self.db.set_remove('key', 'val')
        self.assertFalse(self.db.set_exists('key', 'val'))
        self.db.remove('key')

    def test_set_elements(self):
        self.db.set_add('key', 'val1')
        self.db.set_add('key', 'val2')
        self.assertEqual(self.db.set_elements('key'), {'val1', 'val2'})
        self.db.remove('key')

    def test_set_length(self):
        self.db.set_add('key', 'val')
        self.assertEqual(self.db.set_length('key'), 1)
        self.db.set_remove('key', 'val')
        self.assertEqual(self.db.set_length('key'), 0)
        self.db.remove('key')

    def test_list_lpush(self):
        self.db.list_lpush('key', 'val1')
        self.db.list_lpush('key', 'val2')
        self.assertEqual(self.db.list_elements('key'), ['val2', 'val1'])
        self.db.remove('key')

    def test_list_rpush(self):
        self.db.list_rpush('key', 'val1')
        self.db.list_rpush('key', 'val2')
        self.assertEqual(self.db.list_elements('key'), ['val1', 'val2'])
        self.db.remove('key')

    def test_list_lpop(self):
        self.db.list_rpush('key', 'val1')
        self.db.list_rpush('key', 'val2')
        self.assertEqual(self.db.list_lpop('key'), 'val1')
        self.assertEqual(self.db.list_elements('key'), ['val2'])
        self.db.remove('key')

    def test_list_rpop(self):
        self.db.list_rpush('key', 'val1')
        self.db.list_rpush('key', 'val2')
        self.assertEqual(self.db.list_rpop('key'), 'val2')
        self.assertEqual(self.db.list_elements('key'), ['val1'])
        self.db.remove('key')

    def test_list_index(self):
        self.db.list_rpush('key', 'val1')
        self.db.list_rpush('key', 'val2')
        self.assertEqual(self.db.list_index('key', 0), 'val1')
        self.assertEqual(self.db.list_index('key', 1), 'val2')
        self.db.remove('key')

    def test_list_elements(self):
        self.db.list_rpush('key', 'val1')
        self.db.list_rpush('key', 'val2')
        self.assertEqual(self.db.list_elements('key'), ['val1', 'val2'])
        self.db.remove('key')

    def test_list_iter(self):
        self.db.list_rpush('key', 'val1')
        self.db.list_rpush('key', 'val2')
        self.assertTrue(all([x == y for x, y in itertools.izip(
            ['val1', 'val2'], self.db.list_iter('key'))]))
        self.db.remove('key')

    def test_list_iter_range(self):
        self.db.list_rpush('key', 'val1')
        self.db.list_rpush('key', 'val2')
        self.db.list_rpush('key', 'val3')
        self.assertTrue(all([x == y for x, y in itertools.izip(
            ['val2', 'val3'], self.db.list_iter_range('key', 1, 2))]))
        self.db.remove('key')

    def test_list_remove(self):
        self.db.list_rpush('key', 'val1')
        self.db.list_rpush('key', 'val2')
        self.db.list_remove('key', 'val2')
        self.assertEqual(self.db.list_elements('key'), ['val1'])
        self.db.remove('key')

    def test_list_length(self):
        self.db.list_rpush('key', 'val1')
        self.db.list_rpush('key', 'val2')
        self.assertEqual(self.db.list_length('key'), 2)
        self.db.remove('key')

    def test_dict_set(self):
        self.db.dict_set('key', 'field', 'val')
        self.assertEqual(self.db.dict_get_all('key'), {'field': 'val'})
        self.db.remove('key')

    def test_dict_get(self):
        self.db.dict_set('key', 'field', 'val')
        self.assertEqual(self.db.dict_get('key', 'field'), 'val')
        self.db.remove('key')

    def test_dict_remove(self):
        self.db.dict_set('key', 'field', 'val')
        self.db.dict_remove('key', 'field')
        self.assertEqual(self.db.dict_get_all('key'), {})
        self.db.remove('key')

    def test_dict_keys(self):
        self.db.dict_set('key', 'field1', 'val1')
        self.db.dict_set('key', 'field2', 'val2')
        self.assertEqual(self.db.dict_keys('key'), {'field1', 'field2'})
        self.db.remove('key')

    def test_dict_values(self):
        self.db.dict_set('key', 'field1', 'val1')
        self.db.dict_set('key', 'field2', 'val2')
        self.assertEqual(self.db.dict_values('key'), {'val1', 'val2'})
        self.db.remove('key')

    def test_dict_get_all(self):
        self.db.dict_set('key', 'field1', 'val1')
        self.db.dict_set('key', 'field2', 'val2')
        self.assertEqual(self.db.dict_get_all('key'),
            {'field1': 'val1', 'field2': 'val2'})
        self.db.remove('key')

    def test_publish_subscribe(self):
        recv = threading.Event()
        def listen():
            for msg in self.db.subscribe('key'):
                if msg == 'val':
                    recv.set()
                break
        listen_thread = threading.Thread(target=listen)
        listen_thread.daemon = True
        listen_thread.start()
        self.db.publish('key', 'val')
        self.assertTrue(recv.wait(1))

    def test_transaction(self):
        tran = self.db.transaction()
        tran.set('key1', 'val1')
        tran.set('key2', 'val2')
        self.assertIsNone(self.db.get('key1'))
        self.assertIsNone(self.db.get('key2'))
        tran.commit()
        self.assertEqual(self.db.get('key1'), 'val1')
        self.assertEqual(self.db.get('key2'), 'val2')
        self.db.remove('key1')
        self.db.remove('key2')

    def test_persist(self):
        persist_db = tunldb.TunlDB()
        persist_db.persist(PERSIST_PATH, False)
        persist_db.set('key', 'val')
        persist_db.export_data()
        persist_db = tunldb.TunlDB()
        persist_db.persist(PERSIST_PATH, False)
        self.assertEqual(persist_db.get('key'), 'val')
        os.remove(PERSIST_PATH)

if __name__ == '__main__':
    unittest.main()
