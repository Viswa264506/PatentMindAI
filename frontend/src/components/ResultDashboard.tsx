import ResultTabs from "./ResultTabs";

interface Props {
  result: any;
}

function ResultDashboard({ result }: Props) {
  if (!result) return null;

  const data = result;

  const novelty = data?.novelty_assessment?.novelty_score ?? 0;
  const innovation = data?.novelty_assessment?.innovation_score ?? 0;
  const confidence = data?.strategy_recommendations?.confidence_score
    ? Math.round(data.strategy_recommendations.confidence_score * 100)
    : 0;

  return (
    <div className="dashboard">

      <h2 className="dashboard-title">
        Patent Intelligence Dashboard
      </h2>
      <div className="dashboard-subtitle">Filing Analysis — Generated Report</div>

      <div className="dashboard-grid">

        <div className="dashboard-card">

    <h4>💡 Technology Domain</h4>

    <div className="dashboard-value">
        {data.research_plan.technical_domain}
    </div>

</div>

        <div className="dashboard-card">
          <h4>🎯 Research Focus</h4>
          <p className="card-text">
            {data?.research_plan?.research_focus ?? "N/A"}
          </p>
        </div>

        <div className="dashboard-card">
          <h4>📄 Patents Retrieved</h4>
          <h2>{data?.retrieved_patents?.length ?? 0}</h2>
        </div>

        <div className="dashboard-card">
          <h4>⭐ Novelty Score</h4>

          <div className="seal">
            <span className="seal-value">{novelty}</span>
            <span className="seal-percent">SCORE %</span>
          </div>

          <div className="progress">
            <div
              className="progress-fill"
              style={{ width: `${novelty}%` }}
            />
          </div>
        </div>

        <div className="dashboard-card">
          <h4>🚀 Innovation Score</h4>

          <div className="seal">
            <span className="seal-value">{innovation}</span>
            <span className="seal-percent">SCORE %</span>
          </div>

          <div className="progress">
            <div
              className="progress-fill"
              style={{ width: `${innovation}%` }}
            />
          </div>
        </div>

        <div className="dashboard-card">
          <h4>🧠 Confidence</h4>

          <div className="seal">
            <span className="seal-value">{confidence}</span>
            <span className="seal-percent">SCORE %</span>
          </div>

          <div className="progress">
            <div
              className="progress-fill"
              style={{ width: `${confidence}%` }}
            />
          </div>
        </div>

      </div>

      <ResultTabs result={data} />

    </div>
  );
}

export default ResultDashboard;
