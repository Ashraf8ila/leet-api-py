# LeetCode CLI Tool

This tool allows you to fetch LeetCode user information and daily coding challenge questions using a command-line interface (CLI) or a web-based frontend.

## Features

- Fetch LeetCode user stats
- Fetch daily coding challenge questions for a given timeframe

## Requirements

- Python 3.x
- Flask
- Requests

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/ashraf8ila/leet-api-py.git
    cd leet-api-py
    ```

2. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Command-Line Interface (CLI)

To use the CLI, run the `main.py` script with the appropriate arguments:

- Fetch user info:

    ```sh
    python main.py user-info --username <LeetCodeUsername>
    ```

- Fetch daily questions:

    ```sh
    python main.py daily-questions --start <StartDate> --end <EndDate>
    ```

### Web Application

To use the web-based frontend, run the `app.py` script:

```sh
python app.py
```

Then, open your web browser and navigate to `http://127.0.0.1:5000`.

## License

This project is licensed under the MIT License.
