# Тестовое задание nginx X-Forwarded-For (DevOps)

## Описание

Тестовый стенд на Docker Compose, состоящий из трех nginx в режиме reverse proxy и backend-приложения на Python.

### Цель задания

- передача полного доверенного заголовка `X-Forwarded-For` до приложения;
- получение приложением всей цепочки IP-адресов (пользователь + nginx);
- защита от поддельного `X-Forwarded-For`, который может передать пользователь.

---

## Архитектура

Возможные маршруты прохождения запроса:

```text
Пользователь -> nginx3 -> backend
Пользователь -> nginx2 -> nginx3 -> backend
Пользователь -> nginx1 -> nginx2 -> nginx3 -> backend
```

---

## Состав стенда

- nginx1 — edge reverse proxy
- nginx2 — промежуточный reverse proxy
- nginx3 — reverse proxy перед backend
- backend — Python-приложение, выводящее HTTP-заголовки

---

## Запуск стенда

Сборка и запуск:

```bash
docker compose up -d --build
```

Проверка состояния контейнеров:

```bash
docker ps
```

---

## Протокол тестирования

### 1. Проверка полной цепочки X-Forwarded-For

Запрос через nginx1:

```bash
curl http://localhost:8081
```

Пример результата:

```json
{
  "x_forwarded_for": "172.21.0.1, 172.21.0.4, 172.21.0.3"
}
```

Приложение получает IP пользователя и всю цепочку nginx.

---

### 2. Проверка прямого запроса

Запрос через nginx3:

```bash
curl http://localhost:8083
```

Пример результата:

```json
{
  "x_forwarded_for": "172.21.0.1"
}
```

Приложение получает IP пользователя.

---

### 3. Проверка защиты от spoofing X-Forwarded-For

Попытка передачи поддельного заголовка:

```bash
curl -H "X-Forwarded-For: 8.8.8.8" localhost:8081
```

Пример результата:

```json
{
  "x_forwarded_for": "172.21.0.1, 172.21.0.4, 172.21.0.3"
}
```

Поддельный заголовок игнорируется.

Приложение получает только доверенную цепочку IP.

---

## Реализация

В nginx1 используется:

```nginx
proxy_set_header X-Forwarded-For $remote_addr;
```

Это позволяет:

- не доверять пользовательскому `X-Forwarded-For`;
- создать доверенное начало цепочки.

В nginx2 и nginx3 используется:

```nginx
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

Это позволяет достраивать полную цепочку доверенных proxy.








