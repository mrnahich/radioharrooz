(() => {
  const STREAM_URL = "https://streams.radio.co/s163d89567/listen";

  const cabinet = document.getElementById("cabinet");
  const playBtn = document.getElementById("playBtn");
  const audio = document.getElementById("stream");
  const statusText = document.getElementById("statusText");

  if (!cabinet || !playBtn || !audio) return; // podcast page has no player

  let userWantsPlay = false;

  function setState(state, label) {
    cabinet.dataset.state = state;
    if (label) statusText.textContent = label;
    playBtn.setAttribute(
      "aria-label",
      state === "playing" ? "Pause live radio" : "Play live radio"
    );
  }

  function connect() {
    setState("connecting", "Tuning in…");
    // fresh src each time so we always join the live edge of the stream
    audio.src = STREAM_URL + "?_=" + Date.now();
    audio.load();
    const playPromise = audio.play();
    if (playPromise && playPromise.catch) {
      playPromise.catch(() => {
        setState("paused", "Couldn't connect — tap to retry");
        userWantsPlay = false;
      });
    }
  }

  function disconnect() {
    userWantsPlay = false;
    audio.pause();
    audio.removeAttribute("src");
    audio.load();
    setState("paused", "Off air");
  }

  playBtn.addEventListener("click", () => {
    if (cabinet.dataset.state === "playing" || cabinet.dataset.state === "connecting") {
      disconnect();
    } else {
      userWantsPlay = true;
      connect();
    }
  });

  audio.addEventListener("playing", () => {
    if (userWantsPlay) setState("playing", "On air");
  });

  audio.addEventListener("waiting", () => {
    if (userWantsPlay) setState("connecting", "Buffering…");
  });

  audio.addEventListener("stalled", () => {
    if (userWantsPlay) setState("connecting", "Reconnecting…");
  });

  audio.addEventListener("error", () => {
    if (userWantsPlay) {
      setState("paused", "Connection lost — tap to retry");
      userWantsPlay = false;
    }
  });

  // pause playback if the tab is hidden for a long time isn't necessary for a
  // live stream — intentionally left running so audio continues in background.

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("service-worker.js").catch(() => {});
    });
  }
})();
