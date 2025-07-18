document.addEventListener("DOMContentLoaded", () => {
    // Mobile menu toggle
    const menuToggle = document.getElementById("menuToggle")
    const sidebar = document.getElementById("sidebar")
  
    if (menuToggle && sidebar) {
      menuToggle.addEventListener("click", () => {
        sidebar.classList.toggle("active")
      })
    }
  
    // Dropdown menu functionality
    const dropdownToggles = document.querySelectorAll(".dropdown-toggle")
  
    dropdownToggles.forEach((toggle) => {
      toggle.addEventListener("click", function (e) {
        e.preventDefault()
        const parent = this.closest(".nav-item-dropdown")
  
        // Close other dropdowns at the same level
        const siblings = parent.parentElement.children
        Array.from(siblings).forEach((sibling) => {
          if (sibling !== parent && sibling.classList.contains("nav-item-dropdown")) {
            sibling.classList.remove("active")
          }
        })
  
        // Toggle current dropdown
        parent.classList.toggle("active")
      })
    })
  
    // Active link highlighting
    const currentPath = window.location.pathname
    const navLinks = document.querySelectorAll(".nav-link")
  
    navLinks.forEach((link) => {
      if (link.getAttribute("href") === currentPath) {
        link.classList.add("active")
  
        // Open parent dropdown if this is a nested link
        const parentDropdown = link.closest(".nav-item-dropdown")
        if (parentDropdown) {
          parentDropdown.classList.add("active")
  
          // Also open grandparent dropdown if exists
          const grandParentDropdown = parentDropdown.parentElement.closest(".nav-item-dropdown")
          if (grandParentDropdown) {
            grandParentDropdown.classList.add("active")
          }
        }
      }
    })
  
    // Close sidebar when clicking outside on mobile
    document.addEventListener("click", (e) => {
      if (window.innerWidth <= 768) {
        if (sidebar && !sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
          sidebar.classList.remove("active")
        }
      }
    })
  
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", function (e) {
        e.preventDefault()
        const target = document.querySelector(this.getAttribute("href"))
        if (target) {
          target.scrollIntoView({
            behavior: "smooth",
          })
        }
      })
    })
  
    // Progress animation
    const observerOptions = {
      threshold: 0.1,
      rootMargin: "0px 0px -50px 0px",
    }
  
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animate")
        }
      })
    }, observerOptions)
  
    document.querySelectorAll(".stat-card").forEach((card) => {
      observer.observe(card)
    })
  
    // Sidebar scroll position memory
    const sidebarScrollKey = "sidebar-scroll-position"
  
    if (sidebar) {
      // Restore scroll position
      const savedScrollPosition = localStorage.getItem(sidebarScrollKey)
      if (savedScrollPosition) {
        sidebar.scrollTop = Number.parseInt(savedScrollPosition)
      }
  
      // Save scroll position
      sidebar.addEventListener("scroll", () => {
        localStorage.setItem(sidebarScrollKey, sidebar.scrollTop.toString())
      })
    }
  })
  
  // Function to handle file uploads
  function handleFileUpload(input, previewContainer) {
    const file = input.files[0]
    if (file && file.type === "application/pdf") {
      const reader = new FileReader()
      reader.onload = (e) => {
        // Create preview or handle upload
        console.log("PDF file selected:", file.name)
      }
      reader.readAsDataURL(file)
    }
  }
  
  // Function to update progress
  function updateProgress(materialId, progressValue) {
    fetch(`/update-progress/${materialId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        progress: progressValue,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          // Update UI to reflect progress change
          console.log("Progress updated successfully")
          // Show success message
          showNotification("Jarayon muvaffaqiyatli yangilandi!", "success")
        }
      })
      .catch((error) => {
        console.error("Error updating progress:", error)
        showNotification("Xatolik yuz berdi!", "error")
      })
  }
  
  // Show notification function
  function showNotification(message, type = "info") {
    const notification = document.createElement("div")
    notification.className = `notification notification-${type}`
    notification.innerHTML = `
      <div class="notification-content">
        <span>${message}</span>
        <button class="notification-close">&times;</button>
      </div>
    `
  
    document.body.appendChild(notification)
  
    // Auto remove after 3 seconds
    setTimeout(() => {
      notification.remove()
    }, 3000)
  
    // Manual close
    notification.querySelector(".notification-close").addEventListener("click", () => {
      notification.remove()
    })
  }
  
  // Get CSRF token
  function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";")
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }
  