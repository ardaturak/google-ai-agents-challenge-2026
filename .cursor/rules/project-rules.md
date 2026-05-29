# PRONUVE Water Intelligence — Challenge Kuralları ve Standartları
# Bu dosya projenin tüm kararlarını yönetir

## Proje Bilgisi
- Proje: PRONUVE Water Intelligence Agent
- Challenge: Google for Startups AI Agents Challenge (Track 1 - Build)
- Takım: ProgenX + PRONUVE
- Deadline: 5 Haziran 2026, 17:00 PT (6 Haziran 03:00 TR)

## Teknik Kurallar

### Zorunlu Teknolojiler
- Google Agent Development Kit (ADK) — Python
- Gemini modelleri (2.5 Flash veya Pro)
- Google Cloud Run (deploy)
- MCP (Model Context Protocol) — en az 2 dış araç
- BigQuery (veri katmanı)

### Kod Standartları
- Python 3.12+
- Type hints zorunlu
- Docstring her public fonksiyonda
- Pydantic modelleri (schema validation)
- Async/await tercih edilecek
- Her agent kendi dosyasında

### Güvenlik Kuralları
- .env dosyaları ASLA commit edilmeyecek
- Gerçek ASKİ endpoint'leri kod'da olmayacak
- Park isimleri anonimleştirilecek (Park Alpha, Beta, Gamma...)
- Koordinatlar generic olacak (Ankara genel bölge)
- Abone numaraları rastgele ID'ler olacak
- Tüketim değerleri gerçek PATTERN'i koruyacak ama ±%10-20 noise eklenecek

### Agent Mimarisi Kuralları
- Minimum 7 agent
- Her agent tek sorumluluk (Single Responsibility)
- Agent'lar arası iletişim tool_context.state üzerinden
- Root agent orkestratör rolünde
- SequentialAgent + ParallelAgent + LoopAgent pattern'leri zorunlu
- Human-in-the-Loop en az 1 noktada

### Repo Yapısı
- README.md — İngilizce, net, kurulum adımları
- Architecture diagram — docs/ klasöründe PNG
- requirements.txt — pinned versions
- Dockerfile — Cloud Run ready
- .env.example — gerekli env var'lar (değersiz)
- data/ — anonimleştirilmiş örnek veri
- tests/ — en az birkaç unit test

### Demo Kuralları
- Video 3-5 dakika, İngilizce
- Agent'ın gerçek zamanlı çalışmasını göster
- Terminal/log output göster (agent'lar arası iletişim)
- Anomali tespiti → alert akışını uçtan uca göster
- "Real data from municipal parks in Turkey" de
