import { useEffect, useRef, useState } from "react";

function VoiceInput({
  value,
  onChange,
  disabled = false,
}) {
  const recognitionRef = useRef(null);

  const shouldContinueRef = useRef(false);

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
      let transcript = "";

      for (
        let i = event.resultIndex;
        i < event.results.length;
        i++
      ) {
        if (event.results[i].isFinal) {
          transcript +=
            event.results[i][0].transcript + " ";
        }
      }

      transcript = transcript.trim();

      if (!transcript) return;

      onChange((previous) =>
        previous
          ? `${previous.trim()} ${transcript}`
          : transcript
      );
    };

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onend = () => {
      setIsListening(false);

      if (
        shouldContinueRef.current &&
        !disabled
      ) {
        recognition.start();
      }
    };

    recognition.onerror = (event) => {
      console.log(event);

      if (
        event.error === "no-speech"
      ) {
        return;
      }

      setIsListening(false);
    };

    recognitionRef.current = recognition;

    return () => {
      shouldContinueRef.current = false;
      recognition.stop();
    };
  }, [onChange, disabled]);

  const startListening = () => {
    if (
      !recognitionRef.current ||
      disabled ||
      isListening
    ) {
      return;
    }

    shouldContinueRef.current = true;

    recognitionRef.current.start();
  };

  const stopListening = () => {
    shouldContinueRef.current = false;

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
            fontWeight: "bold",
          }}
        >
          🎤 Recording...
        </p>
      )}
    </div>
  );
}

export default VoiceInput;