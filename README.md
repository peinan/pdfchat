---
title: PDF Chat
emoji: 📄
colorFrom: blue
colorTo: green
sdk: gradio
app_file: src/pdfchat/app.py
pinned: true
---

# pdfchat

![](https://img.shields.io/badge/Python-3.9%2B-%233776AB?style=flat&logo=Python)
![](https://img.shields.io/badge/Gradio-v4.19.2-FF7C00.svg?logo=data:image/svg%2bxml;base64,PHN2ZyB3aWR0aD0iNTc2IiBoZWlnaHQ9IjU3NiIgdmlld0JveD0iMCAwIDU3NiA1NzYiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0yODcuNSAyMjlMODYgMzQ0LjVMMjg3LjUgNDYwTDQ4OSAzNDQuNUwyODcuNSAyMjlaIiBzdHJva2U9InVybCgjcGFpbnQwX2xpbmVhcl8xMDJfNykiIHN0cm9rZS13aWR0aD0iNTkiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPHBhdGggZD0iTTI4Ny41IDExNkw4NiAyMzEuNUwyODcuNSAzNDdMNDg5IDIzMS41TDI4Ny41IDExNloiIHN0cm9rZT0idXJsKCNwYWludDFfbGluZWFyXzEwMl83KSIgc3Ryb2tlLXdpZHRoPSI1OSIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8cGF0aCBkPSJNODYgMzQ0TDI4OCAyMjkiIHN0cm9rZT0idXJsKCNwYWludDJfbGluZWFyXzEwMl83KSIgc3Ryb2tlLXdpZHRoPSI1OSIgc3Ryb2tlLWxpbmVqb2luPSJiZXZlbCIvPgo8ZGVmcz4KPGxpbmVhckdyYWRpZW50IGlkPSJwYWludDBfbGluZWFyXzEwMl83IiB4MT0iNjAiIHkxPSIzNDQiIHgyPSI0MjkuNSIgeTI9IjM0NCIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPgo8c3RvcCBzdG9wLWNvbG9yPSIjRjlEMTAwIi8+CjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iI0Y5NzcwMCIvPgo8L2xpbmVhckdyYWRpZW50Pgo8bGluZWFyR3JhZGllbnQgaWQ9InBhaW50MV9saW5lYXJfMTAyXzciIHgxPSI1MTMuNSIgeTE9IjIzMSIgeDI9IjE0My41IiB5Mj0iMjMxIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CjxzdG9wIHN0b3AtY29sb3I9IiNGOUQxMDAiLz4KPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjRjk3NzAwIi8+CjwvbGluZWFyR3JhZGllbnQ+CjxsaW5lYXJHcmFkaWVudCBpZD0icGFpbnQyX2xpbmVhcl8xMDJfNyIgeDE9IjYwIiB5MT0iMzQ0IiB4Mj0iNDI4Ljk4NyIgeTI9IjM0MS44MTEiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KPHN0b3Agc3RvcC1jb2xvcj0iI0Y5RDEwMCIvPgo8c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiNGOTc3MDAiLz4KPC9saW5lYXJHcmFkaWVudD4KPC9kZWZzPgo8L3N2Zz4K)
[![](https://img.shields.io/badge/%F0%9F%A4%97-Open%20In%20Spaces-blue.svg)](https://huggingface.co/spaces/peinan/pdfchat)

Chat with a PDF document.

<table>
    <tr>
        <th>Screenshot</th>
        <th>Video</th>
    </tr>
    <tr>
        <td><img width="1270" alt="SCR-20240226-bfgp" src="https://github.com/peinan/pdfchat/assets/5601012/a9fec1be-9322-42cf-9ef5-fc742395bb85"></td>
        <td><video src="https://github.com/peinan/pdfchat/assets/5601012/07d62829-35c0-489b-b5db-8f1dc8f8bcb0"/>
</td>
    </tr>
</table>

## Development

### Prerequisites

pre-commit

```bash
pre-commit install
```

rye


```bash
rye sync
```

### Run

```bash
rye run server
```
