import { useState } from "react";

interface Props {
  result: any;
}

/** Renders a simple markdown-flavoured report (#, ##, ###, **bold**, - lists) as styled JSX. */
function MarkdownReport({ text }: { text: string }) {
  const renderInline = (line: string, key: number) => {
    const parts = line.split(/(\*\*[^*]+\*\*)/g).filter(Boolean);
    return (
      <p key={key}>
        {parts.map((part, i) =>
          part.startsWith("**") && part.endsWith("**") ? (
            <strong key={i}>{part.slice(2, -2)}</strong>
          ) : (
            <span key={i}>{part}</span>
          )
        )}
      </p>
    );
  };

  const lines = text.split("\n");

  return (
    <div className="report-body">
      {lines.map((raw, idx) => {
        const line = raw.trim();

        if (!line) return null;

        if (line.startsWith("### ")) {
          return <h4 key={idx}>{line.replace(/^###\s*/, "")}</h4>;
        }
        if (line.startsWith("## ")) {
          return <h3 key={idx}>{line.replace(/^##\s*/, "")}</h3>;
        }
        if (line.startsWith("# ")) {
          return <h2 key={idx}>{line.replace(/^#\s*/, "")}</h2>;
        }
        if (line.startsWith("- ") || line.startsWith("* ")) {
          return (
            <li className="report-li" key={idx}>
              {line.replace(/^[-*]\s*/, "")}
            </li>
          );
        }

        return renderInline(line, idx);
      })}
    </div>
  );
}

const TABS = [
  { key: "overview", label: "Overview" },
  { key: "research", label: "Research Plan" },
  { key: "patents", label: "Patents" },
  { key: "novelty", label: "Novelty" },
  { key: "strategy", label: "Strategy" },
  { key: "report", label: "Report" },
];

function ResultTabs({ result }: Props) {

  if (!result) {
    return null;
}

const data = result;

  const [tab, setTab] = useState("overview");

  return (
    <div>

      <div className="tabs-nav" role="tablist">
        {TABS.map((t) => (
          <button
            key={t.key}
            role="tab"
            aria-selected={tab === t.key}
            className={`tab-btn${tab === t.key ? " active" : ""}`}
            onClick={() => setTab(t.key)}
          >
            {t.label}
            <span className="tab-indicator" />
          </button>
        ))}
      </div>

      {tab === "overview" && (
        <div className="tab-panel">

          <div className="overview-card">
            <h2>Executive Summary</h2>

            <p>
              {data?.strategy_recommendations?.executive_summary ??
                "No executive summary available."}
            </p>

            <hr />

            <h3>Suggested Patent Title</h3>

            <p>
              {data?.strategy_recommendations?.suggested_patent_title ??
                "Not Available"}
            </p>

            <h3>Novelty Score</h3>

            <p>
              {data?.novelty_assessment?.novelty_score ?? "N/A"}
            </p>

            <h3>Innovation Score</h3>

            <p>
              {data?.novelty_assessment?.innovation_score ?? "N/A"}
            </p>

            <h3>Overlap Risk</h3>

            <p>
              {data?.novelty_assessment?.similarity_analysis?.overlap_risk ??
                "N/A"}
            </p>
          </div>

        </div>
      )}

      {tab === "research" && (

  <div className="tab-panel research-container">

    <div className="research-card">

      <h2>Technology Domain</h2>

      <p>{data?.research_plan?.technical_domain}</p>

    </div>

    <div className="research-card">

      <h2>Research Focus</h2>

      <p>{data?.research_plan?.research_focus}</p>

    </div>

    <div className="research-card">

      <h2>Important Concepts</h2>

      <ul>

        {data?.research_plan?.important_concepts?.map(
          (item: string, index: number) => (

            <li key={index}>{item}</li>

          )
        )}

      </ul>

    </div>

    <div className="research-card">

      <h2>Technical Keywords</h2>

      <ul>

        {data?.research_plan?.technical_keywords?.map(
          (item: string, index: number) => (

            <li key={index}>{item}</li>

          )
        )}

      </ul>

    </div>

    <div className="research-card">

      <h2>Search Queries</h2>

      <ul>

        {data?.research_plan?.search_queries?.map(
          (item: string, index: number) => (

            <li key={index}>{item}</li>

          )
        )}

      </ul>

    </div>

  </div>

)}

      {tab === "patents" && (

<div className="tab-panel">

<h2 style={{marginBottom:"24px"}}>

Retrieved Patents ({data?.retrieved_patents?.length ?? 0})

</h2>

<div className="patent-grid">

{data?.retrieved_patents?.map((patent:any,index:number)=>(

<div className="patent-card" key={index}>

<h3>{patent.title}</h3>

<p>

<b>Patent Number</b>

{patent.patent_number}

</p>

<p>

<b>Provider</b>

{patent.provider}

</p>

<p>

<b>Abstract</b>

{patent.abstract}

</p>

{patent.url && (

<a

href={patent.url}

target="_blank"

rel="noreferrer"

className="view-btn"

>

View Patent →

</a>

)}

</div>

))}

</div>

</div>

)}

      {tab === "novelty" && (
        <div className="tab-panel">

          <h2>Novelty Assessment</h2>

          <div className="insight-grid">

            <div className="insight-card insight-card-wide">
              <h3>Assessment Reasoning</h3>
              <p>
                {data?.novelty_assessment?.reasoning ??
                  "No reasoning available."}
              </p>
            </div>

            <div className="insight-card">
              <h3>Confidence</h3>
              <div className="stat-row">
                <span className="stat-number">
                  {data?.novelty_assessment?.confidence_score
                    ? Math.round(data.novelty_assessment.confidence_score * 100)
                    : "N/A"}
                  {data?.novelty_assessment?.confidence_score ? "%" : ""}
                </span>
              </div>
            </div>

            <div className="insight-card">
              <h3>Overlap Risk</h3>
              <span
                className={`risk-badge risk-${(
                  data?.novelty_assessment?.similarity_analysis
                    ?.overlap_risk ?? "unknown"
                )
                  .toString()
                  .toLowerCase()}`}
              >
                {data?.novelty_assessment?.similarity_analysis
                  ?.overlap_risk ?? "N/A"}
              </span>
            </div>

            <div className="insight-card">
              <h3>Existing Features Found</h3>
              <div className="tag-list">
                {data?.novelty_assessment?.similarity_analysis?.existing_features?.map(
                  (item: string, index: number) => (
                    <span className="tag tag-muted" key={index}>
                      {item}
                    </span>
                  )
                )}
              </div>
            </div>

            <div className="insight-card">
              <h3>Unique Features</h3>
              <div className="tag-list">
                {data?.novelty_assessment?.similarity_analysis?.unique_features?.map(
                  (item: string, index: number) => (
                    <span className="tag tag-gold" key={index}>
                      {item}
                    </span>
                  )
                )}
              </div>
            </div>

          </div>

        </div>
      )}

      {tab === "strategy" && (
        <div className="tab-panel">

          <h2>Strategy Recommendations</h2>

          <div className="insight-grid">

            <div className="insight-card insight-card-wide">
              <h3>Executive Summary</h3>
              <p>
                {data?.strategy_recommendations?.executive_summary ?? "N/A"}
              </p>
            </div>

            <div className="insight-card">
              <h3>Confidence</h3>
              <div className="stat-row">
                <span className="stat-number">
                  {data?.strategy_recommendations?.confidence_score
                    ? Math.round(
                        data.strategy_recommendations.confidence_score * 100
                      )
                    : "N/A"}
                  {data?.strategy_recommendations?.confidence_score ? "%" : ""}
                </span>
              </div>
            </div>

            <div className="insight-card">
              <h3>Suggested Patent Title</h3>
              <p>
                {data?.strategy_recommendations?.suggested_patent_title ??
                  "N/A"}
              </p>
            </div>

            <div className="insight-card insight-card-wide">
              <h3>Suggested Abstract</h3>
              <p>
                {data?.strategy_recommendations?.suggested_abstract ?? "N/A"}
              </p>
            </div>

            <div className="insight-card">
              <h3>Improvement Suggestions</h3>
              <ul className="insight-list">
                {data?.strategy_recommendations?.improvement_suggestions?.map(
                  (item: string, index: number) => (
                    <li key={index}>{item}</li>
                  )
                )}
              </ul>
            </div>

            <div className="insight-card">
              <h3>Technical Risk Areas</h3>
              <ul className="insight-list insight-list-risk">
                {data?.strategy_recommendations?.technical_risk_areas?.map(
                  (item: string, index: number) => (
                    <li key={index}>{item}</li>
                  )
                )}
              </ul>
            </div>

            <div className="insight-card insight-card-wide">
              <h3>Future Research Directions</h3>
              <ul className="insight-list">
                {data?.strategy_recommendations?.future_research_directions?.map(
                  (item: string, index: number) => (
                    <li key={index}>{item}</li>
                  )
                )}
              </ul>
            </div>

          </div>

        </div>
      )}

      {tab === "report" && (
        <div className="tab-panel">

          <h2>Final Report</h2>

          <div className="report-card">
            {data?.final_report ? (
              <MarkdownReport text={data.final_report} />
            ) : (
              <p>No report generated.</p>
            )}
          </div>

        </div>
      )}

    </div>
  );
}

export default ResultTabs;
