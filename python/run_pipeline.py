import subprocess
import sys
import os


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from config.logger import logger
from config.error_handler import run_step


def run_script(script_path):
    """
    Execute an existing Python ETL script.
    """

    result = subprocess.run(
        [sys.executable, script_path],
        cwd=PROJECT_ROOT
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Script failed: {script_path}"
        )

def reset_warehouse():
    """
    Clear existing Snowflake warehouse tables
    before loading fresh data.
    """

    reset_script = os.path.join(
        PROJECT_ROOT,
        "python",
        "reset_warehouse.py"
    )

    run_script(reset_script)


def main():

    logger.info("=" * 70)
    logger.info("RETAILPULSE ETL PIPELINE STARTED")
    logger.info("=" * 70)


    run_step(
        "DATA EXTRACTION",
        lambda: run_script(
            os.path.join(
                PROJECT_ROOT,
                "python",
                "extract_all.py"
            )
        )
    )


    run_step(
        "RESET SNOWFLAKE WAREHOUSE",
        reset_warehouse
    )


    dimension_scripts = [
        "load_dimensions.py",
        "load_product.py",
        "load_seller.py",
        "load_warehouse.py"
    ]

    for script in dimension_scripts:

        run_step(
            f"LOAD {script}",
            lambda script=script: run_script(
                os.path.join(
                    PROJECT_ROOT,
                    "python",
                    script
                )
            )
        )


    fact_scripts = [
        "load_fact_sales.py",
        "load_fact_payments.py",
        "load_fact_returns.py",
        "load_fact_reviews.py",
        "load_fact_shipments.py"
    ]

    for script in fact_scripts:

        run_step(
            f"LOAD {script}",
            lambda script=script: run_script(
                os.path.join(
                    PROJECT_ROOT,
                    "python",
                    script
                )
            )
        )


    logger.info("=" * 70)
    logger.info("RETAILPULSE ETL PIPELINE COMPLETED SUCCESSFULLY")
    logger.info("=" * 70)



if __name__ == "__main__":
    main()