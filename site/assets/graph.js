const hiddenTypes = new Set();
let graph = null;
let cy = null;
let selected = null;

const trustLabel = {
  unverified: "Unverified",
  "machine-confirmed": "Machine-confirmed",
  "human-reviewed": "Human-reviewed",
};

async function main() {
  const response = await fetch("graph.json");
  graph = await response.json();
  const counts = document.querySelector("#counts");
  counts.textContent = `${graph.nodes.length} pages · ${graph.edges.length} links`;
  buildLegend();
  buildGraph();
  document.querySelector("#q").addEventListener("input", applyFilters);
  document.querySelector("#close-detail").addEventListener("click", () => select(null));
  const initial = decodeURIComponent(location.hash.replace(/^#/, ""));
  if (initial && graph.nodes.some((node) => node.id === initial)) select(initial);
  else if (graph.nodes.some((node) => node.id === "project")) select("project");
}

function buildLegend() {
  const legend = document.querySelector("#legend");
  const types = [...new Set(graph.nodes.map((node) => node.type))].sort();
  legend.replaceChildren(
    ...types.map((type) => {
      const count = graph.nodes.filter((node) => node.type === type).length;
      const color = graph.nodes.find((node) => node.type === type).color;
      const button = document.createElement("button");
      button.type = "button";
      button.setAttribute("aria-pressed", "true");
      button.innerHTML = `<span class="swatch" style="background:${color}"></span><span>${type}</span><span class="count">${count}</span>`;
      button.addEventListener("click", () => {
        if (hiddenTypes.has(type)) hiddenTypes.delete(type);
        else hiddenTypes.add(type);
        button.setAttribute("aria-pressed", hiddenTypes.has(type) ? "false" : "true");
        applyFilters();
      });
      return button;
    }),
  );
}

function positions() {
  const sections = [...new Set(graph.nodes.map((node) => node.section))];
  const place = {};
  const roots = graph.nodes.filter((node) => node.section === "root");
  const groups = sections.filter((section) => section !== "root");
  roots.forEach((node, index) => {
    const angle = (index / Math.max(roots.length, 1)) * Math.PI * 2;
    place[node.id] = { x: Math.cos(angle) * 70, y: Math.sin(angle) * 70 };
  });
  groups.forEach((section, index) => {
    const members = graph.nodes.filter((node) => node.section === section);
    const angle = (index / groups.length) * Math.PI * 2 - Math.PI / 2;
    const cx = Math.cos(angle) * 460;
    const cy = Math.sin(angle) * 460;
    members.forEach((node, member) => {
      const spread = (member / Math.max(members.length, 1)) * Math.PI * 2;
      const radius = members.length === 1 ? 0 : 120;
      place[node.id] = { x: cx + Math.cos(spread) * radius, y: cy + Math.sin(spread) * radius };
    });
  });
  return place;
}

function buildGraph() {
  const place = positions();
  cy = cytoscape({
    container: document.querySelector("#cy"),
    elements: [
      ...graph.nodes.map((node) => ({ data: node, position: place[node.id] })),
      ...graph.edges.map((edge, index) => ({ data: { ...edge, id: `e${index}` } })),
    ],
    layout: { name: "preset", fit: true, padding: 48 },
    wheelSensitivity: 0.2,
    style: [
      {
        selector: "node",
        style: {
          "background-color": "data(color)",
          label: "data(title)",
          color: "#f7f4ee",
          "font-size": 11,
          "font-family": "Segoe UI, system-ui, sans-serif",
          "text-wrap": "wrap",
          "text-max-width": 120,
          "text-valign": "bottom",
          "text-margin-y": 6,
          width: "data(size)",
          height: "data(size)",
          "border-width": 2,
          "border-color": "#10161d",
          "text-background-color": "#10161d",
          "text-background-opacity": 0.72,
          "text-background-padding": "2px",
        },
      },
      {
        selector: "edge",
        style: {
          width: 1.4,
          "line-color": "#6d7c8d",
          "target-arrow-color": "#6d7c8d",
          "target-arrow-shape": "triangle",
          "curve-style": "bezier",
          opacity: 0.7,
          "arrow-scale": 0.7,
        },
      },
      {
        selector: 'edge[kind = "cites"]',
        style: { "line-style": "dashed", opacity: 0.45 },
      },
      {
        selector: "node:selected",
        style: { "border-width": 4, "border-color": "#f4efe6" },
      },
    ],
  });
  cy.on("tap", "node", (event) => select(event.target.id()));
  cy.on("tap", (event) => {
    if (event.target === cy) select(null);
  });
  cy.fit(undefined, 48);
}

function applyFilters() {
  const query = document.querySelector("#q").value.trim().toLowerCase();
  cy.nodes().forEach((node) => {
    const data = node.data();
    const haystack = [data.title, data.type, data.description, ...(data.tags || []), data.id]
      .join(" ")
      .toLowerCase();
    const hide = hiddenTypes.has(data.type) || (query && !haystack.includes(query));
    node.style("display", hide ? "none" : "element");
  });
  cy.fit(cy.nodes(":visible"), 48);
}

function select(id) {
  selected = id;
  if (!id) {
    document.querySelector("#detail-body").innerHTML = '<p class="lede">Select a page on the graph.</p>';
    cy.elements().unselect();
    history.replaceState(null, "", "index.html");
    return;
  }
  const node = graph.nodes.find((item) => item.id === id);
  if (!node) return;
  cy.elements().unselect();
  cy.getElementById(id).select();
  document.querySelector("#detail-body").innerHTML = renderDetail(node);
  document.querySelectorAll("#detail-body [data-jump]").forEach((button) => {
    button.addEventListener("click", () => select(button.getAttribute("data-jump")));
  });
  history.replaceState(null, "", `index.html#${encodeURIComponent(id)}`);
}

function renderDetail(node) {
  const outgoing = graph.edges.filter((edge) => edge.source === node.id);
  const incoming = graph.edges.filter((edge) => edge.target === node.id);
  const sources = (node.sources || [])
    .map((source) => {
      const label = escapeHtml(source.title || source.resource);
      return source.href
        ? `<li><a href="${escapeAttr(source.href)}">${label}</a></li>`
        : `<li>${label}</li>`;
    })
    .join("");
  return `
    <p class="chips">
      <span class="chip" style="--chip:${escapeAttr(node.color)}">${escapeHtml(node.type)}</span>
      <span class="chip chip-plain">${escapeHtml(node.status)}</span>
      <span class="chip chip-plain">${escapeHtml(trustLabel[node.trust] || node.trust)}</span>
    </p>
    <h2>${escapeHtml(node.title)}</h2>
    <p class="lede">${escapeHtml(node.description)}</p>
    <p class="byline">${escapeHtml([node.generated_by, node.generated_at].filter(Boolean).join(" · ") || "Generator not recorded")}</p>
    <div class="actions">
      <a class="text-button" href="${escapeAttr(node.page)}">Read page</a>
      <a class="text-button" href="${escapeAttr(node.github)}">View on GitHub</a>
    </div>
    ${sources ? `<h3>Sources</h3><ul>${sources}</ul>` : ""}
    ${linkList("Links", outgoing)}
    ${linkList("Linked from", incoming)}
  `;
}

function linkList(title, edges) {
  if (!edges.length) return "";
  const items = edges
    .map((edge) => {
      const other = title === "Links" ? edge.target : edge.source;
      const node = graph.nodes.find((item) => item.id === other);
      const label = node ? node.title : other;
      return `<li><button type="button" class="text-button" data-jump="${escapeAttr(other)}">${escapeHtml(label)}</button> <span class="byline">${escapeHtml(edge.kind)}</span></li>`;
    })
    .join("");
  return `<h3>${escapeHtml(title)}</h3><ul>${items}</ul>`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function escapeAttr(value) {
  return escapeHtml(value).replaceAll('"', "&quot;");
}

main().catch((error) => {
  document.querySelector("#counts").textContent = "Could not load the graph.";
  console.error(error);
});
