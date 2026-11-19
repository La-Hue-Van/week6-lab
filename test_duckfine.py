import unittest

from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):

    def setUp(self):
        self.fine = DuckFine("M001")

    def test_charge_returns_a_fee_for_a_late_duck(self):
        self.assertEqual(self.fine.charge(5), 1.50)

    def test_deluxe_duck_costs_more(self):
        self.assertTrue(self.fine.charge(5, deluxe=True) > 0)

    def test_no_fee_when_returned_on_time(self):
        self.assertEqual(self.fine.charge(0), 0.0)

    def test_negative_days_raises(self):
        with self.assertRaises(ValueError):
            self.fine.charge(-1)

    # --- Added after mutation testing: one per surviving mutant, values from the brief ---

    def test_fine_is_capped_at_five_dollars(self):
        # 20 days late: 18 chargeable x $0.50 = $9.00, but a single fine never exceeds $5
        self.assertAlmostEqual(self.fine.charge(20), 5.00)

    def test_running_total_accumulates_across_fines(self):
        # Fines accumulate: $1.50 (5 days) + $1.00 (4 days) = $2.50
        self.fine.charge(5)
        self.fine.charge(4)
        self.assertAlmostEqual(self.fine.total_owed, 2.50)

    def test_deluxe_fee_is_exactly_double(self):
        # 5 days late: 3 chargeable x $0.50 = $1.50, doubled for Deluxe = $3.00
        self.assertAlmostEqual(self.fine.charge(5, deluxe=True), 3.00)


if __name__ == "__main__":
    unittest.main()