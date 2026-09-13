# Agente de Comunicação Proativa com Segurados

Protótipo (MVP) de um agente de IA que monitora eventos meteorológicos e gera
comunicações preventivas personalizadas para segurados, simulando o envio 
desenvolvido para o desafio "Ferramenta Inteligente para Comunicação Proativa
com o Segurado" (I2A2).


## Como rodar

1. Crie um ambiente virtual e instale as dependências:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copie `.env.example` para `.env` e preencha suas chaves gratuitas:

   - `OPENWEATHER_API_KEY` — https://home.openweathermap.org/api_keys
   - `GEMINI_API_KEY` — https://aistudio.google.com/app/apikey

   O projeto funciona mesmo sem as chaves (usa dados/mensagens de fallback),
   mas com elas a demonstração fica completa e real.

   Para testar a geração/envio de mensagens sem depender do clima real do
   momento, defina `SIMULAR_EVENTOS_EXTREMOS=true` no `.env` — isso força
   chuva intensa em São Paulo, vento forte em Fortaleza, onda de calor em
   Teresina e granizo em Santos.

3. Rode via linha de comando:

   ```bash
   python main.py
   ```

4. Ou rode o dashboard visual:

   ```bash
   streamlit run app.py
   ```

## Estrutura do projeto

```
agente-seguros-clima/
├── data/segurados.csv        # base fictícia de segurados
├── src/
│   ├── state.py               # modelos de dados (Pydantic)
│   ├── data_loader.py         # carrega a base de segurados
│   ├── weather_collector.py   # agente 1 — coleta (OpenWeatherMap)
│   ├── event_detector.py      # agente 2 — identificação de eventos
│   ├── rules_engine.py        # agente 3 — regras de negócio
│   ├── llm_provider.py        # abstração do LLM (Gemini + fallback)
│   ├── message_generator.py   # agente 4 — geração de mensagens
│   ├── notifier.py            # agente 5 — simulação de envio
│   └── graph.py               # orquestração via LangGraph
├── app.py                     # dashboard Streamlit
├── main.py                    # execução via CLI
└── output/notificacoes_simuladas.json  # gerado a cada execução
```

## Licença

Este projeto está licenciado sob a licença MIT — veja o arquivo [LICENSE](LICENSE)
para mais detalhes.
