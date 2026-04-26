# Plano: NetBox MCP Server - Full CRUD Implementation

## TL;DR
> **Objetivo**: Criar um MCP server completo para NetBox com operações CRUD, pesquisa, changelogs
> **Base**: Fork/evolução do official netboxlabs/netbox-mcp-server (read-only)
> **Diferencial**: 7 ferramentas (vs 3 do oficial), operações de escrita, suporte a bulk
> **Público-alvo**: GitHub público, DevOps/NetOps engineers, LLM agents

---

## 1. Estado Atual vs Desejado

### Official netbox-mcp-server (netboxlabs)
| Tool | Descrição | Escrita? |
|------|-----------|----------|
| `netbox_get_objects` | Listar objetos com filtros | ❌ Read-only |
| `netbox_get_object_by_id` | Buscar por ID | ❌ |
| `netbox_get_changelogs` | Histórico de mudanças | ❌ |

### Nosso NetBox MCP v2.0
| Tool | Descrição | Escrita? |
|------|-----------|----------|
| `netbox_search_objects` | Pesquisa global | ❌ |
| `netbox_get_objects` | Listar com filtros + paginação | ❌ |
| `netbox_get_object_by_id` | Buscar por ID | ❌ |
| `netbox_create_object` | Criar objetos | ✅ NEW |
| `netbox_update_object` | Atualizar objetos (PATCH) | ✅ NEW |
| `netbox_delete_object` | Deletar objetos | ✅ NEW |
| `netbox_get_changelogs` | Histórico de mudanças | ❌ |

**Total: 7 tools | 3 read-only + 3 CRUD + 1 changelog**

---

## 2. NetBox API Endpoints (Referência)

### Categorias de Objetos Suportados

| App | Endpoints |
|-----|-----------|
| **dcim** | sites, regions, site-groups, locations, racks, rack-roles, rack-types, manufacturer, device-types, devices, device-roles, platforms, interfaces, cables, console-ports, power-ports, inventory-items |
| **ipam** | roles, vlan-groups, vlans, vrfs, prefixes, ip-addresses, services, route-targets |
| **circuits** | providers, circuits, circuit-types, circuit-terminations |
| **tenancy** | tenants, tenant-groups, contacts, contact-groups, contact-roles |
| **virtualization** | clusters, cluster-types, cluster-groups, virtual-machines, interfaces |
| **extras** | tags, custom-fields, config-contexts, image-attachments, journal-entries |
| **wireless** | wireless-lans, wireless-links |

### HTTP Verbs por Operação

| Operação | HTTP | Body |
|----------|------|------|
| LIST | GET | Query params |
| GET by ID | GET | - |
| CREATE | POST | JSON object |
| CREATE BULK | POST | JSON array |
| UPDATE | PATCH | Partial JSON |
| UPDATE BULK | PATCH | JSON array |
| DELETE | DELETE | - |
| DELETE BULK | DELETE | JSON array |

---

## 3. Estrutura do Projeto

```
netbox-mcp/
├── .git/
├── .env.example
├── .gitignore
├── README.md
├── LICENSE                # Apache 2.0
├── CHANGELOG.md
├── CONTRIBUTING.md
├── pyproject.toml
├── Dockerfile
├── .dockerignore
├── src/
│   └── netbox_mcp_server/
│       ├── __init__.py
│       ├── __main__.py
│       ├── server.py      # MCP tools
│       ├── config.py      # Settings
│       ├── client.py      # HTTP client CRUD
│       ├── types.py       # NETBOX_OBJECT_TYPES
│       └── validators.py  # Filter validation
└── tests/
    ├── conftest.py
    ├── test_client.py
    ├── test_crud.py
    └── test_search.py
```

---

## 4. Design das Ferramentas

### T4.1: netbox_search_objects (READ)
Busca global em todos os objetos (names, IPs, serials, etc).

