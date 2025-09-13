available_languages = {
    'English': 'en',
    'Português': 'pt',
    'Français': 'fr'
}

main = {
    "error": {
        'en': """
# We are sorry...

It looks like our servers are not working right now.

Try to refresh the page in a few moments.
""",
        'pt': """
# Nos desculpe...

Parece que nossos servidores não estão funcionando no momento.

Tente recarregar a página em alguns instantes.
""",
        'fr': """
# Nous sommes désolés…

Il semble que nos serveurs ne fonctionnent pas pour le moment.

Veuillez essayer de recharger la page dans quelques instants.
"""
    },
    "choose_country": {
        'en': """
# Welcome to the :green[Home Estimate AI]! A :blue[Machine Learning] Real Estate Evaluator!

## In this app, you can :red[evaluate properties] from various cities around the world!
            
### Start by choosing a **country**:
""",
        'pt': """
# Bem-vindos ao :green[Home Estimate AI]! Um avaliador de imóveis baseado em :blue[Machine Learning].

## Neste site, você pode :red[avaliar propriedades] de diversas cidades do mundo!

### Comece escolhendo um país:
""",
        'fr': """
# Bienvenue sur :green[Home Estimate AI]! Un évaluateur de biens immobiliers basé sur le :blue[Machine Learning].

## Sur ce site, vous pouvez :red[évaluer des propriétés] dans différentes villes du monde!

### Commencez par choisir un pays :
"""
    },
    "choose_city": {
        'en': """### Choose a **city**:""",
        'pt': """### Escolha uma **cidade**:""",
        'fr': """### Choisissez une ville:"""
    },
    "choose_location": {
        'en': """### Select the property's location on the map""",
        'pt': """### Indique a localização do seu imóvel:""",
        'fr': """### Sélectionnez l'emplacement de la propriété sur la carte"""
    },
    "fill_form": {
        'en': """### Fill the details of your property:""",
        'pt': """### Preencha as informações do seu imóvel:""",
        'fr': """### Remplissez les détails de votre propriété :"""
    },
    "button_form": {
        'en': """Evaluate My Property""",
        'pt': """Avaliar Minha Propriedade""",
        'fr': """Évaluer ma propriété"""
    },
    "no_coords": {
        'en': """Choose the property's location on the map""",
        'pt': """Aponte a localização do imóvel no mapa""",
        'fr': """Indiquez l'emplacement du bien sur la carte"""
    },
}

