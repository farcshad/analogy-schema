#!/usr/bin/env python3
"""
CLI runner for the Analogical Schema Induction Pipeline.
Usage:
    python run_pipeline.py --story fixtures/stories/william_base.json
    python run_pipeline.py --story fixtures/stories/karen_true_analogy.json
    python run_pipeline.py --story fixtures/stories/karen_false_analogy.json
"""

import os
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv

from analogy_schema.models.story import Story
from analogy_schema.llm.openrouter_provider import OpenRouterProvider
from analogy_schema.llm.mock_provider import MockLLMProvider
from analogy_schema.pipeline.single_story_runner import SingleStoryPipeline
from analogy_schema.utils.serialization import save_json, export_backbone_markdown, to_json

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Run single-story causal graph induction pipeline.")
    parser.add_argument("--story", type=str, default="analogy_schema/fixtures/stories/william_base.json", help="Path to story JSON or TXT file.")
    parser.add_argument("--model", type=str, default="deepseek/deepseek-v4-flash", help="OpenRouter model identifier.")
    parser.add_argument("--mock", action="store_true", help="Use deterministic mock responses instead of live LLM.")
    parser.add_argument("--output-dir", type=str, default="outputs", help="Directory to save output artifacts.")
    args = parser.parse_args()

    # Load story
    story_path = Path(args.story)
    if not story_path.exists():
        print(f"Error: Story file not found at {story_path}")
        return

    if story_path.suffix == ".json":
        with open(story_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        story = Story.from_text(
            story_id=data.get("story_id", story_path.stem),
            text=data["text"],
            title=data.get("title"),
            metadata=data.get("metadata", {})
        )
    else:
        text = story_path.read_text(encoding="utf-8")
        story = Story.from_text(story_id=story_path.stem, text=text)

    print(f"Loaded story: {story.story_id} ({len(story.sentences)} sentences)")

    # Select LLM Provider
    if args.mock:
        from analogy_schema.fixtures.mock_responses import (
            get_william_mock_stage_a,
            get_william_mock_stage_b,
            get_william_mock_stage_c,
            get_william_mock_stage_d,
            get_william_mock_stage_f,
            get_william_mock_stage_gh,
        )
        llm = MockLLMProvider()
        llm.register_response("AtomicExtractionOutput", get_william_mock_stage_a())
        llm.register_response("NormalizationOutput", get_william_mock_stage_b())
        llm.register_response("RelationExtractionOutput", get_william_mock_stage_c())
        llm.register_response("GoalOutcomeOutput", get_william_mock_stage_d())
        llm.register_response("BackboneSelectionOutput", get_william_mock_stage_f())
        llm.register_response("MacroAbstractionOutput", get_william_mock_stage_gh())
        print("Using MockLLMProvider")
    else:
        llm = OpenRouterProvider(model_name=args.model, disable_reasoning=True)
        print(f"Using OpenRouterProvider with model: {args.model} (reasoning=off)")

    # Run pipeline
    print("\nRunning Causal Event Graph Induction Pipeline (Stages A -> H)...")
    pipeline = SingleStoryPipeline(llm=llm)
    result = pipeline.run(story)

    # Save outputs
    out_dir = Path(args.output_dir) / story.story_id
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Save rich graph JSON
    save_json(result.rich_graph, str(out_dir / "rich_event_graph.json"))
    # 2. Save causal backbone JSON
    save_json(result.backbone, str(out_dir / "causal_backbone.json"))
    # 3. Save Markdown inspection report
    md_content = export_backbone_markdown(result.backbone)
    with open(out_dir / "backbone_summary.md", "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\nPipeline finished successfully for '{story.story_id}'.")
    print(f"Artifacts saved to: {out_dir}")
    print(f"- Rich Event Graph: {out_dir / 'rich_event_graph.json'}")
    print(f"- Causal Backbone JSON: {out_dir / 'causal_backbone.json'}")
    print(f"- Human-Inspectable Markdown: {out_dir / 'backbone_summary.md'}")
    print("\n" + "=" * 60)
    print(md_content)
    print("=" * 60)


if __name__ == "__main__":
    main()
