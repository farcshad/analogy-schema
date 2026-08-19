let cy = null;
let currentOutputData = null;
let currentView = 'backbone'; // 'backbone' or 'rich'

document.addEventListener('DOMContentLoaded', () => {
  initEventListeners();
  loadOutputsList();
});

function initEventListeners() {
  const outputSelect = document.getElementById('output-select');
  outputSelect.addEventListener('change', () => {
    const selected = outputSelect.value;
    if (selected) {
      loadGraphData(selected, currentView);
    }
  });

  const btnBackbone = document.getElementById('btn-view-backbone');
  const btnRich = document.getElementById('btn-view-rich');

  btnBackbone.addEventListener('click', () => {
    if (currentView !== 'backbone') {
      currentView = 'backbone';
      btnBackbone.classList.add('active');
      btnRich.classList.remove('active');
      const selected = outputSelect.value;
      if (selected) loadGraphData(selected, 'backbone');
    }
  });

  btnRich.addEventListener('click', () => {
    if (currentView !== 'rich') {
      currentView = 'rich';
      btnRich.classList.add('active');
      btnBackbone.classList.remove('active');
      const selected = outputSelect.value;
      if (selected) loadGraphData(selected, 'rich');
    }
  });

  document.getElementById('toggle-explanatory').addEventListener('change', applyEdgeFilters);
  document.getElementById('toggle-temporal').addEventListener('change', applyEdgeFilters);

  document.getElementById('btn-fit').addEventListener('click', () => {
    if (cy) cy.fit(undefined, 40);
  });

  document.getElementById('btn-reset').addEventListener('click', () => {
    if (cy) runLayout();
  });

  const warnBanner = document.getElementById('warnings-banner');
  warnBanner.addEventListener('click', () => {
    const details = document.getElementById('warnings-details');
    if (!details.classList.contains('empty')) {
      details.classList.toggle('hidden');
    }
  });
}

function toggleCard(btn, bodyId) {
  const body = document.getElementById(bodyId);
  if (body) {
    body.classList.toggle('hidden');
  }
  if (btn) {
    btn.classList.toggle('collapsed');
  }
}

async function loadOutputsList() {
  try {
    const res = await fetch('/api/outputs');
    const data = await res.json();
    const select = document.getElementById('output-select');
    select.innerHTML = '';

    if (!data.outputs || data.outputs.length === 0) {
      select.innerHTML = '<option value="">No output directories found</option>';
      return;
    }

    data.outputs.forEach(id => {
      const opt = document.createElement('option');
      opt.value = id;
      opt.textContent = id;
      select.appendChild(opt);
    });

    // Auto-select first available output
    if (data.outputs.length > 0) {
      select.value = data.outputs[0];
      loadGraphData(data.outputs[0], currentView);
    }
  } catch (err) {
    showToast('Failed to load outputs list: ' + err.message);
  }
}

async function loadGraphData(outputId, viewType) {
  showToast(`Loading ${outputId} (${viewType})...`);
  try {
    const endpoint = `/api/outputs/${encodeURIComponent(outputId)}/${viewType}`;
    const res = await fetch(endpoint);
    const data = await res.json();

    if (data.error) {
      showToast(data.error);
      renderEmptyState(data.error);
      return;
    }

    currentOutputData = data;
    renderGraph(data);
    renderSidebarPanels(data);
  } catch (err) {
    showToast('Error loading graph: ' + err.message);
  }
}

function renderEmptyState(msg) {
  const container = document.getElementById('cy');
  container.innerHTML = `<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#8b9bb4;font-size:0.9rem;">${msg}</div>`;
  document.getElementById('inspector-content').innerHTML = `<p class="placeholder-text">${msg}</p>`;
}

