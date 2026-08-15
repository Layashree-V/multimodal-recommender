import { useEffect, useMemo, useState } from "react";

import {
  Menu,
  X,
  Home,
  Compass,
  Bookmark,
  Settings,
  History,
  User,
  Bell,
  Search,
  ChevronRight,
  ChevronLeft,
  Play,
  Heart,
  Share2,
  Clock3,
  Sparkles,
  SlidersHorizontal,
  MoreVertical,
  BookOpen,
  Video,
  Zap,
  Pencil,
  Target,
  Check,
  ArrowRight,
  Flame,
  Trophy,
  BarChart3,
  Newspaper,
  Plane,
  Gamepad2,
  Laptop,
  Brain,
  Coffee,
  Shuffle,
  Mic,
  BookmarkCheck,
  ThumbsUp,
} from "lucide-react";

import "./App.css";

const API = "http://127.0.0.1:8000";

/* =========================================================
   AUTHENTICATION
========================================================= */
function AuthPage({ onAuthenticated }) {
  const [mode, setMode] = useState("signin");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const endpoint = mode === "signup" ? "/auth/signup" : "/auth/signin";
      const body = mode === "signup"
        ? { name: name.trim(), email: email.trim(), password }
        : { name: "", email: email.trim(), password };

      const response = await fetch(`${API}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        const detail = Array.isArray(data.detail)
          ? data.detail.map((item) => item.msg).join(", ")
          : data.detail;
        throw new Error(detail || "Authentication failed.");
      }

      localStorage.setItem("focusfeed_user_id", String(data.user_id));
      localStorage.setItem("focusfeed_user", JSON.stringify(data));
      onAuthenticated(data);
    } catch (err) {
      console.error("Authentication error:", err);
      setError(err.message || "Unable to connect to the server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: "24px", background: "#f7f8fc" }}>
      <div style={{ width: "100%", maxWidth: "430px", background: "white", borderRadius: "24px", padding: "36px", boxShadow: "0 20px 60px rgba(0,0,0,.10)" }}>
        <div style={{ textAlign: "center", marginBottom: "28px" }}>
          <div style={{ width: "56px", height: "56px", borderRadius: "16px", display: "inline-flex", alignItems: "center", justifyContent: "center", background: "#111827", color: "white", fontSize: "26px", fontWeight: 800 }}>F</div>
          <h1 style={{ margin: "16px 0 6px", fontSize: "30px" }}>FocusFeed</h1>
          <p style={{ margin: 0, color: "#6b7280" }}>Focus on what matters.</p>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px", marginBottom: "24px", background: "#f3f4f6", padding: "5px", borderRadius: "12px" }}>
          <button type="button" onClick={() => { setMode("signin"); setError(""); }} style={{ border: 0, borderRadius: "9px", padding: "11px", cursor: "pointer", background: mode === "signin" ? "white" : "transparent", fontWeight: 700 }}>Sign In</button>
          <button type="button" onClick={() => { setMode("signup"); setError(""); }} style={{ border: 0, borderRadius: "9px", padding: "11px", cursor: "pointer", background: mode === "signup" ? "white" : "transparent", fontWeight: 700 }}>Sign Up</button>
        </div>

        <form onSubmit={submit}>
          {mode === "signup" && (
            <label style={{ display: "block", marginBottom: "16px", fontWeight: 600 }}>
              Name
              <input value={name} onChange={(e) => setName(e.target.value)} required placeholder="Your name" style={{ display: "block", width: "100%", boxSizing: "border-box", marginTop: "7px", padding: "13px 14px", border: "1px solid #d1d5db", borderRadius: "10px", fontSize: "15px" }} />
            </label>
          )}

          <label style={{ display: "block", marginBottom: "16px", fontWeight: 600 }}>
            Email
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required placeholder="you@example.com" style={{ display: "block", width: "100%", boxSizing: "border-box", marginTop: "7px", padding: "13px 14px", border: "1px solid #d1d5db", borderRadius: "10px", fontSize: "15px" }} />
          </label>

          <label style={{ display: "block", marginBottom: "16px", fontWeight: 600 }}>
            Password
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required minLength={6} placeholder="At least 6 characters" style={{ display: "block", width: "100%", boxSizing: "border-box", marginTop: "7px", padding: "13px 14px", border: "1px solid #d1d5db", borderRadius: "10px", fontSize: "15px" }} />
          </label>

          {error && <div style={{ marginBottom: "16px", padding: "12px", borderRadius: "10px", background: "#fef2f2", color: "#b91c1c", fontSize: "14px" }}>{error}</div>}

          <button type="submit" disabled={loading} style={{ width: "100%", border: 0, borderRadius: "11px", padding: "14px", cursor: loading ? "not-allowed" : "pointer", background: "#111827", color: "white", fontSize: "16px", fontWeight: 700, opacity: loading ? .7 : 1 }}>
            {loading ? "Please wait..." : mode === "signup" ? "Create account" : "Sign in"}
          </button>
        </form>
      </div>
    </div>
  );
}

/* =========================================================
   SETUP PAGE
   Keep this screen as the first interaction.
========================================================= */

function SetupPage({ onContinue, onSearch }) {
  const [duration, setDuration] = useState(20);

  const topics = [
    {
      name: "Sports",
      icon: "⚽",
      status: "Trending",
      type: "green",
      visual: "sports",
    },
    {
      name: "Technology",
      icon: "💻",
      status: "Popular",
      type: "blue",
      visual: "technology",
    },
    {
      name: "AI & Science",
      icon: "🧠",
      status: "Trending",
      type: "purple",
      visual: "science",
    },
    {
      name: "Business",
      icon: "📊",
      status: "Popular",
      type: "orange",
      visual: "business",
    },
    {
      name: "Travel",
      icon: "✈️",
      status: "Popular",
      type: "blue",
      visual: "travel",
    },
    {
      name: "News & Politics",
      icon: "📰",
      status: "Trending",
      type: "red",
      visual: "news",
    },
    {
      name: "Education",
      icon: "📖",
      status: "Popular",
      type: "green",
      visual: "education",
    },
    {
      name: "Entertainment",
      icon: "🎮",
      status: "Popular",
      type: "purple",
      visual: "entertainment",
    },
  ];

  const suggestions = [
    "🚀 Startups",
    "💗 Health",
    "🪐 Space",
    "🧠 Psychology",
    "🏛 History",
  ];

  return (
    <div className="setup-page">
      <header className="setup-header">
        <div className="brand">
          <div className="brand-logo">F</div>

          <div>
            <div className="brand-name">FocusFeed</div>
            <div className="brand-tagline">
              Focus on what matters.
            </div>
          </div>
        </div>

        <div className="setup-header-actions">
          <button className="icon-button">
            <Bell size={21} />
          </button>

          <div className="avatar">
            M
          </div>
        </div>
      </header>

      <form className="setup-search" onSubmit={(event) => {
        event.preventDefault();
        const value = event.currentTarget.elements.setupSearch.value.trim();
        if (value) onSearch(value);
      }}>
        <Search size={21} />
        <input name="setupSearch" placeholder="Search anything you want to learn..." />
        <Mic size={20} />
      </form>

      <section className="setup-hero">
        <div className="setup-hero-copy">
          <h1>
            What do you want to
            <span> explore today?</span>
          </h1>

          <p>
            Pick a topic or search anything.
            <br />
            We'll build a personalized content path for you.
          </p>
        </div>

        <div className="rocket-art">
          <div className="rocket-circle">
            🚀
          </div>
        </div>
      </section>

      <section className="setup-focus-card">
        <div className="focus-intro">
          <div className="focus-icon">
            <Target size={30} />
          </div>

          <div>
            <h3>
              Start a Focus Session <Sparkles size={16} />
            </h3>

            <p>
              Stay focused with a guided content path
              <br />
              built just for you.
            </p>
          </div>
        </div>

        <div className="duration-area">
          <div className="duration-label">
            <Clock3 size={17} />
            Recommended time
          </div>

          <div className="duration-options">
            {[10, 20, 30].map((value) => (
              <button
                key={value}
                className={
                  duration === value
                    ? "duration active"
                    : "duration"
                }
                onClick={() => setDuration(value)}
              >
                {value} min
              </button>
            ))}

            <button className="duration edit-duration">
              <Pencil size={16} />
            </button>
          </div>
        </div>

        <button
          className="primary-button setup-start-button"
          onClick={() => onContinue(duration)}
        >
          <Play size={18} fill="currentColor" />
          Start Focus Session
        </button>
      </section>

      <section className="setup-section">
        <div className="section-heading">
          <div>
            <h2>Popular topics</h2>
          </div>

          <button className="text-button">
            View all
            <ChevronRight size={17} />
          </button>
        </div>

        <div className="topic-grid">
          {topics.map((topic) => (
            <button
              className="setup-topic-card"
              key={topic.name}
              onClick={() => onSearch(topic.name)}
            >
              <div
                className={`topic-visual ${topic.visual}`}
              >
                <span className="topic-visual-icon">
                  {topic.icon}
                </span>
              </div>

              <div className="topic-card-content">
                <strong>{topic.name}</strong>

                <span
                  className={`topic-status ${topic.type}`}
                >
                  <span />
                  {topic.status}
                </span>
              </div>
            </button>
          ))}
        </div>
      </section>

      <button className="explore-more">
        <span>
          <Compass size={19} />
          Explore more topics
        </span>

        <ChevronRight size={20} />
      </button>

      <section className="setup-section">
        <div className="section-heading">
          <h2>You might like</h2>
        </div>

        <div className="suggestion-row">
          {suggestions.map((item) => (
            <button
              className="suggestion-pill"
              key={item}
              onClick={() => onSearch(item.replace(/^\S+\s/, ""))}
            >
              {item}
            </button>
          ))}
        </div>
      </section>

      <section className="surprise-card">
        <div className="surprise-icon">
          <Sparkles size={27} />
        </div>

        <div>
          <h3>Not sure what to pick?</h3>
          <p>
            Let us suggest something based on your
            interests and reading history.
          </p>
        </div>

        <button className="primary-button surprise-button">
          <Shuffle size={17} />
          Surprise me
        </button>
      </section>

      <button
        className="primary-button continue-button"
        onClick={() => onContinue(duration)}
      >
        Continue
        <ArrowRight size={19} />
      </button>
    </div>
  );
}

/* =========================================================
   APP HEADER
========================================================= */

function AppHeader({ onMenu, onProfile, onSearch, userName }) {
  return (
    <header className="app-header">
      <div className="header-left">
        <button
          className="menu-button"
          onClick={onMenu}
          title="Open menu"
        >
          <Menu size={23} />
        </button>

        <div className="brand compact">
          <div className="brand-logo">F</div>

          <div>
            <div className="brand-name">
              FocusFeed
            </div>
            <div className="brand-tagline">
              Focus on what matters.
            </div>
          </div>
        </div>
      </div>

      <form
        className="global-search"
        onSubmit={(event) => {
          event.preventDefault();
          const value = event.currentTarget.elements.search.value.trim();
          if (value) onSearch(value);
        }}
      >
        <Search size={19} />
        <input
          name="search"
          placeholder="Search anything you want to learn..."
          aria-label="Search anything you want to learn"
        />
      </form>

      <div className="header-right">
        <button className="icon-button notification-button">
          <Bell size={20} />
          <span className="notification-dot" />
        </button>

        <button
          className="profile-avatar"
          onClick={onProfile}
          title={userName || "Profile"}
        >
          {(userName || "U").charAt(0).toUpperCase()}
        </button>
      </div>
    </header>
  );
}

/* =========================================================
   SIDE DRAWER
========================================================= */

function SideDrawer({
  open,
  page,
  setPage,
  onClose,
}) {
  const items = [
    {
      label: "Home",
      icon: Home,
      page: "home",
    },
    {
      label: "Search",
      icon: Search,
      page: "search",
    },
    {
      label: "Saved",
      icon: Bookmark,
      page: "saved",
    },
    {
      label: "Watch History",
      icon: History,
      page: "history",
    },
    {
      label: "Settings",
      icon: Settings,
      page: "settings",
    },
    {
      label: "Profile",
      icon: User,
      page: "profile",
    },
  ];

  if (!open) return null;

  return (
    <>
      <div
        className="drawer-overlay"
        onClick={onClose}
      />

      <aside className="side-drawer">
        <div className="drawer-header">
          <div className="brand compact">
            <div className="brand-logo">F</div>

            <div>
              <div className="brand-name">
                FocusFeed
              </div>
              <div className="brand-tagline">
                Focus on what matters.
              </div>
            </div>
          </div>

          <button
            className="icon-button"
            onClick={onClose}
          >
            <X size={20} />
          </button>
        </div>

        <div className="drawer-section-label">
          NAVIGATION
        </div>

        <nav className="drawer-nav">
          {items.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.page}
                className={
                  page === item.page
                    ? "drawer-item active"
                    : "drawer-item"
                }
                onClick={() => {
                  setPage(item.page);
                  onClose();
                }}
              >
                <Icon size={20} />
                <span>{item.label}</span>

                {page === item.page && (
                  <span className="drawer-active-dot" />
                )}
              </button>
            );
          })}
        </nav>

        <div className="drawer-divider" />

        <div className="drawer-focus-card">
          <div className="drawer-focus-icon">
            <Target size={20} />
          </div>

          <div>
            <strong>Focus Session</strong>
            <span>20:00 remaining</span>
          </div>
        </div>
      </aside>
    </>
  );
}

/* =========================================================
   BOTTOM NAVIGATION
========================================================= */

function BottomNav({
  page,
  setPage,
}) {
  const items = [
    {
      label: "Home",
      page: "home",
      icon: Home,
    },
    {
      label: "Explore",
      page: "explore",
      icon: Compass,
    },
    {
      label: "Blogs",
      page: "blogs",
      icon: Pencil,
    },
    {
      label: "Videos",
      page: "videos",
      icon: Video,
    },
    {
      label: "Shorts",
      page: "shorts",
      icon: Zap,
    },
    {
      label: "Profile",
      page: "profile",
      icon: User,
    },
  ];

  return (
    <nav className="bottom-nav">
      {items.map((item) => {
        const Icon = item.icon;
        const active = page === item.page;

        return (
          <button
            key={item.page}
            className={
              active
                ? "bottom-nav-item active"
                : "bottom-nav-item"
            }
            onClick={() => setPage(item.page)}
          >
            <Icon size={19} />
            <span>{item.label}</span>
          </button>
        );
      })}
    </nav>
  );
}

/* =========================================================
   CONTENT CARD
========================================================= */

function normalizeContentType(itemOrType) {
  const raw =
    typeof itemOrType === "string"
      ? itemOrType
      : itemOrType?.content_type ||
        itemOrType?.contentType ||
        itemOrType?.type ||
        "article";

  const value = String(raw).toLowerCase().replace(/[\s_-]+/g, "");

  if (value === "video" || value === "videos") return "VIDEO";
  if (value === "blog" || value === "blogs") return "BLOG";
  if (value === "short" || value === "shorts") return "SHORTS";
  return "ARTICLE";
}

function getYouTubeEmbedUrl(url = "") {
  const value = String(url);
  const match =
    value.match(/[?&]v=([^&]+)/) ||
    value.match(/youtu\.be\/([^?&]+)/) ||
    value.match(/youtube\.com\/shorts\/([^?&]+)/);

  if (!match) return null;

  return `https://www.youtube.com/embed/${match[1]}`;
}

function ContentCard({
  article,
  type,
  
  onOpen,
  liked = false,
  saved = false,
  onLike,
  onSave,
}) {
  const contentType = normalizeContentType(article || type);

  return (
    <article className="content-card">
      <div
        className={`content-thumbnail ${getVisualClass(
          article.category
        )}`}
      >
        <span className="thumbnail-icon">
          {getCategoryIcon(article.category)}
        </span>

        {contentType === "VIDEO" && (
          <span className="thumbnail-play">
            <Play
              size={17}
              fill="currentColor"
            />
          </span>
        )}

        {contentType === "SHORTS" && (
          <span className="thumbnail-play">
            <Zap size={18} />
          </span>
        )}
      </div>

      <div className="content-main">
        <div className="content-topline">
          <span
            className={`type-pill ${contentType.toLowerCase()}`}
          >
            {contentType}
          </span>

          <span className="content-time">
            {contentType === "VIDEO"
              ? "8 min watch"
              : "5 min read"}
          </span>
        </div>

        <h3>{article.title}</h3>

        <p className="content-source">
          {article.source || "FocusFeed"}
          <span>•</span>
          {article.category || "General"}
        </p>

        <div className="content-footer">
          <span className="match-label">
            {Math.round(
              (article.score || 0.55) * 100
            )}
% Match
          </span>

          <div className="card-actions">
            <button
              className={
                liked
                  ? "small-action liked"
                  : "small-action"
              }
              onClick={(e) => {
                e.stopPropagation();
                onLike?.();
              }}
            >
              <Heart
                size={17}
                fill={
                  liked
                    ? "currentColor"
                    : "none"
                }
              />
            </button>

            <button
              className={
                saved
                  ? "small-action saved"
                  : "small-action"
              }
              onClick={(e) => {
                e.stopPropagation();
                onSave?.();
              }}
            >
              {saved ? (
                <BookmarkCheck size={17} />
              ) : (
                <Bookmark size={17} />
              )}
            </button>

            <button className="small-action">
              <MoreVertical size={17} />
            </button>
          </div>
        </div>
      </div>

      <button
        className="card-open"
        onClick={() => onOpen(article.id)}
      >
        Open
        <ArrowRight size={15} />
      </button>
    </article>
  );
}

/* =========================================================
   HOME
========================================================= */

function HomePage({
  recommendations,
  loading,
  error,
  onOpenArticle,
  likedItems,
  savedItems,
  toggleLike,
  toggleSave,
  setPage,
  onStartFocus,
  focusDuration,
}) {
  const items = recommendations.slice(0, 8);

  return (
    <main className="page-content">
      <section className="welcome-row">
        <div>
          <div className="eyebrow">
            <Sparkles size={15} />
            Personalized for you
          </div>

          <h1>
            Your focus feed,
            <span> curated for you.</span>
          </h1>

          <p>
            Discover useful articles, blogs, videos and
            shorts based on your interests and activity.
          </p>
        </div>

        <div className="welcome-stat">
          <span>Today's focus</span>
          <strong>20 min</strong>
          <small>Keep building your streak</small>
        </div>
      </section>

      <section className="focus-banner">
        <div className="focus-banner-icon">
          <Target size={27} />
        </div>

        <div className="focus-banner-copy">
          <strong>Focus session</strong>
          <span>
            Stay focused with a personalized content path.
          </span>
        </div>

        <div className="focus-countdown">
          <Clock3 size={18} />
          <strong>18:42</strong>
          <span>remaining</span>
        </div>

        <button className="secondary-button">
          View my path
          <ChevronRight size={17} />
        </button>
      </section>

      <div className="page-toolbar">
        <div>
          <h2>Recommended for you</h2>
          <p>
            Content selected using your interests and
            recent activity.
          </p>
        </div>

        <button
          className="secondary-button"
          onClick={() => setPage("explore")}
        >
          Explore topics
          <Compass size={17} />
        </button>
      </div>

      {loading && (
        <div className="state-card">
          <div className="loading-spinner" />
          <strong>Loading recommendations</strong>
          <span>
            Personalizing your feed...
          </span>
        </div>
      )}

      {error && !loading && (
        <div className="state-card error-state">
          <strong>Unable to load recommendations</strong>
          <span>{error}</span>
        </div>
      )}

      {!loading &&
        !error &&
        items.length === 0 && (
          <div className="state-card">
            <Sparkles size={28} />
            <strong>No recommendations yet</strong>
            <span>
              Interact with some content and your feed
              will become personalized.
            </span>
          </div>
        )}

      {!loading &&
        !error &&
        items.length > 0 && (
          <div className="content-grid">
            {items.map((article) => (
              <ContentCard
                key={article.id}
                article={article}
                type={normalizeContentType(article)}
                onOpen={onOpenArticle}
                liked={likedItems[article.id]}
                saved={savedItems[article.id]}
                onLike={() =>
                  toggleLike(article.id)
                }
                onSave={() =>
                  toggleSave(article.id)
                }
              />
            ))}
          </div>
        )}

      <section className="recommendation-explanation">
        <div className="explanation-icon">
          <Sparkles size={22} />
        </div>

        <div>
          <strong>Why these recommendations?</strong>
          <p>
            FocusFeed combines your interests, reading
            behavior, interaction signals and content
            productivity scores to rank your feed.
          </p>
        </div>

        <ChevronRight size={20} />
      </section>
    </main>
  );
}

/* =========================================================
   EXPLORE
========================================================= */

function ExplorePage({ setPage, onSearch }) {
  const topics = [
    ["⚽", "Football", "Sports"],
    ["💻", "Technology", "Technology"],
    ["🧠", "AI & Science", "Science"],
    ["💰", "Finance", "Business"],
    ["✈️", "Travel", "Travel"],
    ["📰", "News", "News"],
    ["📚", "Education", "Education"],
    ["🎮", "Gaming", "Entertainment"],
  ];

  return (
    <main className="page-content">
      <section className="page-title">
        <div>
          <div className="eyebrow">
            <Compass size={15} />
            Explore
          </div>

          <h1>
            What do you want
            <span> to explore?</span>
          </h1>

          <p>
            Choose a topic and we'll bring the most
            relevant content together.
          </p>
        </div>

        <div className="explore-search">
          <Search size={19} />
          <input placeholder="Search topics..." />
        </div>
      </section>

      <section className="topic-dashboard">
        {topics.map(
          ([icon, title, category]) => (
            <button
              className="large-topic-card"
              key={title}
              onClick={() => onSearch(category)}
            >
              <div className="large-topic-icon">
                {icon}
              </div>

              <div>
                <strong>{title}</strong>
                <span>{category}</span>
              </div>

              <ChevronRight size={18} />
            </button>
          )
        )}
      </section>

      <section className="explore-feature">
        <div>
          <span className="eyebrow">
            <Sparkles size={15} />
            Personalized learning path
          </span>

          <h2>
            Follow a topic deeper
          </h2>

          <p>
            Start with an article, continue with a blog,
            watch a video and finish with a quick short.
          </p>

          <button
            className="primary-button"
            onClick={() => setPage("home")}
          >
            Build my path
            <ArrowRight size={17} />
          </button>
        </div>

        <div className="path-visual">
          <div>ARTICLE</div>
          <ArrowRight />
          <div>BLOG</div>
          <ArrowRight />
          <div>VIDEO</div>
          <ArrowRight />
          <div>SHORT</div>
        </div>
      </section>
    </main>
  );
}

/* =========================================================
   SEARCH RESULTS
========================================================= */

function SearchPage({
  query,
  results,
  loading,
  error,
  onOpenArticle,
  likedItems,
  savedItems,
  toggleLike,
  toggleSave,
}) {
  return (
    <main className="page-content">
      <section className="page-title">
        <div>
          <div className="eyebrow">
            <Search size={15} />
            Search
          </div>
          <h1>Results for <span>"{query}".</span></h1>
          <p>Content retrieved by the backend semantic search engine.</p>
        </div>
      </section>

      {loading && (
        <div className="state-card">
          <div className="loading-spinner" />
          <strong>Searching...</strong>
          <span>Finding the most relevant content.</span>
        </div>
      )}

      {error && !loading && (
        <div className="state-card error-state">
          <strong>Search failed</strong>
          <span>{error}</span>
        </div>
      )}

      {!loading && !error && results.length === 0 && (
        <div className="state-card">
          <Search size={28} />
          <strong>No results found</strong>
          <span>Try another topic or a more specific learning query.</span>
        </div>
      )}

      {!loading && !error && results.length > 0 && (
        <div className="content-grid">
          {results.map((article) => (
            <ContentCard
              key={article.id}
              article={article}
              type={normalizeContentType(article)}
              onOpen={onOpenArticle}
              liked={likedItems[article.id]}
              saved={savedItems[article.id]}
              onLike={() => toggleLike(article.id)}
              onSave={() => toggleSave(article.id)}
            />
          ))}
        </div>
      )}
    </main>
  );
}

/* =========================================================
   BLOGS
========================================================= */

function BlogsPage({
  recommendations,
  onOpenArticle,
  savedItems,
  likedItems,
  toggleSave,
  toggleLike,
}) {
  const blogs = recommendations
    .filter((item) => normalizeContentType(item) === "BLOG")
    .slice(0, 12);

  return (
    <main className="page-content">
      <section className="page-title">
        <div>
          <div className="eyebrow">
            <Pencil size={15} />
            Blogs
          </div>

          <h1>
            Deep dives &
            <span> expert perspectives.</span>
          </h1>

          <p>
            Opinions, analysis and stories selected around
            your interests.
          </p>
        </div>
      </section>

      <div className="category-tabs">
        <button className="category-tab active">
          Latest
        </button>
        <button className="category-tab">
          Opinion
        </button>
        <button className="category-tab">
          Analysis
        </button>
        <button className="category-tab">
          Tactics
        </button>
        <button className="category-tab">
          Stories
        </button>
      </div>

      <div className="article-list">
        {blogs.map((article) => (
          <ContentCard
            key={article.id}
            article={article}
            type="BLOG"
            onOpen={onOpenArticle}
            saved={savedItems[article.id]}
            liked={likedItems[article.id]}
            onSave={() =>
              toggleSave(article.id)
            }
            onLike={() =>
              toggleLike(article.id)
            }
          />
        ))}
      </div>

      {blogs.length === 0 && (
        <div className="state-card">
          <Pencil size={28} />
          <strong>
            Blog feed will appear here
          </strong>
          <span>
            Run the backend content ingestion once to populate
            this feed with real blog sources.
          </span>
        </div>
      )}
    </main>
  );
}

/* =========================================================
   VIDEOS
========================================================= */

function VideosPage({
  recommendations,
  onOpenArticle,
  savedItems,
  likedItems,
  toggleSave,
  toggleLike,
}) {
  const videos = recommendations
    .filter((item) => normalizeContentType(item) === "VIDEO")
    .slice(0, 12);

  return (
    <main className="page-content">
      <section className="page-title">
        <div>
          <div className="eyebrow">
            <Video size={15} />
            Videos
          </div>

          <h1>
            Watch smarter,
            <span> not longer.</span>
          </h1>

          <p>
            In-depth explainers, analysis and useful videos
            matched to your interests.
          </p>
        </div>
      </section>

      <div className="category-tabs">
        <button className="category-tab active">
          Latest
        </button>
        <button className="category-tab">
          Match Analysis
        </button>
        <button className="category-tab">
          Tactical
        </button>
        <button className="category-tab">
          Explainers
        </button>
        <button className="category-tab">
          Interviews
        </button>
      </div>

      <div className="video-grid">
        {videos.map((article) => (
          <ContentCard
            key={article.id}
            article={article}
            type="VIDEO"
            onOpen={onOpenArticle}
            saved={savedItems[article.id]}
            liked={likedItems[article.id]}
            onSave={() =>
              toggleSave(article.id)
            }
            onLike={() =>
              toggleLike(article.id)
            }
          />
        ))}
      </div>

      {videos.length === 0 && (
        <div className="state-card">
          <Video size={28} />
          <strong>No videos available yet</strong>
          <span>Run the backend content ingestion to add real video sources.</span>
        </div>
      )}
    </main>
  );
}

/* =========================================================
   SHORTS
========================================================= */

function ShortsPage({
  recommendations,
  onOpenArticle,
}) {
  const shorts = recommendations
    .filter((item) => normalizeContentType(item) === "SHORTS")
    .slice(0, 12);

  return (
    <main className="page-content">
      <section className="shorts-heading">
        <div>
          <div className="eyebrow">
            <Zap size={15} />
            Shorts
          </div>

          <h1>
            Quick ideas.
            <span> Useful moments.</span>
          </h1>

          <p>
            Short-form content designed to give you
            something useful in under a minute.
          </p>
        </div>
      </section>

      <div className="shorts-grid">
        {shorts.map((article) => (
          <button
            className="short-card"
            key={article.id}
            onClick={() =>
              onOpenArticle(article.id)
            }
          >
            <div
              className={`short-visual ${getVisualClass(
                article.category
              )}`}
            >
              <span>
                {getCategoryIcon(
                  article.category
                )}
              </span>

              <div className="short-play">
                <Play
                  size={19}
                  fill="currentColor"
                />
              </div>

              <small>0:59</small>
            </div>

            <div className="short-content">
              <strong>{article.title}</strong>

              <span>
                {article.source || "FocusFeed"} • 59 sec
              </span>
            </div>
          </button>
        ))}
      </div>

      {shorts.length === 0 && (
        <div className="state-card">
          <Zap size={28} />
          <strong>No shorts available yet</strong>
          <span>Run the backend content ingestion to add short-form sources.</span>
        </div>
      )}
    </main>
  );
}

/* =========================================================
   SAVED
========================================================= */

function SavedPage({
  recommendations,
  savedItems,
  savedContent,
  onOpenArticle,
}) {
  const source = savedContent?.length ? savedContent : recommendations;
  const saved = source.filter(
    (item) => savedContent?.length ? true : savedItems[item.id]
  );

  return (
    <main className="page-content">
      <section className="page-title">
        <div>
          <div className="eyebrow">
            <Bookmark size={15} />
            Saved
          </div>

          <h1>
            Your saved
            <span> content.</span>
          </h1>

          <p>
            Everything you've saved in one place.
          </p>
        </div>
      </section>

      <div className="saved-tabs">
        <button className="category-tab active">
          All
        </button>
        <button className="category-tab">
          Articles
        </button>
        <button className="category-tab">
          Blogs
        </button>
        <button className="category-tab">
          Videos
        </button>
        <button className="category-tab">
          Shorts
        </button>
      </div>

      {saved.length > 0 ? (
        <div className="article-list">
          {saved.map((article) => (
            <ContentCard
              key={article.id}
              article={article}
              type="ARTICLE"
              onOpen={onOpenArticle}
              saved
            />
          ))}
        </div>
      ) : (
        <div className="empty-card">
          <Bookmark size={34} />
          <h3>No saved content yet</h3>
          <p>
            Tap the bookmark icon on an article, blog or
            video to save it here.
          </p>
        </div>
      )}
    </main>
  );
}

/* =========================================================
   HISTORY
========================================================= */

function HistoryPage({
  history,
  likedItems,
  savedItems,
  onOpenArticle,
}) {
  return (
    <main className="page-content">
      <section className="page-title">
        <div>
          <div className="eyebrow">
            <History size={15} />
            Watch History
          </div>

          <h1>
            What you've
            <span> consumed.</span>
          </h1>

          <p>
            Articles, blogs, videos and shorts you've
            interacted with.
          </p>
        </div>
      </section>

      <div className="history-summary">
        <div>
          <Clock3 />
          <strong>{history.length}</strong>
          <span>Items consumed</span>
        </div>

        <div>
          <ThumbsUp />
          <strong>
            {
              Object.values(likedItems).filter(Boolean)
                .length
            }
          </strong>
          <span>Liked items</span>
        </div>

        <div>
          <Bookmark />
          <strong>
            {
              Object.values(savedItems).filter(Boolean)
                .length
            }
          </strong>
          <span>Saved items</span>
        </div>
      </div>

      {history.length > 0 ? (
        <div className="article-list">
          {history.map((article) => (
            <ContentCard
              key={article.id}
              article={article}
              type="ARTICLE"
              onOpen={onOpenArticle}
              liked={likedItems[article.id]}
              saved={savedItems[article.id]}
            />
          ))}
        </div>
      ) : (
        <div className="empty-card">
          <History size={34} />
          <h3>Your history is empty</h3>
          <p>
            Open content from your personalized feed and
            it will appear here.
          </p>
        </div>
      )}
    </main>
  );
}

/* =========================================================
   PROFILE
========================================================= */

function ProfilePage({ onLogout, user, stats, loading, onEdit }) {
  const displayName = stats?.name || user?.name || "User";
  const savedCount = stats?.saved_count ?? 0;
  const viewedCount = stats?.viewed_count ?? 0;
  const likedCount = stats?.liked_count ?? 0;
  const sharedCount = stats?.shared_count ?? 0;
  const focusSessions = stats?.focus_sessions ?? 0;
  const readMinutes = Math.round((stats?.total_read_time || 0) / 60);
  const topInterests = stats?.top_interests || [];

  return (
    <main className="page-content">
      <section className="profile-hero-card">
        <div className="large-avatar">{displayName.charAt(0).toUpperCase()}</div>

        <div className="profile-info">
          <div className="eyebrow">
            <User size={15} />
            Profile
          </div>
          <h1>{displayName}</h1>
          <p>{user?.email || "Your FocusFeed account"}</p>
          <button className="secondary-button" onClick={onEdit}>
            <Pencil size={16} />
            Edit profile
          </button>
        </div>

        <div className="focus-streak">
          <Flame size={21} />
          <span>Focus activity</span>
          <strong>{focusSessions} sessions</strong>
          <small>Keep learning consistently.</small>
        </div>
      </section>

      {loading ? (
        <div className="state-card">
          <div className="loading-spinner" />
          <strong>Loading your profile</strong>
          <span>Reading your activity from PostgreSQL.</span>
        </div>
      ) : (
        <>
          <section className="profile-stat-grid">
            <div><Bookmark /><strong>{savedCount}</strong><span>Saved items</span></div>
            <div><History /><strong>{viewedCount}</strong><span>Items viewed</span></div>
            <div><Target /><strong>{focusSessions}</strong><span>Focus sessions</span></div>
            <div><Sparkles /><strong>{topInterests.length}</strong><span>Top interests</span></div>
          </section>

          <section className="activity-card">
            <div className="card-heading">
              <div>
                <h2>Your activity</h2>
                <p>Live totals from your account.</p>
              </div>
            </div>

            <div className="activity-metrics">
              <div className="activity-chart">
                <span>Total reading time</span>
                <strong>{readMinutes} min</strong>
                <div className="fake-chart">
                  <i style={{ height: `${Math.min(100, Math.max(10, viewedCount * 8))}%` }} />
                  <i style={{ height: `${Math.min(100, Math.max(10, likedCount * 12))}%` }} />
                  <i style={{ height: `${Math.min(100, Math.max(10, savedCount * 10))}%` }} />
                  <i style={{ height: `${Math.min(100, Math.max(10, sharedCount * 15))}%` }} />
                  <i style={{ height: `${Math.min(100, Math.max(10, focusSessions * 10))}%` }} />
                </div>
              </div>

              <div className="mix-card">
                <span>Top interests</span>
                <div className="mix-bars">
                  {topInterests.length ? topInterests.map((item) => (
                    <div key={item.category}>
                      <span>{item.category}</span>
                      <b>{item.count}</b>
                    </div>
                  )) : (
                    <div><span>No interests yet</span><b>0</b></div>
                  )}
                </div>
              </div>
            </div>
          </section>

          <section className="settings-card">
            <div className="card-heading">
              <div>
                <h2>Account</h2>
                <p>{user?.email}</p>
              </div>
            </div>
            <PreferenceRow icon={ThumbsUp} title="Liked content" description={`${likedCount} items liked`} />
            <PreferenceRow icon={Share2} title="Shared content" description={`${sharedCount} items shared`} />
          </section>
        </>
      )}

      <button className="primary-button" onClick={onLogout} style={{ marginTop: "20px" }}>
        Sign out
      </button>
    </main>
  );
}

function PreferenceRow({
  icon: Icon,
  title,
  description,
}) {
  return (
    <button className="preference-row">
      <div className="preference-icon">
        <Icon size={19} />
      </div>

      <div>
        <strong>{title}</strong>
        <span>{description}</span>
      </div>

      <ChevronRight size={18} />
    </button>
  );
}

/* =========================================================
   SETTINGS
========================================================= */

function SettingsPage() {
  return (
    <main className="page-content">
      <section className="page-title">
        <div>
          <div className="eyebrow">
            <Settings size={15} />
            Settings
          </div>

          <h1>
            Make FocusFeed
            <span> yours.</span>
          </h1>

          <p>
            Manage your experience and content preferences.
          </p>
        </div>
      </section>

      <div className="settings-layout">
        <section className="settings-card">
          <h2>Content preferences</h2>

          <PreferenceRow
            icon={Sparkles}
            title="More productive content"
            description="Prioritize useful and educational content"
          />

          <PreferenceRow
            icon={Video}
            title="Content types"
            description="Articles • Blogs • Videos • Shorts"
          />

          <PreferenceRow
            icon={Compass}
            title="Interest topics"
            description="Football • Technology • News"
          />
        </section>

        <section className="settings-card">
          <h2>Focus preferences</h2>

          <PreferenceRow
            icon={Clock3}
            title="Recommended focus duration"
            description="20 minutes"
          />

          <PreferenceRow
            icon={Target}
            title="Focus session"
            description="Guided content path enabled"
          />
        </section>
      </div>
    </main>
  );
}

/* =========================================================
   ARTICLE DETAIL
========================================================= */

function ArticleDetail({
  article,
  liked,
  saved,
  shared,
  onLike,
  onSave,
  onShare,
  onClose,
  readTime,
  scrollDepth,
}) {
  return (
    <div className="article-page">
      <div className="article-topbar">
        <button
          className="secondary-button"
          onClick={onClose}
        >
          <ChevronLeft size={18} />
          Back
        </button>

        <div className="article-progress">
          Reading {scrollDepth}%
        </div>
      </div>

      <article className="article-detail">
        <div className="article-meta">
          <span className="category-badge">
            {article.category || "News"}
          </span>

          <span>•</span>

          <span>
            {article.source || "MIND"}
          </span>
        </div>

        <h1>{article.title}</h1>

        {article.description && (
          <p className="article-description">
            {article.description}
          </p>
        )}

        <div className="article-author-row">
          <div className="author-avatar">
            F
          </div>

          <div>
            <strong>FocusFeed</strong>
            <span>
              • {normalizeContentType(article) === "VIDEO" || normalizeContentType(article) === "SHORTS"
                ? `${readTime}s watched`
                : `${Math.max(1, Math.ceil(readTime / 60))} min read`}
            </span>
          </div>
        </div>

        {normalizeContentType(article) === "VIDEO" ||
        normalizeContentType(article) === "SHORTS" ? (
          <div
            className={`article-hero ${getVisualClass(
              article.category
            )}`}
            style={{ overflow: "hidden", padding: 0 }}
          >
            {getYouTubeEmbedUrl(article.url) ? (
              <iframe
                src={getYouTubeEmbedUrl(article.url)}
                title={article.title}
                style={{
                  width: "100%",
                  height: "100%",
                  minHeight: "420px",
                  border: 0,
                }}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowFullScreen
              />
            ) : (
              <a
                href={article.url}
                target="_blank"
                rel="noreferrer"
                className="primary-button"
              >
                Open original video
              </a>
            )}
          </div>
        ) : (
          <div
            className={`article-hero ${getVisualClass(
              article.category
            )}`}
          >
            <span>
              {getCategoryIcon(article.category)}
            </span>
          </div>
        )}

        <div className="article-action-bar">
          <button
            className={
              liked
                ? "article-action liked"
                : "article-action"
            }
            onClick={onLike}
          >
            <Heart
              size={18}
              fill={
                liked
                  ? "currentColor"
                  : "none"
              }
            />
            {liked ? "Liked" : "Like"}
          </button>

          <button
            className={
              saved
                ? "article-action saved"
                : "article-action"
            }
            onClick={onSave}
          >
            {saved ? (
              <BookmarkCheck size={18} />
            ) : (
              <Bookmark size={18} />
            )}
            {saved ? "Saved" : "Save"}
          </button>

          <button
            className={
              shared
                ? "article-action shared"
                : "article-action"
            }
            onClick={onShare}
          >
            <Share2 size={18} />
            {shared ? "Shared" : "Share"}
          </button>
        </div>

        <div className="article-body">
          <p>
            {article.content_text ||
              article.description ||
              "This content does not contain additional text."}
          </p>
        </div>

        {article.url && (
          <div style={{ marginTop: "20px", marginBottom: "20px" }}>
            <a
              href={article.url}
              target="_blank"
              rel="noreferrer"
              className="secondary-button"
              style={{ display: "inline-flex", textDecoration: "none" }}
            >
              Open original source
              <ArrowRight size={16} />
            </a>
          </div>
        )}

        <div className="finish-reading-card">
          <div>
            <Clock3 size={20} />
            <span>
              {normalizeContentType(article) === "VIDEO" || normalizeContentType(article) === "SHORTS"
                ? `Watch time: ${readTime}s`
                : `Reading time: ${readTime}s`}
            </span>
          </div>

          <div>
            <strong>
              {scrollDepth}%
            </strong>
            <span>read</span>
          </div>

          <button
            className="primary-button"
            onClick={onClose}
          >
            <Check size={17} />
            Done
          </button>
        </div>
      </article>
    </div>
  );
}

/* =========================================================
   HELPERS
========================================================= */

function getCategoryIcon(category = "") {
  const value = category.toLowerCase();

  if (
    value.includes("sport") ||
    value.includes("football")
  ) {
    return "⚽";
  }

  if (
    value.includes("tech") ||
    value.includes("science")
  ) {
    return "💻";
  }

  if (value.includes("travel")) {
    return "✈️";
  }

  if (
    value.includes("business") ||
    value.includes("finance")
  ) {
    return "📊";
  }

  if (value.includes("health")) {
    return "💗";
  }

  return "📰";
}

function getVisualClass(category = "") {
  const value = category.toLowerCase();

  if (value.includes("sport")) return "visual-sports";
  if (value.includes("tech")) return "visual-tech";
  if (value.includes("science")) return "visual-science";
  if (value.includes("travel")) return "visual-travel";
  if (value.includes("business")) return "visual-business";
  if (value.includes("health")) return "visual-health";

  return "visual-news";
}


/* =========================================================
   FOCUS SESSION
   Guided, distraction-free content session.
========================================================= */
function FocusSession({
  userId,
  duration,
  recommendations,
  onClose,
  onComplete,
}) {
  const [goal, setGoal] = useState("");
  const [secondsLeft, setSecondsLeft] = useState(Math.max(60, Number(duration || 20) * 60));
  const [running, setRunning] = useState(true);
  const [completed, setCompleted] = useState(false);
  const [startedAt] = useState(() => Date.now());
  const [serverSessionId, setServerSessionId] = useState(null);
  const [serverError, setServerError] = useState("");

  const path = useMemo(() => {
    const usable = Array.isArray(recommendations) ? recommendations : [];
    return usable.slice(0, 4);
  }, [recommendations]);

  useEffect(() => {
    let cancelled = false;

    const startSession = async () => {
      try {
        setServerError("");
        const response = await fetch(`${API}/focus/sessions`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: Number(userId),
            duration_minutes: Number(duration || 20),
            goal: goal.trim() || "General learning",
            content_ids: path.map((item) => Number(item.id)).filter(Boolean),
          }),
        });

        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
          throw new Error(data.detail || "Could not start the focus session.");
        }

        if (!cancelled) {
          setServerSessionId(data.id);
        }
      } catch (error) {
        console.error("Focus session start error:", error);
        if (!cancelled) {
          setServerError(error.message || "Focus session could not be synced.");
        }
      }
    };

    if (Number(userId) > 0) startSession();

    return () => {
      cancelled = true;
    };
  }, []); // Start exactly once when the session screen opens

  useEffect(() => {
    if (!running || completed) return undefined;
    const timer = setInterval(() => {
      setSecondsLeft((value) => {
        if (value <= 1) {
          clearInterval(timer);
          setRunning(false);
          setCompleted(true);
          return 0;
        }
        return value - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [running, completed]);

  const finish = async () => {
    if (!completed) {
      setRunning(false);
      setCompleted(true);
      return;
    }

    const elapsedSeconds = Math.max(0, Math.round((Date.now() - startedAt) / 1000));
    const payload = {
      durationMinutes: Number(duration || 20),
      elapsedSeconds,
      goal: goal.trim() || "General learning",
      completed: true,
    };

    if (serverSessionId) {
      try {
        const response = await fetch(`${API}/focus/sessions/${serverSessionId}/complete`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            elapsed_seconds: elapsedSeconds,
            goal: payload.goal,
            content_ids: path.map((item) => Number(item.id)).filter(Boolean),
          }),
        });

        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
          throw new Error(data.detail || "Could not save the focus session.");
        }
      } catch (error) {
        console.error("Focus session completion error:", error);
        setServerError(error.message || "Could not save the focus session.");
        return;
      }
    }

    await onComplete?.(payload);
    onClose();
  };

  const handleClose = async () => {
    if (serverSessionId && !completed) {
      try {
        await fetch(`${API}/focus/sessions/${serverSessionId}/abandon`, {
          method: "POST",
        });
      } catch (error) {
        console.error("Focus session abandon error:", error);
      }
    }
    onClose();
  };

  const minutes = Math.floor(secondsLeft / 60).toString().padStart(2, "0");
  const seconds = (secondsLeft % 60).toString().padStart(2, "0");
  const totalSeconds = Math.max(60, Number(duration || 20) * 60);
  const progress = Math.min(100, Math.max(0, ((totalSeconds - secondsLeft) / totalSeconds) * 100));

  return (
    <div style={{ position: "fixed", inset: 0, zIndex: 1000, background: "rgba(15,23,42,.72)", backdropFilter: "blur(8px)", display: "flex", alignItems: "center", justifyContent: "center", padding: 20 }}>
      <section style={{ width: "min(900px, 100%)", maxHeight: "92vh", overflowY: "auto", background: "#fff", borderRadius: 28, padding: 28, boxShadow: "0 30px 90px rgba(0,0,0,.28)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", gap: 16, alignItems: "center", marginBottom: 24 }}>
          <div>
            <div className="eyebrow"><Target size={15} /> Focus Session</div>
            <h1 style={{ margin: "8px 0 4px" }}>{completed ? "Session complete 🎉" : "Stay focused."}</h1>
            <p style={{ margin: 0, color: "#64748b" }}>{completed ? "Nice work. Your session is finished." : "A distraction-free path built from your FocusFeed content."}</p>
          {serverError && (
            <div style={{ marginTop: 10, color: "#b45309", fontSize: 13 }}>
              {serverError}
            </div>
          )}
          </div>
          <button className="icon-button" onClick={handleClose} aria-label="Close focus session"><X size={20} /></button>
        </div>

        {!completed && (
          <>
            <label style={{ display: "block", fontWeight: 700, marginBottom: 18 }}>
              What are you focusing on?
              <input value={goal} onChange={(e) => setGoal(e.target.value)} placeholder="e.g. Learn machine learning" style={{ display: "block", width: "100%", boxSizing: "border-box", marginTop: 8, padding: "13px 14px", border: "1px solid #d1d5db", borderRadius: 12, fontSize: 15 }} />
            </label>

            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", padding: "20px 0 26px" }}>
              <div style={{ width: "min(300px, 72vw)", height: "min(300px, 72vw)", borderRadius: "50%", background: `conic-gradient(#111827 ${progress}%, #e5e7eb 0)`, display: "grid", placeItems: "center" }}>
                <div style={{ width: "88%", height: "88%", borderRadius: "50%", background: "white", display: "grid", placeItems: "center", textAlign: "center" }}>
                  <div><strong style={{ display: "block", fontSize: 48, letterSpacing: -2 }}>{minutes}:{seconds}</strong><span style={{ color: "#64748b" }}>remaining</span></div>
                </div>
              </div>
              <div style={{ display: "flex", gap: 10, marginTop: 20 }}>
                <button className="secondary-button" onClick={() => setRunning((value) => !value)}>{running ? "Pause" : "Resume"}</button>
                <button className="primary-button" onClick={finish}><Check size={17} /> Finish session</button>
              </div>
            </div>
          </>
        )}

        {completed && (
          <div style={{ background: "#f8fafc", borderRadius: 18, padding: 24, marginBottom: 22 }}>
            <strong style={{ fontSize: 28 }}>{Math.max(1, Math.round((totalSeconds - secondsLeft) / 60))} min focused</strong>
            <p style={{ color: "#64748b", marginBottom: 0 }}>Goal: {goal.trim() || "General learning"}</p>
          </div>
        )}

        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
            <div><strong>Suggested focus path</strong><div style={{ color: "#64748b", fontSize: 14 }}>Keep the session intentional instead of scrolling endlessly.</div></div>
            <span className="type-pill">{path.length} items</span>
          </div>
          {path.length ? path.map((item, index) => (
            <div key={item.id} style={{ display: "flex", gap: 14, alignItems: "center", padding: "13px 0", borderTop: "1px solid #e5e7eb" }}>
              <div style={{ width: 32, height: 32, borderRadius: 10, background: "#eef2ff", display: "grid", placeItems: "center", fontWeight: 800 }}>{index + 1}</div>
              <div style={{ flex: 1, minWidth: 0 }}><strong style={{ display: "block" }}>{item.title}</strong><span style={{ color: "#64748b", fontSize: 13 }}>{normalizeContentType(item)} • {item.category || "General"}</span></div>
            </div>
          )) : (
            <div className="empty-card"><Sparkles size={26} /><h3>Your path will appear here</h3><p>Once content is available, FocusFeed will place your most relevant items here.</p></div>
          )}
        </div>

        {completed && <button className="primary-button" onClick={finish} style={{ width: "100%", marginTop: 22 }}>Done</button>}
      </section>
    </div>
  );
}

