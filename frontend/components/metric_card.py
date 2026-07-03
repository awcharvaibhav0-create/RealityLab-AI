def render_metric_card(icon: str, label: str, value: str) -> str:
    return f"""
    <div class="metric-card">
        <div class="metric-label">{icon} {label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """
