FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    streamlit==1.35.0 \
    plotly==5.22.0 \
    pandas==2.2.2 \
    google-generativeai==0.8.3

COPY frontend/ ./frontend/

EXPOSE 8080

CMD ["streamlit", "run", "frontend/app.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true", "--theme.base=dark", "--browser.gatherUsageStats=false"]
