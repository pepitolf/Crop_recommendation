from django.test import TestCase
from .models import User, Crop, Knowledge, KnowledgeRule, KnowledgeFuzzyValue

class ModelsTestCase(TestCase):
    def setUp(self):
        self.crop = Crop.objects.create(name="Rice", description="Rice crop")
        self.knowledge = Knowledge.objects.create(name="NPK Value", description="NPK value required for crops")
        self.knowledge_rule = KnowledgeRule.objects.create(crop=self.crop, knowledge=self.knowledge, value=5.5)
        self.knowledge_fuzzy_value = KnowledgeFuzzyValue.objects.create(knowledge_rule=self.knowledge_rule, fuzzy_set_type="High", fuzzy_value=0.8)

    def test_crop_creation(self):
        self.assertEqual(self.crop.name, "Rice")
        self.assertEqual(self.crop.description, "Rice crop")

    def test_knowledge_creation(self):
        self.assertEqual(self.knowledge.name, "NPK Value")
        self.assertEqual(self.knowledge.description, "NPK value required for crops")

    def test_knowledge_rule_creation(self):
        self.assertEqual(self.knowledge_rule.crop, self.crop)
        self.assertEqual(self.knowledge_rule.knowledge, self.knowledge)
        self.assertEqual(self.knowledge_rule.value, 5.5)

    def test_knowledge_fuzzy_value_creation(self):
        self.assertEqual(self.knowledge_fuzzy_value.knowledge_rule, self.knowledge_rule)
        self.assertEqual(self.knowledge_fuzzy_value.fuzzy_set_type, "High")
        self.assertEqual(self.knowledge_fuzzy_value.fuzzy_value, 0.8)