function renderGraph(data) {
  const elements = [];

  // 1. Build Nodes
  (data.nodes || []).forEach(n => {
    let nodeColor = '#38bdf8';
    let borderColor = '#2e3c50';
    let borderWidth = 2;

    const role = (n.role || '').toUpperCase();
    if (n.is_intervention || role === 'INTERVENTION') {
      nodeColor = '#c084fc';
      borderColor = '#a855f7';
      borderWidth = 3;
    } else if (n.is_focal_outcome || role === 'FOCAL_OUTCOME') {
      nodeColor = '#fb7185';
      borderColor = '#f43f5e';
      borderWidth = 3;
    } else if (n.is_contingent_outcome || role === 'CONTINGENT_OUTCOME') {
      nodeColor = '#fb923c';
      borderColor = '#f97316';
      borderWidth = 3;
    } else if (role === 'PROBLEM_STATE') {
      nodeColor = '#e11d48';
      borderColor = '#be123c';
    } else if (role === 'CONSTRAINT') {
      nodeColor = '#fbbf24';
      borderColor = '#d97706';
    } else if (role === 'CAUSAL_ANTECEDENT') {
      nodeColor = '#38bdf8';
      borderColor = '#0284c7';
    } else if (role === 'DOWNSTREAM_REACTION') {
      nodeColor = '#94a3b8';
      borderColor = '#64748b';
    }

    const displayLabel = n.label || n.id;

    elements.push({
      data: {
        id: n.id,
        label: `${n.id}\n${displayLabel}`,
        rawLabel: displayLabel,
        nodeData: n,
        nodeColor: nodeColor,
        borderColor: borderColor,
        borderWidth: borderWidth
      }
    });
  });

  // 2. Build Edges
  (data.edges || []).forEach(e => {
    const isTemporal = Boolean(e.is_temporal || e.category === 'temporal' || e.label === 'BEFORE');
    const edgeColor = isTemporal ? '#fbbf24' : '#38bdf8';
    const lineStyle = isTemporal ? 'dashed' : 'solid';

    elements.push({
      data: {
        id: e.id,
        source: e.source,
        target: e.target,
        label: e.label || 'CAUSES',
        category: e.category || (isTemporal ? 'temporal' : 'explanatory'),
        isTemporal: isTemporal,
        edgeColor: edgeColor,
        lineStyle: lineStyle,
        edgeData: e
      }
    });
  });

  // Initialize Cytoscape
  if (cy) {
    cy.destroy();
  }

  cy = cytoscape({
    container: document.getElementById('cy'),
    elements: elements,
    style: [
      {
        selector: 'node',
        style: {
          'label': 'data(label)',
          'text-wrap': 'wrap',
          'text-max-width': '140px',
          'text-valign': 'center',
          'text-halign': 'center',
          'background-color': '#18202c',
          'border-color': 'data(borderColor)',
          'border-width': 'data(borderWidth)',
          'color': '#f8fafc',
          'font-size': '11px',
          'font-weight': 600,
          'shape': 'round-rectangle',
          'width': '150px',
          'height': '65px',
          'padding': '8px',
          'text-outline-color': '#0f141c',
          'text-outline-width': '1px'
        }
      },
      {
        selector: 'node:selected',
        style: {
          'border-color': '#ffffff',
          'border-width': 4,
          'background-color': '#202b3b',
          'shadow-blur': 15,
          'shadow-color': '#38bdf8',
          'shadow-opacity': 0.8
        }
      },
      {
        selector: 'edge',
        style: {
          'label': 'data(label)',
          'width': 2.5,
          'line-color': 'data(edgeColor)',
          'target-arrow-color': 'data(edgeColor)',
          'target-arrow-shape': 'triangle',
          'curve-style': 'bezier',
          'line-style': 'data(lineStyle)',
          'line-dash-pattern': [6, 4],
          'arrow-scale': 1.2,
          'color': '#e2e8f0',
          'font-size': '10px',
          'font-weight': 600,
          'text-background-color': '#0f141c',
          'text-background-opacity': 0.85,
          'text-background-padding': '3px',
          'text-background-shape': 'round-rectangle',
          'text-rotation': 'autorotate'
        }
      },
      {
        selector: 'edge:selected',
        style: {
          'width': 4,
          'line-color': '#ffffff',
          'target-arrow-color': '#ffffff'
        }
      }
    ],
    layout: {
      name: 'dagre',
      rankDir: 'TB',
      nodeSep: 60,
      rankSep: 80,
      edgeSep: 40
    }
  });

  // Interaction handlers
  cy.on('tap', 'node', evt => {
    const node = evt.target;
    inspectNode(node.data('nodeData'));
  });

  cy.on('tap', 'edge', evt => {
    const edge = evt.target;
    inspectEdge(edge.data('edgeData'));
  });

  cy.on('tap', evt => {
    if (evt.target === cy) {
      clearInspection();
    }
  });

  applyEdgeFilters();
}

function runLayout() {
  if (!cy) return;
  try {
    const layout = cy.layout({
      name: 'dagre',
      rankDir: 'TB',
      nodeSep: 60,
      rankSep: 80,
      animate: true,
      animationDuration: 300
    });
    layout.run();
  } catch (e) {
    cy.layout({ name: 'breadthfirst', directed: true, padding: 40 }).run();
  }
}

