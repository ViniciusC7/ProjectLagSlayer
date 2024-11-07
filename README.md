# LAG SLAYER PRO

**LAG SLAYER** é um programa desenvolvido em Python para otimizar a conexão de rede em sistemas Windows, focado principalmente em reduzir a latência e melhorar a estabilidade em jogos online e atividades que exigem uma conexão de internet rápida e consistente, como downloads e streaming.

##  Funcionalidades

- **Otimização para Jogos Online**: Ajustes na configuração de rede para reduzir o lag e a latência em jogos online.
- **Otimização para Downloads e Streaming**: Melhoria nas configurações de rede para aumentar a velocidade de download e a qualidade de streaming.
- **Configuração Manual do MTU**: Permite que o usuário defina manualmente o valor do MTU (Maximum Transmission Unit) ou use a detecção automática do valor ideal.
- **Configurações de QoS e TCP**: Ajustes para otimizar a qualidade de serviço (QoS) e desativar o Algoritmo de Nagle, aumentando a responsividade da conexão.
- **Visualização das Configurações Atuais**: Mostra as configurações atuais de rede, estatísticas de pacotes, latência e perda de pacotes.

##  Como Funciona

O **LAG SLAYER** realiza alterações nas configurações de rede, incluindo:
- Ajuste automático do MTU para o valor ideal.
- Configurações TCP para melhorar a estabilidade e a capacidade de resposta.
- Ativação da QoS para priorizar pacotes de rede.
- Desativação do Algoritmo de Nagle, que pode reduzir a latência em conexões sensíveis ao tempo, como jogos online.

> **Nota**: O programa precisa ser executado com privilégios de administrador para aplicar algumas otimizações.

##  Tecnologias Utilizadas

- **Python**: Linguagem principal.
- **Tkinter**: Biblioteca para a criação da interface gráfica.
- **Psutil**: Usada para monitorar e exibir estatísticas de rede.
- **Subprocess**: Para executar comandos de rede diretamente no sistema.





<!--# *Project LagSlayer*
**Project LagSlayer** é uma ferramenta para otimizar configurações de rede em sistemas Windows, focada em reduzir a latência para melhorar a performance em jogos e outras aplicações que exigem baixa latência. A ferramenta permite otimizar o DNS e o MTU e também restaurar as configurações originais caso seja necessário.

------------

<!--
###   Funcionalidades
- Otimização de Configurações de Rede: Configura automaticamente o DNS e o MTU para valores ideais, reduzindo a latência.
- Restaurar Configurações Originais: Reverte as configurações de DNS e MTU para os valores anteriores.
- Interface Simples: Um menu interativo permite selecionar opções diretamente no terminal.

------------


<!--###   Como Funciona
1. **Backup:** Ao iniciar o programa, ele armazena as configurações atuais de DNS e MTU.

1. **Otimização:** Define o DNS para 8.8.8.8 e o MTU para 1500, valores que podem reduzir a latência em algumas redes.

1. **Restauração:** Caso deseje reverter as alterações, o programa restaura as configurações salvas no backup inicial.
-->

<!--> ###  Aviso
<!--> Este programa modifica configurações de rede. Recomenda-se o uso apenas para quem entende os efeitos das alterações no DNS e MTU.