results = {
    "error": {
        'en': """
# We are sorry…

It seems something went wrong.

Please try making your prediction again.
""",
        'pt': """
# Nos desculpe...

Parece que algo deu errado.

Por favor tente fazer sua avaliação novamente.
""",
        'fr': """
# Nous sommes désolés…

Il semble qu'une erreur soit survenue.

Veuillez réessayer d'évaluer votre propriété.
"""
        },
    "evaluation": {
        'en': """The estimate value of your property is :green[$ {value:,.0f}].""",
        'pt': """O valor estimado da sua propriedade é :green[$ {value:,.0f}].""",
        'fr': """La valeur estimée de votre propriété est :green[$ {value:,.0f}]."""
    },
    "range_text": {
        'en': """### The ***predicted price range*** below is suggested by the model.""",
        'pt': """### A ***faixa de preços*** sugerida pelo modelo está mostrado abaixo.""",
        'fr': """### La ***fourchette de prix*** suggérée par le modèle est indiquée ci-dessous."""
    },
    "range_limit_min": {
        'en': """Lowest""",
        'pt': """Mínimo""",
        'fr': """Minimum"""
    },
    "range_limit_avg": {
        'en': """Suggested""",
        'pt': """Sugerido""",
        'fr': """Suggéré"""
    },
    "range_limit_max": {
        'en': """High""",
        'pt': """Alta""",
        'fr': """Maximum"""
    },
    "mape_eval_high": {
        'en': """The MAPE of this model is :red[{mape}%] wich is considered :red[HIGH].""",
        'pt': """O MAPE deste modelo é :red[{mape}%], o que consideramos :red[ALTO].""",
        'fr': """"L'EMAPE de ce modèle est de :red[{mape}%], ce qui est considéré comme :red[ÉLEVÉ]."""
    },
    "mape_eval_avg": {
        'en': """The MAPE of this model is :orange[{mape}%] wich is considered :orange[MEDIUM].""",
        'pt': """O MAPE deste modelo é :orange[{mape}%], o que consideramos :orange[MÉDIO].""",
        'fr': """L'EMAPE de ce modèle est de :orange[{mape}%], ce qui est considéré comme :orange[MOYEN]."""
    },
    "mape_eval_low": {
        'en': """The MAPE of this model is :green[{mape}%] wich is considered :green[LOW].""",
        'pt': """O MAPE deste modelo é :green[{mape}%], o que consideramos :green[BAIXO].""",
        'fr': """L'EMAPE de ce modèle est de :green[{mape}%], ce qui est considéré comme :green[FAIBLE]."""
    },
    "about_estimator_title": {
        'en': """🏠 About Our Estimator""",
        'pt': """🏠 Sobre a estimativa""",
        'fr': """🏠 À propos de l'estimation"""
    },
    "about_estimator_text": {
        'en': """
This tool provides an **estimated property price** based on historical data and 
machine learning predictions. The model may include errors and uncertainties.
Use this information as a reference point only. We recommend consulting 
additional sources or professionals before making decisions.

### 📉 About the range
The price range is calculated considering the model performance index called
**MAPE (Mean Absolute Percentage Error)**.

#### ***But what is MAPE?***

Mape is a statistical indicator that measures how wrong our model is on average.
A MAPE of **10%**, for example, means that the predictions are, on average, 
within **10% of the true price**.  The :orange[smaller] the MAPE, the more 
:orange[reliable] the estimate.

{mape_evaluation}
""",
        'pt': """
Esta ferramenta fornece um **preço estimado do imóvel** com base em dados históricos e 
previsões de aprendizado de máquina. O modelo pode conter erros e incertezas.
Use essas informações apenas como referência. Recomendamos consultar 
fontes adicionais ou profissionais antes de tomar quaisquer decisões.

### 📉 Sobre a faixa de preços
A faixa de preços é calculada considerando o índice de desempenho do modelo chamado
**MAPE (Erro Percentual Absoluto Médio)**.

#### ***Mas o que é o MAPE?***

O MAPE é um indicador estatístico que mede, em média, quão errado nosso modelo está.
Um MAPE de **10%**, por exemplo, significa que as previsões estão, em média, 
dentro de **10% do preço real**. Quanto menor o :orange[MAPE], mais 
:orange[confiável] é a estimativa.

{mape_evaluation}
""",
        'fr': """
Cet outil fournit un **prix estimé de la propriété** basé sur des données historiques et 
des prédictions de machine learning. Le modèle peut comporter des erreurs et des incertitudes.
Utilisez ces informations uniquement comme point de référence. Nous recommandons de consulter 
des sources supplémentaires ou des professionnels avant de prendre des décisions.

### 📉 À propos de la fourchette de prix
La fourchette de prix est calculée en tenant compte de l'indice de performance du modèle appelé
**MAPE (Erreur Pourcentage Absolue Moyenne)**.

#### ***Mais qu'est-ce que le MAPE ?***

Le MAPE est un indicateur statistique qui mesure en moyenne à quel point notre modèle se trompe.
Un MAPE de **10%**, par exemple, signifie que les prédictions sont, en moyenne, 
dans un rayon de **10% du prix réel**. Plus le :orange[MAPE] est petit, plus 
:orange[fiable] est l'estimation.

{mape_evaluation}
"""
    },
    "about_creators_title": {
        'en': """👤 About the creators""",
        'pt': """👤 Sobre os criadores""",
        'fr': """👤 À propos des créateurs"""
    },
    "about_creators_Marcus_text": {
        'en': """
### Project
This application was created and is maintained by 
[Marcus Zucareli](https://www.linkedin.com/in/marcus-zucareli/). It is part of 
an [open source project](https://github.com/marcuszucareli/house-price-app) 
and also includes an [API](https://api.home-estimate-ai.uk/docs).
            
It was developed as the final project of the 
[USP Data Science and Analytics MBA](https://mbauspesalq.com/en) and released 
as Open Source.

You can reach me at:

🌐 [Linkedin](https://www.linkedin.com/in/marcus-zucareli/?locale=en_US) | 
💻 [GitHub](https://github.com/marcuszucareli) | 
📱 [WhatsApp](https://wa.me/33745153017) | 
✉️ [papaulozucareli@gmail.com](mailto:papaulozucareli@gmail.com) | 
📞 +33 7 45 15 30 17
""",
        'pt': """
### Projeto
Essa aplicação foi criada e é mantida por  
[Marcus Zucareli](https://www.linkedin.com/in/marcus-zucareli/). Ela é parte de 
 um [projeto open source](https://github.com/marcuszucareli/house-price-app) 
que também inclui uma [API](https://api.home-estimate-ai.uk/docs).
            
Ela foi desenvolvida como trabalho de conclusão de curso para o
[MBA em Data Science e Analytics da USP ](https://mbauspesalq.com/en) e foi
publicada como Open Source.

Você pode me contatar por aqui:

🌐 [Linkedin](https://www.linkedin.com/in/marcus-zucareli/?locale=en_US) | 
💻 [GitHub](https://github.com/marcuszucareli) | 
📱 [WhatsApp](https://wa.me/33745153017) | 
✉️ [papaulozucareli@gmail.com](mailto:papaulozucareli@gmail.com) | 
📞 +33 7 45 15 30 17
""",
        'fr': """
### Projet
Cette application a été créée et est maintenue par [Marcus Zucareli](https://www.linkedin.com/in/marcus-zucareli/). Elle fait partie d'un 
[projet open source](https://github.com/marcuszucareli/house-price-app) 
qui inclut également une [API](https://api.home-estimate-ai.uk/docs).

Elle a été développée comme projet de fin d'études pour le
[MBA en Data Science et Analytics de l'USP](https://mbauspesalq.com/en) et a été
publiée en tant que Open Source.

Vous pouvez me contacter ici :

🌐 [Linkedin](https://www.linkedin.com/in/marcus-zucareli/?locale=en_US) | 
💻 [GitHub](https://github.com/marcuszucareli) | 
📱 [WhatsApp](https://wa.me/33745153017) | 
✉️ [papaulozucareli@gmail.com](mailto:papaulozucareli@gmail.com) | 
📞 +33 7 45 15 30 17
"""
    },
    "about_creators_model": {
        'en': """
### Model
The model used to compute your prediction was created by {author}.

Check their links:
""",
        'pt': """
### Modelo
O modelo usado para calcular o preço do imóvel foi criado por {author}.

Confira seus links:
""",
        'fr': """
### Modèle
Le modèle utilisé pour calculer le prix de la propriété a été créé par {author}.

Consultez ses liens:
"""
    },
    "home_button": {
        'en': """Home""",
        'pt': """Início""",
        'fr': """Accueil"""
    },
}