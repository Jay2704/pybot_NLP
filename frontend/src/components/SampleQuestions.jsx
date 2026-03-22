import "./SampleQuestions.css";

const SAMPLES = [
  "What is list comprehension in Python?",
  "How does a Python decorator work?",
  "What is the difference between `is` and `==` in Python?",
  "Explain Python's Global Interpreter Lock (GIL).",
  "How do you handle exceptions in Python?",
];

export default function SampleQuestions({ onSelect, disabled }) {
  return (
    <div className="sample-questions">
      <p className="sample-questions__title">Try a sample question</p>
      <ul className="sample-questions__list">
        {SAMPLES.map((q) => (
          <li key={q}>
            <button
              type="button"
              className="sample-questions__chip"
              disabled={disabled}
              onClick={() => onSelect(q)}
            >
              {q}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