### T4.2: netbox_get_objects (READ)
Lista paginada com filtros NetBox. Suporte a lookup expressions (name__ic, id__in, etc).

### T4.3: netbox_get_object_by_id (READ)
Objeto por ID com field filtering opcional.

### T4.4: netbox_create_object (CREATE) 🆕
POST para criar objetos. Campos obrigatórios validados.

### T4.5: netbox_update_object (UPDATE) 🆕
PATCH para atualização parcial. Apenas campos alterados.

### T4.6: netbox_delete_object (DELETE) 🆕
DELETE para remover objetos. Confirmação recomendada.

### T4.7: netbox_get_changelogs (READ)
Histórico de mudanças com filtros.

---

## 5. Guardrails de Segurança

- ❌ Não expor token
- ✅ Validar object_type contra allowlist
- ✅ Sanitizar inputs (max 500 chars para changelog_message)
- ✅ Rate limiting no HTTP client
- ✅ Header `Authorization: Token XXX` em todo request

---

## 6. Plano de Execução

### FASE 1: Estrutura Base
 - [x] T1.1: pyproject.toml (dependências, metadata, scripts)
 - [x] T1.2: config.py (Settings pydantic, env vars, CLI args)
  - [x] T1.3: types.py (NETBOX_OBJECT_TYPES completo - 50+ tipos)
  - [x] T1.4: client.py (NetBoxRestClient com GET/POST/PATCH/DELETE)
 - [ ] T1.5: validators.py (filter validation)
 - [ ] T1.6: server.py (FastMCP server + 7 tools)

### FASE 2: Ferramentas READ (3 tools)
- [ ] T2.1: netbox_search_objects
- [ ] T2.2: netbox_get_objects + paginação
- [ ] T2.3: netbox_get_object_by_id + field filtering

### FASE 3: Ferramentas WRITE (3 tools) 🆕
- [ ] T3.1: netbox_create_object (POST)
- [ ] T3.2: netbox_update_object (PATCH)
- [ ] T3.3: netbox_delete_object (DELETE)

### FASE 4: Changelogs (1 tool)
- [ ] T4.1: netbox_get_changelogs

### FASE 5: Documentação + GitHub
 - [ ] T5.1: README.md (badges, quickstart, exemplos, architecture)
 - [ ] T5.2: CONTRIBUTING.md + CHANGELOG.md + LICENSE
 - [x] T5.3: .env.example + .gitignore + Dockerfile
 - [ ] T5.4: Commit inicial + git remote

### FASE 6: Testes
- [ ] T6.1: test_client.py (mock HTTP responses)
- [ ] T6.2: test_crud.py (create/update/delete scenarios)
- [ ] T6.3: test_search.py (search + filters)

### FASE 7: Validação E2E (contra NetBox real LXC 1038)
- [ ] T7.1: Teste de criação de objeto real
- [ ] T7.2: Teste de atualização
- [ ] T7.3: Teste de deleção
- [ ] T7.4: Teste de busca global
- [ ] T7.5: Teste de changelogs
- [ ] T7.6: Gap analysis (o que ficou faltando)

### FASE 8: Deploy no MetaMCP
- [ ] T8.1: Instalar no LXC 1043 (mcp-netbox user)
- [ ] T8.2: Atualizar wrapper script
- [ ] T8.3: Testar via MetaMCP

---

## 7. Acceptance Criteria

- [ ] 7 tools registradas no MCP
- [ ] CREATE/PATCH/DELETE funcionais contra NetBox real
- [ ] Paginação funcionando (limit/offset)
- [ ] Field filtering reduz payload
- [ ] Changelog messages registradas
- [ ] Error handling robusto (401, 403, 404, 500)
- [ ] Object type validation (recusa tipos inválidos)
- [ ] README com badges, quickstart, exemplos
- [ ] Testes passando
- [ ] MetaMCP integration funcionando

---

**Autor**: Prometheus
**Data**: 2026-04-26
**Versão**: 1.0