/* =========================================================
   MAIN APP
========================================================= */

function App() {
  const [authenticated, setAuthenticated] = useState(() => {
    return Boolean(localStorage.getItem("focusfeed_user_id"));
  });

  const [setupComplete, setSetupComplete] =
    useState(() => {
      const storedUserId = Number(
        localStorage.getItem("focusfeed_user_id")
      );

      return (
        storedUserId > 0 &&
        localStorage.getItem(
          `focusfeed_setup_complete_${storedUserId}`
        ) === "true"
      );
    });

  const userId = Number(
    localStorage.getItem("focusfeed_user_id")
  );

  const [page, setPage] = useState("home");
  const [drawerOpen, setDrawerOpen] =
    useState(false);

  const [recommendations, setRecommendations] =
    useState([]);

  const [contentFeeds, setContentFeeds] = useState({
    blogs: [],
    videos: [],
    shorts: [],
  });

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [profileStats, setProfileStats] = useState(null);
  const [profileLoading, setProfileLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchError, setSearchError] = useState("");
  const [editingProfile, setEditingProfile] = useState(false);

  const currentUser = (() => {
    try {
      return JSON.parse(localStorage.getItem("focusfeed_user") || "null");
    } catch {
      return null;
    }
  })();

  const [selectedArticle, setSelectedArticle] =
    useState(null);

  const [interactionId, setInteractionId] =
    useState(null);

  const [readTime, setReadTime] =
    useState(0);

  const [scrollDepth, setScrollDepth] =
    useState(0);

  const [likedItems, setLikedItems] =
    useState(() => {
      try {
        return JSON.parse(
          localStorage.getItem(
            `focusfeed_liked_${userId}`
          ) || "{}"
        );
      } catch {
        return {};
      }
    });

  const [savedItems, setSavedItems] =
    useState(() => {
      try {
        return JSON.parse(
          localStorage.getItem(
            `focusfeed_saved_${userId}`
          ) || "{}"
        );
      } catch {
        return {};
      }
    });

  const [history, setHistory] =
    useState(() => {
      try {
        return JSON.parse(
          localStorage.getItem(
            `focusfeed_history_${userId}`
          ) || "[]"
        );
      } catch {
        return [];
      }
    });

  const [liked, setLiked] =
    useState(false);

  const [saved, setSaved] =
    useState(false);

  const [shared, setShared] =
    useState(false);

  const [focusOpen, setFocusOpen] = useState(false);
  const [focusDuration, setFocusDuration] = useState(20);
  const [focusSessionsLocal, setFocusSessionsLocal] = useState(() => {
    try { return Number(localStorage.getItem(`focusfeed_sessions_${userId}`) || 0); } catch { return 0; }
  });

  /* -------------------------------------------------------
     Fetch recommendations
  ------------------------------------------------------- */

  const fetchRecommendations =
    async () => {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(
          `${API}/recommend/${userId}`
        );

        if (!response.ok) {
          throw new Error(
            "Failed to fetch recommendations"
          );
        }

        const data =
          await response.json();

        setRecommendations(
          Array.isArray(data)
            ? data
            : []
        );
      } catch (err) {
        console.error(err);

        setError(
          "Unable to load recommendations."
        );
      } finally {
        setLoading(false);
      }
    };

  const fetchContentFeed = async (contentType) => {
    try {
      const response = await fetch(
        `${API}/content/feed?content_type=${encodeURIComponent(contentType)}&limit=24`
      );

      if (!response.ok) {
        throw new Error(`Failed to load ${contentType} feed`);
      }

      const data = await response.json();
      return Array.isArray(data) ? data : [];
    } catch (err) {
      console.error(`${contentType} feed error:`, err);
      return [];
    }
  };

  const fetchContentFeeds = async () => {
    const [blogs, videos, shorts] = await Promise.all([
      fetchContentFeed("blog"),
      fetchContentFeed("video"),
      fetchContentFeed("short"),
    ]);

    setContentFeeds({ blogs, videos, shorts });
  };

  const loadProfile = async () => {
    if (!userId) return;
    try {
      setProfileLoading(true);
      const response = await fetch(`${API}/profile/${userId}`);
      if (!response.ok) throw new Error("Failed to load profile");
      const data = await response.json();
      setProfileStats(data);
      if (Array.isArray(data.liked_ids)) {
        const next = {};
        data.liked_ids.forEach((id) => { next[id] = true; });
        setLikedItems(next);
      }
      if (Array.isArray(data.saved_ids)) {
        const next = {};
        data.saved_ids.forEach((id) => { next[id] = true; });
        setSavedItems(next);
      }
      if (Array.isArray(data.history)) setHistory(data.history);
    } catch (err) {
      console.error("Profile load error:", err);
    } finally {
      setProfileLoading(false);
    }
  };

  const performSearch = async (query) => {
    const value = String(query || "").trim();
    if (!value) return;
    setSearchQuery(value);
    if (!setupComplete && userId > 0) {
      localStorage.setItem(`focusfeed_setup_complete_${userId}`, "true");
      setSetupComplete(true);
    }
    setPage("search");
    setSearchLoading(true);
    setSearchError("");
    try {
      const response = await fetch(`${API}/search?query=${encodeURIComponent(value)}`);
      const data = await response.json().catch(() => []);
      if (!response.ok) throw new Error(data.detail || "Search failed");
      setSearchResults(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Search error:", err);
      setSearchResults([]);
      setSearchError(err.message || "Search failed");
    } finally {
      setSearchLoading(false);
    }
  };

  useEffect(() => {
    if (authenticated && setupComplete && userId > 0) {
      fetchRecommendations();
      fetchContentFeeds();
      loadProfile();
    }
  }, [authenticated, setupComplete, userId]);

  /* -------------------------------------------------------
     Persistence
  ------------------------------------------------------- */

  useEffect(() => {
    localStorage.setItem(
      `focusfeed_liked_${userId}`,
      JSON.stringify(likedItems)
    );
  }, [likedItems]);

  useEffect(() => {
    localStorage.setItem(
      `focusfeed_saved_${userId}`,
      JSON.stringify(savedItems)
    );
  }, [savedItems]);

  useEffect(() => {
    localStorage.setItem(
      `focusfeed_history_${userId}`,
      JSON.stringify(history)
    );
  }, [history]);

  /* -------------------------------------------------------
     Click interaction
  ------------------------------------------------------- */

  const trackClick = async (
    contentId
  ) => {
    try {
      const response = await fetch(
        `${API}/interaction`,
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            user_id: userId,
            content_id: contentId,
            clicked: true,
            liked: false,
            saved: false,
            shared: false,
            watch_time: 0,
            read_time: 0,
            scroll_depth: 0,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          "Failed to save click"
        );
      }

      const data =
        await response.json();

      return data.interaction_id;
    } catch (err) {
      console.error(
        "Click tracking error:",
        err
      );

      return null;
    }
  };

  /* -------------------------------------------------------
     Update interaction
  ------------------------------------------------------- */

  const updateInteraction =
    async ({
      interaction = interactionId,
      likedValue = liked,
      savedValue = saved,
      sharedValue = shared,
      readTimeValue = readTime,
      scrollDepthValue = scrollDepth,
    } = {}) => {
      if (!interaction) return;

      try {
        const params =
          new URLSearchParams({
            watch_time: String(
              readTimeValue
            ),
            read_time: String(
              readTimeValue
            ),
            scroll_depth: String(
              scrollDepthValue
            ),
            liked: String(
              likedValue
            ),
            saved: String(
              savedValue
            ),
            shared: String(
              sharedValue
            ),
          });

        await fetch(
          `${API}/interaction/${interaction}?${params}`,
          {
            method: "PUT",
          }
        );
      } catch (err) {
        console.error(
          "Interaction update error:",
          err
        );
      }
    };

  /* -------------------------------------------------------
     Open article
  ------------------------------------------------------- */

  const openArticle =
    async (contentId) => {
      try {
        const newInteractionId =
          await trackClick(
            contentId
          );

        if (!newInteractionId) {
          throw new Error(
            "Interaction could not be created"
          );
        }

        const response =
          await fetch(
            `${API}/content/${contentId}`
          );

        if (!response.ok) {
          throw new Error(
            "Failed to load article"
          );
        }

        const article =
          await response.json();

        setInteractionId(
          newInteractionId
        );

        setSelectedArticle(
          article
        );

        setLiked(
          Boolean(
            likedItems[contentId]
          )
        );

        setSaved(
          Boolean(
            savedItems[contentId]
          )
        );

        setShared(false);
        setReadTime(0);
        setScrollDepth(0);

        setHistory((previous) => {
          const withoutDuplicate =
            previous.filter(
              (item) =>
                item.id !== article.id
            );

          return [
            article,
            ...withoutDuplicate,
          ].slice(0, 30);
        });

        window.scrollTo({
          top: 0,
          behavior: "instant",
        });
      } catch (err) {
        console.error(
          "Article error:",
          err
        );

        setError(
          "Unable to load article."
        );
      }
    };

  /* -------------------------------------------------------
     Reading timer
  ------------------------------------------------------- */

  useEffect(() => {
    if (!selectedArticle) return;

    const timer =
      setInterval(() => {
        setReadTime(
          (previous) =>
            previous + 1
        );
      }, 1000);

    return () =>
      clearInterval(timer);
  }, [selectedArticle]);

  /* -------------------------------------------------------
     Scroll tracking
  ------------------------------------------------------- */

  useEffect(() => {
    if (!selectedArticle) return;

    const handleScroll =
      () => {
        const scrollTop =
          window.scrollY;

        const documentHeight =
          document.documentElement
            .scrollHeight;

        const windowHeight =
          window.innerHeight;

        const scrollable =
          documentHeight -
          windowHeight;

        if (scrollable <= 0) {
          setScrollDepth(100);
          return;
        }

        const percentage =
          (scrollTop /
            scrollable) *
          100;

        setScrollDepth(
          (previous) =>
            Math.max(
              previous,
              Math.min(
                100,
                Math.round(
                  percentage
                )
              )
            )
        );
      };

    window.addEventListener(
      "scroll",
      handleScroll
    );

    return () =>
      window.removeEventListener(
        "scroll",
        handleScroll
      );
  }, [selectedArticle]);

  /* -------------------------------------------------------
     Like
  ------------------------------------------------------- */

  const toggleSave = async (contentId) => {
  const newValue = !savedItems[contentId];

  try {
    // If this article is already open, update its interaction
    if (
      selectedArticle?.id === contentId &&
      interactionId
    ) {
      await updateInteraction({
        interaction: interactionId,
        savedValue: newValue,
      });
    } else {
      // Create a new interaction for card-level Save
      const response = await fetch(
        `${API}/interaction`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_id: userId,
            content_id: contentId,
            clicked: false,
            liked: false,
            saved: newValue,
            shared: false,
            watch_time: 0,
            read_time: 0,
            scroll_depth: 0,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to save interaction");
      }
    }

    setSavedItems((previous) => ({
      ...previous,
      [contentId]: newValue,
    }));

    if (selectedArticle?.id === contentId) {
      setSaved(newValue);
    }

    await loadProfile();

  } catch (error) {
    console.error("Save interaction error:", error);
  }
};


