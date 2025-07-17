functions = [
    {
        "name": "get_weather",
        "description": "Belirtilen şehir için canlı hava durumu bilgisini getirir.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Hava durumu öğrenilecek şehir"
                }
            },
            "required": ["city"]
        }
    }
]
