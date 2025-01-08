from loguru import logger

tool_dict = {
    "process_search_results": "Google Search",
    "async_get_page_content": "Web Fetching",
}


def format_output(message_chunk, model_name):
    if model_name.startswith("azure") or model_name.startswith("gpt"):
        output_chunk = message_chunk.content

    elif model_name.startswith("claude"):
        # message_chunk is a list, containing dictionary or it is just an empty list
        if isinstance(message_chunk.content, list) and message_chunk.content:
            output_chunk = (
                message_chunk.content[0]["text"]
                if "text" in message_chunk.content[0]
                else ""
            )
        else:
            output_chunk = ""

    elif model_name.startswith("gemini"):
        output_chunk = message_chunk.content
    return output_chunk


def format_tool_call(
    ai_message_update_value,
    model_name: str,
):
    def extract_tool_call(ai_message_update_value, model_name):
        if model_name.startswith(("azure", "gpt")):
            tool_call = ai_message_update_value.additional_kwargs["tool_calls"][0]
            return tool_call["function"]["arguments"], tool_call["function"]["name"]

        elif model_name.startswith("claude"):
            # logger.info(f"output_chunk: {ai_message_update_value.content}")
            tool_call = ai_message_update_value.content[-1]
            return tool_call["partial_json"], tool_call["name"]

        elif model_name.startswith("gemini"):
            # logger.info(f"output_chunk: { ai_message_update_value.additional_kwargs}")
            tool_call = ai_message_update_value.additional_kwargs
            return tool_call["function_call"]["arguments"], tool_call["function_call"][
                "name"
            ]

    tool_kwargs, tool_name = extract_tool_call(ai_message_update_value, model_name)
    if tool_kwargs and tool_name:
        log_data = {
            "tool_kwargs": tool_kwargs,
            "tool_name": tool_dict[tool_name],
            "type": "thought_update",
        }
    else:
        log_data = ""
    return log_data
