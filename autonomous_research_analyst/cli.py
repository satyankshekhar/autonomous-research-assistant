import argparse
import asyncio
import json

from autonomous_research_analyst.export.markdown import to_markdown
from autonomous_research_analyst.export.report_json import to_json
from autonomous_research_analyst.graph import ResearchGraph


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run an autonomous research analysis.")
    parser.add_argument("query", help="Research question or topic.")
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format.",
    )
    return parser


async def run(query: str, output_format: str) -> str:
    state = await ResearchGraph().run(query)
    if output_format == "json":
        return json.dumps(to_json(state), indent=2)
    return to_markdown(state)


def main() -> None:
    args = build_parser().parse_args()
    print(asyncio.run(run(args.query, args.format)))


if __name__ == "__main__":
    main()
