# Noções básicas de segurança em apps

Este documento é um exemplo fictício, escrito para demonstrar o projeto AskDocs.

## Armazenamento de credenciais

Tokens de acesso nunca ficam em arquivos de texto simples. No Android usamos o armazenamento seguro do sistema e no iOS o chaveiro. Chaves de API não devem ser colocadas dentro do aplicativo, porque o pacote pode ser aberto e lido.

## Comunicação com o servidor

Toda comunicação usa HTTPS. Em telas sensíveis, como pagamento, a equipe pode fixar o certificado do servidor para impedir interceptação.

## Autenticação

O login usa um provedor de identidade externo. O aplicativo guarda um token de curta duração e um token de renovação. Quando o token de acesso expira, o aplicativo renova em segundo plano. Se a renovação falhar, o usuário volta para a tela de login.

## Dados pessoais

Coletamos apenas o necessário. Logs de erro não podem conter documentos, e-mails ou números de telefone. Antes de enviar um relatório de falha, os campos sensíveis são removidos.
