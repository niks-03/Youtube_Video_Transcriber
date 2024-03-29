function typeWriter(elementId, text, speed) {
    const targetElement = document.getElementById(elementId);
    if (!targetElement) return;
  
    let index = 0;
    const typing = () => {
      if (index < text.length) {
        targetElement.textContent += text.charAt(index);
        index++;
        setTimeout(typing, speed);
      }
    };
  
    typing();
  }
  
  // Call the function on page load
  window.onload = function() {
    typeWriter('heading', 'YOUTUBE TRANSCRIBER!', 100);
  };