function applyEdgeFilters() {
  if (!cy) return;
  const showExplanatory = document.getElementById('toggle-explanatory').checked;
  const showTemporal = document.getElementById('toggle-temporal').checked;

  cy.edges().forEach(edge => {
    const isTemp = edge.data('isTemporal');
    if (isTemp && !showTemporal) {
      edge.style('display', 'none');
    } else if (!isTemp && !showExplanatory) {
      edge.style('display', 'none');
    } else {
      edge.style('display', 'element');
    }
  });
}

function inspectNode(node) {
  const container = document.getElementById('inspector-content');
  if (!node) return;

  const role = node.role || 'STATE';
  const tg = node.temporal_grounding || {};
  const abstr = node.abstraction || {};
  const spans = node.provenance_text_spans || [];

  let html = `
    <div class="detail-row">
      <span class="detail-label">Node Identifier</span>
      <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
        <span class="code-badge">${node.id}</span>
        <span class="role-badge badge-${(role.toLowerCase())}">${role}</span>
        ${node.is_intervention ? '<span class="code-badge" style="color:#c084fc;border-color:#c084fc;">INTERVENTION</span>' : ''}
        ${node.is_focal_outcome ? '<span class="code-badge" style="color:#fb7185;border-color:#fb7185;">FOCAL_OUTCOME</span>' : ''}
        ${node.is_contingent_outcome ? '<span class="code-badge" style="color:#fb923c;border-color:#fb923c;">CONTINGENT_OUTCOME</span>' : ''}
      </div>
    </div>
  `;

  if (currentView === 'backbone') {
    html += `
      <div class="detail-row">
        <span class="detail-label">Abstraction Ladder</span>
        <div class="ladder-box">
          <div class="ladder-item">
            <span class="ladder-tag">Level 2 (Functional):</span>
            <span class="detail-value" style="font-weight:600;color:#38bdf8;">${abstr.level_2_functional || node.label || '-'}</span>
          </div>
          <div class="ladder-item">
            <span class="ladder-tag">Level 1 (Domain):</span>
            <span class="detail-value">${abstr.level_1_domain || '-'}</span>
          </div>
          <div class="ladder-item">
            <span class="ladder-tag">Level 0 (Raw):</span>
            <span class="detail-value">${abstr.level_0_raw || '-'}</span>
          </div>
          <div class="ladder-item">
            <span class="ladder-tag">Level 3 (Schema):</span>
            <span class="detail-value">${abstr.level_3_schema || '-'}</span>
          </div>
        </div>
      </div>

      <div class="detail-row">
        <span class="detail-label">Macro-Node Grounding</span>
        <span class="detail-value">Macro ID: <code>${node.macro_id || '-'}</code> (${node.macro_label || '-'})</span>
        <span class="detail-value">Source Normalized IDs: <code>${(node.source_normalized_ids || []).join(', ') || '-'}</code></span>
      </div>
    `;
  } else {
    // Rich Graph Details
    html += `
      <div class="detail-row">
        <span class="detail-label">Normalized Predicate</span>
        <span class="code-badge">${node.predicate || '-'}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Summary Label</span>
        <span class="detail-value">${node.summary || node.label || '-'}</span>
      </div>
      ${node.arguments ? `
        <div class="detail-row">
          <span class="detail-label">Arguments</span>
          <pre class="code-badge" style="display:block;white-space:pre-wrap;overflow-x:auto;">${JSON.stringify(node.arguments, null, 2)}</pre>
        </div>
      ` : ''}
    `;
  }

  // Temporal Grounding
  html += `
    <div class="detail-row">
      <span class="detail-label">Temporal Grounding</span>
      <div class="ladder-box">
        <div class="ladder-item"><span class="ladder-tag">Onset Phase:</span> <span class="code-badge">${tg.onset_phase || '-'}</span></div>
        <div class="ladder-item"><span class="ladder-tag">Holds at Intervention:</span> <span class="code-badge">${tg.holds_at_intervention ? 'true' : 'false'}</span></div>
        <div class="ladder-item"><span class="ladder-tag">Mention Phase:</span> <span class="code-badge">${tg.mention_phase || '-'}</span></div>
        <div class="ladder-item"><span class="ladder-tag">Temporal Extent:</span> <span class="code-badge">${tg.temporal_extent || '-'}</span></div>
      </div>
    </div>
  `;

  // Provenance Spans
  if (spans && spans.length > 0) {
    html += `
      <div class="detail-row">
        <span class="detail-label">Textual Provenance (${spans.length} spans)</span>
        ${spans.map(s => `<div class="provenance-box">"${escapeHtml(s)}"</div>`).join('')}
      </div>
    `;
  }

  container.innerHTML = html;

  // Highlight in Narrative Text Panel
  highlightProvenanceInStory(spans);

  // Scroll sidebar to top so user sees the details immediately
  const sidebar = document.getElementById('sidebar');
  if (sidebar) {
    sidebar.scrollTop = 0;
  }
}

