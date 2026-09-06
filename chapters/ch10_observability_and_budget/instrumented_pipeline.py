# instrumented_pipeline.py
import json

import anthropic

from tracing_setup import tracer

client = anthropic.Anthropic()


def run_agent(agent_name, system_prompt, user_content):
    with tracer.start_as_current_span(agent_name) as span:
        span.set_attribute("agent.role", agent_name)
        span.set_attribute("input.length_chars", len(user_content))

        response = client.messages.create(
            model="your-provider-model-name",
            max_tokens=800,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}]
        )

        span.set_attribute("tokens.input", response.usage.input_tokens)
        span.set_attribute("tokens.output", response.usage.output_tokens)

        result = json.loads(response.content[0].text)
        if "confidence" in result:
            span.set_attribute("output.confidence", result["confidence"])

        return result
