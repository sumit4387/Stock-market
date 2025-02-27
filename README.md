
## Run the project

Commands are tested on macbook with Python 3.10.6.

Create a virtual environment (if you want):

```shell
cd Stock-market
python -m venv venv
source venv/bin/activate

```

Run tests:

To run tests from the command line use `python -m unittest -v <path to test file>`. For example, the integration test
story can be run with `python -m unittest -v tests/test_story1.py`.

## Assumptions made:

- Fixed dividends only occur in stocks with type preferred.
- The formula to calculate the P/E Ratio is unclear regarding the `Dividend` variable. This project
  uses `Last Dividend`.
- All calculations are rounded to 5 digits.
- One stock can only exist once.
- If a database exist, stocks and trades would have a one-to-many relationship. The table trade would include stock ids
  as foreign keys. 