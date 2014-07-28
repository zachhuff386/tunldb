tunldb: in-memory key value database
====================================

tunldb is an in-memory key value database developed for
`pritunl <http://pritunl.com>`_ with support for transactions,
publish/subscribe messaging paradigm and persisting to a file

Commands
--------

**set**
    **Time complexity: O(1)**

    Set the value of a key

    .. code-block:: python

        >> db.set('key', 'val')

**get**
    **Time complexity: O(1)**

    Get the value of a key

    .. code-block:: python

        >> db.get('key')
        'val'

**exists**
    **Time complexity: O(1)**

    Check if key exists

    .. code-block:: python

        >> db.exists('key')
        True

**rename**
    **Time complexity: O(1)**

    Rename a key

    .. code-block:: python

        >> db.rename('key', 'key2')

**remove**
    **Time complexity: O(1)**

    Remove a key

    .. code-block:: python

        >> db.remove('key')

**expire**
    **Time complexity: O(1)**

    Expire a key, removing it after duration of ttl has passed

    .. code-block:: python

        >> db.expire('key', 30)

**increment**
    **Time complexity: O(1)**

    Increment a key if key has no value key will be set to '1'

    .. code-block:: python

        >> db.increment('key')
        '1'

**decrement**
    **Time complexity: O(1)**

    Decrement a key if key has no value key will be set to '-1'

    .. code-block:: python

        >> db.decrement('key')
        '-1'

**keys**
    **Time complexity: O(n)**

    Return a set of all keys in database

    .. code-block:: python

        >> db.keys()
        {'key1', 'key2'}


**set_add**
    **Time complexity: O(1)**

    Add an element to a set

    .. code-block:: python

        >> db.set_add('key', 'val')

**set_remove**
    **Time complexity: O(1)**

    Remove an element from a set

    .. code-block:: python

        >> db.set_remove('key', 'val')

**set_pop**
    **Time complexity: O(1)**

    Get and remove an arbitrary element from a set

    .. code-block:: python

        >> db.set_pop('key')
        'val'

**set_exists**
    **Time complexity: O(1)**

    Check if an element exists in a set

    .. code-block:: python

        >> db.set_exists('key', 'val')
        True

**set_elements**
    **Time complexity: O(n)**

    Get all the elements in a set

    .. code-block:: python

        >> db.set_elements('key')
        {'val1', 'val2'}

**set_iter**
    **Time complexity: O(n)**

    Iterate all the elements in a set

    .. code-block:: python

        >> [x for x in test.set_iter('key')]
        ['val1', 'val2']

**set_length**
    **Time complexity: O(1)**

    Get the length of a set

    .. code-block:: python

        >> db.set_length('key')
        1

**list_lpush**
    **Time complexity: O(1)**

    Prepend an element to a list

    .. code-block:: python

        >> db.list_lpush('key', 'val')

**list_rpush**
    **Time complexity: O(1)**

    Append an element to a list

    .. code-block:: python

        >> db.list_rpush('key', 'val')

**list_lpop**
    **Time complexity: O(1)**

    Get and remove the first element in a list

    .. code-block:: python

        >> db.list_lpop('key')
        'val'

**list_rpop**
    **Time complexity: O(1)**

    Get and remove the last element in a list

    .. code-block:: python

        >> db.list_rpop('key')
        'val'

**list_index**
    **Time complexity: O(n)**

    Get the element at the givin index in a list

    .. code-block:: python

        >> db.list_index('key', 1)
        'val'

**list_elements**
    **Time complexity: O(n)**

    Get all the elements in a list

    .. code-block:: python

        >> db.list_elements('key')
        ['val1', 'val2']

**list_iter**
    **Time complexity: O(n)**

    Iterate all the elements in a list

    .. code-block:: python

        >> [x for x in test.list_iter('key')]
        ['val1', 'val2']

**list_iter_range**
    **Time complexity: O(n)**

    Iterate a range of elements in a list

    .. code-block:: python

        >> [x for x in test.list_iter_range('key', 1, 3)]
        ['val2', 'val3']

**list_remove**
    **Time complexity: O(n)**

    Remove the first occurrence of an element from a list, optionally
    remove the given number of occurrences from a list

    .. code-block:: python

        >> db.list_remove('key', 'val2', count=2)

**list_length**
    **Time complexity: O(1)**

    Get the length of a list

    .. code-block:: python

        >> db.list_length('key')
        1

**dict_set**
    **Time complexity: O(1)**

    Set the value of a dictionary field

    .. code-block:: python

        >> db.dict_set('key', 'field', 'val')

**dict_get**
    **Time complexity: O(1)**

    Get the value of a dictionary field

    .. code-block:: python

        >> db.dict_set('key', 'field')
        'val'

**dict_remove**
    **Time complexity: O(1)**

    Remove a field from a dictionary

    .. code-block:: python

        >> db.dict_remove('key', 'field')

**dict_keys**
    **Time complexity: O(1)**

    Get all the dictionary fields

    .. code-block:: python

        >> db.dict_keys('key')
        {'field1', 'field2'}

**dict_values**
    **Time complexity: O(n)**

    Get all the field values in a dictionary

    .. code-block:: python

        >> db.dict_values('key')
        {'val1', 'val2'}

**dict_iter**
    **Time complexity: O(n)**

    Iterate all the fields and values in a dictionary

    .. code-block:: python

        >> [x, y for x, y in test.dict_iter('key')]
        [('field1', 'val1'), ('field2', 'val2')]

**dict_get_all**
    **Time complexity: O(n)**

    Get all the fields and values in a dictoary

    .. code-block:: python

        >> db.dict_get_all('key')
        {'field1': 'val1', 'field2': 'val2'}

**subscribe**
    **Time complexity: O(1)**

    Subscribe and listen for messages on a channel, optionally provide a
    timeout to stop listening

    .. code-block:: python

        >> for msg in db.subscribe('key', timeout=5): print msg
        'msg'

**publish**
    **Time complexity: O(n)**

    Publish a message to all subscribers on a channel

    .. code-block:: python

        >> db.publish('key', 'msg')

**transaction**
    **Time complexity: O(1)**

    Begin an atomic database transaction

    .. code-block:: python

        >> tran = db.transaction()
        >> tran.set('key1', 'val1')
        >> tran.set('key2', 'val2')
        >> tran.commit()
        >> db.get('key1')
        'val1'

**persist**
    **Time complexity: O(1)**

    Persist the database to a file, optionally disable the auto save feature

    .. code-block:: python

        >> db.persist('/tmp/test.db', auto_export=False)

**export_data**
    **Time complexity: O(n)**

    Export database to the persist file

    .. code-block:: python

        >> db.persist('/tmp/test.db')
        >> db.set('key', 'val')
        >> db.export_data()
