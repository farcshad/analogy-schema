#!/usr/bin/env python3
"""
High-Performance Concurrent Batch Pipeline Runner.
Runs multiple stories simultaneously with intra-pipeline and inter-pipeline concurrency.

Usage:
    # Run the 6 exact benchmark narratives concurrently:
    python run_batch.py --benchmarks --concurrency 6

    # Run the 3 synthetic fixtures:
    python run_batch.py --synth --concurrency 3

    # Run all fixtures:
    python run_batch.py --all --concurrency 6

    # Run with deterministic mock provider:
    python run_batch.py --benchmarks --mock
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
        with open(story_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        story = Story.from_text(
            story_id=data.get("story_id", story_path.stem),
            text=data["text"]
        )

        print(f"🚀 [START] Processing: {story.story_id} ({len(story.sentences)} sentences)")
        
        try:
            result = await pipeline.arun(story)
            elapsed = time.time() - t0
            
            # Save outputs in neutral directory
            out_dir = output_dir / story.story_id
            out_dir.mkdir(parents=True, exist_ok=True)
            
            save_json(result.rich_graph, str(out_dir / "rich_event_graph.json"))
            save_json(result.backbone, str(out_dir / "causal_backbone.json"))
            
            md_content = export_backbone_markdown(result.backbone)
            with open(out_dir / "backbone_summary.md", "w", encoding="utf-8") as f:
                f.write(md_content)
                
            warnings_count = len(result.validation_warnings)
            warning_msg = f" (⚠️ {warnings_count} warnings)" if warnings_count > 0 else " (✅ 0 warnings)"
            print(f"✅ [DONE] {story.story_id} in {elapsed:.2f}s | Nodes: {len(result.backbone.nodes)}, Explanatory Edges: {len(result.backbone.explanatory_edges)}, Temporal: {len(result.backbone.temporal_constraints)}{warning_msg}")
            return story.story_id, True, elapsed, result.backbone
        except Exception as e:
            elapsed = time.time() - t0
            print(f"❌ [FAILED] {story.story_id} in {elapsed:.2f}s: {e}")
            return story.story_id, False, elapsed, None


async def main_async():
    parser = argparse.ArgumentParser(description="Concurrent multi-story causal graph induction runner.")
    parser.add_argument("--benchmarks", action="store_true", help="Run the 6 exact benchmark fixtures (story_base_01, story_target_01..05).")
    parser.add_argument("--synth", action="store_true", help="Run the 3 synthetic fixtures (synth_story_01..03).")
    parser.add_argument("--all", action="store_true", help="Run all available story fixtures.")
    parser.add_argument("--stories", nargs="+", help="Paths to story JSON files.")
    parser.add_argument("--concurrency", type=int, default=6, help="Maximum concurrent stories to process simultaneously.")
    parser.add_argument("--model", type=str, default="deepseek/deepseek-v4-flash", help="OpenRouter model identifier.")
    parser.add_argument("--mock", action="store_true", help="Use deterministic mock provider.")
    parser.add_argument("--output-dir", type=str, default="outputs", help="Output directory for generated graphs.")
    args = parser.parse_args()

    fixtures_dir = Path("analogy_schema/fixtures/stories")
    story_paths = []
    
    if args.benchmarks:
        story_paths = [
            fixtures_dir / "story_base_01.json",
            fixtures_dir / "story_target_01.json",
            fixtures_dir / "story_target_02.json",
            fixtures_dir / "story_target_03.json",
            fixtures_dir / "story_target_04.json",
            fixtures_dir / "story_target_05.json",
        ]
    elif args.synth:
        story_paths = [
            fixtures_dir / "synth_story_01.json",
            fixtures_dir / "synth_story_02.json",
            fixtures_dir / "synth_story_03.json",
        ]
    elif args.stories:
        story_paths = [Path(p) for p in args.stories]
    elif args.all:
        if fixtures_dir.exists():
            story_paths = sorted(list(fixtures_dir.glob("*.json")))
    else:
        # Default to benchmarks
        story_paths = [
            fixtures_dir / "story_base_01.json",
            fixtures_dir / "story_target_01.json",
            fixtures_dir / "story_target_02.json",
            fixtures_dir / "story_target_03.json",
            fixtures_dir / "story_target_04.json",
            fixtures_dir / "story_target_05.json",
        ]

    # Filter only existing files
    story_paths = [p for p in story_paths if p.exists()]
    if not story_paths:
        print("No story files found to execute.")
        return

    print("=" * 70)
    print(f"🌟 Analogy Schema Induction: Stabilized Batch Runner")
    print(f"📁 Stories to process: {len(story_paths)}")
    print(f"⚡ Inter-story concurrency: {args.concurrency}")
    print(f"🤖 LLM Model: {args.model} {'(Mock)' if args.mock else '(Live OpenRouter, reasoning=off)'}")
    print(f"🔄 Intra-pipeline concurrency: Stage C (Relations) & Stage D (Anchors) in parallel")
    print(f"🔒 Ground-Truth Leakage Shield: Active (StoryInput anonymized, labels quarantined)")
    print("=" * 70)

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

    print("\n" + "=" * 70)
    print(f"🎉 Batch execution completed in {total_elapsed:.2f}s")
    print(f"📊 Summary Table:")
    for sid, success, elapsed, backbone in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        if backbone:
            nodes_summary = ", ".join(f"{nid}:{n.abstraction.level_2_functional}" for nid, n in backbone.nodes.items())
            warnings = backbone.metadata.get("validation_warnings", [])
            w_str = f" | ⚠️ {len(warnings)} warnings" if warnings else " | ✅ 0 warnings"
            print(f"\n📌 Story: {sid} ({elapsed:.2f}s) [{status}{w_str}]")
            print(f"   - Nodes ({len(backbone.nodes)}): {nodes_summary}")
            print(f"   - Explanatory Edges ({len(backbone.explanatory_edges)}): {['(' + e.source_id + ' --' + e.relation_type.value + '--> ' + e.target_id + ')' for e in backbone.explanatory_edges]}")
            print(f"   - Temporal Constraints ({len(backbone.temporal_constraints)}): {['(' + e.source_id + ' --BEFORE--> ' + e.target_id + ')' for e in backbone.temporal_constraints]}")
            if backbone.anchors.contracts:
                print(f"   - Incentive Contracts: {[{'reward': c.promised_reward, 'req': c.contingent_requirement} for c in backbone.anchors.contracts]}")
            if backbone.pruned_node_ids:
                print(f"   - Pruned Nodes: {backbone.pruned_node_ids}")
            if warnings:
                print(f"   - Warnings: {warnings}")
        else:
            print(f"\n📌 Story: {sid} ({elapsed:.2f}s) [{status}]")
            
    print(f"\n💾 All outputs saved under: {output_dir.resolve()}/")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main_async())
