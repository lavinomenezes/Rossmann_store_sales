# Rossmann Store Sales


## Problema de negócio

Rossmann é uma rede de drogarias com mais de 50 anos de atuação e que conta com mais de 4000 lojas espalhadas em 7 países europeus. Para planejar e custear o orçamento para  reforma dessas lojas o CFO requisitou para a equipe de dados uma previsão de faturamento de cada loja nas próximas 6 semanas.Será entregue uma lista contendo a previsão de vendas de cada uma das lojas no conjunto de dados, esses valores também poderão ser acessados por um chatbot no aplicativo de mensagens Telegram.



**Dataset overview**


| **Variable** | **Meaning** |
|:----------:|---------|
|id| an Id that represents a (Store, Date) duple within the test set|
|Store|a unique Id for each store|
|Sales|the turnover for any given day (this is what you are predicting)|
|Customers|the number of customers on a given day|
|Open | an indicator for whether the store was open: 0 = closed, 1 = open |
|StateHoliday | indicates a state holiday. Normally all stores, with few exceptions, are closed on state holidays. Note that all schools are closed on public holidays and weekends. a = public holiday, b = Easter holiday, c = Christmas, 0 = None|
|SchoolHoliday | indicates if the (Store, Date) was affected by the closure of public schools |
|StoreType | differentiates between 4 different store models: a, b, c, d|
|Assortment | describes an assortment level: a = basic, b = extra, c = extended |
|CompetitionDistance | distance in meters to the nearest competitor store|
|CompetitionOpenSince(Month/Year) | gives the approximate year and month of the time the nearest competitor was opened|
|Promo | indicates whether a store is running a promo on that day|
|Promo2 | Promo2 is a continuing and consecutive promotion for some stores: 0 = store is not participating, 1 = store is participating|
|Promo2Since(Year/Week) | describes the year and calendar week when the store started participating in Promo2|
|PromoInterval | describes the consecutive intervals Promo2 is started, naming the months the promotion is started anew. E.g. "Feb,May,Aug,Nov" means each round starts in February, May, August, November of any given year for that store|



##  Questões do negócio

Previsão de vendas para as próximas 6 semanas de cada loja para que o valor previsto possa ser usado para programar reformas nas unidades.


##  Premissas do negócio

<ul>
<li>A variedade do tipo de lojas “Store Type” e do sortimento  “assortment” não está balanceadas e isso num momento inicial pode mascarar o comportamento das vendas totais quando comparadas as categorias;
</li>
<li>A lista final contará apenas com lojas que estavam abertas (open == 1) e que tiveram vendas (sales >0). Assim, é possível que uma loja específica, quando solicitada, não tenha resposta dos valores;

</li>
<li>As informações estão limitadas numa faixa de 3 anos indo de janeiro de 2013 até julho de 2015;

</li>
<li>Como o ano de 2015 está incompleto, a comparação de vendas de datas e feriados entre os anos apresenta comportamento diferente;
</li>
<li>Quando a loja não possui informação de distância pro competidor mais próximo “competition_distance” foi definido o valor de 200.000 metros para simular que a loja não possui competidores próximos.
</li>
</ul>

## Planejamento da Solução

Neste projeto foi aplicado o método CRISP-DM (Cross-Industry Standard Process for Data Mining) adaptado para os processos de ciência de dados que se tornou o CRIS-DS.

A divisão dos passos utilizados no projeto foi:

<ol>
<li><strong>Entendimento de negócio:</strong> Entender um pouco mais sobre a rede de lojas Rossmann e discutir o que motivou a requisição da previsão de vendas, assim, entendendo melhor o problema para apresentar a solução mais eficiente no menor tempo possível.
</li>
<li>
<strong>Coleta de dados:</strong> Todos os dados estavam disponíveis na plataforma kaggle, sendo esta disponibilizada pela própria empresa.
</li>
<li>
<strong>Análise descritiva:</strong> uma breve análise dos dados para adquirir familiaridade com os mesmo, incluindo o tamanho do data frame que estamos lidando assim como os tipo de dados que vamos processar, aplicando estatística descritiva sobre as informações para conhecer o comportamento dela.   
</li>
<li>
<strong>Dados faltantes:</strong> Com a análise descritiva encontrar e preencher dados de colunas que estejam em falta, tomando essas decisões baseados na importância da informação e derivando alguns dados de outras colunas.    
</li>
<li>
<strong>Feature engineering:</strong> criação de novos atributos derivados dos que já existiam para ajudar a ter uma melhor compreensão do comportamento dos dados e para melhorar o desempenho dos modelos de machine learning. os atributos criados foram:
    <ul>
    <li>Year;</li>
    <li>month;</li>
    <li>day;</li>
    <li>week_of_year;</li>
    <li>year_week;</li>
    <li>competition_since;</li>
    <li>Competition_time_month;</li>
    <li>promo_since;</li>
    <li>season;</li>
    <li>promo_time_week.</li>
</ul>
</li>

<li>
<strong>Filtragem de dados:</strong> Remoção de colunas que não tem impacto no modelo e as que foram criadas como auxiliares no processo de feature engineering. Remoção de linhas que não contribuem com o modelo. Sendo eles:
<ul>
        <li>Colunas removidas: 'customers','open','promo_interval', 'month_map'</li>
        <li>Linhas removidas: Lojas que não estão abertas (open==0)  e aquelas que apresentaram vendas no valor de zero ( sales<0) </li>
