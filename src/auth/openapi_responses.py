get_access_token_responses = {
    401: {
        "description": "Authentication Error",
        "content": {
            "application/json": {
                "example": {
                    "message": "Your email or password is incorrect. Please try again."
                }
            }
        },
    }
}
