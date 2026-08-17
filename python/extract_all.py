import subprocess
import sys


EXTRACTION_SCRIPTS = [
    "extract_Customers.py",
    "extract_Products.py",
    "extract_Sellers.py",
    "extract_Orders.py",
    "extract_Order_items.py",
    "extract_Payments.py",
    "extract_Shipments.py",
    "extract_Returns.py",
    "extract_Reviews.py",
    "extract_Warehouse.py"
]


def run_extraction():
    print("=" * 70)
    print("STARTING DATA EXTRACTION")
    print("=" * 70)

    for script in EXTRACTION_SCRIPTS:

        print(f"\nRunning: {script}")
        print("-" * 70)

        result = subprocess.run(
            [sys.executable, "-m", f"python.{script[:-3]}"],
            capture_output=False
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Extraction failed for {script}"
            )

        print(f"Completed: {script}")

    print("\n" + "=" * 70)
    print("ALL DATA EXTRACTION COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    run_extraction()