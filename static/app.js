// ===== Configuration =====
const API = "";  // same origin, no prefix needed

// ===== State =====
let token = localStorage.getItem("token");
let userId = localStorage.getItem("userId");
let username = localStorage.getItem("username");

// ===== On Page Load =====
document.addEventListener("DOMContentLoaded", () => {
    if (token) {
        showApp();
    }
});

// ===== Auth: Tab Switching =====
function showTab(tab) {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    if (tab === "login") {
        document.getElementById("login-form").style.display = "block";
        document.getElementById("register-form").style.display = "none";
        document.querySelectorAll(".tab")[0].classList.add("active");
    } else {
        document.getElementById("login-form").style.display = "none";
        document.getElementById("register-form").style.display = "block";
        document.querySelectorAll(".tab")[1].classList.add("active");
    }
    // Clear messages
    document.querySelectorAll(".error, .success").forEach(el => el.textContent = "");
}

// ===== Auth: Register =====
async function handleRegister(e) {
    e.preventDefault();
    const user = document.getElementById("reg-username").value.trim();
    const pass = document.getElementById("reg-password").value;
    const errorEl = document.getElementById("reg-error");
    const successEl = document.getElementById("reg-success");
    errorEl.textContent = "";
    successEl.textContent = "";

    try {
        const res = await fetch(API + "/users/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: user, password: pass }),
        });
        if (!res.ok) {
            const data = await res.json();
            errorEl.textContent = data.detail || "Registration failed";
            return;
        }
        successEl.textContent = "Account created! You can now login.";
        document.getElementById("reg-username").value = "";
        document.getElementById("reg-password").value = "";
    } catch (err) {
        errorEl.textContent = "Network error";
    }
}

// ===== Auth: Login =====
async function handleLogin(e) {
    e.preventDefault();
    const user = document.getElementById("login-username").value.trim();
    const pass = document.getElementById("login-password").value;
    const errorEl = document.getElementById("login-error");
    errorEl.textContent = "";

    try {
        const res = await fetch(API + "/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: user, password: pass }),
        });
        if (!res.ok) {
            const data = await res.json();
            errorEl.textContent = data.detail || "Login failed";
            return;
        }
        const data = await res.json();
        token = data.access_token;
        userId = data.user_id;
        username = user;
        localStorage.setItem("token", token);
        localStorage.setItem("userId", userId);
        localStorage.setItem("username", username);
        showApp();
    } catch (err) {
        errorEl.textContent = "Network error";
    }
}

// ===== Auth: Logout =====
function logout() {
    token = null;
    userId = null;
    username = null;
    localStorage.removeItem("token");
    localStorage.removeItem("userId");
    localStorage.removeItem("username");
    document.getElementById("auth-section").style.display = "block";
    document.getElementById("posts-section").style.display = "none";
    document.getElementById("logout-btn").style.display = "none";
    document.getElementById("greeting").textContent = "";
    // Clear form inputs
    document.getElementById("login-username").value = "";
    document.getElementById("login-password").value = "";
}

// ===== Show Main App =====
function showApp() {
    document.getElementById("auth-section").style.display = "none";
    document.getElementById("posts-section").style.display = "block";
    document.getElementById("logout-btn").style.display = "inline-block";
    document.getElementById("greeting").textContent = "Hi, " + username;
    loadPosts();
}

// ===== Posts: Load All =====
async function loadPosts() {
    const feed = document.getElementById("posts-feed");
    feed.innerHTML = "<p style='color:#6b7280'>Loading...</p>";

    try {
        const res = await fetch(API + "/posts/");
        if (!res.ok) throw new Error();
        const posts = await res.json();

        if (posts.length === 0) {
            feed.innerHTML = "<p style='color:#6b7280'>No posts yet. Be the first!</p>";
            return;
        }

        // Sort newest first (uuid7 is time-sorted, so string compare works)
        posts.sort((a, b) => b.id.localeCompare(a.id));

        feed.innerHTML = posts.map(post => postHTML(post)).join("");
    } catch (err) {
        feed.innerHTML = "<p class='error'>Failed to load posts</p>";
    }
}

// ===== Posts: Render One =====
function postHTML(post) {
    const isOwner = post.owner_id === userId;
    const date = new Date(post.created_at).toLocaleString();
    return `
        <div class="post-card" id="post-${post.id}">
            <h3>${escapeHtml(post.title)}</h3>
            <p>${escapeHtml(post.content)}</p>
            <div class="post-meta">${date}</div>
            ${isOwner ? `
                <div class="post-actions">
                    <button class="btn btn-small btn-outline" onclick="startEdit('${post.id}')">Edit</button>
                    <button class="btn btn-small btn-danger" onclick="deletePost('${post.id}')">Delete</button>
                </div>
            ` : ""}
        </div>
    `;
}

// ===== Posts: Create =====
async function handleCreatePost(e) {
    e.preventDefault();
    const title = document.getElementById("post-title").value.trim();
    const content = document.getElementById("post-content").value.trim();
    const errorEl = document.getElementById("post-error");
    errorEl.textContent = "";

    try {
        const res = await fetch(API + "/posts/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            },
            body: JSON.stringify({ title, content }),
        });
        if (!res.ok) {
            const data = await res.json();
            errorEl.textContent = data.detail || "Failed to create post";
            return;
        }
        document.getElementById("post-title").value = "";
        document.getElementById("post-content").value = "";
        loadPosts();
    } catch (err) {
        errorEl.textContent = "Network error";
    }
}

// ===== Posts: Delete =====
async function deletePost(id) {
    if (!confirm("Delete this post?")) return;
    try {
        const res = await fetch(API + "/posts/" + id, {
            method: "DELETE",
            headers: { "Authorization": "Bearer " + token },
        });
        if (!res.ok) {
            alert("Failed to delete post");
            return;
        }
        loadPosts();
    } catch (err) {
        alert("Network error");
    }
}

// ===== Posts: Edit =====
function startEdit(id) {
    const card = document.getElementById("post-" + id);
    const title = card.querySelector("h3").textContent;
    const content = card.querySelector("p").textContent;

    // Replace card content with edit form
    card.innerHTML = `
        <form class="edit-form" onsubmit="submitEdit(event, '${id}')">
            <input type="text" id="edit-title-${id}" value="${escapeAttr(title)}" required>
            <textarea id="edit-content-${id}" required>${escapeHtml(content)}</textarea>
            <div class="post-actions">
                <button type="submit" class="btn btn-small">Save</button>
                <button type="button" class="btn btn-small btn-outline" onclick="loadPosts()">Cancel</button>
            </div>
            <p id="edit-error-${id}" class="error"></p>
        </form>
    `;
}

async function submitEdit(e, id) {
    e.preventDefault();
    const title = document.getElementById("edit-title-" + id).value.trim();
    const content = document.getElementById("edit-content-" + id).value.trim();
    const errorEl = document.getElementById("edit-error-" + id);
    errorEl.textContent = "";

    try {
        const res = await fetch(API + "/posts/" + id, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            },
            body: JSON.stringify({ title, content }),
        });
        if (!res.ok) {
            const data = await res.json();
            errorEl.textContent = data.detail || "Failed to update post";
            return;
        }
        loadPosts();
    } catch (err) {
        errorEl.textContent = "Network error";
    }
}

// ===== Utilities =====
function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

function escapeAttr(str) {
    return str.replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}
