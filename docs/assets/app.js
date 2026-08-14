const LABELS = {
  attentional_pathway: "Attentional",
  emotional_pathway: "Emotional",
  relational_pathway: "Relational",
  narrative_pathway: "Narrative",
  communal_pathway: "Communal",
  recovery_index: "Recovery index",
};

const SVG_NS = "http://www.w3.org/2000/svg";

function svgElement(name, attributes = {}) {
  const node = document.createElementNS(SVG_NS, name);
  Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, value));
  return node;
}

function addSvgText(svg, text, x, y, className = "") {
  const node = svgElement("text", { x, y, class: className });
  node.textContent = text;
  svg.appendChild(node);
  return node;
}

function renderForestPlot(items) {
  const host = document.querySelector("#forest-plot");
  host.replaceChildren();
  const width = 700;
  const height = 335;
  const left = 145;
  const right = 46;
  const top = 28;
  const rowHeight = 43;
  const maxValue = Math.max(...items.map((item) => item.ci_high)) * 1.12;
  const scaleX = (value) => left + (value / maxValue) * (width - left - right);
  const svg = svgElement("svg", { viewBox: `0 0 ${width} ${height}`, role: "presentation" });

  [0, 0.25, 0.5, 0.75, 1].forEach((proportion) => {
    const value = proportion * maxValue;
    const x = scaleX(value);
    svg.appendChild(svgElement("line", { x1: x, y1: top - 5, x2: x, y2: height - 35, class: proportion === 0 ? "zero-line" : "grid-line" }));
    addSvgText(svg, value.toFixed(1), x, height - 14).setAttribute("text-anchor", "middle");
  });

  items.forEach((item, index) => {
    const y = top + index * rowHeight + 22;
    const label = addSvgText(svg, LABELS[item.outcome] || item.outcome, 0, y + 4);
    label.setAttribute("font-weight", item.outcome === "recovery_index" ? "700" : "500");
    svg.appendChild(svgElement("line", { x1: scaleX(item.ci_low), y1: y, x2: scaleX(item.ci_high), y2: y, class: "ci-line" }));
    svg.appendChild(svgElement("circle", { cx: scaleX(item.estimate), cy: y, r: 6.5, class: "point" }));
    const estimate = addSvgText(svg, item.estimate.toFixed(2), width - 3, y + 4);
    estimate.setAttribute("text-anchor", "end");
  });
  addSvgText(svg, "Within-person slope (synthetic)", (left + width - right) / 2, height - 1).setAttribute("text-anchor", "middle");
  host.appendChild(svg);
}

function renderTrajectory(rows, participantId) {
  const host = document.querySelector("#trajectory-chart");
  host.replaceChildren();
  const data = rows.filter((row) => row.participant_id === participantId).sort((a, b) => a.study_day - b.study_day);
  const width = 1020;
  const height = 315;
  const margin = { top: 18, right: 25, bottom: 40, left: 44 };
  const x = (day) => margin.left + ((day - 1) / 20) * (width - margin.left - margin.right);
  const y = (value) => height - margin.bottom - (value / 10) * (height - margin.top - margin.bottom);
  const svg = svgElement("svg", { viewBox: `0 0 ${width} ${height}`, role: "presentation" });

  [0, 2, 4, 6, 8, 10].forEach((value) => {
    const yy = y(value);
    svg.appendChild(svgElement("line", { x1: margin.left, y1: yy, x2: width - margin.right, y2: yy, class: "grid-line" }));
    const label = addSvgText(svg, String(value), margin.left - 10, yy + 4);
    label.setAttribute("text-anchor", "end");
  });
  [1, 5, 10, 15, 21].forEach((day) => {
    const label = addSvgText(svg, `Day ${day}`, x(day), height - 12);
    label.setAttribute("text-anchor", "middle");
  });

  const makePath = (key) => data.map((row, index) => `${index ? "L" : "M"}${x(row.study_day)},${y(row[key])}`).join(" ");
  svg.appendChild(svgElement("path", { d: makePath("presence_intensity"), class: "trajectory-line trajectory-presence" }));
  svg.appendChild(svgElement("path", { d: makePath("recovery_index"), class: "trajectory-line trajectory-recovery" }));
  data.forEach((row) => {
    svg.appendChild(svgElement("circle", { cx: x(row.study_day), cy: y(row.presence_intensity), r: 4.5, fill: "#efae92", class: "trajectory-dot" }));
    svg.appendChild(svgElement("circle", { cx: x(row.study_day), cy: y(row.recovery_index), r: 4.5, fill: "#9fc5b8", class: "trajectory-dot" }));
  });
  host.appendChild(svg);
}

