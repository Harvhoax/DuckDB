# Central Mart — DuckDB Retail Analytics

A simple retail batch-processing mini project with a local web dashboard.
Generate synthetic store orders, convert CSV to compressed Parquet, and compare
SQL query performance with one and four CPU workers. No Spark, Hadoop, database
server, frontend build, or external dataset is needed.

## Quick start

Install **Python 3.10 or newer** (3.12 or 3.13 recommended) and Git, or download
this repository using GitHub's **Code → Download ZIP** and extract it first.

```sh
git clone https://github.com/Harvhoax/DuckDB.git
cd DuckDB
```

**Windows:** double-click `start.bat`, or run:

```powershell
python run.py
```

If Windows recognizes `py` instead of `python`, use `py -3 run.py`.

**macOS / Linux:**

```sh
python3 run.py
```

The launcher creates `.venv`, installs the pinned DuckDB dependency, starts the
server, and opens your browser at **http://127.0.0.1:8000**. Internet is needed
for the first installation. Later runs reuse that environment. Choose an order
count and click **Run demo batch** to generate data and populate the dashboard.
Stop the server with **Ctrl+C** in the terminal.

The project works on Windows, macOS, and Linux where a compatible Python/DuckDB
installation is available. It is intended for a normal laptop or desktop, not
mobile devices or a hosted public server. GitHub hosts the source; run Python
locally to use the dashboard.

## Dashboard

- Net sales, completed orders, return rate, and storage savings.
- Store sales comparison, five best-selling products, and monthly sales.
- Actual CSV vs. Parquet query timings using one and four worker threads.
- Downloadable CSV reports and raw benchmark results.
- A visual explanation of the processing pipeline.
- Run 10,000, 100,000, or 1,000,000 synthetic orders from the page.

## Business scenario

A fictional retail chain, Central Mart, wants to compare its Delhi, Mumbai,
Bengaluru, and Pune branches using an order export and a six-product catalog.
The batch joins orders to reference tables, applies discounts, excludes cancelled
and fully returned orders from sales, and produces a manager summary.

`Generate CSV → Convert to Parquet → Join & filter → Parallel aggregation → Reports`

One row is a single-product order, quantity 1–5. Dates span calendar year 2025.
All names, prices, and transactions are synthetic. Roughly 5% of orders are
cancelled and 7% returned; proportions vary. Deterministic hashes mix products,
stores, statuses, quantities, and discounts. The pinned DuckDB version helps
keep generated examples consistent.

Net sales = quantity × unit price less discount, rounded per order to paise.
Cancelled orders generate no revenue and returned orders are fully refunded.
Monthly sales use original order date and final status. Taxes, delivery fees,
partial refunds, inventory, costs, and demand forecasting are omitted. This is
an operational sales report, not an accounting ledger.

## Generated files

Nothing large is committed. Files are generated locally when a batch runs.

| Location | Contents |
| --- | --- |
| `data/sales.csv` | Synthetic order export |
| `data/stores.csv`, `data/products.csv` | Generated store and product reference data |
| `data/sales.parquet` | Zstandard-compressed columnar orders |
| `results/manager_summary.md` | Readable business summary |
| `results/store_performance.csv` | Completed orders, units, and net sales by branch |
| `results/monthly_revenue.csv` | Monthly net sales |
| `results/top_products.csv` | Top five products by net sales |
| `results/order_status.csv` | Counts and potential discounted order value by final status |
| `results/benchmark.json` | Measured timings, configuration, validation, and file sizes |
| `results/query_plan.txt` | Actual DuckDB execution plan |

CSV monetary columns use **paise**; divide by 100 for INR. The UI shows INR,
rounded to whole rupees for readability. Order-status values for returned or
cancelled orders are potential order values, not recognized sales.

Each batch replaces generated data and results. Avoid running the command-line
pipeline separately while a dashboard batch is active. Edit main.py to change
catalog prices or generation rules; editing generated reference CSVs does not
change the next run.

## Command-line processing

After the launcher has installed dependencies, run directly using its environment:

```powershell
# Windows
.venv\Scripts\python main.py --rows 100000 --threads 4 --repeats 3
```

```sh
# macOS / Linux
.venv/bin/python main.py --rows 100000 --threads 4 --repeats 3
```

Default: one million orders. Larger experiments can use `--rows 10000000`;
increase scale gradually according to available disk and RAM.

## What this demonstrates

DuckDB uses CPU workers on **one machine** for parallel scans and eligible
aggregations, combining partial results. Queries run sequentially; each query
can use multiple threads. This demonstrates distributed-style processing ideas,
but does not create a distributed cluster.

Parquet allows reading needed columns, filter pushdown, and row-group skipping
when the layout permits it. The benchmark warms queries and reports the median
of three execution/fetch timings. It is not a cold-disk benchmark. More threads
or Parquet do not guarantee faster execution, especially for small inputs.
Simple synthetic distributions also affect compression. The 1 GB DuckDB memory
budget is not a strict cap on total process RAM.

## Troubleshooting

- **Python not found:** install Python, enable PATH on Windows, and reopen the terminal.
- **Port 8000 occupied:** run `python run.py --port 8001` (use `python3` on macOS/Linux).
- **Browser did not open:** visit the printed local URL manually. For remote/headless
  terminals, pass `--no-browser`; the server still binds only to local loopback.
- **Linux venv/ensurepip missing:** install your distribution's `python3-venv` package.
- **Moved the folder or changed Python:** remove only this project's `.venv` folder,
  then rerun the launcher. Virtual environments are machine-specific and not committed.
- **Install failed:** check internet access and use a Python version supported by
  the pinned DuckDB package. Python 3.12 or 3.13 is recommended.

To install without starting the UI: `python run.py --setup-only`.
You can also install manually: `python -m pip install -r requirements.txt`, then
`python dashboard.py`. The shell helper `sh start.sh` is available on macOS/Linux.

## Verification

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

The smoke test uses a temporary checkout (including a path with spaces), starts
an empty dashboard, runs an actual batch through its API, checks report downloads,
independently recalculates sales from raw CSV, and rejects invalid inputs.
GitHub Actions is configured to run it on Windows, macOS, and Linux with Python
3.10 and 3.13. Check the repository's Actions tab for those results.

## Five-minute demonstration

1. Launch the dashboard and run 100,000 orders.
2. Explain store sales, returns, and best-selling products.
3. Compare file sizes and thread timings.
4. Walk through the four pipeline steps at the bottom.
5. Explain why this is local CPU parallelism rather than a cluster.

References: [DuckDB Python API](https://duckdb.org/docs/current/clients/python/overview),
[COPY](https://duckdb.org/docs/current/sql/statements/copy),
[performance tuning](https://duckdb.org/docs/current/guides/performance/how_to_tune_workloads).
