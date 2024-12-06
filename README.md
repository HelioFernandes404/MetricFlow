# MetricFlow

**MetricFlow** é um projeto que integra **VictoriaMetrics**, **Python** e **Grafana** para criar um sistema de monitoramento eficiente e escalável.

## Descrição

Este projeto foi desenvolvido para explorar e demonstrar a utilização do VictoriaMetrics, um banco de dados de séries temporais de alto desempenho e escalabilidade. Utilizando Python para coleta de métricas e Grafana para visualização, o MetricFlow oferece uma solução completa para monitoramento de sistemas.

## Funcionalidades

- Coleta de métricas personalizadas utilizando scripts em Python.
- Armazenamento eficiente de dados temporais com o VictoriaMetrics.
- Visualização interativa de métricas através de dashboards no Grafana.

## Requisitos

- Docker e Docker Compose instalados na máquina.
- Conhecimentos básicos em Python.

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/HelioFernandes404/MetricFlow.git
   ```

2. **Navegue até o diretório do projeto:**

   ```bash
   cd MetricFlow
   ```

3. **Inicie os serviços com Docker Compose:**

   ```bash
   docker-compose up -d
   ```

   Este comando iniciará os contêineres do VictoriaMetrics e do Grafana.

## Configuração

1. **Configurar o Grafana:**

   - Acesse o Grafana em `http://localhost:3000`.
   - Adicione o VictoriaMetrics como fonte de dados:
     - URL: `http://victoriametrics:8428`
   - Importe os dashboards disponíveis no diretório `grafana_dashboards` do projeto.

2. **Executar scripts de coleta de métricas:**

   - No diretório `scripts`, execute os scripts Python para coletar e enviar métricas para o VictoriaMetrics.

## Uso

- Após a configuração, utilize o Grafana para visualizar as métricas coletadas em tempo real.
- Personalize os dashboards conforme necessário para atender às necessidades específicas de monitoramento.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).