function inspectEdge(edge) {
  const container = document.getElementById('inspector-content');
  if (!edge) return;

  const isTemp = Boolean(edge.is_temporal || edge.category === 'temporal');
  const categoryTag = isTemp ? 'TEMPORAL CONSTRAINT' : 'EXPLANATORY CAUSAL EDGE';

  let html = `
    <div class="detail-row">
      <span class="detail-label">Edge Connection</span>
      <div style="display:flex;align-items:center;gap:8px;">
        <span class="code-badge">${edge.source}</span>
        <span style="color:#8b9bb4;">--<b>${edge.label}</b>--></span>
        <span class="code-badge">${edge.target}</span>
      </div>
      <span class="role-badge" style="background:${isTemp ? '#fbbf24' : '#38bdf8'};color:#0f141c;margin-top:6px;width:fit-content;">${categoryTag}</span>
    </div>

    <div class="detail-row">
      <span class="detail-label">Underlying Rich Relations</span>
      <span class="code-badge">${(edge.underlying_relation_ids || []).join(', ') || 'Direct relation'}</span>
    </div>

    <div class="detail-row">
      <span class="detail-label">Justification / Evidence</span>
      <div class="provenance-box" style="color:#f8fafc;font-style:normal;">
        ${escapeHtml(edge.justification || edge.evidence || 'Evidence directly grounded in rich relation graph.')}
      </div>
    </div>

    <div class="detail-row">
      <span class="detail-label">Confidence & Explicitness</span>
      <span class="detail-value">Confidence: <code>${edge.confidence !== undefined ? edge.confidence : 1.0}</code> | Explicitness: <code>${edge.explicitness || 'explicit'}</code></span>
    </div>
  `;

  container.innerHTML = html;

  const sidebar = document.getElementById('sidebar');
  if (sidebar) {
    sidebar.scrollTop = 0;
  }
}

function clearInspection() {
  document.getElementById('inspector-content').innerHTML = `
    <p class="placeholder-text">Click any node or edge in the graph to inspect its abstraction ladder, functional role, temporal grounding, or provenance.</p>
  `;
  highlightProvenanceInStory([]);
}

