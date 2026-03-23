import profileImg from "../assets/profile.jpg";
import "./ProfileAvatar.css";

const SIZES = ["sm", "md", "lg"];

export default function ProfileAvatar({ size = "md", alt = "Jay", className = "" }) {
  const s = SIZES.includes(size) ? size : "md";
  return (
    <img
      src={profileImg}
      alt={alt}
      width={s === "lg" ? 160 : s === "md" ? 112 : 56}
      height={s === "lg" ? 160 : s === "md" ? 112 : 56}
      className={`profile-avatar profile-avatar--${s}${className ? ` ${className}` : ""}`}
      loading="lazy"
      decoding="async"
    />
  );
}
