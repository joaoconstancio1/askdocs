# Processo de release de apps mobile

Este documento é um exemplo fictício, escrito para demonstrar o projeto AskDocs.

## Versionamento

Usamos versionamento semântico: MAIOR.MENOR.CORREÇÃO. Uma mudança que quebra a compatibilidade com versões antigas do servidor aumenta o número MAIOR. Uma funcionalidade nova aumenta o MENOR. Uma correção de bug aumenta o número de CORREÇÃO.

O número de build é sempre incrementado a cada envio para as lojas, mesmo quando a versão não muda.

## Fluxo de publicação

Toda publicação começa em uma branch de release criada a partir da main. O pipeline de CI roda os testes, gera os pacotes Android e iOS e envia as builds para os canais de teste interno.

Depois de uma rodada de testes manuais, a equipe promove a build para uma liberação gradual. Começamos com 5% dos usuários, observamos o relatório de falhas por 24 horas e só então ampliamos para 100%.

## Plano de reversão

Se a taxa de falhas passar de 1% nas primeiras 24 horas, pausamos a liberação gradual. Funcionalidades novas ficam atrás de uma configuração remota, então podem ser desligadas sem publicar uma nova versão.
