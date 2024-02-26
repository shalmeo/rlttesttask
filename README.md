# RLT Test Task

This project is a Python application that aggregates salary data from a MongoDB database. It groups the data by different time intervals (hour, day, month) and calculates the total salary for each interval.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.10 or higher
- MongoDB

### Installing

1. Clone the repository
```bash
git clone https://github.com/shalmeo/rlttesttask.git
```
2. Navigate to the project directory
```bash
cd rlttesttask
```
3. Install the required packages
```bash
pip install -r requirements.txt
```

4. Setting up env variables
```bash
export MONGO_URI="mongodb://localhost:27017/"
export MONGO_DB="namedb"
export BOT_TOKEN="your_bot_token"
```

### Running the application
```bash
python -m rlttest.bot
```