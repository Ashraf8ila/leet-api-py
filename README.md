# LeetCode CLI Tool

This is a command-line interface (CLI) tool to fetch LeetCode user statistics and daily coding challenge questions.

## Features

- Fetch LeetCode user statistics
- Fetch daily coding challenge questions for a given timeframe

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ashraf8ila/leet-api-py.git
    cd leet-api-py
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Fetch User Info

To fetch LeetCode user statistics, use the `user-info` command with the `--username` argument:
```sh
python main.py user-info --username <your-username>
```

### Fetch Daily Questions

To fetch daily coding challenge questions for a given timeframe, use the `daily-questions` command with the `--start` and `--end` arguments:
```sh
python main.py daily-questions --start YYYY-MM-DD --end YYYY-MM-DD
```

## Example

```sh
python main.py user-info --username johndoe
python main.py daily-questions --start 2023-01-01 --end 2023-01-31
```

## License

This project is licensed under the MIT License.
