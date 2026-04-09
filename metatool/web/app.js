const elements = {
  sourceName: document.querySelector("#source-name"),
  providerName: document.querySelector("#provider-name"),
  sourceCode: document.querySelector("#source-code"),
  statusText: document.querySelector("#status-text"),
  analyzeButton: document.querySelector("#analyze-button"),
  loadExample: document.querySelector("#load-example"),
  metricTotal: document.querySelector("#metric-total"),
  metricHigh: document.querySelector("#metric-high"),
  metricMedium: document.querySelector("#metric-medium"),
  metricLow: document.querySelector("#metric-low"),
  summaryText: document.querySelector("#summary-text"),
  categoryBars: document.querySelector("#category-bars"),
  findingsList: document.querySelector("#findings-list"),
  refactorNotes: document.querySelector("#refactor-notes"),
  refactoredCode: document.querySelector("#refactored-code"),
  reportPreview: document.querySelector("#report-preview"),
};

async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Request failed.");
  }
  return data;
}

function setStatus(message) {
  elements.statusText.textContent = message;
}

function renderMetrics(result) {
  elements.metricTotal.textContent = result.finding_count;
  elements.metricHigh.textContent = result.severity_counts.high;
  elements.metricMedium.textContent = result.severity_counts.medium;
  elements.metricLow.textContent = result.severity_counts.low;
}

function renderCategoryBars(categoryCounts, total) {
  const entries = Object.entries(categoryCounts);
  elements.categoryBars.innerHTML = "";
  if (!entries.length) {
    elements.categoryBars.innerHTML = "<p class='summary-text'>当前没有分类数据。</p>";
    return;
  }

  for (const [category, count] of entries) {
    const ratio = total === 0 ? 0 : Math.max(8, Math.round((count / total) * 100));
    const wrapper = document.createElement("article");
    wrapper.className = "category-bar";
    wrapper.innerHTML = `
      <header>
        <span>${category}</span>
        <span>${count}</span>
      </header>
      <div class="category-bar-track">
        <div class="category-bar-fill" style="width:${ratio}%"></div>
      </div>
    `;
    elements.categoryBars.appendChild(wrapper);
  }
}

function renderFindings(findings) {
  elements.findingsList.innerHTML = "";
  if (!findings.length) {
    elements.findingsList.innerHTML = "<p class='summary-text'>没有检测到问题。</p>";
    return;
  }

  for (const finding of findings) {
    const card = document.createElement("article");
    card.className = "finding-card";
    card.innerHTML = `
      <header>
        <h3>${finding.title}</h3>
        <span class="tag ${finding.severity}">${finding.severity}</span>
      </header>
      <p class="finding-meta">分类：${finding.category} · 行号：${finding.line ?? "unknown"}</p>
      <p class="finding-detail">${finding.detail}</p>
      <p class="finding-recommendation">建议：${finding.recommendation || "请结合上下文人工确认。"}</p>
    `;
    elements.findingsList.appendChild(card);
  }
}

function renderRefactorNotes(notes) {
  elements.refactorNotes.innerHTML = "";
  for (const note of notes) {
    const item = document.createElement("li");
    item.textContent = note;
    elements.refactorNotes.appendChild(item);
  }
}

function renderResult(result) {
  renderMetrics(result);
  renderCategoryBars(result.category_counts, result.finding_count);
  renderFindings(result.findings);
  renderRefactorNotes(result.refactor_notes);
  elements.summaryText.textContent = result.summary;
  elements.refactoredCode.textContent = result.refactored_source;
  elements.reportPreview.textContent = result.markdown_report;
  setStatus(`审查完成，报告已写入 ${result.report_path}，重构代码已写入 ${result.refactored_path}。`);
}

async function analyzeSource() {
  const source = elements.sourceCode.value;
  const sourceName = elements.sourceName.value.trim() || "snippet.py";
  const providerName = elements.providerName.value;

  if (!source.trim()) {
    setStatus("请输入 Python 源码后再开始审查。");
    return;
  }

  if (providerName === "compatible") {
    setStatus("正在调用 compatible provider。如果环境变量未配置，接口会返回错误。");
  } else {
    setStatus("正在分析代码，请稍候...");
  }

  elements.analyzeButton.disabled = true;
  try {
    const result = await requestJson("/api/review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        source,
        source_name: sourceName,
        provider_name: providerName,
        persist_output: true,
      }),
    });
    renderResult(result);
  } catch (error) {
    setStatus(`执行失败：${error.message}`);
  } finally {
    elements.analyzeButton.disabled = false;
  }
}

async function loadExample() {
  setStatus("正在载入示例代码...");
  try {
    const result = await requestJson("/api/example");
    elements.sourceName.value = result.source_name;
    elements.sourceCode.value = result.source;
    setStatus("示例代码已载入，可以直接开始审查。");
  } catch (error) {
    setStatus(`载入示例失败：${error.message}`);
  }
}

elements.analyzeButton.addEventListener("click", analyzeSource);
elements.loadExample.addEventListener("click", loadExample);
window.addEventListener("DOMContentLoaded", loadExample);