function renderExcerpts(excerpts, filter = "all") {
  const host = document.querySelector("#excerpt-grid");
  const filtered = excerpts.filter((item) => filter === "all" || item.human_verified_codes.split("|").includes(filter)).slice(0, 6);
  host.replaceChildren();
  filtered.forEach((item) => {
    const card = document.createElement("article");
    card.className = "excerpt-card";
    const tags = item.human_verified_codes.split("|").map((code) => `<span class="tag">${code.replaceAll("_", " ")}</span>`).join("");
    card.innerHTML = `
      <div class="excerpt-top"><span>${item.excerpt_id}</span><span>synthetic · ${item.interview_wave.replaceAll("_", " ")}</span></div>
      <blockquote>${item.excerpt_text}</blockquote>
      <div class="tags" aria-label="Human-verified example codes">${tags}</div>
      <p class="memo"><strong>Interpretive memo:</strong> ${item.interpretive_memo}</p>
    `;
    host.appendChild(card);
  });
  if (!filtered.length) {
    host.innerHTML = '<p class="error-message">No synthetic excerpts match this filter.</p>';
  }
}

function showLoadError(error) {
  console.error(error);
  ["#forest-plot", "#trajectory-chart", "#excerpt-grid"].forEach((selector) => {
    const node = document.querySelector(selector);
    if (node) node.innerHTML = '<p class="error-message">Demo data could not be loaded. Serve the docs folder with a local web server rather than opening the file directly.</p>';
  });
}

async function initialize() {
  try {
    const [analysisResponse, excerptsResponse] = await Promise.all([
      fetch("data/analysis_summary.json"),
      fetch("data/excerpts.json"),
    ]);
    if (!analysisResponse.ok || !excerptsResponse.ok) throw new Error("Data request failed");
    const analysis = await analysisResponse.json();
    const excerpts = await excerptsResponse.json();

    document.querySelector("#metric-participants").textContent = analysis.metadata.participants;
    document.querySelector("#metric-observations").textContent = analysis.metadata.observations.toLocaleString();
    document.querySelector("#metric-days").textContent = analysis.metadata.study_days;
    renderForestPlot(analysis.associations);

    const lag = analysis.lagged_association;
    document.querySelector("#lag-estimate").textContent = lag.estimate.toFixed(2);
    document.querySelector("#lag-copy").textContent = `95% interval ${lag.ci_low.toFixed(2)} to ${lag.ci_high.toFixed(2)}, based on ${lag.observations} consecutive-day pairs. This is a synthetic association, not an empirical finding.`;

    const participants = [...new Set(analysis.trajectories.map((row) => row.participant_id))];
    const select = document.querySelector("#participant-select");
    participants.forEach((participant) => {
      const option = document.createElement("option");
      option.value = participant;
      option.textContent = participant;
      select.appendChild(option);
    });
    renderTrajectory(analysis.trajectories, participants[0]);
    select.addEventListener("change", () => renderTrajectory(analysis.trajectories, select.value));

    renderExcerpts(excerpts);
    document.querySelectorAll(".filter").forEach((button) => {
      button.addEventListener("click", () => {
        document.querySelectorAll(".filter").forEach((item) => item.classList.remove("active"));
        button.classList.add("active");
        renderExcerpts(excerpts, button.dataset.filter);
      });
    });
  } catch (error) {
    showLoadError(error);
  }
}

initialize();
