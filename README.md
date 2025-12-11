# ShortListResumes Project

## Overview
ShortListResumes is a Python-based application designed to assist in the process of shortlisting resumes. It utilizes a modular architecture with agents that handle specific tasks related to resume processing.

## Project Structure
```
ShortListResumes
├── src
│   ├── agents
│   │   ├── __init__.py
│   │   ├── feedback_agent.py
│   │   ├── filter_agent.py
│   │   ├── rate_agent.py
│   │   └── scoring_agent.py
│   ├── config
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── main.py
├── tests
│   ├── __init__.py
│   └── test_shortlister.py
├── requirements.txt
├── .env.example
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd ShortListResumes
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python src/main.py
```

## Testing
To run the tests, use:
```
pytest tests/
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.