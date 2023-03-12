# Project

<h4 align="center"> 
	🚧  Projeto ⚙️ Em construção...  🚧
</h4>

Tabela de conteúdos
=================
<!--ts-->
   * [Sobre](#sobre)
   * [Tecnologias](#tecnologias)
   * [Apis](#apis)
      * [Api do vendedor](#company)
      * [Api do cliente](#consumer)
      * [Api de pagamentos](#payment)
      * [Api administrativa](#adm)
      * [Api de consumo geral](#public)
      * [Models](#register)
   * [Contribuição](#contribuição)
   * [Autor](#autor)
<!--te-->

## Sobre
  O Projeto foi desenvolvido usando a arquitetura de micro-serviços pois esta arquitetura facilita a manutenção e combinada com CI/CD e kubernetes entrega atualizações para o cliente final sem que o mesmo seja afetado enquanto usa a plataforma.

## Tecnologias
  - Django
  - Docker
  - Kubernetes
  - Github actions

## Apis

### Company
#### Api que contém todos os endpoint usados exclusivamente pelo vendedor.
---
#### Features
	- [x] Cadastrar nova empresa
	- [x] Criar novo produto
	- [ ] Editar produtos
	- [x] Criar funcionários 
### Consumer
#### Api que contém todos os endpoint usados exclusivamente pelo consumidor final.
---
#### Features
	- [x] Criação de cadastro
	- [x] Alteração de senha
	- [x] Pesquisa por um produto específico 
	- [x] Pesquisa pro produtos 
	- [x]Criação de lista de desejos
	- [x] Avaliação do produto
	- [x] Adicionar item no carrinho
	- [x] Remover item do carrinho

### Payment
#### Api que contém todos os endpoint usados exclusivamente para pagamentos.
---
#### Features
	- [ ] Gerar qr code de pagamento
	- [ ] Pagamento por pix
	- [ ] Pagamento com cartão de crédito
	- [ ] Pagamemnto por boleto
	- [ ] Assinatura recorrente
	- [ ] Consulta de pagamentos realizados
	- [ ] Consulta de pagamento indivídual
	- [ ] Cancelamento de assinaturas

### Adm
#### Api usada pelos desenvolvedores e suporte.
---
#### Features
	- [x] Concede permissão a usuários
	- [x] Remove permissão de usuários
	- [x] Adiciona novos estados
	- [x] Adiciona novas cidades
	- [x] Deleta contas
	- [x] Cria subcategorias
	- [x] Cria categorias para empresas
	- [x] Cria categorias para produtos
	- [x] Cria permissões
	- [x] Cria premissões para empresas
	- [x] Criar usuário com acesso staff

### Public
#### Api de uso comum.
---
#### Features
	- [x] Login
	- [x] Logout
	- [x] Logs

### Register
#### Modelos do banco de dados e autenticações de backend.


## Contribuição
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/BrunoTumelero/Projeto_dev/issues)

## Licença
[![License](https://img.shields.io/badge/License-Apache_2.0-_red.svg)](https://opensource.org/licenses/Apache-2.0)

## Autor

 <sub><b>Bruno Tumelero</b></sub>


Feito com ❤️ por Bruno Tumelero 👋🏽 Entre em contato!

[![Linkedin Badge](https://img.shields.io/badge/-Bruno-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/tgmarinho/)](https://www.linkedin.com/in/bruno-tumelero/) 
[![Outlook Badge](https://img.shields.io/badge/email--000?style=social&logo=microsoft-outlook&logoColor=0078d4&link=mailto:Bruno.Tumelero@outlook.com)](mailto:Bruno.Tumelero@outlook.com)
