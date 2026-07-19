import { useEffect, useRef, useState } from "react";

function VoiceInput({
  value,
  onChange,
  disabled = false,
}) {
  const recognitionRef = useRef(null);

  const [supported, setSupported] = useState(false);
  const [isListening, setIsListening] = useState(false);

  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setSupported(false);
      return;
    }

    setSupported(true);

    const recognition = new SpeechRecognition();

    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    recognition.onresult = (event) => {
      let finalTranscript = "";

      for (let i = 0; i < event.results.length; i++) {
        if (event.results[i].isFinal) {
          finalTranscript +=
            event.results[i][0].transcript + " ";
        }
      }

      if (finalTranscript.trim()) {
        onChange((previous) =>
          previous
            ? `${previous.trim()} ${finalTranscript.trim()}`
            : finalTranscript.trim()
        );
      }
    };

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.onerror = () => {
      setIsListening(false);
    };

    recognitionRef.current = recognition;

    return () => {
      recognitionRef.current?.stop();
    };
  }, [onChange]);

  const startListening = () => {
    if (!recognitionRef.current || disabled) {
      return;
    }

    recognitionRef.current.start();
  };

  const stopListening = () => {
    recognitionRef.current?.stop();
  };

  return (
    <div className="content-card">
      <h3>🎤 Voice Explanation</h3>

      {!supported && (
        <p className="error-text">
          Speech Recognition is not supported in this browser.
        </p>
      )}

      <textarea
        rows={6}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        placeholder="Speak or edit the transcript..."
      />

      <div
        style={{
          display: "flex",
          gap: "12px",
          marginTop: "12px",
        }}
      >
        <button
          type="button"
          className="button button--secondary"
          onClick={startListening}
          disabled={
            disabled ||
            !supported ||
            isListening
          }
        >
          Start Recording
        </button>

        <button
          type="button"
          className="button button--secondary"
          onClick={stopListening}
          disabled={
            disabled ||
            !isListening
          }
        >
          Stop Recording
        </button>
      </div>

      {isListening && (
        <p
          style={{
            marginTop: "12px",
            color: "green",
          }}
        >
          Listening...
        </p>
      )}
    </div>
  );
}

export default VoiceInput;