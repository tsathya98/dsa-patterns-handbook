"use client";
import { useEffect, useRef } from "react";
import { basicSetup } from "codemirror";
import { python } from "@codemirror/lang-python";
import { Compartment, EditorState } from "@codemirror/state";
import {
  Decoration,
  EditorView,
  ViewPlugin,
  keymap,
  type DecorationSet,
  type ViewUpdate,
} from "@codemirror/view";
import { indentWithTab } from "@codemirror/commands";
import {
  HighlightStyle,
  indentUnit,
  syntaxHighlighting,
} from "@codemirror/language";
import { tags } from "@lezer/highlight";

const highlighting = HighlightStyle.define([
  { tag: tags.keyword, color: "var(--editor-keyword)" },
  { tag: tags.comment, color: "var(--editor-comment)", fontStyle: "italic" },
  {
    tag: [tags.string, tags.special(tags.string)],
    color: "var(--editor-string)",
  },
  { tag: tags.number, color: "var(--editor-number)" },
  { tag: [tags.bool, tags.null], color: "var(--editor-keyword)" },
  {
    tag: [tags.variableName, tags.propertyName],
    color: "var(--editor-variable)",
  },
  { tag: [tags.className, tags.typeName], color: "var(--editor-type)" },
  {
    tag: [tags.function(tags.variableName), tags.function(tags.propertyName)],
    color: "var(--editor-function)",
  },
  { tag: [tags.operator, tags.punctuation], color: "var(--editor-fg)" },
  { tag: tags.meta, color: "var(--editor-type)" },
]);

function editorTheme() {
  return EditorView.theme(
    {
      "&": {
        height: "100%",
        backgroundColor: "var(--editor-bg)",
        color: "var(--editor-fg)",
      },
      ".cm-scroller": {
        fontFamily: "var(--mono)",
        fontSize: "var(--font-sm)",
        lineHeight: "1.8",
        overflow: "auto",
      },
      ".cm-content": { padding: "14px 0", caretColor: "var(--editor-fg)" },
      ".cm-line": { padding: "0 10px" },
      ".cm-cursor, .cm-dropCursor": { borderLeftColor: "var(--editor-fg)" },
      ".cm-gutters": {
        backgroundColor: "var(--editor-gutter)",
        color: "var(--editor-line-number)",
        borderRight: "1px solid var(--line)",
      },
      ".cm-lineNumbers .cm-gutterElement": {
        minWidth: "38px",
        padding: "0 8px",
      },
      ".cm-activeLine, .cm-activeLineGutter": {
        backgroundColor: "var(--editor-active)",
      },
      "&.cm-focused .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection":
        { backgroundColor: "var(--editor-selection)" },
      "&.cm-focused": {
        outline: "2px solid var(--accent)",
        outlineOffset: "-2px",
      },
      ".cm-matchingBracket": {
        backgroundColor: "var(--editor-selection)",
        outline: "1px solid var(--line-strong)",
      },
      ".cm-searchMatch": {
        backgroundColor: "var(--warning-bg)",
        outline: "1px solid var(--warning-text)",
      },
      ".cm-selectionMatch": {
        backgroundColor: "var(--editor-active)",
        outline: "1px solid var(--line-strong)",
      },
      ".cm-foldPlaceholder": {
        color: "var(--muted)",
        backgroundColor: "var(--panel)",
        borderColor: "var(--line)",
      },
      ".cm-tooltip, .cm-panels": {
        color: "var(--text)",
        backgroundColor: "var(--surface)",
        borderColor: "var(--line-strong)",
      },
      ".cm-tooltip-autocomplete > ul > li[aria-selected]": {
        color: "var(--on-accent)",
        backgroundColor: "var(--accent)",
      },
      ".cm-textfield, .cm-button": {
        color: "var(--text)",
        background: "var(--surface)",
        borderColor: "var(--line-strong)",
      },
    },
    { dark: document.documentElement.dataset.theme === "dark" },
  );
}

