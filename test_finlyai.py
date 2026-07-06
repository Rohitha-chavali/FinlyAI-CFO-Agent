import os
import shutil
import unittest
from inventory import run_inventory_tracker, LowStockAlert
from billing import DraftPurchaseOrder, generate_po_pdf, draft_reorder_email_dry_run

class TestFinlyAI(unittest.TestCase):
    
    def setUp(self):
        # Create a temp directory for PO outputs during tests
        self.test_output_dir = "test_output_pos"
        if not os.path.exists(self.test_output_dir):
            os.makedirs(self.test_output_dir)

    def tearDown(self):
        # Clean up generated test output directory
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)

    def test_inventory_threshold_logic(self):
        # Sample inventory where some are under threshold and some are not
        test_inventory = [
            # Under threshold: 8 on hand vs 20 threshold
            {"sku": "SKU-1001", "name": "Espresso Beans", "on_hand": 8, "safety_threshold": 20, "reorder_qty": 100, "unit_cost": 9.50, "vendor": "Highlands Roasters"},
            # OK: 42 on hand vs 30 threshold
            {"sku": "SKU-1002", "name": "Oat Milk Cartons", "on_hand": 42, "safety_threshold": 30, "reorder_qty": 60, "unit_cost": 2.10, "vendor": "GreenFarm Dairy Co."},
            # Under threshold: 150 on hand vs 500 threshold
            {"sku": "SKU-1003", "name": "12oz Paper Cups", "on_hand": 150, "safety_threshold": 500, "reorder_qty": 2000, "unit_cost": 0.06, "vendor": "PackRight Supplies"},
        ]
        
        alerts = run_inventory_tracker(test_inventory)
        
        # We expect exactly 2 low stock alerts (SKU-1001 and SKU-1003)
        self.assertEqual(len(alerts), 2)
        
        # Verify first alert fields
        alert1 = alerts[0]
        self.assertEqual(alert1.sku, "SKU-1001")
        self.assertEqual(alert1.on_hand, 8)
        self.assertEqual(alert1.est_reorder_cost, 950.0)
        
        # Verify second alert fields
        alert2 = alerts[1]
        self.assertEqual(alert2.sku, "SKU-1003")
        self.assertEqual(alert2.on_hand, 150)
        self.assertEqual(alert2.est_reorder_cost, 120.0)

    def test_po_pdf_generation(self):
        po = DraftPurchaseOrder(
            po_id="PO-TEST-999",
            vendor="Test Vendor",
            sku="SKU-TEST",
            name="Test Coffee Beans",
            qty=50,
            unit_cost=10.0,
            total_cost=500.0
        )
        
        file_path = generate_po_pdf(po, output_dir=self.test_output_dir)
        
        # Verify that the PDF PO was generated successfully
        self.assertTrue(os.path.exists(file_path))
        self.assertEqual(file_path, os.path.join(self.test_output_dir, "PO-TEST-999.pdf"))
        self.assertGreater(os.path.getsize(file_path), 0)

    def test_dry_run_email_generation(self):
        po = DraftPurchaseOrder(
            po_id="PO-TEST-777",
            vendor="Test Vendor Co.",
            sku="SKU-TEST-777",
            name="Paper Filters",
            qty=100,
            unit_cost=1.5,
            total_cost=150.0
        )
        
        email_content = draft_reorder_email_dry_run(po)
        
        # Check that essential fields are in the email content
        self.assertIn("PO-TEST-777", email_content)
        self.assertIn("Test Vendor Co.", email_content)
        self.assertIn("SKU-TEST-777", email_content)
        self.assertIn("Paper Filters", email_content)
        self.assertIn("$150.00", email_content)
        self.assertIn("sales@testvendorco.com", email_content)


if __name__ == "__main__":
    unittest.main()