function renderSidebarPanels(data) {
  // 1. Validation Warnings
  const warnings = data.validation_warnings || [];
  const warnBanner = document.getElementById('warnings-banner');
  const warnDetails = document.getElementById('warnings-details');

  if (warnings.length === 0) {
    warnBanner.className = 'warnings-banner empty';
    warnBanner.innerHTML = `<span class="warning-icon">✓</span> <span class="warning-text">No validation warnings</span>`;
    warnDetails.className = 'warnings-details hidden';
    warnDetails.innerHTML = '';
  } else {
    warnBanner.className = 'warnings-banner has-warnings';
    warnBanner.innerHTML = `<span class="warning-icon">⚠️</span> <span class="warning-text">${warnings.length} Validation Warnings (Click to expand)</span>`;
    warnDetails.className = 'warnings-details hidden';
    warnDetails.innerHTML = warnings.map(w => `<div class="warning-entry">⚠️ ${escapeHtml(w)}</div>`).join('');
  }

  // 2. Incentive Contracts
  const contracts = data.contracts || [];
  const contractsBody = document.getElementById('contracts-body');
  if (contracts.length > 0) {
    contractsBody.innerHTML = contracts.map(c => `
      <div class="ladder-box">
        <div class="ladder-item"><span class="ladder-tag">Promised Reward:</span> <span style="color:#fbbf24;font-weight:600;">${escapeHtml(c.promised_reward)}</span></div>
        <div class="ladder-item"><span class="ladder-tag">Contingent Requirement:</span> <span>${escapeHtml(c.contingent_requirement)}</span></div>
        <div class="ladder-item"><span class="ladder-tag">Condition Polarity:</span> <span class="code-badge">${c.condition_polarity || 'positive'}</span></div>
      </div>
    `).join('');
  } else {
    contractsBody.innerHTML = `<p class="placeholder-text">No structured incentive contracts present.</p>`;
  }

  // 3. Narrative Anchors
  const anchors = data.anchors || {};
  const anchorsBody = document.getElementById('anchors-body');
  if (anchors.central_problem || anchors.central_goal) {
    anchorsBody.innerHTML = `
      <div class="detail-row">
        <span class="detail-label">Central Problem</span>
        <span class="detail-value" style="color:#fb7185;">${escapeHtml(anchors.central_problem || '-')}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Central Goal</span>
        <span class="detail-value" style="color:#38bdf8;">${escapeHtml(anchors.central_goal || '-')}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Anchor IDs</span>
        <span class="detail-value">Interventions: <code>${(anchors.intervention_event_ids || []).join(', ') || '-'}</code></span>
        <span class="detail-value">Focal Outcomes: <code>${(anchors.focal_outcome_ids || []).join(', ') || '-'}</code></span>
        <span class="detail-value">Contingent Outcomes: <code>${(anchors.contingent_outcome_ids || []).join(', ') || '-'}</code></span>
        <span class="detail-value">Downstream Reactions: <code>${(anchors.downstream_reaction_ids || []).join(', ') || '-'}</code></span>
      </div>
    `;
  } else {
    anchorsBody.innerHTML = `<p class="placeholder-text">No anchor metadata available.</p>`;
  }

  // 4. Pruned Events
  const pruned = data.pruned_events || [];
  const prunedBody = document.getElementById('pruned-body');
  if (pruned.length > 0) {
    prunedBody.innerHTML = pruned.map(p => `
      <div class="detail-row" style="border-bottom:1px solid var(--border);padding-bottom:6px;">
        <span class="code-badge">${escapeHtml(p.id)}</span>
        <span class="detail-value" style="color:#94a3b8;font-size:0.78rem;">${escapeHtml(p.reason)}</span>
      </div>
    `).join('');
  } else {
    prunedBody.innerHTML = `<p class="placeholder-text">No events were pruned.</p>`;
  }

  // 5. Narrative Text Panel
  const storyContainer = document.getElementById('story-text-container');
  if (data.story_text) {
    storyContainer.innerHTML = `<p id="story-full-text">${escapeHtml(data.story_text)}</p>`;
  } else {
    storyContainer.innerHTML = `<p class="placeholder-text">Narrative text not available for this output.</p>`;
  }
}

function highlightProvenanceInStory(spans) {
  const storyP = document.getElementById('story-full-text');
  if (!storyP || !currentOutputData || !currentOutputData.story_text) return;

  const originalText = currentOutputData.story_text;
  if (!spans || spans.length === 0) {
    storyP.innerHTML = escapeHtml(originalText);
    return;
  }

  // Collect character intervals to highlight
  const intervals = [];
  spans.forEach(span => {
    if (!span || span.trim().length < 3) return;
    const cleanSpan = span.trim().toLowerCase();
    const lowerText = originalText.toLowerCase();
    let startIdx = 0;
    while ((startIdx = lowerText.indexOf(cleanSpan, startIdx)) !== -1) {
      intervals.push([startIdx, startIdx + cleanSpan.length]);
      startIdx += cleanSpan.length;
    }
  });

  if (intervals.length === 0) {
    storyP.innerHTML = escapeHtml(originalText);
    return;
  }

  // Merge overlapping intervals
  intervals.sort((a, b) => a[0] - b[0]);
  const merged = [intervals[0]];
  for (let i = 1; i < intervals.length; i++) {
    const prev = merged[merged.length - 1];
    const curr = intervals[i];
    if (curr[0] <= prev[1]) {
      prev[1] = Math.max(prev[1], curr[1]);
    } else {
      merged.push(curr);
    }
  }

  // Build safe HTML
  let html = '';
  let lastIdx = 0;
  merged.forEach(([s, e]) => {
    html += escapeHtml(originalText.substring(lastIdx, s));
    html += `<span class="highlighted-text">${escapeHtml(originalText.substring(s, e))}</span>`;
    lastIdx = e;
  });
  html += escapeHtml(originalText.substring(lastIdx));

  storyP.innerHTML = html;
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/"/g, '&quot;')
                    .replace(/'/g, '&#039;');
}

function showToast(msg) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = msg;
  toast.classList.remove('hidden');
  setTimeout(() => {
    toast.classList.add('hidden');
  }, 2500);
}
