# ✅ User Test Plan – *YT Summarizer IA*

**Version**: V1  
**Date**: 2025-05-08  
**Objective**: Validate the correct display and behavior of the user interface elements, functionality of the summarization process, and response rendering.

---

## 📌 1. SUBMISSION FORM

| Test ID | Test Description                      | Steps                          | Expected Result                                              |
|---------|---------------------------------------|--------------------------------|--------------------------------------------------------------|
| T1.1    | YouTube link input is visible         | Load the page                  | Input field for YouTube video is displayed                  |
| T1.2    | IA engine selection is available      | Check radio buttons            | “Ollama” and “OpenAI” options are selectable                |
| T1.3    | API fields toggle with OpenAI         | Select OpenAI engine           | Two input fields appear: API URL and API Key                |
| T1.4    | Language input accepts custom value   | Use dropdown or type custom    | Custom value accepted without rejection                     |
| T1.5    | Detail level selector has 3 options   | Open the detail dropdown       | Options: short, medium, detailed                            |
| T1.6    | Summary type selector has 3 options   | Open the type dropdown         | Options: full, tools & methods, key learnings              |
| T1.7    | Submit button is present              | Load the form                  | “Go for summary” button is visible and active               |

---

## ⌛ 2. LOADING INDICATORS

| Test ID | Test Description                          | Steps            | Expected Result                                                           |
|---------|-------------------------------------------|------------------|---------------------------------------------------------------------------|
| T2.1    | Loader displays on summary start          | Click on submit  | Hourglass + “Generating summary...” + animated dots appear               |
| T2.2    | Loader disappears on completion           | Wait for response| Loading animation is hidden once summary is displayed                    |

---

## 📋 3. RESULT DISPLAY

| Test ID | Test Description                       | Steps                       | Expected Result                                                  |
|---------|----------------------------------------|-----------------------------|------------------------------------------------------------------|
| T3.1    | Summary appears in dedicated block     | Submit valid request        | Summary is displayed inside result container                    |
| T3.2    | Summary is in correct language         | Select “fr” then generate   | Summary is written in French                                    |
| T3.3    | Summary respects detail level          | Choose short/medium/detailed| Output length matches selected detail level                     |
| T3.4    | Summary matches selected type          | Choose tools/insights/full  | Summary content reflects the type of request                    |

---

## 🛠️ 4. SUMMARY ACTIONS

| Test ID | Test Description                 | Steps                      | Expected Result                                                                |
|---------|----------------------------------|----------------------------|--------------------------------------------------------------------------------|
| T4.1    | Action buttons display properly  | After generating a summary | 📥 Download and 📋 Copy buttons appear below the summary                       |
| T4.2    | Download summary as text         | Click 📥 Download button   | The summary is downloaded as `summary.txt` file                                |
| T4.3    | Copy summary to clipboard        | Click 📋 Copy button       | Summary is copied and “Copied!” feedback is shown                              |
| T4.4    | Copy feedback disappears         | Wait 2 seconds after copy  | “Copied!” message disappears automatically after 2 seconds                     |

---

## 🧾 5. UI VISIBILITY & BEHAVIOR

| Test ID | Test Description                          | Steps                            | Expected Result                                                  |
|---------|-------------------------------------------|----------------------------------|------------------------------------------------------------------|
| T5.1    | Summary block hidden on initial load      | Load the page                    | Summary block is not visible                                    |
| T5.2    | Summary block visible after generation    | Submit request                   | Summary container appears with content                          |
| T5.3    | API fields toggle with engine change      | Switch between Ollama ↔ OpenAI   | API URL and Key fields show/hide dynamically                    |
