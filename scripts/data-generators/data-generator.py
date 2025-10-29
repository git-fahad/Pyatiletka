# Only generating data for heavy industry for now

import random
import math
from datetime import datetime, timedelta
from typing import List, Dict
import psycopg2
from psycopg2.extras import execute_batch

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'heavy_industry',
    'user': 'heavy_industry_user',
    'password': 'heavy_industry_pass'
}

# Plan years
PLAN_START = datetime(1986, 1, 1)
PLAN_END = datetime(1990, 12, 31)

# Quality grades with weights
QUALITY_GRADES = ['A', 'B', 'C']
QUALITY_WEIGHTS = [0.70, 0.25, 0.05]  # 70% A, 25% B, 5% C


class ProductionDataGenerator:
    """Generates realistic production data"""

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def get_facilities_and_products(self) -> List[Dict]:
        """Get facility-product combinations that need data"""
        query = """
            SELECT 
                f.facility_id,
                f.facility_name,
                f.capacity_per_day,
                f.workforce_size,
                p.product_id,
                p.product_name,
                p.product_category
            FROM facilities f
            CROSS JOIN products p
            WHERE 
                (f.facility_type = 'STEEL_MILL' AND p.product_category = 'STEEL')
                OR (f.facility_type = 'MACHINERY_FACTORY' AND p.product_category = 'MACHINERY')
                OR (f.facility_type = 'TANK_PLANT' AND p.product_category = 'ARMAMENTS')
            ORDER BY f.facility_id, p.product_id;
        """
        self.cursor.execute(query)
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def calculate_daily_production(self, base_capacity: float, date: datetime,
                                   facility_profile: str = 'average') -> Dict:
        """
        Calculate realistic daily production with various factors

        Factors considered:
        - Seasonal variation
        - Day of week (weekends reduced)
        - Year-over-year improvement
        - Random daily variance
        - Occasional breakdowns
        - Year-end push to meet quotas
        """

        day_of_year = date.timetuple().tm_yday
        year_progress = (date - PLAN_START).days / (PLAN_END - PLAN_START).days

        # 1. Seasonal factor (winter slightly lower production)
        seasonal_factor = 1.0 + 0.1 * math.sin(2 * math.pi * day_of_year / 365)

        # 2. Learning curve - improvement over time
        if facility_profile == 'high_performer':
            learning_factor = 0.90 + year_progress * 0.20  # 90% -> 110%
        elif facility_profile == 'struggling':
            learning_factor = 0.60 + year_progress * 0.25  # 60% -> 85%
        else:  # average
            learning_factor = 0.75 + year_progress * 0.20  # 75% -> 95%

        # 3. Day of week factor
        weekday = date.weekday()
        if weekday >= 5:  # Weekend
            weekend_factor = 0.50  # 50% capacity on weekends
        else:
            weekend_factor = 1.0

        # 4. Random daily variance (±10%)
        daily_variance = random.uniform(0.90, 1.10)

        # 5. Equipment breakdown (2% chance of major issue)
        breakdown = random.random() < 0.02
        breakdown_factor = 0.30 if breakdown else 1.0
        downtime_hours = random.uniform(12, 20) if breakdown else random.uniform(0, 2)

        # 6. Year-end push (December - pressure to meet annual quotas)
        month = date.month
        yearend_push = 1.15 if month == 12 else 1.0

        # 7. Holiday effect (major Soviet holidays - reduced production)
        holidays = [
            (1, 1),  # New Year
            (5, 1),  # International Workers' Day
            (5, 9),  # Victory Day
            (11, 7),  # October Revolution Day
        ]
        is_holiday = (date.month, date.day) in holidays
        holiday_factor = 0.40 if is_holiday else 1.0

        # Calculate final production
        actual_production = (
                base_capacity *
                seasonal_factor *
                learning_factor *
                weekend_factor *
                daily_variance *
                breakdown_factor *
                yearend_push *
                holiday_factor
        )

        # Calculate quality grade (worse during breakdowns or high push)
        if breakdown or yearend_push > 1.0:
            quality = random.choices(QUALITY_GRADES, weights=[0.50, 0.35, 0.15])[0]
        else:
            quality = random.choices(QUALITY_GRADES, weights=QUALITY_WEIGHTS)[0]

        # Defects (more during problems)
        base_defect_rate = 0.002  # 0.2% baseline
        if breakdown:
            defect_rate = 0.015
        elif yearend_push > 1.0:
            defect_rate = 0.008
        else:
            defect_rate = base_defect_rate

        defect_count = int(actual_production * defect_rate)

        return {
            'quantity': round(actual_production, 2),
            'quality_grade': quality,
            'downtime_hours': round(downtime_hours, 2),
            'defect_count': defect_count,
            'is_breakdown': breakdown
        }

    def generate_production_records(self, facility_product: Dict,
                                    start_date: datetime, end_date: datetime,
                                    facility_profile: str = 'average') -> List[tuple]:
        """Generate production records for a facility-product pair"""

        records = []
        current_date = start_date

        facility_id = facility_product['facility_id']
        product_id = facility_product['product_id']
        base_capacity = facility_product['capacity_per_day']
        workforce = facility_product['workforce_size']

        # Adjust base capacity based on product type
        if facility_product['product_category'] == 'STEEL':
            # Steel mills produce multiple products, divide capacity
            base_capacity = base_capacity * 0.3
        elif facility_product['product_category'] == 'MACHINERY':
            # Machinery is counted in units, not tons
            base_capacity = base_capacity * 1.0
        elif facility_product['product_category'] == 'ARMAMENTS':
            # Armaments (tanks) - lower daily production
            base_capacity = base_capacity * 1.0

        while current_date <= end_date:
            # Generate 3 shifts per day
            for shift in [1, 2, 3]:
                production = self.calculate_daily_production(
                    base_capacity / 3,  # Divide by 3 shifts
                    current_date,
                    facility_profile
                )

                # Worker distribution across shifts
                workers_on_shift = int(workforce / 3 * random.uniform(0.90, 1.10))

                # Reporter names (random)
                reporters = [
                    'V. Petrov', 'A. Ivanov', 'N. Sokolov', 'M. Volkov',
                    'D. Kuznetsov', 'S. Fedorov', 'I. Popov', 'O. Smirnov'
                ]

                record = (
                    facility_id,
                    product_id,
                    current_date,
                    production['quantity'],
                    production['quality_grade'],
                    shift,
                    workers_on_shift,
                    production['downtime_hours'],
                    production['defect_count'],
                    f"Daily production report - Shift {shift}",
                    random.choice(reporters),
                    current_date + timedelta(hours=8 * shift)  # reported_at
                )

                records.append(record)

            current_date += timedelta(days=1)

        return records

    def generate_targets(self, facility_product: Dict, year: int) -> List[tuple]:
        """Generate monthly targets for a facility-product pair for one year"""

        targets = []
        facility_id = facility_product['facility_id']
        product_id = facility_product['product_id']
        base_capacity = facility_product['capacity_per_day']

        # Adjust for product type
        if facility_product['product_category'] == 'STEEL':
            base_capacity = base_capacity * 0.3

        # Annual target is base_capacity * 365 * target_multiplier
        target_multiplier = 1.10  # Target is 110% of realistic capacity
        annual_target = base_capacity * 365 * target_multiplier

        for month in range(1, 13):
            # Days in month
            if month in [1, 3, 5, 7, 8, 10, 12]:
                days = 31
            elif month in [4, 6, 9, 11]:
                days = 30
            else:
                days = 29 if year % 4 == 0 else 28

            # Monthly target (proportional to days)
            monthly_target = (annual_target / 365) * days

            quarter = (month - 1) // 3 + 1

            target = (
                facility_id,
                product_id,
                year,
                quarter,
                month,
                round(monthly_target, 2),
                datetime(year - 1, 12, 1),  # Targets set in December of previous year
                f"5-Year Plan Target for {year}"
            )

            targets.append(target)

        return targets

    def insert_production_batch(self, records: List[tuple]):
        """Batch insert production records"""

        query = """
            INSERT INTO actual_production (
                facility_id, product_id, production_date, quantity_produced,
                quality_grade, shift_number, workers_on_shift, 
                equipment_downtime_hours, defect_count, notes, reported_by, reported_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """

        execute_batch(self.cursor, query, records, page_size=1000)
        self.conn.commit()
        print(f"Inserted {len(records)} production records")

    def insert_targets_batch(self, records: List[tuple]):
        """Batch insert target records"""

        query = """
            INSERT INTO production_targets (
                facility_id, product_id, plan_year, quarter, month,
                target_quantity, target_set_date, notes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (facility_id, product_id, plan_year, month) DO NOTHING;
        """

        execute_batch(self.cursor, query, records, page_size=100)
        self.conn.commit()
        print(f"Inserted {len(records)} target records")

    def generate_all_data(self, years: List[int] = [1986, 1987, 1988, 1989, 1990]):
        """Generate complete dataset for specified years"""

        print("=" * 60)
        print("GOSPLAN HEAVY INDUSTRY DATA GENERATION")
        print("=" * 60)

        # Get all facility-product combinations
        facility_products = self.get_facilities_and_products()
        print(f"\nFound {len(facility_products)} facility-product combinations")

        # Assign profiles to facilities (some perform better than others)
        profiles = ['high_performer', 'average', 'average', 'average', 'struggling']

        for year in years:
            print(f"\n{'=' * 60}")
            print(f"Generating data for year {year}")
            print(f"{'=' * 60}")

            # Generate targets for this year
            print(f"\nGenerating targets for {year}...")
            all_targets = []
            for fp in facility_products:
                targets = self.generate_targets(fp, year)
                all_targets.extend(targets)

            self.insert_targets_batch(all_targets)

            # Generate production data
            print(f"\nGenerating production data for {year}...")
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)

            for idx, fp in enumerate(facility_products):
                facility_name = fp['facility_name']
                product_name = fp['product_name']
                profile = random.choice(profiles)

                print(f"  [{idx + 1}/{len(facility_products)}] {facility_name} - {product_name} ({profile})")

                records = self.generate_production_records(
                    fp, start_date, end_date, profile
                )

                self.insert_production_batch(records)

        print("\n" + "=" * 60)
        print("DATA GENERATION COMPLETE!")
        print("=" * 60)

        # Show summary statistics
        self.show_statistics()

    def show_statistics(self):
        """Display summary statistics of generated data"""

        print("\n" + "=" * 60)
        print("DATABASE STATISTICS")
        print("=" * 60)

        queries = [
            ("Total Production Records", "SELECT COUNT(*) FROM actual_production"),
            ("Total Production Targets", "SELECT COUNT(*) FROM production_targets"),
            ("Date Range", "SELECT MIN(production_date), MAX(production_date) FROM actual_production"),
            ("Average Daily Production (Steel, tons)",
             """SELECT ROUND(AVG(quantity_produced), 2) 
                FROM actual_production ap 
                JOIN products p ON ap.product_id = p.product_id 
                WHERE p.product_category = 'STEEL'"""),
            ("Plan Completion Rate (%)",
             """SELECT ROUND(AVG(completion_percentage), 2) 
                FROM plan_vs_actual_monthly"""),
        ]

        for label, query in queries:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            print(f"\n{label}:")
            print(f"  {result}")


def main():
    """Main execution function"""

    print("Connecting to database...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✓ Connected successfully\n")

        generator = ProductionDataGenerator(conn)

        # Generate data for all 5 years
        # For testing, you might want to start with just 1986
        generator.generate_all_data(years=[1986])  # Start with just 1986

        # To generate all years, uncomment:
        # generator.generate_all_data(years=[1986, 1987, 1988, 1989, 1990])

        conn.close()
        print("\n✓ Database connection closed")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise


if __name__ == "__main__":
    main()