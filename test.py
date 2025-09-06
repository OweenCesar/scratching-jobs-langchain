from tavily import TavilyClient

client = TavilyClient("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")
response = client.search(
    query="jobs in Madrid for english teachers",
)

print(response)