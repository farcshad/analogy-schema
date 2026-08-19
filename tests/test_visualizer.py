import json
import pytest
from pathlib import Path
from visualizer.adapters import adapt_causal_backbone_to_vis, adapt_rich_event_graph_to_vis


def test_adapt_causal_backbone():
    outputs_dir = Path(__file__).parent.parent / "outputs"
    sample_dir = outputs_dir / "story_base_01"
    
    if (sample_dir / "causal_backbone.json").exists():
        with open(sample_dir / "causal_backbone.json", "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            
        vis_data = adapt_causal_backbone_to_vis(raw_data, "story_base_01", outputs_dir)
        
        assert vis_data["story_id"] == "story_base_01"
        assert vis_data["view_type"] == "backbone"
        assert len(vis_data["nodes"]) > 0
        
        first_node = vis_data["nodes"][0]
        assert "id" in first_node
        assert "label" in first_node
        assert "role" in first_node
        assert "temporal_grounding" in first_node
        assert "abstraction" in first_node
        
        assert len(vis_data["edges"]) > 0
        first_edge = vis_data["edges"][0]
        assert "source" in first_edge
        assert "target" in first_edge
        assert "label" in first_edge
        assert "is_temporal" in first_edge


def test_adapt_rich_event_graph():
    outputs_dir = Path(__file__).parent.parent / "outputs"
    sample_dir = outputs_dir / "story_base_01"
    
    if (sample_dir / "rich_event_graph.json").exists():
        with open(sample_dir / "rich_event_graph.json", "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            
        vis_data = adapt_rich_event_graph_to_vis(raw_data, "story_base_01", outputs_dir)
        
        assert vis_data["story_id"] == "story_base_01"
        assert vis_data["view_type"] == "rich"
        assert len(vis_data["nodes"]) > 0
        assert len(vis_data["edges"]) > 0
