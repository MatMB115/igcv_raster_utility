# Documentação - IGCV Raster Utility

## Bem-vindo à Documentação Completa

Esta pasta contém a documentação técnica completa do projeto **IGCV Raster Utility**, uma aplicação desktop para processamento, visualização e exportação de dados raster multiespectrais.

## Começando

### Para Usuários
Se você é um usuário final, comece por:
- **[Índice da Documentação](indice.md)** - Visão geral de todos os documentos
- **[README Principal](../README.MD)** - Informações básicas sobre o projeto

### Para Desenvolvedores
Se você é um desenvolvedor ou contribuidor, recomendamos:
- **[Guia de Desenvolvimento](desenvolvimento.md)** - Como contribuir e estender o projeto
- **[Arquitetura do Sistema](arquitetura.md)** - Entendimento da estrutura do código

## Documentos Disponíveis

### Arquitetura e Design
- **[Arquitetura do Sistema](arquitetura.md)** - Padrão MVC, fluxo de dados, princípios de design
- **[Processamento de Dados Raster](processamento_raster.md)** - Operações principais, otimizações, metadados

### Interfaces de Usuário
- **[Interfaces de Usuário](interface_usuario.md)** - GUI e CLI detalhadas, comparações, usabilidade

### Desenvolvimento
- **[Guia de Desenvolvimento](desenvolvimento.md)** - Padrões de código, testes, extensibilidade, compilação de executáveis

### Planejamento
- **[Roadmap de Desenvolvimento](roadmap.md)** - Fases de desenvolvimento, priorizações, cronogramas

### Referência
- **[Índice da Documentação](indice.md)** - Navegação completa e referência rápida

## Estrutura da Documentação

```
docs/
├── README.md                    # Este arquivo
├── indice.md                    # Índice e navegação
├── arquitetura.md               # Arquitetura do sistema
├── processamento_raster.md      # Processamento de dados
├── interface_usuario.md         # Interfaces GUI e CLI
├── desenvolvimento.md           # Guia para desenvolvedores
└── roadmap.md                   # Planejamento futuro
```

## Manutenção da Documentação

### Princípios
- **Atualização contínua** com o desenvolvimento
- **Clareza e simplicidade** na comunicação
- **Exemplos práticos** sempre que possível
- **Consistência** na formatação e estilo

### Responsabilidades
- **Desenvolvedores**: Atualizar documentação técnica
- **Mantenedores**: Revisar e organizar documentação
- **Usuários**: Reportar lacunas ou inconsistências

### Processo de Atualização
1. **Identificar necessidade** de atualização
2. **Modificar documento** relevante
3. **Revisar consistência** com outros documentos
4. **Atualizar índice** se necessário
5. **Comunicar mudanças** à comunidade

## Contribuindo para a Documentação

### Como Contribuir
1. **Identificar** área que precisa de melhoria
2. **Propor** mudanças via issue ou pull request
3. **Seguir** padrões de formatação Markdown
4. **Incluir** exemplos práticos quando relevante
5. **Revisar** consistência com outros documentos

### Padrões de Formatação
- **Markdown** como formato principal
- **Organização visual** clara e consistente
- **Código** em blocos apropriados
- **Links** para navegação entre documentos
- **Tabelas** para informações estruturadas

### Exemplos de Melhorias
- **Correção de erros** técnicos
- **Adição de exemplos** práticos
- **Melhoria da clareza** de explicações
- **Atualização** de informações desatualizadas
- **Tradução** para outros idiomas

## Status da Documentação

### Cobertura Atual
- **Arquitetura**: Documentada completamente
- **Interfaces**: GUI e CLI documentadas
- **Desenvolvimento**: Guias e padrões estabelecidos
- **Processamento**: Operações principais documentadas
- **Roadmap**: Em atualização contínua

### Áreas de Melhoria
- **Exemplos práticos**: Mais casos de uso
- **Tutoriais**: Guias passo a passo
- **FAQ**: Perguntas frequentes
- **Vídeos**: Demonstrações visuais (futuro)

## Links Úteis

### Documentação Externa
- [PyQt5 Documentation](https://doc.qt.io/qtforpython/)
- [rasterio Documentation](https://rasterio.readthedocs.io/)
- [NumPy Documentation](https://numpy.org/doc/)

### Recursos do Projeto
- [Repositório Principal](../README.MD)
- [Issues](https://github.com/your-username/igcv_raster_utility/issues)
- [Releases](https://github.com/your-username/igcv_raster_utility/releases)

### Compilação Rápida
Para gerar executáveis, consulte a seção **Compilação de Executáveis** no [Guia de Desenvolvimento](desenvolvimento.md#compilação-de-executáveis) ou use o script utilitário: `python utils/find_rasterio_paths.py`

## Suporte

### Para Dúvidas sobre o Projeto
- **README Principal**: Informações básicas
- **Issues**: Para bugs e solicitações de features
- **Logs**: Para debugging (pasta `logs/`)
- **Contato**: entre em contato por [email](mailto:matmb@unifei.edu.br)

## Notas Finais

Esta documentação é um **documento vivo** que evolui com o projeto. Sua qualidade e utilidade dependem da colaboração da comunidade.

### Compromissos
- **Manter atualizada** com o desenvolvimento
- **Ser clara e acessível** para diferentes públicos
- **Fornecer exemplos práticos** sempre que possível
- **Facilitar contribuições** da comunidade

### Agradecimentos
Agradecemos a todos os contribuidores que ajudaram a criar e manter esta documentação. Seu feedback e contribuições são essenciais para a qualidade e utilidade destes documentos.

---

*Última atualização: Julho 2025*

*Para dúvidas sobre esta documentação, abra uma issue no repositório.* 