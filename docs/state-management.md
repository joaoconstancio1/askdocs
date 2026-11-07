# Gerenciamento de estado em Flutter

Este documento é um exemplo fictício, escrito para demonstrar o projeto AskDocs.

## Por que separar o estado

A interface deve apenas desenhar o que o estado diz. Regras de negócio, chamadas de rede e decisões ficam fora dos widgets. Isso facilita os testes, porque o estado pode ser verificado sem abrir a tela.

## BLoC e Cubit

Um Cubit expõe métodos que emitem novos estados. Um BLoC recebe eventos e os transforma em estados. Usamos Cubit quando a lógica é simples e BLoC quando é preciso tratar sequências de eventos, como cancelar uma busca anterior quando o usuário digita de novo.

Todo estado é imutável. Para mudar algo, emitimos uma cópia nova do estado com o campo alterado.

## Estados de carregamento e erro

Cada tela que depende de dados tem pelo menos quatro estados: inicial, carregando, sucesso e erro. A tela de erro sempre oferece uma ação para tentar de novo. Em conversas com respostas em streaming, o estado de carregamento permanece ativo enquanto chegam partes da resposta.
