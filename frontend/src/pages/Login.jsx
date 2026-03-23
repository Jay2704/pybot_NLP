import { useState } from "react";
import { Link } from "react-router-dom";
import AuthSplitLayout from "../components/auth/AuthSplitLayout.jsx";
import PasswordField from "../components/auth/PasswordField.jsx";
import { Button, Pill } from "../components/ui/index.js";
import "./authPages.css";

function LoginMarketing() {
  return (
    <>
      <Pill variant="marketing">NEW RELEASE V2.4</Pill>
      <h1 className="auth-mkt__title">
        Python answers, <span className="auth-mkt__highlight">instantly</span>—from real data.
      </h1>
      <p className="auth-mkt__lead">
        PyBot AI pairs a modern chat experience with TF-IDF retrieval over Stack Overflow—style
        knowledge. Sign in to sync preferences (UI demo; no backend yet).
      </p>
      <ul className="auth-mkt__list">
        <li>
          <span className="auth-mkt__icon" aria-hidden>
            ✓
          </span>
          <span>Retrieval-grounded answers with transparent source metadata</span>
        </li>
        <li>
          <span className="auth-mkt__icon" aria-hidden>
            ✓
          </span>
          <span>FastAPI + React stack, ready for Hugging Face Spaces</span>
        </li>
      </ul>
      <div className="auth-mkt__quote">
        <p>&ldquo;Finally a portfolio chatbot that looks like a real product.&rdquo;</p>
        <cite>— Early access waitlist</cite>
      </div>
    </>
  );
}

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <AuthSplitLayout
      marketing={<LoginMarketing />}
    >
      <div className="auth-form-card">
        <h2 className="auth-form-card__title">Welcome Back</h2>
        <p className="auth-form-card__subtitle">Sign in to continue to PyBot AI.</p>

        <form
          onSubmit={(e) => {
            e.preventDefault();
          }}
        >
          <div className="auth-social">
            <Button type="button" variant="outline" fullWidth>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
              </svg>
              Continue with GitHub
            </Button>
            <Button type="button" variant="outline" fullWidth>
              <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden>
                <path
                  fill="#4285F4"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="#34A853"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="#EA4335"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
              Continue with Google
            </Button>
          </div>

          <div className="auth-divider">OR EMAIL</div>

          <div className="auth-field">
            <label className="auth-field__label" htmlFor="login-email">
              Email
            </label>
            <input
              id="login-email"
              type="email"
              className="auth-field__input"
              placeholder="you@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
            />
          </div>

          <PasswordField
            id="login-password"
            label="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
          />

          <div className="auth-row">
            <label className="auth-checkbox">
              <input type="checkbox" name="remember" />
              Remember me
            </label>
            <a className="auth-link" href="#" onClick={(e) => e.preventDefault()}>
              Forgot password?
            </a>
          </div>

          <Button type="submit" variant="auth-submit" fullWidth>
            Sign in
          </Button>
        </form>

        <p className="auth-footer-link">
          Don&apos;t have an account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </AuthSplitLayout>
  );
}
