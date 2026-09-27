# langgraph-post-reflection-agent

A generate-and-critique loop for social posts: one prompt writes the post, another grades it like a viral influencer would, and the graph bounces between them for a few rounds before returning the final draft. No tools, no retrieval — just a model arguing with itself until the copy gets better.

## What it does
- **`chains.py`** — two prompts over the same model: a generator that writes posts, and a reflector that critiques them
- **`main.py`** — a two-node cyclic graph (`generate` ⇄ `reflect`) with a stop condition
- Takes a rough LinkedIn post as input and returns a revised version

## Notes & details
- **The critique gets disguised as a `HumanMessage`.** The reflector's output is re-tagged as if the user wrote it, so the generator treats it as feedback to act on rather than as its own prior turn. Small trick, big behavioural difference.
- **Two personas, one model.** The only thing separating "writer" and "critic" is the system prompt — a cheap way to get adversarial pressure without a second model or a fine-tune.
- **Stopping is deliberately dumb**: bail once the message list passes six entries, roughly three round trips. Deterministic and cheap, versus asking a model to judge when it's satisfied (which tends to either stop immediately or never).
- **Custom state schema** — a `TypedDict` with `Annotated[list[BaseMessage], add_messages]`. Worth comparing against the prebuilt `MessagesState`: this spells out what that shortcut is actually doing, namely attaching an appending reducer to the messages field.
- **`MessagesPlaceholder`** lets the full conversation history flow into both prompts, which is what makes "respond with a revised version of your previous attempt" possible.
- **The graph renders itself to PNG** on every run, so the committed diagram always matches the code.
- **`final_response.txt`** holds a sample run's output if you want to see the shape of the result without spending tokens.
- **Requires** `OPENAI_API_KEY` in `.env`. No search or vector store keys needed.

## Run
```bash
uv sync
uv run main.py
```
