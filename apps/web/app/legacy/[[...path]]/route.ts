import fs from "node:fs";
import path from "node:path";
export const dynamic = "force-dynamic";
export async function GET(
  request: Request,
  { params }: { params: Promise<{ path?: string[] }> },
) {
  const route = (await params).path;
  if (!route) {
    const target = new URL(request.url);
    target.pathname = "/legacy/viewer.html";
    return Response.redirect(target, 307);
  }
  const segments = route;
  if (segments.some((s) => s === ".." || s === "." || s.includes("\\")))
    return new Response("Not found", { status: 404 });
  const root = path.resolve(process.cwd(), "../../generated/legacy");
  const relative = segments.join("/");
  const allowed =
    ["viewer.html", "tracker.html", "faang_plan.html"].includes(relative) ||
    /^static\/vendor\/[a-zA-Z0-9_.-]+$/.test(relative);
  if (!allowed) return new Response("Not found", { status: 404 });
  const file = path.join(root, relative);
  if (!fs.existsSync(file)) return new Response("Not found", { status: 404 });
  const extension = path.extname(file);
  const types: Record<string, string> = {
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".woff2": "font/woff2",
  };
  const body =
    extension === ".html"
      ? fs.readFileSync(file, "utf8").replaceAll("../../content/", "/source/")
      : fs.readFileSync(file);
  return new Response(body, {
    headers: {
      "Content-Type": types[extension] ?? "application/octet-stream",
      "Cache-Control": "no-cache",
    },
  });
}
