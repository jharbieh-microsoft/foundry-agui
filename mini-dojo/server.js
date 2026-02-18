const http = require("http");
const fs = require("fs");
const path = require("path");

const port = Number(process.env.PORT || 3000);
const root = __dirname;

const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
};

const server = http.createServer((req, res) => {
  if (req.method === "POST" && req.url === "/api/chat") {
    let rawBody = "";
    req.on("data", (chunk) => {
      rawBody += chunk;
    });

    req.on("end", async () => {
      try {
        const payload = JSON.parse(rawBody || "{}");
        const endpoint = String(payload.endpoint || process.env.AGUI_ENDPOINT || "http://127.0.0.1:8888/");
        const messages = Array.isArray(payload.messages) ? payload.messages : [];

        const upstream = await fetch(endpoint, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "text/event-stream",
          },
          body: JSON.stringify({ messages }),
        });

        if (!upstream.ok || !upstream.body) {
          res.writeHead(upstream.status || 502, { "Content-Type": "application/json; charset=utf-8" });
          res.end(
            JSON.stringify({
              error: `Upstream failed with ${upstream.status} ${upstream.statusText}`,
            }),
          );
          return;
        }

        res.writeHead(200, {
          "Content-Type": "text/event-stream; charset=utf-8",
          "Cache-Control": "no-cache",
          Connection: "keep-alive",
        });

        const reader = upstream.body.getReader();
        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            break;
          }
          res.write(Buffer.from(value));
        }
        res.end();
      } catch (error) {
        res.writeHead(500, { "Content-Type": "application/json; charset=utf-8" });
        res.end(JSON.stringify({ error: error.message }));
      }
    });

    return;
  }

  const requestPath = req.url === "/" ? "/index.html" : req.url;
  const filePath = path.join(root, requestPath);

  if (!filePath.startsWith(root)) {
    res.writeHead(403);
    res.end("Forbidden");
    return;
  }

  fs.readFile(filePath, (error, data) => {
    if (error) {
      res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      res.end("Not found");
      return;
    }

    const extension = path.extname(filePath).toLowerCase();
    const contentType = mimeTypes[extension] || "application/octet-stream";
    res.writeHead(200, { "Content-Type": contentType });
    res.end(data);
  });
});

server.listen(port, () => {
  console.log(`Dojo standalone running at http://127.0.0.1:${port}`);
});
