shared_responses = {
    401: {
        "description": "Authentication Error",
        "content": {
            "application/json": {
                "example": {"message": "Could not authenticate user."}
            }
        },
    },
    404: {
        "description": "User Not Found Error",
        "content": {
            "application/json": {"example": {"message": "User not found."}}
        },
    },
}
