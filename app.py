import os

from flask import Flask, jsonify, render_template_string
from flask_cors import CORS

from config import Config

from models.call_metrics_model import db

from api.call_metrics_api import call_metrics_bp

app = Flask(__name__)

app.config.from_object(Config)

CORS(app)

# Initialize Database
db.init_app(app)

with app.app_context():
    db.create_all()

# Register API Blueprint
app.register_blueprint(call_metrics_bp)

# Home Route
@app.route("/")
def home():
    return {
        "message": "Backend Running Successfully"
    }


@app.route("/docs")
def docs():
    html = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Clinic Metrics API Docs</title>
        <style>
          :root {
            color-scheme: light;
            --bg: #f6f8fc;
            --panel: rgba(255, 255, 255, 0.92);
            --border: #e3eaf3;
            --text: #10233e;
            --muted: #64748b;
            --primary: #2563eb;
            --success: #059669;
            --code: #0f172a;
          }
          * { box-sizing: border-box; }
          body {
            margin: 0;
            font-family: Inter, Poppins, Segoe UI, Arial, sans-serif;
            background:
              radial-gradient(circle at top left, rgba(37, 99, 235, 0.08), transparent 30%),
              radial-gradient(circle at top right, rgba(124, 58, 237, 0.06), transparent 24%),
              var(--bg);
            color: var(--text);
          }
          .wrap {
            max-width: 1100px;
            margin: 0 auto;
            padding: 32px 20px 48px;
          }
          .hero, .card {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 22px;
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.06);
            backdrop-filter: blur(16px);
          }
          .hero {
            padding: 28px;
            margin-bottom: 18px;
          }
          .eyebrow {
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 12px;
            color: var(--muted);
            font-weight: 700;
            margin-bottom: 10px;
          }
          h1 {
            margin: 0;
            font-size: 34px;
            line-height: 1.1;
          }
          .subtitle {
            margin-top: 10px;
            color: var(--muted);
            font-size: 15px;
            line-height: 1.6;
          }
          .grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 18px;
          }
          .card {
            padding: 22px;
          }
          h2 {
            margin: 0 0 14px;
            font-size: 20px;
          }
          .endpoint {
            display: flex;
            gap: 12px;
            align-items: center;
            padding: 12px 14px;
            border: 1px solid var(--border);
            border-radius: 14px;
            margin-bottom: 10px;
            background: #fff;
          }
          .method {
            font-weight: 800;
            font-size: 12px;
            letter-spacing: 0.06em;
            color: white;
            padding: 6px 10px;
            border-radius: 999px;
            background: var(--primary);
            min-width: 62px;
            text-align: center;
          }
          .method.post { background: var(--success); }
          .method.delete { background: #dc2626; }
          code, pre {
            font-family: Consolas, Monaco, "Courier New", monospace;
          }
          pre {
            margin: 0;
            padding: 14px;
            background: #0f172a;
            color: #e2e8f0;
            border-radius: 14px;
            overflow: auto;
            font-size: 13px;
            line-height: 1.55;
          }
          .muted { color: var(--muted); }
          @media (max-width: 800px) {
            .grid { grid-template-columns: 1fr; }
            h1 { font-size: 28px; }
          }
        </style>
      </head>
      <body>
        <div class="wrap">
          <section class="hero">
            <div class="eyebrow">Clinic Metrics API</div>
            <h1>API Documentation</h1>
            <div class="subtitle">
              This backend powers the dashboard and serves call metrics from the connected database.
              If the database is available, the endpoints below will return live records.
            </div>
          </section>

          <div class="grid">
            <section class="card">
              <h2>Endpoints</h2>
              <div class="endpoint">
                <div class="method">GET</div>
                <div>
                  <div><code>/api/call-metrics</code></div>
                  <div class="muted">List all call metrics.</div>
                </div>
              </div>
              <div class="endpoint">
                <div class="method post">POST</div>
                <div>
                  <div><code>/api/call-metrics</code></div>
                  <div class="muted">Create a new call metric record.</div>
                </div>
              </div>
              <div class="endpoint">
                <div class="method delete">DELETE</div>
                <div>
                  <div><code>/api/call-metrics/&lt;call_id&gt;</code></div>
                  <div class="muted">Delete a call metric by call ID.</div>
                </div>
              </div>
            </section>

            <section class="card">
              <h2>OpenAPI</h2>
              <div class="muted" style="margin-bottom: 12px;">
                You can fetch the schema as JSON:
              </div>
              <pre>{
  "openapi": "3.0.0",
  "paths": {
    "/api/call-metrics": {
      "get": {},
      "post": {}
    },
    "/api/call-metrics/{call_id}": {
      "delete": {}
    }
  }
}</pre>
            </section>
          </div>
        </div>
      </body>
    </html>
    """
    return render_template_string(html)


@app.route("/openapi.json")
def openapi():
    return jsonify(
        {
            "openapi": "3.0.0",
            "info": {
                "title": "Clinic Metrics API",
                "version": "1.0.0",
            },
            "paths": {
                "/api/call-metrics": {
                    "get": {
                        "summary": "List call metrics",
                    },
                    "post": {
                        "summary": "Create a call metric",
                    },
                },
                "/api/call-metrics/{call_id}": {
                    "delete": {
                        "summary": "Delete a call metric by call ID",
                    }
                },
            },
        }
    )

# Run Server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"

    app.run(host="0.0.0.0", port=port, debug=debug)
