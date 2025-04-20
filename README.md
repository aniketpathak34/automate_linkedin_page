# LinkedIn Post Automation API

A FastAPI-based service for automating LinkedIn post creation. This service allows you to create posts on your LinkedIn profile using the LinkedIn API.

## Features

- OAuth2 authentication with LinkedIn
- Create posts on your LinkedIn profile
- Secure token management
- Error handling and logging

## Prerequisites

- Python 3.8+
- LinkedIn Developer Account
- LinkedIn API Credentials

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd linkedin-post-automation
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your LinkedIn credentials:
```env
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
```

## Usage

1. Start the server:
```bash
uvicorn main:app --reload
```

2. Access the API documentation at `http://localhost:8000/docs`

3. Authentication Flow:
   - Visit `/auth` to get the LinkedIn authorization URL
   - Complete the LinkedIn authentication
   - Use the received token to create posts

4. Create a Post:
```bash
curl -X POST "http://localhost:8000/post" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your post content", "token": "your_access_token"}'
```

## API Endpoints

- `GET /`: Root endpoint
- `GET /auth`: Get LinkedIn authorization URL
- `GET /callback`: Handle LinkedIn OAuth callback
- `POST /post`: Create a new LinkedIn post

## Security

- Never commit your `.env` file
- Keep your LinkedIn API credentials secure
- Use environment variables for sensitive data
- The `.gitignore` file is configured to exclude sensitive files

## Error Handling

The API includes comprehensive error handling for:
- Authentication failures
- Invalid tokens
- API rate limits
- Network errors

## Logging

- Logs are stored in the application
- Debug information is available for troubleshooting
- Error messages are user-friendly

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the repository or contact the maintainers.

## Acknowledgments

- LinkedIn API Documentation
- FastAPI Framework
- Python Community