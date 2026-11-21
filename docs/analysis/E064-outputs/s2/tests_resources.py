"""New monitor predicate boundary only; stdlib, no model/data imports."""
import unittest
from release import resource_success

class ResourceBoundaryTests(unittest.TestCase):
    def test_final_sample_and_existing_failures(self):
        cap=8*1024**3
        self.assertTrue(resource_success(0,'COMPLETE',1,60,0,{'rss':cap-1,'commitment':cap-1}))
        self.assertFalse(resource_success(0,'COMPLETE',1,60,0,{'rss':cap,'commitment':1}))
        self.assertFalse(resource_success(0,'COMPLETE',1,60,0,{'rss':1,'commitment':cap+1}))
        self.assertFalse(resource_success(1,'COMPLETE',1,60,0,{'rss':1,'commitment':1}))
        self.assertFalse(resource_success(0,'MEMORY_CAP',1,60,0,{'rss':1,'commitment':1}))
        self.assertFalse(resource_success(0,'COMPLETE',61,60,0,{'rss':1,'commitment':1}))
        self.assertFalse(resource_success(0,'COMPLETE',1,60,3600,{'rss':1,'commitment':1}))

if __name__=='__main__': unittest.main()
