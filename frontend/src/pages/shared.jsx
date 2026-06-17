import React from "react";

export function QueryForm({ value, setValue, placeholder, onSubmit, loading, children, button = "Run" }) {
  return (
    <form className="query-form" onSubmit={onSubmit}>
      <input value={value} onChange={(event) => setValue(event.target.value)} placeholder={placeholder} />
      {children}
      <button type="submit" disabled={loading || !value.trim()}>{loading ? "Running" : button}</button>
    </form>
  );
}

export function Status({ state }) {
  if (state?.error) return <div className="status error">{state.error}</div>;
  if (state?.loading) return <SkeletonRows />;
  return null;
}

export function EmptyState({ children = "No results yet." }) {
  return <div className="empty-state">{children}</div>;
}

export function SkeletonRows() {
  return (
    <div className="skeleton-stack compact">
      <div className="skeleton input" />
      <div className="skeleton panel small" />
    </div>
  );
}

export function useAsyncAction(fn) {
  const [state, setState] = React.useState({ loading: false, error: "", data: null });
  async function run(...args) {
    setState({ loading: true, error: "", data: null });
    try {
      const data = await fn(...args);
      setState({ loading: false, error: "", data });
      return data;
    } catch (error) {
      setState({ loading: false, error: error.message || "Request failed", data: null });
      return null;
    }
  }
  return [state, run, setState];
}

export function formatNumber(value) {
  if (value === undefined || value === null || value === "") return "";
  const number = Number(value);
  if (Number.isNaN(number)) return value;
  return number.toFixed(number >= 1 ? 2 : 3);
}

export function normalizeSuffixes(analysis) {
  const suffixes = analysis?.suffixes || analysis?.suffix_chain || [];
  return suffixes.map((item) => (typeof item === "string" ? item : item?.suffix || item?.value)).filter(Boolean);
}

export function ResultTable({ rows, columns }) {
  if (!rows?.length) return <EmptyState />;
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>{columns.map((column) => <th key={column.key}>{column.label}</th>)}</tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={`${row.word || row.lemma || row.cognate_id || row.query || "row"}-${index}`}>
              {columns.map((column) => <td key={column.key}>{column.render ? column.render(row) : row[column.key]}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function LinearGraph({ nodes, accent = "blue" }) {
  const clean = nodes.filter(Boolean);
  if (!clean.length) return <EmptyState>No graph data.</EmptyState>;
  const width = 760;
  const height = Math.max(150, clean.length * 58);
  return (
    <svg className="graph" viewBox={`0 0 ${width} ${height}`} role="img">
      {clean.map((node, index) => {
        const y = 48 + index * 56;
        return (
          <g key={`${node}-${index}`}>
            {index > 0 && <line x1="52" y1={y - 36} x2="52" y2={y - 14} className="edge" />}
            <circle cx="52" cy={y} r="13" className={`node ${accent}`} />
            <text x="82" y={y + 5}>{node}</text>
          </g>
        );
      })}
    </svg>
  );
}

export function RadialGraph({ nodes }) {
  const clean = nodes.filter(Boolean);
  if (!clean.length) return <EmptyState>No graph data.</EmptyState>;
  const center = { x: 230, y: 155 };
  const radius = 112;
  const outer = clean.slice(1);
  return (
    <svg className="graph graph-compact" viewBox="0 0 460 310" role="img">
      <circle cx={center.x} cy={center.y} r="18" className="node blue" />
      <text x={center.x + 28} y={center.y + 5}>{clean[0]}</text>
      {outer.map((node, index) => {
        const angle = (Math.PI * 2 * index) / Math.max(outer.length, 1) - Math.PI / 2;
        const x = center.x + Math.cos(angle) * radius;
        const y = center.y + Math.sin(angle) * radius;
        return (
          <g key={`${node}-${index}`}>
            <line x1={center.x} y1={center.y} x2={x} y2={y} className="edge" />
            <circle cx={x} cy={y} r="12" className="node green" />
            <text x={x + 16} y={y + 4}>{node}</text>
          </g>
        );
      })}
    </svg>
  );
}
