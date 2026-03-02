def get_list_dlqs_and_topic():
    return [
        {
            "subscription": "subscription-fila-um-dlq",
            "topic": "date-me-topic-fila-um-queue",
        },
        {
            "subscription": "subscription-fila-dois-dlq",
            "topic": "date-me-topic-fila-dois-queue",
        },
        {
            "subscription": "subscription-fila-tres-dlq",
            "topic": "date-me-topic-fila-tres-queue",
        },
        {
            "subscription": "subscription-fila-quatro-dlq",
            "topic": "date-me-topic-fila-quatro-queue",
        },
        {
            "subscription": "subscription-reporting-reported-posts-dlq",
            "topic": "date-me-topic-reporting-reported-posts-queue",
        },
        {
            "subscription": "subscription-reporting-reported-posts-resolved-dlq",
            "topic": "date-me-topic-reporting-reported-comments-queue",
        },
    ]