function indentationGuides(view: EditorView): DecorationSet {
  const ranges = [];
  const seen = new Set<number>();
  for (const range of view.visibleRanges) {
    for (let pos = range.from; pos <= range.to;) {
      const line = view.state.doc.lineAt(pos);
      if (!seen.has(line.from)) {
        seen.add(line.from);
        const prefix = line.text.match(/^[\t ]*/)?.[0] ?? "";
        let columns = 0;
        for (const char of prefix)
          columns += char === "\t" ? 4 - (columns % 4) : 1;
        if (columns)
          ranges.push(
            Decoration.line({
              attributes: {
                class: "cm-indent-guides",
                style: `--indent-columns: ${columns}`,
              },
            }).range(line.from),
          );
      }
      pos = line.to + 1;
    }
  }
  return Decoration.set(ranges, true);
}
const guides = ViewPlugin.fromClass(
  class {
    decorations: DecorationSet;
    constructor(view: EditorView) {
      this.decorations = indentationGuides(view);
    }
    update(update: ViewUpdate) {
      if (update.docChanged || update.viewportChanged)
        this.decorations = indentationGuides(update.view);
    }
  },
  { decorations: (value) => value.decorations },
);

export function PythonEditor({
  value,
  onChange,
  onRun,
  onCursor,
}: {
  value: string;
  onChange: (value: string) => void;
  onRun: (code: string) => void;
  onCursor: (cursor: { line: number; column: number; lines: number }) => void;
}) {
  const host = useRef<HTMLDivElement>(null);
  const editor = useRef<EditorView | null>(null);
  const current = useRef({ value, onChange, onRun, onCursor });
  current.current = { value, onChange, onRun, onCursor };

  useEffect(() => {
    if (!host.current) return;
    const theme = new Compartment();
    const view = new EditorView({
      parent: host.current,
      state: EditorState.create({
        doc: current.current.value,
        extensions: [
          keymap.of([
            {
              key: "Mod-Enter",
              run: (view) => {
                current.current.onRun(view.state.doc.toString());
                return true;
              },
            },
            indentWithTab,
            {
              key: "Escape",
              run: (view) => {
                view.setTabFocusMode(2000);
                return false;
              },
            },
          ]),
          basicSetup,
          python(),
          indentUnit.of("    "),
          EditorState.tabSize.of(4),
          syntaxHighlighting(highlighting),
          theme.of(editorTheme()),
          guides,
          EditorView.contentAttributes.of({
            "aria-label": "Python code editor",
            "aria-describedby": "python-editor-help",
            spellcheck: "false",
            autocapitalize: "off",
            autocorrect: "off",
          }),
          EditorView.updateListener.of((update) => {
            if (update.docChanged)
              current.current.onChange(update.state.doc.toString());
            if (update.selectionSet || update.docChanged) {
              const pos = update.state.selection.main.head;
              const line = update.state.doc.lineAt(pos);
              current.current.onCursor({
                line: line.number,
                column: pos - line.from + 1,
                lines: update.state.doc.lines,
              });
            }
          }),
        ],
      }),
    });
    editor.current = view;
    current.current.onCursor({
      line: 1,
      column: 1,
      lines: view.state.doc.lines,
    });
    const observer = new MutationObserver(() =>
      view.dispatch({ effects: theme.reconfigure(editorTheme()) }),
    );
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["data-theme"],
    });
    return () => {
      observer.disconnect();
      view.destroy();
      editor.current = null;
    };
  }, []);

  useEffect(() => {
    const view = editor.current;
    if (view && view.state.doc.toString() !== value) {
      view.dispatch({
        changes: { from: 0, to: view.state.doc.length, insert: value },
        selection: { anchor: 0 },
        scrollIntoView: true,
      });
    }
  }, [value]);

  return <div className="python-code-editor" ref={host} />;
}
