# Investing Crawler

Esta aplicação consiste em buscar algumas ingormações do site investing e salva-los em um banco SQLite.

### Dados

1 - Cotações de empresas que compõe o indice IBovespa
2 - Cotações de empresas que compõe o indice da Nasdaq*
3 - Cotação do dolar em relação ao real

*No caso das cotações da Nasdaq, também é salvo o valor em reais baseado na última cotação do dolar.

### Instalação

1 - Executar o build da imagem do docker:
```
docker build -t semantix/crawler .
```

2 - Executar o docker:
```
docker run semantix/crawler
```
3 - A busca ocorrerá a cada 2 minutos, logo após os dados serão exibidos no console.