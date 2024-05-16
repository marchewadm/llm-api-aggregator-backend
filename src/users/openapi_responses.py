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

get_profile_responses = {401: shared_responses[401]}
update_password_responses = {401: shared_responses[401]}
update_profile_responses = {401: shared_responses[401]}
