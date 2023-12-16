import unittest
from data_processor.entity import Entity
from data_processor.entity import EntityCollection

class TestEntity(unittest.TestCase):
    """
    Test case for the Entity class.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up resources or initialize variables shared among all tests in this class
        """
        cls.shared_resource = "config.json"

    def setUp(self):
        """
        Set up resources or initialize variables specific to each test in this class
        """
        self.entity = Entity("1", {"field1": 10})

    def test_entity_creation(self):
        """ 
        Test to check whether the attributes of a new Entity instance match the expected values
        """
        self.assertEqual(self.entity.entity_id, "1")
        self.assertEqual(self.entity.field_value_pairs, {"field1": 10})

    def test_add_field(self):
        """
        Test to add key-value pairs to the attributes from an entity
        """
        self.entity.add("field1", 20)
        self.assertEqual(self.entity.field_value_pairs, {"field1": 20})

    def test_add_non_numeric_field(self):
        """
        Test to skip adding non-numeric values in a field
        """
        self.entity.add("field1", "abc")
        # After adding a non-numeric value, field_value_pairs should remain unchanged
        self.assertEqual(self.entity.field_value_pairs, {"field1": 10})

    def tearDown(self):
        """
        Clean up resources after each test in this class
        """
        del self.entity
        
    @classmethod
    def tearDownClass(cls):
        """
        Clean up resources after all tests in this class have run
        """
        del cls.shared_resource
        
class TestEntityCollection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up resources or initialize variables shared among all tests in this class
        """
        cls.entity1 = Entity("1", {"score": 10})
        cls.entity2 = Entity("2", {"score": 20})
        cls.entity3 = Entity("3", {"score": 30})
        cls.entity4 = Entity("3", {"score": 30})
        
    def setUp(self):
        """
        Set up resources or initialize variables specific to each test in this class
        """
        self.collection = EntityCollection(items=[self.entity1, self.entity2, self.entity3])
        self.single_value_collection = EntityCollection(items=[self.entity1])
        self.empty_collection = EntityCollection()
        
    def test_add_entity(self):
        """
        Test to check that an entity is added to the collection
        """
        entity = self.collection.add_entity("4")
        self.assertEqual(len(self.collection.items), 4)
        self.assertIs(self.collection.items[-1], entity)
        
    def test_compute_mean_and_median(self):
        """
        a)Test to check the average from a computable field within a collection is 3 cases:
            1. With a collection containing unique values
            2. With a collection containing only one value
            3. With an empty collection
        b)Test to check the median from a computable field within a collection is 3 cases:
            1. With a collection containing unique values
            2. With a collection containing only one value
            3. With an empty collection
        """
        self.assertEqual(self.collection.compute_mean("score"), 20.0)
        self.assertIsNone(self.empty_collection.compute_mean("score"))
        self.assertEqual(self.single_value_collection.compute_mean("score"), 10.0)
        self.assertEqual(self.collection.compute_median("score"), 20.0)
        self.assertIsNone(self.empty_collection.compute_median("score"))
        self.assertEqual(self.single_value_collection.compute_median("score"), 10.0)

    def test_compute_mode(self):
        """
        Test to check the mode from a computable field within a collection is 3 cases:
        1. With a collection containing unique values
        2. With a collection containing only one value
        3. With an empty collection
        """
        self.assertIsNone(self.collection.compute_mode("score"))
        self.assertIsNone(self.single_value_collection.compute_mode("score"))
        self.assertIsNone(self.empty_collection.compute_mode("score"))
        self.collection.items.append(self.entity4)
        self.assertEqual(self.collection.compute_mode("score"),30,"Test Failed")

    def test_compute_min_and_max(self):
        """
        a)Test to check the min from a computable field within a collection is 3 cases:
            1. With a collection containing unique values
            2. With a collection containing only one value
            3. With an empty collection
        b) Test to check the max from a computable field within a collection is 3 cases:
            1. With a collection containing unique values
            2. With a collection containing only one value
            3. With an empty collection
        """
        self.assertEqual(self.collection.compute_min("score"), 10)
        self.assertIsNone(self.empty_collection.compute_min("score"))
        self.assertEqual(self.single_value_collection.compute_min("score"), 10)
        self.assertEqual(self.collection.compute_max("score"), 30)
        self.assertIsNone(self.empty_collection.compute_max("score"))
        self.assertEqual(self.single_value_collection.compute_max("score"), 10)


    def test_compute_count(self):
        """
        Test to check the count from a computable field within a collection is 3 cases:
        1. With a collection containing unique values
        2. With a collection containing only one value
        3. With an empty collection
        """
        self.assertEqual(self.collection.compute_count("score"), 3)
        self.assertIsNone(self.empty_collection.compute_count("score"))
        self.assertEqual(self.single_value_collection.compute_count("score"), 1)

        
    def tearDown(self):
        """
        Clean up resources after each test in this class
        """
        del self.collection

    @classmethod
    def tearDownClass(cls):
        """
        Clean up resources after all tests in this class have run
        """
        del cls.entity1
        del cls.entity2
        del cls.entity3
