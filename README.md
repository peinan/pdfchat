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
