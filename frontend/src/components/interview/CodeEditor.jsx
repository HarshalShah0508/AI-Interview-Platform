import Editor from "@monaco-editor/react";

function CodeEditor({
  value,
  onChange,
  language,
  disabled = false,
}) {
  return (
    <div className="content-card">
      <h3>💻 Code</h3>

      <Editor
        height="450px"
        language={language.monacoLanguage}
        value={value}
        onChange={(newValue) => onChange(newValue || "")}
        theme="vs"
        options={{
          readOnly: disabled,

          fontSize: 14,

          fontFamily:
            "SFMono-Regular, Consolas, Monaco, Menlo, monospace",

          minimap: {
            enabled: false,
          },

          automaticLayout: true,

          scrollBeyondLastLine: false,

          wordWrap: "on",

          lineNumbers: "on",

          roundedSelection: true,

          tabSize: 4,

          insertSpaces: true,

          autoIndent: "advanced",

          formatOnPaste: true,

          formatOnType: true,

          autoClosingBrackets: "always",

          autoClosingQuotes: "always",

          matchBrackets: "always",

          folding: true,
        }}
      />
    </div>
  );
}

export default CodeEditor;