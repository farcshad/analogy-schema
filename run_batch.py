#!/usr/bin/env python3
"""
High-Performance Concurrent Batch Pipeline Runner.
Runs multiple stories simultaneously with intra-pipeline and inter-pipeline concurrency.

Usage:
    # Run all 6 benchmark narratives concurrently:
    python run_batch.py --all --concurrency 4

    # Run specific stories:
    python run_batch.py --stories analogy_schema/fixtures/stories/william_base.json analogy_schema/fixtures/stories/karen_true_analogy.json

    # Run with deterministic mock provider:
    python run_batch.py --all --mock
"""

import os
import json
import time
import asyncio
import argparse
from pathlib import Path
from dotenv import load_dotenv

from analogy_schema.models.story import Story
from analogy_schema.llm.openrouter_provider import OpenRouterProvider
from analogy_schema.llm.mock_provider import MockLLMProvider
from analogy_schema.pipeline.single_story_runner import SingleStoryPipeline
from analogy_schema.utils.serialization import save_json, export_backbone_markdown

load_dotenv()


async def process_single_story(
    story_path: Path,
    pipeline: SingleStoryPipeline,
    semaphore: asyncio.Semaphore,
    output_dir: Path
):
    async with semaphore:
        t0 = time.time()
        # Load story
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

        print(f"🚀 [START] Processing: {story.story_id} ({len(story.sentences)} sentences)")
        
        try:
            result = await pipeline.arun(story)
            elapsed = time.time() - t0
            
            # Save outputs
            out_dir = output_dir / story.story_id
            out_dir.mkdir(parents=True, exist_ok=True)
            
            save_json(result.rich_graph, str(out_dir / "rich_event_graph.json"))
            save_json(result.backbone, str(out_dir / "causal_backbone.json"))
            
            md_content = export_backbone_markdown(result.backbone)
            with open(out_dir / "backbone_summary.md", "w", encoding="utf-8") as f:
                f.write(md_content)
                
            warnings_count = len(result.validation_warnings)
            warning_msg = f" (⚠️ {warnings_count} warnings)" if warnings_count > 0 else " (✅ 0 warnings)"
            print(f"✅ [DONE] {story.story_id} in {elapsed:.2f}s | Nodes: {len(result.backbone.nodes)}, Edges: {len(result.backbone.edges)}{warning_msg}")
            return story.story_id, True, elapsed, md_content
        except Exception as e:
            elapsed = time.time() - t0
            print(f"❌ [FAILED] {story.story_id} in {elapsed:.2f}s: {e}")
            return story.story_id, False, elapsed, str(e)


async def main_async():
    parser = argparse.ArgumentParser(description="Concurrent multi-story causal graph induction runner.")
    parser.add_argument("--all", action="store_true", help="Run all benchmark fixtures in fixtures/stories/.")
    parser.add_argument("--stories", nargs="+", help="Paths to story JSON files.")
    parser.add_argument("--concurrency", type=int, default=4, help="Maximum concurrent stories to process simultaneously.")
    parser.add_argument("--model", type=str, default="deepseek/deepseek-v4-flash", help="OpenRouter model identifier.")
    parser.add_argument("--mock", action="store_true", help="Use deterministic mock provider.")
    parser.add_argument("--output-dir", type=str, default="outputs", help="Output directory for generated graphs.")
    args = parser.parse_args()

    # Collect story paths
    story_paths = []
    if args.all:
        fixtures_dir = Path("analogy_schema/fixtures/stories")
        if fixtures_dir.exists():
            story_paths = sorted(list(fixtures_dir.glob("*.json")))
    elif args.stories:
        story_paths = [Path(p) for p in args.stories]
    else:
        # Default to the 6 benchmark fixtures
        fixtures_dir = Path("analogy_schema/fixtures/stories")
        if fixtures_dir.exists():
            story_paths = sorted(list(fixtures_dir.glob("*.json")))
        else:
            print("Please specify --stories or --all.")
            return

    if not story_paths:
        print("No story files found.")
        return

    print("=" * 65)
    print(f"🌟 Analogy Schema Induction: Concurrent Batch Runner")
    print(f"📁 Stories to process: {len(story_paths)}")
    print(f"⚡ Inter-story concurrency: {args.concurrency}")
    print(f"🤖 LLM Model: {args.model} {'(Mock)' if args.mock else '(Live OpenRouter, reasoning=off)'}")
    print(f"🔄 Intra-pipeline concurrency: Stage C (Relations) & Stage D (Anchors) run in parallel")
    print("=" * 65)

    # Initialize Provider
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
        llm.register_response("MacroGroupingOutput", get_william_mock_stage_gh())
    else:
        llm = OpenRouterProvider(model_name=args.model, disable_reasoning=True)

    pipeline = SingleStoryPipeline(llm=llm)
    semaphore = asyncio.Semaphore(args.concurrency)
    output_dir = Path(args.output_dir)

    total_start = time.time()
    tasks = [
        process_single_story(sp, pipeline, semaphore, output_dir)
        for sp in story_paths
    ]
    results = await asyncio.gather(*tasks)
    total_elapsed = time.time() - total_start

    print("\n" + "=" * 65)
    print(f"🎉 Batch execution completed in {total_elapsed:.2f}s")
    print(f"📊 Summary:")
    for sid, success, elapsed, _ in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  - {sid:<30} {status} ({elapsed:.2f}s)")
    print(f"💾 All outputs saved under: {output_dir.resolve()}/")
    print("=" * 65)


if __name__ == "__main__":
    asyncio.run(main_async())