</ul>
</li>
<li>
<strong>Análise exploratória de dados:</strong> Criar e validar hipóteses de negócio para melhor entendimento do comportamento dos dados em relação a variável alvo e como elas se influenciam, e definir quais atributos são importantes para o modelo.
</li>
<li>
<strong>Preparação dos dados:</strong> Manipular os dados para se adequarem melhor num modelo de machine learning, 
<ul>
<li>Aplicando a normalização na variável target “sales” para aproximar sua distribuição da normal;</li>
<li>Re-escala dos atributos numéricos para não força o modelo a trabalhar com valores muito altos;</li>
<li>Encoding das variáveis categorias. por fim para atributos cíclicos como dia e dia da semana entre outros apliquei transformação de natureza cíclica. </li>
</ul>
</li>
<li>
<strong>Feature selection:</strong> Neste primeiro ciclo do CRISP foi utilizado o algoritmo boruta para definir os atributos que iremos utilizar no treinamento.
</li>
<li>
<strong>Modelos de machine learning:</strong> Nesta etapa foram aplicados quatro algoritmos de machine learning para definir qual tinha melhor resultados e se adequa melhor ao comportamento dos dados. Sendo eles:
    <ul>
    <li>Linear regression Model;
    <li>Linear Regression Regularized Model - Lasso;</li>
    <li>Random Forest Regressor;</li>
    <li>XGboost Regressor.</li>
</ul>
</li>
<li>
<strong>Fine tuning:</strong> após a escolha do modelo foi aplicado o random search para encontrar os melhores parâmetros do modelo de machine learning.
</li>
<li>
    <strong>Deploy:</strong> Nesta última etapa, já tendo aplicado o modelo final no dataset e observado os valores gerados, o modelo foi colocado em produção online na plataforma heroku, utilizando uma API desenvolvido com a biblioteca Flask para que o CFO da empresa possa ter a qualquer momento os valores de previsão de cada loja por meio de um bot no aplicativo de mensagens Telegram.
</li>
</ol>

##  Os  principais insights de negócio

<h3><strong>Lojas com competidores com até 1000 metros de distância representam 33,26 % das vendas</strong> </h3>

![](https://github.com/lavinomenezes/Rossmann_store_sales_project/blob/main/images/Screenshot_2.png)

Com esse número diminuindo conforme a distância aumenta, ou seja, quanto mais perto competidores maiores são as vendas.

Provavelmente pelo fato de lojas geralmente serem construídas em centros de consumo, consequentemente existe a presença de mais competidores e as lojas que não possuem concorrência próxima devem estar em locais de baixo consumo. é necessário dados geográficos para ir mais afundo nessa conclusão. 
<h3><strong> Lojas com um certo período de venda vendem menos após um período de promoção.</strong></h3> 

Esse fenômeno pode ser causado por dois principais motivos:
<ul>
<li>Devido a promoção os clientes já compraram o necessário para se manterem abastecidos por um maior período de tempo </li>
<li>Devido a promoção se estender por muito tempo o preço promocional se torna o padrão, subjetivamente, diminuindo o interesse em adquirir o produto.</li>
</ul>

<h3><strong>Lojas com mais promoções consecutivas vendem menos</strong></h3>

![](https://github.com/lavinomenezes/Rossmann_store_sales_project/blob/main/images/Screenshot_1.png)

Provavelmente ocorre pelos mesmo motivos da hipótese anterior.


<h3><strong>Imóveis em más condições são mais baratos que aqueles em boas condições</strong></h3>

Imóveis em más condições são em média 66.64 % mais baratos em comparação àqueles em boas condições, então podem ser adquiridos com um baixo investimento e reformados para revenda mantendo um bom lucro.


<i>Todas as hipóteses testadas podem ser vistas no [notebook](https://github.com/lavinomenezes/House_rocket_insight_project/blob/main/notebooks/House_rocket_notebook.ipynb) para ver a descrição total, ou um breve resumo em [Hipóteses](https://github.com/lavinomenezes/House_rocket_insight_project/blob/main/Hipoteses.md)</i>

## Resultados financeiros


Existe um total de 21.461 imóveis disponíveis para compra, de cujo montante 10.498 foram sugeridos para compra. A tabela abaixo descreve os valores resultantes da análise.



| Imóveis dispóniveis | Sugestões para compra | Investimento | Retorno | Lucro |
|:----------------------:|:--------------------:|:-------------:|:--------:|:--------:|
| 21,461 | 10,498 | $5,656,988,504.00 | $6,622,652,682.20 | $965,664,178.2 |




##  Conclusão

Neste projeto foram selecionados imóveis para compra e sugeridos preços de revenda. Também foram testadas hipóteses para entender melhor o comportamento dos preços e o resultado foi entregue para o CEO. A lista de sugestões, assim como os testes dos <i>insights</i> acima descritos, estão disponíveis online em [House rocket insight report](https://house-rocket-insight-report.herokuapp.com/) para serem acessados pelo CEO ou qualquer outro membro da empresa que venha a quem as informações interessem.


Caso tenha interrese no processo completo de tratamnto e análise de dados, pode ser encontrado em: [Python do zero ao DS](https://github.com/lavinomenezes/Python_do_zero_ao_DS)





##  Próximos passos

<ul>
<li>Aumentar a quantidade de informações relevantes sobre os imóveis;
</li>
<li>Explorar mais a fundo as hipóteses promissoras; 
</li>
<li>Testar novas hipóteses;</li>
<li>Explorar modelos de <i>machine learning</i> para prever o comportamento dos preços dos imóveis</li>
</ul>


## Ferramentas utilizadas

<ul>
<li>Jupyter notebook</li>
    <li>Pycharm communit</li>
<li>Python</li>
<li>Pandas</li>
    <li>Seaborn</li>
<li>Streamlit</li>
    <li>Heroku</li>
    <li>Git</li>
</ul>
