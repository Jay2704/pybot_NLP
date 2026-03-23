import "./AuthSplitLayout.css";

/**
 * Split marketing (left) + auth card (right). UI-only shell.
 */
export default function AuthSplitLayout({ marketing, children }) {
  return (
    <div className="auth-page">
      <div className="auth-split">
        <aside className="auth-split__left">{marketing}</aside>
        <div className="auth-split__right">{children}</div>
      </div>
    </div>
  );
}
