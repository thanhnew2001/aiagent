# Facebook Poster

This project is a simple Python application that posts content to Facebook every hour. It utilizes the Facebook API for authentication and posting.

## Project Structure

```
facebook-poster
├── src
│   ├── main.py
│   └── utils.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/facebook-poster.git
   cd facebook-poster
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your Facebook API credentials in `src/main.py`.

## Usage

To start the application, run the following command:
```
python src/main.py
```

The application will authenticate with the Facebook API and begin posting content every hour.

## Configuration

Make sure to set up your Facebook App and obtain the necessary access tokens. Update the relevant sections in `src/main.py` with your credentials.

## License

This project is licensed under the MIT License.