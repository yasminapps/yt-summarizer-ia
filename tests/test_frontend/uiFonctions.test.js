// tests/test_frontend/uiFunctions.test.js

/**
 * @jest-environment jsdom
 */

const fs = require("fs");
const path = require("path");

describe("Frontend UI Functions", () => {
  let html;

  beforeEach(() => {
    html = fs.readFileSync(path.resolve(__dirname, "../../templates/index.html"), "utf8");
    document.documentElement.innerHTML = html.toString();
    require("../../static/script.js");
  });

  test("formatSecondsToMinutes formats seconds correctly", () => {
    const result = window.formatSecondsToMinutes(125);
    expect(result).toBe("2m 5s");
  });

  test("startLoadingAnimation starts dot animation", () => {
    window.startLoadingAnimation();
    const loading = document.getElementById("loading-animation");
    expect(loading.style.display).toBe("flex");
  });

  test("stopLoadingAnimation stops dot animation", () => {
    window.startLoadingAnimation();
    window.stopLoadingAnimation();
    const loading = document.getElementById("loading-animation");
    expect(loading.style.display).toBe("none");
  });

  test("downloadSummary triggers download", () => {
    const el = document.getElementById("summary-result");
    el.innerText = "Test Summary";
    const createObjectURL = jest.fn();
    global.URL.createObjectURL = createObjectURL;
    const click = jest.fn();
    document.createElement = jest.fn(() => ({ click, set href(v) {}, set download(v) {} }));

    window.downloadSummary();
    expect(click).toHaveBeenCalled();
  });

  test("copySummary copies to clipboard", async () => {
    const writeText = jest.fn().mockResolvedValue();
    global.navigator.clipboard = { writeText };
    const el = document.getElementById("summary-result");
    el.innerText = "Copied summary";

    await window.copySummary();
    expect(writeText).toHaveBeenCalledWith("Copied summary");
  });
});
