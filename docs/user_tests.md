# ✅ User Test Plan – *YouTube Transcript & Summary Generator*

**Version**: V2  
**Date**: 2025-05-08  
**Objective**: Validate all core user interactions including transcript extraction, summary generation, dynamic UI behavior, and user actions.

---

## 📌 1. SUBMISSION FORM

| Test ID | Description                            | Steps                            | Expected Result                                          |
|--------|----------------------------------------|----------------------------------|----------------------------------------------------------|
| T1.1   | YouTube link input is visible          | Load the page                    | Input field for YouTube video is displayed               |
| T1.2   | IA engine selection options work        | View radio buttons               | Options: “Ollama”, “OpenAI – User”, “OpenAI – Default”   |
| T1.3   | API fields toggle with OpenAI-User      | Select OpenAI-User               | Input fields for API URL and Key appear                  |
| T1.4   | Language input supports typing          | Type language code manually      | Field accepts typed input (e.g. "fr")                    |
| T1.5   | Detail level has 3 values               | Open dropdown                    | Options: short, medium, detailed                         |
| T1.6   | Summary type has 3 values               | Open dropdown                    | Options: full, tools, insights                           |
| T1.7   | Summary style selector is visible       | Expand advanced options          | Options: text, bullet points, mixed                      |
| T1.8   | Emoji and Table toggles                 | Use advanced options             | Radios for "Add emojis", "Add tables" are functional     |
| T1.9   | Specific instructions field works       | Type into textarea               | Custom instructions are accepted                         |
| T1.10  | Submit buttons visible and enabled      | Load form                        | “Generate Summary” and “Generate Transcript” are active  |

---

## ⌛ 2. LOADING INDICATORS

| Test ID | Description                            | Steps                      | Expected Result                                            |
|--------|----------------------------------------|----------------------------|------------------------------------------------------------|
| T2.1   | Loader appears after submission         | Submit form                | Loading message and animated dots appear                   |
| T2.2   | Loader disappears after response        | Wait for result            | Loading UI is hidden after completion                      |


---

## 📋 3. RESULT DISPLAY

| Test ID | Description                            | Steps                              | Expected Result                                      |
|--------|----------------------------------------|------------------------------------|------------------------------------------------------|
| T3.1   | Summary block appears after success    | Submit valid summary request       | Summary is shown inside the result container         |
| T3.2   | Summary language matches input         | Select language, then submit       | Output is in selected language (e.g. French)         |
| T3.3   | Detail level respected                 | Select short/medium/detailed       | Summary length reflects choice                       |
| T3.4   | Summary type applied                   | Choose type                        | Output focuses on full content / tools / insights    |
| T3.5   | Styling options applied                | Set style, emojis, tables          | Summary reflects style (bullets, emojis, etc.)       |

---

## 🛠️ 4. SUMMARY ACTIONS

| Test ID | Description                            | Steps                         | Expected Result                                      |
|--------|----------------------------------------|-------------------------------|------------------------------------------------------|
| T4.1   | Copy summary button works              | Click 📋 Summary               | Text copied to clipboard                             |
| T4.2   | Copy feedback shows temporarily        | Click copy                    | “✅ Copied!” message shown, then disappears           |
| T4.3   | Download summary button works          | Click 📥 Summary               | File `summary.txt` is downloaded                     |
| T4.4   | Copy transcript buttons work           | Generate transcript           | Buttons appear and function as expected              |
| T4.5   | Download transcript buttons work       | Generate transcript           | Buttons appear and function as expected              |

---

## 🧾 5. UI BEHAVIOR

| Test ID | Description                            | Steps                              | Expected Result                                     |
|--------|----------------------------------------|------------------------------------|-----------------------------------------------------|
| T5.1   | Summary block hidden at first load     | Load page                          | No result section visible                           |
| T5.2   | Summary block appears after submit     | Submit form                        | Result block and action buttons appear              |
| T5.3   | Transcript-only mode works             | Click "Generate Transcript Only"   | Only transcript is displayed                        |
| T5.4   | Language is pre-filled from browser    | Open the form                      | Language field auto-filled (e.g. `fr`, `en`)        |
| T5.5   | Engine change hides API fields         | Switch from OpenAI-user to others  | API Key / URL fields are hidden                     |

---

## ✅ 6. EDGE CASES & ERRORS

| Test ID | Description                            | Steps                              | Expected Result                                     |
|--------|----------------------------------------|------------------------------------|-----------------------------------------------------|
| T6.1   | Empty URL shows error                   | Submit with no URL                 | Error message: "Invalid YouTube URL"                |
| T6.2   | Broken video shows fallback message     | Submit invalid URL                 | Error: "Transcript not available or error occurred" |
| T6.3   | Server failure returns 500              | Trigger exception (test mode)      | Error message: "Server-side error"                  |

---

## 📋 Test Completion Checklist

- [ ] All UI elements rendered correctly  
- [ ] Summary output matches settings  
- [ ] All buttons functional and responsive  
- [ ] Clipboard + download verified  
- [ ] Error handling shown when applicable  
- [ ] Language auto-detection validated  

---

**Tested on:** Chrome / Firefox / Safari – Desktop  
**Next step:** add visual screenshots and Selenium automation later if needed