const toggleLike = async (contentId) => {
  const newValue = !likedItems[contentId];

  try {
    // If article is currently open
    if (
      selectedArticle?.id === contentId &&
      interactionId
    ) {
      await updateInteraction({
        interaction: interactionId,
        likedValue: newValue,
      });
    } else {
      // Create interaction for card-level Like
      const response = await fetch(
        `${API}/interaction`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_id: userId,
            content_id: contentId,
            clicked: false,
            liked: newValue,
            saved: false,
            shared: false,
            watch_time: 0,
            read_time: 0,
            scroll_depth: 0,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to save interaction");
      }
    }

    setLikedItems((previous) => ({
      ...previous,
      [contentId]: newValue,
    }));

    if (selectedArticle?.id === contentId) {
      setLiked(newValue);
    }

    await loadProfile();

  } catch (error) {
    console.error("Like interaction error:", error);
  }
};


const handleArticleLike = async () => {
  if (!selectedArticle) {
    return;
  }

  const newValue = !liked;

  try {
    if (!interactionId) {
      console.error("No interaction ID for article");
      return;
    }

    await updateInteraction({
      interaction: interactionId,
      likedValue: newValue,
    });

    setLiked(newValue);

    setLikedItems((previous) => ({
      ...previous,
      [selectedArticle.id]: newValue,
    }));

    await loadProfile();

  } catch (error) {
    console.error("Article like error:", error);
  }
};

  const handleArticleSave =
    async () => {
      const newValue = !saved;

      setSaved(newValue);

      if (selectedArticle) {
        setSavedItems(
          (previous) => ({
            ...previous,
            [selectedArticle.id]:
              newValue,
          })
        );
      }

      await updateInteraction({
        savedValue: newValue,
      });
    };

  /* -------------------------------------------------------
     Share
  ------------------------------------------------------- */

  const handleShare =
    async () => {
      try {
        if (!selectedArticle) return;

        const shareUrl =
          window.location.href;

        if (
          navigator.share
        ) {
          await navigator.share({
            title:
              selectedArticle.title,
            text:
              selectedArticle.description ||
              selectedArticle.title,
            url: shareUrl,
          });
        } else {
          await navigator.clipboard.writeText(
            shareUrl
          );

          alert(
            "Article link copied!"
          );
        }

        setShared(true);

        await updateInteraction({
          sharedValue: true,
        });
      } catch (err) {
        if (
          err?.name !==
          "AbortError"
        ) {
          console.error(
            "Share error:",
            err
          );
        }
      }
    };

  /* -------------------------------------------------------
     Close article
  ------------------------------------------------------- */

  const closeArticle =
    async () => {
      await updateInteraction({
        likedValue: liked,
        savedValue: saved,
        sharedValue: shared,
        readTimeValue:
          readTime,
        scrollDepthValue:
          scrollDepth,
      });

      setSelectedArticle(null);
      setInteractionId(null);
      setReadTime(0);
      setScrollDepth(0);
      setLiked(false);
      setSaved(false);
      setShared(false);

      window.scrollTo({
        top: 0,
        behavior: "instant",
      });

      fetchRecommendations();
      loadProfile();
    };

  /* -------------------------------------------------------
     Setup completion
  ------------------------------------------------------- */

  const finishSetup =
    (duration = 20) => {
      localStorage.setItem(
        `focusfeed_setup_complete_${userId}`,
        "true"
      );

      setFocusDuration(Number(duration) || 20);
      setSetupComplete(true);
      setPage("home");
      setFocusOpen(true);
    };

  const completeFocusSession = async ({ durationMinutes, elapsedSeconds, goal, completed }) => {
    // The backend is now the source of truth for completed focus sessions.
    console.info("Focus session completed", { durationMinutes, elapsedSeconds, goal, completed });
    await loadProfile();
  };

  /* -------------------------------------------------------
     Authentication screen
  ------------------------------------------------------- */

  if (!authenticated || userId <= 0) {
    return (
      <AuthPage
        onAuthenticated={() => {
          setAuthenticated(true);
          setSetupComplete(
            localStorage.getItem(`focusfeed_setup_complete_${Number(localStorage.getItem("focusfeed_user_id"))}`) === "true"
          );
        }}
      />
    );
  }

  /* -------------------------------------------------------
     Setup screen
  ------------------------------------------------------- */

  if (!setupComplete) {
    return (
      <SetupPage
        onContinue={finishSetup}
        onSearch={performSearch}
      />
    );
  }

  /* -------------------------------------------------------
     Article detail
  ------------------------------------------------------- */

  if (selectedArticle) {
    return (
      <ArticleDetail
        article={selectedArticle}
        liked={liked}
        saved={saved}
        shared={shared}
        onLike={handleArticleLike}
        onSave={handleArticleSave}
        onShare={handleShare}
        onClose={closeArticle}
        readTime={readTime}
        scrollDepth={scrollDepth}
      />
    );
  }

  /* -------------------------------------------------------
     Main page
  ------------------------------------------------------- */

  const renderPage =
    () => {
      switch (page) {
        case "search":
          return (
            <SearchPage
              query={searchQuery}
              results={searchResults}
              loading={searchLoading}
              error={searchError}
              onOpenArticle={openArticle}
              likedItems={likedItems}
              savedItems={savedItems}
              toggleLike={toggleLike}
              toggleSave={toggleSave}
            />
          );

        case "explore":
          return (
            <ExplorePage
              setPage={setPage}
              onSearch={performSearch}
            />
          );

        case "blogs":
          return (
            <BlogsPage
              recommendations={
                contentFeeds.blogs
              }
              onOpenArticle={
                openArticle
              }
              savedItems={
                savedItems
              }
              likedItems={
                likedItems
              }
              toggleSave={
                toggleSave
              }
              toggleLike={
                toggleLike
              }
            />
          );

        case "videos":
          return (
            <VideosPage
              recommendations={
                contentFeeds.videos
              }
              onOpenArticle={
                openArticle
              }
              savedItems={
                savedItems
              }
              likedItems={
                likedItems
              }
              toggleSave={
                toggleSave
              }
              toggleLike={
                toggleLike
              }
            />
          );

        case "shorts":
          return (
            <ShortsPage
              recommendations={
                contentFeeds.shorts
              }
              onOpenArticle={
                openArticle
              }
            />
          );

        case "saved":
          return (
            <SavedPage
              recommendations={
                recommendations
              }
              savedItems={
                savedItems
              }
              savedContent={profileStats?.saved || []}
              onOpenArticle={
                openArticle
              }
            />
          );

        case "history":
          return (
            <HistoryPage
              history={history}
              likedItems={
                likedItems
              }
              savedItems={
                savedItems
              }
              onOpenArticle={
                openArticle
              }
            />
          );

        case "settings":
          return <SettingsPage />;

        case "profile":
          return (
            <ProfilePage
              user={currentUser}
              stats={profileStats}
              loading={profileLoading}
              onEdit={() => {
                const nextName = window.prompt("Enter your name", currentUser?.name || "");
                if (nextName && nextName.trim()) {
                  fetch(`${API}/profile/${userId}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name: nextName.trim() }),
                  })
                    .then(async (response) => {
                      const data = await response.json();
                      if (!response.ok) throw new Error(data.detail || "Profile update failed");
                      localStorage.setItem("focusfeed_user", JSON.stringify(data));
                      setProfileStats((previous) => ({ ...previous, name: data.name, email: data.email }));
                    })
                    .catch((err) => alert(err.message));
                }
              }}
              onLogout={() => {
                localStorage.removeItem("focusfeed_user_id");
                localStorage.removeItem("focusfeed_user");
                localStorage.removeItem(
                  `focusfeed_setup_complete_${userId}`
                );
                setAuthenticated(false);
                setSetupComplete(false);
                setPage("home");
              }}
            />
          );

        case "home":
        default:
          return (
            <HomePage
              recommendations={
                recommendations
              }
              loading={loading}
              error={error}
              onOpenArticle={
                openArticle
              }
              likedItems={
                likedItems
              }
              savedItems={
                savedItems
              }
              toggleLike={
                toggleLike
              }
              toggleSave={
                toggleSave
              }
              setPage={setPage}
            />
          );
      }
    };

  return (
    <>
      {focusOpen && (
        <FocusSession
          userId={userId}
          duration={focusDuration}
          recommendations={recommendations}
          onClose={() => setFocusOpen(false)}
          onComplete={completeFocusSession}
        />
      )}
      <div className="app-shell">
      <AppHeader
        onMenu={() => setDrawerOpen(true)}
        onProfile={() => setPage("profile")}
        onSearch={performSearch}
        userName={currentUser?.name}
      />

      <SideDrawer
        open={drawerOpen}
        page={page}
        setPage={setPage}
        onClose={() =>
          setDrawerOpen(false)
        }
      />

      <div className="app-main">
        {renderPage()}
      </div>

      <BottomNav
        page={page}
        setPage={setPage}
      />
      </div>
    </>
  );
}

export default App;