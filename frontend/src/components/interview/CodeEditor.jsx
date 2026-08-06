import Editor from "@monaco-editor/react";

function CodeEditor({
  value,
  onChange,
  disabled = false,
}) {
  return (
    <div className="content-card">
      <h3 style={{ color: "red", fontSize: "32px" }}>
  🚀 MONACO TEST
</h3>

      <Editor
        height="450px"
        defaultLanguage="cpp"
        language="cpp"
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

          scrollBeyondLastLine: false,

          automaticLayout: true,

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

          glyphMargin: false,

          folding: true,
        }}
      />
    </div>
  );
}

export default CodeEditor;