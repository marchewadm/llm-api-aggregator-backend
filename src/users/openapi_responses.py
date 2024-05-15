shared_responses = {
    401: {
        "description": "Authentication Error",
        "content": {
            "application/json": {
                "example": {"message": "Could not authenticate user."}
            }
        },
    },
}

update_password_responses = {401: shared_responses[401]}
